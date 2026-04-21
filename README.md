# Xcode Workflow Skills

> [!WARNING]
> **This repository is archived.** The active skills have moved to two dedicated repos:
>
> ### [→ workflow-audit](https://github.com/Terryc21/workflow-audit)
> 5-layer UI workflow audit for SwiftUI apps. Finds orphaned views, dead ends, buried buttons, dismiss traps, unwired data, and 20+ other issue categories. Claude Code plugin.
>
> ### [→ radar-suite](https://github.com/Terryc21/radar-suite)
> 6 data-focused audit skills: data model completeness, time-bomb detection, UI path tracing, round-trip data flow verification, visual design consistency, and capstone ship/no-ship grading.
>
> **For bug reports, feature requests, or questions, please use the active repos. This one no longer accepts issues or PRs.**

---

## Why this repo is archived

The original `xcode-workflow-skills` bundled 25 skills into one plugin. Over time it became clear the skills fell into two clear families with different update cadences and scopes:

- **Workflow and navigation audits** moved to [workflow-audit](https://github.com/Terryc21/workflow-audit), which has since grown into a standalone 5-layer audit plugin.
- **Data and correctness audits** moved to [radar-suite](https://github.com/Terryc21/radar-suite), a monorepo of six coordinated audit skills with cross-skill handoffs.

Splitting them let each family evolve independently without dragging unrelated changes through every release.

## Discontinued skills

The following skills from this repo are discontinued and will not be maintained. If you relied on any of them, see the "Recommended alternatives" section below for active projects that cover similar ground.

| Skill | Description |
|-------|-------------|
| `/review-changes` | Pre-commit review |
| `/scan-similar-bugs` | Cross-codebase pattern search |
| `/dead-code-scanner` | Unused code detection |
| `/tech-talk-reportcard` | Technical A-F grading |
| `/plain-talk-reportcard` | Non-technical A-F grading |
| `/codebase-audit` | 24-domain comprehensive audit |
| `/plan` | Epic decomposition and task planning |
| `/safe-refactor` | Blast radius analysis and rollback |
| `/explain` | Code walkthrough and explanation |
| `/run-tests` | Smart test execution |
| `/generate-tests` | Test generation with mocks and edge cases |
| `/ui-scan` | UI test setup and accessibility scan |
| `/debug` | Systematic bug investigation |
| `/security-audit` | Security and privacy manifest scan |
| `/performance-check` | Performance anti-pattern detection |
| `/release-prep` | Pre-release checklist |
| `/release-screenshots` | App Store screenshot capture |
| `/update-website` | Website sync with app changes |
| `/commands` | Skill listing |
| `/enhanced-commands` | Skill listing with examples |

## Recommended alternatives

If you're looking for skills that cover similar ground to the discontinued list above, these are excellent:

- **[Axiom](https://charleswiltgen.github.io/Axiom/)** by [Charles Wiltgen](https://github.com/CharlesWiltgen). Comprehensive iOS development skills for Claude Code. Covers concurrency, memory debugging, SwiftUI performance, accessibility, build fixing, security, and much more. Highly recommended.
- **Swift Pro Skills** by [Paul Hudson](https://github.com/twostraws). SwiftData Pro, SwiftUI Pro, Swift Concurrency Pro, and Swift Testing Pro. Deep-dive code review and best practices for modern Swift development.

## License

MIT

## Author

Created by [Terry Nyberg](https://github.com/Terryc21)
