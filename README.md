
---

Crime Analysis Dashboard

A data-driven web application that analyzes and visualizes crime data across India (2001–2012) using an interactive map and dashboard.


---

Overview

India Crime Atlas converts raw NCRB district-wise IPC crime data into meaningful insights through a combination of data processing and web visualization.

The project includes:

State-wise crime analysis

Interactive choropleth map

Crime ranking by state and district

Women safety insights and helplines

A complete data pipeline for reproducibility



---

Features

Interactive Crime Map

Built using Leaflet.js

Displays state-wise crime distribution

Hover to preview data, click to open dashboard

Source: 


State Dashboard

Displays:

Helplines

Top crimes

Women safety data


Dynamic state selection via URL

Source: 


Women Safety Analysis

Extracts major crime categories against women:

Rape

Dowry deaths

Domestic violence


Includes both universal and state-specific helplines

Source: 


Data Pipeline

Automated pipeline to process raw data and generate outputs.

Run everything using:




Pipeline steps:

1. Data cleaning


2. State-level aggregation


3. Top crime extraction


4. Women safety analysis


5. Map generation


6. Dashboard bundling




---

Project Structure

.
├── data_pipeline/
│   ├── 01_clean_data.py
│   ├── 02_state_summary.py
│   ├── 03_top_crimes.py
│   ├── 04_women_safety.py
│   ├── 05_generate_map.py
│   ├── 06_bundle_dashboard.py
│   └── run_pipeline.py
│
├── cleaned/
├── processed/
├── dashboard_data.json
├── india_crime_map.html
├── index.html
└── india_states.geojson


---

Installation

1. Clone the repository:



git clone https://github.com/your-username/india-crime-atlas.git
cd india-crime-atlas

2. Install dependencies:



pip install pandas folium


---

Usage

Run Data Pipeline

cd data_pipeline
python run_pipeline.py

This will generate:

Cleaned dataset

Processed JSON files

Interactive map

Dashboard data bundle


Open the Application

Open india_crime_map.html in a browser

Click on any state to view detailed dashboard



---

Data Source

NCRB District-wise IPC Crimes Dataset (2001–2012)



---

Technologies Used

Backend:

Python

Pandas

Folium


Frontend:

HTML

CSS

JavaScript

Leaflet.js



---

Novelty

Combines data engineering and frontend visualization in a single pipeline

Provides both macro (state-level) and micro (district-level) insights

Integrates women safety analytics with actionable helpline data

Uses a single bundled JSON (dashboard_data.json) for efficient frontend loading



---

Future Improvements

Real-time data integration

Predictive crime analysis using machine learning

Mobile responsiveness improvements

Advanced filtering and search
