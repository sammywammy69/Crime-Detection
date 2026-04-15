# India Crime Atlas
## Overview
**India Crime Atlas** is an end-to-end data pipeline and interactive web dashboard designed to visualize district-wise IPC (Indian Penal Code) crimes from 2001 to 2012. Using National Crime Records Bureau (NCRB) data, this tool generates a comprehensive choropleth map of India and provides detailed, state-by-state breakdowns of criminal activity, with a dedicated focus on women's safety.
## Key Features
 * **Interactive Choropleth Map:** A dark-themed, responsive map powered by Leaflet and Folium, visualizing state safety scores and total crime volumes.
 * **Deep-Dive Dashboards:** Click on any state to open a specialized dashboard (index.html) displaying the state's top IPC crimes, women's safety statistics, and critical emergency helplines.
 * **Automated Data Pipeline:** A robust, modular Python pipeline that cleans raw CSV data, computes regional summaries, and bundles the outputs into lightweight JSON files for the frontend.
 * **Women's Safety Focus:** Dedicated data extraction for crimes against women, paired with a curated database of universal and state-specific emergency helplines.
## Tech Stack
 * **Data Processing:** Python 3, pandas
 * **Geospatial Visualization:** folium, GeoJSON
 * **Frontend:** HTML5, CSS3, Vanilla JavaScript, Leaflet.js
## Project Structure
The project is split into an automated backend data pipeline and a static frontend architecture.
### 1. Data Pipeline
Execute the master runner (run_pipeline.py) to run the scripts in sequence:
 * 01_clean_data.py: Normalizes raw NCRB data, standardizes state names, and outputs cleaned/crimes_clean.csv.
 * 02_state_summary.py: Computes safety scores, state ranks, and yearly crime trends.
 * 03_top_crimes.py: Aggregates the top 5 distinct IPC crimes per state and district.
 * 04_women_safety.py: Extracts statistics specifically related to crimes against women and maps emergency helplines.
 * 05_generate_map.py: Combines data with india_states.geojson to build the interactive india_crime_map.html.
 * 06_bundle_dashboard.py: Packages all individual JSON outputs into a single, compact dashboard_data.json to minimize browser fetch requests.
### 2. Frontend
 * india_crime_map.html: The primary entry point. A full-screen interactive map that previews state data on hover and links to the detailed dashboard on click.
 * index.html: The state-specific detail view, parsing URL parameters to display relevant dashboard_data.json records in a highly stylized neon-cyberpunk UI.
## Installation & Usage
### Prerequisites
 * Python 3.7+
 * The raw dataset: 01_District_wise_crimes_committed_IPC_2001_2012.csv (placed in the root or parent directory as specified).
 * Geospatial boundaries: india_states.geojson.
### Setup
**1. Clone the repository and navigate to the pipeline directory:**
```bash
git clone <your-repo-url>
cd data_pipeline

```
**2. Install Python dependencies:**
```bash
pip install pandas folium

```
**3. Run the master data pippeline:**
```bash
python run_pipeline.py

```
*This command will process the raw dataset, generate all JSON files, map outputs, and the final dashboard bundle. Wait for the success confirmation in the terminal.*
**4. Launch the application:**
Simply open india_crime_map.html in your web browser. No local web server is required, but you can use Live Server or Python's http.server if you prefer:
```bash
python -m http.server 8000

```
Then navigate to http://localhost:8000/india_crime_map.html.
