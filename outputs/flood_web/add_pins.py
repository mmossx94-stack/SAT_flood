import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add Checkbox to HTML
old_tools = '<label><input type="checkbox" id="showHealthRegions" checked>แสดงเส้นเขตสุขภาพ <span style="display:inline-block;width:36px;height:1px;background:#475569" aria-hidden="true"></span></label><span id="healthRegionStatus" class="sub"></span></div>'
new_tools = '<label><input type="checkbox" id="showHealthRegions" checked>แสดงเส้นเขตสุขภาพ <span style="display:inline-block;width:36px;height:1px;background:#475569" aria-hidden="true"></span></label><label style="margin-left:16px"><input type="checkbox" id="showStationPins">แสดงหมุดสถานี</label><span id="healthRegionStatus" class="sub" style="margin-left:16px"></span></div>'
if old_tools in html:
    html = html.replace(old_tools, new_tools)
    print("Added checkbox HTML")
else:
    print("Could not find tools HTML")

# 2. Add event listener
old_listener = "$('showHealthRegions').addEventListener('change',renderHealthRegions);"
new_listener = "$('showHealthRegions').addEventListener('change',renderHealthRegions);$('showStationPins').addEventListener('change',()=>renderMap());"
if old_listener in html:
    html = html.replace(old_listener, new_listener)
    print("Added event listener")
else:
    print("Could not find listener")

# 3. Add rendering logic for pins in national map
old_render = "if(L.heatLayer&&heatData.length)L.heatLayer(heatData,{radius:30,blur:24,maxZoom:8,max:6,minOpacity:.06,gradient:{.15:'#93c5fd',.4:'#3b82f6',.7:'#1d4ed8',1:'#082f6b'}}).addTo(layers);"
new_render = """if(L.heatLayer&&heatData.length)L.heatLayer(heatData,{radius:30,blur:24,maxZoom:8,max:6,minOpacity:.06,gradient:{.15:'#93c5fd',.4:'#3b82f6',.7:'#1d4ed8',1:'#082f6b'}}).addTo(layers);
if($('showStationPins')?.checked){
  currentStations.filter(r=>typeof r.latitude==='number'&&typeof r.longitude==='number'&&quality(r)==='ภายใน 24 ชั่วโมง').forEach(r=>{
    const rank=WATER_STATUS[canonicalWaterStatus(r.flood_status_source)]?.rank||0;
    const c=rank>=5?'#082f6b':rank>=4?'#1d4ed8':rank>=3?'#3b82f6':rank>=2?'#93c5fd':'transparent';
    if(c!=='transparent'){
      L.circleMarker([r.latitude,r.longitude],{radius:4,fillColor:c,fillOpacity:0.8,color:'#ffffff',weight:1}).bindTooltip(`<b>${esc(r.station_id)}</b><br>${esc(r.flood_status_source)}`).addTo(layers);
    }
  });
}"""
if old_render in html:
    html = html.replace(old_render, new_render)
    print("Added pin rendering logic")
else:
    print("Could not find render logic")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
