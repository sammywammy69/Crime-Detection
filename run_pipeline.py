"""
run_pipeline.py
---------------
Master runner — executes the full data pipeline in order.
Run this once to regenerate all processed files and the map.

Usage:
    cd data_pipeline
    python run_pipeline.py

Requirements:
    pip install pandas folium
"""

import subprocess, sys, time

SCRIPTS = [
    ("01_clean_data.py",       "Clean & normalise raw CSV"),
    ("02_state_summary.py",    "Compute state safety scores & yearly trends"),
    ("03_top_crimes.py",       "Rank top crimes by state & district"),
    ("04_women_safety.py",     "Extract women crime data & helplines"),
    ("05_generate_map.py",     "Generate Folium choropleth map"),
    ("06_bundle_dashboard.py", "Bundle all JSON into dashboard_data.json"),
]

print("=" * 58)
print("  India Crime Atlas — Data Pipeline")
print("=" * 58)

total_start = time.time()
for script, desc in SCRIPTS:
    print(f"\n▶  {desc}")
    print(f"   Running {script} …")
    t0 = time.time()
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    elapsed = time.time() - t0
    if result.returncode != 0:
        print(f"   ❌  ERROR in {script}:\n{result.stderr}")
        sys.exit(1)
    for line in result.stdout.strip().splitlines():
        print(f"   {line}")
    print(f"   ⏱  {elapsed:.2f}s")

print("\n" + "=" * 58)
print(f"  Pipeline complete in {time.time() - total_start:.1f}s")
print("  Outputs:")
print("    data_pipeline/cleaned/crimes_clean.csv")
print("    data_pipeline/processed/*.json   (7 files)")
print("    india_crime_map.html")
print("    dashboard_data.json")
print("=" * 58)
