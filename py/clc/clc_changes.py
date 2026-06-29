"""Exports load_descriptions: index UXLC change-log prose by noted-atom citation.

UXLC's ``<x>`` element carries only a one-letter code; the human-readable prose
for each lettered note lives in the ``<correction><description>`` of the change
that added it (brainstorm §5, §7.3). We index those descriptions by the change's
citation so clc_collect can join prose onto the noted atom.

The citation key is ``(book_id, chnu, vrnu, position)`` where ``position`` is the
1-based atom index within the verse (counting <w>/<q>/<k>), matching UXLC's own
change-citation positions and the atom enumeration in clc_read.

The integer position is the join key, but it is fragile: if atoms are ever merged
or split, positions shift and the join would silently land on the wrong atom. So
each descriptor also carries ``letters`` — the letter-only form of the change's
word — as a backup the join can assert against (see clc_collect). A collision
needs *both* the position and the letter-string to match the wrong atom, which is
vanishingly unlikely outside of an immediately-repeated identical word.
"""

import os
import xml.etree.ElementTree as ET

import mb_cmn.hebrew_letters as hl
import uxlc_misc.my_uxlc_changes as my_uxlc_changes
import uxlc_misc.my_uxlc_book_abbreviations as bka

_CHANGES_DIR = "in/UXLC-misc"


def load_descriptions():
    """Map (book_id, chnu, vrnu, position) -> list of change descriptors.

    Each descriptor is ``{"text": <description prose>, "codes": [transnote type,
    ...], "letters": <letter-only form of the change's word>}``.
    """
    index = {}
    for filename in my_uxlc_changes.FILENAMES:
        path = os.path.join(_CHANGES_DIR, filename)
        if os.path.exists(path):  # FILENAMES includes a fake/placeholder that may be absent
            _index_one_file(index, path)
    return index


def _index_one_file(index, path):
    root = ET.parse(path).getroot()
    for change in root.iter("change"):
        key = _citation_key(change)
        if key is None:
            continue
        descriptor = {
            "text": change.findtext("description"),
            "codes": [tn.findtext("type") for tn in change.iter("transnote")],
            "letters": _word_letters(change),
        }
        index.setdefault(key, []).append(descriptor)


def _word_letters(change):
    # The change's word as letters only, for the backup consistency check.
    # Prefer the "after" text (changetext); fall back to "before" (reftext),
    # since note-only changes sometimes leave changetext empty in the XML.
    changetext_letters = hl.letters(change.findtext("changetext") or "")
    return changetext_letters or hl.letters(change.findtext("reftext") or "")


def _citation_key(change):
    citation = change.find("citation")
    if citation is None:
        return None
    book_id = bka.BKNA_MAP_UXLC_TO_STD.get(citation.findtext("book"))
    if book_id is None:
        return None
    try:
        chnu = int(citation.findtext("c"))
        vrnu = int(citation.findtext("v"))
        position = int(citation.findtext("position"))
    except (TypeError, ValueError):
        return None
    return book_id, chnu, vrnu, position
