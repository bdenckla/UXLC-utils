"""Self-contained test for clc_dual_cant (the first CLC test module).

Run from anywhere:  python py/clc/clc_dual_cant_test.py
Prints "clc_dual_cant: OK" on success; raises AssertionError on failure.

It reads Genesis 35:22 straight from the UXLC XML (paths derived from __file__,
so it is independent of cwd and of the my_uxlc reader), then checks the split is
**near-subtractive with two narrow charities**: each strand is the combined text
with only the *other* strand's divergence cluster resolved — position-safely, so
a mark that recurs elsewhere as a shared mark is never touched — plus, for the
alef strand, a *supplied* sof-pasuq held in ``atom["additions"]`` (bracketed/green
in the render), never folded into the strand text. Synthetic ``split_word`` cases
pin the position-safety for QUPO (two vowels) and rafe+dagesh divergences; the
QUPO case is also now proven on real data (ex 20:3 / dt 5:7's atom 7 פני, the only
QUPO-vowel Decalogue verses — see ``test_decalogue_qupo_vowel_split``).
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
from mb_cmn import str_defs as sd  # noqa: E402
import uxlc_misc.uxlc_utils_html as H  # noqa: E402

_XML = os.path.join(_REPO_ROOT, "in", "UXLC-39", "Genesis.xml")

_CGJ = sd.CGJ
_METEG = hpo.MTGOSLQ
_SOF_PASUQ = hpu.SOPA
_MAQAF = hpu.MAQ
_RAFE = hpo.RAFE
_DAGESH = hpo.DAGOMOSD
_PATAX = hpo.PATAX
_QAMATS = hpo.QAMATS
_PASOLEG = hpu.PASOLEG

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


def _word_text(w):
    # The word's Hebrew = the <w>'s own text + each child's TAIL. A <w> may hold an <x>
    # note marker whose text is a note code (e.g. "c" on Deut 5:17 תרצח) — NOT part of the
    # word — with the Hebrew continuing in that child's tail. So skip child text, keep tails.
    return ((w.text or "") + "".join((ch.tail or "") for ch in w)).strip()


def _read_atoms(xml_name, chnu, vrnu):
    """One verse as clc_read-shaped atoms, parsed directly from a UXLC XML file."""
    path = os.path.join(_REPO_ROOT, "in", "UXLC-39", xml_name)
    root = ET.parse(path).getroot()
    for c in root.iter("c"):
        if c.get("n") != str(chnu):
            continue
        for v in c.iter("v"):
            if v.get("n") != str(vrnu):
                continue
            return [
                {"kind": "w", "text": _word_text(w), "types": []}
                for w in v
                if w.tag == "w"
            ]
    raise AssertionError(f"{xml_name} {chnu}:{vrnu} not found in UXLC XML")


def _read_combined_atoms():
    """Gen 35:22 as clc_read-shaped atoms, parsed directly from the UXLC XML."""
    return _read_atoms("Genesis.xml", 35, 22)


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
    # dt 5:16 sits inside the Decalogue passage range and had a paseq-tokenization atom-count
    # mismatch (#29) like its 6 siblings, but resolves to NO divergence at all: once MAM's
    # paseq is folded the same way UXLC embeds it, taxton and elyon are byte-identical for
    # every word, so it is correctly NOT registered as a dual-cant verse.
    assert not dc.is_dual_cant("Deuter", 5, 16)


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


def test_split_word_position_safe_paseq():
    # A word carries a SHARED paseq earlier (present in both readings — e.g. two paseq-marked
    # clauses in one atom, an unrelated coincidence) and a second, DIVERGENT paseq later that
    # only one strand keeps — mirroring UXLC's own convention of a preceding space before an
    # embedded paseq (the paseq-tokenization class, #29). The cluster anchors on the divergent
    # carrier letter + space + paseq, a substring unique to that site, so cluster-replace
    # touches only that occurrence and leaves the earlier, shared one untouched.
    carrier1, carrier2 = hl.LAMED, hl.MEM
    shared = carrier1 + _PASOLEG  # unrelated, merely-coincidental shared paseq earlier in the word
    cluster = carrier2 + " " + _PASOLEG
    word = shared + cluster
    entry = {"cluster": cluster, "alef": cluster, "bet": carrier2 + " "}
    alef = dc.split_word(word, entry, "alef")
    bet = dc.split_word(word, entry, "bet")
    assert alef == word                        # taxton keeps both paseqs: nothing subtracted
    assert bet == shared + carrier2 + " "       # elyon drops only the divergent (later) one
    assert _count(alef, _PASOLEG) == 2 and _count(bet, _PASOLEG) == 1  # shared paseq safe


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
        # sof-pasuq (pashut chants Gen 35:22 as two verses).
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
    alef_html = _render(clc_render._plain_text_contents(alef_view.atoms, bet_view.atoms))
    assert "clc-added-during-detangling" in alef_html
    assert _SOF_PASUQ in alef_html and "[" in alef_html and "]" in alef_html
    # bet supplies nothing → no green span.
    bet_html = _render(clc_render._plain_text_contents(bet_view.atoms, alef_view.atoms))
    assert "clc-added-during-detangling" not in bet_html

    # The synthesized doc-column note carries the exact template prose, the
    # snippet, and the bracketed/green mark.
    assert len(alef_view.notes) == 1
    note_html = H.el_to_str_no_wbr(clc_render._added_note_block(alef_view.notes[0]))
    assert "sof pasuq in " in note_html
    assert "added out of thin air, to improve legibility" in note_html
    assert "clc-added-during-detangling" in note_html
    assert bet_view.notes == ()
    # The snippet AND its bracketed mark sit inside one dir="rtl" wrapper (a span
    # whose only attr is dir, distinct from the inner lang="hbo" dir="rtl" snippet
    # span) so the whole <word>[mark] reorders as one RTL unit in the LTR note —
    # rather than the [mark] floating to the wrong side.
    i_wrap = note_html.index('<span dir="rtl">')
    i_snippet = note_html.index('lang="hbo"', i_wrap)
    i_mark = note_html.index("clc-added-bracket", i_wrap)
    assert i_wrap < i_snippet < i_mark, note_html


def test_decalogue_sof_pasuq_suppression():
    # A sof-pasuq tracks its silluq: at a verse boundary one strand ends (silluq +
    # sof-pasuq) while the other continues (etnaxta), and the continuing strand drops
    # the sof-pasuq — it never sits on a non-silluq word (Ben's rule).
    etnahta = acc.ATN
    # ex 20:2 עבדים (atom 9): elyon ends, taxton continues.
    _c, alef, bet = dc.strand_views("Exodus", 20, 2, _read_atoms("Exodus.xml", 20, 2))
    a9, b9 = alef.atoms[8]["text"], bet.atoms[8]["text"]
    assert _SOF_PASUQ not in a9 and _METEG not in a9 and etnahta in a9, a9  # taxton: etnaxta
    assert _SOF_PASUQ in b9 and _METEG in b9 and etnahta not in b9, b9      # elyon: silluq+sof-pasuq
    # ex 20:5 לשנאי (atom 21): the mirror — taxton ends, elyon continues.
    _c5, alef5, bet5 = dc.strand_views("Exodus", 20, 5, _read_atoms("Exodus.xml", 20, 5))
    a21, b21 = alef5.atoms[20]["text"], bet5.atoms[20]["text"]
    assert _SOF_PASUQ in a21 and _METEG in a21 and etnahta not in a21, a21  # taxton: silluq+sof-pasuq
    assert _SOF_PASUQ not in b21 and etnahta in b21, b21                    # elyon: etnaxta
    # No strand invents a sof-pasuq, and neither supplies one here (unlike Gen 35:22).
    assert all(v.notes == () for v in (alef, bet, alef5, bet5))


def test_decalogue_supplied_sof_pasuq():
    # ex 20:8 (זכור): the first SUPPLIED sof-pasuq in the Decalogues. Its last word
    # לְקַדְּשֽׁ֗וֹ ends the taxton (alef) prose verse — silluq, present in UXLC — while elyon
    # (bet) keeps revia and reads on. UXLC has NO sof-pasuq there (unlike ex 20:5 atom 21,
    # the same shape, where it did); MAM's cant-alef confirms one belongs, so taxton supplies
    # it — bracketed/green in atom["additions"], never folded into the subtracted text.
    revia, silluq = acc.REV, _METEG
    combined = _read_atoms("Exodus.xml", 20, 8)
    assert len(combined) == 5, f"expected 5 atoms, got {len(combined)}"
    _c, alef, bet = dc.strand_views("Exodus", 20, 8, combined)

    a5, b5 = alef.atoms[4], bet.atoms[4]          # לקדשו, the supplied-supply word
    # taxton: keeps silluq, drops revia, and the supplied sof-pasuq is metadata only.
    assert silluq in a5["text"] and revia not in a5["text"], a5["text"]
    assert _SOF_PASUQ not in a5["text"], a5["text"]
    assert a5["additions"] == [_SOF_PASUQ]
    # elyon: keeps revia, drops silluq, supplies nothing.
    assert revia in b5["text"] and silluq not in b5["text"], b5["text"]
    assert _SOF_PASUQ not in b5["text"]
    assert b5.get("additions", []) == []

    # The SUBTRACTED text of neither strand invents a sof-pasuq — UXLC's ex 20:8 has none
    # (the omission CLC restores), so both subtracted strands still have zero; only alef's
    # rendered form (text + supplied) carries one.
    whole_combined = "".join(a["text"] for a in combined)
    assert _count(whole_combined, _SOF_PASUQ) == 0
    for view, n_supplied in ((alef, 1), (bet, 0)):
        whole_text = "".join(a["text"] for a in view.atoms)
        assert _count(whole_text, _SOF_PASUQ) == 0
        supplied = [ch for a in view.atoms for ch in a.get("additions", ())]
        assert _count(whole_text + "".join(supplied), _SOF_PASUQ) == n_supplied
    assert len(alef.notes) == 1 and alef.notes[0]["kind"] == "sof pasuq"
    assert bet.notes == ()

    # The supplied sof-pasuq renders bracketed/green in the alef text column; bet stays plain.
    alef_html = _render(clc_render._plain_text_contents(alef.atoms, bet.atoms))
    assert "clc-added-during-detangling" in alef_html and _SOF_PASUQ in alef_html
    bet_html = _render(clc_render._plain_text_contents(bet.atoms, alef.atoms))
    assert "clc-added-during-detangling" not in bet_html


def test_decalogue_rafe_dagesh():
    # A בגדכפת letter the two strands harden/soften differently. Policy 1 (faithful): the
    # HARD strand keeps UXLC's dagesh, the SOFT strand keeps UXLC's rafe; each drops the
    # other's mark. Where UXLC has no rafe, the soft letter stays bare (no rafe supplied).
    tipeha = acc.TIP

    # ex 20:13 (לא תרצח): UXLC stacks dagesh+rafe on the ת. taxton (alef) is SOFT — it joins
    # the next commandment (mid-unit tipxa, no verse-end); elyon (bet) is HARD and ends its
    # one-word verse (dagesh + silluq + sof-pasuq). Pure subtraction — no mark supplied.
    _c, alef, bet = dc.strand_views("Exodus", 20, 13, _read_atoms("Exodus.xml", 20, 13))
    a, b = alef.atoms[1]["text"], bet.atoms[1]["text"]          # תרצח
    assert _RAFE in a and _DAGESH not in a, a                   # taxton: soft (rafe kept)
    assert tipeha in a and _METEG not in a and _SOF_PASUQ not in a, a  # mid-unit, reads on
    assert _DAGESH in b and _RAFE not in b, b                   # elyon: hard (dagesh kept)
    assert _METEG in b and _SOF_PASUQ in b and tipeha not in b, b      # silluq + sof-pasuq
    assert all(v.notes == () for v in (alef, bet))        # nothing supplied here

    # ex 20:9 (ששת...): atom 5 כָּל־ — taxton HARD (keeps dagesh), elyon SOFT. UXLC has NO
    # rafe on this כל, so elyon's kaf is bare (Policy 1 supplies none). Atom 6 still supplies
    # the taxton sof-pasuq, so the verse is otherwise the ex 20:8 shape.
    _c9, alef9, bet9 = dc.strand_views("Exodus", 20, 9, _read_atoms("Exodus.xml", 20, 9))
    a5, b5 = alef9.atoms[4]["text"], bet9.atoms[4]["text"]      # כל
    assert _DAGESH in a5, a5                                    # taxton: hard (dagesh kept)
    assert _DAGESH not in b5 and _RAFE not in b5, b5            # elyon: bare (no rafe supplied)
    assert _count(a5, hl.KAF) == _count(b5, hl.KAF) == 1        # consonant untouched
    assert alef9.atoms[5]["additions"] == [_SOF_PASUQ]          # atom 6 supplies the sof-pasuq
    assert len(alef9.notes) == 1 and bet9.notes == ()


def test_decalogue_omitted_accent():
    # Ben's policy: an accent a strand wants but UXLC left untangled is NOTED, never supplied.
    # The strand shows the word with that accent absent; a doc-column note records the gap, and
    # nothing green/bracketed is added to the strand text.
    tipeha, etnahta, pashta, silluq = acc.TIP, acc.ATN, acc.PASH, _METEG
    OMIT = dc.clc_note.SOURCE_DUAL_CANT_OMITTED_ACCENT
    # Names are asserted from the canonical authority, never hardcoded: the omitted/present
    # accents must read exactly as describe_diff spells them ("tipexa", "zaqef-qatan", …).
    # "silluq" is the lone exception — CLC's own override for U+05BD (which describe_diff knows
    # only as "meteg"), so it is pinned as a literal.
    canon = dc.describe_diff.accent_name

    def _omit_notes(view):  # the omitted-accent notes only
        return [n for n in view.notes if n["source"] == OMIT]

    # dt 5:6 (אנכי): UXLC has only the taxton accents; elyon's tipxa (atom 1) and etnaxta
    # (atom 3) are omitted. taxton keeps its accents; elyon shows those words accent-less.
    _c, alef, bet = dc.strand_views("Deuter", 5, 6, _read_atoms("Deuteronomy.xml", 5, 6))
    a1, b1 = alef.atoms[0]["text"], bet.atoms[0]["text"]      # אנכי
    assert pashta in a1 and tipeha not in a1, a1              # taxton: keeps pashta
    assert pashta not in b1 and tipeha not in b1, b1          # elyon: accent-less (none supplied)
    assert alef.notes == ()                                   # taxton omits nothing
    bnotes = _omit_notes(bet)
    assert [n["kind"] for n in bnotes] == [canon(acc.TIP), canon(acc.ATN)], bnotes
    assert all(n["strand"] == "elyon" and n["other_strand"] == "taḥton" for n in bnotes)
    # the note names the accent UXLC actually HAS (taxton's pashta on אנכי, zaqef-qatan on אלהיך).
    assert [n["present_kind"] for n in bnotes] == [canon(acc.PASH), canon(acc.ZAQ_Q)], bnotes
    assert bet.atoms[0]["omitted_accents"] == [tipeha]
    assert bet.atoms[2]["omitted_accents"] == [etnahta]

    # dt 5:13 (ימים): the mirror direction — UXLC has only the elyon munax, so the taxton's
    # pashta (atom 2) is omitted; taxton shows ימים accent-less, elyon keeps the munax.
    _c, alef, bet = dc.strand_views("Deuter", 5, 13, _read_atoms("Deuteronomy.xml", 5, 13))
    a2, b2 = alef.atoms[1]["text"], bet.atoms[1]["text"]      # ימים
    assert pashta not in a2 and acc.MUN not in a2, a2         # taxton: accent-less (none supplied)
    assert acc.MUN in b2, b2                                  # elyon: keeps the munax
    anotes = _omit_notes(alef)
    assert [n["kind"] for n in anotes] == [canon(acc.PASH)] and anotes[0]["strand"] == "taḥton"
    assert anotes[0]["present_kind"] == canon(acc.MUN)   # UXLC has the elyon munax here
    assert _omit_notes(bet) == []

    # dt 5:17 (תרצח): UXLC has the elyon verse-end's sof-pasuq but NOT its silluq, so elyon's
    # silluq is omitted: elyon keeps dagesh (hard) + the lone sof-pasuq, no accent shown; taxton
    # keeps rafe (soft) + its mid-unit tipxa, sof-pasuq suppressed.
    _c, alef, bet = dc.strand_views("Deuter", 5, 17, _read_atoms("Deuteronomy.xml", 5, 17))
    a, b = alef.atoms[1]["text"], bet.atoms[1]["text"]        # תרצח
    assert _RAFE in a and tipeha in a and _SOF_PASUQ not in a, a       # taxton: soft, reads on
    assert _DAGESH in b and _SOF_PASUQ in b, b                        # elyon: hard, verse-end
    assert silluq not in b and tipeha not in b, b                     # but its silluq is omitted
    bnotes = _omit_notes(bet)
    assert [n["kind"] for n in bnotes] == ["silluq"] and bnotes[0]["strand"] == "elyon"
    assert bnotes[0]["present_kind"] == canon(acc.TIP)   # UXLC has taxton's tipexa here
    assert _omit_notes(alef) == []

    # Render: the omitted-accent note names BOTH accents — the one wanted (silluq) and the one
    # UXLC actually has (the taxton strand's tipxa) — shows the bare word, and adds NOTHING green
    # or bracketed (unlike a supplied mark). No abstract "the other strand's accent".
    note_html = H.el_to_str_no_wbr(clc_render._omitted_note_block(bnotes[0]))
    assert "elyon strand calls for a silluq" in note_html
    assert f"carries only the taḥton strand’s {canon(acc.TIP)}" in note_html
    assert "beyond the limits of CLC’s charity to supply the missing silluq" in note_html
    assert "clc-added-during-detangling" not in note_html and "clc-added-bracket" not in note_html
    # and the strand TEXT column supplies no green mark for an omitted accent.
    bet_html = _render(clc_render._plain_text_contents(bet.atoms, alef.atoms))
    assert "clc-added-during-detangling" not in bet_html


def test_decalogue_qupo_vowel_split():
    # ex 20:3 / dt 5:7 (לא יהיה־לך אלהים אחרים על־פני): the QUPO vowel split, the last of the
    # Decalogue's divergence mechanisms. Atom 7 פני stacks patax vs. qamats on the SAME letter
    # (the נ) — pure position-safe subtraction, exactly like rafe/dagesh: taxton keeps qamats +
    # meteg, elyon keeps patax + revia. The word's OWN shared prefix vowel (פ's qamats) is a
    # second, unrelated occurrence of the same mark type and must survive in BOTH strands —
    # pinning the fix for the whole-word-markset trap a naive divergence scan falls into.
    # Also exercises: a SUPPLIED maqaf (the first in the Decalogues, atom 1) and an OMITTED
    # accent (atom 2) — both already-proven mechanisms, newly auto-derivable for maqaf.
    canon = dc.describe_diff.accent_name
    OMIT = dc.clc_note.SOURCE_DUAL_CANT_OMITTED_ACCENT
    ADD = dc.clc_note.SOURCE_DUAL_CANT_ADDITION

    def _omit_notes(view):
        return [n for n in view.notes if n["source"] == OMIT]

    # ex 20:3
    combined = _read_atoms("Exodus.xml", 20, 3)
    _c, alef, bet = dc.strand_views("Exodus", 20, 3, combined)

    # atom 1 (לא): taxton drops the shared munax, keeps only meteg, and SUPPLIES a maqaf —
    # the first-ever supplied maqaf in the Decalogues — joining it to the next word.
    a1, b1 = alef.atoms[0]["text"], bet.atoms[0]["text"]
    assert _METEG in a1 and acc.MUN not in a1, a1
    assert acc.MUN in b1 and _METEG not in b1, b1
    assert alef.atoms[0]["additions"] == [_MAQAF]
    assert bet.atoms[0].get("additions", []) == []

    # atom 2 (יהיה): taxton's own merkha is OMITTED (UXLC left it untangled) — taxton shows
    # the word bare, with neither the merkha it wants nor elyon's meteg/maqaf; elyon keeps
    # both (its own trailing meteg + the maqaf joining יהיה to לך).
    a2, b2 = alef.atoms[1]["text"], bet.atoms[1]["text"]
    assert acc.MER not in a2 and _METEG not in a2 and _MAQAF not in a2, a2
    assert _METEG in b2 and _MAQAF in b2, b2
    anotes = _omit_notes(alef)
    assert [n["kind"] for n in anotes] == [canon(acc.MER)] and anotes[0]["strand"] == "taḥton"
    assert _omit_notes(bet) == []

    # atom 7 (פני): the QUPO split itself. taxton keeps qamats TWICE (its own, on the נ, plus
    # the word's unrelated shared prefix qamats on פ) + meteg, drops patax/revia entirely;
    # elyon keeps patax + revia plus the shared prefix qamats, drops the נ's own qamats + meteg.
    a7, b7 = alef.atoms[6]["text"], bet.atoms[6]["text"]
    assert _count(a7, _QAMATS) == 2 and _METEG in a7, a7
    assert _PATAX not in a7 and acc.REV not in a7, a7
    assert _count(b7, _QAMATS) == 1 and _PATAX in b7 and acc.REV in b7, b7
    assert _METEG not in b7, b7
    assert alef.atoms[6]["additions"] == [_SOF_PASUQ]
    assert bet.atoms[6].get("additions", []) == []
    assert _SOF_PASUQ not in a7 and _SOF_PASUQ not in b7  # supplied out-of-band, not in text

    # taxton's notes, in atom order: supplied maqaf (atom 1), omitted merkha (atom 2),
    # supplied sof-pasuq (atom 7). elyon supplies/omits nothing in this verse.
    add_notes = [n for n in alef.notes if n["source"] == ADD]
    assert [n["kind"] for n in add_notes] == ["maqaf", "sof pasuq"]
    assert len(_omit_notes(alef)) == 1
    assert bet.notes == ()

    # dt 5:7 — same QUPO shape at atom 7, but atom 1/2 mirror the other way: taxton here has
    # NO meteg to keep at all (UXLC's לא carries only munax), so it drops the munax outright
    # and supplies a maqaf just the same; and it is ELYON's silluq that is omitted at atom 2
    # (UXLC's maqaf-joined יהיה־ has no meteg for elyon to keep), while taxton keeps its own
    # merkha, already present in UXLC (no omission on the taxton side here).
    combined7 = _read_atoms("Deuteronomy.xml", 5, 7)
    _c7, alef7, bet7 = dc.strand_views("Deuter", 5, 7, combined7)

    a1d, b1d = alef7.atoms[0]["text"], bet7.atoms[0]["text"]
    assert acc.MUN not in a1d and _METEG not in a1d, a1d
    assert acc.MUN in b1d, b1d
    assert alef7.atoms[0]["additions"] == [_MAQAF]

    a2d, b2d = alef7.atoms[1]["text"], bet7.atoms[1]["text"]
    assert acc.MER in a2d and _MAQAF not in a2d, a2d
    assert _METEG not in b2d and _MAQAF in b2d, b2d
    d_omit = _omit_notes(bet7)
    assert [n["kind"] for n in d_omit] == ["silluq"] and d_omit[0]["strand"] == "elyon"
    assert _omit_notes(alef7) == []

    a7d, b7d = alef7.atoms[6]["text"], bet7.atoms[6]["text"]
    assert _count(a7d, _QAMATS) == 2 and _METEG in a7d and _PATAX not in a7d, a7d
    assert _count(b7d, _QAMATS) == 1 and _PATAX in b7d and acc.REV in b7d, b7d
    assert alef7.atoms[6]["additions"] == [_SOF_PASUQ]
    assert bet7.atoms[6].get("additions", []) == []


def test_decalogue_paseq_tokenization():
    # ex 20:4 (לא תעשה לך פסל...): the first paseq-tokenization verse (#29) — MAM-simple
    # tokenizes a standalone paseq as its own word where UXLC embeds it directly in the
    # preceding word's atom, which looked like a real word-count mismatch until
    # tools/dump_mam_strands.py's _fold_paseq folded it the same way. Once folded, the paseq
    # is an ordinary divergent mark flowing through the same position-safe subtraction path
    # as any other mark class: elyon keeps it, taxton drops it, at atoms 4/8/14 here.
    combined4 = _read_atoms("Exodus.xml", 20, 4)
    assert len(combined4) == 16, f"expected 16 atoms, got {len(combined4)}"
    _c4, alef4, bet4 = dc.strand_views("Exodus", 20, 4, combined4)
    for i in (3, 7, 13):  # atoms 4, 8, 14 (0-based): פסל / בשמים / במים
        a, b = alef4.atoms[i]["text"], bet4.atoms[i]["text"]
        assert _PASOLEG not in a and _PASOLEG in b, (i, a, b)

    # atom 1 (לא): taxton SUPPLIES the first-ever maqaf of this verse's own kind (like ex
    # 20:3's atom 1), joining it to the next word; atom 16 (לארץ) SUPPLIES the verse-end
    # sof-pasuq (taxton ends the verse here; elyon reads on, like ex 20:8's atom 5).
    assert alef4.atoms[0]["additions"] == [_MAQAF]
    assert alef4.atoms[15]["additions"] == [_SOF_PASUQ]
    assert bet4.atoms[0].get("additions", []) == [] and bet4.atoms[15].get("additions", []) == []

    # atom 12 / atom 15 (מתחת, occurrences 1 and 2 — #28's open question, closed by #29): the
    # count mismatch came from paseq elsewhere in the verse, NOT from מתחת. Occurrence 1 IS a
    # third QUPO vowel-split case (patax vs. qamats stacked on one letter, same shape as ex
    # 20:3's פני): taxton keeps its own qamats + atnach, plus the word's unrelated shared
    # trailing patax (the ordinary vowel on חַת); elyon keeps patax (replacing the qamats) +
    # gershayim, plus that same shared trailing patax — so patax appears once in taxton (the
    # shared one only) but twice in elyon (its own divergent one plus the shared one).
    # Occurrence 2 (atom 15) is a plain two-accent divergence.
    a12, b12 = alef4.atoms[11]["text"], bet4.atoms[11]["text"]
    assert _count(a12, _QAMATS) == 1 and _count(a12, _PATAX) == 1, a12
    assert acc.ATN in a12 and acc.GER not in a12, a12
    assert _count(b12, _QAMATS) == 0 and _count(b12, _PATAX) == 2, b12
    assert acc.GER in b12 and acc.ATN not in b12, b12
    a15, b15 = alef4.atoms[14]["text"], bet4.atoms[14]["text"]
    assert acc.MER in a15 and acc.MUN not in a15, a15
    assert acc.MUN in b15 and acc.MER not in b15, b15

    # ex 20:10 (...לא תעשה כל מלאכה): the second paseq-tokenization verse — this time atom 3
    # diverges in the SAME direction as ex 20:4 (elyon keeps, taxton drops), but atom 10 (אתה
    # ׀) is the sharpest case: this word carries no accent of its own, so the divergence
    # cluster is the bare paseq alone — taxton keeps it as a standalone word in MAM's alef
    # list, elyon drops it outright (its resolution is "", like an omitted accent but for
    # punctuation: never SUPPLIED, only ever suppressed, since UXLC already has the mark).
    combined10 = _read_atoms("Exodus.xml", 20, 10)
    assert len(combined10) == 18, f"expected 18 atoms, got {len(combined10)}"
    _c10, alef10, bet10 = dc.strand_views("Exodus", 20, 10, combined10)
    a3, b3 = alef10.atoms[2]["text"], bet10.atoms[2]["text"]
    assert _PASOLEG not in a3 and _PASOLEG in b3, (a3, b3)
    a10, b10 = alef10.atoms[9]["text"], bet10.atoms[9]["text"]
    assert _PASOLEG in a10 and _PASOLEG not in b10, (a10, b10)
    assert alef10.atoms[17]["additions"] == [_SOF_PASUQ]
    assert bet10.atoms[17].get("additions", []) == []


def test_decalogue_paseq_tokenization_deuteronomy():
    # dt 5:8 — the Deuteronomy twin of ex 20:4 (#29). Same three paseq atoms (elyon keeps,
    # taxton drops) and the same מתחת pair, but here NEITHER occurrence is QUPO — an ordinary
    # cross-book textual difference from ex 20:4 (see the module comment in clc_dual_cant.py).
    # Atom 2 also carries an OMITTED accent (taxton's qadma UXLC left untangled).
    OMIT = dc.clc_note.SOURCE_DUAL_CANT_OMITTED_ACCENT
    combined8 = _read_atoms("Deuteronomy.xml", 5, 8)
    assert len(combined8) == 16, f"expected 16 atoms, got {len(combined8)}"
    _c8, alef8, bet8 = dc.strand_views("Deuter", 5, 8, combined8)
    for i in (3, 7, 13):  # atoms 4, 8, 14 (0-based): פסל / בשמים / במים
        a, b = alef8.atoms[i]["text"], bet8.atoms[i]["text"]
        assert _PASOLEG not in a and _PASOLEG in b, (i, a, b)
    # atom 12 (מתחת, occurrence 1): NOT QUPO here (unlike ex 20:4's twin atom) — patax appears
    # only ONCE in each strand (the ordinary shared trailing vowel on חַת), never stacked.
    a12, b12 = alef8.atoms[11]["text"], bet8.atoms[11]["text"]
    assert _count(a12, _PATAX) == 1 and _count(b12, _PATAX) == 1, (a12, b12)
    omit8 = [n for n in alef8.notes if n["source"] == OMIT]
    assert len(omit8) == 1 and omit8[0]["kind"] == dc.describe_diff.accent_name(acc.QOM)

    # dt 5:12 (שמור...): the Deuteronomy twin of ex 20:8's supplied-sof-pasuq shape, plus a
    # paseq-tokenization atom (#29): atom 7 צוך ׀ — elyon keeps the paseq, taxton drops it.
    combined12 = _read_atoms("Deuteronomy.xml", 5, 12)
    assert len(combined12) == 9, f"expected 9 atoms, got {len(combined12)}"
    _c12, alef12, bet12 = dc.strand_views("Deuter", 5, 12, combined12)
    a7, b7 = alef12.atoms[6]["text"], bet12.atoms[6]["text"]
    assert _PASOLEG not in a7 and _PASOLEG in b7, (a7, b7)
    assert alef12.atoms[8]["additions"] == [_SOF_PASUQ]
    assert bet12.atoms[8].get("additions", []) == []

    # dt 5:14 shares ex 20:10's front half verbatim (same ...יום השביעי שבת... opening,
    # including atom 3's paseq divergence) before running on to its own verse-14 ending
    # (atom 26) — pure accent divergence there, no paseq/QUPO/rafe.
    combined14 = _read_atoms("Deuteronomy.xml", 5, 14)
    assert len(combined14) == 26, f"expected 26 atoms, got {len(combined14)}"
    _c14, alef14, bet14 = dc.strand_views("Deuter", 5, 14, combined14)
    a3, b3 = alef14.atoms[2]["text"], bet14.atoms[2]["text"]
    assert _PASOLEG not in a3 and _PASOLEG in b3, (a3, b3)
    a26, b26 = alef14.atoms[25]["text"], bet14.atoms[25]["text"]
    assert _SOF_PASUQ in a26 and _METEG in a26 and acc.ATN not in a26, a26  # taxton: verse-end
    assert acc.ATN in b26 and _SOF_PASUQ not in b26, b26                    # elyon: reads on

    # dt 5:15 (וזכרת...), unique to Deuteronomy's Decalogue (no Exodus twin): its own
    # paseq-tokenization atom (#29) is atom 4 היית ׀ — elyon keeps it, taxton drops it, same
    # direction as every other paseq atom above.
    combined15 = _read_atoms("Deuteronomy.xml", 5, 15)
    assert len(combined15) == 23, f"expected 23 atoms, got {len(combined15)}"
    _c15, alef15, bet15 = dc.strand_views("Deuter", 5, 15, combined15)
    a4, b4 = alef15.atoms[3]["text"], bet15.atoms[3]["text"]
    assert _PASOLEG not in a4 and _PASOLEG in b4, (a4, b4)


def test_strand_same_highlighting():
    # A strand word is de-highlighted (clc-strand-same) iff it is identical ACROSS
    # the two strands (taxton == elyon), not merely equal to the combined form.
    # ex 20:9 atom 5 כָּל־: taxton keeps the dagesh — so it EQUALS the combined form
    # (the old strand-vs-combined rule grayed it) — while elyon drops it. That is a
    # real divergence, so it must stay highlighted, not grayed.
    combined9 = _read_atoms("Exodus.xml", 20, 9)
    _c, alef9, bet9 = dc.strand_views("Exodus", 20, 9, combined9)
    kol_alef, kol_bet = alef9.atoms[4]["text"], bet9.atoms[4]["text"]
    assert kol_alef == combined9[4]["text"]   # taxton == combined (would-be old gray)
    assert kol_alef != kol_bet                # but taxton != elyon → a divergence
    alef9_html = _render(clc_render._plain_text_contents(alef9.atoms, bet9.atoms))
    bet9_html = _render(clc_render._plain_text_contents(bet9.atoms, alef9.atoms))
    assert f'clc-strand-same">{kol_alef}' not in alef9_html   # highlighted, not gray
    assert f'clc-strand-same">{kol_bet}' not in bet9_html

    # A genuinely shared word (absent from the oracle — identical in both strands)
    # stays grayed. ex 20:8 atom 2 אֶת־ diverges in neither strand.
    _c8, alef8, bet8 = dc.strand_views("Exodus", 20, 8, _read_atoms("Exodus.xml", 20, 8))
    et = alef8.atoms[1]["text"]
    assert et == bet8.atoms[1]["text"]
    alef8_html = _render(clc_render._plain_text_contents(alef8.atoms, bet8.atoms))
    assert f'clc-strand-same">{et}' in alef8_html


def main():
    test_is_dual_cant()
    test_decalogue_sof_pasuq_suppression()
    test_decalogue_supplied_sof_pasuq()
    test_decalogue_rafe_dagesh()
    test_decalogue_omitted_accent()
    test_decalogue_qupo_vowel_split()
    test_decalogue_paseq_tokenization()
    test_decalogue_paseq_tokenization_deuteronomy()
    test_split_word_core()
    test_split_word_position_safe_qupo()
    test_split_word_position_safe_rafe_dagesh()
    test_split_word_position_safe_paseq()
    test_strand_views_strict()
    test_added_render()
    test_strand_same_highlighting()
    print("clc_dual_cant: OK")


if __name__ == "__main__":
    main()
