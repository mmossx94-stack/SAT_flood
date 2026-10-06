"""
news_scraper.py  v2.0
ระบบกวาดข่าวน้ำท่วมรายวัน — TF-IDF based Word Cloud
──────────────────────────────────────────────────────
ปรับปรุง:
  1. ตัดคำค้นหาเอง (น้ำท่วม ฯลฯ) ออกจาก Word Cloud
  2. ใช้ TF-IDF ให้ได้คำที่ "เป็นประเด็น" ไม่ใช่คำซ้ำทั่วไป
  3. ทำ dedup ข้อความ title ที่ซ้ำในแต่ละบทความ
  4. กรอง boilerplate จากชื่อสำนักข่าว, HTML entities
  5. เน้นคำนามที่มีความหมาย: สถานที่, ชื่อ, เหตุการณ์
"""

import json
import re
import math
import sys
from datetime import datetime, timedelta, timezone
from collections import Counter, defaultdict
from pathlib import Path

import requests
import feedparser
from bs4 import BeautifulSoup

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).parent / "news_data"
OUTPUT_DIR.mkdir(exist_ok=True)

TODAY = datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d")
NOW_UTC = datetime.now(timezone.utc)

# กรองเฉพาะข่าวที่เผยแพร่ภายในกี่ชั่วโมงที่ผ่านมา
HOURS_WINDOW = 30
CUTOFF_UTC = NOW_UTC - timedelta(hours=HOURS_WINDOW)

# ──────────────────────────────────────────────
# คำค้นหาที่ใช้ search — ห้ามแสดงใน Word Cloud
# เพราะ "แน่นอน" ว่าต้องปรากฏ ไม่ได้บอกประเด็น
# ──────────────────────────────────────────────
SEARCH_QUERY_WORDS = {
    # ไทย
    "น้ำท่วม", "อุทกภัย", "น้ำหลาก", "น้ำล้น", "น้ำท่วมขัง", "น้ำ",
    "ท่วม", "ท่วมขัง", "ท่วมสูง",
    # อังกฤษ
    "flood", "flooding", "floods", "flooded", "inundation",
    "floodwater", "floodwaters",
}

# ──────────────────────────────────────────────
# STOPWORDS ไทย (คำทั่วไป ไม่ใช่ประเด็น)
# ──────────────────────────────────────────────
THAI_STOPWORDS = {
    # function words / particles
    "ของ","ใน","และ","ที่","มี","ได้","การ","ให้","จาก","เป็น","ว่า","จะ","ด้วย","นี้",
    "แต่","ไม่","กับ","ยัง","ก็","จึง","โดย","ซึ่ง","เพื่อ","หรือ","มา","ไป","อยู่",
    "กัน","นั้น","เมื่อ","เพราะ","แล้ว","เพิ่ม","ขึ้น","ลง","เช่น","ทั้ง","หาก",
    "ต้อง","รวม","ต่อ","ถึง","เข้า","ออก","ขณะ","ส่วน","ดัง","พร้อม","ตาม",
    "ด้าน","ทำให้","ทั้งนี้","เขา","เธอ","พวก","เรา","พวกเรา","ทั้งหมด",
    "อีก","เพียง","แม้","เพื่อให้","สำหรับ","นำ","ตน","ทั้ง","บาง",
    "ซึ่ง","อัน","เหล่า","เหล่านี้","ดัง","ดังกล่าว","ดังนั้น","ดังนี้",
    "ต่อไป","นับแต่","ตั้งแต่","ขณะที่","อย่างไร","อย่างไรก็","แม้ว่า",
    "ซึ่ง","ดัง","ใด","ใคร","อะไร","เมื่อไหร่","อย่างใด","ทั้งนั้น",
    # หน่วยนับ/เวลา
    "คน","วัน","ปี","เดือน","ชั่วโมง","นาที","วินาที","บาท","ร้อย","พัน",
    "หมื่น","ล้าน","แห่ง","แห่งที่","ราย","ครั้ง","แบบ","ชนิด","ประเภท",
    # verbs ทั่วไป
    "กล่าว","กล่าวว่า","เปิดเผย","ระบุ","พบ","ชี้","ห่วง","แจ้ง","คาด",
    "ทราบ","เชื่อ","ยืนยัน","ปฏิเสธ","เตือน","สั่ง","ขอ","ช่วย","ส่ง","รับ",
    "รายงาน","เร่ง","ดำเนิน","ดำเนินการ","ดำเนินงาน","ปฏิบัติ","ดูแล",
    "ติดตาม","ตรวจสอบ","ประสาน","บูรณาการ","บริหาร","จัดการ",
    "มอบ","รวบรวม","สนับสนุน","ออก","เดิน","บอก","ทำ","ใช้","ขาย","ซื้อ",
    "เปิด","ปิด","ยก","ลด","เพิ่ม","ปรับ","วาง","ตั้ง","วาง","วัด",
    # nouns generic
    "ข้อมูล","สถิติ","สถานการณ์","พื้นที่","บริเวณ","ประเทศ","ไทย",
    "รัฐบาล","หน่วยงาน","เจ้าหน้าที่","ทหาร","ตำรวจ","ผู้ว่า","นายก",
    "รัฐมนตรี","กระทรวง","กรม","สำนัก","องค์กร","ศูนย์","คณะ",
    "ประชาชน","ราษฎร","ชาวบ้าน","ชาว","ผู้","ผู้ว่าฯ","นายกฯ",
    "จังหวัด","อำเภอ","ตำบล","ชุมชน","เขต","แขวง","หมู่บ้าน","หมู่",
    "วันที่","เวลา","ช่วง","ระยะ","ประมาณ","ราว","ประมาณการ",
    "ผล","ผลการ","สรุป","รายละเอียด","ขั้นตอน","แผน","แผนการ",
    "เรื่อง","ประเด็น","กรณี","เหตุการณ์","สาเหตุ","ผลกระทบ",
    "ช่วยเหลือ","บรรเทา","ป้องกัน","แก้ไข","ฟื้นฟู","รับมือ","เตรียม",
    "ปภ","สจ","กทม","ทบ","อบต","อบจ","รพ","สสจ",  # ตัวย่อที่ไม่บอกประเด็น
    # ชื่อสำนักข่าว (boilerplate)
    "สวพ","ผู้จัดการ","แนวหน้า","เดลินิวส์","คมชัดลึก","ข่าวสด","ไทยโพสต์",
    "สยามรัฐ","มติชน","ไทยรัฐ","กรุงเทพธุรกิจ","ประชาชาติ","ฐานเศรษฐกิจ",
    "บางกอกโพสต์","เนชั่น","เนชั่นทีวี","อมรินทร์","เวิร์คพอยท์","ทรูวิชั่น",
    "ไทยพีบีเอส","สปริง","ทีวีพูล","ช่องวัน","ช่อง","เช้าหัวเขียว",
    # คำสั้นเกิน / คำนำหน้า
    "นาย","นาง","นางสาว","ดร","ศ","รศ","ผศ","พล","พลตำรวจ","พลทหาร",
    "ผ่าน","มา","ไป","ให้","กับ","ต่อ","จาก","ถึง","ใน","บน","ที่",
    "เผย","บอก","ชี้แจง","ระบุ","ยืนยัน",
    # คำ generic อื่น
    "อัปเดต","ออนไลน์","ล่าสุด","ทันที","เร็วๆ","บัดนี้","ขณะนี้",
    "เคียงข้าง",  # campaign slogan ไม่ใช่ประเด็น
    "กว่า","ลุย","สูง","ตกหนัก","ประชุม","แพ่ง","เร่ง",
    # คำการเมือง/บุคคล/Noise ที่ไม่เกี่ยวกับการเฝ้าระวัง
    "พรรคเพื่อไทย","พรรค","สส","ส.ส.","ชัชชาติ","อนุทิน","ฝ่ายค้าน","การเมือง",
    "วันนี้","แจก","จุล","มิติ","สื่อสาร","พลัง","เคหะ","ได้รับ","หลาย",
    "เริ่ม","ฟ้า","พันธิ์","รับเงิน","เช็ค","บก","สิ่","ร่วม","ความ","อย่าง",
    # คำ Noise 2-3 ตัวอักษร/คำกริยา/คำกว้างที่ไม่สื่อประเด็น
    "รอ","ทีม","เด็ก","หลัง","ชุด","โอน","จ่าย","เงิน","งบ","หุ้น","สว","ข่าว",
    "รัฐ","ฝั่ง","ภาค","กลาง","เดอะ","เตอร์","รีพอร์ต","กำลังใจ","มีใจ","การเรียน",
    "ประกันภัย","ต่อ","เนื่อง","ต่อเนื่อง","ทวี","คง","ยังคง","กล่อง",
    "สำรวจ","ประสพ","ประสบ","ทาง","ระบบ","เดินหน้า","เรื่อง",
    "ตุลาคม","กันยายน","พฤศจิกายน","สิงหาคม","เมษายน","ดอนเมือง","ถนนสายหลัก",
    # ชื่อเพจ/สื่อออนไลน์/แคมเปญ
    "เดอะรีพอร์ตเตอร์","ผู้จัดการออนไลน์","มิติหุ้น","อินน์นิวส์","ไทยคู่ฟ้า",
    "เดอะรีพอร์ต","รีพอร์ตเตอร์","มิติ","ออนไลน์","ผู้จัดการ",
}

# ──────────────────────────────────────────────
# COMPOUND WORDS FOR TRIE TOKENIZER
# ──────────────────────────────────────────────
COMPOUND_WORDS_TH = [
    "ผู้ประสบอุทกภัย", "ผู้ประสบภัย", "เงินเยียวยา", "ถุงยังชีพ", "จุดท่วมขัง",
    "ประตูระบายน้ำ", "เครื่องสูบน้ำ", "พนังกั้นน้ำ", "คันกั้นน้ำ", "สถานีสูบน้ำ",
    "อ่างเก็บน้ำ", "ท้ายเขื่อน", "เจ้าพระยา", "ป่าสักชลสิทธิ์", "ขุดลอกคลอง",
    "ทางระบายน้ำ", "ทุ่งรับน้ำ", "เยียวยาผู้ประสบภัย", "ศูนย์พักพิง", "สุขาเคลื่อนที่",
    "เรือพลาสติก", "โรงครัวพระราชทาน", "น้ำท่วมขัง", "ฝนตกหนัก", "ร่องมรสุม",
    "ปริมาณฝน", "ระดับน้ำ", "ปริมาณน้ำ", "ล้นตลิ่ง", "น้ำหลาก", "ทะเลหนุน",
    "ถนนสายหลัก", "การระบายน้ำ", "แจ้งเตือนภัย", "เฝ้าระวังพิเศษ", "ยกของขึ้นที่สูง",
    "หลังน้ำท่วม", "หลังน้ำลด", "ฟื้นฟูหลังน้ำท่วม", "เยียวยาหลังน้ำท่วม", "โรคหลังน้ำท่วม",
    "ขยะหลังน้ำท่วม", "ซ่อมแซมบ้าน", "ทำความสะอาดบ้าน",
]

# ──────────────────────────────────────────────
# WORD CATEGORIES & DOMAIN BOOSTING
# ──────────────────────────────────────────────
MONITORING_KEYWORDS = {
    # สภาพน้ำ / ระดับน้ำ / การระบาย
    "ระดับน้ำ", "ปริมาณน้ำ", "ล้นตลิ่ง", "ทะลัก", "น้ำหลาก", "ทะเลหนุน", "ทุ่งรับน้ำ",
    "น้ำเอ่อ", "ระดับ", "ระบายน้ำ", "ผันน้ำ", "แก้มลิง", "ทางน้ำ", "ตลิ่ง", "มวลน้ำ",
    "น้ำขัง", "ท่วมขัง", "ไหลหลาก", "ระบาย", "เอ่อล้น",
    # เขื่อน / สถานี / โครงสร้าง
    "เขื่อน", "ประตูระบายน้ำ", "เครื่องสูบน้ำ", "พนังกั้นน้ำ", "คันกั้นน้ำ", "ขุดลอก",
    "สถานีสูบน้ำ", "อ่างเก็บน้ำ", "ท้ายเขื่อน", "เจ้าพระยา", "ป่าสัก", "ป่าสักชลสิทธิ์",
    # เฝ้าระวัง / สภาพอากาศ / เตือนภัย
    "เฝ้าระวัง", "เตือนภัย", "จุดเสี่ยง", "จุดท่วมขัง", "ฝนตกหนัก", "พายุ", "ร่องมรสุม",
    "มรสุม", "ตกหนัก", "เสี่ยงภัย", "สีแดง", "สีส้ม", "วิกฤต", "ปริมาณฝน", "ฝน", "ขัง",
    "เสี่ยง", "เตือน", "เฝ้าระวังพิเศษ",
}

RELIEF_KEYWORDS = {
    "อพยพ", "ศูนย์พักพิง", "ยกของขึ้นที่สูง", "เตรียมรับมือ", "ถุงยังชีพ", "ยังชีพ",
    "เยียวยา", "แจกจ่าย", "ถุง", "ผู้ประสบภัย", "ผู้ประสบอุทกภัย", "เรือพลาสติก",
    "สุขาเคลื่อนที่", "โรงครัว", "ช่วยเหลือ", "บรรเทา", "เยียวยาผู้ประสบภัย",
}

POST_FLOOD_KEYWORDS = {
    "หลังน้ำท่วม", "หลังน้ำลด", "ฟื้นฟู", "ทำความสะอาด", "ซ่อมแซม", "ขยะ",
    "ฟื้นฟูหลังน้ำท่วม", "เยียวยาหลังน้ำท่วม", "โรคหลังน้ำท่วม", "ขยะหลังน้ำท่วม",
    "ล้างบ้าน", "เชื้อรา", "ซ่อมบ้าน",
}

LOCATION_KEYWORDS = {
    "กรุงเทพมหานคร", "กทม", "ปทุมธานี", "นนทบุรี", "ฉะเชิงเทรา", "อยุธยา",
    "พระนครศรีอยุธยา", "เชียงใหม่", "เชียงราย", "ปราจีนบุรี", "ลาดกระบัง",
    "ดอนเมือง", "สุโขทัย", "แพร่", "น่าน", "ตาก", "บุรีรัมย์", "อุบลราชธานี",
    "นครราชสีมา", "นครสวรรค์", "อ่างทอง", "สิงห์บุรี", "เมือง",
}

MONITORING_BOOST_FACTOR = 2.5
RELIEF_BOOST_FACTOR = 1.5
POST_FLOOD_BOOST_FACTOR = 2.0


# ──────────────────────────────────────────────
# STOPWORDS อังกฤษ
# ──────────────────────────────────────────────
ENG_STOPWORDS = {
    "the","a","an","and","or","but","in","on","at","to","for","of","with","by",
    "from","is","are","was","were","be","been","being","have","has","had",
    "do","does","did","will","would","could","should","may","might","shall",
    "this","that","these","those","it","its","he","she","they","we","you",
    "i","my","your","his","her","their","our","who","which","what","when",
    "where","how","as","if","so","then","than","up","out","about","into",
    "through","after","before","over","under","more","all","also","just",
    "not","no","can","said","says","say","per","cent","percent","also",
    "one","two","three","four","five","than","more","most","such","like",
    "new","news","report","year","month","day","week","time","government",
    "official","minister","department","agency","province","thailand","thai",
    "bangkok","water","area","level","nbsp","facebook","twitter","line",
    "reuters","today","share","read","more","click","here","photo",
    # boilerplate seo
    "source","via","related","articles","article","read","latest","update",
    "reporters","online","households",
    # ชื่อสำนักข่าวไทย (รั่วมาในภาษาอังกฤษ)
    "thairath","thaipost","thaipbs","matichon","sanook","kapook","khaosod",
    "prachachat","nationtv","amarintv","posttoday","thairath","workpoint",
    "spring","live","room","post","nation","standard","manager","daily",
    "naewna","komchadluek","bangkokpost","bangkokbiznews",
    # คำอื่นๆ ที่ไม่บอกประเด็น
    "home","back","next","prev","prev","page","menu","search","close",
    "email","print","save","comment","view","full","more","show","hide",
    "click","open","close","sign","login","register","subscribe",
}

# ──────────────────────────────────────────────
# RSS FEEDS
# ──────────────────────────────────────────────
RSS_FEEDS = [
    "https://news.google.com/rss/search?q=น้ำท่วม&hl=th&gl=TH&ceid=TH:th",
    "https://news.google.com/rss/search?q=หลังน้ำท่วม&hl=th&gl=TH&ceid=TH:th",
    "https://news.google.com/rss/search?q=อุทกภัย&hl=th&gl=TH&ceid=TH:th",
    "https://news.google.com/rss/search?q=ฟื้นฟู+น้ำท่วม&hl=th&gl=TH&ceid=TH:th",
    "https://news.google.com/rss/search?q=flood+Thailand&hl=en&gl=TH&ceid=TH:en",
    "https://www.matichon.co.th/feed",
    "https://www.thaipbs.or.th/feeds/",
    "https://www.thairath.co.th/rss/news",
]

DIRECT_SOURCES = [
    {
        "url": "https://www.disaster.go.th/th/news",
        "name": "กรมป้องกันและบรรเทาสาธารณภัย",
        "selector": "h2, h3, .news-title, .article-title, .card-title",
    },
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    )
}

FLOOD_KEYWORDS_TH = [
    "น้ำท่วม","อุทกภัย","น้ำล้น","ระดับน้ำ","น้ำหลาก","น้ำท่วมขัง",
    "น้ำเอ่อ","น้ำท่วมสูง","ฝนตกหนัก","พายุ","ดินถล่ม","เขื่อน",
    "ระบายน้ำ","อพยพ","ผู้ประสบภัย","ภัยพิบัติ","ท่วม","หลังน้ำท่วม","หลังน้ำลด","ฟื้นฟู",
]
FLOOD_KEYWORDS_EN = [
    "flood","flooding","inundation","storm","rainfall","water level",
    "overflow","evacuation","disaster","monsoon","dam","submerged",
]

# ──────────────────────────────────────────────
# BOILERPLATE PATTERNS ที่ต้องตัดออก
# (pattern ที่ซ้ำกันในทุกบทความจาก Google News)
# ──────────────────────────────────────────────
BOILERPLATE_RE = re.compile(
    r'(thairath\.co\.th|matichon\.co\.th|thaipbs\.or\.th|'
    r'thestandard\.co|khaosod\.co\.th|prachachat\.net|'
    r'sanook\.com|kapook\.com|line\s*today|FM\s*\d+|'
    r'&nbsp;|&amp;|&lt;|&gt;|&quot;|&#\d+;|\||\-\s*\w+\.)',
    re.IGNORECASE
)

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def clean_text(raw: str) -> str:
    """ทำความสะอาดข้อความก่อน tokenize"""
    # ลบ HTML entities
    text = re.sub(r'&[a-zA-Z]+;|&#\d+;', ' ', raw)
    # ลบ HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # ลบ URLs
    text = re.sub(r'https?://\S+', ' ', text)
    # ลบ boilerplate สำนักข่าว
    text = BOILERPLATE_RE.sub(' ', text)
    # ลบ punctuation ที่ไม่ใช่อักษร
    text = re.sub(r'[^\u0E00-\u0E7Fa-zA-Z\s]', ' ', text)
    # ลบ whitespace ซ้ำ
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def dedup_title_in_text(title: str, text: str) -> str:
    """
    RSS title มักซ้ำอยู่ใน summary/text
    ลบ title ออกจาก text เพื่อไม่ให้นับซ้ำ
    """
    clean_title = clean_text(title)
    # ลบ title ที่อยู่ใน text (ซ้ำๆ)
    if clean_title and len(clean_title) > 10:
        text = text.replace(clean_title, ' ')
    return text


def is_flood_related(text: str) -> bool:
    text_lower = text.lower()
    return any(k.lower() in text_lower for k in FLOOD_KEYWORDS_TH + FLOOD_KEYWORDS_EN)


_domain_trie = None

def get_domain_trie():
    global _domain_trie
    if _domain_trie is None:
        try:
            from pythainlp.tokenize import Trie
            _domain_trie = Trie(COMPOUND_WORDS_TH)
        except Exception:
            _domain_trie = False
    return _domain_trie


def tokenize_th(text: str) -> list:
    """Tokenize ภาษาไทย พร้อมใช้ Custom Trie เพื่อรวมคำประสมสำคัญ"""
    try:
        from pythainlp.tokenize import word_tokenize
        trie = get_domain_trie()
        if trie:
            tokens = word_tokenize(text, custom_dict=trie, engine="newmm", keep_whitespace=False)
        else:
            tokens = word_tokenize(text, engine="newmm", keep_whitespace=False)
        return [t.strip() for t in tokens if t.strip()]
    except ImportError:
        return re.findall(r'[\u0E00-\u0E7F]+', text)


def tokenize_en(text: str) -> list:
    return re.findall(r'[a-zA-Z]{4,}', text.lower())


ALLOWED_2CHAR_WORDS = {"ฝน", "ขัง", "กทม", "ปภ", "ทบ", "คลอง", "เขื่อน"}

def is_valid_th(token: str) -> bool:
    """เช็คว่าเป็นคำภาษาไทยที่ควรแสดง"""
    if not re.match(r'^[\u0E00-\u0E7F]+$', token):
        return False
    if token in THAI_STOPWORDS or token in SEARCH_QUERY_WORDS:
        return False
    if re.match(r'^[\u0E50-\u0E59]+$', token):  # ตัวเลขไทย
        return False
    if len(token) < 2:
        return False
    if len(token) == 2 and token not in ALLOWED_2CHAR_WORDS:
        return False
    return True


def is_valid_en(token: str) -> bool:
    """เช็คว่าเป็นคำภาษาอังกฤษที่ควรแสดง"""
    return (
        len(token) >= 4
        and token not in ENG_STOPWORDS
        and token not in SEARCH_QUERY_WORDS
        and re.match(r'^[a-zA-Z]+$', token)
    )


# ──────────────────────────────────────────────
# SCRAPERS
# ──────────────────────────────────────────────
def scrape_rss(feed_url: str) -> list:
    articles = []
    skipped_old = 0
    skipped_nodate = 0
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:50]:  # ขยาย limit เผื่อบทความเก่าโดน filter
            title = getattr(entry, "title", "") or ""
            summary = getattr(entry, "summary", "") or ""

            # ── กรองวันเวลา ──────────────────────────────────
            pub = getattr(entry, "published_parsed", None) \
                  or getattr(entry, "updated_parsed", None)
            if pub:
                # published_parsed เป็น UTC (time.struct_time)
                pub_dt = datetime(*pub[:6], tzinfo=timezone.utc)
                if pub_dt < CUTOFF_UTC:
                    skipped_old += 1
                    continue  # ข่าวเก่าเกิน HOURS_WINDOW ชั่วโมง — ข้าม
                pub_iso = pub_dt.astimezone(
                    timezone(timedelta(hours=7))
                ).strftime("%Y-%m-%d %H:%M")
                age_h = round((NOW_UTC - pub_dt).total_seconds() / 3600, 1)
            else:
                # ไม่มีวันที่ → ยังคงเก็บไว้แต่ mark ว่าไม่ทราบ
                skipped_nodate += 1
                pub_iso = "ไม่ทราบ"
                age_h = None

            # ── Clean text ───────────────────────────────────
            clean_title = clean_text(title)
            clean_summary = clean_text(summary)
            clean_summary = dedup_title_in_text(clean_title, clean_summary)
            combined = (clean_title + " " + clean_summary).strip()

            if is_flood_related(combined):
                articles.append({
                    "title": title,
                    "title_clean": clean_title,
                    "text_clean": combined,
                    "source": feed.feed.get("title", feed_url),
                    "url": getattr(entry, "link", ""),
                    "published_at": pub_iso,
                    "age_hours": age_h,
                    "date": TODAY,
                })
    except Exception as e:
        print(f"  [RSS Error] {feed_url[:50]}: {e}")

    if skipped_old:
        print(f"    ↳ ตัดออก {skipped_old} บทความ (เก่าเกิน {HOURS_WINDOW} ชม.)", end="")
    if skipped_nodate:
        print(f"  ⚠ ไม่มีวันที่ {skipped_nodate} บทความ", end="")
    if skipped_old or skipped_nodate:
        print()
    return articles


def scrape_direct(source: dict) -> list:
    articles = []
    try:
        resp = requests.get(source["url"], headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        for el in soup.select(source["selector"])[:50]:
            raw = el.get_text(separator=" ").strip()
            cleaned = clean_text(raw)
            if cleaned and is_flood_related(cleaned):
                articles.append({
                    "title": raw[:200],
                    "title_clean": cleaned[:200],
                    "text_clean": cleaned,
                    "source": source["name"],
                    "url": source["url"],
                    "date": TODAY,
                })
    except Exception as e:
        print(f"  [Direct Error] {source['name']}: {e}")
    return articles


# ──────────────────────────────────────────────
# TF-IDF WORD SCORING
# ──────────────────────────────────────────────
def build_tfidf_scores(articles: list, lang: str) -> dict:
    """
    คำนวณ TF-IDF score ต่อคำ
    - TF  = ความถี่ในบทความนั้น (normalized)
    - IDF = log(N / df) — คำที่ปรากฏทุกบทความได้ score ต่ำ
    Return: {word: tfidf_sum} เรียงจากมากไปน้อย
    """
    N = len(articles)
    if N == 0:
        return {}

    # สร้าง token list ต่อบทความ
    doc_tokens = []
    for a in articles:
        text = a["text_clean"]
        if lang == "th":
            tokens = [t for t in tokenize_th(text) if is_valid_th(t)]
        else:
            tokens = [t for t in tokenize_en(text) if is_valid_en(t)]
        doc_tokens.append(tokens)

    # คำนวณ DF (document frequency)
    df = defaultdict(int)
    for tokens in doc_tokens:
        for word in set(tokens):  # นับแต่ละบทความครั้งเดียว
            df[word] += 1

    # คำนวณ TF-IDF รวมทุกบทความ
    tfidf_sum = defaultdict(float)
    for tokens in doc_tokens:
        if not tokens:
            continue
        tf_counter = Counter(tokens)
        total = len(tokens)
        for word, count in tf_counter.items():
            tf = count / total
            idf = math.log((N + 1) / (df[word] + 1)) + 1  # smoothed IDF
            score = tf * idf
            if lang == "th":
                if word in MONITORING_KEYWORDS:
                    score *= MONITORING_BOOST_FACTOR
                elif word in RELIEF_KEYWORDS:
                    score *= RELIEF_BOOST_FACTOR
                elif word in POST_FLOOD_KEYWORDS:
                    score *= POST_FLOOD_BOOST_FACTOR
            tfidf_sum[word] += score

    # กรองคำที่ปรากฏน้อยเกินไป (< 2 บทความ) — อาจเป็น noise
    tfidf_filtered = {
        w: s for w, s in tfidf_sum.items()
        if df[w] >= 2  # ต้องปรากฏในอย่างน้อย 2 บทความ
    }

    return dict(sorted(tfidf_filtered.items(), key=lambda x: -x[1]))


def build_raw_freq(articles: list, lang: str) -> dict:
    """
    Raw frequency (ยังกรองคำค้นหาออก + dedup ข้อความ)
    ใช้ประกอบเพื่อดูจำนวนครั้งที่ปรากฏจริงๆ
    """
    counter = Counter()
    for a in articles:
        text = a["text_clean"]
        if lang == "th":
            tokens = [t for t in tokenize_th(text) if is_valid_th(t)]
        else:
            tokens = [t for t in tokenize_en(text) if is_valid_en(t)]
        counter.update(tokens)
    return dict(counter.most_common(200))


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] เริ่มกวาดข่าวน้ำท่วม วันที่ {TODAY}")
    print("=" * 60)

    all_articles = []

    # RSS
    for url in RSS_FEEDS:
        arts = scrape_rss(url)
        label = url.split('q=')[-1].split('&')[0] if 'q=' in url else url[:40]
        print(f"  RSS [{label}] → {len(arts)} บทความ")
        all_articles.extend(arts)

    # Direct
    for src in DIRECT_SOURCES:
        arts = scrape_direct(src)
        print(f"  Direct [{src['name']}] → {len(arts)} บทความ")
        all_articles.extend(arts)

    # Dedup โดยเปรียบ title_clean
    seen = set()
    unique = []
    for a in all_articles:
        key = a["title_clean"][:60].strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(a)

    print(f"\n  รวม {len(unique)} บทความ (ไม่ซ้ำ) จากทั้งหมด {len(all_articles)}")

    # ──── TF-IDF scoring ────
    print("\n  คำนวณ TF-IDF ...")
    tfidf_th = build_tfidf_scores(unique, "th")
    tfidf_en = build_tfidf_scores(unique, "en")

    # ──── Raw freq (สำหรับ tooltip แสดงจำนวนครั้ง) ────
    freq_th = build_raw_freq(unique, "th")
    freq_en = build_raw_freq(unique, "en")

    # รวม output: ใช้ TF-IDF ในการจัดลำดับ, raw freq เป็น display value
    def merge_scores(tfidf: dict, raw_freq: dict, top_n: int = 100) -> dict:
        """
        เรียงตาม TF-IDF แต่แสดงค่า raw_freq เป็น "ขนาด" ใน word cloud
        เพื่อให้ตัวเลขอ่านง่าย (ครั้งที่ปรากฏ)
        """
        top_words = list(tfidf.keys())[:top_n]
        return {w: raw_freq.get(w, 1) for w in top_words if raw_freq.get(w, 0) >= 2}

    word_cloud_th = merge_scores(tfidf_th, freq_th, 80)
    word_cloud_en = merge_scores(tfidf_en, freq_en, 60)

    # Combined: รวม TH + EN แต่ normalize scale ให้ใกล้เคียงกัน
    # (EN มักมีความถี่ต่ำกว่าเพราะบทความส่วนใหญ่เป็นไทย)
    max_th = max(word_cloud_th.values()) if word_cloud_th else 1
    max_en = max(word_cloud_en.values()) if word_cloud_en else 1
    combined = {}
    for w, v in word_cloud_th.items():
        combined[w] = round(v / max_th * 100)
    for w, v in word_cloud_en.items():
        combined[w] = round(v / max_en * 60)  # EN scale เล็กกว่า

    def get_word_category(w: str) -> str:
        if w in MONITORING_KEYWORDS:
            return "monitoring"
        elif w in RELIEF_KEYWORDS:
            return "relief"
        elif w in POST_FLOOD_KEYWORDS:
            return "post_flood"
        elif w in LOCATION_KEYWORDS:
            return "location"
        return "general"

    word_categories = {w: get_word_category(w) for w in word_cloud_th.keys()}

    # ──── Save ────
    payload = {
        "date": TODAY,
        "article_count": len(unique),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "method": "tfidf",
        "note": "คำในข้อมูลนี้ผ่านการคัดกรองด้วย TF-IDF และเพิ่มน้ำหนักคำกลุ่มเฝ้าระวังน้ำท่วม",
        "word_categories": word_categories,
        "word_freq": {
            "th": word_cloud_th,
            "en": word_cloud_en,
            "combined": combined,
        },
        "tfidf_scores": {
            "th": {k: round(v, 4) for k, v in list(tfidf_th.items())[:80]},
            "en": {k: round(v, 4) for k, v in list(tfidf_en.items())[:60]},
        },
        "articles_preview": [
            {
                "title": a["title"][:150],
                "source": a["source"],
                "url": a["url"],
            }
            for a in unique[:20]
        ],
    }

    # บันทึก daily file
    daily_file = OUTPUT_DIR / f"wordfreq_{TODAY}.json"
    with open(daily_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # บันทึก latest (Dashboard อ่าน)
    latest_file = OUTPUT_DIR / "wordfreq_latest.json"
    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # บันทึก articles
    articles_file = OUTPUT_DIR / f"articles_{TODAY}.json"
    with open(articles_file, "w", encoding="utf-8") as f:
        json.dump(
            {"date": TODAY, "count": len(unique), "articles": unique},
            f, ensure_ascii=False, indent=2
        )

    print(f"\n  บันทึก → {latest_file.name}")
    print(f"  บันทึก → {daily_file.name}")

    # แสดงผลตัวอย่าง
    print(f"\n{'='*60}")
    print(f"  คำที่บอกประเด็น (ไทย) — top 15:")
    for i, (w, v) in enumerate(list(word_cloud_th.items())[:15], 1):
        tfidf_score = round(tfidf_th.get(w, 0), 3)
        print(f"    {i:2d}. {w:<20} freq={v:3d}  tfidf={tfidf_score}")

    print(f"\n  คำที่บอกประเด็น (อังกฤษ) — top 10:")
    for i, (w, v) in enumerate(list(word_cloud_en.items())[:10], 1):
        tfidf_score = round(tfidf_en.get(w, 0), 3)
        print(f"    {i:2d}. {w:<20} freq={v:3d}  tfidf={tfidf_score}")

    print(f"\n  เสร็จสิ้น! {len(unique)} บทความ")


if __name__ == "__main__":
    main()
