import json
import subprocess
import sys
import unicodedata
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
REL_PATHS = (
    "gh-pages/fois/features_of_interest-kq.json",
    "gh-pages/fois/features_of_interest-mark-grammar.json",
)
OUT_PATH = REPO_ROOT / ".novc" / "foi_unicode_diff.txt"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    lines = []
    for rel_path in REL_PATHS:
        old_obj = _load_committed_json(rel_path)
        new_obj = _load_worktree_json(rel_path)
        _compare(old_obj, new_obj, rel_path, lines)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


def _load_committed_json(rel_path):
    content = subprocess.check_output(
        ["git", "show", f"HEAD:{rel_path}"],
        cwd=REPO_ROOT,
        encoding="utf-8",
    )
    return json.loads(content)


def _load_worktree_json(rel_path):
    return json.loads((REPO_ROOT / rel_path).read_text(encoding="utf-8"))


def _compare(old_obj, new_obj, path, lines):
    if type(old_obj) is not type(new_obj):
        _record_scalar_diff(path, old_obj, new_obj, lines)
        return
    if isinstance(old_obj, dict):
        assert old_obj.keys() == new_obj.keys(), path
        for key in old_obj:
            _compare(old_obj[key], new_obj[key], f"{path}.{key}", lines)
        return
    if isinstance(old_obj, list):
        assert len(old_obj) == len(new_obj), path
        for idx, old_item in enumerate(old_obj):
            _compare(old_item, new_obj[idx], f"{path}[{idx}]", lines)
        return
    if old_obj != new_obj:
        _record_scalar_diff(path, old_obj, new_obj, lines)


def _record_scalar_diff(path, old_val, new_val, lines):
    lines.append(f"PATH: {path}")
    lines.append(f"OLD: {old_val!r}")
    lines.append(f"NEW: {new_val!r}")
    if isinstance(old_val, str) and isinstance(new_val, str):
        lines.append("OLD CODE POINTS:")
        lines.extend(_describe_string(old_val))
        lines.append("NEW CODE POINTS:")
        lines.extend(_describe_string(new_val))
    lines.append("")


def _describe_string(value):
    if value == "":
        return ["  <empty>"]
    rows = []
    for idx, char in enumerate(value):
        name = unicodedata.name(char, "<no name>")
        rows.append(f"  [{idx}] {char!r} U+{ord(char):04X} {name}")
    return rows


if __name__ == "__main__":
    main()
