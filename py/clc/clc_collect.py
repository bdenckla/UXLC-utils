"""Exports collect_for_book: UXLC <x> notes + their note-page prose -> ClcNotes.

This is the skeleton's note source (build-order step 3). It surfaces the
under-bar ambiguity UXLC already flags (m/d/t) but does NOT yet resolve it:
there is no accent grammar and no charitable departure here, so every note has
``is_uxlc_departure=False`` and ``clc_reading == uxlc_reading``. Charity layers
on later (design doc §3, §7.1).

Each note's prose is the *actual* tanach.us note page, read offline from the
committed local copy (clc_note_pages; downloaded by main_clc_download_notes). The
build never touches the network, so its output is deterministic. An atom with no
local page shows a fixed per-code marker -- never the imperative change-log
description, which is an instruction to the editor, not a note. clc_changes is
kept only for the atom-letter consistency guard.
"""

import mb_cmn.hebrew_letters as hl
import clc.clc_changes as clc_changes
import clc.clc_note as clc_note
import clc.clc_note_pages as clc_note_pages
import clc.clc_read as clc_read
import uxlc_misc.my_uxlc as my_uxlc

# The under-bar ambiguity codes that seed CLC (design doc §2): m (prose
# merkha/meteg), d (poetic deḥi/tarḥa), and the catch-all t. Listed m/d/t first.
UNDER_BAR_CODES = ("m", "d", "t")

# Marker shown for an atom with no downloaded note page (e.g. its code predates
# the change log, design doc §9 #2). A fixed per-code constant, so the output
# stays deterministic; never the imperative change-log description.
_CODE_MEANING = {
    "m": "possible merkha rather than meteg (prose under-bar)",
    "d": "possible deḥi re-read as tipeḥa/tarḥa (poetic under-bar)",
    "t": "transcription uncertainty — examine the mark below the letter",
}

# Reviewed atom/change-log letter mismatches that are NOT atom merges/splits and
# so are accepted rather than raised by _check_atom_consistency. Keyed by
# (book, ch, v, position) with the reason. Any *unlisted* mismatch still raises.
_KNOWN_ATOM_MISMATCHES = {
    ("Jeremiah", 27, 11, 10): (
        "Current UXLC reads וְהִנַּחְתִּיו (3ms suffix vav); the 2023 'severely "
        "damaged text' change recorded וְהִנַּחְתִּי (no suffix vav). Position is "
        "correct — the change-log text differs from current UXLC by one letter."
    ),
}


def iter_noted_atoms(book, codes=UNDER_BAR_CODES):
    """Yield ``(ch, v, position, atom, code)`` for each atom carrying a code.

    The single source of truth for which (atom, code) pairs are CLC notes, shared
    by collect_for_book and the note-page downloader (main_clc_download_notes) so
    the two cannot drift. ``position`` is the 1-based atom index within the verse.
    """
    for chidx, chapter in enumerate(book):
        for vridx, verse in enumerate(chapter):
            for atidx, atom in enumerate(verse):
                for code in atom["types"]:
                    if code in codes:
                        yield chidx + 1, vridx + 1, atidx + 1, atom, code


def collect_for_book(book_id, codes=UNDER_BAR_CODES, chapters=None):
    """Read book_id and emit ClcNotes for atoms carrying one of ``codes``.

    Returns ``(book, notes)`` where ``book`` is the full read structure (chapters
    -> verses -> atoms) and ``notes`` is a list of ClcNote. Reads note prose
    offline from the committed local pages (clc_note_pages); never the network.
    ``chapters`` (a set of 1-based chapter numbers, or None) limits note
    collection to those chapters; ``book`` is still the whole book, and the render
    side applies the same limit.
    """
    book = clc_read.read_book(book_id)
    descriptions = clc_changes.load_descriptions()
    notes = []
    page_prose_count = 0
    for ch, v, position, atom, code in iter_noted_atoms(book, codes):
        if chapters is not None and ch not in chapters:
            continue
        prose = clc_note_pages.local_note_prose(book_id, ch, v, position, code)
        page_prose_count += prose is not None
        notes.append(
            _make_note(book_id, ch, v, position, atom, code, descriptions, prose)
        )
    _report_prose_coverage(page_prose_count, len(notes))
    return book, notes


def _report_prose_coverage(page_prose_count, total):
    missing = total - page_prose_count
    msg = (
        f"CLC notes: {page_prose_count}/{total} use a downloaded note page; "
        f"{missing} have no local page (generic per-code marker)."
    )
    if missing:
        msg += " Run main_clc_download_notes to fetch the missing pages."
    print(msg)


def _make_note(book_id, ch, v, position, atom, code, descriptions, page_prose):
    atom_text = atom["text"]
    records = descriptions.get((book_id, ch, v, position), [])
    _check_atom_consistency(book_id, ch, v, position, atom_text, records)
    return clc_note.ClcNote(
        book=book_id,
        ch=ch,
        v=v,
        atom_index=position,
        atom_text=atom_text,
        note_code=code,
        note_text=page_prose or _fallback_text(code),
        source=clc_note.SOURCE_UXLC_X_NOTE,
        diff_type=clc_note.DIFF_UNDER_BAR,
        is_uxlc_departure=False,    # skeleton only surfaces the ambiguity
        uxlc_reading=atom_text,
        clc_reading=atom_text,      # ... so CLC's reading == UXLC's for now
        source_url=my_uxlc.note_page_url(book_id, ch, v, position, code)
        if page_prose
        else "",
    )


def _fallback_text(code):
    return f"UXLC ‘{code}’ note: {_CODE_MEANING.get(code, 'see UXLC')}."


def _check_atom_consistency(book_id, ch, v, position, atom_text, records):
    """Backup guard for the fragile position-based join (see clc_changes).

    The integer position is the join key; the letter-only atom text is the
    backup. Every change cited at this position recorded the word(s) then
    present, so the current atom should match one of them (a ketiv/qere pair
    contributes both members). If it matches none, the atomization has drifted
    (atoms merged or split) and the position no longer means what the change log
    meant — we fail loudly rather than silently mislabel the atom. Reviewed
    exceptions that are not merges/splits live in _KNOWN_ATOM_MISMATCHES.
    """
    expected = {r["letters"] for r in records if r["letters"]}
    if not expected:
        return  # no recorded letters to verify against
    actual = hl.letters(atom_text)
    if actual in expected:
        return
    accepted = (book_id, ch, v, position) in _KNOWN_ATOM_MISMATCHES
    assert accepted, (
        f"CLC atom/change-log mismatch at {book_id} {ch}:{v}.{position}: atom "
        f"letters {actual!r} match none of the change-log letters "
        f"{sorted(expected)!r}. Either atom positions shifted (atoms merged or "
        "split) since the notes were recorded, or the change log's recorded text "
        "differs from current UXLC at this position. If reviewed and acceptable, "
        "add (book, ch, v, position) to _KNOWN_ATOM_MISMATCHES."
    )
