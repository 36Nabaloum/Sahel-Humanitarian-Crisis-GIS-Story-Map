"""
build_map.py — Build Sahel GIS Story Map HTML
Generates a self-contained, GitHub Pages-ready HTML file.
"""
import json, os

os.makedirs("output", exist_ok=True)

with open("data/region_needs.json")    as f: regions   = json.load(f)
with open("data/incidents.json")       as f: incidents = json.load(f)
with open("data/response_points.json") as f: response  = json.load(f)
with open("data/idp_flows.json")       as f: flows     = json.load(f)

regions_js   = json.dumps(regions,   separators=(",",":"))
incidents_js = json.dumps(incidents, separators=(",",":"))
response_js  = json.dumps(response,  separators=(",",":"))
flows_js     = json.dumps(flows,     separators=(",",":"))

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"Segoe UI",system-ui,sans-serif;background:#0d1117;color:#e6edf3}
#app{display:flex;flex-direction:column;height:100vh}
header{background:#1b4332;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;border-bottom:2px solid #40916c}
.hdr-title h1{font-size:17px;font-weight:700;color:#d8f3dc}
.hdr-title p{font-size:11px;color:#95d5b2;margin-top:2px}
.hdr-kpis{display:flex;gap:14px}
.kpi{text-align:center;background:rgba(0,0,0,.3);border-radius:8px;padding:5px 14px}
.kpi .v{font-size:15px;font-weight:700;color:#d8f3dc}
.kpi .l{font-size:9px;color:#95d5b2;text-transform:uppercase;letter-spacing:.6px}
#main{display:flex;flex:1;min-height:0}
#sidebar{width:290px;flex-shrink:0;background:#161b22;border-right:1px solid #30363d;display:flex;flex-direction:column;overflow:hidden}
.tabs{display:flex;border-bottom:1px solid #30363d;flex-shrink:0}
.tb{flex:1;padding:9px 4px;font-size:11px;font-weight:600;border:none;background:transparent;color:#8b949e;cursor:pointer;letter-spacing:.3px}
.tb.on{color:#52c788;border-bottom:2px solid #52c788;background:#0d1117}
.tb:hover:not(.on){color:#e6edf3;background:#21262d}
.tab-body{flex:1;overflow-y:auto;padding:12px}
.pane{display:none}.pane.on{display:block}
.grp{margin-bottom:14px}
.grp h4{font-size:10px;text-transform:uppercase;letter-spacing:.8px;color:#8b949e;margin-bottom:7px;padding-bottom:3px;border-bottom:1px solid #21262d}
.li{display:flex;align-items:center;gap:8px;padding:5px 4px;border-radius:5px;cursor:pointer}
.li:hover{background:#21262d}
.li input{accent-color:#52c788;width:13px;height:13px;cursor:pointer}
.li label{font-size:11.5px;cursor:pointer;flex:1;color:#e6edf3}
.dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.rc{background:#21262d;border-radius:7px;padding:9px 11px;margin-bottom:7px;cursor:pointer;transition:all .2s;border-left:3px solid #52c788}
.rc:hover{background:#2d333b;transform:translateX(2px)}
.rc.critical{border-left-color:#f85149}.rc.high{border-left-color:#f0883e}.rc.medium{border-left-color:#f0c030}
.rc .rn{font-size:11.5px;font-weight:700;color:#e6edf3}.rc .rc2{font-size:10px;color:#8b949e;margin-bottom:4px}
.rc .bw{background:#0d1117;border-radius:3px;height:4px;margin:3px 0}
.rc .bf{height:4px;border-radius:3px;background:#52c788}
.rc.critical .bf{background:#f85149}.rc.high .bf{background:#f0883e}.rc.medium .bf{background:#f0c030}
.rc .rs{display:flex;justify-content:space-between;margin-top:4px;font-size:10px;color:#8b949e}
.lg-blk{margin-bottom:13px}
.lg-blk h5{font-size:10px;color:#8b949e;margin-bottom:5px;text-transform:uppercase;letter-spacing:.5px}
.lg-row{display:flex;align-items:center;gap:7px;margin-bottom:3px;font-size:11px;color:#e6edf3}
.sw{width:13px;height:13px;border-radius:3px;flex-shrink:0}
#map{flex:1;min-height:0}
.leaflet-container{background:#0d1117}
.cpop{min-width:210px}
.ph{font-size:13px;font-weight:700;color:#1b4332;border-bottom:2px solid #40916c;padding-bottom:5px;margin-bottom:7px}
.pr{display:flex;justify-content:space-between;margin-bottom:3px;font-size:11.5px}
.pl{color:#666}.pv{font-weight:600;color:#222}
.pb{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700;margin-top:3px;color:#fff}
#bar{background:#161b22;border-top:1px solid #30363d;padding:6px 16px;font-size:11px;color:#8b949e;flex-shrink:0;display:flex;justify-content:space-between;align-items:center}
"""

JS = """
const REG=REGIONS_DATA, INC=INCIDENTS_DATA, RES=RESPONSE_DATA, FLW=FLOWS_DATA;
const TC={Critical:"#f85149",High:"#f0883e",Medium:"#f0c030",Low:"#52c788"};
const CONF=new Set(["Armed Conflict","IED Attack","Banditry","Kidnapping","Intercommunal Violence"]);
const NAT=new Set(["Flood","Drought","Disease Outbreak"]);
function ic(t){return CONF.has(t)?"#f85149":NAT.has(t)?"#f0c030":"#bc8cff"}
function fmt(n){return n>=1e6?(n/1e6).toFixed(1)+"M":n>=1e3?(n/1e3).toFixed(0)+"k":""+n}
function pct(v){return(v*100).toFixed(0)+"%"}

document.getElementById("kv-idp").textContent =fmt(REG.reduce((s,r)=>s+r.idp_count,0));
document.getElementById("kv-ben").textContent =fmt(RES.reduce((s,r)=>s+r.beneficiaries,0));
document.getElementById("kv-inc").textContent =INC.length;
document.getElementById("kv-crit").textContent=REG.filter(r=>r.priority_tier==="Critical").length;

const map=L.map("map",{center:[14,1.5],zoom:5,minZoom:4,maxZoom:14});
const tiles={
  dark:L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",{attribution:"© CartoDB",maxZoom:19}),
  sat:L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",{attribution:"© Esri",maxZoom:18}),
  osm:L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{attribution:"© OSM",maxZoom:19})
};
tiles.dark.addTo(map);
let curBase=tiles.dark;
window.setBase=n=>{curBase.remove();curBase=tiles[n];curBase.addTo(map);curBase.bringToBack()};

const LG={
  bubbles: L.layerGroup().addTo(map),
  heat:    L.layerGroup(),
  flows:   L.layerGroup().addTo(map),
  conflict:L.layerGroup().addTo(map),
  natural: L.layerGroup().addTo(map),
  other:   L.layerGroup().addTo(map),
  response:L.layerGroup().addTo(map),
};
window.toggleL=n=>{const c=document.getElementById("l-"+n);c&&c.checked?LG[n].addTo(map):LG[n].remove()};

REG.forEach(r=>{
  const rad=Math.max(6,Math.min(36,Math.sqrt(r.idp_count)*0.028));
  const col=TC[r.priority_tier]||"#52c788";
  const m=L.circleMarker([r.lat,r.lon],{radius:rad,fillColor:col,fillOpacity:0.55,color:col,weight:1.5});
  m.bindPopup(`<div class="cpop"><div class="ph">${r.name}, ${r.country}</div>
    <div class="pr"><span class="pl">IDPs</span><span class="pv">${fmt(r.idp_count)}</span></div>
    <div class="pr"><span class="pl">In need</span><span class="pv">${pct(r.pct_in_need)}</span></div>
    <div class="pr"><span class="pl">Food insecurity</span><span class="pv">${pct(r.food_insec_pct)}</span></div>
    <div class="pr"><span class="pl">SAM rate</span><span class="pv">${pct(r.sam_rate)}</span></div>
    <div class="pr"><span class="pl">Water access</span><span class="pv">${pct(r.water_access_pct)}</span></div>
    <div class="pr"><span class="pl">Need score</span><span class="pv">${r.need_score}/10</span></div>
    <span class="pb" style="background:${col}">${r.priority_tier}</span></div>`,{maxWidth:260});
  m.on("mouseover",()=>{document.getElementById("inf").textContent=`${r.name} (${r.country}) — IDPs: ${fmt(r.idp_count)} | Score: ${r.need_score}/10 | ${r.priority_tier}`});
  LG.bubbles.addLayer(m);
});
REG.forEach(r=>{
  const col=r.need_score>=8?"#f85149":r.need_score>=6?"#f0883e":r.need_score>=4?"#f0c030":"#52c788";
  LG.heat.addLayer(L.circleMarker([r.lat,r.lon],{radius:30,fillColor:col,fillOpacity:r.need_score/10*0.35,color:col,weight:1,opacity:0.5}));
});
FLW.forEach(f=>{
  const w=Math.max(1,Math.min(7,Math.sqrt(f.displaced_count/5000)));
  const line=L.polyline([[f.from_lat,f.from_lon],[f.to_lat,f.to_lon]],
    {color:"#79c0ff",weight:w,opacity:0.55,dashArray:f.displaced_count>30000?null:"6,4"});
  line.bindPopup(`<div class="cpop"><div class="ph">Displacement Flow</div>
    <div class="pr"><span class="pl">From</span><span class="pv">${f.from_name}, ${f.from_country}</span></div>
    <div class="pr"><span class="pl">To</span><span class="pv">${f.to_name}, ${f.to_country}</span></div>
    <div class="pr"><span class="pl">Displaced</span><span class="pv">${fmt(f.displaced_count)}</span></div>
    <div class="pr"><span class="pl">Cause</span><span class="pv">${f.primary_cause}</span></div></div>`,{maxWidth:240});
  line.on("mouseover",()=>{document.getElementById("inf").textContent=`Flow: ${f.from_name} → ${f.to_name} | ${fmt(f.displaced_count)} people | ${f.primary_cause}`});
  LG.flows.addLayer(line);
  const ml=(f.from_lat+f.to_lat*2)/3, mn=(f.from_lon+f.to_lon*2)/3;
  LG.flows.addLayer(L.circleMarker([ml,mn],{radius:3,fillColor:"#79c0ff",fillOpacity:0.8,color:"#79c0ff",weight:1}));
});
INC.forEach(i=>{
  const col=ic(i.type);
  const grp=CONF.has(i.type)?"conflict":NAT.has(i.type)?"natural":"other";
  const rad=i.severity==="Critical"?9:i.severity==="High"?7:i.severity==="Medium"?5:3.5;
  const m=L.circleMarker([i.lat,i.lon],{radius:rad,fillColor:col,fillOpacity:0.75,color:"#0d1117",weight:1});
  m.bindPopup(`<div class="cpop"><div class="ph">${i.type}</div>
    <div class="pr"><span class="pl">Location</span><span class="pv">${i.region}, ${i.country}</span></div>
    <div class="pr"><span class="pl">Date</span><span class="pv">${i.date}</span></div>
    <div class="pr"><span class="pl">Severity</span><span class="pv">${i.severity}</span></div>
    ${i.fatalities>0?`<div class="pr"><span class="pl">Fatalities</span><span class="pv">${i.fatalities}</span></div>`:""}
    ${i.displaced>0?`<div class="pr"><span class="pl">Displaced</span><span class="pv">${fmt(i.displaced)}</span></div>`:""}
    <div class="pr"><span class="pl">Source</span><span class="pv">${i.source}</span></div></div>`,{maxWidth:240});
  m.on("mouseover",()=>{document.getElementById("inf").textContent=`[${i.date}] ${i.type} — ${i.region}, ${i.country} | Severity: ${i.severity}${i.fatalities>0?" | Fatalities: "+i.fatalities:""}`});
  LG[grp].addLayer(m);
});
const OC={IRC:"#52c788",ACF:"#79c0ff",MSF:"#f0c030",WFP:"#bc8cff",UNICEF:"#006FCF",OCHA:"#0078AD",SPONG:"#40916c"};
RES.forEach(r=>{
  if(r.status==="Completed")return;
  const col=OC[r.organization]||"#52c788";
  const sz=r.beneficiaries>20000?8:r.beneficiaries>8000?6:4;
  const m=L.circleMarker([r.lat,r.lon],{radius:sz,fillColor:col,fillOpacity:0.85,color:"white",weight:1.2});
  m.bindPopup(`<div class="cpop"><div class="ph">${r.organization} — ${r.sector}</div>
    <div class="pr"><span class="pl">Location</span><span class="pv">${r.region}, ${r.country}</span></div>
    <div class="pr"><span class="pl">Beneficiaries</span><span class="pv">${fmt(r.beneficiaries)}</span></div>
    <div class="pr"><span class="pl">Budget</span><span class="pv">$${fmt(r.budget_usd)}</span></div>
    <div class="pr"><span class="pl">Donor</span><span class="pv">${r.donor}</span></div>
    <div class="pr"><span class="pl">Status</span><span class="pv">${r.status}</span></div></div>`,{maxWidth:240});
  m.on("mouseover",()=>{document.getElementById("inf").textContent=`${r.organization} | ${r.sector} | ${r.region}, ${r.country} | ${fmt(r.beneficiaries)} beneficiaries`});
  LG.response.addLayer(m);
});

const sorted=[...REG].sort((a,b)=>b.need_score-a.need_score);
const list=document.getElementById("rlist");
sorted.forEach(r=>{
  const div=document.createElement("div");
  div.className="rc "+(r.priority_tier.toLowerCase());
  div.innerHTML=`<div class="rn">${r.name}</div><div class="rc2">${r.country}</div>
    <div class="bw"><div class="bf" style="width:${r.need_score*10}%"></div></div>
    <div class="rs"><span>IDPs: ${fmt(r.idp_count)}</span><span>Score: ${r.need_score}/10</span></div>`;
  div.onclick=()=>{map.flyTo([r.lat,r.lon],7,{duration:1.2});showTab("layers")};
  list.appendChild(div);
});

window.showTab=n=>{
  document.querySelectorAll(".tb").forEach((b,i)=>{
    ["layers","regions","legend"].forEach((t,j)=>{if(j===i)b.classList.toggle("on",t===n)});
  });
  document.querySelectorAll(".pane").forEach(p=>p.classList.toggle("on",p.id==="p-"+n));
};
"""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sahel Humanitarian Crisis — GIS Story Map | NABALOUM Emile</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="app">
<header>
  <div class="hdr-title">
    <h1>&#127758; Sahel Humanitarian Crisis &mdash; GIS Story Map</h1>
    <p>Interactive needs mapping &amp; response tracking | 4 countries &middot; 20 regions | NABALOUM Emile</p>
  </div>
  <div class="hdr-kpis">
    <div class="kpi"><div class="v" id="kv-idp">&mdash;</div><div class="l">IDPs</div></div>
    <div class="kpi"><div class="v" id="kv-ben">&mdash;</div><div class="l">Beneficiaries</div></div>
    <div class="kpi"><div class="v" id="kv-inc">&mdash;</div><div class="l">Incidents</div></div>
    <div class="kpi"><div class="v" id="kv-crit">&mdash;</div><div class="l">Critical Regions</div></div>
  </div>
</header>
<div id="main">
  <div id="sidebar">
    <div class="tabs">
      <button class="tb on" onclick="showTab('layers')">LAYERS</button>
      <button class="tb" onclick="showTab('regions')">REGIONS</button>
      <button class="tb" onclick="showTab('legend')">LEGEND</button>
    </div>
    <div class="tab-body">
      <div class="pane on" id="p-layers">
        <div class="grp">
          <h4>Needs &amp; Context</h4>
          <div class="li"><input type="checkbox" id="l-bubbles" checked onchange="toggleL('bubbles')"><div class="dot" style="background:#f85149"></div><label for="l-bubbles">IDP Population (bubbles)</label></div>
          <div class="li"><input type="checkbox" id="l-heat" onchange="toggleL('heat')"><div class="dot" style="background:#f0883e"></div><label for="l-heat">Need Score (choropleth)</label></div>
          <div class="li"><input type="checkbox" id="l-flows" checked onchange="toggleL('flows')"><div class="dot" style="background:#79c0ff"></div><label for="l-flows">IDP Displacement Flows</label></div>
        </div>
        <div class="grp">
          <h4>Security Incidents</h4>
          <div class="li"><input type="checkbox" id="l-conflict" checked onchange="toggleL('conflict')"><div class="dot" style="background:#f85149"></div><label for="l-conflict">Armed Conflict / IED</label></div>
          <div class="li"><input type="checkbox" id="l-natural" checked onchange="toggleL('natural')"><div class="dot" style="background:#f0c030"></div><label for="l-natural">Natural Hazards</label></div>
          <div class="li"><input type="checkbox" id="l-other" checked onchange="toggleL('other')"><div class="dot" style="background:#bc8cff"></div><label for="l-other">Other Incidents</label></div>
        </div>
        <div class="grp">
          <h4>Humanitarian Response</h4>
          <div class="li"><input type="checkbox" id="l-response" checked onchange="toggleL('response')"><div class="dot" style="background:#52c788"></div><label for="l-response">Active Response Sites</label></div>
        </div>
        <div class="grp">
          <h4>Base Map</h4>
          <div class="li"><input type="radio" name="bm" value="dark" checked onchange="setBase('dark')"><label>Dark (default)</label></div>
          <div class="li"><input type="radio" name="bm" value="sat" onchange="setBase('sat')"><label>Satellite</label></div>
          <div class="li"><input type="radio" name="bm" value="osm" onchange="setBase('osm')"><label>OpenStreetMap</label></div>
        </div>
      </div>
      <div class="pane" id="p-regions"><div id="rlist"></div></div>
      <div class="pane" id="p-legend">
        <div class="lg-blk">
          <h5>IDP Population (bubble size)</h5>
          <div class="lg-row"><div class="sw" style="background:#f85149;border-radius:50%;width:8px;height:8px"></div>&lt; 20k IDPs</div>
          <div class="lg-row"><div class="sw" style="background:#f85149;border-radius:50%;width:12px;height:12px"></div>20k &ndash; 80k IDPs</div>
          <div class="lg-row"><div class="sw" style="background:#f85149;border-radius:50%;width:18px;height:18px"></div>&gt; 80k IDPs</div>
        </div>
        <div class="lg-blk">
          <h5>Priority Tier (bubble color)</h5>
          <div class="lg-row"><div class="sw" style="background:#f85149"></div>Critical &mdash; Need score &ge; 8</div>
          <div class="lg-row"><div class="sw" style="background:#f0883e"></div>High &mdash; Need score &ge; 6</div>
          <div class="lg-row"><div class="sw" style="background:#f0c030"></div>Medium &mdash; Need score &ge; 4</div>
          <div class="lg-row"><div class="sw" style="background:#52c788"></div>Low &mdash; Need score &lt; 4</div>
        </div>
        <div class="lg-blk">
          <h5>Security Incidents (size = severity)</h5>
          <div class="lg-row"><div class="sw" style="background:#f85149;border-radius:50%"></div>Armed Conflict / IED / Banditry</div>
          <div class="lg-row"><div class="sw" style="background:#f0c030;border-radius:50%"></div>Flood / Drought / Disease</div>
          <div class="lg-row"><div class="sw" style="background:#bc8cff;border-radius:50%"></div>Other incidents</div>
        </div>
        <div class="lg-blk">
          <h5>Response Sites (size = beneficiaries)</h5>
          <div class="lg-row"><div class="sw" style="background:#52c788;border-radius:50%"></div>Active humanitarian site</div>
        </div>
        <div class="lg-blk">
          <h5>IDP Displacement Flows</h5>
          <div class="lg-row"><div style="width:24px;height:3px;background:#79c0ff;border-radius:2px"></div>Movement corridor (width = volume)</div>
        </div>
        <div style="margin-top:14px;padding:10px;background:#21262d;border-radius:8px;font-size:10.5px;color:#8b949e;line-height:1.7">
          <strong style="color:#e6edf3">Data sources</strong><br>
          Simulated from: ACLED, OCHA ReliefWeb,<br>IOM DTM, IRC MEAL System, SPONG/UNICEF<br><br>
          <strong style="color:#e6edf3">Author</strong><br>
          NABALOUM Emile<br>emi.nabaloum@gmail.com<br>
          github.com/nabaloum-emile
        </div>
      </div>
    </div>
  </div>
  <div id="map"></div>
</div>
<div id="bar">
  <span id="inf">Hover over any feature for details | Click for full popup</span>
  <span>&#127758; Sahel GIS Story Map v1.0 &nbsp;&middot;&nbsp; NABALOUM Emile &nbsp;&middot;&nbsp; emi.nabaloum@gmail.com</span>
</div>
</div>
<script>
const REGIONS_DATA={regions_js};
const INCIDENTS_DATA={incidents_js};
const RESPONSE_DATA={response_js};
const FLOWS_DATA={flows_js};
{JS}
</script>
</body>
</html>"""

with open("output/sahel_story_map.html","w",encoding="utf-8") as f:
    f.write(HTML)

size_kb = os.path.getsize("output/sahel_story_map.html") / 1024
print(f"Map generated: output/sahel_story_map.html ({size_kb:.0f} KB)")
print("Self-contained — ready for GitHub Pages, no server needed")
