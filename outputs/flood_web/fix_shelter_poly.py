import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_str = """ L.geoJSON(window.BKK_DISTRICTS_GEOJSON, {
   style: f => {
     const d=f.properties.dname, rs=waterRows.filter(r=>r.district_or_area===d);
     const sum=districtWaterSummary(rs);
     distSummaries.set(d, sum);
     return {fillColor:sum.color,fillOpacity:state.district&&state.district!==d?0.05:0.25,color:sum.color,weight:2,opacity:state.district&&state.district!==d?0.1:0.8};
   },
   onEachFeature: (f,l) => {
     const d=f.properties.dname, sum=distSummaries.get(d);
     l.bindTooltip(`<b>เขต${esc(d)}</b><br>${sum.drivers.length?`สถานีวิกฤต/เตือนภัยสูงสุด: ${esc(sum.status)} (${sum.drivers.length} แห่ง)`:`จุดวัดน้ำ: ${sum.status||'ไม่มี'}`}`);
     l.on('click', ()=> { state.district=state.district===d?'':d; $('district').value=state.district; render(); window.scrollTo({top:0,behavior:'smooth'}); });
   }
 }).addTo(shelterLayers);"""

new_str = """
 for(const name of districts)distSummaries.set(name,districtWaterSummary(waterRows.filter(r=>String(r.district_or_area??'').replace(/^เขต/,'').trim()===name&&quality(r)==='ภายใน 24 ชั่วโมง')));
 L.geoJSON(window.BKK_DISTRICTS_GEOJSON, {
   style(feature){const name=feature.properties.amp_th,summary=distSummaries.get(name)||districtWaterSummary([]),active=!state.district||state.district===name;return {className:'bkk-district',color:summary.status?summary.color:(active?'#334155':'#94a3b8'),weight:summary.status?3:(state.district===name?2.5:1),fillColor:'transparent',fillOpacity:0}},
   onEachFeature(feature,layer){
    const name=feature.properties.amp_th,summary=distSummaries.get(name)||districtWaterSummary([]);
    layer.bindTooltip(`<b>เขต${esc(name)}</b><br>${summary.drivers.length?`สถานีวิกฤต/เตือนภัยสูงสุด: ${esc(summary.status)} (${summary.drivers.length} แห่ง)`:`จุดวัดน้ำ: ${summary.status||'ไม่มีข้อมูลผ่านเกณฑ์'}`}`);
    layer.on('click',()=>{state.district=state.district===name?'':name;$('district').value=state.district;render()});
   }
 }).addTo(shelterLayers);
"""

if old_str in html:
    html = html.replace(old_str, new_str)
    print("Fixed polygon logic!")
else:
    print("Could not find polygon logic!")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
