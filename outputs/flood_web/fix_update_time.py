import sys
sys.stdout.reconfigure(encoding="utf-8")

# Fix server.py
with open("outputs/flood_web/server.py", "r", encoding="utf-8") as f:
    server_py = f.read()

old_dis = "disasters = [pick(r, 'Record_ID Report_Date Ingested_At Region Province Disaster_Type Affected_Districts_Count District_Names Affected_Subdistricts_Count Affected_Villages_Count Affected_Households Casualties_Deaths Water_Level_Trend Current_Status Remarks Source_URL') for r in raw['Disaster_DB']]"
new_dis = "disasters = [pick(r, 'Record_ID Report_Date Ingested_At Update_Time Region Province Disaster_Type Affected_Districts_Count District_Names Affected_Subdistricts_Count Affected_Villages_Count Affected_Households Casualties_Deaths Water_Level_Trend Current_Status Remarks Source_URL') for r in raw['Disaster_DB']]"

if old_dis in server_py:
    server_py = server_py.replace(old_dis, new_dis)
    print("Fixed server.py")
else:
    print("Could not find line in server.py")

with open("outputs/flood_web/server.py", "w", encoding="utf-8") as f:
    f.write(server_py)

# Fix build_gas_final.py (it doesn't use pick(), it serializes the whole sheet, so it's already there)
