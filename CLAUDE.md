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
  refresh `in/` from tanach.us. **Neither can run as of 2026-08-03**: that site's `robots.txt`
  now disallows both `/Books/Tanach.xml.zip` and `/Notes/`, and the downloader obeys it. They
  raise `RobotsDisallowedError` rather than fetching. Do not work around it. **Re-tested
  2026-08-12, still blocked** — Chris Kimball had written that he would restore the old
  `robots.txt`, but the live file is byte-identical to the version that broke the downloads
  (`Last-Modified: Sun, 02 Aug 2026 10:51:46 GMT`), and both programs still raise. Kimball's
  reply named `hcanat.us`, which turns out to be a real host on tanach.us' own address, serving
  `/Books/` and its own separate `robots.txt` — and both programs raise there too, run with the
  `--host` argument they grew for the test (MAM-basics `58171b2`). All six URLs the two programs
  fetch, across both hosts, were run live. The evidence is in
  `.novc/robots-retest-2026-08-12.md`, beside the outgoing `.novc/email-to-chris-kimball.md` that
  Kimball was answering and the reply drafted from it, `.novc/email-to-chris-kimball-2.md`.

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
