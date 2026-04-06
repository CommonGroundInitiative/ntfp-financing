"""
seed_supabase.py
One-time import of all schemes from data/schemes.json into Supabase.
Also used by the GitHub Action to re-sync after every Excel update
(it deletes all active records first, then re-inserts from the JSON).

Usage:
    SUPABASE_URL=https://xxxx.supabase.co \
    SUPABASE_SERVICE_KEY=eyJ... \
    python scripts/seed_supabase.py

Requires: requests  (pip install requests)
"""

import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

ROOT       = Path(__file__).parent.parent
JSON_PATH  = ROOT / "data" / "schemes.json"

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SERVICE_KEY  = os.environ.get("SUPABASE_SERVICE_KEY", "")

if not SUPABASE_URL or not SERVICE_KEY:
    print(
        "ERROR: Set SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables.",
        file=sys.stderr,
    )
    sys.exit(1)

HEADERS = {
    "apikey":        SERVICE_KEY,
    "Authorization": f"Bearer {SERVICE_KEY}",
    "Content-Type":  "application/json",
    "Prefer":        "return=representation",
}


def api(path: str) -> str:
    return f"{SUPABASE_URL}/rest/v1/{path}"


def delete_all_active():
    """Remove all currently active schemes (and their activities via CASCADE)."""
    print("Deleting existing active schemes…")
    r = requests.delete(
        api("schemes"),
        headers=HEADERS,
        params={"status": "eq.active"},
    )
    r.raise_for_status()
    print(f"  Deleted {len(r.json()) if r.text else 0} schemes.")


def insert_scheme(s: dict) -> str:
    """Insert one scheme, return its new UUID."""
    payload = {
        "scheme_no":                 s.get("schemeNo", ""),
        "name":                      s["name"],
        "ministry":                  s.get("ministry", ""),
        "fund_recipient":            s.get("fundRecipient", ""),
        "socio_economic_preference": s.get("socioEconomicPreference", "Open to All"),
        "state_central":             s.get("stateCentral", "Central"),
        "status":                    "active",
    }
    r = requests.post(api("schemes"), headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()[0]["id"]


def insert_activities(scheme_id: str, activities: list):
    """Bulk-insert all activities for a scheme."""
    if not activities:
        return
    payload = [
        {
            "scheme_id":            scheme_id,
            "end_recipient_type":   a.get("endRecipientType", ""),
            "value_chain_activity": a.get("valueChainActivity", ""),
            "financing_type":       a.get("financingType", ""),
            "financing_notes":      a.get("financingNotes", ""),
            "link":                 a.get("link", ""),
        }
        for a in activities
    ]
    r = requests.post(api("scheme_activities"), headers=HEADERS, json=payload)
    r.raise_for_status()


def main():
    if not JSON_PATH.exists():
        print(f"ERROR: {JSON_PATH} not found. Run excel_to_json.py first.", file=sys.stderr)
        sys.exit(1)

    with open(JSON_PATH, encoding="utf-8") as f:
        schemes = json.load(f)

    delete_all_active()

    print(f"Inserting {len(schemes)} schemes…")
    for i, s in enumerate(schemes, 1):
        scheme_id = insert_scheme(s)
        insert_activities(scheme_id, s.get("activities", []))
        print(f"  [{i}/{len(schemes)}] {s['name']}")

    print(f"\n✓ Done. {len(schemes)} schemes now active in Supabase.")


if __name__ == "__main__":
    main()
