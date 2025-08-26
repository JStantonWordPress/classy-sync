# Google Sheets API Setup Guide

This guide will walk you through setting up Google Sheets API access for the Classy transactions sync script.

## Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click "New Project"
4. Enter a project name (e.g., "Classy Sync")
5. Click "Create"

## Step 2: Enable Google Sheets API

1. In the Google Cloud Console, make sure your new project is selected
2. Go to the [APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard)
3. Click "Enable APIs and Services"
4. Search for "Google Sheets API"
5. Click on "Google Sheets API" from the results
6. Click "Enable"

## Step 3: Create a Service Account

1. Go to [APIs & Services > Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" → "Service Account"
3. Fill in the service account details:
   - **Service account name**: `classy-sync-service`
   - **Service account ID**: (auto-generated)
   - **Description**: `Service account for Classy API to Google Sheets sync`
4. Click "Create and Continue"
5. Skip the optional steps by clicking "Done"

## Step 4: Create and Download Credentials

1. In the Credentials page, find your newly created service account
2. Click on the service account email address
3. Go to the "Keys" tab
4. Click "Add Key" → "Create new key"
5. Select "JSON" format
6. Click "Create"
7. The JSON file will be automatically downloaded to your computer

## Step 5: Set Up the Credentials File

1. Rename the downloaded JSON file to `credentials.json`
2. Move the file to your `classy-sync` directory
3. The file should be in the same directory as your Python scripts

**Important**: Keep this file secure and never commit it to version control!

## Step 6: Share Your Google Sheet

1. Open the JSON credentials file and find the `client_email` field
2. Copy the email address (it will look like: `classy-sync-service@your-project.iam.gserviceaccount.com`)
3. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1xCr8VSAjx-7xmD0mPtWX0gxCn_72YjF_bw20ILeXDpo/edit
4. Click the "Share" button in the top right
5. Paste the service account email address
6. Set permissions to "Editor"
7. Uncheck "Notify people" (since it's a service account)
8. Click "Share"

## Step 7: Verify Your Setup

Your `classy-sync` directory should now contain:
```
classy-sync/
├── classy_transactions_sync.py
├── config.py
├── requirements.txt
├── credentials.json          ← Your Google credentials file
├── setup_google_auth.md
└── logs/                     ← Will be created automatically
```

## Step 8: Test the Connection

You can test if everything is set up correctly by running:

```bash
cd classy-sync
python3 -c "
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

try:
    credentials = Credentials.from_service_account_file('credentials.json')
    service = build('sheets', 'v4', credentials=credentials)
    print('✅ Google Sheets API connection successful!')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

## Troubleshooting

### Common Issues:

1. **"File not found" error**: Make sure `credentials.json` is in the correct directory
2. **"Permission denied" error**: Make sure you shared the sheet with the service account email
3. **"API not enabled" error**: Make sure you enabled the Google Sheets API in step 2

### Security Notes:

- Never share your `credentials.json` file
- Never commit it to version control
- Consider adding `credentials.json` to your `.gitignore` file
- The service account only has access to sheets you explicitly share with it

## Next Steps

Once you've completed this setup, you can:
1. Install the Python dependencies: `pip3 install -r requirements.txt`
2. Run the sync script: `python3 classy_transactions_sync.py`
3. Set up the daily cron job using the provided installation script
