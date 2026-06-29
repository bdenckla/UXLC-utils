"""Exports note-page prose: the *actual* tanach.us note, fetched and parsed.

UXLC's ``<x>`` code points at a per-(atom, code) note page on tanach.us, e.g.
``https://tanach.us/Notes/Proverbs/Proverbs.5.19.4-m.html``. Its reader-facing
*note* prose is usually similar to, but not the same as, the change-log
*description* that added it (what ``clc_changes`` indexes). This module fetches
that page (politely, cached) and returns its note prose, so ``clc_collect`` can
prefer the real note over the change-log description.

Two page formats are in the wild and must both be handled:

  * NoteMaker-generated (newer): prose is body-level ``<p>`` paragraphs; the
    change-log description is an ``<h2>``; the author is ``<p><b><i>...</i></b></p>``
    and the change link a ``<p align="right"><b><a>...</a></b></p>``.

  * Hand-authored (older, ~2021): the note's lead line is an ``<h4>`` and the rest
    of the prose is *bare* body text split by self-closing ``<p/>`` separators (no
    ``<p>...</p>`` wrappers at all); the author is a bare ``<b><i>...</i></b>``.

Both formats share the same noise, so one rule covers them: the prose is the body
text that is NOT inside a ``<table>`` (image credit / note index), NOT inside the
``<h1>`` citation or ``<h2>`` change-log description, and NOT inside inline markup
(``<b>``/``<i>``/``<a>``, which wrap the author and the change link). Everything
else in the body -- ``<p>`` text, ``<h4>`` text, and bare text -- is note prose.
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


# Inline markup that wraps non-prose (author byline, change link, image credit).
# Text inside any of these is skipped in both page formats.
_SKIP_TEXT_TAGS = frozenset({"b", "i", "a", "em", "strong"})
# Headings that are not prose: the citation and the change-log description.
_SKIP_HEADING_TAGS = frozenset({"h1", "h2"})
# Block-level tags whose boundaries end one prose run and start the next.
_BLOCK_TAGS = frozenset(
    {"p", "br", "div", "center", "tr", "li", "h1", "h2", "h3", "h4", "h5", "h6"}
)


class _NoteProseExtractor(html.parser.HTMLParser):
    """Collect the body note prose across both tanach.us note-page formats.

    Prose is body text outside any ``<table>``, outside the ``<h1>``/``<h2>``
    citation and change-log heading, and outside inline ``<b>``/``<i>``/``<a>``
    author and change-link markup. Block boundaries split it into paragraphs.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._in_body = False
        self._table_depth = 0
        self._heading_depth = 0   # inside <h1>/<h2> (citation, change description)
        self._inline_depth = 0    # inside <b>/<i>/<a> (author, link, credit)
        self._buf = []
        self.paragraphs = []

    def _collecting(self):
        return (
            self._in_body
            and not self._table_depth
            and not self._heading_depth
            and not self._inline_depth
        )

    def _flush(self):
        text = _WS_RE.sub(" ", "".join(self._buf)).strip()
        if text:
            self.paragraphs.append(text)
        self._buf = []

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self._in_body = True
        elif tag in _BLOCK_TAGS:
            self._flush()  # close any run before a block boundary
        if tag == "table":
            self._table_depth += 1
        elif tag in _SKIP_HEADING_TAGS:
            self._heading_depth += 1
        elif tag in _SKIP_TEXT_TAGS:
            self._inline_depth += 1

    def handle_startendtag(self, tag, attrs):
        if tag in _BLOCK_TAGS:
            self._flush()  # self-closing <p/> and <br/> are paragraph separators

    def handle_endtag(self, tag):
        if tag in _BLOCK_TAGS:
            self._flush()
        if tag == "table":
            self._table_depth = max(self._table_depth - 1, 0)
        elif tag in _SKIP_HEADING_TAGS:
            self._heading_depth = max(self._heading_depth - 1, 0)
        elif tag in _SKIP_TEXT_TAGS:
            self._inline_depth = max(self._inline_depth - 1, 0)

    def handle_data(self, data):
        if self._collecting():
            self._buf.append(data)
