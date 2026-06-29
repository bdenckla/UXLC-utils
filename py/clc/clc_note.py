"""Exports ClcNote, the single note schema all CLC note sources flow into.

The skeleton only sources UXLC's own ``<x>`` under-bar notes (m/d/t), but the
schema is deliberately source-agnostic: bracket notes, change records, FOIs,
dagesh restorations, etc. all feed this same record (brainstorm §8, "one
renderer, many sources"). Records are plain data (JSON-serializable) so the same
notes can later drive the §7.9 differences-from-UXLC index.
"""

from dataclasses import dataclass, asdict


# --- source tags (the "source" field) ---
SOURCE_UXLC_X_NOTE = "uxlc-x-note"  # UXLC <x> note + its change-log prose
SOURCE_DUAL_CANT_ADDITION = "dual-cant-addition"  # punctuation supplied to clarify one strand

# --- difference types (the "diff_type" field, for the §7.9 index) ---
DIFF_UNDER_BAR = "under-bar"
DIFF_DUAL_CANT_ADDED_PUNCT = "dual-cant-added-punct"  # charitable additive divergence mark (§7.7)


@dataclass
class ClcNote:
    """One CLC note about one atom. Plain data; see brainstorm §8 for fields."""

    book: str            # bk39 id, e.g. "Proverbs"
    ch: int              # chapter number (1-based)
    v: int               # verse number (1-based)
    atom_index: int      # atom position within the verse (1-based; counts w/q/k)
    atom_text: str       # the pointed Hebrew atom text
    note_code: str       # UXLC one-letter <x> code, e.g. "m", "d", "t"
    note_text: str       # the tanach.us note-page prose (downloaded; see clc_note_pages)
    source: str          # provenance of the note (see SOURCE_* above)
    diff_type: str       # classification for the §7.9 index (see DIFF_* above)
    is_uxlc_departure: bool  # does CLC depart from UXLC here?
    uxlc_reading: str    # what UXLC reads at this atom
    clc_reading: str     # what CLC reads at this atom

    def as_dict(self):
        """Return a plain JSON-serializable dict of this note."""
        return asdict(self)
