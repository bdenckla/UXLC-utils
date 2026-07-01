"""Answer: at dt5:13 (ימים) and dt5:17 (תרצח), does WLC (the detangler's source) differ from
UXLC (CLC's source)? If so, the detangler's supplied-mark output is explained by its INPUT,
not by any 'grammar engine' story. Dumps, per verse: UXLC atoms, the WLC verse text, the two
MAM strands, and the wlc-utils detangler's supplied_marks records (wlc_word / mam_word). UTF-8."""

import json
import sys
import unicodedata
from pathlib import Path

_UXLC = Path(r"C:\Users\BenDe\GitRepos\UXLC-utils")
_WLC = Path(r"C:\Users\BenDe\GitRepos\wlc-utils")
sys.path.insert(0, str(_UXLC / "py"))
sys.path.insert(0, str(_WLC / "py"))

import clc.clc_read as clc_read  # noqa: E402
import mb_cmn.hebrew_accents as acc  # noqa: E402
import mb_cmn.hebrew_letters as hl  # noqa: E402
import mb_cmn.hebrew_points as hpo  # noqa: E402
import mb_cmn.hebrew_punctuation as hpu  # noqa: E402
from accgram import rtms_data  # noqa: E402

_CGJ = "\N{COMBINING GRAPHEME JOINER}"
_NAME = {}
for _pfx, _mod in (("acc", acc), ("hpo", hpo), ("hpu", hpu), ("hl", hl)):
    for _n, _v in vars(_mod).items():
        if _n.isupper() and isinstance(_v, str) and len(_v) == 1:
            _NAME.setdefault(_v, f"{_pfx}.{_n}")
_NAME[_CGJ] = "_CGJ"
_BASE_LO, _BASE_HI = 0x05D0, 0x05EA


def _is_base(ch):
    return _BASE_LO <= ord(ch) <= _BASE_HI


def _spell(s):
    return " + ".join(
        f"{_NAME.get(ch, 'U+%04X' % ord(ch))}{'' if _is_base(ch) else '<mark>'}" for ch in s
    ) or "(empty)"


def _marks(s):
    return _spell("".join(ch for ch in s if not _is_base(ch)))


out = []
wlc_dir = rtms_data.default_wlc422_kq_u_dir(_WLC)
wlc_index = rtms_data.load_wlc422_index(wlc_dir)
strands = json.loads((_UXLC / ".novc" / "mam_strands.json").read_text("utf-8"))
dual = json.loads((_WLC / "out" / "accgram" / "dual-cant" / "_dual_cant.json").read_text("utf-8"))

# supplied_marks across all passages, keyed by bcv
sup_by_bcv = {}
for p in dual.get("passages", []):
    for s in p.get("supplied_marks", []):
        sup_by_bcv.setdefault(s["bcv"], []).append(s)

book = clc_read.read_book("Deuter")
for ch, v, target_i, gloss in ((5, 13, 2, "ימים"), (5, 17, 2, "תרצח")):
    out.append(f"================ dt{ch}:{v}  (target atom {target_i} = {gloss}) ================")
    uxlc_atoms = [a["text"] for a in book[ch - 1][v - 1]]
    wlc_text = rtms_data.verse_unicode_text(wlc_index, "dt", ch, v)
    wlc_words = wlc_text.split()
    s = strands[f"dt{ch}:{v}"]
    out.append(f"  UXLC atoms ({len(uxlc_atoms)}): {' | '.join(uxlc_atoms)}")
    out.append(f"  WLC  words ({len(wlc_words)}): {' | '.join(wlc_words)}")
    ti = target_i - 1
    ux = uxlc_atoms[ti] if ti < len(uxlc_atoms) else "(missing)"
    wl = wlc_words[ti] if ti < len(wlc_words) else "(missing)"
    al = s["alef"][ti] if ti < len(s["alef"]) else "(missing)"
    be = s["bet"][ti] if ti < len(s["bet"]) else "(missing)"
    out.append(f"  -- target word {gloss} --")
    out.append(f"     UXLC   {ux}   marks: {_marks(ux)}")
    out.append(f"     WLC    {wl}   marks: {_marks(wl)}")
    out.append(f"     MAM-alef {al}   marks: {_marks(al)}")
    out.append(f"     MAM-bet  {be}   marks: {_marks(be)}")
    out.append(f"     UXLC vs WLC identical? {ux == wl}")
    out.append("  detangler supplied_marks for this verse:")
    for sm in sup_by_bcv.get(f"dt{ch}:{v}", []):
        out.append(f"     strand={sm.get('strand')}/{sm.get('strand_label')} "
                   f"accent={sm.get('accent_name')} source={sm.get('source')}")
        out.append(f"       wlc_word={sm.get('wlc_word')!r}  marks: {_marks(sm.get('wlc_word',''))}")
        out.append(f"       mam_word={sm.get('mam_word')!r}  marks: {_marks(sm.get('mam_word',''))}")
    if not sup_by_bcv.get(f"dt{ch}:{v}"):
        out.append("     (none reported)")
    out.append("")

(_UXLC / ".novc" / "wlc_vs_uxlc.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote .novc/wlc_vs_uxlc.txt")
