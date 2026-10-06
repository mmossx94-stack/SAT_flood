import sys, re
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update BKK map polygons
# Old: fillColor:'transparent',fillOpacity:0
# New: fillColor:summary.status?summary.color:'transparent',fillOpacity:summary.status?0.4:0
old_poly = "fillColor:'transparent',fillOpacity:0"
new_poly = "fillColor:summary.status?summary.color:'transparent',fillOpacity:summary.status?0.4:0"
html = html.replace(old_poly, new_poly)

# 2. Add CSS for shelter-full
css = """
<style>
@keyframes pulse-scale {
  0% { transform: rotate(-45deg) scale(1); }
  50% { transform: rotate(-45deg) scale(1.35); }
  100% { transform: rotate(-45deg) scale(1); }
}
.shelter-full {
  animation: pulse-scale 1.5s infinite ease-in-out;
  border: 2px solid #fff !important;
  box-shadow: 0 2px 6px rgba(0,0,0,0.5) !important;
}
.shelter-pin-full {
  z-index: 1000 !important;
}
</style>
"""
# Insert CSS before closing head
html = html.replace('</head>', css + '</head>')

# 3. Update addShelterPins function
old_marker = "icon:L.divIcon({className:'shelter-pin',html:`<span class=\"shelter-symbol\" style=\"--shelter-color:${color}\" aria-hidden=\"true\"></span>`,iconSize:[pinSize,pinSize],iconAnchor:[pinSize/2,pinSize*1.2]}),title"

new_marker = "icon:L.divIcon({className: (status==='เต็ม' || (r.capacity>0 && r.occupied>=r.capacity)) ? 'shelter-pin shelter-pin-full' : 'shelter-pin',html:`<span class=\"shelter-symbol ${(status==='เต็ม' || (r.capacity>0 && r.occupied>=r.capacity)) ? 'shelter-full' : ''}\" style=\"--shelter-color:${color}\" aria-hidden=\"true\"></span>`,iconSize:[pinSize,pinSize],iconAnchor:[pinSize/2,pinSize*1.2]}),title"

html = html.replace(old_marker, new_marker)

with open("outputs/flood_web/template.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated BKK map and shelter pins!")
