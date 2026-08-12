# Scan Discipline — Shared Reference

> **Imported by:** `tech-talk/SKILL.md`, `plain-talk/SKILL.md`
> **Source of truth** for the freshness rule, the regex constraint, and the
> candidate-vs-finding verification rule.
>
> ⚠️ Both importers previously carried their own copies of these rules. They drifted.
> If you change a rule here, you change it for every report-card skill — that is the
> point. Do not re-inline any of this into a SKILL.md.

---

## Freshness

Base all findings on current source code only. Do not read or reference files in
`.agents/`, `scratch/`, or prior audit reports. Ignore cached findings from auto-memory
or previous sessions. Every finding must come from scanning the actual codebase as it
exists now.

**Exception:** reading a previous report's **grades only** (never its findings) for
trend comparison is allowed in the trend-check step.

**Why:** an audit skill that can read its own prior output will launder stale findings
forward, and the staleness is invisible in the result — the second report looks like
confirmation of the first when it is really an echo of it.

---

## Regex constraint: NO lookahead or lookbehind (load-bearing)

**Never write `(?!`, `(?=`, `(?<=`, or `(?<!` in a Grep pattern.** The Grep tool's
default engine does not support look-around: the pattern does not error loudly — it
matches **nothing**, prints an advisory to stderr, and **exits 0**.

A scan returning zero hits then satisfies the grading rule "0-1 confirmed findings → A",
so the category is graded **A on evidence that was never collected**. The failure is
silent and biased toward a flattering grade, which is the worst possible direction for a
grading skill.

*Measured 2026-08-11 on a codebase with 11 ViewModel types: the pattern
`(class|struct).*ViewModel(?!.*@MainActor)` returned **0** files under the default engine
(silent miss → grade A) and **11** with PCRE2 forced on — neither answer resembling the
verified reality of zero violations.*

**Use match-then-filter instead**, which the verification rule below already requires:
write a plain pattern that over-matches candidates, then READ each hit to classify it.

⚠️ **A regex that needs to know about a neighbouring line cannot be a line-scoped grep
at all.** Swift attributes (`@MainActor`, `@Observable`, `@available`) sit on lines
*above* the declaration they modify. That determination belongs in the Read step, not
the pattern.

---

## Verification Rule (CRITICAL)

Grep patterns produce CANDIDATES, not confirmed issues. Before reporting ANY finding:

1. **Read the flagged file** — at minimum 20 lines of context around the match
2. **Check structural context** — a pattern inside a nested closure may be safe
   depending on the outer scope
3. **Classify before reporting** — label each hit CONFIRMED, FALSE_POSITIVE, or
   INTENTIONAL
4. **Never report grep counts as issue counts** — "60 `DispatchQueue.main` calls" is a
   grep count; the real issue count requires classifying each one
5. **INTENTIONAL hits** — note them in the category narrative as acknowledged design
   decisions (they inform grading), but do NOT list them in the Issue Rating Table

### Reading traps that produce false findings

Both of these were hit in practice on 2026-08-11 while verifying this very skill:

- ⚠️ **Read the whole attribute stack, not one line up.** Real declarations stack three
  or four attributes (`@available` / `@MainActor` / `@Observable` / `final class`). A
  one-line window reports correctly-annotated types as violations. Read upward until a
  blank line, a `}`, or an `import`.
- ⚠️ **A filename is not a type.** A file named `*ViewModel.swift` need not contain a
  ViewModel — enum namespaces of static helpers are commonly parked there. Grade on the
  types the pattern actually returns, never on a filename inventory.

### Common false positives

- `Task {}` inside an `@MainActor` class or view body → inherits isolation, safe
- `DispatchQueue.main.asyncAfter` for animation/layout → intentional
- `nonisolated` on protocol requirement methods → required by the protocol
- `http://` in XML namespace URIs → not a real HTTP endpoint
- `as!` after a `guard let` or `is` check → already validated
- `try?` in optional chaining for expected-nil paths → intentional
