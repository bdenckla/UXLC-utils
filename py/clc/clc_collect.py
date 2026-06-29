"""Exports collect_for_book: UXLC <x> notes + their note-page prose -> ClcNotes.

This is the skeleton's note source (build-order step 3). It surfaces the
under-bar ambiguity UXLC already flags (m/d/t) but does NOT yet resolve it:
there is no accent grammar and no charitable departure here, so every note has
``is_uxlc_departure=False`` and ``clc_reading == uxlc_reading``. Charity layers
on later (brainstorm §3, §7.1).

Each note's prose is the *actual* tanach.us note page (clc_note_pages), which is
usually similar to but not the same as the change-log description that added the
note. The change-log description (clc_changes) is kept only as a fallback for
the few atoms whose note page is missing.
"""

import mb_cmn.hebrew_letters as hl
import clc.clc_changes as clc_changes
import clc.clc_note as clc_note
import clc.clc_note_pages as clc_note_pages
import clc.clc_read as clc_read

# The under-bar ambiguity codes that seed CLC (brainstorm §2): m (prose
# merkha/meteg), d (poetic deḥi/tarḥa), and the catch-all t. Listed m/d/t first.
UNDER_BAR_CODES = ("m", "d", "t")

# Fallback note text for the few atoms whose code predates the change log and so
# has no <description> prose (brainstorm §9 #2). Avoids borrowing unrelated prose.
_CODE_MEANING = {
    "m": "possible merkha rather than meteg (prose under-bar)",
    "d": "possible deḥi re-read as tipeḥa/tarḥa (poetic under-bar)",
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


def collect_for_book(book_id, codes=UNDER_BAR_CODES):
    """Read book_id and emit ClcNotes for atoms carrying one of ``codes``.

    Returns ``(book, notes)`` where ``book`` is the read structure (chapters ->
    verses -> atoms) and ``notes`` is a list of ClcNote.
    """
    book = clc_read.read_book(book_id)
    descriptions = clc_changes.load_descriptions()
    notes = []
    page_prose_count = 0
    with clc_note_pages.make_session() as session:
        for chidx, chapter in enumerate(book):
            for vridx, verse in enumerate(chapter):
                for atidx, atom in enumerate(verse):
                    position = atidx + 1
                    for code in atom["types"]:
                        if code in codes:
                            ch, v = chidx + 1, vridx + 1
                            prose = clc_note_pages.fetch_note_prose(
                                session, book_id, ch, v, position, code
                            )
                            page_prose_count += prose is not None
                            notes.append(
                                _make_note(
                                    book_id, ch, v, position,
                                    atom, code, descriptions, prose,
                                )
                            )
    _report_prose_coverage(page_prose_count, len(notes))
    return book, notes


def _report_prose_coverage(page_prose_count, total):
    fallbacks = total - page_prose_count
    print(
        f"CLC notes: {page_prose_count}/{total} use tanach.us note-page prose; "
        f"{fallbacks} fall back to the change-log description"
    )


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
        note_text=page_prose or _change_log_text(records, code),
        source=clc_note.SOURCE_UXLC_X_NOTE,
        diff_type=clc_note.DIFF_UNDER_BAR,
        is_uxlc_departure=False,    # skeleton only surfaces the ambiguity
        uxlc_reading=atom_text,
        clc_reading=atom_text,      # ... so CLC's reading == UXLC's for now
    )


def _change_log_text(records, code):
    """Fallback when no note page: the change-log description, else code meaning."""
    matching = [r["text"] for r in records if code in (r["codes"] or []) and r["text"]]
    if matching:
        return matching[0]
    return _fallback_text(code)


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
