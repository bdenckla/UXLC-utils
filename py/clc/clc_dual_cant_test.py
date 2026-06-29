"""Self-contained test for clc_dual_cant (the first CLC test module).

Run from anywhere:  python py/clc/clc_dual_cant_test.py
Prints "clc_dual_cant: OK" on success; raises AssertionError on failure.

It reads Genesis 35:22 straight from the UXLC XML (paths derived from __file__,
so it is independent of cwd and of the my_uxlc reader), then checks the split is
**near-subtractive with two narrow charities**: each strand is the combined text
with only the *other* reading's divergence cluster resolved — position-safely, so
a mark that recurs elsewhere as a shared mark is never touched — plus, for the
alef strand, a *supplied* sof-pasuq held in ``atom["additions"]`` (bracketed/green
in the render), never folded into the strand text. Synthetic ``split_word`` cases
pin the position-safety for QUPO (two vowels) and rafe+dagesh divergences.
"""

import os
import sys
import xml.etree.ElementTree as ET

_HERE = os.path.dirname(os.path.abspath(__file__))
_PY_ROOT = os.path.dirname(_HERE)            # py/
_REPO_ROOT = os.path.dirname(_PY_ROOT)       # repo root
sys.path.insert(0, _PY_ROOT)

import clc.clc_dual_cant as dc  # noqa: E402
import clc.clc_render as clc_render  # noqa: E402
import mb_cmn.hebrew_accents as acc  # noqa: E402
import mb_cmn.hebrew_letters as hl  # noqa: E402
import mb_cmn.hebrew_points as hpo  # noqa: E402
import mb_cmn.hebrew_punctuation as hpu  # noqa: E402
import uxlc_misc.uxlc_utils_html as H  # noqa: E402

_XML = os.path.join(_REPO_ROOT, "in", "UXLC-39", "Genesis.xml")

_CGJ = "͏"
_METEG = hpo.MTGOSLQ
_SOF_PASUQ = hpu.SOPA
_MAQAF = hpu.MAQ
_RAFE = hpo.RAFE
_DAGESH = hpo.DAGOMOSD
_PATAX = hpo.PATAX
_QAMATS = hpo.QAMATS

# Codepoints a strict split may delete from a divergence cluster: cantillation
# accents (U+0591–U+05AF), meteg, the CGJ, and — new with QUPO / rafe+dagesh —
# the vowels/points that can themselves diverge. This is only the subsequence
# *floor* (_is_strict_deletion); divergence atoms are pinned exactly below.
_REMOVABLE = (
    {chr(cp) for cp in range(0x0591, 0x05B0)}
    | {_CGJ, _METEG, _RAFE, _DAGESH, _PATAX, _QAMATS}
)

# Independent reference for the accent-only split of Gen 35:22's divergence atoms
# (the prior behaviour). atom_index -> (alef_only, bet_only).
_OLD = {
    7: (acc.ZAQ_Q, acc.REV),
    8: (acc.ZAQ_G, acc.PASH),
    10: (acc.TIP, acc.PASH),
    12: (acc.ATN, acc.ZAQ_Q),
    14: (_METEG, acc.ATN),
}


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


def _old_split(text, atom_index, strand):
    """Accent-only set-membership split — the independent oracle the new
    cluster-replace must reproduce on the real Gen 35:22 atoms."""
    alef_only, bet_only = _OLD[atom_index]
    drop = set(_CGJ)
    drop.update(bet_only if strand == "alef" else alef_only)
    return "".join(ch for ch in text if ch not in drop)


def _is_strict_deletion(combined, strand):
    """True iff `strand` is `combined` with only removable chars deleted (order kept)."""
    si = 0
    for ch in combined:
        if si < len(strand) and strand[si] == ch:
            si += 1
        elif ch not in _REMOVABLE:
            return False  # a non-removable char (letter/maqaf/sof-pasuq) vanished
    return si == len(strand)  # every strand char was matched (nothing added/reordered)


def _count(text, ch):
    return sum(c == ch for c in text)


def _render(pieces):
    return "".join(H.el_to_str_no_wbr(p) for p in pieces)


def test_is_dual_cant():
    assert dc.is_dual_cant("Genesis", 35, 22)
    assert not dc.is_dual_cant("Genesis", 35, 21)
    assert not dc.is_dual_cant("Proverbs", 35, 22)


def test_split_word_core():
    zaqef, revia = acc.ZAQ_Q, acc.REV
    combined = "ר" + zaqef + revia + "ן"  # base + two stacked accents
    entry = {"cluster": zaqef + revia, "alef": zaqef, "bet": revia}
    assert dc.split_word(combined, entry, "alef") == "ר" + zaqef + "ן"
    assert dc.split_word(combined, entry, "bet") == "ר" + revia + "ן"

    # Atom-14 shape: etnahta + CGJ + meteg. Each strand keeps one accent, drops
    # the other *and* the now-orphaned CGJ — all inside the one cluster.
    etnahta = acc.ATN
    c14 = "א" + etnahta + _CGJ + _METEG + "ל"
    entry14 = {"cluster": etnahta + _CGJ + _METEG, "alef": _METEG, "bet": etnahta}
    assert dc.split_word(c14, entry14, "alef") == "א" + _METEG + "ל"
    assert dc.split_word(c14, entry14, "bet") == "א" + etnahta + "ל"


def test_split_word_position_safe_qupo():
    # A QUPO letter carries patax + qamats + two accents; the SAME word also has a
    # shared patax EARLIER. A set-membership "drop patax" (the old approach) would
    # delete that shared patax too; cluster-replace touches only the cluster.
    acc_a, acc_b = acc.MAH, acc.QOM          # two arbitrary distinct accents
    carrier = hl.LAMED
    cluster = carrier + _PATAX + _QAMATS + acc_a + acc_b
    word = hl.KAF + _PATAX + cluster + hl.FMEM  # shared patax on kaf, then QUPO lamed
    entry = {"cluster": cluster, "alef": carrier + _PATAX + acc_a,
             "bet": carrier + _QAMATS + acc_b}
    alef = dc.split_word(word, entry, "alef")
    bet = dc.split_word(word, entry, "bet")
    assert alef == hl.KAF + _PATAX + carrier + _PATAX + acc_a + hl.FMEM
    assert bet == hl.KAF + _PATAX + carrier + _QAMATS + acc_b + hl.FMEM
    assert _count(alef, _PATAX) == 2 and _count(bet, _PATAX) == 1  # shared patax safe
    assert _count(bet, _QAMATS) == 1


def test_split_word_position_safe_rafe_dagesh():
    # A tav carries rafe + dagesh; a shared dagesh sits EARLIER in the word. The
    # bet strand drops the cluster's dagesh (keeps rafe) — but the shared dagesh
    # must survive, which set-membership dropping would not guarantee.
    carrier = hl.TAV
    cluster = carrier + _DAGESH + _RAFE
    word = hl.BET + _DAGESH + cluster + hl.HE  # shared dagesh on bet, then tav
    entry = {"cluster": cluster, "alef": carrier + _DAGESH, "bet": carrier + _RAFE}
    alef = dc.split_word(word, entry, "alef")
    bet = dc.split_word(word, entry, "bet")
    assert alef == hl.BET + _DAGESH + carrier + _DAGESH + hl.HE
    assert bet == hl.BET + _DAGESH + carrier + _RAFE + hl.HE
    assert _count(alef, _DAGESH) == 2 and _count(bet, _DAGESH) == 1  # shared dagesh safe
    assert _count(bet, _RAFE) == 1


def test_strand_views_strict():
    combined = _read_combined_atoms()
    assert len(combined) == 19, f"expected 19 atoms, got {len(combined)}"

    views = dc.strand_views("Genesis", 35, 22, combined)
    assert [v.suffix for v in views] == ["C", "א", "ב"]

    c_view, alef_view, bet_view = views
    assert c_view.atoms is combined  # combined form is unchanged

    divergence = {7, 8, 10, 12, 14}  # 1-based atom indices
    whole_combined = "".join(a["text"] for a in combined)
    for view, strand in ((alef_view, "alef"), (bet_view, "bet")):
        assert len(view.atoms) == len(combined)
        whole_text = "".join(a["text"] for a in view.atoms)
        # The *subtracted* text invents/loses no division marks — supplied marks
        # live out-of-band in atom["additions"], never folded into the text.
        assert _count(whole_text, _SOF_PASUQ) == _count(whole_combined, _SOF_PASUQ) == 1
        assert _count(whole_text, _MAQAF) == _count(whole_combined, _MAQAF) == 2
        for i, (co, st) in enumerate(zip(combined, view.atoms), start=1):
            assert _is_strict_deletion(co["text"], st["text"]), f"atom {i} not a strict deletion"
            if i not in divergence:
                assert st["text"] == co["text"], f"atom {i} should be untouched"
                assert "additions" not in st, f"untouched atom {i} should stay identical"
            else:
                assert st["text"] != co["text"], f"atom {i} should differ (divergence)"
                assert st["text"] == _old_split(co["text"], i, strand), f"atom {i} text"
        # Rendered marks = subtracted text + supplied marks: only alef gains a
        # sof-pasuq (pashuṭ chants Gen 35:22 as two verses).
        supplied = [ch for a in view.atoms for ch in a.get("additions", ())]
        rendered = whole_text + "".join(supplied)
        assert _count(rendered, _SOF_PASUQ) == 1 + (1 if strand == "alef" else 0)

    # The supplied sof-pasuq is metadata on alef atom 14 only — in no strand text.
    assert alef_view.atoms[13]["additions"] == [_SOF_PASUQ]
    assert bet_view.atoms[13]["additions"] == []
    assert _SOF_PASUQ not in alef_view.atoms[13]["text"]

    # Pin the headline divergence words by accent identity.
    zaqef, revia, etnahta = acc.ZAQ_Q, acc.REV, acc.ATN
    assert revia not in alef_view.atoms[6]["text"] and zaqef in alef_view.atoms[6]["text"]  # רְאוּבֵן
    assert zaqef not in bet_view.atoms[6]["text"] and revia in bet_view.atoms[6]["text"]
    # Atom 14 (יִשְׂרָאֵל): alef keeps meteg (no etnahta, no CGJ, no sof-pasuq in text);
    # bet keeps etnahta (no meteg, no CGJ).
    a14, b14 = alef_view.atoms[13]["text"], bet_view.atoms[13]["text"]
    assert _METEG in a14 and etnahta not in a14 and _CGJ not in a14 and _SOF_PASUQ not in a14
    assert etnahta in b14 and _METEG not in b14 and _CGJ not in b14


def test_added_render():
    combined = _read_combined_atoms()
    _c, alef_view, bet_view = dc.strand_views("Genesis", 35, 22, combined)

    # The supplied sof-pasuq renders bracketed, the mark itself in the green
    # "added" class, in the alef strand's text column.
    alef_html = _render(clc_render._plain_text_contents(alef_view.atoms, combined))
    assert "clc-added-during-detangling" in alef_html
    assert _SOF_PASUQ in alef_html and "[" in alef_html and "]" in alef_html
    # bet supplies nothing → no green span.
    bet_html = _render(clc_render._plain_text_contents(bet_view.atoms, combined))
    assert "clc-added-during-detangling" not in bet_html

    # The synthesized doc-column note carries the exact template prose, the
    # snippet, and the bracketed/green mark.
    assert len(alef_view.added_notes) == 1
    note_html = H.el_to_str_no_wbr(clc_render._added_note_block(alef_view.added_notes[0]))
    assert "sof pasuq in " in note_html
    assert "added out of thin air, to improve legibility" in note_html
    assert "clc-added-during-detangling" in note_html
    assert bet_view.added_notes == ()


def main():
    test_is_dual_cant()
    test_split_word_core()
    test_split_word_position_safe_qupo()
    test_split_word_position_safe_rafe_dagesh()
    test_strand_views_strict()
    test_added_render()
    print("clc_dual_cant: OK")


if __name__ == "__main__":
    main()
