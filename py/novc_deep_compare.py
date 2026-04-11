import xml.etree.ElementTree as ET
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# Parse XML - extract full detail from 2026.02.05 entries
xml_path = Path(
    r"c:\Users\BenDe\GitRepos\UXLC-utils\in\UXLC-misc\2026.04.01 - Changes.xml"
)
tree = ET.parse(xml_path)
root = tree.getroot()

xml_entries = []
for date_elem in root.iter("date"):
    date_text = date_elem.find("date")
    if date_text is not None and date_text.text == "2026.02.05":
        for change in date_elem.findall("change"):
            cit = change.find("citation")
            lc = change.find("lc")
            notes = [n.text for n in change.findall("notes/note") if n.text]
            xml_entries.append(
                {
                    "n": int(change.find("n").text),
                    "ref": f"Job {cit.find('c').text}:{cit.find('v').text}",
                    "cv": f"{cit.find('c').text}:{cit.find('v').text}",
                    "pos": cit.find("position").text,
                    "desc": change.find("description").text or "",
                    "reftext": (change.find("reftext").text or "").strip(),
                    "changetext": (change.find("changetext").text or "").strip(),
                    "lc_page": (
                        lc.find("folio").text.replace("Folio_", "")
                        if lc.find("folio") is not None
                        else ""
                    ),
                    "lc_col": (
                        lc.find("column").text if lc.find("column") is not None else ""
                    ),
                    "lc_line": (
                        lc.find("line").text if lc.find("line") is not None else ""
                    ),
                    "change_type": (change.find("type").text or ""),
                    "notes": notes,
                }
            )
        break

# Load quirkrecs
qr_path = Path(r"C:\Users\BenDe\GitRepos\book-of-job\out\enriched-quirkrecs.json")
quirkrecs = json.loads(qr_path.read_text(encoding="utf-8"))

# Also load the mapping file to know which XML entries match which quirkrecs
map_path = Path(
    r"c:\Users\BenDe\GitRepos\UXLC-utils\in\UXLC-misc\2026.04.01-map-to-book-of-job.json"
)
mapping = json.loads(map_path.read_text(encoding="utf-8"))

# Build lookup: html filename -> quirkrec index
# The HTML filenames in the mapping correspond 1:1 with the quirkrecs order
html_chain_files = [m["html"] for m in mapping["matched"]]

# Build: xml n -> quirkrec
# The matched entries in the mapping give us xml n -> html file
# The quirkrecs are in the same order as the html chain
# So matched[i] -> quirkrecs[i]
n_to_qr = {}
for i, m in enumerate(mapping["matched"]):
    n_to_qr[m["n"]] = quirkrecs[i]


# Keyword extraction helpers
def extract_letter_refs(text):
    """Extract Hebrew letter names mentioned in English text."""
    letters = [
        "alef",
        "bet",
        "gimmel",
        "dalet",
        "he",
        "vav",
        "zayin",
        "het",
        "tet",
        "yod",
        "kaf",
        "lamed",
        "mem",
        "nun",
        "samekh",
        "ayin",
        "pe",
        "tsadi",
        "qof",
        "resh",
        "shin",
        "sin",
        "tav",
    ]
    found = set()
    low = text.lower()
    for l in letters:
        if l in low:
            found.add(l)
    return found


def extract_mark_refs(text):
    """Extract diacritical/accent mark names from text (English or Hebrew)."""
    marks_en = [
        "dagesh",
        "mapiq",
        "meteg",
        "merkha",
        "dehi",
        "tipeha",
        "revia",
        "geresh",
        "munah",
        "etnachta",
        "siluq",
        "shuruq",
        "holam",
        "hiriq",
        "patah",
        "qamats",
        "segol",
        "sheva",
        "hataf",
        "paseq",
        "maqaf",
        "ole",
        "mahapakh",
        "geresh-muqdam",
    ]
    marks_he = {
        "דגש": "dagesh",
        "מפיק": "mapiq",
        "געיה": "meteg",
        "מרכא": "merkha",
        "דחי": "dehi",
        "טרחא": "tipeha",
        "רביע": "revia",
        "גרש": "geresh",
        "מונח": "munah",
        "אתנח": "etnachta",
        "סילוק": "siluq",
        "שורוק": "shuruq",
        "חולם": "holam",
        "חיריק": "hiriq",
        "פתח": "patah",
        "קמץ": "qamats",
        "סגול": "segol",
        "שווא": "sheva",
        "חטף": "hataf",
        "פסק": "paseq",
        "מקף": "maqaf",
        "עולה": "ole",
        "גרש מוקדם": "geresh-muqdam",
    }
    found = set()
    low = text.lower()
    for m in marks_en:
        if m in low:
            found.add(m)
    for heb, eng in marks_he.items():
        if heb in text:
            found.add(eng)
    return found


def extract_hebrew_letters_from_word(word):
    """Extract base Hebrew letters from a pointed word."""
    # Unicode ranges for Hebrew letters
    return [c for c in word if "\u05d0" <= c <= "\u05ea"]


# Compare
issues = []
ok_count = 0

for xe in xml_entries:
    if xe["n"] not in n_to_qr:
        continue  # xml_only entry, skip
    qr = n_to_qr[xe["n"]]

    entry_issues = []

    # 1. Verse reference match
    if xe["cv"] != qr["qr-cv"]:
        entry_issues.append(f"CV MISMATCH: xml={xe['cv']} qr={qr['qr-cv']}")

    # 2. LC location match
    qr_loc = qr.get("qr-lc-loc", {})
    qr_page = str(qr_loc.get("page", ""))
    qr_col = str(qr_loc.get("column", ""))
    qr_line_raw = qr_loc.get("line", "")
    qr_blanks = qr_loc.get("including-blank-lines", 0)
    # Normalize negative line numbers: -N means N from bottom of 28-line column
    if isinstance(qr_line_raw, int) and qr_line_raw < 0:
        qr_line_normalized = 28 + qr_line_raw
    else:
        qr_line_normalized = qr_line_raw
    # Subtract blank lines only for positive (top-down) line numbers.
    # Negative (bottom-up) line numbers already exclude blank lines.
    if isinstance(qr_line_raw, int) and qr_line_raw > 0 and isinstance(qr_blanks, int):
        qr_line_adjusted = qr_line_normalized - qr_blanks
    else:
        qr_line_adjusted = qr_line_normalized
    qr_line = str(qr_line_adjusted)
    if xe["lc_page"] and qr_page and xe["lc_page"] != qr_page:
        entry_issues.append(f"LC PAGE: xml={xe['lc_page']} qr={qr_page}")
    if xe["lc_col"] and qr_col and xe["lc_col"] != qr_col:
        entry_issues.append(f"LC COL: xml={xe['lc_col']} qr={qr_col}")
    if xe["lc_line"] and qr_line and xe["lc_line"] != qr_line:
        entry_issues.append(
            f"LC LINE: xml={xe['lc_line']} qr={qr_line} (raw={qr_line_raw}, blanks={qr_blanks})"
        )

    # 3. Hebrew text comparison
    # The XML reftext should match either qr-consensus or qr-lc-proposed
    qr_cons = qr.get("qr-consensus", "")
    qr_prop = qr.get("qr-lc-proposed", "")
    xml_ref = xe["reftext"]
    xml_chg = xe["changetext"]
    # Check if the XML Hebrew words appear in the quirkrec
    texts_match = False
    if xml_ref and (
        xml_ref in qr_cons
        or xml_ref in qr_prop
        or qr_cons in xml_ref
        or qr_prop in xml_ref
    ):
        texts_match = True
    # Also check if the base letters are the same
    if not texts_match and xml_ref:
        xml_letters = extract_hebrew_letters_from_word(xml_ref)
        cons_letters = extract_hebrew_letters_from_word(qr_cons)
        prop_letters = extract_hebrew_letters_from_word(qr_prop)
        if xml_letters and (xml_letters == cons_letters or xml_letters == prop_letters):
            texts_match = True
    if not texts_match and xml_ref:
        entry_issues.append(
            f"HEBREW: xml='{xml_ref}' qr-cons='{qr_cons}' qr-prop='{qr_prop}'"
        )

    # 4. Semantic topic comparison
    # Extract what marks/letters the XML desc talks about vs what qr-what-is-weird talks about
    xml_desc = xe["desc"]
    qr_weird = qr.get("qr-what-is-weird", "")
    if isinstance(qr_weird, list):
        qr_weird = " ".join(str(x) for x in qr_weird if x)
    qr_autodiff = " ".join(str(x) for x in qr.get("qr-auto-diff", []) if x)
    qr_comment = qr.get("qr-generic-comment", "")
    if isinstance(qr_comment, list):
        qr_comment = " ".join(str(x) for x in qr_comment)

    xml_marks = extract_mark_refs(xml_desc)
    qr_marks = extract_mark_refs(qr_weird + " " + qr_autodiff + " " + qr_comment)
    xml_letters = extract_letter_refs(xml_desc)
    qr_letters = extract_letter_refs(qr_weird)

    # Check if they share at least one mark or letter topic
    shared_marks = xml_marks & qr_marks
    shared_letters = xml_letters & qr_letters
    if not shared_marks and not shared_letters and xml_marks and qr_marks:
        entry_issues.append(
            f"TOPIC: xml marks={sorted(xml_marks)} qr marks={sorted(qr_marks)}"
        )

    if entry_issues:
        issues.append((xe, qr, entry_issues))
    else:
        ok_count += 1

print(f"Compared: {ok_count + len(issues)} entries")
print(f"OK (all fields match or are semantically compatible): {ok_count}")
print(f"Issues found: {len(issues)}")
print()

for xe, qr, entry_issues in issues:
    print(f"--- #{xe['n']} {xe['ref']}.{xe['pos']} ---")
    print(f"  XML desc: {xe['desc']}")
    print(f"  QR weird: {qr.get('qr-what-is-weird', '')}")
    print(f"  QR auto-diff: {qr.get('qr-auto-diff', '')}")
    for iss in entry_issues:
        print(f"  ** {iss}")
    print()
