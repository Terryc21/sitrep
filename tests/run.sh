#!/usr/bin/env bash
# xcode-workflow-skills self-test harness
#
# These are pure-instruction skills — no helper scripts to unit-test. What IS mechanical
# is the `Grep pattern="..."` strings the skills tell the agent to run, and those are
# exactly where a silent, grade-inflating bug was found on 2026-08-11. This harness
# executes them against a fixture project with known-positive and known-negative cases.
#
# Run:            bash tests/run.sh
# Exit 0 = pass.  Any failure exits non-zero and names the assertion.

set -uo pipefail   # NOT -e: we want every check to run, then report collectively

cd "$(dirname "$0")"
TESTS_DIR="$(pwd -P)"
REPO_ROOT="$(cd .. && pwd -P)"

FAILED=0

echo "=== scan-pattern regression bench ==="
python3 "$TESTS_DIR/test_scan_patterns.py" || FAILED=1

echo
echo "=== fixture sanity ==="
FIX="$TESTS_DIR/fixtures/sample-project/Sources"
for f in GoodViewModel.swift BadViewModel.swift HelpersViewModel.swift; do
  if [[ -f "$FIX/$f" ]]; then
    echo "  PASS  fixture present: $f"
  else
    echo "  FAIL  fixture MISSING: $f"
    FAILED=1
  fi
done

echo
if [[ $FAILED -ne 0 ]]; then
  echo "TESTS FAILED"
  exit 1
fi
echo "All tests passed."
