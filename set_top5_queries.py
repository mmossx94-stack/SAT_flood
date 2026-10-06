import pathlib

paths = [
    pathlib.Path(r'C:\xampp\htdocs\SAT_update\Dashboard\trends_scraper.py'),
    pathlib.Path(r'f:\2569_น้ำท่วม\SAT\Dashboard\trends_scraper.py')
]

fallback_code = '''    fallback_p1 = [
        {"query": "เรดาร์ฝน กทม ล่าสุด", "growth": "Breakout", "intent": "เช็คสภาพอากาศ"},
        {"query": "ย้ายของขึ้นที่สูง ทำอย่างไร", "growth": "+5200%", "intent": "เตรียมย้ายทรัพย์สิน"},
        {"query": "isowall กัน น้ำท่วม", "growth": "+350%", "intent": "จัดหาอุปกรณ์ป้องกัน"},
        {"query": "ระดับ น้ำ ปิง เจ้าพระยา", "growth": "+170%", "intent": "เฝ้าระวังระดับน้ำ"},
        {"query": "กระสอบทราย ซื้อที่ไหน", "growth": "+450%", "intent": "อุปกรณ์ป้องกันน้ำท่วม"}
    ]
    fallback_p2 = [
        {"query": "เบอร์ ติดต่อ สายด่วน ปภ 1784", "growth": "Breakout", "intent": "ขอความช่วยเหลือด่วน"},
        {"query": "ศูนย์พักพิง ใกล้ฉัน น้ำท่วม", "growth": "+9500%", "intent": "หาอพยพปลอดภัย"},
        {"query": "วิธี ตัดไฟ บ้าน น้ำท่วม", "growth": "+1200%", "intent": "ความปลอดภัยในบ้าน"},
        {"query": "ถุงยังชีพ ลงทะเบียน อพยพ", "growth": "+2850%", "intent": "ปัจจัย 4 ฉุกเฉิน"},
        {"query": "สุขาเคลื่อนที่ น้ำท่วม", "growth": "+1800%", "intent": "สุขอนามัยฉุกเฉิน"}
    ]
    fallback_p3 = [
        {"query": "ลง ทะเบียน เยียวยา น้ำท่วม", "growth": "+4050%", "intent": "ยื่นสิทธิชดเชย"},
        {"query": "ทาง รัฐ น้ำท่วม", "growth": "+5200%", "intent": "ลงทะเบียนเยียวยา"},
        {"query": "ตาม หา ป้าย ทะเบียน หลัง น้ำท่วม", "growth": "+2500%", "intent": "ทรัพย์สินสูญหาย"},
        {"query": "วิธี ทำความสะอาด บ้าน หลัง น้ำท่วม", "growth": "+3100%", "intent": "ฟื้นฟูที่อยู่อาศัย"},
        {"query": "วิธียื่น ขอ เงินเยียวยา หลัง น้ำท่วม", "growth": "+3500%", "intent": "ขั้นตอนขอรับเงินชดเชย"}
    ]'''

for p in paths:
    if p.exists():
        text = p.read_text(encoding='utf-8')
        start_fb1 = text.find("    fallback_p1 = [")
        if start_fb1 == -1:
            start_fb1 = text.find("fallback_p1 = [")
            
        end_fb3 = text.find("p1_clean = ")
        
        if start_fb1 != -1 and end_fb3 != -1:
            text = text[:start_fb1] + fallback_code + "\n\n    " + text[end_fb3:]

        p.write_text(text, encoding='utf-8')
        print(f"Fixed indentation for {p}")
