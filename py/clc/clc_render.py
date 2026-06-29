"""Exports write_book: render a CLC book as a 3-column always-link page.

Layout (brainstorm §7.3, build-order step 4): one row per verse, columns
``ref | text | doc``. The text column is running verse text; every noted word is
an always-link (no MAM short-inline / long-link threshold) to its note in the
doc column of the same row. CLC defines its own ``clc-*`` CSS vocabulary parallel
to MAM's ``mam-doc-*`` (brainstorm §8); the rules live in gh-pages/style.css.
"""

import uxlc_misc.uxlc_utils_html as H

_OUT_DIR = "gh-pages/clc"
_HBO_ATTR = {"lang": "hbo", "dir": "rtl"}


def write_book(book_id, book, notes):
    """Write gh-pages/clc/<book_id>.html and return its path."""
    notes_by_atom = _group_by_atom(notes)
    rows = [H.table_row_of_headers(("ref", "text", "doc"))]
    for chidx, chapter in enumerate(book):
        for vridx, verse in enumerate(chapter):
            rows.append(_verse_row(chidx + 1, vridx + 1, verse, notes_by_atom))
    table = H.table(rows, {"class": "clc-3col border-collapse"})
    body = _body_wrapper(book_id, notes, table)
    out_path = f"{_OUT_DIR}/{book_id}.html"
    write_ctx = H.WriteCtx(title=f"CLC — {book_id}", path=out_path, add_wbr=True)
    H.write_html_to_file(body, write_ctx, "../")
    return out_path


def _group_by_atom(notes):
    grouped = {}
    for note in notes:
        grouped.setdefault((note.ch, note.v, note.atom_index), []).append(note)
    return grouped


def _verse_row(ch, v, verse, notes_by_atom):
    ref_cell = H.table_datum(f"{ch}:{v}", {"class": "clc-ref"})
    text_cell = H.table_datum(
        _text_contents(ch, v, verse, notes_by_atom),
        {**_HBO_ATTR, "class": "clc-text"},
    )
    doc_cell = H.table_datum(
        _doc_contents(ch, v, verse, notes_by_atom), {"class": "clc-doc"}
    )
    return H.table_row((ref_cell, text_cell, doc_cell))


def _text_contents(ch, v, verse, notes_by_atom):
    pieces = []
    for atidx, atom in enumerate(verse):
        atom_text = atom["text"]
        if (ch, v, atidx + 1) in notes_by_atom:
            href = f"#{_anchor_id(ch, v, atidx + 1)}"
            pieces.append(H.anchor(atom_text, {"href": href, "class": "clc-doc-target"}))
        else:
            pieces.append(atom_text)
        pieces.append(" ")
    return pieces


def _doc_contents(ch, v, verse, notes_by_atom):
    blocks = []
    for atidx, _atom in enumerate(verse):
        atom_notes = notes_by_atom.get((ch, v, atidx + 1))
        if atom_notes:
            blocks.append(_note_block(ch, v, atidx + 1, atom_notes))
    return blocks


def _note_block(ch, v, position, atom_notes):
    entries = [
        H.span(f"{ch}:{v}.{position} ", {"class": "clc-note-ref"}),
        H.span(atom_notes[0].atom_text, _HBO_ATTR),
    ]
    for note in atom_notes:
        entries.append(H.line_break())
        entries.append(H.span(f"[{note.note_code}] ", {"class": "clc-note-code"}))
        entries.append(note.note_text)
    return H.div(entries, {"id": _anchor_id(ch, v, position), "class": "clc-note"})


def _anchor_id(ch, v, position):
    return f"clc-{ch}-{v}-{position}"


def _body_wrapper(book_id, notes, table):
    style = "max-width: 60rem; margin-left: auto; margin-right: auto"
    contents = [
        H.heading_level_1(f"Charitable Leningrad Codex — {book_id}"),
        _intro_para(notes),
        table,
    ]
    return [H.div(contents, {"style": style})]


def _intro_para(notes):
    return H.para(
        [
            "CLC walking skeleton. This page surfaces UXLC's own ",
            H.code("<x>"),
            f" under-bar notes ({_code_counts_text(notes)}) as always-links, each "
            "carrying the note prose from the UXLC change log. No accent grammar "
            "and no charitable resolution yet — see doc/clc-brainstorm.md.",
        ]
    )


def _code_counts_text(notes):
    counts = {}
    for note in notes:
        counts[note.note_code] = counts.get(note.note_code, 0) + 1
    parts = [f"{counts[code]}×{code}" for code in ("m", "d", "t") if code in counts]
    return ", ".join(parts) if parts else "none"
