"""Dump the CLC(vtrad-BHS) <-> MAM(vtrad-MAM, merged-elyon) Decalogue verse map.

THROWAWAY SCAFFOLDING (issues #42-45). Disposable once the harvest is hand-encoded.
Remaining debt that would be UNACCEPTABLE in official code: it does a live cross-repo
import from `MAM-basics/py`. That is NOT generally allowed -- the sanctioned way to
reuse MAM-basics code is VENDORING (copy the module in), and even that is impossible
here because only `mb_*` dirs are vendorable while this pulls from `py_misc`
(vtrad_data / vtrad_helpers), which is neither importable nor vendorable. A real
dependency would need the converter exposed via a public `mb_*` entry point (or the
tiny Decalogue map inlined). Tolerated ONLY because this script retires with #42-45.
(The machine-absolute path has already been replaced with a sibling-repo relative one.)


Foundation for the MAM-doc-note harvest (issues #42/#43/#44) and the vtrad-MAM
overlay (#45), and the shared CLC->MAM verse-map that #38 also needs. Design doc
§7.8 / §7.12: MAM's Decalogue verse numbering (merged ta'am-elyon) runs ~1 behind
CLC's vtrad-BHS, so a verse map is needed before any MAM doc-note can be keyed to a
CLC verse.

We do NOT re-derive the map: we reuse MAM-basics' existing MAM->{BHS,Sef}
versification converter (py_misc.vtrad_data.BCV_DIC_FROM_MAM_TO_YYY, built the same
way MAM-simple is emitted in BHS/Sefaria numbering) and merely invert + serialize
the Exodus-20 / Deuteronomy-5 slice. Follows the tools/dump_mam_strands.py precedent
(reach into the sibling MAM repo, write a scratch JSON under .novc/ that a later
hand-encoding step consumes -- nothing of MAM is embedded at CLC runtime).

Run: python tools/dump_mam_decalogue_versemap.py
"""

import json
import sys
from pathlib import Path

# Sibling-repo relative path (…/GitRepos/MAM-basics/py), not a machine-absolute one.
_MAM_PY = Path(__file__).resolve().parents[2] / "MAM-basics" / "py"
sys.path.insert(0, str(_MAM_PY))

from mb_cmn import bib_locales as tbn  # noqa: E402
from py_misc import vtrad_data  # noqa: E402
from py_misc import vtrad_helpers as helpers  # noqa: E402

# The two Decalogue passages, by (bk39id, chapter). CLC/§7.7 detangles exactly these.
_PASSAGES = ((tbn.BK_EXODUS, 20), (tbn.BK_DEUTER, 5))
_BK_SHORT = {tbn.BK_EXODUS: "Ex", tbn.BK_DEUTER: "Dt"}

_CVVE_TYPE_NAME = {
    helpers.CVVE_TYPE_SAME_CONTENTS: "same-contents",
    helpers.CVVE_TYPE_NO_CONTENTS: "no-contents",
    helpers.CVVE_TYPE_PARTIAL_CONTENTS: "partial-contents",  # a split part
}


def _bk_ch(bcvt):
    return tbn.bcvt_get_bk39id(bcvt), tbn.bcvt_get_chnu(bcvt)


def _ref_str(bk39id, chnu, vrnu):
    return f"{_BK_SHORT.get(bk39id, bk39id)} {chnu}:{vrnu}"


def _mam_ref_str(bcvtmam):
    bk39id, chnu, vrnu = tbn.bcvt_get_bcv_triple(bcvtmam)
    return _ref_str(bk39id, chnu, vrnu)


def _forward_entries(vtrad):
    """MAM -> target-vtrad rows for the Decalogue passages, as plain dicts."""
    dic = vtrad_data.BCV_DIC_FROM_MAM_TO_YYY[vtrad]
    rows = []
    for bcvtmam, maprec in dic.items():
        if _bk_ch(bcvtmam) not in _PASSAGES:
            continue
        targets = []
        for cvve in maprec:
            cvt = helpers.cvve_get_cvv(cvve)
            chnu, vrnu = tbn.cvt_get_chnu(cvt), tbn.cvt_get_vrnu(cvt)
            targets.append(
                {
                    "ref": _ref_str(tbn.bcvt_get_bk39id(bcvtmam), chnu, vrnu),
                    "chnu": chnu,
                    "vrnu": vrnu,
                    "kind": _CVVE_TYPE_NAME[helpers.cvve_get_type(cvve)],
                }
            )
        rows.append(
            {
                "mam_ref": _mam_ref_str(bcvtmam),
                "mam_chnu": tbn.bcvt_get_chnu(bcvtmam),
                "mam_vrnu": tbn.bcvt_get_vrnu(bcvtmam),
                "targets": targets,
                "one_to_many": len(targets) > 1,
            }
        )
    rows.sort(key=lambda r: (r["mam_ref"].split()[0], r["mam_chnu"], r["mam_vrnu"]))
    return rows


def _invert_to_bhs(bhs_rows):
    """target(BHS) -> MAM, the direction CLC (BHS-primary) actually consults."""
    inv = {}
    for row in bhs_rows:
        for tgt in row["targets"]:
            inv.setdefault(
                tgt["ref"],
                {"bhs_ref": tgt["ref"], "mam_ref": row["mam_ref"], "kind": tgt["kind"]},
            )
    return [inv[k] for k in sorted(inv, key=lambda r: (r.split()[0], r))]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    bhs_rows = _forward_entries(tbn.VT_BHS)
    sef_rows = _forward_entries(tbn.VT_SEF)
    out = {
        "_about": (
            "CLC(vtrad-BHS) <-> MAM(vtrad-MAM merged-elyon) Decalogue verse map. "
            "Only NON-identity verses appear here (splits + shifted spans); every "
            "other Decalogue verse maps 1:1 with the same chnu/vrnu. Reused from "
            "MAM-basics py_misc.vtrad_data.BCV_DIC_FROM_MAM_TO_YYY."
        ),
        "mam_to_bhs": bhs_rows,
        "mam_to_sef": sef_rows,
        "bhs_to_mam": _invert_to_bhs(bhs_rows),
    }
    out_path = Path(__file__).resolve().parent.parent / ".novc" / "mam_decalogue_versemap.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out_path}")

    print("\nMAM -> BHS (non-identity Decalogue verses):")
    for row in bhs_rows:
        arrow = "  =>  " if not row["one_to_many"] else "  =>  [split] "
        tgts = ", ".join(t["ref"] for t in row["targets"])
        print(f"  MAM {row['mam_ref']:<8}{arrow}{tgts}")


if __name__ == "__main__":
    main()
