with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add station dots to the BKK map
# Find the end of renderDistrictWaterMap where it fits bounds
old_bkk_end = "if($('showShelterPins').checked)addShelterPins(layers,currentShelters);\n map.stop();"

new_bkk_end = """if($('showShelterPins').checked)addShelterPins(layers,currentShelters);
 currentStations.forEach(r=>{
  if(typeof r.latitude!=='number'||typeof r.longitude!=='number')return;
  let q=quality(r),status=canonicalWaterStatus(r.flood_status_source),c=q!=='ภายใน 24 ชั่วโมง'?'#75858b':(WATER_STATUS[status]?WATER_STATUS[status].color:'#ffffff');
  L.circleMarker([r.latitude,r.longitude],{radius: 2.5,fillColor:c,color:'#fff',weight:0.5,fillOpacity:1}).bindPopup(`<b>${esc(r.station_name)}</b><br>${esc(r.district_or_area)}<br>ระดับน้ำ ${esc(r.water_in_m_msl)} ม. รทก.<br>${esc(r.flood_status_source)} · ${esc(q)}<br>${time(r.observed_at_th)}`).addTo(layers);
 });
 map.stop();"""

content = content.replace(old_bkk_end, new_bkk_end)

with open('outputs/flood_web/template.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Added station dots to BKK map")
