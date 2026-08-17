# CLAUDE.md

## This repo contains no Python. Its generators live in `../MAM-basics/py/`

UXLC-utils is data and documentation: `in/`, `out/`, `gh-pages/`, `data/`, `doc/`. Everything
under `out/`, `gh-pages/` and `data/` is generated, and **every generator lives in the sibling
repo `../MAM-basics`**, which writes back into this one. All 102 tracked `.py` files, plus
`tools/`, `.vscode/` and `.github/copilot-instructions.md`, left this repo on 2026-08-03; do not
add one back, and do not go looking here for the code that produced a file you are reading. Run
everything below from `C:\Users\BenDe\GitRepos\MAM-basics`, with that repo's own interpreter —
this repo's `requirements.txt` went with the code, and whatever `.venv` is left here has nothing
to run.

Most of it regenerates in one command:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe C:\Users\BenDe\GitRepos\MAM-basics\py\main_uxlc_mega.py
```

That is this repo's own pipeline, and **not** MAM-basics' `py/main_0_mega.py`, which is the
tree-wide one and writes nothing here. It was `py/main_0_mega.py` in this repo until the move;
the rename is what keeps the two apart. Its five steps run in this order, and each is also
runnable on its own:

- `main_uxlc_check_changes.py` — `out/UXLC-misc/`, the change-log derivatives
  (`all_changes.json`, `sanity_problems.json` and their neighbours).
- `main_fois.py` — `gh-pages/fois/`, the features-of-interest catalog and its HTML view.
- `main_write_page_break_info.py` — `data/lci_augrecs.json`, and copies
  `in/UXLC-misc/lci_recs.json` to `data/lci_recs.json`. Both are generated, despite living under
  a directory named `data`.
- `main_amb_early_mtg.py` — `gh-pages/amb-early-mtg/`, the ambiguous-early-meteg survey.
- `main_uxlc_word_list.py` — `out/uxlc-words.json` and `out/uxlc-words-fragile.json`.

Three more entry points write here and are **outside** the mega, so nothing rewrites their output
routinely:

- `main_clc.py` — `gh-pages/clc/`, the CLC edition's pages. Run it after the mega; the
  regeneration is not complete without it.
- `main_map_changes_to_book_of_job.py` — `in/UXLC-misc/2026.04.01-map-to-book-of-job.json`. The
  one tracked file under `in/` that a program writes, and it reads the sibling `../book-of-job`'s
  `out/enriched-quirkrecs.json` and `gh-pages/jobn-details/` to do it.
- `main_uxlc_download_changes.py` and `main_clc_download_notes.py` — the two downloaders, which
  refresh `in/`. **They fetch from `hcanat.us`, not from tanach.us, as of 2026-08-12**, and they
  do it by default: `MAM-basics/py/uxlc_misc/my_uxlc.py` now declares `UXLC_DOWNLOAD_HOST`
  ("hcanat.us") beside `UXLC_HOST` ("tanach.us"), and `--host` is only for reaching a third host.
  Read `UXLC_DOWNLOAD_HOST`'s docstring before running either program.

  **`UXLC_HOST` and `UXLC_DOWNLOAD_HOST` name two different hosts and are not interchangeable.**
  `UXLC_HOST` is where UXLC is *published*, and it is the host every URL on a rendered page names,
  whichever host a run fetched from; `UXLC_DOWNLOAD_HOST` is where the bytes come from. One
  constant did both jobs until 2026-08-12, when the two stopped being the same string.

  **tanach.us is blocked, on purpose, and is expected to stay that way.** Its `robots.txt` has
  disallowed every path for every user agent since 2026-08-02, and `mb_cmn.polite_download` obeys
  it, so a fetch from tanach.us raises `RobotsDisallowedError` before making a request. Do not
  work around it. Chris Kimball opened hcanat.us rather than reopening tanach.us; Ben's decision,
  2026-08-12, was to take that as the answer.

  **`main_clc_download_notes` will mix two note-page templates** under `in/UXLC-notes/`, because
  hcanat.us builds those pages from a newer one than the 477 committed here. Nobody has decided to
  accept that. hcanat.us' `/Books/` and `/Changes/` raise no such question — they came back
  byte-identical to what is tracked.

  A `--host` run naming any host other than `UXLC_DOWNLOAD_HOST` downloads without rebuilding, so
  a third host's bytes cannot reach the tracked outputs silently. A default run **does** rebuild.

  The evidence for all of this — the robots.txt texts, the file-by-file comparison, the four ways
  the note templates differ — is `.novc/robots-retest-2026-08-12.md`, whose §6 its own §9 corrects,
  so read §9 first. The correspondence with Kimball is beside it, `.novc/email-to-chris-kimball.md`
  and `-2`, `-3`.

Two more read from here without writing: `main_verify_notes_zip.py`, which checks the committed
`in/UXLC-notes/` pages against a `Notes.zip` snapshot in `~/Downloads`, and
`main_uxlc_estimate_atom_loc.py`, an ad-hoc "where on the page is this atom" query.

**Not everything under the generated trees is generated at all.** 87 of the 214 tracked artifacts
here are untouched by a full run, measured by mtime on 2026-08-03: 81 images under
`gh-pages/amb-early-mtg/img/`, 2 under `gh-pages/img/`, `gh-pages/index.html`,
`gh-pages/style.css`, `gh-pages/woff2/Taamey_D.woff2`, and `out/UXLC-misc/map-changes-to-book-of-job.md`
— that last a hand-authored prose report that happens to sit under a generated tree. Deleting any
of the 87 in the belief that a rebuild brings it back will lose it.

`.novc/` stays here — it is this repo's gitignored scratch directory, and the tanach.us HTTP cache
and the downloaded `Tanach.xml.zip` still write into it (`uxlc_paths.novc_dir`,
`uxlc_paths.tanach_us_http_cache_dir`).

**Every `py/...` path in `doc/` now means `../MAM-basics/py/...`.** `doc/clc-design.md` links to 19
distinct such paths and `doc/clc-skeleton-plan.md` cites more; none was rewritten, because they are
accurate about which module does what and only wrong about which repo it is in. Read them with
that substitution. The one exception is `py/mb_cmn/mb_cmn_bib_locales.py`, cited in
`doc/clc-design.md` §"Vendored common code": it did not move, because it was never a vendored copy
— it was MAM-basics' `bib_locales.py` plus six local aliases, and its callers now use
`mb_cmn.bib_locales` directly.

**Every `wlc-utils/...` path in `doc/` now means `../MAM-basics/...` as well.** The rest of that
repo — data, pages, `doc/` — was evacuated into MAM-basics too (copied 2026-08-12, wlc-utils
emptied to a redirect host 2026-08-17; `MAM-basics/doc/PLAN-evacuate-the-rest-of-wlc-utils.md`).
The one exception is `wlc-utils/data/lci_recs.json`, cited in `doc/clc-design.md` §6: the move
also **renamed** it, so it is `../MAM-basics/in/lci_recs.json` now.

## This repo's issues stay here; new ones are filed in MAM-basics

The issues were **not** transferred when the Python left. They keep their numbers and stay in
`bdenckla/UXLC-utils`, and this is still where they are read, commented on and closed. So **a bare
`#NN` in this repo's `doc/` and in this file still means a UXLC-utils issue**; none was
requalified, because qualifying them would imply they had been ambiguous.

New issues, including new work on the generators now in `../MAM-basics/py/`, are filed in
**MAM-basics**. There a bare `#NN` means a MAM-basics issue, and the moved code cites this repo's
as `UXLC-utils#NN`.

## Reading MAM data — the parsed form, never the raw source

Stated here because `doc/clc-design.md` assumes it: CLC draws on MAM from `../MAM-parsed`,
preferably the `/plus` variety, using `mb_diff_mpu`'s readers — never by regex over the raw
wikisource source, which would reinvent the template parser MAM-parsed already ran. It is not
repeated in `../MAM-basics/CLAUDE.md`, because it is already that repo's own practice:
`mb_cmn/read_books_from_mam_parsed_plus.py` is how thirteen modules there read MAM, and
`mb_diff_mpu` is native code there rather than a vendored copy.

## `doc/clc-design.md` is the CLC design document and stays here

It is about the edition — its versification, its note sources, its rendering decisions — not about
the code, which is why it did not move. `doc/clc-skeleton-plan.md` likewise.
