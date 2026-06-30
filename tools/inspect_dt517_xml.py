"""Dump the raw XML structure of Deut 5:17's words + how clc_read tokenizes the verse,
to see why the test's naive _read_atoms truncates word 2 (תרצח). Writes UTF-8."""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "py"))
import clc.clc_read as clc_read  # noqa: E402

out = []
root = ET.parse(_REPO / "in" / "UXLC-39" / "Deuteronomy.xml").getroot()
for c in root.iter("c"):
    if c.get("n") != "5":
        continue
    for v in c.iter("v"):
        if v.get("n") != "17":
            continue
        for i, w in enumerate(v):
            out.append(f"elem {i}: tag={w.tag!r} text={w.text!r} tail={w.tail!r}")
            for ch in w:
                out.append(f"    child tag={ch.tag!r} text={ch.text!r} tail={ch.tail!r} attrib={ch.attrib}")
            out.append(f"    itertext={''.join(w.itertext())!r}")

out.append("---- clc_read tokenization of Deut 5:17 ----")
book = clc_read.read_book("Deuter")
for j, atom in enumerate(book[5 - 1][17 - 1], start=1):
    out.append(f"atom {j}: {atom!r}")

(_REPO / ".novc" / "dt517_xml.txt").write_text("\n".join(out), encoding="utf-8")
print("wrote .novc/dt517_xml.txt")
