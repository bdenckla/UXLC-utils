# CLC skeleton — narrow build plan (for a fresh session)

> **Purpose:** a small, self-contained plan to stand up the **CLC walking skeleton** in a fresh
> session, without re-reading the whole brainstorm. Background and rationale live in
> [doc/clc-brainstorm.md](clc-brainstorm.md); this file is just the build order. Keep it narrow —
> the point is one end-to-end vertical slice, not the whole edition.

## Definition of done (skeleton)

A driver `py/main_clc.py` that, for **one pilot book (or chapter)**, reads today's UXLC text and
writes a static page under **`gh-pages/clc/`** in MAM-style **3 columns** (reference | text | doc),
where the doc column shows **UXLC's own `<x>` notes** (start with `m`/`d`/`t`) **as always-links**,
each carrying the note's prose pulled from the change log. **No accent grammar, no charitable
resolution yet** — the skeleton proves the pipeline (read → CLC note schema → one renderer →
`gh-pages/clc/`). Charity layers on later.

## Locked decisions (do not re-litigate)

- **Home:** `py/clc/` (Python) + `gh-pages/clc/` (output). Existing repo modules are importable
  directly (not vendored) — see brainstorm §4.
- **Notes policy:** **always link** (uniform; no MAM short-inline / long-link threshold). §7.3.
- **Versification:** primary `vtrad-BHS`. §7.8. (No MAM-boundary coloring in the skeleton.)
- **First note source:** UXLC `<x>` notes, leading with the under-bar-ambiguity codes
  **`m` (prose merkha/meteg/tipeḥa)** and **`d` (poetic deḥi/tarḥa/…)**, plus catch-all `t`. §2, §5.
- **Note schema is defined from requirements (§8), NOT from the `amb_early_mtg` record.**

## Reusable assets (verified on disk)

| need | use |
|---|---|
| read UXLC text | `uxlc_misc/my_uxlc.read(book_id)` → chapters→verses→words; or `my_uxlc.read_all_books(handlers)`. Examples: [py/main_uxlc_word_list.py](../py/main_uxlc_word_list.py), [py/main_fois.py](../py/main_fois.py) |
| extract `<x>` note codes per atom | the FOIs reader pattern — [`_handle_wc_x`](../py/main_fois.py#L54-L59) builds `atom[2]["types"]` |
| note **prose** (the apparatus text) | the `<correction><description>` that added the note, ingested by [py/uxlc_changes/](../py/uxlc_changes/); raw in each `in/UXLC-39/*.xml` header + dated `in/UXLC-misc/* - Changes.xml`. **Join to the noted atom by citation `ch:v.atom`.** |
| book ids / order / cant-system | `mb_cmn.mb_cmn_bib_locales` (`ALL_BOOK_IDS`), `mb_cmn.cantsys` (prose/poetic), `_is_prose_section_of_job` |
| JSON / file output | `mb_cmn.file_io.json_dump_to_file_path` |
| 3-column presentation model | MAM-with-doc: `MAM-basics/py/mwd/mwd_write_book.py`, `mam_doc_utils.mark_doc_targets`, `mwd_utils.html_for_ver_ndd` (brainstorm §5). Output examples in `MAM-with-doc/gh-pages/*.html` |
| fonts / css | reuse `gh-pages/woff2/Taamey_D.woff2` + `gh-pages/style.css`; borrow `mam-doc-*` CSS or define `clc-doc-*` |

## Build order

1. **`py/clc/` package + `py/main_clc.py` driver** that reads one pilot book and writes
   `gh-pages/clc/<book>.html`. Get an empty 3-column page rendering first.
2. **CLC note schema** (one dict/dataclass): `book, ch, v, atom, word, note_code, note_text,
   source, diff_type, is_uxlc_departure, uxlc_reading, clc_reading`. Plain data (JSON-serializable)
   so the same records can later feed the §7.9 difference index. (Schema fields per brainstorm §8.)
3. **Note source = `<x>` notes joined to change-log prose.** Collect per-atom `<x>` codes; for each,
   look up the `<correction><description>` by citation to fill `note_text`. Emit CLC notes for the
   pilot, **`m`/`d`/`t` first**. (Skeleton: `is_uxlc_departure=False`, `diff_type='under-bar'`,
   `clc_reading` = UXLC reading — we are only *surfacing* the ambiguity, not yet resolving it.)
4. **Always-link 3-column renderer.** Text column = running verse text; each noted word links to its
   note (anchor / per-note entry). Reference column = book ch:v(.atom).
5. **Pilot scope:** pick a slice that contains at least one `m` and one `d` note so both under-bar
   paths render (e.g. a Psalms chapter for `d` + a Torah chapter for `m`); a whole short book is also
   fine. Leave exact choice to the session.

## Explicitly OUT of scope for the skeleton (later phases)

Accent-grammar integration & actual charitable resolution (§2a/§3/§9 #1); the `q`-dagesh restoration
(§7.15); bracket notes (§7.2); change-records-as-notes beyond the join above (§7.4); FOIs as notes
(§7.5); images / Sefaria links (§7.6); detangled Decalogues (§7.7); MAM-boundary versification color
(§7.8); the differences-from-UXLC index (§7.9); the intro essay (§7.10); BHL Appendix A (§7.11);
meteg-position normalization (§7.13); control-char stripping (§7.14). Each is "a new note source
feeding the one renderer" once the skeleton exists.

## Still-open inputs the session may need to decide

- Exact pilot book/chapter.
- Whether doc links target per-note anchors on a single big-doc page (MAM-style) or a notes page.
- Final schema field names.
