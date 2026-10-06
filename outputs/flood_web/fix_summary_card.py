import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_str = """   for(const r of currentShelters) {
     if(r.status_source === 'เต็ม' || (r.capacity > 0 && r.occupied >= r.capacity)) bkkShelterFull++;
     bkkShelterCap += (r.capacity || 0);
     bkkShelterOcc += (r.occupied || 0);
   }
 }
$('cards').innerHTML=bkk?card('จำนวนเขตที่วิกฤต',bkkCriticalDistricts,'เขต','จากข้อมูลสถานีน้ำ 24 ชม.',true)+card('จำนวนสถานีน้ำที่วิกฤต',bkkCriticalStations,'สถานี',`จากทั้งหมด ${fmt(fresh.length)} สถานีที่ข้อมูลอัปเดต`)+card('สัดส่วนผู้เข้าพักศูนย์พักพิง',bkkShelterOcc,'คน',`รองรับได้ทั้งหมด ${fmt(bkkShelterCap)} คน`)+card('จำนวนศูนย์พักพิงที่เต็ม',bkkShelterFull,'แห่ง',`จากศูนย์ที่มีพิกัดทั้งหมด ${fmt(currentShelters.length)} แห่ง`):"""

new_str = """   for(const r of currentShelters) {
     if(r.status_source === 'เต็ม' || r.status_source === 'ใกล้เต็ม' || (r.capacity > 0 && r.occupied >= r.capacity)) bkkShelterFull++;
     bkkShelterCap += (r.capacity || 0);
     bkkShelterOcc += (r.occupied || 0);
   }
 }
$('cards').innerHTML=bkk?card('จำนวนเขตที่วิกฤต',bkkCriticalDistricts,'เขต','จากข้อมูลสถานีน้ำ 24 ชม.',true)+card('จำนวนสถานีน้ำที่วิกฤต',bkkCriticalStations,'สถานี',`จากทั้งหมด ${fmt(fresh.length)} สถานีที่ข้อมูลอัปเดต`)+card('สัดส่วนผู้เข้าพักศูนย์พักพิง',bkkShelterOcc,'คน',`รองรับได้ทั้งหมด ${fmt(bkkShelterCap)} คน`)+card('จำนวนศูนย์ที่เต็ม/ใกล้เต็ม',bkkShelterFull,'แห่ง',`จากศูนย์ที่มีพิกัดทั้งหมด ${fmt(currentShelters.length)} แห่ง`):"""

if old_str in html:
    html = html.replace(old_str, new_str)
    print("Fixed card logic!")
else:
    print("Could not find card logic!")

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
