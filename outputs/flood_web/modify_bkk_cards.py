import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# We need to insert the calculations before `$('cards').innerHTML = ...`
idx = html.find("$('cards').innerHTML=bkk?")
if idx == -1:
    print("Could not find cards assignment!")
    sys.exit(1)

# Let's write the calculation code
calc_code = """
 let bkkCriticalDistricts = 0, bkkCriticalStations = 0, bkkShelterFull = 0, bkkShelterCap = 0, bkkShelterOcc = 0;
 if(bkk) {
   const distMap = new Map();
   for(const r of currentStations) {
     if(quality(r) !== 'ภายใน 24 ชั่วโมง') continue;
     const st = canonicalWaterStatus(r.flood_status_source);
     if(st === 'วิกฤต') bkkCriticalStations++;
     if(WATER_STATUS[st]) {
       const currentRank = distMap.get(r.district_or_area) || 0;
       if(WATER_STATUS[st].rank > currentRank) distMap.set(r.district_or_area, WATER_STATUS[st].rank);
     }
   }
   for(const rank of distMap.values()) {
     if(rank >= (WATER_STATUS['วิกฤต']?.rank || 4)) bkkCriticalDistricts++;
   }
   for(const r of currentShelters) {
     if(r.status_source === 'เต็ม' || (r.capacity > 0 && r.occupied >= r.capacity)) bkkShelterFull++;
     bkkShelterCap += (r.capacity || 0);
     bkkShelterOcc += (r.occupied || 0);
   }
 }
"""

old_bkk_cards = "bkk?card('ครัวเรือนตามรายงาน ปภ. ทั้ง กทม.',households,'ครัวเรือน','ไม่แจกแจงรายเขตในไฟล์',true)+card('สถานีคลองในพื้นที่เลือก',currentStations.length,'แห่ง',`ข้อมูลอายุ 0–24 ชั่วโมง ${fmt(fresh.length)} แห่ง`)+card('ผู้พักพิงในพื้นที่เลือก',currentShelters.length?sum(currentShelters,'occupied'):null,'คน',`ศูนย์พักพิงที่มีรายงาน ${fmt(currentShelters.length)} แห่ง`)+card('ที่ว่างตามรายงานต้นทาง',currentShelters.length?sum(currentShelters,'available'):null,'คน','ต้องตรวจความพร้อมกับศูนย์อีกครั้ง'):"

new_bkk_cards = "bkk?card('จำนวนเขตที่วิกฤต',bkkCriticalDistricts,'เขต','จากข้อมูลสถานีน้ำ 24 ชม.',true)+card('จำนวนสถานีน้ำที่วิกฤต',bkkCriticalStations,'สถานี',`จากทั้งหมด ${fmt(fresh.length)} สถานีที่ข้อมูลอัปเดต`)+card('สัดส่วนผู้เข้าพักศูนย์พักพิง',bkkShelterOcc,'คน',`รองรับได้ทั้งหมด ${fmt(bkkShelterCap)} คน`)+card('จำนวนศูนย์พักพิงที่เต็ม',bkkShelterFull,'แห่ง',`จากศูนย์ที่มีพิกัดทั้งหมด ${fmt(currentShelters.length)} แห่ง`):"

# Replace the assignment
html = html[:idx] + calc_code + html[idx:].replace(old_bkk_cards, new_bkk_cards)

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated BKK cards!")
