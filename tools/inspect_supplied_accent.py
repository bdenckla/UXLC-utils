"""Dump the SUPPLIED-ACCENT divergence verses for hand adjudication (Ben's cantillation call).

For each of dt5:6, dt5:13, dt5:17 (the supplied-accent group) and dt5:8 (the WLC
merkha-for-qadma anomaly), print per atom: UXLC's combined marks, MAM's cant-alef and
cant-bet marks (named), and — computed the SAME way gen_entry does — the markset diff:
which marks are alef-only / bet-only, and for each whether UXLC HAS it (a plain
subtraction) or LACKS it (a SUPPLIED mark, and to which strand). The point is to see,
on the data, exactly which accent must be supplied to which reading.

Run from repo root: python .novc/inspect_supplied_accent.py  ->  .novc/supplied_accent.txt
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
from mb_cmn import str_defs as sd  # noqa: E402

_CGJ = sd.CGJ
_TSINNORIT = acc.ZSH_OR_TSIT
_STRANDS = json.loads((_REPO / ".novc" / "mam_strands.json").read_text("utf-8"))

# codepoint -> mb_cmn constant name, for legibility.
_NAME = {}
for _pfx, _mod in (("acc", acc), ("hpo", hpo), ("hpu", hpu), ("hl", hl)):
    for _n, _v in vars(_mod).items():
        if _n.isupper() and isinstance(_v, str) and len(_v) == 1:
            _NAME.setdefault(_v, f"{_pfx}.{_n}")
_NAME[_CGJ] = "_CGJ"
_NAME[_TSINNORIT] = "tsinnorit"

_BASE_LO, _BASE_HI = 0x05D0, 0x05EA


def _is_base(ch):
    return _BASE_LO <= ord(ch) <= _BASE_HI


def _spell(chars):
    return " + ".join(_NAME.get(c, f"U+{ord(c):04X}") for c in chars) or "(none)"


def _markset(word):
    """Same as gen_entry._mam_markset: marks only, minus tsinnorit + CGJ."""
    return {ch for ch in word if not _is_base(ch) and ch != _TSINNORIT and ch != _CGJ}


# verses to adjudicate: the supplied-accent group + the dt5:8 anomaly.
_VERSES = [
    ("Deuter", "dt", 5, 6, "אנכי... (elyon chants vv.6-? as one; UXLC wrote taḥton accents)"),
    ("Deuter", "dt", 5, 13, "שֵׁשֶׁת ימים... (Sabbath; alef PASHTA on ימים?)"),
    ("Deuter", "dt", 5, 17, "לא תרצח (elyon SILLUQ on תרצח?)"),
    ("Deuter", "dt", 5, 8, "ANOMALY: WLC merkha-for-qadma"),
]

_OUT = []


def emit(s=""):
    _OUT.append(s)


def main():
    for bk39, bb, ch, v, gloss in _VERSES:
        book = clc_read.read_book(bk39)
        uxlc = [a["text"] for a in book[ch - 1][v - 1]]
        s = _STRANDS[f"{bb}{ch}:{v}"]
        alef, bet = s["alef"], s["bet"]
        emit(f"================ {bb}{ch}:{v}  {gloss} ================")
        emit(f"  counts: uxlc={len(uxlc)} alef={len(alef)} bet={len(bet)}")
        if not (len(uxlc) == len(alef) == len(bet)):
            emit("  !! COUNT MISMATCH — atoms do not 1:1 align; skipping per-atom diff")
            emit("")
            continue
        for i, (ua, a, b) in enumerate(zip(uxlc, alef, bet), start=1):
            ua_set, a_set, b_set = _markset(ua), _markset(a), _markset(b)
            alef_only = a_set - b_set
            bet_only = b_set - a_set
            if not (alef_only or bet_only):
                continue  # shared marks only — not a divergence atom
            emit(f"  -- atom {i:2d}  uxlc={ua}   alef={a}   bet={b}")
            emit(f"       uxlc-marks: {_spell(sorted(ua_set, key=ord))}")
            emit(f"       alef-marks: {_spell(sorted(a_set, key=ord))}")
            emit(f"       bet -marks: {_spell(sorted(b_set, key=ord))}")
            for label, only in (("alef", alef_only), ("bet", bet_only)):
                for m in sorted(only, key=ord):
                    has = "in UXLC (subtract)" if m in ua else ">>> SUPPLIED (UXLC lacks it)"
                    emit(f"       {label}-only {_NAME.get(m, hex(ord(m))):14} {has}")
        emit()
    out = _REPO / ".novc" / "supplied_accent.txt"
    out.write_text("\n".join(_OUT), encoding="utf-8")
    print(f"wrote {out} ({len(_OUT)} lines)")


if __name__ == "__main__":
    main()
