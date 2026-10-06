import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/server.py", "r", encoding="utf-8") as f:
    code = f.read()

old_pick = "pick(r, 'Record_ID Report_Date Ingested_At Region Province Disaster_Type Affected_Districts_Count Affected_Households Casualties_Deaths Water_Level_Trend Current_Status Source_URL')"
new_pick = "pick(r, 'Record_ID Report_Date Ingested_At Region Province Disaster_Type Affected_Districts_Count District_Names Affected_Subdistricts_Count Affected_Villages_Count Affected_Households Casualties_Deaths Water_Level_Trend Current_Status Source_URL')"

if old_pick in code:
    code = code.replace(old_pick, new_pick)
    print("Updated server.py pick list")

with open("outputs/flood_web/server.py", "w", encoding="utf-8") as f:
    f.write(code)

with open("outputs/flood_apps_script/Code.gs", "r", encoding="utf-8") as f:
    gs = f.read()
    
# In Code.gs it might be an array of string headers
old_gs = "'Record_ID','Report_Date','Ingested_At','Region','Province','Disaster_Type','Affected_Districts_Count','Affected_Households','Casualties_Deaths','Water_Level_Trend','Current_Status','Source_URL'"
new_gs = "'Record_ID','Report_Date','Ingested_At','Region','Province','Disaster_Type','Affected_Districts_Count','District_Names','Affected_Subdistricts_Count','Affected_Villages_Count','Affected_Households','Casualties_Deaths','Water_Level_Trend','Current_Status','Source_URL'"

if old_gs in gs:
    gs = gs.replace(old_gs, new_gs)
    print("Updated Code.gs pick list")

with open("outputs/flood_apps_script/Code.gs", "w", encoding="utf-8") as f:
    f.write(gs)

print("Done")
