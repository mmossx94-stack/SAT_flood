import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_source = "$('mapSource').innerHTML=sourceLinks(currentStations,bkk?'สถานีระดับน้ำ กทม. (ตามข้อมูลต้นทาง)':'สถานีระดับน้ำ: ThaiWater')+'<br>ข้อมูลที่แสดงอ่านจาก '+esc(DATA.source)+' · ชีต '+(bkk?'BKK_water_DB':'thai_water_DB');"

new_source = """const waterTime = currentStations.map(r=>r.Ingested_At||r.updated_at_source||r.observed_at_th||r.fetched_at_th).filter(x=>x).sort().pop();
const shelterTime = currentShelters.map(r=>r.Ingested_At).filter(x=>x).sort().pop();
$('mapSource').innerHTML = bkk ?
  '<b>ที่มาของข้อมูลในแผนที่</b><br/>' +
  '1. ข้อมูลน้ำ จากสำนักการระบายน้ำ <a href="https://weather.bangkok.go.th/water/" target="_blank">weather.bangkok.go.th/water</a> อัพเดท ณ ' + (waterTime ? date(waterTime) + ' ' + time(waterTime) : 'ไม่ระบุ') + '<br/>' +
  '2. ข้อมูลศูนย์พักพิง กรุงเทพมหานคร <a href="https://floodsupport.bangkok.go.th/" target="_blank">floodsupport.bangkok.go.th</a> อัพเดท ณ ' + (shelterTime ? date(shelterTime) + ' ' + time(shelterTime) : 'ไม่ระบุ')
  :
  sourceLinks(currentStations, 'สถานีระดับน้ำ: ThaiWater') + '<br>ข้อมูลที่แสดงอ่านจาก ' + esc(DATA.source) + ' · ชีต thai_water_DB';"""

if old_source in html:
    html = html.replace(old_source, new_source)
    print("Replaced mapSource!")
else:
    print("Could not find old mapSource")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
