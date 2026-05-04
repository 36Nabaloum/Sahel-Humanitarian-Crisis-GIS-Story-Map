"""
generate_gis_data.py
Generates realistic GIS datasets for the Sahel Story Map.
Outputs: regions.json, incidents.json, needs.json, response.json
"""
import json, random, math
random.seed(2025)

# Real approximate centroids for Sahel regions
REGIONS = [
    # Burkina Faso
    {"id":"BF-SAH","name":"Sahel","country":"Burkina Faso","lat":14.30,"lon":-0.35,"area_km2":25719,"pop":1430000},
    {"id":"BF-NOR","name":"Nord","country":"Burkina Faso","lat":13.70,"lon":-2.20,"area_km2":16238,"pop":1430000},
    {"id":"BF-EST","name":"Est","country":"Burkina Faso","lat":12.30,"lon":0.90,"area_km2":46694,"pop":1580000},
    {"id":"BF-CEN","name":"Centre","country":"Burkina Faso","lat":12.37,"lon":-1.53,"area_km2":1464,"pop":2400000},
    {"id":"BF-CAS","name":"Cascades","country":"Burkina Faso","lat":10.40,"lon":-4.30,"area_km2":18768,"pop":770000},
    # Mali
    {"id":"ML-MOP","name":"Mopti","country":"Mali","lat":14.50,"lon":-3.90,"area_km2":79017,"pop":2560000},
    {"id":"ML-GAO","name":"Gao","country":"Mali","lat":16.27,"lon":1.63,"area_km2":170572,"pop":630000},
    {"id":"ML-TOM","name":"Tombouctou","country":"Mali","lat":16.77,"lon":-3.00,"area_km2":496611,"pop":680000},
    {"id":"ML-SEG","name":"Ségou","country":"Mali","lat":13.45,"lon":-6.27,"area_km2":64821,"pop":2570000},
    {"id":"ML-BAM","name":"Bamako","country":"Mali","lat":12.65,"lon":-8.00,"area_km2":267,"pop":3600000},
    # Niger
    {"id":"NE-DIF","name":"Diffa","country":"Niger","lat":13.32,"lon":12.62,"area_km2":156906,"pop":650000},
    {"id":"NE-ZIN","name":"Zinder","country":"Niger","lat":13.80,"lon":8.97,"area_km2":145430,"pop":3860000},
    {"id":"NE-MAR","name":"Maradi","country":"Niger","lat":13.50,"lon":7.10,"area_km2":41796,"pop":4620000},
    {"id":"NE-AGA","name":"Agadez","country":"Niger","lat":18.99,"lon":8.00,"area_km2":667799,"pop":610000},
    {"id":"NE-NIA","name":"Niamey","country":"Niger","lat":13.51,"lon":2.12,"area_km2":670,"pop":1580000},
    # Chad
    {"id":"TD-LAC","name":"Lac","country":"Chad","lat":13.18,"lon":14.10,"area_km2":22320,"pop":450000},
    {"id":"TD-OUA","name":"Ouaddaï","country":"Chad","lat":13.85,"lon":21.40,"area_km2":76240,"pop":730000},
    {"id":"TD-NDJ","name":"N'Djaména","country":"Chad","lat":12.13,"lon":15.05,"area_km2":900,"pop":1700000},
    {"id":"TD-BOR","name":"Borkou","country":"Chad","lat":18.50,"lon":18.00,"area_km2":100000,"pop":110000},
    {"id":"TD-KAN","name":"Kanem","country":"Chad","lat":15.00,"lon":15.50,"area_km2":114520,"pop":520000},
]

INCIDENT_TYPES = ["Armed Conflict","IED Attack","Banditry","Kidnapping",
                   "Intercommunal Violence","Flood","Drought","Disease Outbreak"]
SEVERITIES     = ["Low","Medium","High","Critical"]
SECTORS        = ["Nutrition","WASH","Shelter","Protection","Health","Food Security"]
DONORS         = ["USAID","UNICEF","OCHA","BHA","NORAD","EU","WFP"]
ORGS           = ["IRC","ACF","MSF","WFP","UNICEF","OCHA","SPONG","Save the Children"]

# ── 1. Region-level humanitarian needs ───────────────────────
region_needs = []
for r in REGIONS:
    idp_count  = random.randint(5000, 280000)
    need_score = round(random.uniform(2.5, 9.5), 1)
    region_needs.append({
        **r,
        "idp_count":       idp_count,
        "refugee_count":   random.randint(0, 80000),
        "pct_in_need":     round(random.uniform(0.30, 0.92), 2),
        "food_insec_pct":  round(random.uniform(0.25, 0.85), 2),
        "sam_rate":        round(random.uniform(0.08, 0.42), 3),
        "water_access_pct":round(random.uniform(0.20, 0.78), 2),
        "need_score":      need_score,    # 1-10 composite
        "priority_tier":   ("Critical" if need_score >= 8
                            else "High"    if need_score >= 6
                            else "Medium"  if need_score >= 4
                            else "Low"),
        "top_sector":      random.choice(SECTORS),
        "lead_agency":     random.choice(ORGS),
    })

with open("data/region_needs.json","w") as f:
    json.dump(region_needs, f, indent=2)

# ── 2. Security incidents (point layer) ──────────────────────
incidents = []
for i in range(180):
    r    = random.choice(REGIONS)
    dlat = random.gauss(0, 1.2)
    dlon = random.gauss(0, 1.2)
    inc_type = random.choices(
        INCIDENT_TYPES,
        weights=[30,12,18,8,14,10,5,3]
    )[0]
    fatalities = (0 if inc_type not in ["Armed Conflict","IED Attack","Intercommunal Violence"]
                  else random.randint(0, 24))
    incidents.append({
        "id":           f"INC-{i+1:04d}",
        "lat":          round(r["lat"] + dlat, 4),
        "lon":          round(r["lon"] + dlon, 4),
        "country":      r["country"],
        "region":       r["name"],
        "type":         inc_type,
        "severity":     random.choices(SEVERITIES, weights=[25,40,25,10])[0],
        "fatalities":   fatalities,
        "displaced":    random.randint(0, 8000) if inc_type in
                        ["Armed Conflict","Flood","Intercommunal Violence"] else 0,
        "date":         f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
        "source":       random.choice(["ACLED","OCHA","ReliefWeb","Local Authority"]),
    })

with open("data/incidents.json","w") as f:
    json.dump(incidents, f, indent=2)

# ── 3. Humanitarian response points (organisation presence) ──
response_points = []
for i in range(120):
    r      = random.choice(REGIONS)
    org    = random.choice(ORGS)
    sector = random.choice(SECTORS)
    donor  = random.choice(DONORS)
    bens   = random.randint(500, 45000)
    response_points.append({
        "id":           f"RESP-{i+1:04d}",
        "lat":          round(r["lat"] + random.gauss(0, 0.6), 4),
        "lon":          round(r["lon"] + random.gauss(0, 0.6), 4),
        "country":      r["country"],
        "region":       r["name"],
        "organization": org,
        "sector":       sector,
        "donor":        donor,
        "beneficiaries":bens,
        "budget_usd":   random.randint(50000, 2000000),
        "status":       random.choices(["Active","Planned","Completed"],
                                        weights=[60,25,15])[0],
        "start_date":   f"2024-{random.randint(1,6):02d}-01",
    })

with open("data/response_points.json","w") as f:
    json.dump(response_points, f, indent=2)

# ── 4. IDP movement flows ─────────────────────────────────────
flows = []
high_need = [r for r in REGIONS if r["id"] in
             ["BF-SAH","BF-EST","ML-MOP","ML-GAO","NE-DIF","TD-LAC"]]
safe_areas = [r for r in REGIONS if r["id"] in
              ["BF-CEN","ML-BAM","NE-NIA","NE-MAR","TD-NDJ"]]

for i in range(30):
    src  = random.choice(high_need)
    dst  = random.choice(safe_areas)
    if src["id"] != dst["id"]:
        flows.append({
            "id":       f"FLOW-{i+1:03d}",
            "from_id":  src["id"],
            "from_name":src["name"],
            "from_country": src["country"],
            "from_lat": src["lat"],
            "from_lon": src["lon"],
            "to_id":    dst["id"],
            "to_name":  dst["name"],
            "to_country": dst["country"],
            "to_lat":   dst["lat"],
            "to_lon":   dst["lon"],
            "displaced_count": random.randint(2000, 65000),
            "peak_month":      f"2024-{random.randint(1,12):02d}",
            "primary_cause":   random.choice(
                ["Armed Conflict","Flood","Drought","Intercommunal Violence"]),
        })

with open("data/idp_flows.json","w") as f:
    json.dump(flows, f, indent=2)

print(f"GIS data generated:")
print(f"  region_needs.json    : {len(region_needs)} regions")
print(f"  incidents.json       : {len(incidents)} incident points")
print(f"  response_points.json : {len(response_points)} response sites")
print(f"  idp_flows.json       : {len(flows)} displacement flows")
