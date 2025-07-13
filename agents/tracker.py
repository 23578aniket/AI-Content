from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import date, timedelta
import json

# Load service account key
SERVICE_ACCOUNT_FILE = 'config/gsc_service_account.json'
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
PROPERTY_URI = 'https://yourdomain.com/'  # Must include trailing slash

# Auth setup
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('searchconsole', 'v1', credentials=credentials)


def fetch_search_analytics(start_date, end_date):
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['query', 'page'],
        'rowLimit': 50,
        'startRow': 0
    }

    response = service.searchanalytics().query(
        siteUrl=PROPERTY_URI, body=request).execute()

    return response.get('rows', [])


def save_data(rows):
    output_file = 'data/logs/search_console_data.json'
    with open(output_file, 'w') as f:
        json.dump(rows, f, indent=2)
    print(f"📊 SEO data saved to {output_file}")


def main():
    today = date.today()
    seven_days_ago = today - timedelta(days=7)
    rows = fetch_search_analytics(str(seven_days_ago), str(today))

    for row in rows:
        print(f"{row['keys'][0]} → {row['clicks']} clicks | {row['impressions']} views | CTR: {row['ctr']:.2%}")

    save_data(rows)


if __name__ == '__main__':
    main()
