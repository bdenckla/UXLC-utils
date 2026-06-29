"""Self-contained test for clc_dual_cant (the first CLC test module).

Run from anywhere:  python py/clc/clc_dual_cant_test.py
Prints "clc_dual_cant: OK" on success; raises AssertionError on failure.

It reads Genesis 35:22 straight from the UXLC XML (paths derived from __file__,
so it is independent of cwd and of the my_uxlc reader), then checks that the
strand split is **strictly subtractive**: each strand is the combined text with
only the *other* reading's accent(s) (and any CGJ) deleted — nothing supplied,
no vowel/maqaf/sof-pasuq added or removed, no re-division.
"""

import os
import sys
import xml.etree.ElementTree as ET

_HERE = os.path.dirname(os.path.abspath(__file__))
_PY_ROOT = os.path.dirname(_HERE)            # py/
_REPO_ROOT = os.path.dirname(_PY_ROOT)       # repo root
sys.path.insert(0, _PY_ROOT)

import clc.clc_dual_cant as dc  # noqa: E402

_XML = os.path.join(_REPO_ROOT, "in", "UXLC-39", "Genesis.xml")

# Codepoints removable by a strict split: cantillation accents (U+0591–U+05AF),
# the meteg (U+05BD, a divergence mark at Gen 35:22 atom 14) and the CGJ.
_CGJ = "͏"
_METEG = "ֽ"
_SOF_PASUQ = "׃"
_MAQAF = "־"
_REMOVABLE = {chr(cp) for cp in range(0x0591, 0x05B0)} | {_CGJ, _METEG}


def _read_combined_atoms():
    """Gen 35:22 as clc_read-shaped atoms, parsed directly from the UXLC XML."""
    root = ET.parse(_XML).getroot()
    for c in root.iter("c"):
        if c.get("n") != "35":
            continue
        for v in c.iter("v"):
            if v.get("n") != "22":
                continue
            return [
                {"kind": "w", "text": (w.text or "").strip(), "types": []}
                for w in v
                if w.tag == "w"
            ]
    raise AssertionError("Genesis 35:22 not found in UXLC XML")


def _is_strict_deletion(combined, strand):
    """True iff `strand` is `combined` with only removable chars deleted (order kept)."""
    si = 0
    for ch in combined:
        if si < len(strand) and strand[si] == ch:
            si += 1
        elif ch not in _REMOVABLE:
            return False  # a non-removable char (letter/vowel/maqaf/sof-pasuq) vanished
    return si == len(strand)  # every strand char was matched (nothing added/reordered)


def _count(text, ch):
    return sum(c == ch for c in text)


def test_is_dual_cant():
    assert dc.is_dual_cant("Genesis", 35, 22)
    assert not dc.is_dual_cant("Genesis", 35, 21)
    assert not dc.is_dual_cant("Proverbs", 35, 22)


def test_split_word_core():
    zaqef, revia = "֔", "֗"
    combined = "ר" + zaqef + revia + "ן"  # base + two stacked accents
    assert dc.split_word(combined, zaqef, revia, "alef") == "ר" + zaqef + "ן"
    assert dc.split_word(combined, zaqef, revia, "bet") == "ר" + revia + "ן"

    # Atom-14 shape: etnahta + CGJ + meteg. Each strand keeps one accent, drops
    # the other *and* the now-orphaned CGJ.
    etnahta = "֑"
    c14 = "א" + etnahta + _CGJ + _METEG + "ל"
    assert dc.split_word(c14, _METEG, etnahta, "alef") == "א" + _METEG + "ל"
    assert dc.split_word(c14, _METEG, etnahta, "bet") == "א" + etnahta + "ל"


def test_strand_views_strict():
    combined = _read_combined_atoms()
    assert len(combined) == 19, f"expected 19 atoms, got {len(combined)}"

    views = dc.strand_views("Genesis", 35, 22, combined)
    assert [v.suffix for v in views] == ["C", "א", "ב"]

    c_view, alef_view, bet_view = views
    assert c_view.atoms is combined  # combined form is unchanged

    divergence = {7, 8, 10, 12, 14}  # 1-based atom indices
    for view in (alef_view, bet_view):
        assert len(view.atoms) == len(combined)
        whole_combined = "".join(a["text"] for a in combined)
        whole_strand = "".join(a["text"] for a in view.atoms)
        # No division marks invented or lost, across the whole verse:
        assert _count(whole_strand, _SOF_PASUQ) == _count(whole_combined, _SOF_PASUQ) == 1
        assert _count(whole_strand, _MAQAF) == _count(whole_combined, _MAQAF) == 2
        for i, (co, st) in enumerate(zip(combined, view.atoms), start=1):
            assert _is_strict_deletion(co["text"], st["text"]), f"atom {i} not a strict deletion"
            if i not in divergence:
                assert st["text"] == co["text"], f"atom {i} should be untouched"
            else:
                assert st["text"] != co["text"], f"atom {i} should differ (divergence)"

    # Pin the headline divergence words by accent identity.
    zaqef, revia, etnahta = "֔", "֗", "֑"
    assert revia not in alef_view.atoms[6]["text"] and zaqef in alef_view.atoms[6]["text"]  # רְאוּבֵן
    assert zaqef not in bet_view.atoms[6]["text"] and revia in bet_view.atoms[6]["text"]
    # Atom 14 (יִשְׂרָאֵל): alef keeps meteg (no etnahta, no CGJ, no sof-pasuq added);
    # bet keeps etnahta (no meteg, no CGJ).
    a14, b14 = alef_view.atoms[13]["text"], bet_view.atoms[13]["text"]
    assert _METEG in a14 and etnahta not in a14 and _CGJ not in a14 and _SOF_PASUQ not in a14
    assert etnahta in b14 and _METEG not in b14 and _CGJ not in b14 and _SOF_PASUQ not in b14


def main():
    test_is_dual_cant()
    test_split_word_core()
    test_strand_views_strict()
    print("clc_dual_cant: OK")


if __name__ == "__main__":
    main()
