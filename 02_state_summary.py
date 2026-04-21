"""
02_state_summary.py
-------------------
Aggregates the cleaned data to state level.
Produces:
  • processed/state_summary.json   – total crimes, safety score, rank
  • processed/state_yearly.json    – total IPC crimes per state per year
                                     (used for trend charts on the dashboard)

Safety Score formula:
    score = round( (1 - state_total / max_state_total) * 100, 1 )
Higher score = fewer crimes relative to the worst-ranked state.
"""

import pandas as pd
import json, os

CLEAN_CSV = "cleaned/crimes_clean.csv"
OUT_DIR   = "processed"
os.makedirs(OUT_DIR, exist_ok=True)

META  = {"STATE", "DISTRICT", "YEAR"}

df = pd.read_csv(CLEAN_CSV)
crime_cols = [c for c in df.columns if c not in META]

# ── 1. State totals ─────────────────────────────────────────────────────────
state_df = df.groupby("STATE")[crime_cols].sum().reset_index()

max_total = state_df["TOTAL IPC CRIMES"].max()
state_df["SAFETY_SCORE"] = ((1 - state_df["TOTAL IPC CRIMES"] / max_total) * 100).round(1)
state_df["RANK"] = state_df["TOTAL IPC CRIMES"].rank(method="min").astype(int)

summary = []
for _, row in state_df.iterrows():
    summary.append({
        "state"        : row["STATE"],
        "total_crimes" : int(row["TOTAL IPC CRIMES"]),
        "safety_score" : float(row["SAFETY_SCORE"]),
        "rank"         : int(row["RANK"]),   # 1 = most crimes
    })

with open(f"{OUT_DIR}/state_summary.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"✅  state_summary.json  ({len(summary)} states)")

# ── 2. Yearly totals per state ───────────────────────────────────────────────
yearly = (
    df.groupby(["STATE", "YEAR"])["TOTAL IPC CRIMES"]
    .sum()
    .reset_index()
    .rename(columns={"TOTAL IPC CRIMES": "total"})
)

yearly_dict = {}
for state, grp in yearly.groupby("STATE"):
    yearly_dict[state] = [
        {"year": int(r["YEAR"]), "total": int(r["total"])}
        for _, r in grp.sort_values("YEAR").iterrows()
    ]

with open(f"{OUT_DIR}/state_yearly.json", "w") as f:
    json.dump(yearly_dict, f, indent=2)
print(f"✅  state_yearly.json   ({len(yearly_dict)} states × 12 years)")
