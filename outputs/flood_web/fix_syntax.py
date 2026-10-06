import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    
idx = js.find("$('areaTable').innerHTML=")
end = js.find("];}}", idx) + 4

chunk_to_remove = js[idx:end]
if len(chunk_to_remove) > 0:
    js = js[:idx] + "}\n\nrenderAreas();\nrenderStations();\n" + js[end:]
    with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
        f.write(js)
    print("Removed inline areaTable and added proper closing brace and render calls!")
else:
    print("Chunk not found.")
