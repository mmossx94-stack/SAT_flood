@echo off
:: ═══════════════════════════════════════════════════════════════
:: run_news_scraper.bat
:: สคริปต์รันกวาดข่าวน้ำท่วมรายวัน
:: ใช้ร่วมกับ Windows Task Scheduler เพื่อรันอัตโนมัติทุกวัน
:: ═══════════════════════════════════════════════════════════════

SET SCRIPT_DIR=%~dp0
SET LOG_DIR=%SCRIPT_DIR%news_data\logs

:: สร้างโฟลเดอร์ logs
IF NOT EXIST "%LOG_DIR%" mkdir "%LOG_DIR%"

:: รันสคริปต์
echo [%date% %time%] เริ่มกวาดข่าว... >> "%LOG_DIR%\run_log.txt"
python -X utf8 "%SCRIPT_DIR%news_scraper.py" >> "%LOG_DIR%\run_log.txt" 2>&1

IF %ERRORLEVEL% EQU 0 (
    echo [%date% %time%] สำเร็จ >> "%LOG_DIR%\run_log.txt"
) ELSE (
    echo [%date% %time%] ERROR: รหัส %ERRORLEVEL% >> "%LOG_DIR%\run_log.txt"
)

echo เสร็จสิ้น! ดูผลที่ news_data\wordfreq_latest.json
