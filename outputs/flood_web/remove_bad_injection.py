import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

bad_injection = """
 renderAreas(reports, allowed);
 renderStations();
 paginateTables();requestAnimationFrame(updateTableHints);"""

if bad_injection in js:
    js = js.replace(bad_injection, "\n paginateTables();requestAnimationFrame(updateTableHints);")
    with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
        f.write(js)
    print("Removed bad injection.")
else:
    print("Not found.")
