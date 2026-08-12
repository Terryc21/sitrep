# Changelog

All notable changes to these Claude Code skills will be documented in this file.

## [2.3.0] - 2026-08-11

Repo unarchived and **renamed `xcode-workflow-skills` → `sitrep`**. The two report-card
skills go to **3.1.0**; the plugin manifests to **2.3.0**. Minor, not patch: a scan that
never ran now runs.

**Rename note.** GitHub redirects the old URL indefinitely, so existing clones and links
keep working — but only for as long as no new repo claims the name
`xcode-workflow-skills`. Do not create one. The plugin manifest's `name` field changed
too, so anyone who installed from the marketplace under the old name should reinstall.

⚠️ **Note on the gap in this file.** Entries jump from 1.1.0 (February) to 2.3.0 — the
manifests had reached 2.2.0 and individual skills 2.1.0–3.0.0 with no changelog entries
in between. Those intermediate changes are not reconstructed here.

### Skills renamed

`tech-talk-reportcard` → **`tech-talk`** · `plain-talk-reportcard` → **`plain-talk`**

The `-reportcard` suffix restated what the repo name now carries, and "report card" is the
artifact The Honest Machine ch. 8 indicts — a letter grade that reads as an answer.
`tech-talk` / `plain-talk` name the *register* instead: the same examination, told two
ways. Invocation becomes `/tech-talk` and `/plain-talk`; the old command names stop
working. Directory, frontmatter `name:`, and installed symlink were moved together — a
mismatch between any two of those three silently breaks skill loading.

Historical entries below (1.0.0, February) keep the original names on purpose.

### tech-talk (3.0.0 → 3.1.0)

- 🔴 **FIXED: the Concurrency scan never ran.** `(class|struct).*ViewModel(?!.*@MainActor)`
  used negative lookahead, which the default Grep engine does not support. The pattern did
  not error — it matched **nothing** and **exited 0**, which the grading rule reads as
  "0-1 confirmed findings → A". Concurrency (10% of the weighted grade) was scored **A on
  evidence that was never collected**. Measured against a real 11-ViewModel codebase: **0**
  matches by default, **11** with PCRE2 forced on, against a verified reality of **zero**
  violations — neither number resembling the truth.
- Same defect fixed in the three `[weak self]` capture-list patterns.
- Both replaced with match-then-filter, which the skill's own verification rule already
  required.

### plain-talk (3.0.0 → 3.1.0)

- Audience-specific rules preserved and sharpened (confirmed-issues-only; explain
  INTENTIONAL hits in plain terms).
- Documented that its reduced column set — no Risk:Fix, Risk:No Fix, Blast Radius — is a
  deliberate divergence for non-technical readers, not drift.

### Shared (`skills/shared/`)

- **New `scan-discipline.md`** — freshness rule, the no-lookahead constraint with its
  measured evidence, the candidate-vs-finding verification rule, and two reading traps
  (read the whole attribute stack; a filename is not a type).
- **New `session-setup.md`** — opening interview, timeline grading adjustment, trend
  check, follow-up menu.
- **`rating-system.md` header corrected** — it named importers (`workflow-audit`, `plan`)
  that had moved to another repo, leaving it orphaned while both report cards kept inline
  copies.
- Real prose duplication between the two skills: **21 lines → 10**.
- Trend check now states "no prior report found" instead of silently omitting the section.

### Tests (new)

- `tests/run.sh` + `tests/test_scan_patterns.py` — **19 assertions over 63 extracted
  patterns**. Asserts every pattern compiles under a non-PCRE engine, contains no
  look-around, and behaves correctly against fixtures.
- `tests/fixtures/sample-project/` — three files, each encoding a trap that produced a real
  false result: a correctly-annotated ViewModel whose `@MainActor` sits three lines up; a
  genuinely defective one; and a `*ViewModel.swift` containing **no ViewModel**.
- **Mutation-tested both ways:** reintroducing the lookahead fails the look-around
  assertion; a valid-but-over-strict regex fails four match assertions.

### docs

- `skill-handoff-design.md` — removed project-identifying content (name, real source paths,
  a real feature symbol, and a section listing audit findings) per the local-only-markdown
  rule. This repo is public and had never been in scope of the 2026-07-31 sweep, which
  covered a different directory tree.

## [1.1.0] - 2026-02-17

### scan-similar-bugs
- Added **Phase 2.5: Cross-Platform Verification** for iOS/macOS projects
- Added "Platform-specific UI" bug category
- Added bidirectional scanning (iOS → macOS, macOS → iOS)
- Added common cross-platform invariants checklist
- Added whitelist for legitimate platform-only code
- Added "Platform" column to findings summary table

## [1.0.0] - 2026-02-15

### Initial Release
- debug
- enhanced-commands
- explain
- generate-tests
- implementation-plan
- migrate-schema
- performance-check
- plain-talk-reportcard
- release-prep
- release-screenshots
- review-changes
- run-tests
- safe-refactor
- scan-similar-bugs
- security-audit
- tech-talk-reportcard
- ui-scan
