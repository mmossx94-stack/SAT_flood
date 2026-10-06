import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("outputs/flood_web/template.html", "r", encoding="utf-8") as f:
    html = f.read()
    idx = html.find("$('sideTitle').textContent='ความพร้อมศูนย์พักพิง';")
    if idx == -1: print("Not found Title")
    else:
        end = html.find(";", html.find("sideSub", idx)+10)
        print("TITLE CODE:")
        print(html[idx:end+1])
    
    idx2 = html.find("$('sideBody').innerHTML =")
    if idx2 == -1: print("Not found Body")
    else:
        end2 = html.find("</table>';", idx2)
        print("\nBODY CODE:")
        print(html[idx2:end2+10])
