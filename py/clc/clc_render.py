"""Exports write_book: render a CLC book as a 3-column always-link page.

Layout (brainstorm §7.3, build-order step 4): one row per verse, columns
``text | ref | doc``. The verse-number (ref) is a narrow central spine with the
Hebrew text on its left and the doc apparatus on its right; keeping the text
adjacent to the ref means a short verse stays butted against its label (no need
for zebra shading to tie the two together). The text column is running verse
text; every noted word is an always-link (no MAM short-inline / long-link
threshold) to its note in the doc column of the same row. CLC defines its own
``clc-*`` CSS vocabulary parallel
to MAM's ``mam-doc-*`` (brainstorm §8); the rules live in gh-pages/style.css.
"""

import mb_cmn.hebrew_punctuation as hpu   # for hpu.MAQ (־, U+05BE)
import clc.clc_dual_cant as clc_dual_cant
import clc.clc_kq as clc_kq
import uxlc_misc.uxlc_utils_html as H

_OUT_DIR = "gh-pages/clc"
_HBO_ATTR = {"lang": "hbo", "dir": "rtl"}


def write_book(book_id, book, notes):
    """Write gh-pages/clc/<book_id>.html and return its path."""
    notes_by_atom = _group_by_atom(notes)
    rows = [H.table_row_of_headers(("text", "ref", "doc"))]
    for chidx, chapter in enumerate(book):
        for vridx, verse in enumerate(chapter):
            ch, v = chidx + 1, vridx + 1
            if clc_dual_cant.is_dual_cant(book_id, ch, v):
                rows.extend(_dual_cant_rows(book_id, ch, v, verse, notes_by_atom))
            else:
                rows.append(_verse_row(ch, v, verse, notes_by_atom))
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
    return H.table_row((text_cell, ref_cell, doc_cell))


def _dual_cant_rows(book_id, ch, v, verse, notes_by_atom):
    # A dual-cantillation verse (e.g. Gen 35:22) becomes three grouped rows:
    # combined (C), strand alef (א), strand bet (ב). The combined row keeps the
    # full always-link behaviour (its notes/anchors); the strand rows show the
    # strictly-split text plain, with only a short reading label in the doc
    # column. CSS ties the three into one verse block (gh-pages/style.css).
    views = clc_dual_cant.strand_views(book_id, ch, v, verse)
    rows = []
    for pos, view in enumerate(views):
        ref_cell = H.table_datum(
            f"{ch}:{v}-{view.suffix}", _strand_ref_attr(view.tooltip, pos, len(views))
        )
        if view.suffix == clc_dual_cant.SUFFIX_COMBINED:
            text_cell = H.table_datum(
                _text_contents(ch, v, view.atoms, notes_by_atom),
                {**_HBO_ATTR, "class": "clc-text"},
            )
            doc_cell = H.table_datum(
                _doc_contents(ch, v, view.atoms, notes_by_atom), {"class": "clc-doc"}
            )
        else:
            text_cell = H.table_datum(
                _plain_text_contents(view.atoms, verse), {**_HBO_ATTR, "class": "clc-text"}
            )
            doc_cell = H.table_datum(
                H.span(view.doc_label, {"class": "clc-strand-label"}), {"class": "clc-doc"}
            )
        rows.append(H.table_row((text_cell, ref_cell, doc_cell)))
    return rows


def _strand_ref_attr(tooltip, pos, count):
    # Group the strand rows into one verse block: the first row keeps the top
    # divider, the last keeps the bottom one, the middle rows drop both.
    classes = ["clc-ref", "clc-ref-strand"]
    if pos == 0:
        classes.append("clc-strand-first")
    if pos == count - 1:
        classes.append("clc-strand-last")
    return {"class": " ".join(classes), "title": tooltip}


def _text_contents(ch, v, verse, notes_by_atom):
    # Group ketiv/qere atoms into units (clc_kq) so each renders as one boxed
    # ruby — qere on the baseline, ketiv above — and adjacent independent pairs
    # stay visibly separate from a grouped multi-word unit. Plain words render
    # exactly as before: an always-link if noted, otherwise bare text.
    pieces = []
    for item in clc_kq.iter_render_units(verse):
        if isinstance(item, clc_kq.KqUnit):
            pieces.append(clc_kq.kq_ruby(item, notes_by_atom, ch, v))
            _append_join_space(pieces, clc_kq.join_text(item))
        else:
            if (ch, v, item.position) in notes_by_atom:
                href = f"#{_anchor_id(ch, v, item.position)}"
                pieces.append(H.anchor(item.text, {"href": href, "class": "clc-doc-target"}))
            else:
                pieces.append(item.text)
            _append_join_space(pieces, item.text)
    return pieces


def _plain_text_contents(strand_atoms, combined_atoms):
    # Like _text_contents but with no note always-links — used by the alef/bet
    # strand rows of a dual-cant verse, whose notes/anchors live on the combined
    # row only (re-emitting them here would duplicate anchor ids). Each word
    # identical to the combined form is de-highlighted (clc-strand-same) so the
    # few divergence words stand out by contrast.
    pieces = []
    for strand_atom, combined_atom in zip(strand_atoms, combined_atoms):
        atom_text = strand_atom["text"]
        if atom_text == combined_atom["text"]:
            pieces.append(H.span(atom_text, {"class": "clc-strand-same"}))
        else:
            pieces.append(atom_text)
        _append_join_space(pieces, atom_text)
    return pieces


def _append_join_space(pieces, atom_text):
    # Smart-join: an atom ending in maqaf butts directly against the next atom
    # (one hyphenated compound, e.g. אֶת־הָאָרֶץ); add_wbr still allows a line
    # break at the maqaf. Only non-maqaf atoms get a separating space.
    if not atom_text.endswith(hpu.MAQ):
        pieces.append(" ")


def _doc_contents(ch, v, verse, notes_by_atom):
    blocks = []
    for atidx, _atom in enumerate(verse):
        atom_notes = notes_by_atom.get((ch, v, atidx + 1))
        if atom_notes:
            blocks.append(_note_block(ch, v, atidx + 1, atom_notes))
    return blocks


def _note_block(ch, v, position, atom_notes):
    entries = [
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
            "carrying its tanach.us note-page prose (the change-log description that "
            "added the note is used only as a fallback). No accent grammar and no "
            "charitable resolution yet — see doc/clc-brainstorm.md.",
        ]
    )


def _code_counts_text(notes):
    counts = {}
    for note in notes:
        counts[note.note_code] = counts.get(note.note_code, 0) + 1
    parts = [f"{counts[code]}×{code}" for code in ("m", "d", "t") if code in counts]
    return ", ".join(parts) if parts else "none"
