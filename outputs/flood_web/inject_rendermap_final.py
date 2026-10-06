import sys
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

js = js.replace("renderAreas();\nrenderStations();\n}", "renderMap();\nrenderAreas();\nrenderStations();\n}")
with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
