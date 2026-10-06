import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    
js = js.replace("}\n\nrenderAreas();\nrenderStations();\n", "\nrenderAreas();\nrenderStations();\n}\n")
with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
print("Moved render calls inside render()!")
