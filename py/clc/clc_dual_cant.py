"""Exports the CLC dual-cantillation strand splitter (design doc §7.7).

A few prose loci carry **two cantillation traditions at once** — the Decalogues
(Exod 20, Deut 5) and **Genesis 35:22**, the first application here. UXLC stores
them as one *combined* form in which both strands' accents are stacked onto the
same words (e.g. רְאוּבֵ֔֗ן carries both zaqef ``U+0594`` and revia ``U+0597``).

This module splits that combined form into the two single-cantillation strands —
alef and bet — for side-by-side display. The split is **near-subtractive, with one
narrowly-scoped, always-marked charity (supplying punctuation only) plus, where a
strand wants an accent UXLC omitted, a note in lieu of inventing one**:

  * **Position-safe subtraction.** Each strand is UXLC's own combined word with
    only the *other* strand's **divergence cluster** resolved: an accent, its
    intimately-tracking **word-division punctuation** (a maqaf / sof-pasuq /
    legarmeh that goes only with that strand — so a sof-pasuq is *suppressed*
    when its silluq is, and never lands on a word whose last accent is e.g.
    etnaḥta), and — where the two strands stack them on one letter — the other
    strand's **vowel** (a QUPO word's patax vs. qamats) or **rafe/dagesh**. The
    cluster is replaced *by name at its exact site* (``str.replace(cluster,
    resolution, 1)``), so a mark that recurs elsewhere in the word as a *shared*
    mark is never touched.
  * **Marked supply — punctuation only.** A *word-division* mark a strand needs
    but UXLC lacks may be **supplied — never silently**: it is rendered
    **bracketed and green** (CSS ``clc-added-during-detangling``) with a
    synthesized "added out of thin air" note (e.g. a sof-pasuq breaking Gen
    35:22's pashuṭ into its two chanted verses). Only the three accent-coupled
    punctuation marks — **maqaf / sof-pasuq / legarmeh** — are ever supplied; so
    far three sof-pasuqs are (Gen 35:22 pashuṭ, and the taḥton verse-ends of Exod
    20:8 לקדשו and 20:9 מלאכתך, where UXLC has none).
  * **Omitted accent — noted, never supplied.** Where a strand's chanting calls
    for an *accent* UXLC left untangled (it has only the other strand's accent
    on that word), CLC — a *diplomatic* edition — does **not** invent one: it
    shows the word as UXLC has it (that accent absent) and synthesizes a per-strand
    **note** instead. This is the sharpened §7.7 departure from the wlc-utils
    *detangler*, which (being a grammar-checker) *supplies* the missing accent from
    MAM so its strand parses. The Decalogue cases: Deut 5:6 (elyon's tipeḥa on אנכי
    + etnaḥta on אלהיך), 5:13 (taḥton's pashta on ימים), 5:17 (elyon's silluq on
    תרצח — UXLC has the sof-pasuq but not its silluq).

No consonant is changed and no *shared* mark removed (a mark both strands keep
stays in both); only the divergent marks — accent and the punctuation that tracks
it — are subtracted. MAM (via the wlc-utils detangler) is consulted **only as the
oracle** for *which* of two stacked marks belongs to which strand, where a
supplied break falls, and which accent a strand wants where UXLC has only the
other's — encoded once, by hand, in ``_ORACLE`` below. Nothing of MAM's text is
imported.

This is the same charitable shape as the legarmeh-vs-paseq feature (§7.16): both
improve UXLC by importing MAM's auxiliary adjudication of an ambiguity that is
grammatical, not graphical.
"""

from dataclasses import dataclass

import mb_cmn.hebrew_accents as acc
import mb_cmn.hebrew_letters as hl
import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_punctuation as hpu
import mb_diff_mpu.describe_diff as describe_diff
import clc.clc_note as clc_note


# Combining grapheme joiner: a control char (no textual meaning) used in the
# combined form only to sequence two stacked accents. Once a single accent
# remains it has nothing to sequence, so a strand drops it (cf. §7.14). It lives
# inside a divergence cluster (atom 14) and simply isn't in either resolution.
_CGJ = "͏"

_STRAND_ALEF = "alef"
_STRAND_BET = "bet"

# The closed set of marks a strand may have SUPPLIED (the additive charity) — only
# accent-coupled *word-division punctuation*. An accent UXLC omitted is NEVER supplied;
# it is recorded as an omitted-accent note (see _OMITTABLE / _omitted_note). Legarmeh is
# suppliable in principle (the third punctuation mark, §7.7) but never arises in the
# Decalogues — there it is only ever suppressed — so it is not in this set yet.
_SUPPLIABLE = {hpu.MAQ, hpu.SOPA}
# Display names for a supplied mark, used in the synthesized doc-column note.
_ADDED_NAME = {hpu.MAQ: "maqaf", hpu.SOPA: "sof pasuq"}

def _is_accent(ch):
    """A cantillation accent (U+0591–U+05AF) or the meteg/silluq mark (U+05BD)."""
    return 0x0591 <= ord(ch) <= 0x05AF or ch == hpo.MTGOSLQ


def _accent_name(ch):
    """Display name of an accent for an omitted-accent note, taken from the canonical
    mb_diff_mpu authority (``describe_diff.accent_name`` — e.g. "tipeḥa", "zaqef-qatan",
    "munaḥ") so CLC never reinvents a spelling. One CLC override: U+05BD is named "silluq"
    — its verse-final reading here (design doc §2) — where describe_diff knows that
    codepoint only as the mark "meteg" (its ``accent_name`` falls back to the raw Unicode
    name there). ``_validate_oracle`` guarantees every omittable accent has a canonical
    name, so this never returns a "HEBREW …" placeholder."""
    if ch == hpo.MTGOSLQ:
        return "silluq"
    return describe_diff.accent_name(ch)


# Ref-label suffixes shown in the page (user-facing): combined / alef / bet.
SUFFIX_COMBINED = "C"
SUFFIX_ALEF = "א"  # HEBREW LETTER ALEF
SUFFIX_BET = "ב"   # HEBREW LETTER BET

# Hover description for the combined ref label (book-independent).
TOOLTIP_COMBINED = (
    "Combined cantillation — both strands' accents tangled together, "
    "as written in the Leningrad Codex."
)


# Each dual-cant book uses a different pair of strand traditions, so the alef/bet
# doc-labels and tooltips are per-book: Genesis 35:22 is pashuṭ / midrashit; the
# Decalogues (Exodus 20, Deuteronomy 5) are taḥton / elyon. The alef strand is always
# the verse-by-verse strand, bet the grouped/alternative one.
@dataclass(frozen=True)
class _Strand:
    doc_label: str  # short doc-column label
    tooltip: str    # hover description for the ref label
    short: str      # bare strand name (e.g. "taḥton"), for the omitted-accent note prose


_PASHUT = _Strand(
    "pashuṭ (simple) strand",
    "Strand א (pashuṭ / simple): the verse-by-verse accentuation, "
    "separated from the combined marks using MAM as oracle — no mark "
    "subtracted but the other strand's, only a maqaf/sof-pasuq supplied.",
    "pashuṭ",
)
_MIDRASHIT = _Strand(
    "midrashit (interpretive) strand",
    "Strand ב (midrashit / interpretive): the alternative accentuation, "
    "separated the same way.",
    "midrashit",
)
_TAXTON = _Strand(
    "taḥton (lower) strand",
    "Strand א (taḥton / lower): the verse-by-verse cantillation that divides the "
    "Decalogue into its prose verses, separated from the combined marks using MAM as "
    "oracle — only the other strand's accents and the punctuation tracking them are "
    "subtracted (so a sof-pasuq is dropped where this strand does not end a verse).",
    "taḥton",
)
_ELYON = _Strand(
    "elyon (upper) strand",
    "Strand ב (elyon / upper): the cantillation that chants each commandment as one "
    "verse, separated the same way.",
    "elyon",
)

# alef/bet strands per dual-cant book (bk39 id).
_STRANDS = {
    "Genesis": (_PASHUT, _MIDRASHIT),
    "Exodus": (_TAXTON, _ELYON),
    "Deuter": (_TAXTON, _ELYON),
}


# The hardcoded oracle. For each dual-cant verse, map a 1-based atom index (only
# the *divergence* words, where the two strands stack marks) to a resolution:
#
#   atom_index -> {
#       "cluster": exact combined substring that diverges (incl. CGJ if present),
#       "alef":    the cluster's alef resolution (a subsequence of "cluster"),
#       "bet":     the cluster's bet  resolution (a subsequence of "cluster"),
#       "add":     optional {strand: [char, ...]} of maqaf/sof-pasuq SUPPLIED to
#                  that strand (rendered bracketed/green + a synthesized note),
#       "omit":    optional {strand: [accent, ...]} an accent that strand's chanting
#                  wants but UXLC omitted — NOTED, never supplied (so it is NOT in
#                  the strand's text; just a synthesized note). Accents only.
#   }
#
# Building a strand replaces "cluster" with that strand's resolution at its exact
# site (position-safe — a recurrence of any constituent mark elsewhere is left
# alone) and appends any supplied marks. Clusters/resolutions are spelled from
# named mark constants so the (invisible, combining) bytes are legible and match
# UXLC byte-for-byte — guarded by _validate_oracle() at import and by the
# `cluster in combined_text` assert in split_word. Every atom not listed carries
# a single shared mark and is left byte-for-byte.
#
# Genesis 35:22 (clusters derived by diffing UXLC's combined words against the
# alef/bet strands; cross-checked to reproduce the prior accent-only split):
#
#   atom  combined word   alef keeps              bet keeps
#   ----  --------------  ---------------------   ---------------------
#    7    רְאוּבֵ֔֗ן        zaqef qatan  U+0594     revia        U+0597
#    8    וַיִּשְׁכַּ֕ב֙      zaqef gadol  U+0595     pashta       U+0599
#   10    בִּלְהָ֖ה֙         tipeha       U+0596     pashta       U+0599
#   12    אָבִ֑֔יו          etnahta      U+0591     zaqef qatan  U+0594
#   14    יִשְׂרָאֵ֑͏ֽל       meteg/silluq U+05BD     etnahta      U+0591  (CGJ dropped)
#         + alef ALSO gains a supplied sof-pasuq — pashuṭ chants this as a verse end.
_ORACLE = {
    "Genesis": {
        (35, 22): {
            7: {"cluster": acc.ZAQ_Q + acc.REV, "alef": acc.ZAQ_Q, "bet": acc.REV},
            8: {
                "cluster": acc.ZAQ_G + hl.BET + acc.PASH,
                "alef": acc.ZAQ_G + hl.BET,
                "bet": hl.BET + acc.PASH,
            },
            10: {
                "cluster": acc.TIP + hl.HE + acc.PASH,
                "alef": acc.TIP + hl.HE,
                "bet": hl.HE + acc.PASH,
            },
            12: {"cluster": acc.ATN + acc.ZAQ_Q, "alef": acc.ATN, "bet": acc.ZAQ_Q},
            14: {
                "cluster": acc.ATN + _CGJ + hpo.MTGOSLQ,
                "alef": hpo.MTGOSLQ,
                "bet": acc.ATN,
                "add": {_STRAND_ALEF: [hpu.SOPA]},
            },
        },
    },
    # The Decalogues (Exodus 20, Deuteronomy 5), taḥton (alef) / elyon (bet). Derived from
    # MAM-simple's cant-alef / cant-bet strands (the oracle) diffed against UXLC's combined
    # atoms by .novc/gen_entry.py, then self-verified by simulating split_word. Punctuation
    # tracks accents: where a strand keeps a NON-silluq final accent (e.g. etnaḥta) while
    # the other keeps silluq, the sof-pasuq is SUPPRESSED in the non-silluq strand — it
    # appears only on a silluq word (e.g. ex 20:2 atom 9: elyon keeps silluq + sof-pasuq,
    # taḥton keeps etnaḥta with the sof-pasuq removed; ex 20:5 atom 21 is the mirror).
    # Encoded so far: the pure-accent (+ sof-pasuq-suppression) verses; ex 20:8 / ex 20:9
    # whose taḥton verse-end SUPPLIES a sof-pasuq UXLC omitted (the additive charity); the
    # rafe/dagesh verses (ex 20:9,13–15; dt 5:13,17,18,19) where the two strands harden/soften a
    # בגדכפת letter — the hard strand keeps UXLC's dagesh, the soft keeps UXLC's rafe (faithful,
    # Policy 1; bare where UXLC has no rafe, as in ex 20:9 כל); and the OMITTED-accent verses
    # (dt 5:6,13,17) where UXLC has only one strand's accent and the other's is NOTED, never
    # supplied (Ben's policy — see the "omit" field and _omitted_note). Still TBD: a QUPO vowel
    # split (ex 20:3, dt 5:7) and the maqaf word-division / count-mismatch verses (ex 20:4,10;
    # dt 5:8,12,14,15,16) — see .novc/entries.txt for the partition.
    "Exodus": {
        (20, 2): {
            1: {"cluster": acc.TIP + hl.YOD + acc.PASH, "alef": hl.YOD + acc.PASH, "bet": acc.TIP + hl.YOD},
            3: {"cluster": acc.ATN + acc.ZAQ_Q, "alef": acc.ZAQ_Q, "bet": acc.ATN},
            8: {"cluster": acc.MUN + acc.MER, "alef": acc.MUN, "bet": acc.MER},
            9: {"cluster": acc.ATN + _CGJ + hpo.MTGOSLQ + hl.YOD + hl.FMEM + hpu.SOPA, "alef": acc.ATN + hl.YOD + hl.FMEM, "bet": hpo.MTGOSLQ + hl.YOD + hl.FMEM + hpu.SOPA},
        },
        (20, 5): {
            2: {"cluster": acc.MER + acc.MUN, "alef": acc.MER, "bet": acc.MUN},
            3: {"cluster": acc.TIP + hl.FMEM + acc.Z_OR_TSOR, "alef": acc.TIP + hl.FMEM, "bet": hl.FMEM + acc.Z_OR_TSOR},
            5: {"cluster": acc.ATN + hl.FMEM + acc.SEG_A, "alef": acc.ATN + hl.FMEM, "bet": hl.FMEM + acc.SEG_A},
            21: {"cluster": hpo.MTGOSLQ + acc.ATN + hl.YOD + hpu.SOPA, "alef": hpo.MTGOSLQ + hl.YOD + hpu.SOPA, "bet": acc.ATN + hl.YOD},
        },
        (20, 6): {
            1: {"cluster": acc.MER + acc.MAH, "alef": acc.MER, "bet": acc.MAH},
            2: {"cluster": acc.TIP + acc.PASH + hl.SAMEKH + hpo.SEGOL_V + hl.DALET + acc.PASH, "alef": acc.TIP + hl.SAMEKH + hpo.SEGOL_V + hl.DALET, "bet": acc.PASH + hl.SAMEKH + hpo.SEGOL_V + hl.DALET + acc.PASH},
            3: {"cluster": acc.ATN + acc.ZAQ_Q, "alef": acc.ATN, "bet": acc.ZAQ_Q},
        },
        # ex 20:8 — the first SUPPLIED sof-pasuq in the Decalogues (the additive charity,
        # like Gen 35:22). Atom 5 לְקַדְּשֽׁ֗וֹ ends the Sabbath-commandment's *first* prose
        # verse: taḥton (alef) chants a verse-end there — silluq, already in UXLC — while
        # elyon (bet) keeps revia and reads on (its Sabbath verse runs vv.8–11). UXLC has
        # no sof-pasuq here (cf. ex 20:5 atom 21, the same shape, where it DID); MAM's
        # cant-alef confirms one belongs, so taḥton SUPPLIES it (bracketed/green). Atoms
        # 1/3/4 are pure-accent. ex 20:9 / dt 5:12 also want a supplied sof-pasuq but are
        # entangled with a rafe/dagesh (כָּל) and a maqaf count-mismatch respectively — TBD.
        (20, 8): {
            1: {"cluster": acc.TEV + hl.VAV + hpo.XOLAM + hl.RESH + acc.TEL_Q, "alef": acc.TEV + hl.VAV + hpo.XOLAM + hl.RESH, "bet": hl.VAV + hpo.XOLAM + hl.RESH + acc.TEL_Q},
            3: {"cluster": acc.MER + acc.QOM, "alef": acc.MER, "bet": acc.QOM},
            4: {"cluster": acc.TIP + acc.GER, "alef": acc.TIP, "bet": acc.GER},
            5: {"cluster": hpo.MTGOSLQ + acc.REV, "alef": hpo.MTGOSLQ, "bet": acc.REV, "add": {_STRAND_ALEF: [hpu.SOPA]}},
        },
        # ex 20:9 (ששת ימים תעבד): the first rafe/dagesh split. Atom 5 כָּל־ ("all") — taḥton
        # keeps the dagesh (hard: ועשית took a disjunctive tipḥa, so כל opens after a pause),
        # elyon drops it (soft: ועשית took a conjunctive munaḥ). UXLC has no rafe here, so
        # the soft kaf stays bare (faithful — Policy 1). Atom 6 מלאכתך supplies a sof-pasuq
        # (taḥton ends v.9; elyon keeps segolta and reads on).
        (20, 9): {
            1: {"cluster": acc.MAH + acc.MUN, "alef": acc.MAH, "bet": acc.MUN},
            2: {"cluster": acc.MUN + hl.YOD + hl.FMEM + acc.PASH, "alef": hl.YOD + hl.FMEM + acc.PASH, "bet": acc.MUN + hl.YOD + hl.FMEM},
            3: {"cluster": acc.ZAQ_Q + hl.DALET + acc.Z_OR_TSOR, "alef": acc.ZAQ_Q + hl.DALET, "bet": hl.DALET + acc.Z_OR_TSOR},
            4: {"cluster": acc.TIP + acc.MUN, "alef": acc.TIP, "bet": acc.MUN},
            5: {"cluster": hl.KAF + hpo.DAGOMOSD, "alef": hl.KAF + hpo.DAGOMOSD, "bet": hl.KAF},
            6: {"cluster": hpo.MTGOSLQ + hl.FKAF + hpo.QAMATS + acc.SEG_A, "alef": hpo.MTGOSLQ + hl.FKAF + hpo.QAMATS, "bet": hl.FKAF + hpo.QAMATS + acc.SEG_A, "add": {_STRAND_ALEF: [hpu.SOPA]}},
        },
        # ex 20:13–15 (לא תרצח / תנאף / תגנב): here taḥton joins each short commandment to the
        # next (לא takes a conjunctive merkha/munaḥ, so the verb opens SOFT) while elyon chants
        # each as its own verse (לא takes a disjunctive tipḥa → verb HARD + silluq + sof-pasuq).
        # UXLC stacks dagesh+rafe on the verb's first letter, so the split is pure subtraction:
        # taḥton keeps the rafe (soft) + its mid-unit accent, elyon keeps the dagesh (hard) +
        # silluq + sof-pasuq. (Faithful — Policy 1: the soft letter shows UXLC's own rafe.)
        (20, 13): {
            1: {"cluster": acc.MER + acc.TIP, "alef": acc.MER, "bet": acc.TIP},
            2: {"cluster": hl.TAV + hpo.DAGOMOSD + hpo.RAFE + hpo.XIRIQ + hl.RESH + hpo.SHEVA + hl.TSADI + hpo.QAMATS + acc.TIP + _CGJ + hpo.MTGOSLQ + hl.XET + hpu.SOPA, "alef": hl.TAV + hpo.RAFE + hpo.XIRIQ + hl.RESH + hpo.SHEVA + hl.TSADI + hpo.QAMATS + acc.TIP + hl.XET, "bet": hl.TAV + hpo.DAGOMOSD + hpo.XIRIQ + hl.RESH + hpo.SHEVA + hl.TSADI + hpo.QAMATS + hpo.MTGOSLQ + hl.XET + hpu.SOPA},
        },
        (20, 14): {
            1: {"cluster": acc.MUN + acc.TIP, "alef": acc.MUN, "bet": acc.TIP},
            2: {"cluster": hl.TAV + hpo.DAGOMOSD + hpo.RAFE + hpo.XIRIQ + hl.NUN + hpo.SHEVA + hl.ALEF + hpo.QAMATS + acc.ATN + _CGJ + hpo.MTGOSLQ + hl.FPE + hpu.SOPA, "alef": hl.TAV + hpo.RAFE + hpo.XIRIQ + hl.NUN + hpo.SHEVA + hl.ALEF + hpo.QAMATS + acc.ATN + hl.FPE, "bet": hl.TAV + hpo.DAGOMOSD + hpo.XIRIQ + hl.NUN + hpo.SHEVA + hl.ALEF + hpo.QAMATS + hpo.MTGOSLQ + hl.FPE + hpu.SOPA},
        },
        (20, 15): {
            1: {"cluster": acc.MUN + acc.TIP, "alef": acc.MUN, "bet": acc.TIP},
            2: {"cluster": hl.TAV + hpo.DAGOMOSD + hpo.RAFE + hpo.XIRIQ + hl.GIMEL + hpo.SHEVA + hl.NUN + hpo.XOLAM + hpo.MTGOSLQ + acc.ZAQ_Q + hl.BET + hpu.SOPA, "alef": hl.TAV + hpo.RAFE + hpo.XIRIQ + hl.GIMEL + hpo.SHEVA + hl.NUN + hpo.XOLAM + acc.ZAQ_Q + hl.BET, "bet": hl.TAV + hpo.DAGOMOSD + hpo.XIRIQ + hl.GIMEL + hpo.SHEVA + hl.NUN + hpo.XOLAM + hpo.MTGOSLQ + hl.BET + hpu.SOPA},
        },
    },
    "Deuter": {
        # dt 5:6 (אנכי...): the Deuteronomy twin of ex 20:2, but where UXLC there stacked BOTH
        # strands' accents, here it has only the taḥton's — so elyon's are OMITTED, not present.
        # Atom 1 אנכי: taḥton keeps its pashta; elyon wants a tipḥa UXLC left untangled (noted, not
        # supplied) → elyon shows אנכי accent-less. Atom 3 אלהיך likewise: taḥton zaqef kept, elyon's
        # etnaḥta omitted. Atoms 8/9 are the pure-subtraction shape of ex 20:2 (munaḥ/merkha; then
        # etnaḥta vs. silluq+sof-pasuq at the verse end).
        (5, 6): {
            1: {"cluster": acc.PASH, "alef": acc.PASH, "bet": "", "omit": {_STRAND_BET: [acc.TIP]}},
            3: {"cluster": acc.ZAQ_Q, "alef": acc.ZAQ_Q, "bet": "", "omit": {_STRAND_BET: [acc.ATN]}},
            8: {"cluster": acc.MUN + acc.MER, "alef": acc.MUN, "bet": acc.MER},
            9: {"cluster": acc.ATN + _CGJ + hpo.MTGOSLQ + hl.YOD + hl.FMEM + hpu.SOPA, "alef": acc.ATN + hl.YOD + hl.FMEM, "bet": hpo.MTGOSLQ + hl.YOD + hl.FMEM + hpu.SOPA},
        },
        (5, 9): {
            2: {"cluster": acc.MER + acc.MUN, "alef": acc.MER, "bet": acc.MUN},
            3: {"cluster": acc.TIP + hl.FMEM + acc.Z_OR_TSOR, "alef": acc.TIP + hl.FMEM, "bet": hl.FMEM + acc.Z_OR_TSOR},
            5: {"cluster": acc.ATN + hl.FMEM + acc.SEG_A, "alef": acc.ATN + hl.FMEM, "bet": hl.FMEM + acc.SEG_A},
            21: {"cluster": hpo.MTGOSLQ + acc.ATN + hl.YOD + hpu.SOPA, "alef": hpo.MTGOSLQ + hl.YOD + hpu.SOPA, "bet": acc.ATN + hl.YOD},
        },
        (5, 10): {
            1: {"cluster": acc.MER + acc.MAH, "alef": acc.MER, "bet": acc.MAH},
            2: {"cluster": acc.TIP + acc.PASH + hl.SAMEKH + hpo.SEGOL_V + hl.DALET + acc.PASH, "alef": acc.TIP + hl.SAMEKH + hpo.SEGOL_V + hl.DALET, "bet": acc.PASH + hl.SAMEKH + hpo.SEGOL_V + hl.DALET + acc.PASH},
            3: {"cluster": acc.ATN + acc.ZAQ_Q, "alef": acc.ATN, "bet": acc.ZAQ_Q},
        },
        # dt 5:13 (ששת ימים...): the Deuteronomy twin of ex 20:9, but UXLC has only the elyon
        # munaḥ on ימים (atom 2), so the taḥton's PASHTA is OMITTED — noted, not supplied; taḥton
        # shows ימים accent-less. Atom 5 כל is the mirror of ex 20:9's: here taḥton is HARD (dagesh)
        # and UXLC DOES have a rafe, so elyon is soft (rafe kept) — faithful Policy 1. Atom 6 ends
        # the taḥton verse (silluq + sof-pasuq, both in UXLC — no supply, unlike ex 20:9).
        (5, 13): {
            1: {"cluster": acc.MUN + acc.MAH, "alef": acc.MAH, "bet": acc.MUN},
            2: {"cluster": acc.MUN, "alef": "", "bet": acc.MUN, "omit": {_STRAND_ALEF: [acc.PASH]}},
            3: {"cluster": acc.ZAQ_Q + hl.DALET + acc.Z_OR_TSOR, "alef": acc.ZAQ_Q + hl.DALET, "bet": hl.DALET + acc.Z_OR_TSOR},
            4: {"cluster": acc.TIP + acc.MUN, "alef": acc.TIP, "bet": acc.MUN},
            5: {"cluster": hl.KAF + hpo.DAGOMOSD + hpo.RAFE, "alef": hl.KAF + hpo.DAGOMOSD, "bet": hl.KAF + hpo.RAFE},
            6: {"cluster": hpo.MTGOSLQ + hl.FKAF + hpo.QAMATS + acc.SEG_A + hpu.SOPA, "alef": hpo.MTGOSLQ + hl.FKAF + hpo.QAMATS + hpu.SOPA, "bet": hl.FKAF + hpo.QAMATS + acc.SEG_A},
        },
        # dt 5:17 (לא תרצח): the Deuteronomy twin of ex 20:13, but UXLC has the elyon verse-end's
        # sof-pasuq WITHOUT its silluq — so elyon's SILLUQ is OMITTED (noted, not supplied): elyon's
        # תרצח keeps the dagesh (hard) + the lone sof-pasuq, with no accent shown. taḥton keeps the
        # rafe (soft) + its mid-unit tipḥa and reads on (sof-pasuq suppressed).
        (5, 17): {
            1: {"cluster": acc.MER + acc.TIP, "alef": acc.MER, "bet": acc.TIP},
            2: {"cluster": hl.TAV + hpo.DAGOMOSD + hpo.RAFE + hpo.XIRIQ + hl.RESH + hpo.SHEVA + hl.TSADI + hpo.QAMATS + acc.TIP + hl.XET + hpu.SOPA, "alef": hl.TAV + hpo.RAFE + hpo.XIRIQ + hl.RESH + hpo.SHEVA + hl.TSADI + hpo.QAMATS + acc.TIP + hl.XET, "bet": hl.TAV + hpo.DAGOMOSD + hpo.XIRIQ + hl.RESH + hpo.SHEVA + hl.TSADI + hpo.QAMATS + hl.XET + hpu.SOPA, "omit": {_STRAND_BET: [hpo.MTGOSLQ]}},
        },
        # dt 5:18–19 (לא תנאף / תגנב): the Deuteronomy twins of ex 20:14–15 — same rafe/dagesh
        # split (taḥton soft via the rafe, elyon hard via the dagesh + silluq + sof-pasuq), all
        # stacked in UXLC so it is pure subtraction. (Unlike dt 5:17, UXLC here DOES have the
        # elyon silluq, so nothing is omitted.)
        (5, 18): {
            1: {"cluster": acc.MUN + acc.TIP, "alef": acc.MUN, "bet": acc.TIP},
            2: {"cluster": hl.TAV + hpo.DAGOMOSD + hpo.RAFE + hpo.XIRIQ + hl.NUN + hpo.SHEVA + hl.ALEF + hpo.QAMATS + hpo.MTGOSLQ + acc.ATN + hl.FPE + hpu.SOPA, "alef": hl.TAV + hpo.RAFE + hpo.XIRIQ + hl.NUN + hpo.SHEVA + hl.ALEF + hpo.QAMATS + acc.ATN + hl.FPE, "bet": hl.TAV + hpo.DAGOMOSD + hpo.XIRIQ + hl.NUN + hpo.SHEVA + hl.ALEF + hpo.QAMATS + hpo.MTGOSLQ + hl.FPE + hpu.SOPA},
        },
        (5, 19): {
            1: {"cluster": acc.MUN + acc.TIP, "alef": acc.MUN, "bet": acc.TIP},
            2: {"cluster": hl.TAV + hpo.DAGOMOSD + hpo.RAFE + hpo.XIRIQ + hl.GIMEL + hpo.SHEVA + hl.NUN + hpo.XOLAM + hpo.MTGOSLQ + acc.ZAQ_Q + hl.BET + hpu.SOPA, "alef": hl.TAV + hpo.RAFE + hpo.XIRIQ + hl.GIMEL + hpo.SHEVA + hl.NUN + hpo.XOLAM + acc.ZAQ_Q + hl.BET, "bet": hl.TAV + hpo.DAGOMOSD + hpo.XIRIQ + hl.GIMEL + hpo.SHEVA + hl.NUN + hpo.XOLAM + hpo.MTGOSLQ + hl.BET + hpu.SOPA},
        },
    },
}


@dataclass(frozen=True)
class StrandView:
    """One displayable form of a dual-cant verse: combined, alef, or bet."""

    suffix: str    # ref-label suffix: "C" / "א" / "ב"
    tooltip: str   # hover description for the ref label
    doc_label: str  # short doc-column label ("" for the combined form)
    atoms: list    # atom dicts (clc_read shape + "additions" on split atoms)
    notes: tuple = ()  # synthesized strand notes: supplied-mark + omitted-accent (strand only)


def is_dual_cant(book_id, ch, v):
    """Is (book, chapter, verse) one of the dual-cantillation loci?"""
    return (ch, v) in _ORACLE.get(book_id, {})


def split_word(combined_text, entry, strand):
    """Position-safely resolve one divergence atom for ``strand`` (subtractive only).

    Replaces the FIRST occurrence of ``entry['cluster']`` with the strand's
    resolution (``entry['alef']`` or ``entry['bet']``). A constituent mark that
    recurs elsewhere in the word as a shared mark is untouched. Returns the
    strictly-subtracted text; SUPPLIED punctuation is applied separately (see
    ``_split_atom``), never folded into the returned text.
    """
    resolution = entry[strand]
    cluster = entry["cluster"]
    assert cluster in combined_text, (combined_text, cluster)
    return combined_text.replace(cluster, resolution, 1)


def strand_views(book_id, ch, v, verse_atoms):
    """Return the three displayable views (combined, alef, bet) of a dual-cant verse.

    ``verse_atoms`` is the verse's atom list from clc_read. The combined view
    reuses those atoms unchanged; each alef/bet view holds fresh atom dicts whose
    text has the other strand's divergence cluster resolved (see ``split_word``)
    plus an ``additions`` list, and a tuple of synthesized notes — one per mark it
    supplies and one per accent it wants but UXLC omitted.
    """
    oracle = _ORACLE[book_id][(ch, v)]
    alef_strand, bet_strand = _STRANDS[book_id]
    alef_atoms = _strand_atoms(verse_atoms, oracle, _STRAND_ALEF)
    bet_atoms = _strand_atoms(verse_atoms, oracle, _STRAND_BET)
    return [
        StrandView(SUFFIX_COMBINED, TOOLTIP_COMBINED, "", verse_atoms),
        StrandView(
            SUFFIX_ALEF, alef_strand.tooltip, alef_strand.doc_label,
            alef_atoms, _strand_notes(alef_atoms, bet_atoms, alef_strand, bet_strand),
        ),
        StrandView(
            SUFFIX_BET, bet_strand.tooltip, bet_strand.doc_label,
            bet_atoms, _strand_notes(bet_atoms, alef_atoms, bet_strand, alef_strand),
        ),
    ]


def _strand_atoms(verse_atoms, oracle, strand):
    return [
        _split_atom(atom, atom_index, oracle, strand)
        for atom_index, atom in enumerate(verse_atoms, start=1)
    ]


def _split_atom(atom, atom_index, oracle, strand):
    entry = oracle.get(atom_index)
    if entry is None:
        return atom  # shared single mark (or no mark) — unchanged
    text = split_word(atom["text"], entry, strand)
    additions = entry.get("add", {}).get(strand, [])
    omitted = entry.get("omit", {}).get(strand, [])
    return {**atom, "text": text, "additions": list(additions),
            "omitted_accents": list(omitted)}


def _strand_notes(strand_atoms, other_strand_atoms, strand, other_strand):
    """Synthesize this strand's notes: one per SUPPLIED mark and one per accent it
    wants but UXLC OMITTED, in atom order.

    ``other_strand_atoms`` is the sibling strand's atoms — used to name the accent UXLC
    *does* have at an omitted-accent atom (the one the other strand keeps and this one
    lacks), so the note says which accent it is rather than an abstract placeholder.

    Lightweight, JSON-serializable dicts — NOT ClcNotes: strand rows own no
    anchors/always-links and no §7.9 departure record yet (design doc §7.7 keeps
    strands display-only). clc_render composes the prose around the snippet.
    """
    notes = []
    for atom, other_atom in zip(strand_atoms, other_strand_atoms):
        for added_char in atom.get("additions", ()):
            notes.append(_added_note(atom["text"], added_char))
        for omitted_char in atom.get("omitted_accents", ()):
            present = _present_accent(atom["text"], other_atom["text"])
            notes.append(_omitted_note(atom["text"], omitted_char, present, strand, other_strand))
    return tuple(notes)


def _present_accent(this_text, other_text):
    """The accent UXLC has at this atom: the (single) accent the OTHER strand keeps and
    this strand lacks — i.e. the divergent accent present in UXLC. ``None`` if none."""
    this_accents = {ch for ch in this_text if _is_accent(ch)}
    return next((ch for ch in other_text if _is_accent(ch) and ch not in this_accents), None)


def _added_note(snippet, added_char):
    return {
        "kind": _ADDED_NAME[added_char],   # "maqaf" / "sof pasuq"
        "char": added_char,                # the supplied mark itself
        "snippet": snippet,                # the strand word that receives it
        "source": clc_note.SOURCE_DUAL_CANT_ADDITION,
        "diff_type": clc_note.DIFF_DUAL_CANT_ADDED_PUNCT,
    }


def _omitted_note(snippet, accent_char, present_char, strand, other_strand):
    """An accent this strand wants but UXLC omitted — noted, not supplied. The snippet is
    the strand word AS SHOWN (that accent absent); no mark is rendered. ``present_char`` is
    the accent UXLC *does* have here (the other strand's), named in the note for concreteness."""
    return {
        "kind": _accent_name(accent_char),       # the wanted accent, e.g. "silluq"
        "char": accent_char,                     # the wanted accent (for reference; not rendered)
        "present_kind": _accent_name(present_char) if present_char else None,  # the accent UXLC has
        "present_char": present_char,
        "snippet": snippet,                      # the strand word, shown without the accent
        "strand": strand.short,                  # the strand that wants it ("elyon"/"taḥton"/…)
        "other_strand": other_strand.short,      # the strand whose accent UXLC does have
        "source": clc_note.SOURCE_DUAL_CANT_OMITTED_ACCENT,
        "diff_type": clc_note.DIFF_DUAL_CANT_OMITTED_ACCENT,
    }


def _is_subsequence(sub, whole):
    it = iter(whole)
    return all(ch in it for ch in sub)


def _validate_oracle():
    """Fail loudly at import on an oracle typo (cheap; catches bad bytes early)."""
    for book in _ORACLE.values():
        for entry in (e for verse in book.values() for e in verse.values()):
            cluster = entry["cluster"]
            for strand in (_STRAND_ALEF, _STRAND_BET):
                assert _is_subsequence(entry[strand], cluster), (entry, strand)
            for added in entry.get("add", {}).values():
                for ch in added:
                    assert ch in _SUPPLIABLE, ch  # only punctuation is ever supplied
            for omitted in entry.get("omit", {}).values():
                for ch in omitted:
                    # only ACCENTS are noted-as-omitted; punctuation would be supplied instead.
                    # Require a canonical display name so the note reads cleanly — either a
                    # curated mb_diff_mpu name or CLC's silluq override for U+05BD — never a raw
                    # "HEBREW …" Unicode fallback (see _accent_name).
                    assert _is_accent(ch), ch
                    assert ch == hpo.MTGOSLQ or ch in describe_diff.ACCENT_NAMES, ch
                    assert ch not in _SUPPLIABLE, ch


_validate_oracle()
