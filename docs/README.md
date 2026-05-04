# 🗺 Sahel Humanitarian Crisis — GIS Story Map

> **Author:** NABALOUM Emile | emi.nabaloum@gmail.com
> **Stack:** Python · Leaflet.js · HTML/CSS/JS · GeoJSON
> **Live demo:** [nabaloum-emile.github.io/portfolio/project4_gis/](https://github.com)
> **Type:** Single-file HTML — zero server, zero install, GitHub Pages ready

---

## 📌 Overview

An interactive **GIS Story Map** visualising the humanitarian crisis across 4 Sahel countries (Burkina Faso, Mali, Niger, Chad). Built with **Leaflet.js** — a single self-contained HTML file ready for deployment on GitHub Pages.

Replicates the type of geospatial analysis delivered for **SPONG/OCHA** (adopted for emergency planning, 2024–2025).

---

## 🗂 Map Layers

| Layer | Type | Data Points | Description |
|-------|------|-------------|-------------|
| IDP Population | Proportional circles | 20 regions | Bubble size = IDP count, colour = priority tier |
| Need Score | Choropleth circles | 20 regions | Composite humanitarian need (1–10) |
| IDP Displacement Flows | Polylines | 30 flows | Movement corridors, width = volume |
| Security Incidents | Points | 180 events | Armed conflict, natural hazards, other |
| Response Sites | Points | ~100 active | Organisation presence, size = beneficiaries |

---

## 📊 Dataset Summary

| Dataset | Records | Key Fields |
|---------|---------|-----------|
| `region_needs.json` | 20 regions | IDP count, SAM rate, food insecurity, need score, priority tier |
| `incidents.json` | 180 events | Type, severity, fatalities, displaced, date, source |
| `response_points.json` | 120 sites | Organisation, sector, donor, beneficiaries, budget |
| `idp_flows.json` | 30 flows | Origin/destination, displaced count, primary cause |

---

## 🎨 Features

### Interactive Controls
- **Layer toggle checkboxes** — show/hide any layer combination
- **3 base maps** — Dark (default), Satellite, OpenStreetMap
- **Clickable popups** — full data card on click for every feature
- **Hover info bar** — region/incident summary on mouse-over
- **Regions panel** — sorted list with need score bar + fly-to on click
- **Legend panel** — full symbol explanation

### Visual Design
- **Dark theme** — professional humanitarian mapping aesthetic
- **Proportional bubbles** — IDP count drives circle radius
- **Red → Green colour scale** — Critical/High/Medium/Low priority tiers
- **Flow lines** — displacement corridors with variable width
- **Incident severity** — circle size encodes severity level

### Popup Information (example — region bubble)
```
Sahel, Burkina Faso
IDPs:           48k
In need:        78%
Food insec.:    65%
SAM rate:       31%
Water access:   42%
Need score:     8.4/10
[Critical]
```

---

## 🚀 Deployment

### Option 1 — GitHub Pages (recommended)
```bash
# 1. Copy to your repo
cp output/sahel_story_map.html docs/index.html

# 2. Enable GitHub Pages in repo Settings → Pages → Source: docs/
# 3. Your map is live at: https://username.github.io/portfolio/
```

### Option 2 — Local browser
```bash
# Just open the file — no server needed
open output/sahel_story_map.html       # macOS
xdg-open output/sahel_story_map.html   # Linux
start output/sahel_story_map.html      # Windows
```

### Rebuild map (after data changes)
```bash
cd project4_gis
python3 data/generate_gis_data.py   # regenerate datasets
python3 src/build_map.py             # rebuild HTML
```

---

## 📁 File Structure

```
project4_gis/
│
├── src/
│   └── build_map.py            # Map builder — inlines data into HTML
│
├── data/
│   ├── generate_gis_data.py    # Dataset generator
│   ├── region_needs.json       # 20 region-level needs profiles
│   ├── incidents.json          # 180 security/crisis incidents
│   ├── response_points.json    # 120 humanitarian response sites
│   └── idp_flows.json          # 30 IDP displacement flows
│
├── output/
│   └── sahel_story_map.html    # ← DEPLOY THIS FILE (93 KB, self-contained)
│
└── docs/
    └── README.md               # This file
```

---

## 🎯 Real-World Context

This map replicates the type of geospatial analysis that was:
- **Adopted by OCHA Burkina Faso** for emergency planning and resource prioritisation (SPONG, 2024–2025)
- Used in **IRC quarterly reporting** for geographic programme monitoring
- Applied in **MSI/USAID** Sahel MRCS independent monitoring for USAID programme managers

The map covers the 4 main countries of the **G5 Sahel** humanitarian crisis zone, one of the world's fastest-growing humanitarian emergencies.

---

## 🤝 Connect

| Channel | Link |
|---------|------|
| Email | emi.nabaloum@gmail.com |
| LinkedIn | [linkedin.com/in/nabaloum-emile](https://linkedin.com) |
| WhatsApp | +226 67 07 82 76 |

*Part of the [NABALOUM Emile Data Portfolio](../README.md)*
