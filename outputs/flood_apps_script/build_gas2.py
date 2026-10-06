import re

with open('outputs/flood_web/template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# The original has:
# (async function(){try{const res=await fetch('/api/data');DATA=await res.json();
# Let's replace the whole try block up to the geojson check.

html = html.replace("const res=await fetch('/api/data');DATA=await res.json();", "DATA = JSON.parse(await new Promise((resolve, reject) => google.script.run.withSuccessHandler(resolve).withFailureHandler(reject).getDashboardData()));")
html = html.replace("const resGeo=await fetch('/thai_provinces.json');window.PROVINCES_GEOJSON=resGeo.ok?await resGeo.json():null;", "")
html = html.replace("}catch(e){window.PROVINCES_GEOJSON=null}", "")

# Inject GeoJSON
script_start = "<script>"
injection = "<?!= HtmlService.createHtmlOutputFromFile('GeoJSON').getContent(); ?>"
html = html.replace(script_start, script_start + "\n" + injection + "\n", 1)

with open('outputs/flood_apps_script/Index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Updated Index.html")
