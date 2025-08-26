# Getting Started - Classy to Google Sheets Sync

## 🎯 What This Does

This script automatically syncs all ~14,000 transactions from your Classy campaign to your Google Sheet every day at 6 AM.

## 🚀 Quick Setup (5 Steps)

### Step 1: Run the Installation
```bash
cd classy-sync
./install.sh
```

### Step 2: Set Up Google API Access
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project called "Classy Sync"
3. Enable the Google Sheets API
4. Create a Service Account
5. Download the JSON credentials file
6. Rename it to `credentials.json` and put it in this folder

**Detailed instructions**: See `setup_google_auth.md`

### Step 3: Share Your Google Sheet
1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1xCr8VSAjx-7xmD0mPtWX0gxCn_72YjF_bw20ILeXDpo/edit
2. Click "Share"
3. Add the service account email (from the credentials.json file)
4. Give it "Editor" permissions

### Step 4: Test Everything
```bash
python3 test_sync.py
```
You should see: ✅ All tests passed!

### Step 5: Run Your First Sync
```bash
python3 classy_transactions_sync.py
```

## ✅ That's It!

The script will now run automatically every day at 6 AM and update your Google Sheet with fresh data from Classy.

## 📋 What Gets Synced

- Transaction ID, amounts, fees
- Donor names and emails  
- Payment methods and dates
- Fundraising pages and teams
- Comments and tribute information
- All ~14,000 transactions from campaign #656775

## 🔍 Monitoring

Check if it's working:
```bash
# View recent logs
tail -20 logs/classy_sync.log

# Check cron job
crontab -l
```

## 🆘 Need Help?

1. **Read the logs**: `tail -f logs/classy_sync.log`
2. **Test connections**: `python3 test_sync.py`
3. **Check the detailed guides**: `README.md` and `setup_google_auth.md`

## 📁 Files You Created

- `credentials.json` ← Your Google API credentials (keep this secure!)
- `logs/` ← Log files will appear here
- `run_sync.sh` ← Created by install script
- `test_sync.py` ← Created by install script

## 🔒 Security Note

Never share or commit the `credentials.json` file - it contains your Google API access keys!
