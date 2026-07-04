"""Harvest MAM's Decalogue doc-note markup for the CLC MAM-alignment features.

THROWAWAY SCAFFOLDING (issues #42-45): its only product is a .novc/ JSON that a human
reads to hand-encode the CLC oracle; it dies once the issues are encoded. But unlike
the first cut, it no longer reinvents the wikisource parser or hardcode a machine path.

Source is **MAM-parsed/plus** (the already-parsed structured JSON), NOT the raw
A-Torah.csv wikisource templates. In /plus each verse is [col_c, col_d, col_e] where
col_e is a sequence of strings and template objects ({"tmpl_name": ..,
"tmpl_params": ..}); a dual-cant verse wraps its combined text (which carries the
doc-notes) in {"tmpl_name": "מ:כפול", "tmpl_params": {"כפול": <seq>, "א": .., "ב": ..}}.
We read the JSON directly over the sibling-repo relative path (../MAM-parsed), so there
is no absolute path and no dependency on MAM-basics' non-public py_misc.

What maps onto which CLC feature:
  * legarmeh   template {"tmpl_name": "מ:לגרמיה-2"}            -> #42 (§7.16)
  * paseq      template {"tmpl_name": "מ:פסק"}                 -> #42 legarmeh-vs-paseq contrast
  * pisqah be'emtsa pasuq  any template param == "פסקא באמצע פסוק",
               strand-specific when it sits under מ:כפול's א/ב  -> #42 (§7.7)
  * two marks on one letter: /plus has NO dedicated template (the CSV's
    {{שני טעמים..}} / {{מ:טעם ומתג..}} were resolved into stacked Unicode); the
    structural tell is a CGJ (U+034F) in a נוסח lemma, e.g. מִתָּ֑͏ַ֜חַת / תִּֿרְצָ֖͏ֽח,
    with the marks named in the note body                     -> #44 QUPO + silluq/meteg (§7.7)
  * per-witness sof-pasuq: נוסח body "<sigla>=חסר סימן נקודותיים של סוף פסוק לטעם ה.."
                                                               -> #43 (§7.7)
  * plus every נוסח doc-note (lemma + flattened body) verbatim, the general harvest.

(The /plus format is documented — see MAM-parsed/README.md -> gh-pages/plus/html/
mpplus*.html. There is a SECOND doc-note type, מ:הערה-2 [targeted scroll-difference
notes], distinct from נוסח; it does NOT occur in the two Decalogues, so we don't
harvest it here. The README warns the /plus format is not yet stable.)

Verse refs are keyed to MAM's own (merged-elyon) numbering -- the /plus chapter/verse
keys ARE that numbering -- and to CLC/vtrad-BHS via tools/dump_mam_decalogue_versemap.py.

Run: python tools/dump_mam_decalogue_versemap.py   (first, to refresh the verse map)
     python tools/dump_mam_decalogue_docnotes.py
"""

import json
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent           # .../GitRepos/UXLC-utils
_GITREPOS = _REPO.parent                                 # .../GitRepos
_PARSED_PLUS = _GITREPOS / "MAM-parsed" / "plus"
_VERSEMAP = _REPO / ".novc" / "mam_decalogue_versemap.json"

# (short-ref, /plus filename, chapter-key) for the two Decalogue passages.
_PASSAGES = (("Ex", "A2-Exodus.json", "20"), ("Dt", "A5-Deuter.json", "5"))

_PISQAH = "פסקא באמצע פסוק"
_CGJ = chr(0x034F)  # COMBINING GRAPHEME JOINER -- MAM stacks two marks on one letter with it
_SOFPASUQ_RE = re.compile(
    r"([^=/]*?)=חסר סימן נקודותיים של סוף פסוק לטעם ה(תחתון|עליון)"
)


def _last_word(text_parts):
    toks = "".join(text_parts).split()
    return toks[-1] if toks else ""


def _flatten_note_body(body):
    """Join the string pieces of a נוסח '2' body (drop {{ש}} line-break templates)."""
    if isinstance(body, str):
        return body
    if isinstance(body, list):
        return " / ".join(x for x in body if isinstance(x, str))
    return ""


def _new_findings():
    return {
        "legarmeh": [],
        "paseq": [],
        "pisqah": [],
        "dual_mark_on_letter": [],
        "sofpasuq_per_witness": [],
        "nusach_notes": [],
    }


def _walk_markers(node, text, found):
    """Walk col_e collecting inline markers. Descends into מ:כפול's combined text only
    (NOT its rendered א/ב strands -- those duplicate the markers)."""
    if isinstance(node, str):
        text.append(node)
        return
    if isinstance(node, list):
        for x in node:
            _walk_markers(x, text, found)
        return
    if not isinstance(node, dict) or "tmpl_name" not in node:
        return
    name = node["tmpl_name"]
    params = node.get("tmpl_params", {})
    if name == "מ:לגרמיה-2":
        found["legarmeh"].append({"word": _last_word(text)})
    elif name == "מ:פסק":
        found["paseq"].append({"word": _last_word(text)})
    elif name == "מ:כפול":
        _walk_markers(params.get("כפול", []), text, found)  # only the combined text
    elif name == "נוסח":
        lemma = params.get("1", "")
        desc = _flatten_note_body(params.get("2", ""))
        found["nusach_notes"].append({"lemma": lemma, "note": desc})
        for sigla, strand in _SOFPASUQ_RE.findall(desc):
            found["sofpasuq_per_witness"].append(
                {"witnesses_lacking": sigla.strip().strip(","), "strand": strand}
            )
        if isinstance(lemma, str) and _CGJ in lemma:
            found["dual_mark_on_letter"].append(
                {"lemma": lemma.replace(_CGJ, ""), "note": desc}
            )
        if isinstance(lemma, str):
            text.append(lemma)  # keep word-before correct for later markers


def _collect_pisqah(node, found, parent_key=None):
    """Separate whole-verse scan: any template whose params carry the pisqah phrase.
    Tags the strand when the marker sits under מ:כפול's א/ב param."""
    if isinstance(node, dict):
        if node.get("tmpl_name") and _PISQAH in json.dumps(
            node.get("tmpl_params", {}), ensure_ascii=False
        ):
            strand = {"א": "taxton", "ב": "elyon"}.get(parent_key, "shared")
            found["pisqah"].append({"strand": strand})
            return  # don't double-count the phrase in nested copies
        for key, val in node.items():
            _collect_pisqah(val, found, key)
    elif isinstance(node, list):
        for x in node:
            _collect_pisqah(x, found, parent_key)


def _load_versemap():
    if not _VERSEMAP.exists():
        return {}
    data = json.loads(_VERSEMAP.read_text(encoding="utf-8"))
    return {r["mam_ref"]: [t["ref"] for t in r["targets"]] for r in data.get("mam_to_bhs", [])}


def _chapter(book_path, chnu):
    data = json.loads(book_path.read_text(encoding="utf-8"))
    for bk in data["book39s"]:
        if chnu in bk["chapters"]:
            return bk["chapters"][chnu]
    return {}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    versemap = _load_versemap()
    verses = []
    for short, filename, chnu in _PASSAGES:
        chapter = _chapter(_PARSED_PLUS / filename, chnu)
        for vn in sorted((k for k in chapter if k.isdigit()), key=int):
            verse = chapter[vn]
            found = _new_findings()
            col_e = verse[2] if len(verse) > 2 else []
            _walk_markers(col_e, [], found)
            _collect_pisqah(verse, found)
            found = {k: v for k, v in found.items() if v}
            if not found:
                continue
            mam_ref = f"{short} {chnu}:{int(vn)}"
            verses.append(
                {
                    "mam_ref": mam_ref,
                    "clc_bhs_refs": versemap.get(mam_ref, [mam_ref]),
                    "findings": found,
                }
            )

    out = {
        "_about": (
            "MAM Decalogue doc-note harvest (issues #42/#43/#44), read from the "
            "already-parsed MAM-parsed/plus JSON. Keyed to MAM's merged-elyon verse "
            "and the CLC/vtrad-BHS verse(s). Signal for by-hand encoding -- nothing "
            "here is embedded at CLC runtime."
        ),
        "verses": verses,
    }
    out_path = _REPO / ".novc" / "mam_decalogue_docnotes.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out_path} ({len(verses)} verses with findings)\n")

    tally = {}
    for v in verses:
        for cat, items in v["findings"].items():
            tally[cat] = tally.get(cat, 0) + len(items)
        cats = ", ".join(f"{k}×{len(x)}" for k, x in v["findings"].items())
        clc = "/".join(v["clc_bhs_refs"])
        print(f"  MAM {v['mam_ref']:<8} (CLC {clc}): {cats}")
    print("\ntotals:", ", ".join(f"{k}={n}" for k, n in sorted(tally.items())))


if __name__ == "__main__":
    main()
