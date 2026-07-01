# CLC dual-cantillation derivation tools

Dev scripts that derive and verify the hand-built `_ORACLE` in
`py/clc/clc_dual_cant.py` (the Decalogue / Genesis 35:22 dual-cantillation split).
Promoted out of the gitignored `.novc/` scratch dir so the only copy is
version-controlled. Status / backlog for the dual-cant work: **GitHub issue #20**.

## Running

Run from the repo root, e.g.:

    python tools/gen_entry.py

Each script adds `<repo>/py` to `sys.path` and resolves the repo root as the parent
of this `tools/` dir, so the scripts must stay exactly one level below the repo root.
Regenerable inputs/outputs live in the gitignored `.novc/` (e.g.
`.novc/mam_strands.json`, `.novc/entries.txt`), not here.

## Sibling-repo dependencies

These consult two sibling repos on disk under `C:\Users\BenDe\GitRepos`:

- **wlc-utils** — the MAM-simple loader and the detangler's `_dual_cant.json`.
- **MAM-basics** — the MAM-simple data (`json-vtrad-bhs`).

## Scripts

- `dump_mam_strands.py` → `.novc/mam_strands.json` — MAM cant-alef/bet/combined strands (the oracle signal). **Run this first**; the others read it.
- `gen_entry.py` → `.novc/entries.txt` — derives + **self-verifies** `_ORACLE` entries and writes the ENCODE/DEFER partition + per-atom diagnostics. The crown jewel.
- `derive_oracle.py` → `.novc/oracle_report.txt` — per-atom divergence report (which marks each strand keeps); flags the count-mismatch verses.
- `inspect_dualcant.py` — dumps the wlc-utils detangler's supplied / division / anomaly inventory.
- `inspect_rafe_dagesh.py` → `.novc/rafe_dagesh.txt` — byte-level rafe/dagesh dump + the driving previous-word accent.
- `inspect_supplied_accent.py` → `.novc/supplied_accent.txt` — the 3-source byte diff that adjudicated the dt 5:6/13/17 omitted accents.
- `inspect_wlc_vs_uxlc.py` → `.novc/wlc_vs_uxlc.txt` — proves UXLC ≠ WLC at dt 5:13/17 (explains the detangler "discrepancy").
- `inspect_dt517_xml.py` → `.novc/dt517_xml.txt` — dt 5:17 XML inspection.

## Note-page verification (issue #24)

Unrelated to the dual-cant oracle above — a standalone cross-check for the
committed tanach.us note pages:

- `verify_notes_zip.py` → `.novc/notes_zip_verify.txt` — confirms each committed
  `in/UXLC-notes/<book>/*.html` against the frozen `Notes.zip` snapshot. Classifies
  every page as byte-`IDENTICAL`, `PROSE-EQUAL` (differs only in tanach.us template
  chrome; the prose CLC extracts is identical), or `PROSE-DIFFERS`, and dumps the
  prose for any mismatch. Read-only; the zip path defaults to the frozen snapshot
  and can be overridden with an argument.
