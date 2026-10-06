import sys
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()

js = js.replace('renderDistrictWaterMap(fit);renderShelterMap();return}', 'try{renderDistrictWaterMap(fit);}catch(e){console.error("DIST_ERR:", e)} try{renderShelterMap();}catch(e){console.error("SHELTER_ERR:", e)} return}')
with open("outputs/flood_web/dashboard.js", "w", encoding="utf-8") as f:
    f.write(js)
