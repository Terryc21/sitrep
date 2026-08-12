#!/usr/bin/env python3
"""Regression bench for the report-card skills' Grep patterns.

Why this file exists
--------------------
These are pure-instruction skills: no helper scripts, nothing to unit-test in the
usual sense. But the `Grep pattern="..."` strings ARE mechanical, and on 2026-08-11 one
of them was found to be silently broken in the worst possible direction:

    Grep pattern="(class|struct).*ViewModel(?!.*@MainActor)"

The default Grep engine does not support look-around. The pattern did not error — it
matched NOTHING and exited 0. A zero-hit scan then satisfied the grading rule
"0-1 confirmed findings -> A", so the Concurrency category (10% of the weighted grade)
was awarded an A on evidence that was never collected. Silent, and biased toward a
flattering grade, which is the worst direction for a grading skill.

Nothing could have caught that, because nothing ever executed the patterns.

What these tests assert
-----------------------
1. Every extracted pattern COMPILES under Python's `re` (a proxy for the default
   non-PCRE engine — it rejects the same look-around constructs).
2. No pattern contains look-around at all.
3. The ViewModel-declaration pattern matches all three fixture ViewModels' *files*
   and, critically, DISTINGUISHES the annotated from the unannotated one only after
   reading the attribute stack — the property the old regex pretended to have.
4. The capture-list pattern flags the un-weak closure and the weak one alike
   (over-match by design; classification happens in the Read step).
5. Category weights sum to 100%.

Run:  python3 tests/test_scan_patterns.py     (exit 0 = pass)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "sample-project" / "Sources"

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + ("" if ok else f"  (got {got!r}, want {want!r})"))
    if not ok:
        FAILURES.append(label)


# Pull every `Grep pattern="..."` out of the two report-card skills.
PATTERN_RE = re.compile(r'Grep pattern="((?:[^"\\]|\\.)*)"')
LOOKAROUND_RE = re.compile(r'\(\?[=!<]')


def extract_patterns():
    found = []
    for skill in ("tech-talk", "plain-talk"):
        f = SKILLS / skill / "SKILL.md"
        if not f.exists():
            continue
        for i, line in enumerate(f.read_text().splitlines(), 1):
            for m in PATTERN_RE.finditer(line):
                found.append((skill, i, m.group(1)))
    return found


print("pattern extraction:")
patterns = extract_patterns()
check("found patterns to test", len(patterns) > 0, True)
print(f"        ({len(patterns)} patterns across both skills)")

# --- 1. every pattern compiles under a non-PCRE engine -----------------------
print("\npattern validity:")
bad_compile = []
for skill, line, pat in patterns:
    try:
        re.compile(pat)
    except re.error as e:
        bad_compile.append(f"{skill}:{line} {pat!r} ({e})")
check("every pattern compiles", bad_compile, [])

# --- 2. no look-around anywhere (the CRITICAL bug class) ---------------------
lookaround = [f"{s}:{l} {p!r}" for s, l, p in patterns if LOOKAROUND_RE.search(p)]
check("no look-around in any pattern", lookaround, [])

# --- 3. the ViewModel pattern behaves on real fixture code -------------------
print("\nViewModel scan against fixtures:")
VM_PAT = None
for skill, line, pat in patterns:
    if "ViewModel" in pat and ("class" in pat or "struct" in pat):
        VM_PAT = pat
        break
check("ViewModel declaration pattern present", VM_PAT is not None, True)

if VM_PAT:
    rx = re.compile(VM_PAT)
    matched = {f.name for f in FIXTURE.glob("*ViewModel.swift")
               if any(rx.search(l) for l in f.read_text().splitlines())}
    # Files that DECLARE a ViewModel type:
    check("matches the correctly-annotated ViewModel", "GoodViewModel.swift" in matched, True)
    check("matches the defective ViewModel", "BadViewModel.swift" in matched, True)
    # The filename-is-not-a-type trap:
    check("does NOT match the helpers-only file", "HelpersViewModel.swift" in matched, False)
    check("returns a non-empty candidate set", len(matched) > 0, True)

    # The property the old lookahead FAKED: distinguishing annotated from not.
    # A line-scoped regex cannot do this; the Read step must, by scanning the
    # attribute stack upward. Assert that the stack-reading rule is what works.
    def has_mainactor_above(path):
        lines = path.read_text().splitlines()
        for i, l in enumerate(lines):
            if rx.search(l):
                j = i - 1
                while j >= 0 and lines[j].strip().startswith("@"):
                    if "@MainActor" in lines[j]:
                        return True
                    j -= 1
                return False
        return False

    check("attribute-stack read finds @MainActor on the good VM",
          has_mainactor_above(FIXTURE / "GoodViewModel.swift"), True)
    check("attribute-stack read finds the bad VM unannotated",
          has_mainactor_above(FIXTURE / "BadViewModel.swift"), False)
    # A one-line window would get GoodViewModel wrong — prove the window matters.
    good = (FIXTURE / "GoodViewModel.swift").read_text().splitlines()
    decl = next(i for i, l in enumerate(good) if rx.search(l))
    check("a ONE-line window would misreport the good VM (why the rule says read the stack)",
          "@MainActor" in good[decl - 1], False)

# --- 4. capture-list pattern over-matches by design --------------------------
print("\ncapture-list scan against fixtures:")
CAP_PAT = next((p for _, _, p in patterns if r"\{\s*\[" in p), None)
check("capture-list pattern present", CAP_PAT is not None, True)
if CAP_PAT:
    rx2 = re.compile(CAP_PAT)
    hits = {f.name for f in FIXTURE.glob("*.swift")
            if any(rx2.search(l) for l in f.read_text().splitlines())}
    check("flags the un-weak closure (true positive)", "BadViewModel.swift" in hits, True)
    check("also flags the weak closure (over-match is intended)",
          "GoodViewModel.swift" in hits, True)

# --- 5. category weights sum to 100% -----------------------------------------
print("\ngrading integrity:")
tech = (SKILLS / "tech-talk" / "SKILL.md").read_text()
weights = [int(m) for m in re.findall(r"\|\s*(\d{1,2})%\s*\|", tech)]
check("category weights sum to 100", sum(weights), 100)

# --- 6. shared references resolve --------------------------------------------
print("\nshared references:")
dangling = []
for skill in ("tech-talk", "plain-talk"):
    f = SKILLS / skill / "SKILL.md"
    for ref in set(re.findall(r"\.\./shared/([a-z-]+\.md)", f.read_text())):
        if not (SKILLS / "shared" / ref).exists():
            dangling.append(f"{skill} -> {ref}")
check("every ../shared/ reference resolves", dangling, [])

print()
if FAILURES:
    print(f"FAIL — {len(FAILURES)} assertion(s): {', '.join(FAILURES)}")
    sys.exit(1)
print("All scan-pattern assertions passed.")
