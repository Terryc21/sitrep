---
name: plain-talk
description: 'Codebase analysis with A-F grades explained in plain language for non-technical stakeholders. Self-contained iOS/Swift audit. Triggers: "plain talk", "plain talk report card", "stakeholder report", "non-technical audit".'
version: 3.1.0
author: Terry Nyberg
license: MIT
allowed-tools: [Glob, Grep, Read, Write, AskUserQuestion]
metadata:
  tier: analysis
  category: analysis
---

# Plain-Talk Report Card Generator

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Generate a codebase report card with A-F grades explained in plain, non-technical language for project managers, executives, or non-developer stakeholders.

All findings use the **Issue Rating Table** format. Include a brief plain-language explanation above the table so non-technical readers understand what the columns mean.

---

## Step 1: Before Starting

📖 **Run the opening interview from `../shared/session-setup.md` § Opening interview.**
It defines the CLAUDE.md and Timeline questions (plus the timeline grading adjustment)
shared by all report-card skills.

**Focus question — specific to this skill.** Use this as the third question:

```
  {
    "question": "Any areas to emphasize?",
    "header": "Focus",
    "options": [
      {"label": "Standard analysis (Recommended)", "description": "Cover all categories equally"},
      {"label": "Emphasize user experience", "description": "Focus on what users see and feel"},
      {"label": "Emphasize reliability", "description": "Focus on crashes, errors, data safety"},
      {"label": "Emphasize accessibility", "description": "Focus on usability for all users"}
    ],
    "multiSelect": false
  }
```

**CLAUDE.md summary depth for this skill:** 2-3 **non-technical** bullets — no framework
names or API references.

### Freshness

📖 **Read `../shared/scan-discipline.md` § Freshness and follow it.** In short: current
source only, never `.agents/`/`scratch/`/prior reports, with one exception for reading a
previous report's **grades only** in Step 2. The shared file is authoritative — do not
re-inline the rule here.

---

## Step 2: Trend Check

Check for a previous report to show improvement over time:

```
Glob pattern=".agents/research/*-plain-reportcard.md"
```

If found, read ONLY the grade summary line from the most recent report. Do not read or reuse any findings.

---

## Step 3: Understand the App

Before scanning for issues, understand what this app does:

1. **What is it?** — Read the app entry point and 2-3 key views to understand the purpose
2. **Who uses it?** — Consumer app, business tool, utility, game?
3. **How big is it?** — File count, approximate lines of code
4. **Key features** — List 3-5 main things users do in the app

This context shapes how findings are explained in plain language.

---

## Step 4: Automated Scans

Run all grep patterns below. Every finding MUST be verified by reading the flagged file before reporting — see Step 5.

### 4.1 User Experience

```bash
# Loading states — does the app show feedback during waits?
Grep pattern="ProgressView|\.loading|isLoading" glob="**/*.swift" output_mode="files_with_matches"

# Error handling — does the app show friendly error messages?
Grep pattern="(alert|errorMessage|showError)" glob="**/*.swift" output_mode="files_with_matches"

# Empty states — what happens when there's no data?
Grep pattern="(emptyState|EmptyView|ContentUnavailableView|noItems)" glob="**/*.swift" output_mode="files_with_matches"

# View complexity — large views may indicate poor UX structure
# Read flagged files and check if view body exceeds ~80 lines
Grep pattern="var body.*some View" glob="**/*View*.swift" output_mode="files_with_matches"
```

### 4.2 Reliability

```bash
# Force casts — can cause crashes if data is unexpected
# FALSE POSITIVE: as! after guard let or is check is already validated
Grep pattern="as!" glob="**/*.swift"

# Bare try? — silently ignores errors that users should know about
# FALSE POSITIVE: try? where nil is the expected/designed fallback
# INTENTIONAL: try? for operations where failure is acceptable (e.g., deleting a file that may not exist)
Grep pattern="try\?" glob="**/*.swift"

# Error handling coverage
Grep pattern="catch\s*\{" glob="**/*.swift" output_mode="files_with_matches"

# Data backup/sync support
Grep pattern="(CloudKit|iCloud|backup|BackupManager)" glob="**/*.swift" output_mode="files_with_matches"
```

### 4.3 Accessibility

```bash
# Fixed font sizes — breaks system text size preferences
# INTENTIONAL: some hardcoded sizes prevent clipping in constrained containers (e.g., badges, icons)
# Read each hit — classify as CONFIRMED (should migrate) or INTENTIONAL (constrained layout)
Grep pattern="\.font\(\.system\(size:" glob="**/*.swift"

# Accessibility label coverage
Grep pattern="\.accessibilityLabel" glob="**/*.swift" output_mode="count"

# Images needing descriptions for screen readers
# Read each — decorative images should use .accessibilityHidden(true)
Grep pattern="Image\(\"" glob="**/*.swift"
Grep pattern="Image\(systemName:" glob="**/*.swift"

# Testing support (accessibility identifiers)
Grep pattern="\.accessibilityIdentifier" glob="**/*.swift" output_mode="count"
```

### 4.4 Security

```bash
# Hardcoded secrets — passwords/keys visible in code
Grep pattern="(api[_-]?key|apikey|secret[_-]?key|client[_-]?secret|password|token)\s*[:=]\s*[\"'][^\"']+[\"']" glob="**/*.swift" -i

# Sensitive data stored insecurely (should be in Keychain)
Grep pattern="(UserDefaults|@AppStorage).*\b(password|token|secret|apiKey|credential)" glob="**/*.swift" -i

# Unencrypted connections
# FALSE POSITIVE: http://localhost, XML namespaces
Grep pattern="http://" glob="**/*.swift"

# Secure storage usage (positive signal)
Grep pattern="(Keychain|SecItem|kSecClass)" glob="**/*.swift" output_mode="files_with_matches"

# Privacy manifest (required for App Store)
Glob pattern="**/PrivacyInfo.xcprivacy"
```

### 4.5 Performance

```bash
# @Query without predicate (loads all data when only some is needed)
# Read file to check if only .count is accessed (should use fetchCount)
# INTENTIONAL: views that genuinely need all records (e.g., main item list) are OK
Grep pattern="@Query\s+(private\s+)?var" glob="**/*.swift"

# Timer usage (potential battery drain)
Grep pattern="Timer\.(scheduledTimer|publish)" glob="**/*.swift"

# Continuous location tracking (high battery cost)
Grep pattern="startUpdatingLocation" glob="**/*.swift"

# Main thread file I/O (can freeze the app)
# FALSE POSITIVE: FileManager in async/background context is fine
Grep pattern="(FileManager|Data\(contentsOf|String\(contentsOf)" glob="**/*View*.swift"
```

### 4.6 Code Health

```bash
# Large files (>500 lines) — harder to maintain
Glob pattern="**/*.swift"
# After finding files, check line counts with: wc -l <file>

# TODO/FIXME markers — self-documented known work
# These are INTENTIONAL markers, not bugs. Count for code health grading
# but do not list individual TODOs as issues
Grep pattern="(TODO|FIXME|HACK|XXX):" glob="**/*.swift"

# Deprecated API usage
Grep pattern="@available.*deprecated" glob="**/*.swift"

# Legacy patterns that should be modernized
# CLASSIFY: animation delay vs state update vs layout workaround
Grep pattern="DispatchQueue\.main\.(async|sync)" glob="**/*.swift"
```

### 4.7 Testing

```bash
# Test file inventory
Glob pattern="**/*Tests.swift"
Glob pattern="**/*Test.swift"
Glob pattern="**/*UITests*.swift"

# Framework usage
Grep pattern="import Testing" glob="**/*Test*.swift" output_mode="count"
Grep pattern="import XCTest" glob="**/*Test*.swift" output_mode="count"

# Compare test count to source file count for coverage estimate
```

---

## Step 5: Verification Rule (CRITICAL)

📖 **Read `../shared/scan-discipline.md` and follow it in full before compiling any
finding.** It is the source of truth for the regex constraint (no lookahead — it matches
nothing and exits 0, silently grading a category **A** on an un-run scan), the
candidate-vs-finding rule, and the reading traps. Do not re-inline those rules here; they
are shared with `tech-talk` so a fix lands in both at once.

**Additional rule for THIS skill's audience** (not in the shared file, because it applies
only to a non-technical report):

- **Only report CONFIRMED issues.** A false positive is far more damaging here than in a
  technical report — a non-technical stakeholder cannot evaluate its accuracy, so a wrong
  finding is indistinguishable from a right one and erodes trust in the whole report.
  When in doubt, leave it out and mention the uncertainty in the category narrative
  instead.
- When explaining an INTENTIONAL hit in the category summary, say why it is deliberate in
  plain terms (e.g., "some text sizes are fixed on purpose so labels don't get cut off"),
  not just that it was classified as intentional.

---

## Step 6: Grading

### Grade Scale (with plain-language meaning)

| Grade | Technical | Plain Language |
|-------|-----------|----------------|
| A | Excellent — best practices, minimal issues | Like a car that passed inspection with no issues |
| B | Good — solid, minor improvements needed | Runs well, a few minor things to tune up |
| C | Adequate — functional but gaps exist | Gets you there, but needs some attention |
| D | Poor — significant issues | Needs real work before it's dependable |
| F | Failing — critical problems | Not safe for daily use yet |

Use +/- modifiers. Convert to points: A=4, B=3, C=2, D=1, F=0 (±0.3 for +/-).

### Categories

| Category | Weight | What It Means | Why It Matters |
|----------|--------|---------------|----------------|
| User Experience | 15% | How the app feels to use | Happy users, good reviews |
| Reliability | 15% | Does the app crash or lose data? | Trust and retention |
| Accessibility | 10% | Can everyone use it? | Wider audience, legal compliance |
| Security | 15% | Is user data protected? | Trust, privacy laws |
| Performance | 15% | Is the app fast and battery-friendly? | User satisfaction |
| Code Health | 10% | Is the code easy to maintain? | Future features ship faster |
| Testing | 15% | Is the app well-tested? | Fewer bugs reach users |

> **Note to reader:** "Weight" means how much this category affects the overall grade. Security (15%) matters more than Code Health (10%).

### Overall Grade Calculation

```
Overall = (Experience × 0.15) + (Reliability × 0.15) + (Accessibility × 0.10)
        + (Security × 0.15) + (Performance × 0.15) + (Health × 0.10) + (Testing × 0.15)
```

### Timeline Adjustment

- **Pre-release:** Double-weight Security and Reliability findings
- **Post-release:** Standard weights
- **Planning:** Double-weight Code Health and Testing findings

---

## Step 7: Output Format

Write to `.agents/research/YYYY-MM-DD-plain-reportcard.md`.

### 1. Executive Summary (FIRST — 2-3 sentences)

The very first thing in the report. A non-technical reader should understand the app's health in 10 seconds.

Example:
> This app is in good shape for release with strong security and reliability. The main gaps are accessibility (making it usable for everyone) and test coverage (automated checks that catch bugs before users see them). These improvements would strengthen the app significantly.

### 2. Key Questions Answered

Answer these directly — stakeholders will ask them:

```
**Is this app ready to ship?** [Yes / Yes with caveats / Not yet]
**What's the biggest risk?** [One sentence]
**What should we prioritize?** [Top 1-2 items]
```

### 3. CLAUDE.md Summary (if included)

2-3 non-technical bullet points. If excluded: "Project context was excluded per request."

### 4. Project Overview

```
App Size: Medium (~28,000 lines of code across 142 files)
Test Coverage: Partial (47 automated tests, 12 UI tests)
```

### 5. Grade Summary Line

```
Overall: B+ (Experience B+ | Reliability A- | Accessibility C+ | Security A | Performance B | Health B+ | Testing C+)
```

### 6. Trend Comparison (if previous report exists)

```
Progress Since Last Report (YYYY-MM-DD):
  User Experience: B → B+ (improved) | Accessibility: C → C+ (improved) | Security: A → A (maintained)
```

### 7. Per-Category Grades

For each category:
- **Grade** and plain-language one-liner ("What this means")
- **What's working well** — strengths in plain language
- **What needs attention** — confirmed findings only, explained simply

Example:
```
### User Experience: B+
**What this means:** The app is pleasant to use with room for minor polish.

**What's working well:**
- App responds quickly to taps and gestures
- Clean layout that's easy to navigate

**What needs attention:**
- Some screens don't show a loading indicator — users may think the app froze
- Error messages use technical jargon instead of helpful guidance
```

Do NOT use `[HIGH]`/`[MED]`/`[LOW]` tags in the per-category sections. Keep them plain language. The Issue Rating Table (below) handles prioritization.

### 8. Issue Rating Table

Include a plain-language introduction before the table:

> **Reading this table:** Each row is something that needs attention. "Urgency" shows how soon to fix it. "Risk: No Fix" shows what happens if we don't. "ROI" shows whether the fix is worth the effort (🟠 = excellent value). "Fix Effort" shows roughly how big the job is.

Then render the full Issue Rating Table sorted by urgency descending, then ROI:

```
| # | Finding | Urgency | Risk: Fix | Risk: No Fix | ROI | Blast Radius | Fix Effort |
|---|---------|---------|-----------|-------------|-----|-------------|------------|
| 1 | ... | 🔴 Critical | ... | ... | ... | ... | ... |
```

📖 **Column definitions, indicator scales, and the one-table hard rule:
`../shared/rating-system.md`** — the source of truth, shared with
`tech-talk`. Quick reference:

- **Urgency:** 🔴 CRITICAL · 🟡 HIGH · 🟢 MEDIUM · ⚪ LOW
- **ROI:** 🟠 Excellent · 🟢 Good · 🟡 Marginal · 🔴 Poor
- **Fix Effort:** Trivial / Small / Medium / Large

⚠️ This skill deliberately shows a **reduced** column set — Risk:Fix, Risk:No Fix, and
Blast Radius are omitted because they need technical judgment a non-technical reader
cannot apply. That is an intentional divergence from the shared spec, not drift. Keep the
columns you do show identical to the shared definitions.

### 9. Recommended Next Steps

Group by timeline. Do NOT fabricate specific time estimates — use relative sizing (small/medium/large effort) unless you can estimate from actual code scope.

```
Immediate (Before Release):
- [Finding #1] — plain-language rationale

Soon (Next Few Weeks):
- [Finding #3] — plain-language rationale

Eventually (Backlog):
- [Finding #5] — plain-language rationale
```

---

## Step 8: Follow-up

📖 **Use the menu in `../shared/session-setup.md` § Follow-up menu**, including its
handling of each option. (This skill previously labelled the middle option "Create an
action plan" rather than "Create implementation plan" — a drift with no purpose. Use the
shared wording.)

---

## Plain Language Glossary

When these terms appear in code or scan results, translate them for the reader:

| Technical Term | Plain Language |
|----------------|----------------|
| Accessibility | Making the app usable by everyone, including people with disabilities |
| API | The way the app talks to servers or other apps |
| Async/await | A way of doing things in the background without freezing the app |
| CI/CD | Automated systems that test and release the app |
| Concurrency | The app doing multiple things at once without getting confused |
| Crash | The app unexpectedly closes — user loses their place |
| Dynamic Type | Users can change text size in their phone settings |
| Force unwrap | Code that assumes data exists — crashes if it doesn't |
| Keychain | Apple's secure vault for storing passwords and secrets |
| Migration | Updating how data is stored when the app gets a new version |
| Privacy Manifest | A file Apple requires that declares what user data the app accesses |
| Retain cycle | A memory bug that slowly makes the app use more and more memory |
| SwiftData | Apple's system for saving data on the device |
| SwiftUI | Apple's modern toolkit for building app screens |
| UI test | An automated robot that taps through the app like a real user |
| Unit test | An automated check that verifies a small piece of the app works correctly |
| VoiceOver | Apple's built-in screen reader that speaks what's on screen for blind users |
| WCAG | International standards for making apps accessible to everyone |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't determine app purpose | Read the app entry point, main navigation, and 2-3 views |
| Too many grep hits to verify | Narrow the glob pattern to specific directories |
| Category has no findings | Grade A — note "No issues detected" and list what was scanned |
| Stakeholder wants technical detail | Point them to `/tech-talk` for the developer version |
