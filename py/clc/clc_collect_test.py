"""Self-contained test for clc_collect (the CLC note-collection module).

Run from anywhere:  python py/clc/clc_collect_test.py
Prints "clc_collect: OK" on success; raises AssertionError on failure.

Covers clc_collect's pending-UXLC-change patch (_UXLC_PENDING_CHANGES_APPLIED):
Deut 5:8.2's mid-word pashta is corrected to a qadma upstream, before any note or
strand split ever runs — CLC's first-ever real is_uxlc_departure=True instance
(design doc §7.4), and the first real UXLC-text departure the strand oracle
(clc_dual_cant) sees, rather than an omitted-accent annotation.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_PY_ROOT = os.path.dirname(_HERE)            # py/
sys.path.insert(0, _PY_ROOT)

import clc.clc_collect as clc_collect  # noqa: E402
import clc.clc_dual_cant as clc_dual_cant  # noqa: E402
import clc.clc_note as clc_note  # noqa: E402
import clc.clc_render as clc_render  # noqa: E402
import mb_cmn.hebrew_accents as acc  # noqa: E402
import uxlc_misc.uxlc_utils_html as H  # noqa: E402


def _deut_5_8_atom2_note(notes):
    matches = [n for n in notes if n.ch == 5 and n.v == 8 and n.atom_index == 2]
    assert len(matches) == 1, matches
    return matches[0]


def test_text_patch():
    book, _notes = clc_collect.collect_for_book("Deuter", chapters={5})
    atom = book[4][7][1]  # ch5, v8, atom-index 2 (0-based: [4][7][1])
    assert acc.QOM in atom["text"] and acc.PASH not in atom["text"], atom["text"]


def test_note_fields():
    _book, notes = clc_collect.collect_for_book("Deuter", chapters={5})
    note = _deut_5_8_atom2_note(notes)
    assert note.is_uxlc_departure is True
    assert acc.PASH in note.uxlc_reading and acc.QOM not in note.uxlc_reading
    assert acc.QOM in note.clc_reading and acc.PASH not in note.clc_reading
    assert note.diff_type == clc_note.DIFF_UXLC_PENDING_CHANGE_APPLIED
    assert note.superseding_uxlc_change == ("2026.10.19", "2026.04.10-10")
    assert note.note_code == "t"


def test_no_leakage():
    _book, notes = clc_collect.collect_for_book("Deuter", chapters={5})
    for note in notes:
        if note.ch == 5 and note.v == 8 and note.atom_index == 2:
            continue
        assert note.is_uxlc_departure is False, note
        assert note.uxlc_reading == note.clc_reading == note.atom_text, note


def test_render():
    _book, notes = clc_collect.collect_for_book("Deuter", chapters={5})
    note = _deut_5_8_atom2_note(notes)
    html = H.el_to_str_no_wbr(clc_render._note_block(5, 8, 2, [note]))
    assert "clc-added-note" in html
    assert "pashta" in html and "qadma" in html
    # No note-code prefix or superseding-change citation: those belong to showing
    # the UXLC note itself, which this departure note deliberately doesn't. But
    # "pending change" itself links to the change record.
    assert 'class="clc-note-code"' not in html
    assert 'class="clc-superseded-cite"' not in html
    assert '>pending change</a>' in html
    assert "2026.04.10-10" in html  # in the link's href, not as visible cite text
    assert note.note_text not in html  # still-suppressed stale prose never shown


def test_dual_cant_integration():
    # Confirms clc_dual_cant._ORACLE's simplified dt 5:8 atom-2 entry (no more "omit")
    # against *real* patched input, not just in isolation.
    book, _notes = clc_collect.collect_for_book("Deuter", chapters={5})
    _c8, alef8, bet8 = clc_dual_cant.strand_views("Deuter", 5, 8, book[4][7])
    assert acc.QOM in alef8.atoms[1]["text"] and acc.PASH not in alef8.atoms[1]["text"]
    assert acc.QOM in bet8.atoms[1]["text"] and acc.PASH not in bet8.atoms[1]["text"]
    OMIT = clc_dual_cant.clc_note.SOURCE_DUAL_CANT_OMITTED_ACCENT
    assert [n for n in alef8.notes if n["source"] == OMIT] == []
    assert [n for n in bet8.notes if n["source"] == OMIT] == []


def main():
    test_text_patch()
    test_note_fields()
    test_no_leakage()
    test_render()
    test_dual_cant_integration()
    print("clc_collect: OK")


if __name__ == "__main__":
    main()
