"""Exports main: download a book's tanach.us note pages into committed files.

This is the *network* half of CLC notes, kept separate from the build on purpose
(like py/main_uxlc_download_changes.py downloads the core UXLC XML): the CLC build
itself (main_clc) reads only these committed local pages and never touches the
network, so its output is deterministic.

Usage (run from the repo root, network required, NOT part of the default build):

    python py/main_clc_download_notes.py [BookId]      # default: Proverbs

For each of the book's noted atoms (the same (atom, code) pairs the build uses,
via clc_collect.iter_noted_atoms), fetch
``https://tanach.us/Notes/<name>/<name>.<ch>.<v>.<position>-<code>.html`` -- where
``<name>`` is the canonical UXLC book name (my_uxlc.book_basename; e.g. id
"2Samuel" -> "Samuel_2"), the part that the build path historically got wrong --
and write the HTML to the committed
``in/UXLC-notes/<book_id>/<book_id>.<ch>.<v>.<position>-<code>.html``.

(The pages reference detail images, e.g. ``.../images/.../2-Detail.jpg``; pulling
those down can be added here later -- see the note in the loop.)
"""

import sys

import requests

from mb_cmn import polite_download
import mb_cmn.file_io as my_open
import mb_cmn.mb_cmn_bib_locales as tbn
import uxlc_misc.my_uxlc as my_uxlc
import clc.clc_collect as clc_collect
import clc.clc_note_pages as clc_note_pages
import clc.clc_read as clc_read

_DEFAULT_BOOK = tbn.BK_PROV


def note_page_url(book_id, ch, v, position, code):
    """The tanach.us note-page URL for one (atom, code), by canonical book name."""
    name = my_uxlc.book_basename(book_id)
    return f"https://tanach.us/Notes/{name}/{name}.{ch}.{v}.{position}-{code}.html"


def _download_one(session, book_id, ch, v, position, code):
    """Fetch one note page and write it locally; return True on success.

    Returns False if the page is missing (404 -- the note predates the change log,
    or tanach.us has none) or the request fails after retries.
    """
    url = note_page_url(book_id, ch, v, position, code)
    try:
        text = session.get_text(url, timeout=20, encoding="utf-8")
    except requests.RequestException:
        return False
    out_path = clc_note_pages.local_page_path(book_id, ch, v, position, code)
    _show_progress(out_path)
    my_open.with_tmp_openw(out_path, {"newline": ""}, _write_callback, text)
    # (Future) parse <img src> from `text` and download referenced detail images.
    return True


def _write_callback(text, out_fp):
    out_fp.write(text)


def _show_progress(path):
    print(path)


def main():
    """Download note pages for one book into in/UXLC-notes/ (network step)."""
    book_id = sys.argv[1] if len(sys.argv) > 1 else _DEFAULT_BOOK
    assert book_id in tbn.ALL_BOOK_IDS, f"unknown book id: {book_id!r}"
    book = clc_read.read_book(book_id)
    found = missing = 0
    with polite_download.PoliteDownloader(_NOTES_CONFIG) as session:
        for ch, v, position, _atom, code in clc_collect.iter_noted_atoms(book):
            if _download_one(session, book_id, ch, v, position, code):
                found += 1
            else:
                missing += 1
    print(
        f"CLC note pages for {book_id}: {found} downloaded, "
        f"{missing} missing (404 / no page)"
    )


_NOTES_CONFIG = polite_download.PoliteDownloadConfig(
    user_agent=(
        "Mozilla/5.0 (compatible; uxlc-clc-notes/1.0; +educational/personal-study)"
    ),
    default_timeout_s=30.0,
    accept_language="he,en;q=0.5",
    referer="https://tanach.us/",
    default_headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
    },
    throttle=polite_download.ThrottleConfig(min_delay_s=1.5, mean_delay_s=3.0),
    retry=polite_download.RetryConfig(max_attempts=4),
    cache=polite_download.CacheConfig(dir_path=".novc/http-cache/tanach-us"),
    obey_robots_txt=True,
)


if __name__ == "__main__":
    main()
