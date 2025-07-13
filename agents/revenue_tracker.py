from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import date, timedelta
import json
from pathlib import Path

# File paths
OUTPUT_PATH = Path("data/logs/adsense_earnings.json")
CREDENTIALS_FILE = 'config/adsense_service_account.json'

# Setup
SCOPES = ['https://www.googleapis.com/auth/adsense.readonly']
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)

adsense = build('adsense', 'v2', credentials=credentials)

def get_earnings(start_date, end_date):
    account_id = 'accounts/pub-XXXXXXX'  # Replace with your AdSense account ID

    report = adsense.accounts().reports().generate(
        account=account_id,
        dateRange='CUSTOM',
        startDate={'year': start_date.year, 'month': start_date.month, 'day': start_date.day},
        endDate={'year': end_date.year, 'month': end_date.month, 'day': end_date.day},
        metrics=['ESTIMATED_EARNINGS', 'IMPRESSIONS', 'CLICKS'],
        dimensions=['DATE']
    ).execute()

    return report.get("rows", [])

def save_data(rows):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(rows, f, indent=2)
    print(f"📊 Earnings data saved to {OUTPUT_PATH}")

def main():
    today = date.today()
    week_ago = today - timedelta(days=7)
    earnings = get_earnings(week_ago, today)

    for row in earnings:
        print(row)

    save_data(earnings)

if __name__ == "__main__":
    main()
