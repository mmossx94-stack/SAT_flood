import sys
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    start = js.find("quality=")
    if start == -1: start = js.find("quality =")
    if start == -1: start = js.find("quality(")
    print(js[max(0, start-50):start+150])
