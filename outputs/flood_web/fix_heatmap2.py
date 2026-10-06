with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add leaflet.heat CDN after the leaflet CSS
old_head = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">'
new_head = '''<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>'''
# But first check if leaflet JS is already inline or via CDN
import re

# Add leaflet.heat ONLY — leaflet may already be embedded inline
# Add before </head>
old_close_head = '</style>'
# Look for the first occurrence
idx = html.find('</style>')
# Instead add script right before <script> block
main_script_idx = html.find('<script>')

leaflet_heat_tag = '<script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>'
leaflet_js_tag = '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'

# Check if leaflet JS CDN is in the html
if 'leaflet.js' not in html:
    # Add both before <script>
    html = html[:main_script_idx] + leaflet_js_tag + '\n' + leaflet_heat_tag + '\n' + html[main_script_idx:]
else:
    # Just add heat after leaflet.js
    leaflet_js_end = html.find('leaflet.js">')
    insert_after = html.find('>', leaflet_js_end) + 1
    html = html[:insert_after] + '\n' + leaflet_heat_tag + html[insert_after:]

print("Added leaflet.heat")

# 2. Map severity rank to intensity 0..1
# WATER_STATUS rank: ล้นตลิ่ง=5, วิกฤต=4, เตือนภัย=3, เฝ้าระวัง=2, ปกติ=1, unknown=0
# Remove all old station circleMarker loops (both inside renderDistrictWaterMap and renderMap)

# 2a. In renderDistrictWaterMap: remove the currentStations.forEach block that draws circles
old_bkk_dots = '''currentStations.forEach(r=>{
  if(typeof r.latitude!=='number'||typeof r.longitude!=='number')return;
  let q=quality(r),status=canonicalWaterStatus(r.flood_status_source),c=q!=='ภายใน 24 ชั่วโมง'?'#75858b':(WATER_STATUS[status]?WATER_STATUS[status].color:'#ffffff');
  L.circleMarker([r.latitude,r.longitude],{radius:12,fillColor:c,color:'transparent',weight:0,fillOpacity:c==='transparent'?0:0.65}).bindPopup(`<b>${esc(r.station_name)}</b><br>${esc(r.district_or_area)}<br>ระดับน้ำ ${esc(r.water_in_m_msl)} ม. รทก.<br>${esc(r.flood_status_source)} · ${esc(q)}<br>${time(r.observed_at_th)}`).addTo(layers);
 });'''

new_bkk_dots = '''// heatmap drawn below'''

html = html.replace(old_bkk_dots, new_bkk_dots)

# 2b. Find and replace the national map circleMarker forEach
old_national_dots = re.search(
    r"const pts=\[\];currentStations\.forEach\(r=>\{if\(typeof r\.latitude.*?renderShelterMap\(\);\}",
    html, re.DOTALL
)
if old_national_dots:
    old_block = old_national_dots.group(0)
    new_block = old_block.replace(
        r"L.circleMarker([r.latitude,r.longitude],{radius:12,fillColor:c,color:'transparent',weight:0,fillOpacity:c==='transparent'?0:0.65})",
        r"L.circleMarker([r.latitude,r.longitude],{radius:5,fillColor:c,color:c==='transparent'?'#aaa':'#333',weight:0.5,fillOpacity:c==='transparent'?0:0.8})"
    )
    # Also add heatmap layer rendering at the end of national map
    new_block = new_block[:-1] + '''
  // Draw heatmap for stations
  if(window.L && L.heatLayer){
    const heatData=currentStations.filter(r=>typeof r.latitude==='number'&&typeof r.longitude==='number').map(r=>{
      const status=canonicalWaterStatus(r.flood_status_source),q=quality(r);
      const rank=WATER_STATUS[status]?.rank||0;
      const intensity=q!=='ภายใน 24 ชั่วโมง'?0:rank/5;
      return [r.latitude,r.longitude,intensity];
    }).filter(d=>d[2]>0);
    L.heatLayer(heatData,{radius:30,blur:20,maxZoom:12,max:1.0,gradient:{0.2:'#3b82f6',0.4:'#22c55e',0.6:'#facc15',0.8:'#f97316',1.0:'#9333ea'}}).addTo(layers);
  }
}'''
    html = html.replace(old_block, new_block)
    print("Replaced national map dots + added heatmap")
else:
    print("Could not find national map forEach block")

# 3. Update renderDistrictWaterMap to add heatmap (after the map.stop() etc.)
# Add heatmap layer at the end of renderDistrictWaterMap
old_bkk_end = " map.stop();map.invalidateSize({animate:false});map.fitBounds((selected||area).getBounds(),{padding:[24,24],maxZoom:13,animate:false});"
new_bkk_end = """ // Draw heatmap for BKK stations
 if(window.L && L.heatLayer){
   const heatData=currentStations.filter(r=>typeof r.latitude==='number'&&typeof r.longitude==='number').map(r=>{
     const status=canonicalWaterStatus(r.flood_status_source),q=quality(r);
     const rank=WATER_STATUS[status]?.rank||0;
     const intensity=q!=='ภายใน 24 ชั่วโมง'?0:rank/5;
     return [r.latitude,r.longitude,intensity];
   }).filter(d=>d[2]>0);
   if(heatData.length) L.heatLayer(heatData,{radius:35,blur:25,maxZoom:14,max:1.0,gradient:{0.2:'#3b82f6',0.4:'#22c55e',0.6:'#facc15',0.8:'#f97316',1.0:'#9333ea'}}).addTo(layers);
 }
 map.stop();map.invalidateSize({animate:false});map.fitBounds((selected||area).getBounds(),{padding:[24,24],maxZoom:13,animate:false});"""

html = html.replace(old_bkk_end, new_bkk_end)

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done")
