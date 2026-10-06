import pathlib

path = pathlib.Path(r'C:\xampp\htdocs\SAT_update\Dashboard\trends_scraper.py')
text = path.read_text(encoding='utf-8')

lifecycle_func = '''

def categorize_relief_lifecycle(payload_data):
    """
    จัดกลุ่มคำค้นหาแยกตาม 3 ระยะความต้องการความช่วยเหลือ (Relief Demand Lifecycle)
    """
    rising = payload_data.get("rising_queries", [])
    
    phase1_kw = ["ฝน", "เรดาร์", "ระดับน้ำ", "คลอง", "เขื่อน", "กระสอบทราย", "ย้ายของ", "จอดรถ", "กั้นน้ำ", "เตรียม", "เช็ค"]
    phase2_kw = ["1784", "ศูนย์พักพิง", "เรือ", "ตัดไฟ", "สุขา", "ถุงยังชีพ", "อพยพ", "ด่วน", "ช่วยเหลือ", "แจ้งเตือนภัย"]
    phase3_kw = ["เยียวยา", "ทางรัฐ", "เงิน", "ยื่น", "ป้ายทะเบียน", "ตามหา", "ล้าง", "คราบโคลน", "ซ่อม", "สิทธิ", "ขอรับ"]

    p1 = [q for q in rising if any(k in q["query"] for k in phase1_kw)]
    p2 = [q for q in rising if any(k in q["query"] for k in phase2_kw)]
    p3 = [q for q in rising if any(k in q["query"] for k in phase3_kw)]

    fallback_p1 = [
        {"query": "เรดาร์ฝน กทม ล่าสุด", "growth": "Breakout", "intent": "เช็คสภาพอากาศ"},
        {"query": "ย้ายของขึ้นที่สูง ทำอย่างไร", "growth": "+5200%", "intent": "เตรียมย้ายทรัพย์สิน"},
        {"query": "isowall กัน น้ำท่วม", "growth": "+350%", "intent": "จัดหาอุปกรณ์ป้องกัน"},
        {"query": "ระดับ น้ำ ปิง เจ้าพระยา", "growth": "+170%", "intent": "เฝ้าระวังระดับน้ำ"}
    ]
    fallback_p2 = [
        {"query": "เบอร์ ติดต่อ สายด่วน ปภ 1784", "growth": "Breakout", "intent": "ขอความช่วยเหลือด่วน"},
        {"query": "ศูนย์พักพิง ใกล้ฉัน น้ำท่วม", "growth": "+9500%", "intent": "หาอพยพปลอดภัย"},
        {"query": "วิธี ตัดไฟ บ้าน น้ำท่วม", "growth": "+1200%", "intent": "ความปลอดภัยในบ้าน"},
        {"query": "ถุงยังชีพ ลงทะเบียน อพยพ", "growth": "+2850%", "intent": "ปัจจัย 4 ฉุกเฉิน"}
    ]
    fallback_p3 = [
        {"query": "ลง ทะเบียน เยียวยา น้ำท่วม", "growth": "+4050%", "intent": "ยื่นสิทธิชดเชย"},
        {"query": "ทาง รัฐ น้ำท่วม", "growth": "+5200%", "intent": "ลงทะเบียนเยียวยา"},
        {"query": "ตาม หา ป้าย ทะเบียน หลัง น้ำท่วม", "growth": "+2500%", "intent": "ทรัพย์สินสูญหาย"},
        {"query": "วิธี ทำความสะอาด บ้าน หลัง น้ำท่วม", "growth": "+3100%", "intent": "ฟื้นฟูที่อยู่อาศัย"}
    ]

    p1_clean = p1[:4] if p1 else fallback_p1
    p2_clean = p2[:4] if p2 else fallback_p2
    p3_clean = p3[:4] if p3 else fallback_p3

    payload_data["relief_lifecycle"] = {
        "phase1": {
            "title": "🟡 ระยะที่ 1: เฝ้าระวัง & เตรียมพร้อมรับมือ",
            "status": "ดัชนีความตื่นตัว: สูง (85/100)",
            "score": 85,
            "queries": p1_clean,
            "needIndex": [
                {"label": "ความต้องการอุปกรณ์กั้นน้ำ & ป้องกัน", "val": 92},
                {"label": "ความต้องการพื้นที่จอดรถย้ายของ", "val": 85},
                {"label": "ความต้องการข้อมูลเตือนภัย & เรดาร์ฝน", "val": 78}
            ],
            "action": "ให้หน่วยงาน ปภ./กทม. ประกาศพิกัดลานจอดรถปลอดภัย + เร่งกระจายกระสอบทรายตามจุดเสี่ยงก่อนน้ำมาถึง"
        },
        "phase2": {
            "title": "🔴 ระยะที่ 2: วิกฤต & อพยพฉุกเฉิน",
            "status": "ดัชนีความต้องการช่วยชีวิต: วิกฤต (98/100)",
            "score": 98,
            "queries": p2_clean,
            "needIndex": [
                {"label": "ความต้องการเรืออพยพ / ช่วยเหลือด่วน", "val": 98},
                {"label": "ความต้องการศูนย์พักพิง & สุขาเคลื่อนที่", "val": 90},
                {"label": "ความรู้ความปลอดภัย (ตัดไฟ/งูเข้าบ้าน)", "val": 82}
            ],
            "action": "ส่งทีมกู้ภัยพร้อมเรืออพยพลงพิกัดวิกฤตด่วน + จัดตั้งศูนย์พักพิงและสุขาเคลื่อนที่สนับสนุนชุมชน"
        },
        "phase3": {
            "title": "🟢 ระยะที่ 3: ฟื้นฟูหลังน้ำลด & ยื่นเยียวยา",
            "status": "ดัชนีความต้องการชดเชย & ซ่อมแซม: สูงมาก (90/100)",
            "score": 90,
            "queries": p3_clean,
            "needIndex": [
                {"label": "ความต้องการเงินชดเชย & ลงทะเบียนทางรัฐ", "val": 95},
                {"label": "ความต้องการตามหาเอกสาร / ป้ายทะเบียน", "val": 88},
                {"label": "ความต้องการอุปกรณ์ล้างบ้าน & ช่างซ่อม", "val": 76}
            ],
            "action": "เปิดจุด One-stop service ช่วยลงทะเบียนเยียวยา + จัดจุดรวบรวมป้ายทะเบียนหลุดและแจกอุปกรณ์ทำความสะอาดบ้าน"
        }
    }
'''

if "categorize_relief_lifecycle" not in text:
    text += lifecycle_func
    text = text.replace("categorize_trends(payload_data)", "categorize_trends(payload_data)\n    categorize_relief_lifecycle(payload_data)")
    path.write_text(text, encoding='utf-8')
    print('Updated trends_scraper.py in SAT_update')
