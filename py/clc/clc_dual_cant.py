"""Exports the CLC dual-cantillation strand splitter (brainstorm §7.7).

A few prose loci carry **two cantillation traditions at once** — the Decalogues
(Exod 20, Deut 5) and **Genesis 35:22**, the first application here. UXLC stores
them as one *combined* form in which both readings' accents are stacked onto the
same words (e.g. רְאוּבֵ֔֗ן carries both zaqef ``U+0594`` and revia ``U+0597``).

This module splits that combined form into the two single-cantillation strands —
alef and bet — for side-by-side display. Unlike ``wlc-utils/py/accgram/
dual_cant_detangle.py`` (which *charitably supplies* missing accents and *changes
word division*), CLC's split is deliberately **strict and purely subtractive**:

  * each strand is UXLC's own combined word with **only the other strand's
    accent(s) removed** — never a mark supplied, never a maqaf/sof-pasuq/vowel
    added or removed, never a re-division;
  * MAM (via the wlc-utils detangler) is consulted **only as the oracle** for
    *which* of two stacked accents belongs to which reading — encoded once, by
    hand, in ``_ORACLE`` below. Nothing of MAM's text or division is imported.

This is the same charitable shape as the legarmeh-vs-paseq feature (§7.16): both
improve UXLC by importing MAM's auxiliary adjudication of an ambiguity that is
grammatical, not graphical.
"""

from dataclasses import dataclass


# Combining grapheme joiner: a control char (no textual meaning) used in the
# combined form only to sequence two stacked accents. Once a single accent
# remains it has nothing to sequence, so a strand drops it (cf. §7.14). Removing
# it does not violate "strict": it is not a vowel, accent, maqaf or sof-pasuq.
_CGJ = "͏"

_STRAND_ALEF = "alef"
_STRAND_BET = "bet"

# Ref-label suffixes shown in the page (user-facing): combined / alef / bet.
SUFFIX_COMBINED = "C"
SUFFIX_ALEF = "א"  # HEBREW LETTER ALEF
SUFFIX_BET = "ב"   # HEBREW LETTER BET

# Hover descriptions for each ref label.
TOOLTIP_COMBINED = (
    "Combined cantillation — both readings' accents tangled together, "
    "as written in the Leningrad Codex."
)
TOOLTIP_ALEF = (
    "Reading א (pashuṭ / simple): the verse-by-verse accentuation, "
    "strictly separated from the combined marks using MAM as oracle — "
    "no marks supplied, no division changed."
)
TOOLTIP_BET = (
    "Reading ב (midrashit / interpretive): the alternative accentuation, "
    "strictly separated the same way."
)

# Short doc-column label naming each strand's reading.
DOC_LABEL_ALEF = "pashuṭ (simple) reading"
DOC_LABEL_BET = "midrashit (interpretive) reading"


# The hardcoded oracle. For each dual-cant verse, map a 1-based atom index (only
# the *divergence* words, where the combined form stacks two accents) to the
# accent codepoint each reading keeps:  atom_index -> (alef_only, bet_only).
# Building a strand removes the *other* reading's codepoint(s) (plus any CGJ);
# every atom not listed carries a single shared accent and is left byte-for-byte.
#
# Genesis 35:22 (derived by diffing UXLC's combined words against the alef/bet
# strands in wlc-utils/out/accgram/dual-cant/_dual_cant.json):
#
#   atom  combined word   alef keeps            bet keeps
#   ----  --------------  -------------------   -------------------
#    7    רְאוּבֵ֔֗ן        zaqef qatan  U+0594   revia        U+0597
#    8    וַיִּשְׁכַּ֕ב֙      zaqef gadol  U+0595   pashta       U+0599
#   10    בִּלְהָ֖ה֙         tipeha       U+0596   pashta       U+0599
#   12    אָבִ֑֔יו          etnahta      U+0591   zaqef qatan  U+0594
#   14    יִשְׂרָאֵ֑͏ֽל       meteg/silluq U+05BD   etnahta      U+0591  (CGJ dropped)
_ORACLE = {
    "Genesis": {
        (35, 22): {
            7: ("֔", "֗"),
            8: ("֕", "֙"),
            10: ("֖", "֙"),
            12: ("֑", "֔"),
            14: ("ֽ", "֑"),
        },
    },
}


@dataclass(frozen=True)
class StrandView:
    """One displayable form of a dual-cant verse: combined, alef, or bet."""

    suffix: str    # ref-label suffix: "C" / "א" / "ב"
    tooltip: str   # hover description for the ref label
    doc_label: str  # short doc-column label ("" for the combined form)
    atoms: list    # atom dicts (same shape as clc_read: {"kind","text","types"})


def is_dual_cant(book_id, ch, v):
    """Is (book, chapter, verse) one of the dual-cantillation loci?"""
    return (ch, v) in _ORACLE.get(book_id, {})


def split_word(combined_text, alef_only, bet_only, strand):
    """Strictly split one divergence word: drop the other strand's accent(s).

    Removes only ``bet_only`` (for the alef strand) or ``alef_only`` (for the bet
    strand), plus any CGJ. Everything else — consonants, niqqud, maqaf, sof-pasuq
    and the strand's own accent — is preserved byte-for-byte.
    """
    drop = set(_CGJ)
    drop.update(bet_only if strand == _STRAND_ALEF else alef_only)
    return "".join(ch for ch in combined_text if ch not in drop)


def strand_views(book_id, ch, v, verse_atoms):
    """Return the three displayable views (combined, alef, bet) of a dual-cant verse.

    ``verse_atoms`` is the verse's atom list from clc_read. The combined view
    reuses those atoms unchanged; the alef/bet views are fresh atom dicts whose
    text has the other strand's accents subtracted (see ``split_word``).
    """
    oracle = _ORACLE[book_id][(ch, v)]
    return [
        StrandView(SUFFIX_COMBINED, TOOLTIP_COMBINED, "", verse_atoms),
        StrandView(
            SUFFIX_ALEF, TOOLTIP_ALEF, DOC_LABEL_ALEF,
            _strand_atoms(verse_atoms, oracle, _STRAND_ALEF),
        ),
        StrandView(
            SUFFIX_BET, TOOLTIP_BET, DOC_LABEL_BET,
            _strand_atoms(verse_atoms, oracle, _STRAND_BET),
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
        return atom  # shared single accent (or no accent) — unchanged
    alef_only, bet_only = entry
    return {**atom, "text": split_word(atom["text"], alef_only, bet_only, strand)}
