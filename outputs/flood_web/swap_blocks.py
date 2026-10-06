import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

start_grid = html.find('<div class="detailgrid">')
end_grid = html.find('<section class="panel"><div class="panel-head"><div><h2>รายละเอียดสถานีระดับน้ำ</h2>')

if start_grid != -1 and end_grid != -1:
    grid_html = html[start_grid:end_grid]
    html = html[:start_grid] + html[end_grid:]
    
    idx_footer = html.find('<footer class="foot">')
    html = html[:idx_footer] + grid_html + html[idx_footer:]
    
    with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Swapped blocks successfully!")
else:
    print("Could not find the blocks.")
