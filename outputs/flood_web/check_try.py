import sys
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    print("try count:", js.count("try{"))
    print("catch count:", js.count("catch("))
