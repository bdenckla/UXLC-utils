"""Exports main: run the repo's tests through the one entry point under ``py/``.

Usage (run from the repo root, like the other py/main_*.py drivers):

    python py/main_test.py                     # every registered test module
    python py/main_test.py --clc-kq            # just one (repeatable)
    python py/main_test.py --list              # the registry, one line per module

This exists so no test file needs to touch ``sys.path`` (GitHub issue #56).
CPython puts a script's own directory at ``sys.path[0]``, so running *this*
file puts ``py/`` there, and every test module's ``import clc.clc_kq`` /
``import repo_hygiene.source_hygiene`` resolves with no path configuration at
all. That is also why the test modules no longer carry an
``if __name__ == "__main__"`` block: they are not independently runnable, and a
direct ``python py/clc/clc_kq_test.py`` would only fail on the import.

The contract a test module owes this runner is a single ``main()`` that runs
its own checks and raises (``AssertionError``, or ``SystemExit`` with a nonzero
code) on failure. Each is called in-process, one at a time, with failures
caught so a later module still runs; the exit status is nonzero if any failed.

``TEST_MODULE_SPECS`` below is hand-maintained, which in the two sibling repos
using this pattern has meant an unlisted test file silently never running --
worse than a skip, since it reports nothing at all. So ``check_registry()``
walks ``py/`` for ``*_test.py`` on every run and fails if the two disagree,
rather than leaving it to a reader to compare ``--list`` against ``git
ls-files``.
"""

import argparse
import importlib
import os
import sys
from dataclasses import dataclass

_PY_ROOT = os.path.dirname(os.path.abspath(__file__))

# This runner's own name ends in "_test.py" too, so discovery would otherwise
# report it as an unregistered test module.
_SELF = os.path.basename(os.path.abspath(__file__))

# Not ours to police: the vendored packages are kept byte-identical to their
# MAM-basics originals, so a test file appearing in one is upstream's business.
_PRUNED_DIRS = {"__pycache__", "mb_cmn", "mb_diff_mpu"}


@dataclass(frozen=True)
class TestModuleSpec:
    flag: str
    module_name: str
    help_text: str


TEST_MODULE_SPECS = (
    TestModuleSpec(
        flag="clc-attribution",
        module_name="clc.clc_attribution_test",
        help_text="Run CLC UXLC-attribution citation tests.",
    ),
    TestModuleSpec(
        flag="clc-collect",
        module_name="clc.clc_collect_test",
        help_text="Run CLC note-collection tests (pending-change patch, relegation).",
    ),
    TestModuleSpec(
        flag="clc-dual-cant",
        module_name="clc.clc_dual_cant_test",
        help_text="Run CLC dual-cantillation strand-split tests.",
    ),
    TestModuleSpec(
        flag="clc-kq",
        module_name="clc.clc_kq_test",
        help_text="Run CLC ketiv/qere grouping and ruby tests.",
    ),
    TestModuleSpec(
        flag="clc-note-pages",
        module_name="clc.clc_note_pages_test",
        help_text="Run tanach.us note-page prose-extraction tests.",
    ),
    TestModuleSpec(
        flag="clc-versification",
        module_name="clc.clc_versification_test",
        help_text="Run the vtrad-MAM Decalogue verse-map tests.",
    ),
    TestModuleSpec(
        flag="nfc-h-dot-below",
        module_name="repo_hygiene.nfc_h_dot_below_test",
        help_text="Run NFC h-with-dot-below enforcement tests (issues #21, #26).",
    ),
    TestModuleSpec(
        flag="source-hygiene",
        module_name="repo_hygiene.source_hygiene_test",
        help_text="Run source-hygiene guard tests (issues #22, #26).",
    ),
)


def discovered_module_names():
    """Dotted names of every ``*_test.py`` under ``py/``, vendored dirs pruned."""
    found = []
    for dirpath, dirnames, filenames in os.walk(_PY_ROOT):
        dirnames[:] = [d for d in dirnames if d not in _PRUNED_DIRS]
        rel_dir = os.path.relpath(dirpath, _PY_ROOT)
        for name in sorted(filenames):
            if not name.endswith("_test.py"):
                continue
            if rel_dir == "." and name == _SELF:
                continue
            stem = name[: -len(".py")]
            parts = [] if rel_dir == "." else rel_dir.replace(os.sep, "/").split("/")
            found.append(".".join(parts + [stem]))
    return sorted(found)


def check_registry():
    """Raise if TEST_MODULE_SPECS and the tree disagree about what the tests are."""
    registered = {spec.module_name for spec in TEST_MODULE_SPECS}
    discovered = set(discovered_module_names())
    unregistered = sorted(discovered - registered)
    missing = sorted(registered - discovered)
    problems = []
    if unregistered:
        problems.append(
            "test files present but not in TEST_MODULE_SPECS (they would never "
            f"run): {unregistered}"
        )
    if missing:
        problems.append(f"registered but no such file under py/: {missing}")
    if problems:
        raise AssertionError(
            "main_test registry is out of date: " + "; ".join(problems)
        )


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Run the repo's tests through a single py/ entry point, so module "
            "imports resolve without any sys.path configuration."
        )
    )
    for spec in TEST_MODULE_SPECS:
        parser.add_argument(f"--{spec.flag}", action="store_true", help=spec.help_text)
    parser.add_argument(
        "--list",
        action="store_true",
        help="List the registered test modules and exit.",
    )
    return parser


def selected_specs(args):
    """The specs the flags asked for -- all of them if no flag was given."""
    chosen = [
        spec for spec in TEST_MODULE_SPECS if getattr(args, spec.flag.replace("-", "_"))
    ]
    return chosen or list(TEST_MODULE_SPECS)


def _run_one(spec):
    """Run one module's main(); return True if it passed."""
    try:
        module = importlib.import_module(spec.module_name)
        module.main()
    except SystemExit as exc:
        if exc.code:
            print(f"tests: FAILED {spec.module_name} (exit {exc.code})")
            return False
    except Exception as exc:  # a test's AssertionError, or a broken import
        print(f"tests: FAILED {spec.module_name}: {type(exc).__name__}: {exc}")
        return False
    return True


def main():
    """Run the selected test modules in-process, then report the tally."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = build_parser().parse_args()

    if args.list:
        for spec in TEST_MODULE_SPECS:
            print(f"--{spec.flag}\t{spec.module_name}")
        check_registry()
        return

    check_registry()
    specs = selected_specs(args)
    failed = [spec.module_name for spec in specs if not _run_one(spec)]
    print(f"tests: {len(specs) - len(failed)}/{len(specs)} passed")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
