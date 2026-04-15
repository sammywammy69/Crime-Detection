"""
01_clean_data.py
----------------
Loads the raw NCRB IPC district-wise crime CSV (2001–2012),
cleans column names, normalises state names, converts all
crime columns to numeric, and writes a tidy CSV that every
downstream script imports instead of touching the original.

Output: cleaned/crimes_clean.csv
"""

import pandas as pd
import os

RAW_CSV  = "../01_District_wise_crimes_committed_IPC_2001_2012.csv"
OUT_DIR  = "cleaned"
OUT_FILE = os.path.join(OUT_DIR, "crimes_clean.csv")

os.makedirs(OUT_DIR, exist_ok=True)

# ── 1. Load ────────────────────────────────────────────────────────────────
df = pd.read_csv(RAW_CSV)
df.columns = df.columns.str.strip().str.upper()

# ── 2. Rename key meta columns ─────────────────────────────────────────────
df.rename(columns={"STATE/UT": "STATE", "YEAR": "YEAR", "DISTRICT": "DISTRICT"}, inplace=True)

# ── 3. Normalise state names ────────────────────────────────────────────────
STATE_MAP = {
    "A & N ISLANDS"   : "Andaman and Nicobar Islands",
    "DELHI UT"        : "Delhi",
    "D & N HAVELI"    : "Dadra and Nagar Haveli",
    "DAMAN & DIU"     : "Daman and Diu",
    "UTTARANCHAL"     : "Uttarakhand",
    "ORISSA"          : "Odisha",
}
df["STATE"] = df["STATE"].replace(STATE_MAP)

# ── 4. Cast all crime columns to numeric ────────────────────────────────────
META_COLS = {"STATE", "DISTRICT", "YEAR"}
crime_cols = [c for c in df.columns if c not in META_COLS]
df[crime_cols] = df[crime_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

# ── 5. Save ─────────────────────────────────────────────────────────────────
df.to_csv(OUT_FILE, index=False)

states   = df["STATE"].nunique()
years    = sorted(df["YEAR"].unique())
print(f"✅  Cleaned CSV saved → {OUT_FILE}")
print(f"    Rows: {len(df):,}  |  States: {states}  |  Years: {years[0]}–{years[-1]}")
print(f"    Crime columns ({len(crime_cols)}): {crime_cols[:5]} …")
