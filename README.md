# Sitrep

A situation report for your codebase: graded, sourced, and honest about what wasn't
checked.

Sitrep examines an iOS/Swift codebase across nine categories, verifies every finding by
reading the flagged code (never by trusting a grep count), and reports the result twice:
once for engineers, once for the people who fund them.

## Active skills

| Skill | Audience | What you get |
|-------|----------|--------------|
| `tech-talk-reportcard` | Developers | A-F grades across 9 categories (Architecture, Security, Performance, Concurrency, Accessibility, Testing, and more), a consolidated Issue Rating Table, and next steps grouped by timeline |
| `plain-talk-reportcard` | Stakeholders | The same examination explained in plain language, with only confirmed issues reported. A false positive is worse than a missed one when the reader can't evaluate accuracy |

Shared discipline lives in `skills/shared/` and is imported by both:

- `scan-discipline.md`: grep patterns produce candidates, not findings. Every hit is read
  and classified before it can appear in a report. No look-around regex, ever (see below).
- `session-setup.md`: the opening interview, trend check, and follow-up menu.
- `rating-system.md`: column definitions and indicator scales, one table, one row per
  finding.

## Why the scans are tested

In August 2026 the Concurrency scan was found to have never run. Its regex used negative
lookahead, which the default engine does not support. The pattern matched nothing, exited
0, and the empty result satisfied the grading rule "0-1 confirmed findings = A". Ten
percent of the weighted grade was being awarded on evidence that was never collected.

`tests/run.sh` now extracts every grep pattern from both skills and executes it against a
fixture project with known-positive and known-negative cases. A pattern that silently
stops matching fails the suite. Run it before trusting a report:

```bash
bash tests/run.sh
```

## Why "Sitrep"

A military situation report states current conditions, capabilities, and threats before a
decision, and a real sitrep includes what is not known. That is the posture these skills
aim for: the grade is only as good as the declared coverage behind it.

## Dormant skills

`generate-tests`, `release-prep`, and `safe-refactor` remain in the repo but are not
maintained. Use them as-is or see the alternatives below.

## History

This repo began as `xcode-workflow-skills`, a bundle of 25 skills. The two largest
families outgrew it and moved to dedicated repos:

- **Workflow and navigation audits** became
  [workflow-audit](https://github.com/Terryc21/workflow-audit), a standalone 5-layer
  audit plugin.
- **Data and correctness audits** became
  [radar-suite](https://github.com/Terryc21/radar-suite), six coordinated audit skills
  with cross-skill handoffs.

The report cards stayed, were rebuilt with tested scans and shared discipline, and the
repo was renamed Sitrep in August 2026. Other skills from the original bundle
(`review-changes`, `debug`, `explain`, `run-tests`, `ui-scan`, `security-audit`,
`performance-check`, `codebase-audit`, `plan`, and others) are discontinued.

## Recommended alternatives

For ground the discontinued skills used to cover:

- **[Axiom](https://charleswiltgen.github.io/Axiom/)** by
  [Charles Wiltgen](https://github.com/CharlesWiltgen). Comprehensive iOS development
  skills for Claude Code: concurrency, memory debugging, SwiftUI performance,
  accessibility, build fixing, security, and much more. Highly recommended.
- **Swift Pro Skills** by [Paul Hudson](https://github.com/twostraws). SwiftData Pro,
  SwiftUI Pro, Swift Concurrency Pro, and Swift Testing Pro. Deep-dive code review and
  best practices for modern Swift development.

## License

MIT

## Author

Created by [Terry Nyberg](https://github.com/Terryc21)
