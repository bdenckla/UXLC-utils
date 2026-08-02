"""Resolve the UXLC-utils DATA root, and the subtrees this repo's code reads and writes.

THIS MODULE IS DELIBERATELY TWO-ROOTED, and that is the whole point of its
existence.  Today the code and the corpus are both in this repo, so the two roots
have the same value and nothing distinguishes them.  That stops being true when
the Python moves into MAM-basics (``MAM-basics/doc/PLAN-evacuate-python-from-UXLC-utils.md``),
and every path composed off the wrong one then resolves silently into the wrong
tree.  So the two are named apart *before* the move, while the 216 tracked
artifacts here are still the oracle that can prove a path change harmless:

  * the CODE root is ``mb_cmn.paths.repo_root()`` -- what ``py/`` is under, what
    ``repo_hygiene`` scans, what ``git`` and ``gh`` act on;
  * the DATA root is ``uxlc_data_root()`` below -- ``in/``, ``out/``,
    ``gh-pages/``, ``data/`` and the gitignored ``.novc/``.

Before the move ``uxlc_data_root()`` is this repo; after it, the one line below
becomes ``paths.require_sibling("UXLC-utils", paths.sibling_repo("UXLC-utils"))``
and nothing else changes.  That is the entire retarget, and it is one line because
no other module composes a data path off anything but this one.

What this replaces is cwd-relative string literals -- ``"in/UXLC-39"``,
``"gh-pages/clc"``, ``"out/UXLC-misc/all_changes.json"`` -- which resolve
correctly only while the process runs from this repo's root.  Two test modules
were already working around that, one of them by ``os.chdir``-ing to the repo root
before calling the library.

``mb_cmn.paths`` (vendored from MAM-basics) owns sibling-repo resolution and its
``REPO_<NAME>_DIR`` / ``REPOS_ROOT`` override chain; this module delegates rather
than keeping a second copy of it.  ``mb_cmn/paths.py`` was added to this repo's
vendored subset for that purpose; ``main_update_vendored_files.py`` copies by
intersection with what is already present in ``py/mb_cmn/``, so it stays.
"""

from __future__ import annotations

from pathlib import Path

from mb_cmn import paths


def uxlc_data_root() -> Path:
    """Path to the UXLC-utils corpus this code reads and writes.

    The one line that changes when the Python moves out -- see the module docstring.
    """
    return paths.repo_root()


def in_dir() -> Path:
    """Committed inputs: downloads from tanach.us plus hand-curated files."""
    return uxlc_data_root() / "in"


def out_dir() -> Path:
    """Generated-output tree, 27 tracked files."""
    return uxlc_data_root() / "out"


def gh_pages_dir() -> Path:
    """Published-HTML tree, 184 tracked files, served at bdenckla.github.io/UXLC-utils."""
    return uxlc_data_root() / "gh-pages"


def data_dir() -> Path:
    """Generated data other repos consume (``lci_augrecs.json``, ``lci_recs.json``).

    Generated, despite the name: ``main_write_page_break_info`` writes one file here
    and copies the other in from ``in/UXLC-misc/``.  Both are tracked, so both are
    part of the oracle.
    """
    return uxlc_data_root() / "data"


def novc_dir() -> Path:
    """Gitignored scratch tree (``<uxlc_data_root>/.novc``).

    Named for the ``.gitignore`` entry rather than for what it holds, because what it
    holds is deliberately unclassified: whatever a run wants to write and nobody wants
    to commit.
    """
    return uxlc_data_root() / ".novc"


def uxlc_39_dir() -> Path:
    """The canonical UXLC core XML, one file per book39 (``in/UXLC-39``)."""
    return in_dir() / "UXLC-39"


def uxlc_rest_dir() -> Path:
    """The non-book39 members of the tanach.us Tanach.xml zip (``in/UXLC-rest``)."""
    return in_dir() / "UXLC-rest"


def uxlc_misc_dir() -> Path:
    """The UXLC change logs and the hand-curated CSV/JSON beside them (``in/UXLC-misc``)."""
    return in_dir() / "UXLC-misc"


def uxlc_misc_fixed_dir() -> Path:
    """Hand-corrected overrides that shadow ``in/UXLC-misc`` (see ``uxlc_misc_path.get``)."""
    return in_dir() / "UXLC-misc-fixed"


def uxlc_notes_dir() -> Path:
    """The downloaded tanach.us note pages (``in/UXLC-notes``), one HTML per (atom, code)."""
    return in_dir() / "UXLC-notes"


def out_uxlc_misc_dir() -> Path:
    """Change-log derivatives (``out/UXLC-misc``): all_changes.json and its neighbours."""
    return out_dir() / "UXLC-misc"


def clc_pages_dir() -> Path:
    """The CLC edition's published pages (``gh-pages/clc``)."""
    return gh_pages_dir() / "clc"


def fois_pages_dir() -> Path:
    """The features-of-interest catalog's published pages (``gh-pages/fois``)."""
    return gh_pages_dir() / "fois"


def amb_early_mtg_pages_dir() -> Path:
    """The ambiguous-early-meteg survey's published pages (``gh-pages/amb-early-mtg``)."""
    return gh_pages_dir() / "amb-early-mtg"


def tanach_us_http_cache_dir() -> Path:
    """Where the polite downloader caches tanach.us responses (``.novc/http-cache/tanach-us``)."""
    return novc_dir() / "http-cache" / "tanach-us"


def sibling(name: str) -> Path:
    """``mb_cmn.paths.sibling_repo``, re-exported so call sites import one paths module."""
    return paths.sibling_repo(name)


def require_sibling(name: str, path: Path) -> Path:
    """``mb_cmn.paths.require_sibling`` -- see it for why a missing sibling is not a skip."""
    return paths.require_sibling(name, path)


def book_of_job_dir() -> Path:
    """The book-of-job clone, whose quirkrecs ``main_map_changes_to_book_of_job`` maps onto."""
    return sibling("book-of-job")


def require_book_of_job_dir() -> Path:
    """``book_of_job_dir``, checked -- see ``require_sibling`` for why this is not a skip."""
    return require_sibling("book-of-job", book_of_job_dir())
