"""
excel_to_json.py
Converts data/schemes.xlsx → data/schemes.json

Run manually:  python scripts/excel_to_json.py
Also called by GitHub Actions on every Excel update.

Requires: openpyxl  (pip install openpyxl)
"""

import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).parent.parent
EXCEL_PATH = ROOT / "data" / "schemes.xlsx"
JSON_PATH  = ROOT / "data" / "schemes.json"

NS = {"ns": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def col_to_num(col: str) -> int:
    num = 0
    for c in col:
        num = num * 26 + (ord(c) - ord("A") + 1)
    return num - 1


def parse_ref(ref: str):
    m = re.match(r"([A-Z]+)(\d+)", ref)
    return col_to_num(m.group(1)), int(m.group(2)) - 1


def read_shared_strings(z: zipfile.ZipFile):
    shared = []
    with z.open("xl/sharedStrings.xml") as f:
        root = ET.parse(f).getroot()
    for si in root.findall("ns:si", NS):
        t = si.find("ns:t", NS)
        if t is not None and t.text:
            shared.append(t.text)
        else:
            parts = [r.find("ns:t", NS) for r in si.findall("ns:r", NS)]
            shared.append("".join(p.text or "" for p in parts if p is not None))
    return shared


def read_sheet(z: zipfile.ZipFile, sheet_name: str, shared: list) -> dict:
    with z.open(f"xl/worksheets/{sheet_name}") as f:
        root = ET.parse(f).getroot()
    rows = {}
    for row in root.findall(".//ns:row", NS):
        rn = int(row.get("r"))
        rows[rn] = {}
        for cell in row.findall("ns:c", NS):
            ref = cell.get("r")
            t   = cell.get("t")
            v   = cell.find("ns:v", NS)
            if v is not None and v.text:
                val = shared[int(v.text)] if t == "s" else v.text
                col, _ = parse_ref(ref)
                rows[rn][col] = val
    return rows


def build_schemes(rows: dict) -> list:
    schemes_map: dict = {}
    for rn in sorted(rows.keys())[1:]:          # skip header row
        row = rows[rn]
        if not row or not row.get(1):
            continue
        name = row.get(1, "").strip()
        if not name:
            continue
        if name not in schemes_map:
            schemes_map[name] = {
                "schemeNo":                row.get(0, "").strip(),
                "name":                    name,
                "ministry":                row.get(2, "").strip(),
                "fundRecipient":           row.get(3, "").strip(),
                "socioEconomicPreference": row.get(7, "").strip() or "Open to All",
                "stateCentral":            row.get(8, "").strip(),
                "endRecipientTypes":       [],
                "valueChainActivities":    [],
                "financingTypes":          [],
                "activities":              [],
                "links":                   [],
            }
        s = schemes_map[name]
        for field, key in [
            (4, "endRecipientTypes"),
            (5, "valueChainActivities"),
            (6, "financingTypes"),
        ]:
            val = row.get(field, "").strip()
            if val and val not in s[key]:
                s[key].append(val)
        link = row.get(10, "").strip()
        if link and link not in s["links"]:
            s["links"].append(link)
        s["activities"].append({
            "endRecipientType":    row.get(4, "").strip(),
            "valueChainActivity":  row.get(5, "").strip(),
            "financingType":       row.get(6, "").strip(),
            "financingNotes":      row.get(9, "").strip(),
            "link":                link,
        })
    schemes = sorted(
        schemes_map.values(),
        key=lambda x: float(x["schemeNo"]) if x["schemeNo"] else 0,
    )
    # Normalise "None" preference
    for s in schemes:
        if s["socioEconomicPreference"].lower() in ("none", ""):
            s["socioEconomicPreference"] = "Open to All"
    return schemes


def main():
    if not EXCEL_PATH.exists():
        print(f"ERROR: {EXCEL_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    z = zipfile.ZipFile(EXCEL_PATH)
    shared = read_shared_strings(z)
    rows   = read_sheet(z, "sheet2.xml", shared)   # sheet2 = main data sheet
    schemes = build_schemes(rows)

    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(schemes, f, ensure_ascii=False, indent=2)

    print(f"✓ Wrote {len(schemes)} schemes to {JSON_PATH}")


if __name__ == "__main__":
    main()
