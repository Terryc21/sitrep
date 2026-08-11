# Tests

```bash
bash tests/run.sh
```

Exit 0 = pass.

## What is tested, and why only this

These are **pure-instruction skills** — no Python, no shell helpers, nothing with a
return value. An LLM's grade output is not deterministic and is not asserted here.

What *is* deterministic is the `Grep pattern="..."` strings the skills instruct the agent
to run. Those are code in every way that matters, and they are where the only CRITICAL
bug this repo has had was found.

### The bug these tests exist to prevent

On 2026-08-11 the Concurrency scan used:

```
Grep pattern="(class|struct).*ViewModel(?!.*@MainActor)"
```

The default Grep engine does not support look-around. The pattern did not error — it
**matched nothing and exited 0**. A zero-hit scan satisfies the grading rule "0-1
confirmed findings → A", so Concurrency (10% of the weighted grade) scored an **A on
evidence that was never collected**.

Both failure directions were measured against a real codebase: **0** matches under the
default engine, **11** with PCRE2 forced on, against a verified reality of **zero**
violations. Neither number resembled the truth.

Nothing caught it because nothing ever executed the patterns. Now something does.

## Coverage

| Check | Catches |
|---|---|
| Every pattern compiles under a non-PCRE engine | Syntactically invalid regex |
| No look-around in any pattern | The CRITICAL bug class above |
| ViewModel pattern matches both fixture ViewModels | A pattern that silently stops matching |
| ViewModel pattern does NOT match the helpers-only file | The filename-is-not-a-type trap |
| Attribute-stack read distinguishes annotated from not | The one-line-window false-positive trap |
| Capture-list pattern over-matches by design | Confirms classification belongs in the Read step |
| Category weights sum to 100% | A grading formula that silently stops totalling |
| Every `../shared/` reference resolves | Dangling shared-file references |

## Fixtures

`fixtures/sample-project/Sources/` — three files, each encoding a trap that produced a
real false result:

- **`GoodViewModel.swift`** — correctly annotated, but `@MainActor` sits *three lines*
  above the declaration behind `@available` and `@Observable`. A one-line read window
  reports it as a violation. (Produced 5 false positives out of 5 on a real codebase.)
- **`BadViewModel.swift`** — genuinely missing `@MainActor`, plus a capture list with no
  `weak`. The known-positive: a scan reporting zero findings here is broken.
- **`HelpersViewModel.swift`** — named `*ViewModel.swift`, contains **no ViewModel** (two
  enum namespaces of static helpers). Absence of `@MainActor` is correct. This shape made
  a reviewer's "ground truth" wrong before any scan ran.

## Mutation-tested

Both failure modes were verified to actually fail:

1. Reintroducing the lookahead pattern → `no look-around in any pattern` fails, naming
   the file, line, and pattern.
2. Replacing it with a valid-but-over-strict regex (`^class \w*ViewModel \{`) → four
   assertions fail, because it silently stops matching real declarations.

A test that cannot fail is not a test. If you change a pattern, re-run the mutations.
