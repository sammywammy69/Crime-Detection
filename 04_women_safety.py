"""
04_women_safety.py
------------------
Extracts all crime-against-women categories and produces:
  • processed/women_crimes_state.json   – totals per state
  • processed/women_crimes_yearly.json  – year-wise trend per state
  • processed/women_helplines.json      – curated state helpline numbers

Women-specific IPC columns used:
  RAPE | KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS |
  DOWRY DEATHS | ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY |
  INSULT TO MODESTY OF WOMEN | CRUELTY BY HUSBAND OR HIS RELATIVES |
  IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES
"""

import pandas as pd
import json, os

CLEAN_CSV = "cleaned/crimes_clean.csv"
OUT_DIR   = "processed"

WOMEN_COLS = [
    "RAPE",
    "KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS",
    "DOWRY DEATHS",
    "ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY",
    "INSULT TO MODESTY OF WOMEN",
    "CRUELTY BY HUSBAND OR HIS RELATIVES",
    "IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES",
]

df = pd.read_csv(CLEAN_CSV)
available = [c for c in WOMEN_COLS if c in df.columns]

# ── 1. State-level women crime totals ────────────────────────────────────────
state_df = df.groupby("STATE")[available].sum().reset_index()

women_crimes = {}
for _, row in state_df.iterrows():
    women_crimes[row["STATE"]] = {
        col.title(): int(row[col]) for col in available
    }

with open(f"{OUT_DIR}/women_crimes_state.json", "w") as f:
    json.dump(women_crimes, f, indent=2)
print(f"✅  women_crimes_state.json  ({len(women_crimes)} states, {len(available)} crime types)")

# ── 2. Year-wise trend per state ─────────────────────────────────────────────
yearly_df = df.groupby(["STATE", "YEAR"])[available].sum().reset_index()

women_yearly = {}
for state, grp in yearly_df.groupby("STATE"):
    women_yearly[state] = [
        {
            "year": int(r["YEAR"]),
            **{col.title(): int(r[col]) for col in available}
        }
        for _, r in grp.sort_values("YEAR").iterrows()
    ]

with open(f"{OUT_DIR}/women_crimes_yearly.json", "w") as f:
    json.dump(women_yearly, f, indent=2)
print(f"✅  women_crimes_yearly.json ({len(women_yearly)} states × 12 years)")

# ── 3. State-specific helpline numbers ───────────────────────────────────────
HELPLINES = {
    "ANDHRA PRADESH"             : {"SHE Teams": "100", "Women Helpline": "1091", "AP Women Commission": "040-23390460"},
    "ARUNACHAL PRADESH"          : {"Women Helpline": "1091", "Police": "100"},
    "ASSAM"                      : {"Women Helpline": "1091", "Assam Police": "100", "Women Commission": "0361-2237272"},
    "BIHAR"                      : {"Women Helpline": "1091", "Bihar Women Commission": "0612-2215556"},
    "CHANDIGARH"                 : {"Women Helpline": "1091", "Police": "100"},
    "CHHATTISGARH"               : {"Women Helpline": "1091", "CG Mahila Ayog": "0771-2445002"},
    "Dadra and Nagar Haveli"     : {"Women Helpline": "1091", "Police": "100"},
    "Daman and Diu"              : {"Women Helpline": "1091", "Police": "100"},
    "Delhi"                      : {"Women Helpline": "181", "Delhi Police PCR": "100", "Delhi Commission for Women": "011-23379181"},
    "GOA"                        : {"Women Helpline": "1091", "Women & Child Dev": "0832-2438591"},
    "GUJARAT"                    : {"Abhayam Helpline": "181", "Women Helpline": "1091"},
    "HARYANA"                    : {"Women Helpline": "1091", "Durga Shakti": "1008"},
    "HIMACHAL PRADESH"           : {"Women Helpline": "1091", "Police": "100"},
    "JAMMU & KASHMIR"            : {"Women Helpline": "1091", "Police": "100"},
    "JHARKHAND"                  : {"Women Helpline": "1091", "JH Women Commission": "0651-2490008"},
    "KARNATAKA"                  : {"Vanitha Sahayavani": "1091", "Police": "100"},
    "KERALA"                     : {"Women Helpline": "1091", "Police Women Cell": "0471-2722399", "Nirbhaya": "0471-2337484"},
    "LAKSHADWEEP"                : {"Women Helpline": "1091", "Police": "100"},
    "MADHYA PRADESH"             : {"Women Helpline": "1091", "MP Women Commission": "0755-2661912"},
    "MAHARASHTRA"                : {"Women Helpline": "1091", "iCall (Tata)": "9152987821", "Mumbai Police": "100"},
    "MANIPUR"                    : {"Women Helpline": "1091", "Police": "100"},
    "MEGHALAYA"                  : {"Women Helpline": "1091", "Police": "100"},
    "MIZORAM"                    : {"Women Helpline": "1091", "Police": "100"},
    "NAGALAND"                   : {"Women Helpline": "1091", "Police": "100"},
    "Odisha"                     : {"Women Helpline": "1091", "Odisha Women Commission": "0674-2392707"},
    "PUDUCHERRY"                 : {"Women Helpline": "1091", "Police": "100"},
    "PUNJAB"                     : {"Women Helpline": "1091", "Punjab Women Commission": "0172-2740819"},
    "RAJASTHAN"                  : {"Women Helpline": "1091", "Abhay Command Centre": "181"},
    "SIKKIM"                     : {"Women Helpline": "1091", "Police": "100"},
    "TAMIL NADU"                 : {"Women Helpline": "1091", "All Women Police Stn": "044-28512526"},
    "TRIPURA"                    : {"Women Helpline": "1091", "Police": "100"},
    "UTTAR PRADESH"              : {"Women Power Line": "1090", "Police": "100", "Anti-Romeo Squad": "1090"},
    "UTTARAKHAND"                : {"Women Helpline": "1091", "Police": "100"},
    "WEST BENGAL"                : {"Women Helpline": "1091", "WB Commission for Women": "1800-345-8181"},
    "Andaman and Nicobar Islands": {"Women Helpline": "1091", "Police": "100"},
}

# Also write universal helplines as a separate key
UNIVERSAL = {
    "Police"         : "100",
    "Women Helpline" : "1091",
    "Domestic Abuse" : "181",
    "Emergency"      : "112",
    "Child Helpline" : "1098",
    "Cyber Crime"    : "1930",
}

output = {
    "universal": UNIVERSAL,
    "by_state" : HELPLINES,
}

with open(f"{OUT_DIR}/women_helplines.json", "w") as f:
    json.dump(output, f, indent=2)
print(f"✅  women_helplines.json     ({len(HELPLINES)} states + universal numbers)")
