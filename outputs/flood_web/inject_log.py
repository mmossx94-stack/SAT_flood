import sys
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

js = js.replace('layers.clearLayers();', 'console.log("Before clear:", layers.getLayers().length); layers.clearLayers(); console.log("After clear:", layers.getLayers().length);')
with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
