
import json, os, sys, logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

DASHBOARD_DIR = Path(__file__).resolve().parent.parent / 'Dashboard'
sys.path.append(str(DASHBOARD_DIR))

try:
    from trends_scraper import fetch_google_trends
except ImportError:
    logger.warning('trends_scraper.py not found in path')
    fetch_google_trends = None

def get_gspread_client(creds_path=None):
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    if not creds_path:
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'service_account.json')
    
    creds_file = Path(creds_path)
    if not creds_file.is_absolute():
        creds_file = Path(__file__).resolve().parent.parent / creds_path

    if not creds_file.exists():
        raise FileNotFoundError(f'Service Account file not found at: {creds_file}')

    logger.info(f'Authenticating using credentials: {creds_file}')
    creds = Credentials.from_service_account_file(str(creds_file), scopes=scopes)
    return gspread.authorize(creds)

def update_google_trends_sheet(spreadsheet, payload_data):
    tab_name = 'Google_Trends_DB'
    try:
        worksheet = spreadsheet.worksheet(tab_name)
    except Exception:
        logger.info(f'Creating new worksheet tab: {tab_name}')
        worksheet = spreadsheet.add_worksheet(title=tab_name, rows='500', cols='20')

    raw_json = json.dumps(payload_data, ensure_ascii=False)
    updated_at = payload_data.get('updated_at', datetime.now(timezone(timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S'))

    logger.info('Writing JSON payload to Cell A1...')
    worksheet.update_cell(1, 1, raw_json)
    worksheet.update_cell(1, 2, f'Updated At: {updated_at}')

    table_rows = [
        ['Keyword / Topic', 'Growth / Score', 'Category', 'Source Keyword'],
    ]

    rising = payload_data.get('rising_queries', [])
    for q in rising:
        table_rows.append([
            q.get('query', ''),
            q.get('growth', q.get('value', '')),
            'Rising Query',
            q.get('keyword', '')
        ])

    cats = payload_data.get('categorized_queries', {})
    for cat_name, items in cats.items():
        for item in items:
            table_rows.append([
                item.get('query', ''),
                item.get('growth', item.get('value', '')),
                f'Category: {cat_name}',
                item.get('keyword', 'Google Trends')
            ])

    logger.info(f'Writing {len(table_rows)} tabular rows starting at A3...')
    worksheet.update('A3', table_rows)
    logger.info(f'Successfully updated tab {tab_name}!')

def run_etl(spreadsheet_id=None, creds_path=None):
    spreadsheet_id = spreadsheet_id or os.getenv('SPREADSHEET_ID')
    if not spreadsheet_id:
        logger.error('SPREADSHEET_ID is required! Set env var SPREADSHEET_ID or pass --spreadsheet-id.')
        return False

    logger.info('=== Starting SAT Flood Data ETL Pipeline ===')

    latest_json_path = DASHBOARD_DIR / 'news_data' / 'google_trends_latest.json'
    if fetch_google_trends:
        try:
            logger.info('Fetching fresh Google Trends data...')
            fetch_google_trends()
        except Exception as e:
            logger.warning(f'fetch_google_trends failed, reading existing JSON if available: {e}')

    if not latest_json_path.exists():
        latest_json_path = DASHBOARD_DIR / 'google_trends_latest.json'

    if not latest_json_path.exists():
        logger.error(f'No Google Trends JSON file found at {latest_json_path}')
        return False

    with open(latest_json_path, 'r', encoding='utf-8') as f:
        payload_data = json.load(f)

    client = get_gspread_client(creds_path)
    logger.info(f'Opening Google Spreadsheet ID: {spreadsheet_id}')
    spreadsheet = client.open_by_key(spreadsheet_id)

    update_google_trends_sheet(spreadsheet, payload_data)
    logger.info('=== SAT Flood Data ETL Pipeline Completed Successfully ===')
    return True

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Upload SAT Flood Data and Trends to Google Sheets')
    parser.add_argument('--spreadsheet-id', help='Google Spreadsheet ID')
    parser.add_argument('--creds-file', help='Path to service_account.json')
    args = parser.parse_args()

    success = run_etl(spreadsheet_id=args.spreadsheet_id, creds_path=args.creds_file)
    sys.exit(0 if success else 1)
