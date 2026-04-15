"""
06_bundle_dashboard.py
-----------------------
Reads all processed JSON files and merges them into one compact
dashboard_data.json that the index.html loads at runtime.

This keeps index.html free of raw data while giving the browser
a single fetch instead of five separate requests.

Input files (all under processed/):
    state_summary.json
    state_yearly.json
    top_crimes_state.json
    crime_heatmap.json
    women_crimes_state.json
    women_crimes_yearly.json
    women_helplines.json

Output: ../dashboard_data.json
"""

import json, os

PROCESSED = "processed"
OUTPUT    = "../dashboard_data.json"

def load(filename):
    path = os.path.join(PROCESSED, filename)
    with open(path) as f:
        return json.load(f)

bundle = {
    "meta": {
        "source"   : "NCRB District-wise IPC Crimes 2001–2012",
        "generated": __import__("datetime").date.today().isoformat(),
        "scripts"  : [
            "01_clean_data.py → cleaned/crimes_clean.csv",
            "02_state_summary.py → state_summary.json, state_yearly.json",
            "03_top_crimes.py → top_crimes_state.json, top_crimes_district.json, crime_heatmap.json",
            "04_women_safety.py → women_crimes_state.json, women_crimes_yearly.json, women_helplines.json",
            "05_generate_map.py → india_crime_map.html",
            "06_bundle_dashboard.py → dashboard_data.json  ← (this file)",
        ],
    },
    "state_summary"      : load("state_summary.json"),
    "state_yearly"       : load("state_yearly.json"),
    "top_crimes_state"   : load("top_crimes_state.json"),
    "crime_heatmap"      : load("crime_heatmap.json"),
    "women_crimes_state" : load("women_crimes_state.json"),
    "women_crimes_yearly": load("women_crimes_yearly.json"),
    "women_helplines"    : load("women_helplines.json"),
}

with open(OUTPUT, "w") as f:
    json.dump(bundle, f, separators=(",", ":"))   # compact for browser

size_kb = os.path.getsize(OUTPUT) / 1024
print(f"✅  dashboard_data.json  ({size_kb:.1f} KB)")
print(f"    Sections: {[k for k in bundle if k != 'meta']}")
