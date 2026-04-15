"""
05_generate_map.py
------------------
Reads processed/state_summary.json and india_states.geojson to build
an interactive Folium choropleth map of India coloured by Safety Score.

Each state tooltip shows:
  • State name
  • Safety Score
  • Total IPC crimes (2001–2012)

Output: ../india_crime_map.html
"""

import folium
import json
import pandas as pd

SUMMARY_JSON  = "processed/state_summary.json"
GEOJSON_FILE  = "../india_states.geojson"
OUTPUT_HTML   = "../india_crime_map.html"

# ── 1. Load data ─────────────────────────────────────────────────────────────
with open(SUMMARY_JSON) as f:
    summary = json.load(f)

df = pd.DataFrame(summary)

with open(GEOJSON_FILE, encoding="utf-8") as f:
    geojson_data = json.load(f)

# ── 2. Build lookup for tooltips ─────────────────────────────────────────────
lookup = {row["state"]: row for row in summary}

# Attach stats to each GeoJSON feature for tooltip
for feat in geojson_data["features"]:
    name = feat["properties"].get("ST_NM", "")
    info = lookup.get(name, {})
    feat["properties"]["Safety_Score"] = info.get("safety_score", "N/A")
    feat["properties"]["Total_Crimes"]  = f"{info.get('total_crimes', 0):,}"
    feat["properties"]["Rank"]          = info.get("rank", "N/A")

# ── 3. Create map ────────────────────────────────────────────────────────────
m = folium.Map(
    location=[22.5, 78.9],
    zoom_start=5,
    tiles="cartodb dark_matter",
)

# Choropleth layer
folium.Choropleth(
    geo_data=geojson_data,
    data=df,
    columns=["state", "safety_score"],
    key_on="feature.properties.ST_NM",
    fill_color="RdYlGn",      # red = unsafe, green = safe
    fill_opacity=0.78,
    line_opacity=0.25,
    legend_name="Safety Score  (100 = safest)",
    nan_fill_color="#1a1a2e",
).add_to(m)

# Invisible overlay for rich tooltips
folium.GeoJson(
    geojson_data,
    style_function=lambda x: {"fillOpacity": 0, "weight": 0.4, "color": "#ffffff22"},
    tooltip=folium.GeoJsonTooltip(
        fields=["ST_NM", "Safety_Score", "Total_Crimes", "Rank"],
        aliases=["State", "Safety Score", "Total Crimes (2001–12)", "Crime Rank"],
        localize=True,
        sticky=False,
        style="""
            background-color: #05050f;
            color: #e8e8f0;
            font-family: 'Exo 2', sans-serif;
            font-size: 13px;
            border: 1px solid #ff2244;
            border-radius: 8px;
            padding: 8px 12px;
        """,
    ),
    highlight_function=lambda x: {"fillOpacity": 0.15, "weight": 1.5, "color": "#ff2244"},
).add_to(m)

# ── 4. Save ──────────────────────────────────────────────────────────────────
m.save(OUTPUT_HTML)
print(f"✅  Choropleth map saved → {OUTPUT_HTML}")
print(f"    States mapped: {len(df)}  |  Score range: {df['safety_score'].min()}–{df['safety_score'].max()}")
