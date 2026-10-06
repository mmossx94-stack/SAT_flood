import re, sys
sys.stdout.reconfigure(encoding="utf-8")

with open("outputs/flood_web/server.py", "r", encoding="utf-8") as f:
    code = f.read()

old_pick = "pick(r, 'Record_ID Report_Date Ingested_At Region Province Disaster_Type Affected_Districts_Count District_Names Affected_Subdistricts_Count Affected_Villages_Count Affected_Households Casualties_Deaths Water_Level_Trend Current_Status Source_URL')"
new_pick = "pick(r, 'Record_ID Report_Date Ingested_At Region Province Disaster_Type Affected_Districts_Count District_Names Affected_Subdistricts_Count Affected_Villages_Count Affected_Households Casualties_Deaths Water_Level_Trend Current_Status Remarks Source_URL')"

if old_pick in code:
    code = code.replace(old_pick, new_pick)
    print("Updated server.py pick list to include Remarks")
else:
    print("Could not find old pick list")

with open("outputs/flood_web/server.py", "w", encoding="utf-8") as f:
    f.write(code)
