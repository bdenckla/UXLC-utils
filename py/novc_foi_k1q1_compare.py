import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
BASE_COMMIT = "6d9f248"
OUT_PATH = REPO_ROOT / ".novc" / "foi_k1q1_compare.txt"

sys.path.insert(0, str(REPO_ROOT))

import main_fois
import py_misc.my_uxlc as my_uxlc
import py_misc.my_tanakh_book_names as tbn


def main():
    current_cases = _all_k1q1_cases(_current_books())
    old_cases = _all_k1q1_cases(_books_from_commit(BASE_COMMIT))
    only_current = sorted(current_cases - old_cases)
    only_old = sorted(old_cases - current_cases)
    lines = [
        f"BASE_COMMIT: {BASE_COMMIT}",
        f"OLD_COUNT: {len(old_cases)}",
        f"NEW_COUNT: {len(current_cases)}",
        f"ONLY_CURRENT: {len(only_current)}",
        f"ONLY_OLD: {len(only_old)}",
        "",
        "ONLY_CURRENT_CASES:",
    ]
    lines.extend(_fmt_case(case) for case in only_current)
    lines.append("")
    lines.append("ONLY_OLD_CASES:")
    lines.extend(_fmt_case(case) for case in only_old)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


def _current_books():
    return my_uxlc.read_all_books(main_fois._VERSE_CHILD_HANDLERS)


def _books_from_commit(commit):
    books = {}
    for bkid in tbn.ALL_BOOK_IDS:
        basename = my_uxlc._UXLC_BOOK_FILE_NAMES[bkid]
        xml_text = _read_xml_from_commit(commit, basename)
        root = ET.fromstring(xml_text)
        books[bkid] = _read_book_root(root)
    return books


def _read_xml_from_commit(commit, basename):
    rel_paths = [f"in/UXLC-39/{basename}.xml", f"in/UXLC/{basename}.xml"]
    for rel_path in rel_paths:
        try:
            return subprocess.check_output(
                ["git", "show", f"{commit}:{rel_path}"],
                cwd=REPO_ROOT,
                encoding="utf-8",
            )
        except subprocess.CalledProcessError:
            pass
    raise FileNotFoundError(basename)


def _read_book_root(root):
    chapters = []
    for chapter in root.iter("c"):
        verses = []
        for verse in chapter.iter("v"):
            atoms = []
            for verse_child in verse:
                my_uxlc.dispatch_on_tag(
                    atoms, verse_child, main_fois._VERSE_CHILD_HANDLERS
                )
            verses.append(atoms)
        chapters.append(verses)
    return chapters


def _all_k1q1_cases(books):
    cases = set()
    for bkid, chapters in books.items():
        for chidx, chapter in enumerate(chapters):
            for vridx, verse in enumerate(chapter):
                bcv = bkid, chidx + 1, vridx + 1
                cases.update(_k1q1_cases_for_verse(bcv, verse))
    return cases


def _k1q1_cases_for_verse(bcv, verse):
    cases = set()
    state = {"k_stack": [], "q_stack": [], "bcvp": None}
    for atidx, atom in enumerate(verse):
        bcvp = (*bcv, atidx + 1)
        kind, text = atom
        if kind == "w":
            _maybe_record_case(cases, state)
            _clear_state(state)
            continue
        if kind == "k":
            if state["q_stack"]:
                _maybe_record_case(cases, state)
                _clear_state(state)
            state["k_stack"].append(text)
            state["bcvp"] = bcvp
            continue
        if kind == "q":
            state["q_stack"].append(text)
            state["bcvp"] = bcvp
            continue
        raise AssertionError(kind)
    _maybe_record_case(cases, state)
    return cases


def _maybe_record_case(cases, state):
    if len(state["k_stack"]) == 1 and len(state["q_stack"]) == 1:
        cases.add(
            (
                _bcvp_str(state["bcvp"]),
                state["k_stack"][0],
                state["q_stack"][0],
            )
        )


def _clear_state(state):
    state["k_stack"] = []
    state["q_stack"] = []
    state["bcvp"] = None


def _bcvp_str(bcvp):
    bkid, chnu, vrnu, atnu = bcvp
    return f"{bkid} {chnu}:{vrnu}.{atnu}"


def _fmt_case(case):
    if not case:
        return "<none>"
    bcvp, ketiv, qere = case
    return f"{bcvp} | k={ketiv!r} | q={qere!r}"


if __name__ == "__main__":
    main()
