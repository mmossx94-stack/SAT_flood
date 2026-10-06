import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the HTML to include class "shelter-filter"
old_html = """<input type="checkbox" class="filter-pill-checkbox" data-filter="ว่าง" checked>"""
if old_html in html:
    html = html.replace('class="filter-pill-checkbox" data-filter', 'class="filter-pill-checkbox shelter-filter" data-filter')
    print("Added shelter-filter class")

old_func = """function renderShelterMap(){
 if(state.tab!=='bkk'||!window.L)return;
 if(!shelterMap){shelterMap=L.map('shelterMap',{scrollWheelZoom:false}).setView([13.75,100.55],10);shelterLayers=L.layerGroup().addTo(shelterMap)}
 shelterLayers.clearLayers();
 const boundary=window.PROVINCES_GEOJSON?.features.filter(f=>f.properties.pro_th==='กรุงเทพมหานคร');
 let outline=null;
 if(boundary?.length)outline=L.geoJSON({type:'FeatureCollection',features:boundary},{style:{color:'#627880',weight:1,fill:false},interactive:false}).addTo(shelterLayers);
 const rows=currentShelters.filter(r=>typeof r.latitude==='number'&&typeof r.longitude==='number');
 const pts=addShelterPins(shelterLayers,rows);
 $('shelterStatusLegend').innerHTML=shelterLegend();
 $('shelterMapCount').textContent=fmt(rows.length)+' / '+fmt(currentShelters.length)+' แห่ง มีพิกัด';
 $('shelterMapSubtitle').textContent=(state.district?'เขต'+state.district:'ทุกเขต กทม.')+' · '+(currentShelters.length?rows.length?'แสดงเฉพาะศูนย์ที่มีพิกัดจริง':'ไม่มีพิกัดศูนย์พักพิงในพื้นที่ที่เลือก':'ไม่มีรายงานศูนย์พักพิงในพื้นที่ที่เลือก');
 shelterMap.invalidateSize();if(pts.length)shelterMap.fitBounds(pts,{padding:[28,28],maxZoom:13});else if(outline)shelterMap.fitBounds(outline.getBounds());else shelterMap.setView([13.75,100.55],10);
}"""

new_func = """function renderShelterMap(){
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

 const allowedStatuses = new Set(Array.from(document.querySelectorAll('.shelter-filter:checked')).map(cb=>cb.dataset.filter));
 const filteredShelters = currentShelters.filter(r=>allowedStatuses.has(canonicalShelterStatus(r.occupied,r.capacity)));
 const pts=addShelterPins(shelterLayers, filteredShelters.filter(r=>typeof r.latitude==='number'&&typeof r.longitude==='number'));
 
 shelterMap.invalidateSize();
 if(pts.length) shelterMap.fitBounds(pts,{padding:[28,28],maxZoom:13});
 else shelterMap.setView([13.75,100.55],10);
 
 const timeStr = filteredShelters.map(r=>r.Ingested_At||r.updated_at_source||r.fetched_at_th).filter(x=>x).sort().pop();
 $('shelterMapSource').innerHTML = `<b>อัปเดต ณ:</b> ${timeStr ? time(timeStr) : 'ไม่ระบุ'}`;
 $('shelterMapNote').innerHTML = '<b style="color:#334155">คำอธิบายแผนที่:</b><br/>' + '• <b>เส้นกรอบเขต:</b> สีบ่งบอกสถานะของสถานีน้ำที่รุนแรงที่สุดในเขตนั้นๆ<br/>' + (heatData.length ? '• <b>Heatmap (สีฟุ้ง):</b> แสดงจุดหนาแน่นของสถานีน้ำ <i>*ไม่ใช่พื้นที่น้ำท่วมจริง</i><br/>' : '• <b>Heatmap:</b> (ไม่มีข้อมูลสถานีอัปเดตใน 24 ชม. จึงไม่แสดง Heatmap)<br/>') + '• <b>หมุด:</b> ตำแหน่งศูนย์พักพิง กรองตามสถานะที่เลือกไว้ด้านบน';
 
 renderShelterTable(filteredShelters);
}

function renderShelterTable(shelters) {
  const sorted = [...shelters].sort((a,b) => {
    const sa = canonicalShelterStatus(a.occupied, a.capacity);
    const sb = canonicalShelterStatus(b.occupied, b.capacity);
    const rank = s => s==='เต็ม'?3 : s==='ใกล้เต็ม'?2 : s==='ว่าง'?1 : 0;
    if(rank(sb) !== rank(sa)) return rank(sb) - rank(sa);
    return (a.district||'').localeCompare(b.district||'','th');
  });
  
  const rowsHtml = sorted.map(s => {
    const st = canonicalShelterStatus(s.occupied, s.capacity);
    const stColor = st==='เต็ม'?'#dc2626':st==='ใกล้เต็ม'?'#ea580c':st==='ว่าง'?'#16a34a':'#64748b';
    return `<tr>
      <td>${esc(s.district||'ไม่ระบุ')}</td>
      <td>${esc(s.shelter_name)}</td>
      <td style="color:${stColor}; font-weight:600">${esc(st)}</td>
      <td class="num">${fmt(s.occupied)} / ${fmt(s.capacity)}</td>
    </tr>`;
  }).join('');
  
  $('shelterSideBody').innerHTML = `<table class="data-table">
    <thead>
      <tr style="position: sticky; top: 0; background: #f8fafc; z-index: 1;">
        <th>เขต</th>
        <th>ชื่อศูนย์พักพิง</th>
        <th>สถานะ</th>
        <th class="num">ผู้พัก / ความจุ</th>
      </tr>
    </thead>
    <tbody>
      ${rowsHtml || '<tr><td colspan="4" style="text-align:center;color:#666">ไม่มีศูนย์พักพิงในเงื่อนไขที่เลือก</td></tr>'}
    </tbody>
  </table>`;
}
"""

if old_func in html:
    html = html.replace(old_func, new_func)
    print("Replaced renderShelterMap")
else:
    print("Could not find renderShelterMap")

# Also add event listeners to shelter-filter
events_script = "$('showShelterPins').addEventListener('change',()=>renderMap());"
new_events = "$('showShelterPins').addEventListener('change',()=>renderMap());\ndocument.querySelectorAll('.shelter-filter').forEach(cb=>cb.addEventListener('change',()=>renderShelterMap()));"
if events_script in html:
    html = html.replace(events_script, new_events)
    print("Added shelter filter event listeners")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
