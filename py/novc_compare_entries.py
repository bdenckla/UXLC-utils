import xml.etree.ElementTree as ET
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# Parse XML
xml_path = Path(
    r"c:\Users\BenDe\GitRepos\UXLC-utils\in\UXLC-misc\2026.04.01 - Changes.xml"
)
tree = ET.parse(xml_path)
root = tree.getroot()

# Find the 2026.02.05 date block and extract entries
xml_entries = []
for date_elem in root.iter("date"):
    date_text = date_elem.find("date")
    if date_text is not None and date_text.text == "2026.02.05":
        for change in date_elem.findall("change"):
            n = change.find("n").text
            cit = change.find("citation")
            book = cit.find("book").text
            c = cit.find("c").text
            v = cit.find("v").text
            pos = cit.find("position").text
            desc = change.find("description").text
            xml_entries.append(
                {
                    "n": int(n),
                    "book": book,
                    "c": c,
                    "v": v,
                    "pos": pos,
                    "desc": desc,
                    "ref": f"{book} {c}:{v}",
                }
            )
        break

# Follow HTML chain starting from 0119.html
html_dir = Path(r"C:\Users\BenDe\GitRepos\book-of-job\docs\jobn-details")
html_entries = []
current = "0119.html"
while current and len(html_entries) < 200:
    fpath = html_dir / current
    if not fpath.exists():
        html_entries.append({"file": current, "ref": "FILE NOT FOUND", "desc": ""})
        break
    text = fpath.read_text(encoding="utf-8")
    # title
    m = re.search(r"<title>(.*?)</title>", text)
    title = m.group(1) if m else "?"
    # description from 3rd td
    tds = re.findall(r"<td[^>]*>(.*?)</td>", text, re.DOTALL)
    desc = ""
    if len(tds) >= 3:
        desc = re.sub(r"<[^>]+>", "", tds[2]).strip()
        desc = re.sub(r"\s+", " ", desc)
    html_entries.append({"file": current, "ref": title, "desc": desc})
    # find next link
    m = re.search(r'href="([^"]+)">next', text)
    if m:
        current = m.group(1)
    else:
        break

# Align by verse reference using a simple two-pointer approach
# For entries sharing the same ref (e.g. Job 8:16 appearing twice),
# consume them in order within each sequence.
print(f"XML entries: {len(xml_entries)}, HTML entries: {len(html_entries)}")
print()

xi, hi = 0, 0
matched = []
xml_only = []
html_only = []

while xi < len(xml_entries) and hi < len(html_entries):
    xe = xml_entries[xi]
    he = html_entries[hi]
    if xe["ref"] == he["ref"]:
        matched.append((xe, he))
        xi += 1
        hi += 1
    else:
        # Look ahead a few entries in each to find a match
        found_in_html = None
        for look in range(1, 4):
            if (
                hi + look < len(html_entries)
                and xml_entries[xi]["ref"] == html_entries[hi + look]["ref"]
            ):
                found_in_html = look
                break
        found_in_xml = None
        for look in range(1, 4):
            if (
                xi + look < len(xml_entries)
                and xml_entries[xi + look]["ref"] == html_entries[hi]["ref"]
            ):
                found_in_xml = look
                break
        if found_in_html is not None and (
            found_in_xml is None or found_in_html <= found_in_xml
        ):
            for skip in range(found_in_html):
                html_only.append(html_entries[hi + skip])
            hi += found_in_html
        elif found_in_xml is not None:
            for skip in range(found_in_xml):
                xml_only.append(xml_entries[xi + skip])
            xi += found_in_xml
        else:
            xml_only.append(xe)
            xi += 1

while xi < len(xml_entries):
    xml_only.append(xml_entries[xi])
    xi += 1
while hi < len(html_entries):
    html_only.append(html_entries[hi])
    hi += 1

print(
    f"Matched: {len(matched)}, XML-only: {len(xml_only)}, HTML-only: {len(html_only)}"
)

# Write JSON mapping
import json

output = {
    "xml_source": "in/UXLC-misc/2026.04.01 - Changes.xml",
    "html_base": "../book-of-job/docs/jobn-details/",
    "changeset": "2026.02.05",
    "matched": [
        {
            "n": xe["n"],
            "ref": xe["ref"],
            "pos": xe["pos"],
            "html": he["file"],
        }
        for xe, he in matched
    ],
    "xml_only": [
        {
            "n": xe["n"],
            "ref": xe["ref"],
            "pos": xe["pos"],
            "desc": xe["desc"],
        }
        for xe in xml_only
    ],
    "html_only": [
        {
            "html": he["file"],
            "ref": he["ref"],
        }
        for he in html_only
    ],
}

out_path = Path(
    r"c:\Users\BenDe\GitRepos\UXLC-utils\in\UXLC-misc\2026.04.01-map-to-book-of-job.json"
)
out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {out_path}")
