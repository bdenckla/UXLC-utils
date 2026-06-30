"""Exports main: build the CLC walking skeleton for one pilot book.

Usage (run from the repo root, like the other py/main_*.py drivers):

    python py/main_clc.py [BookId] [chapter]   # default book: Proverbs

Proverbs is the default pilot because it is a single poetic book that carries
both ``m`` and ``d`` under-bar notes, so both seed paths render (build-order
step 5). Pass any bk39 id (e.g. "Psalms", "Job", "Genesis") to retarget. Pass an
optional 1-based chapter number to limit output to that chapter (e.g.
``python py/main_clc.py Exodus 20`` for the Decalogue) — handy for focusing on a
dual-cant chapter without the rest of the book.

Writes (``<label>`` is ``<book>`` for a whole book, ``<book>-<chapter>`` if limited):
    gh-pages/clc/<label>.html        the 3-column always-link page
    gh-pages/clc/<label>-notes.json  the CLC notes as plain data (feeds §7.9 later)
"""

import sys

import mb_cmn.file_io as my_open
import mb_cmn.mb_cmn_bib_locales as tbn
import clc.clc_collect as clc_collect
import clc.clc_render as clc_render

_DEFAULT_BOOK = tbn.BK_PROV


def main():
    """Build the CLC skeleton page + notes JSON for one pilot book."""
    book_id = sys.argv[1] if len(sys.argv) > 1 else _DEFAULT_BOOK
    assert book_id in tbn.ALL_BOOK_IDS, f"unknown book id: {book_id!r}"
    chapters = {int(sys.argv[2])} if len(sys.argv) > 2 else None
    book, notes = clc_collect.collect_for_book(book_id, chapters=chapters)
    html_path = clc_render.write_book(book_id, book, notes, chapters=chapters)
    label = clc_render.out_label(book_id, chapters)
    notes_path = f"gh-pages/clc/{label}-notes.json"
    my_open.json_dump_to_file_path([note.as_dict() for note in notes], notes_path)
    print(f"CLC skeleton: {len(notes)} notes for {label}")
    print(f"  wrote {html_path}")
    print(f"  wrote {notes_path}")


if __name__ == "__main__":
    main()
