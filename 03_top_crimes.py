"""
03_top_crimes.py
----------------
Computes the top IPC crime categories for each state AND each district.
Excludes sub-categories and catch-all buckets so the ranking reflects
meaningful, named offences only.

Outputs:
  • processed/top_crimes_state.json   – top N crimes per state
  • processed/top_crimes_district.json – top N crimes per district
                                         (nested under state)
  • processed/crime_heatmap.json      – all crime totals per state
                                         (used for a full breakdown table)
"""

import pandas as pd
import json, os

CLEAN_CSV = "cleaned/crimes_clean.csv"
OUT_DIR   = "processed"
TOP_N     = 5   # how many top crimes to keep

META  = {"STATE", "DISTRICT", "YEAR"}
# Exclude derived / catch-all columns
EXCL  = {
    "TOTAL IPC CRIMES",
    "CUSTODIAL RAPE",
    "OTHER RAPE",
    "OTHER THEFT",
    "KIDNAPPING AND ABDUCTION OF OTHERS",
    "OTHER IPC CRIMES",
    "PREPARATION AND ASSEMBLY FOR DACOITY",
}

df = pd.read_csv(CLEAN_CSV)
crime_cols = [c for c in df.columns if c not in META and c not in EXCL]

# ── helper ──────────────────────────────────────────────────────────────────
def top_n(series: pd.Series, n: int):
    top = series.astype(float).nlargest(n)
    return [{"crime": k.title(), "count": int(v)} for k, v in top.items()]

# ── 1. State-level top N ─────────────────────────────────────────────────────
state_df = df.groupby("STATE")[crime_cols].sum()

state_top = {}
for state, row in state_df.iterrows():
    state_top[state] = top_n(row, TOP_N)

with open(f"{OUT_DIR}/top_crimes_state.json", "w") as f:
    json.dump(state_top, f, indent=2)
print(f"✅  top_crimes_state.json   (top {TOP_N} crimes, {len(state_top)} states)")

# ── 2. District-level top N (nested under state) ─────────────────────────────
dist_df  = df.groupby(["STATE", "DISTRICT"])[crime_cols].sum().reset_index()

district_top = {}
for _, row in dist_df.iterrows():
    state, dist = row["STATE"], row["DISTRICT"]
    district_top.setdefault(state, {})[dist] = top_n(row[crime_cols], TOP_N)

with open(f"{OUT_DIR}/top_crimes_district.json", "w") as f:
    json.dump(district_top, f, indent=2)
total_dist = sum(len(v) for v in district_top.values())
print(f"✅  top_crimes_district.json ({total_dist} districts across {len(district_top)} states)")

# ── 3. Full crime heatmap (all categories, state totals) ─────────────────────
heatmap = {}
for state, row in state_df.iterrows():
    heatmap[state] = {col.title(): int(row[col]) for col in crime_cols}

with open(f"{OUT_DIR}/crime_heatmap.json", "w") as f:
    json.dump(heatmap, f, indent=2)
print(f"✅  crime_heatmap.json      ({len(crime_cols)} crime types per state)")
