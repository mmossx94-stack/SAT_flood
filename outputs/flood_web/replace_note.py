import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

old_note = """$('districtWaterNote').textContent=heatData.length?'Heatmap แสดงความหนาแน่นของสถานีถ่วงน้ำหนักตามสถานะระดับน้ำ ณ เวลานำเข้า ไม่ใช่ขอบเขตน้ำท่วมจริง · กดเขตเพื่อดูสถานะและเวลาวัด':'ไม่มีสถานีที่มีสถานะระดับน้ำและเวลาข้อมูลผ่านเกณฑ์ 24 ชั่วโมงในพื้นที่เลือก จึงไม่แสดง Heatmap · เส้นเขตและหมุดศูนย์พักพิงยังใช้งานได้';"""
new_note = """$('districtWaterNote').innerHTML = '<b style="color:#334155">คำอธิบายแผนที่:</b><br/>' + '• <b>เส้นกรอบเขต:</b> สีบ่งบอกสถานะของสถานีน้ำที่รุนแรงที่สุดในเขตนั้นๆ (อัปเดต 24 ชม.)<br/>' + (heatData.length ? '• <b>Heatmap (สีฟุ้ง):</b> แสดงจุดหนาแน่นของสถานีน้ำ (ยิ่งสีน้ำเงินเข้ม = วิกฤต) <i>*ไม่ใช่พื้นที่น้ำท่วมจริง</i><br/>' : '• <b>Heatmap:</b> (ไม่มีข้อมูลสถานีอัปเดตใน 24 ชม. จึงไม่แสดง Heatmap)<br/>') + '• <b>หมุด:</b> ตำแหน่งศูนย์พักพิง สามารถกดกรองสถานะ (ว่าง/เต็ม) ได้ที่ปุ่มด้านบน<br/>' + '<i style="color:#64748b; margin-top:4px; display:block">👉 กดคลิกที่พื้นที่แต่ละเขต เพื่อดูรายชื่อสถานีน้ำทั้งหมดในเขตนั้น</i>';"""

if old_note in html:
    html = html.replace(old_note, new_note)
    print("Replaced note!")
else:
    print("Could not find old note")
    
with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
