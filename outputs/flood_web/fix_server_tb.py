with open('outputs/flood_web/server.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_tb = """            except Exception as exc:
                print('Google Sheets read failed:', repr(exc), flush=True)"""
new_tb = """            except Exception as exc:
                import traceback
                traceback.print_exc()
                print('Google Sheets read failed:', repr(exc), flush=True)"""

content = content.replace(old_tb, new_tb)
with open('outputs/flood_web/server.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Added traceback to server.py")
