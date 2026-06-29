"""Exports the CLC dual-cantillation strand splitter (brainstorm §7.7).

A few prose loci carry **two cantillation traditions at once** — the Decalogues
(Exod 20, Deut 5) and **Genesis 35:22**, the first application here. UXLC stores
them as one *combined* form in which both readings' accents are stacked onto the
same words (e.g. רְאוּבֵ֔֗ן carries both zaqef ``U+0594`` and revia ``U+0597``).

This module splits that combined form into the two single-cantillation strands —
alef and bet — for side-by-side display. The split is **near-subtractive, with
two narrowly-scoped charities** — a deliberate, *loud* departure from a purely
subtractive split (cf. ``wlc-utils/py/accgram/dual_cant_detangle.py``, which is
charitable but silent):

  * **Position-safe subtraction.** Each strand is UXLC's own combined word with
    only the *other* strand's **divergence cluster** resolved: an accent, and —
    where the two readings stack them on one letter — the other strand's **vowel**
    (a QUPO word's patax vs. qamats) or **rafe/dagesh**. The cluster is replaced
    *by name at its exact site* (``str.replace(cluster, resolution, 1)``), so a
    mark that recurs elsewhere in the word as a *shared* mark is never touched.
  * **Supplied punctuation.** A strand may have a **maqaf or sof-pasuq supplied**
    — never anything else — *only* to improve legibility of that single reading
    (e.g. a sof-pasuq breaking Gen 35:22's pashuṭ into its two chanted verses).
    Every supplied mark is rendered **bracketed and green** (CSS
    ``clc-added-during-detangling``) and carries a synthesized "added out of thin
    air" note; nothing is silently baked in (clc_render renders both).

No consonant is changed, no *shared* mark removed, no re-division. MAM (via the
wlc-utils detangler) is consulted **only as the oracle** for *which* of two
stacked marks belongs to which reading, and where a supplied break falls —
encoded once, by hand, in ``_ORACLE`` below. Nothing of MAM's text is imported.

This is the same charitable shape as the legarmeh-vs-paseq feature (§7.16): both
improve UXLC by importing MAM's auxiliary adjudication of an ambiguity that is
grammatical, not graphical.
"""

from dataclasses import dataclass

import mb_cmn.hebrew_accents as acc
import mb_cmn.hebrew_letters as hl
import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_punctuation as hpu
import clc.clc_note as clc_note


# Combining grapheme joiner: a control char (no textual meaning) used in the
# combined form only to sequence two stacked accents. Once a single accent
# remains it has nothing to sequence, so a strand drops it (cf. §7.14). It lives
# inside a divergence cluster (atom 14) and simply isn't in either resolution.
_CGJ = "͏"

_STRAND_ALEF = "alef"
_STRAND_BET = "bet"

# The closed set of marks a strand may have SUPPLIED (the additive charity).
_SUPPLIABLE = {hpu.MAQ, hpu.SOPA}
# Display names for a supplied mark, used in the synthesized doc-column note.
_ADDED_NAME = {hpu.MAQ: "maqaf", hpu.SOPA: "sof pasuq"}

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
    "separated from the combined marks using MAM as oracle — no mark "
    "subtracted but the other reading's, only a maqaf/sof-pasuq supplied."
)
TOOLTIP_BET = (
    "Reading ב (midrashit / interpretive): the alternative accentuation, "
    "separated the same way."
)

# Short doc-column label naming each strand's reading.
DOC_LABEL_ALEF = "pashuṭ (simple) reading"
DOC_LABEL_BET = "midrashit (interpretive) reading"


# The hardcoded oracle. For each dual-cant verse, map a 1-based atom index (only
# the *divergence* words, where the two readings stack marks) to a resolution:
#
#   atom_index -> {
#       "cluster": exact combined substring that diverges (incl. CGJ if present),
#       "alef":    the cluster's alef resolution (a subsequence of "cluster"),
#       "bet":     the cluster's bet  resolution (a subsequence of "cluster"),
#       "add":     optional {strand: [char, ...]} of maqaf/sof-pasuq SUPPLIED to
#                  that strand (rendered bracketed/green + a synthesized note),
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
}


@dataclass(frozen=True)
class StrandView:
    """One displayable form of a dual-cant verse: combined, alef, or bet."""

    suffix: str    # ref-label suffix: "C" / "א" / "ב"
    tooltip: str   # hover description for the ref label
    doc_label: str  # short doc-column label ("" for the combined form)
    atoms: list    # atom dicts (clc_read shape + "additions" on split atoms)
    added_notes: tuple = ()  # synthesized "added out of thin air" notes (strand only)


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
    plus an ``additions`` list, and a tuple of synthesized notes for any marks it
    supplies.
    """
    oracle = _ORACLE[book_id][(ch, v)]
    alef_atoms = _strand_atoms(verse_atoms, oracle, _STRAND_ALEF)
    bet_atoms = _strand_atoms(verse_atoms, oracle, _STRAND_BET)
    return [
        StrandView(SUFFIX_COMBINED, TOOLTIP_COMBINED, "", verse_atoms),
        StrandView(
            SUFFIX_ALEF, TOOLTIP_ALEF, DOC_LABEL_ALEF,
            alef_atoms, _strand_added_notes(alef_atoms),
        ),
        StrandView(
            SUFFIX_BET, TOOLTIP_BET, DOC_LABEL_BET,
            bet_atoms, _strand_added_notes(bet_atoms),
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
    return {**atom, "text": text, "additions": list(additions)}


def _strand_added_notes(strand_atoms):
    """Synthesize one note per supplied mark across a strand's atoms.

    Lightweight, JSON-serializable dicts — NOT ClcNotes: strand rows own no
    anchors/always-links and no §7.9 departure record yet (brainstorm §7.7 keeps
    strands display-only). clc_render composes the prose around the snippet.
    """
    notes = []
    for atom in strand_atoms:
        for added_char in atom.get("additions", ()):
            notes.append(_added_note(atom["text"], added_char))
    return tuple(notes)


def _added_note(snippet, added_char):
    return {
        "kind": _ADDED_NAME[added_char],   # "maqaf" / "sof pasuq"
        "char": added_char,                # the supplied mark itself
        "snippet": snippet,                # the strand word that receives it
        "source": clc_note.SOURCE_DUAL_CANT_ADDITION,
        "diff_type": clc_note.DIFF_DUAL_CANT_ADDED_PUNCT,
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
                    assert ch in _SUPPLIABLE, ch


_validate_oracle()
