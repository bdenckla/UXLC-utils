"""Exports note-page prose: the *actual* tanach.us note, fetched and parsed.

UXLC's ``<x>`` code points at a per-(atom, code) note page on tanach.us, e.g.
``https://tanach.us/Notes/Proverbs/Proverbs.5.19.4-m.html``. That page's ``<h2>``
is the change-log *description* that added the note (what ``clc_changes`` indexes),
but its body ``<p>`` paragraphs are the reader-facing *note* itself -- usually
similar to, but not the same as, the change prose. This module fetches that page
(politely, cached) and returns its note prose, so ``clc_collect`` can prefer the
real note over the change-log description.

Pages are NoteMaker-generated and highly regular:

    <h1>citation</h1>
    <h2>change-log description</h2>
    <table> image + credit </table>
    <p>note prose ...</p>            (one or more, plain text)
    <p><b><i>author</i></b></p>
    <p align="right"><b><a ...>change link</a></b></p>
    <table> "all 'x' notes" / note-index links </table>

The note prose is exactly the body-level ``<p>`` that is plain text (no child
elements, no ``align``): the author and change-link paragraphs carry inline
markup, and the credit/index links live inside ``<table>``.
"""

import html.parser
import re

import requests

from mb_cmn import polite_download

_CACHE_DIR = ".novc/http-cache/tanach-us"  # shared with main_uxlc_download_changes
_USER_AGENT = (
    "Mozilla/5.0 (compatible; uxlc-clc-notes/1.0; +educational/personal-study)"
)
_NOTES_CONFIG = polite_download.PoliteDownloadConfig(
    user_agent=_USER_AGENT,
    default_timeout_s=30.0,
    accept_language="he,en;q=0.5",
    referer="https://tanach.us/",
    default_headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
    },
    throttle=polite_download.ThrottleConfig(min_delay_s=1.5, mean_delay_s=3.0),
    retry=polite_download.RetryConfig(max_attempts=4),
    cache=polite_download.CacheConfig(dir_path=_CACHE_DIR),
    obey_robots_txt=True,
)

_WS_RE = re.compile(r"\s+")


def make_session():
    """Return a PoliteDownloader for tanach.us note pages (use as a context manager)."""
    return polite_download.PoliteDownloader(_NOTES_CONFIG)


def note_page_url(book_id, ch, v, position, code):
    """The tanach.us note-page URL for one (atom, code).

    ``book_id`` is the bk39 id, which is also the tanach.us Notes folder/file name
    for single-token book names (e.g. "Proverbs"). Numbered/multi-word books would
    need a name map; until then a wrong URL simply 404s and the caller falls back.
    """
    return f"https://tanach.us/Notes/{book_id}/{book_id}.{ch}.{v}.{position}-{code}.html"


def fetch_note_prose(session, book_id, ch, v, position, code):
    """Return the note page's prose (paragraphs joined), or None if unavailable.

    None means "no usable note page" -- a 404 (the note predates the change log,
    or the URL's book name does not match tanach.us), a network failure after
    retries, or a page with no plain-text prose paragraphs. The caller then falls
    back to the change-log description.
    """
    url = note_page_url(book_id, ch, v, position, code)
    try:
        text = session.get_text(url, timeout=20, encoding="utf-8")
    except requests.RequestException:
        return None
    paragraphs = _extract_prose_paragraphs(text)
    return " ".join(paragraphs) if paragraphs else None


def _extract_prose_paragraphs(page_text):
    parser = _NoteProseExtractor()
    parser.feed(page_text)
    return parser.paragraphs


class _NoteProseExtractor(html.parser.HTMLParser):
    """Collect body-level plain-text ``<p>`` paragraphs (the note prose)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._table_depth = 0
        self._in_p = False
        self._p_has_child = False
        self._p_has_align = False
        self._buf = []
        self.paragraphs = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._table_depth += 1
        elif self._table_depth:
            pass  # ignore everything inside the image-credit / note-index tables
        elif tag == "p":
            self._in_p = True
            self._p_has_child = False
            self._p_has_align = any(name == "align" for name, _ in attrs)
            self._buf = []
        elif self._in_p:
            self._p_has_child = True  # author/link paragraphs carry inline markup

    def handle_startendtag(self, tag, attrs):
        if self._table_depth == 0 and self._in_p:
            self._p_has_child = True

    def handle_endtag(self, tag):
        if tag == "table":
            self._table_depth = max(self._table_depth - 1, 0)
        elif self._table_depth:
            pass
        elif tag == "p" and self._in_p:
            text = _WS_RE.sub(" ", "".join(self._buf)).strip()
            if text and not self._p_has_child and not self._p_has_align:
                self.paragraphs.append(text)
            self._in_p = False

    def handle_data(self, data):
        if self._table_depth == 0 and self._in_p:
            self._buf.append(data)
