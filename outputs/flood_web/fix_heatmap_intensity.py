import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# Old logic in BKK:
# const heatData=currentStations.filter(r=>typeof r.latitude==='number'&&typeof r.longitude==='number').map(r=>{
#   const status=canonicalWaterStatus(r.flood_status_source),q=quality(r);
#   const rank=WATER_STATUS[status]?.rank||0;
#   const intensity=q!=='ภายใน 24 ชั่วโมง'?0:rank/5;
#   return [r.latitude,r.longitude,intensity];
# }).filter(d=>d[2]>0);

old_bkk_heat = "const intensity=q!=='ภายใน 24 ชั่วโมง'?0:rank/5;"
# Find max rank among fresh stations first
new_bkk_heat = "const maxRank = Math.max(...currentStations.filter(r=>quality(r)==='ภายใน 24 ชั่วโมง').map(r=>WATER_STATUS[canonicalWaterStatus(r.flood_status_source)]?.rank||1)); const intensity=q!=='ภายใน 24 ชั่วโมง'?0:rank/maxRank;"

if old_bkk_heat in html:
    html = html.replace(old_bkk_heat, new_bkk_heat)
    print("Replaced BKK heatmap intensity calculation")
else:
    print("Could not find old_bkk_heat")

# National map has:
# const heatData=currentStations.map(r=>{
#   const rank=WATER_STATUS[canonicalWaterStatus(r.flood_status_source)]?.rank||0;
#   return [r.latitude,r.longitude,({1:.1,2:.2,3:.5,4:.8,5:1})[rank]||0];
# }).filter(r=>r[2]>0);

old_nat_heat = "return [r.latitude,r.longitude,({1:.1,2:.2,3:.5,4:.8,5:1})[rank]||0];"
new_nat_heat = "const maxRank = Math.max(...currentStations.filter(r=>quality(r)==='ภายใน 24 ชั่วโมง').map(r=>WATER_STATUS[canonicalWaterStatus(r.flood_status_source)]?.rank||1)); return [r.latitude,r.longitude, rank ? (rank/maxRank) : 0];"

if old_nat_heat in html:
    html = html.replace(old_nat_heat, new_nat_heat)
    print("Replaced NAT heatmap intensity calculation")
else:
    print("Could not find old_nat_heat")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
