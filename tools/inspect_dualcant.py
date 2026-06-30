"""Print the authoritative supplied-mark / division-change / anomaly inventory from the
wlc-utils detangler output (_dual_cant.json), ASCII fields only (safe for cp1252 console).
"""

import json
from pathlib import Path

_F = Path(r"C:\Users\BenDe\GitRepos\wlc-utils\out\accgram\dual-cant\_dual_cant.json")
data = json.loads(_F.read_text(encoding="utf-8"))


def _find(node, key):
    """Yield every dict in the tree that has `key`."""
    if isinstance(node, dict):
        if key in node:
            yield node
        for v in node.values():
            yield from _find(v, key)
    elif isinstance(node, list):
        for v in node:
            yield from _find(v, key)


passages = data["passages"] if isinstance(data, dict) and "passages" in data else data
for p in passages if isinstance(passages, list) else []:
    name = p.get("name", "?")
    print(f"\n===== passage {name} =====")
    sup = p.get("supplied_marks", [])
    div = p.get("division_changes", [])
    anom = p.get("anomalies", [])
    print(f"-- supplied_marks ({len(sup)}) --")
    for s in sup:
        print(f"   {s.get('bcv'):8} {s.get('strand'):4} {s.get('strand_label'):8} "
              f"accent={s.get('accent_name')} source={s.get('source')}")
    print(f"-- division_changes ({len(div)}) --")
    for d in div:
        print(f"   {d.get('bcv'):8} {d.get('strand'):4} {d.get('strand_label'):8} "
              f"{d.get('delta'):7} {d.get('mark')}")
    print(f"-- anomalies ({len(anom)}) --")
    for a in anom:
        print(f"   {a.get('bcv'):8} {a.get('strand'):4} {a.get('strand_label'):8} "
              f"expected=[{a.get('expected_name')}] found=[{a.get('found_name')}]")
