import sys
with open("outputs/flood_web/dashboard.js", "r", encoding="utf-8") as f:
    js = f.read()
    start = js.find(" sum=")
    if start == -1: start = js.find(" sum =")
    if start == -1: start = js.find("function sum")
    print(js[start-50:start+100])
