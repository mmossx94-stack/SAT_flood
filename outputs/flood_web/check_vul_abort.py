import sys

with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

js = js.replace("const sums = [sum(vulData, 'elderly')", "console.log('vulData len:', vulData.length, 'sums:', [sum(vulData, 'elderly'), sum(vulData, 'pregnant'), sum(vulData, 'children')]); const sums = [sum(vulData, 'elderly')")

with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
