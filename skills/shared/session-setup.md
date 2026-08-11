# Session Setup — Shared Reference

> **Imported by:** `tech-talk-reportcard/SKILL.md`, `plain-talk-reportcard/SKILL.md`
> **Source of truth** for the opening interview, the trend check, and the follow-up menu.
>
> ⚠️ Each importer had its own copy of these blocks and they had already drifted (the
> timeline options matched; the focus options and CLAUDE.md wording did not). Change them
> here, once.

---

## Opening interview

Ask before scanning anything. The first two questions are identical across report-card
skills; the third is **skill-specific** and each skill defines its own (see below).

```
AskUserQuestion with questions:
[
  {
    "question": "Should the analysis consider CLAUDE.md project instructions?",
    "header": "CLAUDE.md",
    "options": [
      {"label": "Yes, use CLAUDE.md (Recommended)", "description": "Include project context, coding standards, and preferences"},
      {"label": "No, ignore CLAUDE.md", "description": "Unbiased analysis without project-specific instructions"}
    ],
    "multiSelect": false
  },
  {
    "question": "What is your timeline?",
    "header": "Timeline",
    "options": [
      {"label": "Pre-release", "description": "Preparing for App Store — urgency matters"},
      {"label": "Post-release", "description": "App is live, ongoing improvement"},
      {"label": "Planning phase", "description": "Gathering info for roadmap"}
    ],
    "multiSelect": false
  },
  <<< third question: see the importing skill's "Focus question" section >>>
]
```

**If "Yes" for CLAUDE.md:** read CLAUDE.md at the repo root and summarize its key points.
Use those guidelines throughout the analysis. (How many bullets, and at what reading
level, is the importing skill's call.)

**If "No":** skip it, and state in the report that it was intentionally excluded.

### Timeline adjustment

Applies to grading in every report-card skill:

- **Pre-release:** double-weight Security and Performance findings
- **Post-release:** standard weights
- **Planning:** double-weight Architecture and Testing findings

---

## Trend check

Look for a previous report to enable grade-trend comparison. Each skill globs its own
filename pattern (`*-tech-reportcard.md`, `*-plain-reportcard.md`).

Read **ONLY the grade summary line** from the most recent report. Do not read or reuse
any findings — those must come fresh from scanning, per
`scan-discipline.md § Freshness`.

⚠️ **If no previous report is found, say so in the output** ("No prior report found —
this is the first grade for this project"). Omitting the trend section silently is
indistinguishable from a trend of "no change," and `.agents/research/` is volatile enough
that a prior report can disappear between runs.

---

## Follow-up menu

Ask after presenting the report:

```
AskUserQuestion with questions:
[
  {
    "question": "What would you like to do next?",
    "header": "Next",
    "options": [
      {"label": "Fix critical issues now", "description": "Walk through each critical/high issue with code fixes"},
      {"label": "Create implementation plan", "description": "Generate a prioritized plan from the findings"},
      {"label": "Report is sufficient", "description": "End here — report saved to .agents/research/"}
    ],
    "multiSelect": false
  }
]
```

- **Fix critical issues now:** walk each 🔴/🟡 finding, show the code, propose a fix,
  apply only after approval.
- **Create implementation plan:** group findings into phases and present as a structured
  plan.
