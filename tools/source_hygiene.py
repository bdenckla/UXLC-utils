"""Source-hygiene guard for hand-authored Python source (GitHub issue #22).

Enforces one rule today -- **no orphan combining mark**: a string literal whose
first character is a Unicode combining mark. Written raw, such a mark renders as
an invisible or floating diacritic hanging off the opening quote -- unreadable in
an editor, un-diffable in review, and easily reintroduced by hand. The fix is a
named escape ``"\\N{UNICODE NAME}"`` (byte-identical at runtime, self-documenting,
plain ASCII in the file).

Why raw source, not the decoded AST value: Python decodes ``\\N{...}`` / ``\\uXXXX``
escapes when it builds the AST, so the *approved* escaped form and a *raw* orphan
mark produce the identical ``ast.Constant.value``. The distinction survives only
in the source bytes. So we locate string literals via the AST (precise: only real
literals, never a mark inside a comment) but test each literal's **raw source
segment** -- a leading escape ``\\`` is a base character and is accepted; a leading
raw combining mark is flagged.

The "first character of the literal" test is deliberate: it catches the floating
diacritic while leaving genuine Hebrew *text* data untouched. The one legitimate
case in the tree is a word in ``py/uxlc_fois/fois_mark_grammar_foi.py`` whose
combining accent follows a ZERO WIDTH JOINER mid-string -- the literal starts with
a base letter, so it is not flagged.

Shared harness: file discovery + a pluggable tuple of ``Check``s, each yielding
``Offense(relpath, line, codepoint, uname, detail)``. The sibling Unicode-hygiene
guard of issues #21/#26 (decomposed vs precomposed h-with-dot) plugs in as another
``Check`` reusing ``Offense`` / ``format_offense`` / ``scan``; only the detector
and the file set differ, not the mechanism.

Two entry points, one scanner:
  * ``tools/source_hygiene_test.py``   -- the standalone ``*_test.py`` guard.
  * ``python tools/source_hygiene.py`` -- the CLI the pre-commit hook runs; prints
                                          each offender and exits non-zero when the
                                          tree is dirty.

Escape hatch: a trailing ``# combining-ok`` on the offending line suppresses it,
for the rare case where a bare combining mark is genuinely the clearest form.
"""

import ast
import os
import sys
import unicodedata
from collections import namedtuple

Offense = namedtuple("Offense", "relpath line codepoint uname detail")

# Directory names pruned from the walk: Python's bytecode cache and the two
# vendored packages (kept byte-identical to upstream; not ours to police).
_PRUNED_DIRS = {"__pycache__", "mb_cmn", "mb_diff_mpu"}

# Roots of hand-authored Python source, relative to the repo root. Data and
# generated trees (in/, out/, gh-pages/, .novc/) are never under these, so they
# are excluded by construction.
_SOURCE_ROOTS = ("py", "tools")

# Legal string prefixes (r, b, f, u and case/combination variants) that may sit
# between the start of a literal's source segment and its opening quote.
_STRING_PREFIX_CHARS = "rbfuRBFU"

_PRAGMA = "# combining-ok"


def iter_source_files(repo_root):
    """Repo-relative paths of hand-authored ``*.py`` under ``py/`` and ``tools/``."""
    for root_name in _SOURCE_ROOTS:
        root = os.path.join(repo_root, root_name)
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in _PRUNED_DIRS]
            for name in filenames:
                if name.endswith(".py"):
                    full = os.path.join(dirpath, name)
                    yield os.path.relpath(full, repo_root).replace(os.sep, "/")


def _first_string_body_char(seg):
    """The first character *inside* a string literal's raw source ``seg``.

    Skips any string prefix and the opening quote (single or triple). Returns
    ``None`` if ``seg`` is not a plain quoted literal we can read.
    """
    i = 0
    while i < len(seg) and seg[i] in _STRING_PREFIX_CHARS:
        i += 1
    if seg[i : i + 3] in ('"""', "'''"):
        i += 3
    elif i < len(seg) and seg[i] in "\"'":
        i += 1
    else:
        return None
    return seg[i] if i < len(seg) else None


def find_orphan_combining_marks(relpath, text):
    """Yield an ``Offense`` per string literal whose raw source starts with a combining mark.

    Walks the AST so only real string *literals* are inspected, then reads each
    literal's raw source segment so an escaped mark (``\\N{...}`` / ``\\uXXXX``) is
    accepted and only a raw orphan mark is flagged. A trailing ``# combining-ok``
    on the line suppresses the finding.
    """
    lines = text.splitlines()
    tree = ast.parse(text, filename=relpath)
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        seg = ast.get_source_segment(text, node)
        if seg is None:
            continue
        ch = _first_string_body_char(seg)
        if ch is None or not unicodedata.combining(ch):
            continue
        line = node.lineno
        if _PRAGMA in lines[line - 1]:
            continue
        yield Offense(
            relpath=relpath,
            line=line,
            codepoint=f"U+{ord(ch):04X}",
            uname=unicodedata.name(ch, f"<unnamed U+{ord(ch):04X}>"),
            detail="orphan combining mark; use a \\N{NAME} escape",
        )


Check = namedtuple("Check", "name applies run")

# The pluggable check tuple. Sibling guards (issues #21/#26) add entries here.
CHECKS = (
    Check(
        name="orphan-combining-mark",
        applies=lambda relpath: relpath.endswith(".py"),
        run=find_orphan_combining_marks,
    ),
)


def scan(repo_root, files=None, checks=CHECKS):
    """Run every applicable check over ``files`` (default: the whole source tree).

    Returns the offenses sorted by ``(relpath, line, codepoint)``.
    """
    if files is None:
        files = iter_source_files(repo_root)
    offenses = []
    for relpath in files:
        with open(os.path.join(repo_root, relpath), encoding="utf-8") as f:
            text = f.read()
        for check in checks:
            if check.applies(relpath):
                offenses.extend(check.run(relpath, text))
    offenses.sort(key=lambda o: (o.relpath, o.line, o.codepoint))
    return offenses


def format_offense(offense):
    """``path:line  U+XXXX NAME`` -- the actionable one-line report."""
    return f"{offense.relpath}:{offense.line}  {offense.codepoint} {offense.uname}"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    offenses = scan(repo_root)
    if offenses:
        print("orphan combining marks in source (use \\N{NAME} escapes):")
        for offense in offenses:
            print("  " + format_offense(offense))
        print(f"\n{len(offenses)} offender(s). See GitHub issue #22.")
        return 1
    print("source_hygiene: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
