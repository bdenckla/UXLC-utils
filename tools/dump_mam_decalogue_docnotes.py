"""Harvest MAM's Decalogue doc-note markup for the CLC MAM-alignment features.

THROWAWAY SCAFFOLDING (issues #42-45): its only product is a .novc/ JSON that a human
reads to hand-encode the CLC oracle; it dies once the issues are encoded.

Source is **MAM-parsed/plus** (already-parsed structured JSON), read directly over the
sibling-repo relative path (../MAM-parsed) -- no absolute path, no MAM-basics import.
Each verse is [CP, DP, EP]; EP (index 2) is the body sequence of strings and template
objects. Rather than re-walk the template format by hand, this reuses the repo's
already-vendored MAM-parsed-plus helpers in py/mb_diff_mpu (the same module CLC's own
clc_dual_cant / clc_render use):
  * get_param            -- robust template-param access across historical formats
  * is_parashah_template -- classify סס/ססס/פפ section-break markers
  * flatten_element      -- flatten a nested EP element to body text

What maps onto which CLC feature:
  * legarmeh   {"tmpl_name": "מ:לגרמיה-2"}                     -> #42 (§7.16)
  * paseq      {"tmpl_name": "מ:פסק"}                          -> #42 legarmeh-vs-paseq contrast
  * pisqah be'emtsa pasuq  a parashah template whose param 1 == "פסקא באמצע פסוק",
               strand-specific when it sits under מ:כפול's א/ב  -> #42 (§7.7)
  * two marks on one letter: /plus keeps no dedicated template (the CSV's
    {{שני טעמים..}} / {{מ:טעם ומתג..}} were resolved into stacked Unicode); the tell is
    a CGJ (U+034F) in a נוסח lemma, e.g. מִתָּ֑͏ַ֜חַת / תִּֿרְצָ֖͏ֽח, marks named in the body  -> #44 (§7.7)
  * per-witness sof-pasuq: נוסח body "<sigla>=חסר סימן נקודותיים של סוף פסוק לטעם ה.." -> #43 (§7.7)
  * plus every נוסח doc-note (lemma + body) verbatim, the general harvest.

(The /plus format is documented -- see MAM-parsed/README.md -> gh-pages/plus/html/
mpplus*.html. A SECOND doc-note type, מ:הערה-2 [scroll-difference notes], distinct from
נוסח, does NOT occur in the two Decalogues, so it is not harvested here. The README
warns the /plus format is not yet stable.)

Verse refs are keyed to MAM's merged-elyon numbering (the /plus chapter/verse keys)
and to CLC/vtrad-BHS via tools/dump_mam_decalogue_versemap.py.

Run: python tools/dump_mam_decalogue_versemap.py   (first, to refresh the verse map)
     python tools/dump_mam_decalogue_docnotes.py
"""

import json
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent            # .../GitRepos/UXLC-utils
sys.path.insert(0, str(_REPO / "py"))                     # vendored mb_diff_mpu lives here

from mb_diff_mpu.mpplus_param_access import MISSING, get_param  # noqa: E402
from mb_diff_mpu.mpplus_flatten import is_parashah_template, flatten_element  # noqa: E402

_PARSED_PLUS = _REPO.parent / "MAM-parsed" / "plus"
_VERSEMAP = _REPO / ".novc" / "mam_decalogue_versemap.json"

# (short-ref, /plus filename, chapter-key) for the two Decalogue passages.
_PASSAGES = (("Ex", "A2-Exodus.json", "20"), ("Dt", "A5-Deuter.json", "5"))

_LEGARMEH = ("מ:לגרמיה-2", "מ:לגרמיה")
_PISQAH = "פסקא באמצע פסוק"
_CGJ = chr(0x034F)  # COMBINING GRAPHEME JOINER -- MAM stacks two marks on one letter with it
_SOFPASUQ_RE = re.compile(
    r"([^=/]*?)=חסר סימן נקודותיים של סוף פסוק לטעם ה(תחתון|עליון)"
)


def _param(tmpl, key):
    v = get_param(tmpl, key)
    return None if v is MISSING else v


def _last_word(text_parts):
    toks = "".join(text_parts).split()
    return toks[-1] if toks else ""


def _note_body_text(param2):
    """Flatten a נוסח '2' body but keep {{ש}} line breaks as ' / ' separators, so the
    per-witness sigla groups stay bounded for _SOFPASUQ_RE (flatten_element would
    concatenate them with no separator)."""
    if param2 is None:
        return ""
    if isinstance(param2, str):
        return param2
    if isinstance(param2, list):
        return " / ".join(x for x in param2 if isinstance(x, str))
    return flatten_element(param2)


def _new_findings():
    return {k: [] for k in (
        "legarmeh", "paseq", "pisqah",
        "dual_mark_on_letter", "sofpasuq_per_witness", "nusach_notes",
    )}


def _walk_markers(node, text, found):
    """Collect inline markers + נוסח notes from an EP array. Descends into מ:כפול's
    combined text only (NOT its rendered א/ב strands, which duplicate the markers)."""
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
    if name in _LEGARMEH:
        found["legarmeh"].append({"word": _last_word(text)})
    elif name == "מ:פסק":
        found["paseq"].append({"word": _last_word(text)})
    elif name == "מ:כפול":
        _walk_markers(_param(node, "כפול"), text, found)  # combined text only
    elif name == "נוסח":
        p1, p2 = _param(node, "1"), _param(node, "2")
        lemma = flatten_element(p1) if p1 is not None else ""
        body = _note_body_text(p2)
        found["nusach_notes"].append({"lemma": lemma, "note": body})
        for sigla, strand in _SOFPASUQ_RE.findall(body):
            found["sofpasuq_per_witness"].append(
                {"witnesses_lacking": sigla.strip().strip(","), "strand": strand}
            )
        if _CGJ in lemma:
            found["dual_mark_on_letter"].append(
                {"lemma": lemma.replace(_CGJ, ""), "note": body}
            )
        # A נוסח's param 1 is the TARGET -- part of the running text itself -- so walk it
        # (not just append its flattened string): a מ:פסק / מ:לגרמיה-2 nested there (e.g. Ex
        # 20:3 בשמים, whose paseq sits inside a נוסח recording L's disputed stroke) is a real,
        # tagged mark and must be counted, not hidden behind the flattened "‖" lemma.
        if p1 is not None:
            _walk_markers(p1, text, found)
    elif is_parashah_template(name):
        text.append(" ")  # a section break separates words; pisqah handled separately


def _collect_pisqah(node, found, parent_key=None):
    """Whole-verse scan for pisqah-be'emtsa-pasuq markers, tagging the strand when the
    marker sits under מ:כפול's א/ב param (א=taxton, ב=elyon per the /plus dualcant spec)."""
    if isinstance(node, dict):
        name = node.get("tmpl_name")
        if name and is_parashah_template(name) and _param(node, "1") == _PISQAH:
            strand = {"א": "taxton", "ב": "elyon"}.get(parent_key, "shared")
            found["pisqah"].append({"strand": strand})
            return
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
            ep = verse[2] if len(verse) > 2 else []          # [CP, DP, EP] -> EP
            _walk_markers(ep, [], found)
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
            "already-parsed MAM-parsed/plus JSON via the vendored py/mb_diff_mpu "
            "helpers. Keyed to MAM's merged-elyon verse and the CLC/vtrad-BHS "
            "verse(s). Signal for by-hand encoding -- nothing here is embedded at "
            "CLC runtime."
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
        print(f"  MAM {v['mam_ref']:<8} (CLC {'/'.join(v['clc_bhs_refs'])}): {cats}")
    print("\ntotals:", ", ".join(f"{k}={n}" for k, n in sorted(tally.items())))


if __name__ == "__main__":
    main()
