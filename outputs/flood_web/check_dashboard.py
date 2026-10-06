import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    print("Length of dashboard.js:", len(js))
    print("Does it contain window.vulChartInstance? ", "window.vulChartInstance" in js)
