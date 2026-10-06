import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    print("Length of template.html:", len(html))
    print("Does it contain <style>? ", "<style>" in html)
    print("Does it contain window.vulChartInstance? ", "window.vulChartInstance" in html)
