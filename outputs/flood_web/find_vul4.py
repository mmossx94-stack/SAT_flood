import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    start_str = '<section class="panel"><div class="panel-head"><div><h2>กลุ่มเปราะบางเพื่อวางแผนรองรับ'
    idx = html.find(start_str)
    end = html.find('</section>', idx) + 10
    print(html[idx:end])
