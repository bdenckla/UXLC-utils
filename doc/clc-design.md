# Charitable Leningrad Codex (CLC) — Design

> **Living design doc for CLC.** Editorial principles, the feature set (at varying maturity — see the
> §11 status table), decisions already made, and the open questions that remain — for a new
> diplomatic edition of the Leningrad Codex (LC), kin to UXLC. Not an exhaustive spec, and not every
> future item is captured. **[TBD]** flags open questions inline; §9 consolidates them; the companion
> build plan is [doc/clc-skeleton-plan.md](clc-skeleton-plan.md).

---

## 1. The thesis: "charity"

**Name:** Charitable Leningrad Codex — **CLC**.

The defining feature relative to UXLC: **where UXLC has an *uncharitable* transcription,
CLC gives the *naqdan* (pointing-scribe) the benefit of the doubt.** All things being equal
(or even slightly unequal), CLC prefers the **"least weird"** reading — the one that makes the
naqdan look like he knew what he was doing, rather than the one that makes him look like he
blundered.

This is not "correcting" the LC and it is not "fixing" it to match a grammar. It is a
transcription stance: when the image is ambiguous, decide the ambiguity in the direction that
is internally coherent. UXLC, by contrast, often resolves the same ambiguities mechanically
(e.g. by *mark angle*), which can manufacture weirdness that the scribe probably never intended.

> Working tension to keep honest: charity must not become silent emendation. Every charitable
> choice that departs from UXLC should be **recorded as a note** (see §7.3–7.5) so the reader
> can see what we did and why. "Charitable but transparent." Two features carry the transparency
> half: an **introductory essay** that *argues* the principle (§7.10), and a
> **differences-from-UXLC index** that *shows the receipts* (§7.9).

---

## 2. The core ambiguity: the vertical under-bar

The richest vein of charity is the **vertical (or near-vertical) bar written below a letter.**
The same-ish glyph can be any of:

- a **meteg** / gaʿya (metrical secondary stress; not an accent),
- a **tipeḥa** (accent; *prose only*),
- a **tarḥa** (accent; *poetic only*),
- a **merkha** (accent; occurs in *both* prose and poetic systems),
- a **yored** (accent; *poetic only*),
- a **silluq** (accent; verse-final) — the easiest of these to distinguish, by context (it falls on the last word of the verse, before *sof pasuq*).

**UXLC already flags many of these against itself.** Its one-letter `<x>` notes mark exactly this
ambiguity in-text: **`m`** ("possible *merkha* rather than *meteg*", 42×, prose), **`d`** ("*deḥi*
re-read as *tipeḥa/tarḥa*", 29×, poetic only), plus the catch-all **`t`** (among 233×, e.g. "examine
mark below … as possible merkha"). That is **~70+ scribal under-bars UXLC itself is unsure about** —
the natural in-text seed for CLC's charitable resolution (see §3, §5, §7.1). Tellingly, UXLC's own
change log resolves them *by stroke angle* — *"the meteg … might be a merkha, but is not sufficiently
inclined"* — which is precisely the method §2a proposes to replace with accent grammar.

Two **distinct** sub-problems live under this heading. Keep them separate:

### 2a. Identity ambiguity — *which mark is it?*
A bar below the letter could be meteg vs. tipeḥa/tarḥa vs. merkha vs. yored. UXLC leans on the
**angle/position** of the stroke in the image to decide. CLC's stance: **resolve primarily by
context — i.e. by accent grammar — not by mark angle.** If the accentuation of the verse makes
only one of these grammatically possible (or overwhelmingly likely), transcribe *that*, even if
the scribe's stroke is drawn at a slightly "wrong" angle.

→ This is the genuinely *new* CLC work. It leans directly on an **accent-grammar engine that
already exists** in the sibling repo `wlc-utils` (see §5).

**CLC resolves more charitably than UXLC's own binary framing.** The candidate set is *every*
under-bar mark the relevant system licenses, not just the two UXLC happened to name in a note:
- an **`m`** case (prose) ranges over **{meteg, merkha, tipeḥa}** — not only UXLC's meteg/merkha.
  (UXLC's change log already re-encodes both *merkha→meteg* and *tipeḥa→meteg* under the same `m`
  note, so all three are empirically in play.)
- a **`d`** case (poetic) ranges over **{tarḥa, deḥi, meteg, merkha, yored}** — never *tipeḥa*
  (not a poetic accent, though moot at the codepoint level — see next).
- **Codepoint collisions matter for the output.** These grammatical identities are not all distinct
  in Unicode: *tipeḥa = tarḥa =* **U+0596** and *merkha = yored =* **U+05A5**. So a charitable
  re-reading can change a mark's *identity* without changing its codepoint — meaning some
  CLC-vs-UXLC departures live only in the **note prose / labeling** (the §8 "UXLC reading vs CLC
  reading" pair, §7.9 diff), not in the text bytes.

### 2b. Ownership ambiguity — *is a coded "early meteg" really just a normal meteg?* (minor footnote)
A much smaller, rarer issue than 2a. UXLC sometimes codes a meteg on a ḥaṭef-bearing
letter as an **early meteg** via a ZWJ trick (`meteg + U+034F` → the `ֽ͏ַ` sequence). In a **confirmed one or two cases**,
the better reading is simply a **normal meteg on the previous letter**. An old, **likely-unfinished**
exploratory program (`amb_early_mtg`) once scanned for other such candidates.

→ This is a **minor footnote, not a pillar.** CLC mostly **dissolves** the question by *not encoding
meteg position at all* (§7.13); what little remains of `amb_early_mtg` is just one "candidate UXLC
issues" lead among several in §7.12 — **not** the prototype of the note schema or of anything else.

> So: **CLC's charity is, first and foremost, (2a) under-bar identity resolved by accent grammar,
> seeded by UXLC's own ~70+ `m`/`d`/`t` self-doubts (§2 intro), applied wherever the image is
> genuinely ambiguous.** The early-meteg question (2b) is a minor footnote, largely dissolved by §7.13.

---

## 3. How accent grammar resolves identity (2a)

The plan-shaped idea (kept deliberately brief):

1. For each word/verse, compute the **expected accentuation** under the relevant system
   (the 21 prose books vs. the 3 poetic books — אמ״ת = Job, Proverbs, Psalms).
2. Where the LC image shows an ambiguous under-bar, ask the grammar: *which of
   {meteg, tipeḥa/tarḥa, merkha, yored} is licit / expected here?*
   (Start from UXLC's own `m`/`d`/`t` flags, §2. System-specific candidate sets: **prose →**
   {meteg, merkha, tipeḥa}; **poetic →** {meteg, merkha, tarḥa, deḥi, yored}.)
3. If exactly one is licit → transcribe it (charitable resolution).
4. If more than one is licit → use the grammar's **continuous grammaticality measure** to rank the legal options and
   provisionally go with the most likely; where they remain close, also weigh image evidence
   (angle, position). Either way, **record a note** disclosing the ambiguity — admitting our
   uncertainty to the interested reader rather than feigning certainty.
5. If the grammar says *none* of them is licit → that is a candidate **anomaly** (possible scribal
   error or possible transcription error upstream) — flag it, don't silently "fix" it.

This mirrors, almost exactly, the "supplied marks vs. anomalies" output of the
dual-cantillation detangler in `wlc-utils` (§5, §7.7): charitable supply where the grammar is
confident, explicit anomaly where it is not.

**[TBD]** Where does the accent-grammar engine live for CLC? Vendor `wlc-utils/py/accgram` in
the way `mb_cmn` is already vendored, or call it cross-repo? (See §5 vendoring notes.)

---

## 4. Scope / relationship to UXLC

- **Home (decided): CLC lives *in this repo*, not a separate one.** Python goes in **`py/clc/`**
  and the HTML/CSS/JS output goes in **`gh-pages/clc/`** — alongside the existing
  `gh-pages/amb-early-mtg/` and `gh-pages/fois/`. Consequence: the existing assets in §5 are
  **directly importable** (e.g. `import uxlc_amb_early_mtg…`, `uxlc_fois…`, `uxlc_changes…`,
  `uxlc_lci…`, `mb_cmn…`) rather than vendored. The only thing still arriving cross-repo is the
  accent-grammar engine from `wlc-utils` (see §9 #1).
- CLC stays **close to UXLC** — same base text, same book set, diplomatic intent. It is a
  *re-reading of the ambiguous marks* plus a *richer notes/presentation layer*, not a new
  collation from scratch.
- Versification: **primary = `vtrad-BHS`.** Optionally also surface **`vtrad-MAM`** where it
  differs (e.g. render the MAM verse boundary in a different color / as a secondary marker).
  **[TBD]** exact mechanism; `mb_cmn` book-locale utilities are the likely home for vtrad logic.

---

## 5. What already exists (inventory of reusable assets)

A pleasant surprise from exploring the repos: **most of CLC's plumbing already exists.** CLC is
largely an act of *composition* over existing machinery, plus the new identity-resolution work.

### In this repo (UXLC-utils)

- **UXLC's own `<x>` notes — the in-text charity seed (and most of the apparatus prose):**
  UXLC tags ambiguous/edited atoms with a one-letter note in an `<x>` element, already parsed by
  [`_handle_wc_x`](py/main_fois.py#L54-L59) into each atom's `types`. Corpus tally (39 books):

  | code | n | meaning | prose in change log |
  |---|---|---|---|
  | `t` | 233 | transcription uncertainty (damaged/indistinct; "examine as possible merkha") | 207 |
  | `c` | 103 | cantillation / word-division oddity | 90 |
  | `m` | 42 | **under-bar: possible merkha vs meteg (prose)** — §2a seed | 39 |
  | `y` | 36 | yatir ketiv | 36 |
  | `q` | 35 | qere fix (mostly "removed unsupported dagesh" — §7.15) | 35 |
  | `d` | 29 | **under-bar: deḥi↔tipeḥa/tarḥa (poetic)** — §2a seed | 28 |
  | `4`–`8`, `X` | 38 | rarer transcription codes | 0 |

  → **Note-text source (settled — see §7.3, §9 #2):** the rendered note prose is **the actual
  tanach.us note page** for each `(atom, code)` (e.g. `Notes/Proverbs/Proverbs.5.19.4-m.html`),
  downloaded by [py/main_clc_download_notes.py](py/main_clc_download_notes.py) into committed
  [in/UXLC-notes/](in/UXLC-notes/) and read **offline** at build time by
  [py/clc/clc_note_pages.py](py/clc/clc_note_pages.py) (the build never touches the network →
  deterministic). The change-log `<correction><description>` (e.g. *"Add note 'm' for possible merkha
  rather than meteg under the gimel"*), ingested by [py/uxlc_changes/](py/uxlc_changes/), is an
  *imperative instruction to the editor*, **not** the reader-facing note — so it is **no longer the
  prose source**; it survives only as the atom-letter **consistency guard** (the table's "prose in
  change log" column is now just that guard's coverage, joinable by citation `ch:v.atom`). An atom
  with no downloaded page — the **38 numeric/`X`** notes, or any not yet fetched — shows a fixed
  **per-code marker** ([`_fallback_text`](py/clc/clc_collect.py)), never the change-log text.

- **Ambiguous early meteg (`amb_early_mtg`) — a *minor*, likely-unfinished side-investigation:**
  [py/uxlc_amb_early_mtg/amb_early_mtg.py](py/uxlc_amb_early_mtg/amb_early_mtg.py) — a hand-curated
  catalog of words with an ambiguous early meteg. Each record carries a charitable judgment:
  - verdicts: *"Better transcribed as a normal meteg on the first letter"* (`_BETTER_1`),
    *"…on letter 2"* (`_BETTER_2`), *"Perhaps better…"* (`_PERHAPS_BETTER_1`), *"Unclear from the
    LC image alone"* (`_UNCLEAR`);
  - cross-references to **MAM** (with a status reason *and* a Wikisource diff URL), to **AC**
    (Aleppo), to **Sassoon 1053**, to **BHS**, and to existing **UXLC change proposals**;
  - image filenames per word (LC, and sometimes BHS/AC/Sassoon comparanda).
  - Driver [py/main_amb_early_mtg.py](py/main_amb_early_mtg.py) → emits HTML to
    `gh-pages/amb-early-mtg/` (`index.html`, `dubious.html`, `full-record/`, `img/`).
  - Supporting modules: `amb_early_mtg_full.py`, `amb_early_mtg_summary.py`, `*_extend.py`,
    `*_three_and_beyond.py`, `*_html_for_img.py`, `*_url_generator.py` (Sefaria image URL gen).
  - Seed list also lives as [Possible false early meteg marks.csv](Possible%20false%20early%20meteg%20marks.csv)
    and the matching `.code-search`.

  → It is **one harvesting lead among several** (§7.12), **not** a pillar and **not** the CLC note
  schema; §7.13's "don't encode meteg position" largely moots it. Its record shape (word, bcvp,
  verdict, comparanda images, cross-refs, links) is a *prior example* the §8 schema can borrow
  from — nothing more.

- **Features of interest (FOIs):** [py/main_fois.py](py/main_fois.py) +
  [py/uxlc_fois/](py/uxlc_fois/) — collects `kq` (ketiv/qere), `mark-grammar`, `mark-grammar-2`.
  Outputs JSON + HTML to `gh-pages/fois/`.

- **UXLC change records:** [py/uxlc_changes/](py/uxlc_changes/) (`uxlc_change_prep.py`,
  `uxlc_authors.py`, `uxlc_bhl_appendix_a.py`, `uxlc_change_sanity.py`, `uxlc_changes_loc.py`).
  The raw change data is the dated `* - Changes.xml` files in `in/UXLC-misc/` (2020 → 2026).
  Download/refresh via [py/main_uxlc_download_changes.py](py/main_uxlc_download_changes.py);
  check via [py/main_uxlc_check_changes.py](py/main_uxlc_check_changes.py).

- **Image / atom-location guessing:**
  [py/main_uxlc_estimate_atom_loc.py](py/main_uxlc_estimate_atom_loc.py) +
  `uxlc_misc/my_uxlc_location.py` (`page_and_guesses`) + [py/uxlc_lci/](py/uxlc_lci/). Given
  book/chapter/verse/atom, guesses the LC folio/column/line → which image to show.

- **Page-break info:** [py/main_write_page_break_info.py](py/main_write_page_break_info.py)
  (LC line/page boundaries; builds `data/lci_augrecs.json`).

- **Existing site scaffold:** `gh-pages/` already has `index.html`, `style.css`, and a Hebrew
  font `woff2/Taamey_D.woff2`.

- **Vendored common code:** `py/mb_cmn/` (from `MAM-basics`) including `mb_cmn_bib_locales`
  (book IDs/locales) and `he_wikisource_url.he_diff_url` (used to build MAM diff links).

### In sibling repos

- **`wlc-utils` — accent grammar + bracket notes + detangling (the heavy lifting for §2a, §7.2, §7.7):**
  - WLC 4.22 in kq-u form: `wlc-utils/out/wlc422-kq-u/` (`0header.json` + `1verses_*.json` per
    book group). **Bracket notes are embedded inline** in the Hebrew text strings as `]X` codes
    (e.g. `]1`, `]c`, `]Q`).
  - Bracket-note definitions: `wlc-utils/py/cmn/wlc_bracket_note_definitions.py` (~31 codes,
    multi-source: Manual 4.22, the legacy WTS supplement, Amos.xml notes).
  - Bracket-note parsing/HTML: `wlc-utils/py/accgram/rtmsr_bracket_notes.py`.
  - **Accent-grammar engine:** `wlc-utils/py/accgram/` — the prose/poetic grammar checker.
  - **Untangled Decalogues + Gen 35:22:** `wlc-utils/py/accgram/dual_cant_detangle.py`
    (passages `gn 35:22` pashut/midrashit, `ex 20:2-17` & `dt 5:6-21` taḥton/elyon). Uses
    MAM-simple as the oracle to split merged accents into two single-cantillation streams;
    produces parse trees + **4 charitably "supplied" marks** + **1 anomaly** (Deut 5:8 תעשה).
    Loader `wlc-utils/py/accgram/mam_simple_verse.py` (`vels_cant_alef` / `vels_cant_bet`).
  - Vendoring: `wlc-utils` itself vendors `mb_cmn` from `MAM-basics` and `in/UXLC-*` from this
    repo, refreshed by its `main_update_vendored_files.py`. So cross-repo vendoring is an
    established pattern here.

- **`MAM-with-doc` / `MAM-basics` — the notes presentation model (§7.3):**
  - 3-column layout: **reference | text | documentation.** No word-interrupting callouts; the
    text column stays readable.
  - **Short notes (≤ 400 chars)** render *inline* in the doc column, target word colored blue
    (`mam-doc-target-without-callout`), no marker.
  - **Long notes (> 400 chars)** get a red asterisk callout (`mam-doc-callout`) after the word +
    a link to a separate "big-doc" page with an anchor.
  - Threshold logic: `MAM-basics/py/py_misc/mwd_utils.py` `html_for_ver_ndd()`
    (`if not length_of_docs > 400`). Marking logic: `MAM-basics/py/py_misc/mam_doc_utils.py`
    `mark_doc_targets()`. Book writer: `MAM-basics/py/mwd/mwd_write_book.py`.
  - External links seen in MAM big-doc pages: NLI manuscripts, archive.org (Ginsburg), British
    Library, mgketer.org. (No Sefaria/Wikisource/tanach.us links in MAM's own output.)

---

## 6. Resolved: the `data/` dir vs. `codex-index-leningrad`

This doc originally asked: *is the LC-index info vendored here in `data/`, or is `data/` the source
and it's vendored into `codex-index-leningrad`?* Findings:

- **`data/` here is a built artifact local to UXLC-utils, not vendored from codex-index-leningrad.**
  - [data/lci_recs.json](data/lci_recs.json) is **copied** from `in/UXLC-misc/lci_recs.json` by
    [main_write_page_break_info.py:17](py/main_write_page_break_info.py#L17). Its header says
    `Derived-From: LCIndex` → `https://tanach.us/XSL/LCIndex.xml` → `USC-WSRP-Index`
    (USC West Semitic Research Project). So the *ultimate* source is tanach.us's LCIndex, not a
    local codex-index repo.
  - [data/lci_augrecs.json](data/lci_augrecs.json) is **generated** here by
    [main_write_page_break_info.py:16](py/main_write_page_break_info.py#L16) (augments each LCI
    record with word counts and start/stop line numbers).
- **The vendoring relationship with codex-index-leningrad runs the *other* direction.** Per
  [shared-with-codex-index-leningrad.md](shared-with-codex-index-leningrad.md) and
  `.github/copilot-instructions.md`: **UXLC-utils is canonical**, and
  `codex-index-leningrad/UXLC-utils-sparse/` is a *sparse vendored copy of this repo* (refreshed
  by that repo's `main_update_vendored_files.py`).
- **`codex-index-leningrad` is not currently checked out** as a sibling (only `codex-index-aleppo`
  is present in `GitRepos/`). The image-guessing machinery CLC needs (§5) **already lives here**.

**So, for "higher-accuracy image guesses based on info in codex-index-leningrad":** the *current*
guesser uses LCI data that already lives here (`data/` ← `in/UXLC-misc/lci_recs.json` ← tanach.us).
If codex-index-leningrad holds *richer* per-line/per-column index data than tanach.us's LCIndex,
that repo would need to be checked out and its index compared/merged. **[TBD]** — confirm what
codex-index-leningrad actually adds over the LCIndex once it's available locally. (Note the same
LCI data has also been vendored into `wlc-utils/data/lci_recs.json`.) Convenience: the
`UXLC-utils.code-workspace` file already lists `../codex-index-leningrad` as a second workspace
folder — but that path is **not cloned yet**, so it will show as missing until cloned.

---

## 7. Feature inventory

Each is a feature this doc names, organized with grounding + open questions.

### 7.1 Charitable under-bar transcription *(the headline feature)*
- Identity (2a) via accent grammar, **seeded by UXLC's own `m`/`d`/`t` notes** (§2, §5): start from
  the ~70+ atoms UXLC already flags, resolve each over its system's candidate set (prose
  {meteg, merkha, tipeḥa}; poetic {meteg, merkha, tarḥa, deḥi, yored}) by grammatical licitness,
  charitably overriding UXLC's angle-based call where the grammar is confident.
- Every departure from UXLC → a CLC note carrying a verdict + rationale (§8 schema). For the seeded
  cases the rationale text is partly **free** from UXLC's own change-log description (§5).
- **[TBD]** Source the grammar from `wlc-utils/py/accgram` (vendor vs. cross-call).
- **[TBD]** Define the verdict vocabulary precisely (extend `_BETTER_1`/`_UNCLEAR`/… to cover
  the identity cases: "grammar licenses only tipeḥa here," etc.).

### 7.2 Restoration of WLC bracket notes
- Source: the vendored `wlc-utils/out/wlc422-kq-u/` (kq-u WLC 4.22), with definitions from
  `wlc-utils/py/cmn/wlc_bracket_note_definitions.py`.
- **Caution:** apply a bracket note to a word **only after careful
  inspection** when that word **differs between UXLC and WLC** — the note may no longer apply.
  → Implies a per-word UXLC-vs-WLC diff gate before attaching a bracket note. **[TBD]** build/
  reuse that diff (wlc-utils already has 4.20-vs-4.22 diff tooling; a WLC-vs-UXLC diff may need
  to be added).

### 7.3 UXLC notes — MAM-style, no word-interrupting callouts
- Adopt the MAM-with-doc presentation: text column stays clean; notes live in a side column /
  apparatus. **Difference from MAM:** CLC wants notes to be **always links**, whereas
  MAM only links the *long* (> 400-char) notes and inlines the short ones. → CLC drops the
  length threshold and links uniformly. **Decided: always link** — uniform links, no MAM-style
  inline-short / link-long threshold.
- **Note text source — settled (once this doc's biggest unknown).** The `<x>` element carries
  only a one-letter *type* (cf. [`_handle_wc_x`](py/main_fois.py#L54-L59)); the rendered prose is the
  **actual tanach.us note page**, downloaded **offline** into committed [in/UXLC-notes/](in/UXLC-notes/)
  by [main_clc_download_notes](py/main_clc_download_notes.py) and read at build time by
  [clc_note_pages](py/clc/clc_note_pages.py). The change-log `<correction><description>` (ingested by
  [py/uxlc_changes/](py/uxlc_changes/)) turned out to be an editor-facing *instruction*, not the
  note, so it is **demoted to the atom-letter consistency guard only**; an atom with no page shows a
  fixed per-code marker (§5, §9 #2). The `wlc-utils` bracket-note definitions cover the separate
  bracket-note layer (§7.2).
- **Body placement is a *separate* axis from the link.** "Always link" (above) governs only the
  affordance on the word — every note links, uniformly, no threshold. It does **not** dictate where
  the note *body* renders. On *placement* CLC does keep MAM's length threshold (§5):
  - **Now (skeleton):** every body renders **inline in the doc column** of the same verse row
    ([`_note_block`](py/clc/clc_render.py#L197-L205)), regardless of length.
  - **Intended:** keep short notes inline, but **relegate long notes to a separate "big-doc" page,
    as in MAM-with-doc** (§5) — the always-link then points across to the anchored body on that page
    instead of into the same-row doc cell. So the uniform link stays; only the long body moves
    off-page. The stable anchor id (`clc-{ch}-{v}-{pos}`) makes this a render-time change only; the
    note JSON (§8) is unaffected.

### 7.4 UXLC change records as a kind of note
- We **have** the change text (the dated `* - Changes.xml` in `in/UXLC-misc/`, processed by
  `uxlc_changes/`). Present a change record as just another note type attached to its word.
- Cross-link to the existing change-proposal references already present in `amb_early_mtg`
  records (e.g. `"existing UXLC change proposal": ("2024.04.01", "2024.01.29-4")`).

### 7.5 FOIs as a kind of note
- Surface FOIs (`kq`, `mark-grammar`, `mark-grammar-2`, …) as notes, **especially the rarer
  ones**. Reuse [py/uxlc_fois/](py/uxlc_fois/).
- **[TBD]** rarity ranking / which FOIs are worth showing inline vs. on demand.
- **Done so far — ketiv/qere display.** The `kq` FOI is already surfaced — not (yet) as a side-note
  but as the **text-column rendering itself**: each k/q unit is a boxed `<ruby>` (qere on the
  baseline, ketiv above; small bracketed placeholders for the qere-without-ketiv / ketiv-without-qere
  cases), [py/clc/clc_kq.py](py/clc/clc_kq.py). The other FOIs (`mark-grammar`, …) are **not** surfaced yet.

### 7.6 Images
- **Sefaria + MAM links:** mirror UXLC's tanach.us presentation by linking each verse to its
  Sefaria LC image and to MAM-with-doc. (The `amb_early_mtg_url_generator.py` already builds
  Sefaria image URLs — reuse it.)
- **Higher-accuracy image guesses:** §6 — current guesser uses LCI data already here; revisit if
  codex-index-leningrad offers a finer index.
- **B&W → color upgrade:** the relatively few black-and-white images embedded in notes / change
  records should be upgraded to color. Likely **manual with automatic assistance** (batch-match a
  B&W crop to the color Sefaria scan, propose the color replacement, human confirms). **[TBD]**
  pipeline.
- **Scraping:** images for changes/notes may need to be **scraped** (source **[TBD]** — tanach.us
  change pages? Sefaria? NLI?). Respect source terms.

### 7.7 Untangled Decalogues + Genesis 35:22
- Build on `wlc-utils/py/accgram/dual_cant_detangle.py`: present Exod 20, Deut 5, and Gen 35:22
  as **two clean single-cantillation streams** each (taḥton/elyon; pashut/midrashit) instead of
  the merged tangle.
- The detangler's **"supplied marks" are themselves charitable acts** (marks the scribe didn't
  write because both strands share them) and its **anomalies** (e.g. Deut 5:8 תעשה) are exactly
  the kind of thing CLC should foot-note rather than hide. Strong fit with the CLC thesis — and CLC
  now does this itself for the narrow **maqaf/sof-pasuq** subset, supplying them **bracketed, green,
  and footnoted** rather than hidden (as raw UXLC) or silently baked in (as the detangler).

**Single-strand display.** Where a dual-cant verse is one row today, CLC shows **three**: the
combined form plus its two strands — labeled e.g. `35:22-C`, `35:22-א` (pashuṭ), `35:22-ב`
(midrashit), each ref label carrying a hover description, the three grouped as one verse block.
**Genesis 35:22 is the first application** (`py/clc/clc_dual_cant.py`, rendered by
`clc_render.py`); the Decalogues follow by adding their oracle entries.

**Near-subtractive split — a deliberate, *narrowed* departure from the detangler.** The accgram
detangler — a *grammar-checker* — is *charitable* about the strand *text*: it **supplies** omitted
accents (so each strand parses) and freely **changes word division**. CLC, a *diplomatic* edition,
is far more restrained: it shows UXLC's own marks, **supplies only punctuation**, and where a strand
wants an *accent* UXLC omitted it **notes** the gap rather than inventing one. So the displayed strand
text is **near-subtractive, with two narrowly-scoped, loudly-flagged charities, plus one annotation**:
- **Position-safe subtraction.** Each strand is UXLC's own combined word with only the *other*
  strand's **divergence cluster** resolved: an accent, the **word-division punctuation that tracks
  it** (a maqaf / sof-pasuq / legarmeh belonging to that strand — so a sof-pasuq is *suppressed*
  when its silluq is, and never sits on a word whose last accent is e.g. etnaḥta), and — where the
  two strands stack them on one letter — the other strand's **vowel** (a QUPO word's patax vs.
  qamats) or **rafe/dagesh**. For rafe/dagesh the policy is **faithful**: where the two strands
  harden/soften a בגדכפת letter (driven by the previous word's accent — a disjunctive pause hardens,
  a conjunctive juncture softens), the **hard** strand keeps UXLC's dagesh and the **soft** strand
  keeps UXLC's rafe; where UXLC has no rafe (e.g. ex 20:9 כל) the soft letter stays **bare** — no
  rafe is ever supplied. The cluster is replaced *by name at its exact site*
  (`str.replace(cluster, resolution, 1)`), so a mark that recurs elsewhere in the word as a *shared*
  mark is never touched.
- **Marked supply — *punctuation only*, bracketed and footnoted, never silent.** Only an
  accent-coupled **word-division** mark a strand needs but UXLC lacks may be **supplied**, and only
  to improve legibility (e.g. the sof-pasuq that breaks Gen 35:22's pashuṭ into its two chanted
  verses), rendered **bracketed and green** (CSS `clc-added-during-detangling`) with a synthesized
  "added out of thin air" note. The closed suppliable set is **maqaf / sof-pasuq / legarmeh** (the
  rule: *no punctuation supplied unless clearly marked as supplied* — cf. the green/bracketed
  additions in wlc-utils). Three sof-pasuqs are supplied so far — Gen 35:22 (pashuṭ) and the taḥton
  verse-ends of Exod 20:8 (לקדשו) and 20:9 (מלאכתך), where UXLC has none.
- **Omitted accent — *noted, never supplied*.** Where a strand's chanting calls for an **accent**
  UXLC left untangled (it has only the *other* strand's accent on that word), CLC does **not**
  invent one — the sharpened departure from the detangler, which *does* supply it to parse. CLC shows
  the word as UXLC has it (that accent simply absent) and emits a per-strand note: *"the elyon
  strand calls for a silluq on תרצח here, but UXLC's combined text carries only the taḥton strand's
  accent, and it is beyond the limits of CLC's charity to supply the missing silluq."* The Decalogue cases: **Deut 5:6** (elyon's tipḥa on אנכי + etnaḥta
  on אלהיך), **5:13** (taḥton's pashta on ימים), **5:17** (elyon's silluq on תרצח — UXLC has the
  sof-pasuq but not its silluq, so elyon shows a lone sof-pasuq). Still deferred: the QUPO vowel
  splits (ex 20:3, dt 5:7) and the maqaf word-division / count-mismatch verses (ex 20:4, 10; dt 5:8,
  12, 14, 15, 16).

No consonant is changed and no *shared* mark removed (a mark both strands keep stays in both); only
the divergent marks — accent and the punctuation tracking it — are subtracted (subtraction, incl. of
punctuation, is not re-division). MAM (via the detangler) is consulted **only as the oracle** — for
*which* of two stacked marks belongs to which strand, *where* a supplied break falls, and *which*
accent a strand wants where UXLC has only the other's. The detangler's remaining supplied-marks /
anomalies stay valuable as **logged footnotes**, never silent edits.

This is the same shape as the **legarmeh-vs-paseq** feature (§7.16): both *improve UXLC by importing
MAM's auxiliary adjudication* of an ambiguity that is **grammatical, not graphical**, differing only
in subject — which-accent-belongs-to-which-strand here, legarmeh-vs-paseq identity there. A
**supplied** punctuation mark emits a synthesized note (`source` `dual-cant-addition`, `diff_type`
`dual-cant-added-punct`); an **omitted** accent likewise emits one (`source`/`diff_type`
`dual-cant-omitted-accent` — see `py/clc/clc_note.py`): lightweight **per-strand** notes, **not** yet
ClcNotes / §7.9 index rows. The subtractive divergences remain **display-only** (no ClcNote departure
records yet).

### 7.8 Versification
- Primary `vtrad-BHS`; optionally show `vtrad-MAM` differences in a distinct color/marker (§4).

### 7.9 Differences-from-UXLC index *(sortable / filterable)* — *important*
A first-class **"what does CLC change vs. UXLC, and where"** index. This is the public face of
"charitable but transparent" (§1): it makes every departure auditable in one place. Mechanically
it is a **view over the CLC note schema** (§8) — every note that records a *departure* from UXLC
becomes one row.

Per-difference data (columns): location (book, ch:v, atom), the **UXLC reading vs. the CLC
reading**, the **difference type**, prose/poetic, and a link out to the full note + image.

**Filters:**
- **by biblical book.**
- **by prose vs. poetic — at the *verse* level, not book level**, because **Job mixes both.**
  Already solvable with existing code: [mb_cmn/cantsys.py](py/mb_cmn/cantsys.py) (prose/poetic
  system abstraction) + [`_is_prose_section_of_job`](py/mb_cmn/mb_cmn_bib_locales.py#L359), which
  encodes Job 1–2, 3:1, and 42:7–17 as **prose** and the rest of Job as poetic. So: a verse is
  poetic iff its book is Psalms/Proverbs/Job **and** it is not a Job prose section; the other 36
  books are all prose. (Function is currently `_`-private — promote/wrap it for CLC.)
- **by difference type** — `under-bar` is the headline type (§2); others **[TBD]**; keep a `misc`
  bucket so nothing is ever unclassified.

**Sorts:**
- **by difference type.**
- **by biblical order = LC *manuscript* order.** Because CLC is a **diplomatic** edition,
  **manuscript order wins** over printed/standard order wherever they differ. ⚠️ **Gap:** the code
  today encodes **standard printed order only** —
  [`ordered_short`](py/mb_cmn/mb_cmn_bib_locales.py#L343) (`'A1'`…`'FD'`) and
  [`get_bknu`](py/mb_cmn/mb_cmn_bib_locales.py#L63) (`1`…`39`, with 2 Chronicles **last**). L's
  manuscript order differs — e.g. **Chronicles heads the Writings**, and the Latter Prophets run
  **Jeremiah → Ezekiel → Isaiah**. So an **LC-manuscript-order key must be added** (see §9 #10).
  ("MAM book order" likely tracks the printed order too, which is exactly why manuscript order has
  to be its own thing here.)

**Implementation sketch:** one generated page under `gh-pages/clc/`, backed by a JSON array of
difference records, with **client-side JS** doing the sort/filter (this is the "JS" part of the
gh-pages/clc output). Keep the records as plain data so the *same* JSON drives both this index and
the per-verse note rendering.

### 7.10 Introductory prose — editorial principles & feature tour *(front matter)*
A human-facing **introduction** to the edition: an essay / landing page that lays out the
**editorial principles** and tours the features. The **chief principle is charity** (§1) — it gets
the most space and the clearest worked examples.

Characteristics:
- **Prose**, not just a feature list — explain *why* charity, and what "least weird" means in
  practice; state plainly that charity is bounded by transparency (every departure is logged).
- **Pointed Hebrew examples** inline (use the Taamey font already in `gh-pages/woff2/`), ideally
  the very cases already curated in `amb_early_mtg` (e.g. וַיַּעֲשׂוּ, בְּנֵי־), each shown as
  **UXLC reading vs. CLC reading** so the difference is concrete.
- **Images**: LC crops — and comparanda (AC, Sassoon 1053, BHS) — beside the examples, so the
  reader sees the ambiguous under-bar with their own eyes. Reuse the image assets/links from §7.6.
- Also introduce the rest: the no-word-interrupting-callout notes model (§7.3), bracket-note
  restoration (§7.2), change-records & FOIs as notes (§7.4–7.5), the detangled Decalogues + Gen
  35:22 (§7.7), versification (§7.8) — and link prominently to the differences-from-UXLC index
  (§7.9) as "see exactly what we changed."
- Lives as the **`gh-pages/clc/` landing page** (`index.html`) — the front door of the edition.

Pairs with §7.9: the intro **argues** charity; the index **shows the receipts**.

**Status: not started.** No `gh-pages/clc/index.html` exists yet. The only front-matter so far is a
short **per-book intro paragraph** at the top of each generated page
([`_intro_para`](py/clc/clc_render.py)) describing the skeleton — not the editorial-principles essay.

### 7.11 BHL agreement: body vs. Appendix A *(a correctness fix, not a preference)*
A reading that **agrees with the BHL body but is flagged in BHL Appendix A** should count as
**not agreeing with BHL as a whole.** Appendix A is part of BHL's verdict, not a separable
optional layer. The claim: **UXLC gets this wrong** — it presents agreement-with-body and
agreement-with-appendix as if they were the *same level* of agreement (or at least does not rank
them). CLC should model BHL agreement with that granularity:
- agrees with body **and** clean in Appendix A → genuine agreement with BHL;
- agrees with body **but** flagged in Appendix A → **not** agreement with BHL.

This is framed as a **correctness** issue, not editorial taste — worth its own difference-type /
note category in §7.9 / §8.

Grounding: the repo already ingests **BHL Appendix A, but for Psalms only** so far —
[uxlc_bhl_appendix_a.py](py/uxlc_changes/uxlc_bhl_appendix_a.py) reads
`in/UXLC-misc/BHL Appendix A Psalms.csv` (book ch:v plus optional word-index locales). Extending
Appendix A coverage beyond Psalms belongs to §7.12's long tail. **[TBD]** locate how UXLC encodes
its BHL agreement, so CLC can show the corrected judgment precisely.

### 7.12 Harvesting desirable changes from other editions
Sources to mine for changes CLC might want to adopt. Each yields **candidate** notes / charitable
diffs, **reviewed before adoption** (cf. the bracket-note caution in §7.2 — a suggestion is a
candidate, not an automatic change):
- **MAM ל= ("lamed equals", i.e. "L reads…") notes** — harvest from **`MAM-parsed/plus`** (or an
  edition that renders notes, e.g. `MAM-with-doc/gh-pages`). These ל= notes point precisely at
  what L actually has, i.e. often at exactly the changes CLC would like.
- **`book-of-job`** (sibling repo; self-contained, with its own `gh-pages` + many check scripts) —
  a **small, realistic, short-term** harvest set. Likely the first real harvesting target.
- **`amb_early_mtg`** (the early-meteg catalog, §2b/§5) — a small, **likely-unfinished** local scan
  for possible early-meteg mis-codings; a minor lead of the same flavor as the others here, mostly
  mooted by §7.13. Listed for completeness, not prioritized.
- **All of BHL Appendix A** (beyond the current Psalms-only slice, §7.11) **+ Da'at Miqra** — a
  comprehensive review would be ideal but is an explicit **long-term / "probably never get around
  to it"** goal. Don't block on it.

### 7.13 Don't encode early or medial meteg *(drop a BHS distinction now read as noise)*
CLC **does not encode early or medial meteg**: it places meteg in its default position and drops
the positional distinction. Faithfully preserving early/medial meteg placement is a **BHS feature
that some 50 years of scholarship has reframed as closer to a bug** — there is **no evidence the
placement is anything but scribal whim**, i.e. no evidence it means anything. So CLC treats meteg
position as non-significant rather than reproducing it.
- **Relationship to §2b:** declining to encode early/medial placement *largely dissolves* the 2b
  "which letter owns the early meteg?" question — meteg simply goes in its default position. 2b's
  value then shifts toward **evidence**: the candidates it surfaces are data points that the
  placement is whimsical, which is the very justification for this policy.
- Still a **logged departure** from UXLC (§1 transparency): each normalization → a note + a
  difference-index row (§7.9), difference type e.g. `meteg-position`.
- **[TBD]** pin down exactly how UXLC encodes early vs. medial meteg (the U+034F trick of §2b
  covers the early case; confirm the medial one) so every instance can be detected and normalized.

### 7.14 Remove questionable control-character use from UXLC
CLC **strips control characters UXLC uses for non-semantic reasons.** The clear case: a **joiner
used not to encode a meteg but to nudge most fonts into more felicitous spacing** — exploiting
quirky font handling for a purely cosmetic result. That is a presentation hack riding on undefined
behavior, not part of the text, so CLC removes it.
- Two distinct uses to keep separate: (a) a joiner that **encodes medial/early meteg** — a
  *legitimate* use of the joiner *if* you actually want medial meteg (but CLC drops medial meteg
  anyway, §7.13); and (b) the **spacing hack** — no textual meaning, remove. Both disappear in CLC,
  for different reasons.
- **Codepoint precision matters:** §2b's early-meteg trick is actually **U+034F (combining grapheme
  joiner)**, not a true ZWJ; the spacing hack may be an actual **ZWJ (U+200D)**. **[TBD]** audit
  UXLC for *every* control-character use and classify each as semantic (keep/transform) vs. cosmetic
  (drop); at least one spacing-hack joiner is known — find the rest.
- Log each removal as a departure (§7.9), difference type e.g. `control-char`.
- **Done so far — only the dual-cant case.** The strand splitter already drops an **orphaned CGJ**
  (U+034F) that the combined form used merely to *sequence* two stacked accents: once one accent is
  removed it has nothing left to sequence, so the strand omits it
  ([py/clc/clc_dual_cant.py](py/clc/clc_dual_cant.py), §7.7). The general control-character
  **audit/strip** across UXLC (the spacing-hack ZWJ, etc.) is **not started**.

### 7.15 Charitable restoration of "unsupported" dagesh (the `q` notes)
UXLC's **`q` notes** (35×) are almost all UXLC *removing* an **"unsupported" dagesh** from a qere
(or qere-without-ketiv) word — e.g. *"Remove unsupported dagesh in yod of qere word"*, *"… from bet
in qere-without-ketiv word"*. In the spirit of charity, CLC will **supply (restore) the dagesh** in
some or all of these — UXLC's removal is the *uncharitable* reading. **Manual review per case** (a
few `q` notes instead touch a maqaf, sheva, or yod, not a dagesh). Each restoration → a logged
departure (§7.9), difference type e.g. `dagesh`. The data is in hand: the `q` note marks the atom and
the change-log description names exactly what was removed (§5).

### 7.16 Legarmeh vs. paseq distinction *(borrow MAM's calls)*
A **second** ambiguous-vertical-bar problem, **distinct from the under-bar (§2)**: a vertical bar
standing **after / between words** can be either an ordinary **paseq** (a separating stroke — *not*
an accent) or the paseq that, together with a preceding conjunctive, forms the disjunctive
**legarmeh** (in the prose books, *munaḥ legarmeh* = *munaḥ* + paseq; the poetic system has its own
legarmeh forms over its own conjunctives — **[TBD]** pin down the poetic inventory). A word carrying
a genuine *munaḥ* that merely *happens* to be followed by an independent paseq looks **identical** to
*munaḥ legarmeh*; the difference is **grammatical, not graphical** — exactly the kind of ambiguity
CLC exists to resolve charitably.

**Goal: borrow MAM's legarmeh-vs-paseq distinctions.** MAM (Miqra according to the Masorah) already
adjudicates this throughout, so — as with the ל= harvest (§7.12), the strict strand split's MAM
oracle (§7.7), and the vtrad-MAM overlay (§7.8) — CLC takes **MAM's call as the charitable oracle**,
cross-checked by accent grammar where it's checkable. Same shape as the headline under-bar
resolution (§7.1, §3): grammar/oracle fixes the identity; every departure from UXLC is **logged**
(§7.9) with a verdict + rationale.
- **[TBD]** Does `wlc-utils/py/accgram` (§5) already distinguish legarmeh from paseq, or only the
  under-bar accents? If yes, reuse; if no, lean on MAM-as-oracle (cf. §7.7).
- **[TBD] Codepoint precision (cf. §2a).** There is **no dedicated "legarmeh" codepoint** — it is
  *munaḥ* (U+05A3) + *paseq* (U+05C0), the same bytes as *munaḥ* followed by an ordinary paseq. So,
  as with the §2a U+0596/U+05A5 collisions, a charitable re-reading may change only the **note prose
  / labeling**, not the text bytes. Confirm whether UXLC nonetheless distinguishes them somehow.
- Difference type for §7.9 / §8: **`legarmeh-paseq`**.

---

## 8. Presentation / tech notes
- Output is a static site under **`gh-pages/clc/`** (same pattern as `gh-pages/amb-early-mtg/`
  and `gh-pages/fois/`, and as MAM).
- Reuse the Taamey font (`gh-pages/woff2/Taamey_D.woff2`) + `style.css`.
- Borrow MAM's 3-column CSS vocabulary (`mam-doc-*`) or define a parallel `clc-doc-*` set.
- **Note-body placement (see §7.3):** short notes inline in the doc column, **long notes relegated
  to a separate "big-doc" page** (MAM-with-doc model, §5); the always-link points to wherever the
  body lives. The skeleton currently inlines *all* bodies — long-note off-loading is still to-do.
- Note schema: a single **CLC note** type that all sources (charitable under-bar verdicts, bracket
  notes, UXLC `<x>` notes + their tanach.us note-page prose, change records, FOIs, dagesh
  restorations) flow into — **one renderer, many sources**. Fields: atom text, bcvp, note text,
  source (e.g. `uxlc-x-note`, `dual-cant-addition`, `dual-cant-omitted-accent`), plus for the
  difference index (§7.9) a **`diff_type`** (`under-bar` | `dual-cant-added-punct` |
  `dual-cant-omitted-accent` | `legarmeh-paseq` | `dagesh` | `meteg-position` | `control-char` |
  `bhl-appendix` | … | `misc`), an **`is_uxlc_departure`** flag, and the **UXLC reading vs. CLC
  reading** pair. The difference index is then just "render the notes where `is_uxlc_departure`, as a
  table." (The `amb_early_mtg` record is one prior example to borrow field ideas from — not the
  definition.) **Implemented so far:** `ClcNote` (py/clc/clc_note.py) with sources `uxlc-x-note` and
  `dual-cant-addition` and diff types `under-bar` and `dual-cant-added-punct`. The dual-cant **"added
  out of thin air"** (supplied-punctuation) and **omitted-accent** notes (§7.7) are *separate,
  lightweight* per-strand dicts — **not** full `ClcNote`s (strand rows carry no anchors / §7.9 row yet).

---

## 9. Open questions (consolidated)
1. **Accent grammar integration:** with CLC living here (§4), the choice narrows to: **vendor
   `wlc-utils/py/accgram`** into this repo (the established `mb_cmn`-style pattern, via a
   `main_update_vendored_files.py`-type refresh) **vs. cross-call** it. Vendoring is the more
   likely fit. (The old "CLC as its own repo" option is now off the table — see §4.)
2. **UXLC note text source** (§7.3) — **settled** (§5): the rendered prose is the **tanach.us note
   page**, downloaded offline into committed `in/UXLC-notes/` (`main_clc_download_notes`) and read by
   `clc_note_pages`; the change-log `<correction><description>` is demoted to the atom-letter
   consistency guard only. Remaining gap: atoms with **no note page** (the **38 numeric/`X`** notes,
   or any not yet fetched) fall back to a fixed per-code marker; plus any tanach.us apparatus beyond
   the `<x>` notes.
3. **codex-index-leningrad** — clone it (the `.code-workspace` already references it as a 2nd
   folder, but it isn't on disk); then confirm whether it improves image guesses over the
   tanach.us LCIndex already vendored here (§6).
4. **Image scraping source & licensing** (§7.6).
5. **B&W → color** upgrade pipeline — how much can be automated (§7.6).
6. ~~**"Always link" vs. MAM's inline-short/link-long**~~ **Decided: always link** (§7.3).
7. **Verdict vocabulary** for identity (2a) ambiguities (§7.1).
8. **WLC-vs-UXLC per-word diff** to gate bracket-note application (§7.2).
9. ~~**Where does CLC live?**~~ **Decided:** in this repo — `py/clc/` + `gh-pages/clc/` (§4).
10. **LC manuscript book order** must be encoded for the difference-index sort (§7.9). The code
    only has standard printed order today. *(Verse-level prose/poetic, by contrast, is **already**
    available — `cantsys` + `_is_prose_section_of_job`; not an open question.)*

## 10. Rough ordering (not a plan — just gravity)
A loose sense of what unblocks what, without committing to phases:
- The **note schema + one renderer** is the spine — most features are "a new note source feeding
  one renderer." (Define it from §8's requirements, not from `amb_early_mtg`.)
- The **accent-grammar integration** is the long pole for the headline charitable feature (2a).
- The **UXLC-note-text source** is **no longer a long pole** — the real tanach.us note pages are
  downloaded offline into committed `in/UXLC-notes/` and read at build time (§5, §9 #2); atoms with
  no page fall back to a fixed per-code marker.
- Bracket notes, change records, FOIs, Sefaria/MAM links are comparatively cheap once the schema
  and renderer exist (the data largely exists already).
- Image color-upgrade and scraping are independent side quests.

---

## 11. Implementation status (as of 2026-06-29)

A snapshot of where the code (`py/clc/`, build driver `py/main_clc.py` + the separate offline
note-downloader `py/main_clc_download_notes.py`) stands against the §7 feature list. The **walking
skeleton (doc/clc-skeleton-plan.md) is complete and exceeded**; output exists for three pilot books
(Genesis, Proverbs, 2 Samuel) under `gh-pages/clc/`. Everything under the table is built but was
**not** named in §7.

| feature | status | where / note |
|---|---|---|
| §7.1 charitable under-bar | **seed only** | m/d/t notes *surfaced* (clc_collect); no accent grammar / resolution — `is_uxlc_departure` always False |
| §7.2 bracket-note restoration | not started | — |
| §7.3 MAM-style always-link notes | **done (skeleton form)** | 3-col `text \| ref \| doc` always-link renderer (clc_render); all bodies inline — long-note big-doc page still TODO |
| §7.4 change records as notes | not started | change log used only for the consistency guard, not as a note |
| §7.5 FOIs as notes | **partial** | ketiv/qere rendered as a boxed ruby (clc_kq); other FOIs not surfaced |
| §7.6 images / Sefaria links | not started | — |
| §7.7 dual-cant strands | **partial** | Gen 35:22 + most Decalogue verses done (clc_dual_cant `_ORACLE`: ex 20:2,5,6,8,9,13–15; dt 5:6,9,10,13,17,18,19) — pure-accent + sof-pasuq suppression, 3 supplied sof-pasuqs (Gen 35:22, ex 20:8/9), rafe/dagesh by the faithful policy, and omitted-accent notes (dt 5:6,13,17 — accents NOTED, never supplied: punctuation only). Deferred: QUPO vowel split (ex 20:3, dt 5:7), maqaf count-mismatch (ex 20:4,10; dt 5:8,12,14,15,16). No §7.9 departure rows |
| §7.8 versification | not started | primary vtrad-BHS implied; no MAM-boundary overlay |
| §7.9 differences-from-UXLC index | not started | needs `is_uxlc_departure` departures (none yet) + LC manuscript order (§9 #10) |
| §7.10 intro essay / landing page | not started | per-book `_intro_para` only; no `gh-pages/clc/index.html` |
| §7.11 BHL body vs. Appendix A | not started | Appendix A ingested for Psalms only (pre-CLC) |
| §7.12 harvesting other editions | not started | — |
| §7.13 drop early/medial meteg | not started | — |
| §7.14 strip cosmetic control chars | **partial** | orphaned CGJ dropped in the strand splitter only; no general audit |
| §7.15 restore "unsupported" dagesh (`q`) | not started | — |
| §7.16 legarmeh vs. paseq | not started | doc only |

**Ad-hoc / plumbing built (not in the §7 list):**
- **Offline note download/build split** — `main_clc_download_notes` fetches tanach.us note pages into
  committed `in/UXLC-notes/`; the build reads them locally and never hits the network (deterministic).
  Fixes the multi-word/numbered-book URL bug via `my_uxlc.book_basename` (e.g. `2Samuel` → `Samuel_2`).
- **`clc_collect.iter_noted_atoms`** — one source of truth for the noted `(atom, code)` pairs, shared
  by the build and the downloader so the two cannot drift.
- **Atom/change-log consistency guard** (`clc_collect._check_atom_consistency`,
  `_KNOWN_ATOM_MISMATCHES`) — fails loudly if atomization drifts from the recorded change positions.
- **Ketiv/qere boxed ruby** (clc_kq) and **smart-join of maqaf compounds** in running text (clc_render).
- **Column order `text | ref | doc`** with the ref as a narrow central spine (not the originally
  sketched `reference | text | doc`).
- **`clc-*` / `clc-added-*` CSS** vocabulary in `gh-pages/style.css`.
- **Unit tests:** `clc_dual_cant_test.py`, `clc_kq_test.py`.
