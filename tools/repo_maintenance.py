"""Repo maintenance: clean .novc/, run all tests, run the routine rebuild.

Run from anywhere (each step resolves paths from this file's location):

    python tools/repo_maintenance.py
    python tools/repo_maintenance.py --skip-novc
    python tools/repo_maintenance.py --skip-tests
    python tools/repo_maintenance.py --skip-rebuild
    python tools/repo_maintenance.py --continue-on-test-failure

Three independent steps, in order:

1. Wipe the gitignored ``.novc/`` scratch dir. Everything in it is a
   regenerable download cache or tool output, never a durable result -- see
   ``README.md`` and ``tools/README.md``.
2. Run every ``*_test.py`` file found under the repo (excluding ``.venv``,
   ``.novc``, ``__pycache__``). Each test file is self-contained -- see their
   own docstrings -- so this just discovers and shells out to each.
3. Run ``py/main_0_mega.py``, the routine downstream rebuild. The two download
   scripts (``main_uxlc_download_changes.py``, ``main_clc_download_notes.py``)
   are deliberately not part of this -- run them by hand when you want fresh
   UXLC inputs; ``main_0_mega.py`` already covers every other parameterless,
   non-download rebuild step.

The rebuild step is skipped if the test step failed, unless
``--continue-on-test-failure`` is given.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_NOVC = _REPO / ".novc"
_EXCLUDED_PARTS = {".venv", ".novc", "__pycache__"}


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-novc", action="store_true", help="don't clean .novc/"
    )
    parser.add_argument(
        "--skip-tests", action="store_true", help="don't run the test suite"
    )
    parser.add_argument(
        "--skip-rebuild", action="store_true", help="don't run py/main_0_mega.py"
    )
    parser.add_argument(
        "--continue-on-test-failure",
        action="store_true",
        help="run the rebuild step even if a test failed",
    )
    return parser.parse_args()


def clean_novc():
    if not _NOVC.exists():
        print(".novc: nothing to clean (directory does not exist)")
        return
    removed = sorted(p.name for p in _NOVC.iterdir())
    shutil.rmtree(_NOVC)
    _NOVC.mkdir()
    if removed:
        print(f".novc: removed {len(removed)} entries: {', '.join(removed)}")
    else:
        print(".novc: already empty")


def _discover_tests():
    return [
        p
        for p in sorted(_REPO.rglob("*_test.py"))
        if not _EXCLUDED_PARTS & set(p.parts)
    ]


def run_tests():
    tests = _discover_tests()
    if not tests:
        print("tests: no *_test.py files found")
        return True
    failed = []
    for test in tests:
        rel = test.relative_to(_REPO)
        result = subprocess.run([sys.executable, str(test)], cwd=_REPO)
        print(f"tests: {'OK' if result.returncode == 0 else 'FAILED':<6} {rel}")
        if result.returncode != 0:
            failed.append(rel)
    print(f"tests: {len(tests) - len(failed)}/{len(tests)} passed")
    return not failed


def run_rebuild():
    script = _REPO / "py" / "main_0_mega.py"
    result = subprocess.run([sys.executable, str(script)], cwd=_REPO)
    print(
        "rebuild: OK"
        if result.returncode == 0
        else f"rebuild: FAILED (exit {result.returncode})"
    )
    return result.returncode == 0


def main():
    # Line-buffer so status lines interleave correctly with the child
    # processes' own output when stdout isn't a live terminal (e.g. redirected
    # to a log file).
    sys.stdout.reconfigure(line_buffering=True)
    args = _parse_args()
    ok = True
    tests_ok = True

    if not args.skip_novc:
        clean_novc()

    if not args.skip_tests:
        tests_ok = run_tests()
        ok = tests_ok and ok

    if not args.skip_rebuild:
        if tests_ok or args.continue_on_test_failure:
            ok = run_rebuild() and ok
        else:
            print(
                "rebuild: skipped (tests failed; pass --continue-on-test-failure "
                "to run anyway)"
            )
            ok = False

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
