import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_str = """function renderShelterMap(){
 if(state.tab!=='bkk'||!window.L)return;
 if(!shelterMap){shelterMap=L.map('shelterMap',{scrollWheelZoom:false}).setView([13.75,100.55],10);shelterLayers=L.layerGroup().addTo(shelterMap)}
 shelterLayers.clearLayers();
 $('shelterMapLegend2').innerHTML=districtWaterLegendHTML();
 $('shelterStatusLegend').innerHTML=shelterLegend();

 if(!window.BKK_DISTRICTS_GEOJSON) { shelterMap.setView([13.75,100.55],10); return; }
 const waterRows=DATA.bkkStations.filter(r=>r.province==='กรุงเทพมหานคร');
 const activeStatuses=new Set(waterRows.map(r=>canonicalWaterStatus(r.flood_status_source)));
 const distSummaries=new Map();
 const heatData=waterRows.filter(r=>typeof r.latitude==='number'&&typeof r.longitude==='number').map(r=>{
   const st=canonicalWaterStatus(r.flood_status_source), q=quality(r);
   const rank=WATER_STATUS[st]?.rank||0;
   const maxRank = Math.max(...waterRows.filter(r=>quality(r)==='ภายใน 24 ชั่วโมง').map(r=>WATER_STATUS[canonicalWaterStatus(r.flood_status_source)]?.rank||1));
   return [r.latitude,r.longitude,q!=='ภายใน 24 ชั่วโมง'?0:rank/maxRank];
 }).filter(d=>d[2]>0);
 
 if(heatData.length && L.heatLayer) L.heatLayer(heatData,{radius:40,blur:20,maxZoom:14,max:1.0,minOpacity:0.05,gradient:{.3:'#93c5fd',.5:'#3b82f6',.7:'#1d4ed8',1:'#082f6b'}}).addTo(shelterLayers);

 L.geoJSON(window.BKK_DISTRICTS_GEOJSON, {
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
 }).addTo(shelterLayers);

 const getStatus = r => { let s=String(r.status_source||'').trim(); return s==='เปิดให้บริการ/ว่าง'?'ว่าง':s==='ใกล้เต็ม'?'ใกล้เต็ม':s==='เต็ม'?'เต็ม':'ไม่ทราบ'; };
 const bkkShelters = DATA.shelters.filter(r=>(!state.district||r.district===state.district));
 const allowedStatuses = new Set(Array.from(document.querySelectorAll('.shelter-filter:checked')).map(cb=>cb.dataset.filter));
 const filteredShelters = bkkShelters.filter(r=>allowedStatuses.has(getStatus(r)));"""

new_str = """const getShelterStatus = r => { let s=String(r.status_source||'').trim(); return s==='เปิดให้บริการ/ว่าง'?'ว่าง':s==='ใกล้เต็ม'?'ใกล้เต็ม':s==='เต็ม'?'เต็ม':'ไม่ทราบ'; };

function renderShelterMap(){
 if(state.tab!=='bkk'||!window.L)return;
 if(!shelterMap){shelterMap=L.map('shelterMap',{scrollWheelZoom:false}).setView([13.75,100.55],10);shelterLayers=L.layerGroup().addTo(shelterMap)}
 shelterLayers.clearLayers();
 $('shelterMapLegend2').innerHTML=districtWaterLegendHTML();
 $('shelterStatusLegend').innerHTML=shelterLegend();

 if(!window.BKK_DISTRICTS_GEOJSON) { shelterMap.setView([13.75,100.55],10); return; }
 const waterRows=DATA.bkkStations.filter(r=>r.province==='กรุงเทพมหานคร');
 const activeStatuses=new Set(waterRows.map(r=>canonicalWaterStatus(r.flood_status_source)));
 const distSummaries=new Map();
 const heatData=waterRows.filter(r=>typeof r.latitude==='number'&&typeof r.longitude==='number').map(r=>{
   const st=canonicalWaterStatus(r.flood_status_source), q=quality(r);
   const rank=WATER_STATUS[st]?.rank||0;
   const maxRank = Math.max(...waterRows.filter(r=>quality(r)==='ภายใน 24 ชั่วโมง').map(r=>WATER_STATUS[canonicalWaterStatus(r.flood_status_source)]?.rank||1));
   return [r.latitude,r.longitude,q!=='ภายใน 24 ชั่วโมง'?0:rank/maxRank];
 }).filter(d=>d[2]>0);
 
 if(heatData.length && L.heatLayer) L.heatLayer(heatData,{radius:40,blur:20,maxZoom:14,max:1.0,minOpacity:0.05,gradient:{.3:'#93c5fd',.5:'#3b82f6',.7:'#1d4ed8',1:'#082f6b'}}).addTo(shelterLayers);

 L.geoJSON(window.BKK_DISTRICTS_GEOJSON, {
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
 }).addTo(shelterLayers);

 const bkkShelters = DATA.shelters.filter(r=>(!state.district||r.district===state.district));
 const allowedStatuses = new Set(Array.from(document.querySelectorAll('.shelter-filter:checked')).map(cb=>cb.dataset.filter));
 const filteredShelters = bkkShelters.filter(r=>allowedStatuses.has(getShelterStatus(r)));"""

html = html.replace(old_str, new_str)
html = html.replace('getStatus(', 'getShelterStatus(')

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Fixed getShelterStatus scope")
