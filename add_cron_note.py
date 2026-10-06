import pathlib

paths = [
    pathlib.Path(r'f:\2569_น้ำท่วม\SAT\Dashboard\index.html'),
    pathlib.Path(r'C:\xampp\htdocs\SAT_update\Dashboard\index.html')
]

for p in paths:
    if p.exists():
        text = p.read_text(encoding='utf-8')
        
        # 1. Update News header
        old_news = "document.getElementById('newsUpdateTime').innerHTML =\n        `อัปเดตล่าสุด: ${newsData.updated_at || newsData.date} | ${newsData.article_count || 0} บทความ${methodBadge} <span class=\"badge bg-light text-dark border ms-2\"><i class=\"bi bi-arrow-repeat text-success\"></i> หน้าเว็บดึงข้อมูลอัตโนมัติ: ${newsPollTime} น.</span>`;"
        
        new_news = "const cronBadge = `<span class=\"badge bg-light text-secondary border ms-2\" style=\"font-size:0.78rem; font-weight:normal;\" title=\"ระบบหลังบ้านกวาดข้อมูลใหม่ทุก 2 ชั่วโมง\"><i class=\"bi bi-clock-history text-muted me-1\"></i>ระบบอัปเดตข้อมูลทุก 2 ชม.</span>`;\n      document.getElementById('newsUpdateTime').innerHTML =\n        `อัปเดตล่าสุด: ${newsData.updated_at || newsData.date} | ${newsData.article_count || 0} บทความ${methodBadge} ${cronBadge} <span class=\"badge bg-light text-dark border ms-2\"><i class=\"bi bi-arrow-repeat text-success\"></i> หน้าเว็บดึงข้อมูลอัตโนมัติ: ${newsPollTime} น.</span>`;"
        
        # 2. Update Trends header
        old_trends = "document.getElementById('trendsUpdateTime').innerHTML =\n        `<span class=\"badge bg-danger me-2\">ดึงตรง</span> <strong>ข้อมูลอัปเดตล่าสุด: ${trendsData.updated_at}</strong> (ย้อนหลังประจำวันที่ ${trendsData.date}) <span class=\"badge bg-light text-dark border ms-2\"><i class=\"bi bi-arrow-repeat text-success\"></i> หน้าเว็บดึงข้อมูลอัตโนมัติ: ${lastPollTime} น.</span>`;"

        new_trends = "const cronBadge = `<span class=\"badge bg-light text-secondary border ms-2\" style=\"font-size:0.78rem; font-weight:normal;\" title=\"ระบบหลังบ้านกวาดข้อมูลใหม่ทุก 2 ชั่วโมง\"><i class=\"bi bi-clock-history text-muted me-1\"></i>ระบบอัปเดตข้อมูลทุก 2 ชม.</span>`;\n      document.getElementById('trendsUpdateTime').innerHTML =\n        `<span class=\"badge bg-danger me-2\">ดึงตรง</span> <strong>ข้อมูลอัปเดตล่าสุด: ${trendsData.updated_at}</strong> (ย้อนหลังประจำวันที่ ${trendsData.date}) ${cronBadge} <span class=\"badge bg-light text-dark border ms-2\"><i class=\"bi bi-arrow-repeat text-success\"></i> หน้าเว็บดึงข้อมูลอัตโนมัติ: ${lastPollTime} น.</span>`;"

        if old_news in text:
            text = text.replace(old_news, new_news)
        else:
            print(f'old_news pattern not matched in {p}')

        if old_trends in text:
            text = text.replace(old_trends, new_trends)
        else:
            print(f'old_trends pattern not matched in {p}')

        p.write_text(text, encoding='utf-8')
        print(f'Successfully updated {p}')
