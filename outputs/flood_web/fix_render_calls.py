import sys

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

# Add missing calls right before paginateTables();
calls = """
 renderAreas(reports, allowed);
 renderStations();
"""

js = js.replace("paginateTables();requestAnimationFrame(updateTableHints);", calls + " paginateTables();requestAnimationFrame(updateTableHints);")

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Added missing render calls!")
