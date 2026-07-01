"""Decode the rafe/dagesh divergence atoms (and the accent that drives them) to a UTF-8 file.

The deferred rafe/dagesh group of the Decalogue dual-cant detangler: words where the two
readings disagree on whether a בגדכפת letter is hard (dagesh) or soft (rafe). The split
is almost always GRAMMATICAL — a letter is hard after a disjunctive accent (pause) on the
previous word, soft after a conjunctive one — so this dumps, per atom: UXLC's combined
bytes, MAM's cant-alef and cant-bet bytes (named codepoint-by-codepoint), AND the previous
atom's marks in each reading, so the conjunctive/disjunctive driver is visible.

Run from repo root: python .novc/inspect_rafe_dagesh.py  ->  .novc/rafe_dagesh.txt
"""

import json
import sys
import unicodedata
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "py"))

import clc.clc_read as clc_read  # noqa: E402
import mb_cmn.hebrew_accents as acc  # noqa: E402
import mb_cmn.hebrew_letters as hl  # noqa: E402
import mb_cmn.hebrew_points as hpo  # noqa: E402
import mb_cmn.hebrew_punctuation as hpu  # noqa: E402

_CGJ = "\N{COMBINING GRAPHEME JOINER}"
_STRANDS = json.loads((_REPO / ".novc" / "mam_strands.json").read_text("utf-8"))

# codepoint -> mb_cmn constant name, for legibility.
_NAME = {}
for _pfx, _mod in (("acc", acc), ("hpo", hpo), ("hpu", hpu), ("hl", hl)):
    for _n, _v in vars(_mod).items():
        if _n.isupper() and isinstance(_v, str) and len(_v) == 1:
            _NAME.setdefault(_v, f"{_pfx}.{_n}")
_NAME[_CGJ] = "_CGJ"

_BASE_LO, _BASE_HI = 0x05D0, 0x05EA


def _is_base(ch):
    return _BASE_LO <= ord(ch) <= _BASE_HI


def _decode(word):
    """word -> 'char U+XXXX const/unicodename' lines, marks flagged."""
    out = []
    for ch in word:
        const = _NAME.get(ch, "")
        uname = unicodedata.name(ch, "?")
        tag = "" if _is_base(ch) else "   <- mark"
        out.append(f"      {ch!r:>6} U+{ord(ch):04X}  {const:14} {uname}{tag}")
    return "\n".join(out)


def _marks(word):
    return [ch for ch in word if not _is_base(ch)]


def _spell(chars):
    return " + ".join(_NAME.get(c, f"U+{ord(c):04X}") for c in chars) or "(none)"


# (book39, bb, ch, v, atom_index_1based, gloss) — the rafe/dagesh divergence atoms,
# with the previous atom (the accent driver) shown alongside.
_ATOMS = [
    ("Exodus", "ex", 20, 9, 5, "כל (prev: ועשית)"),
    ("Exodus", "ex", 20, 13, 2, "תרצח (prev: לא)"),
    ("Exodus", "ex", 20, 14, 2, "תנאף (prev: לא)"),
    ("Exodus", "ex", 20, 15, 2, "תגנב (prev: לא)"),
    ("Deuter", "dt", 5, 13, 5, "כל (prev: ועשית)"),
    ("Deuter", "dt", 5, 17, 2, "תרצח (prev: לא)"),
    ("Deuter", "dt", 5, 18, 2, "תנאף (prev: לא)"),
    ("Deuter", "dt", 5, 19, 2, "תגנב (prev: לא)"),
]

_OUT = []


def emit(s=""):
    _OUT.append(s)


def main():
    for bk39, bb, ch, v, ai, gloss in _ATOMS:
        book = clc_read.read_book(bk39)
        uxlc = [a["text"] for a in book[ch - 1][v - 1]]
        s = _STRANDS[f"{bb}{ch}:{v}"]
        alef, bet = s["alef"], s["bet"]
        i = ai - 1
        emit(f"===== {bb}{ch}:{v} atom {ai}: {gloss} =====")
        for label, word in (("UXLC ", uxlc[i]), ("alef ", alef[i]), ("bet  ", bet[i])):
            emit(f"  {label} {word}")
            emit(_decode(word))
        emit(f"  divergence: alef-marks={_spell(_marks(alef[i]))}  "
             f"bet-marks={_spell(_marks(bet[i]))}")
        if i >= 1:  # the previous word's accent: the conjunctive/disjunctive driver
            emit(f"  PREV atom {ai-1}: uxlc={uxlc[i-1]}  "
                 f"alef-marks={_spell(_marks(alef[i-1]))}  bet-marks={_spell(_marks(bet[i-1]))}")
        emit()
    out = _REPO / ".novc" / "rafe_dagesh.txt"
    out.write_text("\n".join(_OUT), encoding="utf-8")
    print(f"wrote {out} ({len(_OUT)} lines)")


if __name__ == "__main__":
    main()
