# Classy API to Google Sheets Sync

This Python script automatically syncs transaction data from the Classy API to a Google Sheet on a daily basis.

## 📋 Overview

- **Source**: Classy API Campaign #656775 (approximately 14,000 transactions)
- **Destination**: Google Sheet (ID: 1xCr8VSAjx-7xmD0mPtWX0gxCn_72YjF_bw20ILeXDpo)
- **Schedule**: Daily at 6:00 AM via cron job
- **Update Method**: Full refresh (clears and repopulates all data)

## 🚀 Quick Start

### 1. Run the Installation Script
```bash
cd classy-sync
chmod +x install.sh
./install.sh
```

### 2. Set Up Google API Credentials
Follow the detailed guide in `setup_google_auth.md` to:
- Create a Google Cloud project
- Enable Google Sheets API
- Create service account credentials
- Share your Google Sheet with the service account

### 3. Test the Setup
```bash
python3 test_sync.py
```

### 4. Run a Manual Sync
```bash
python3 classy_transactions_sync.py
```

## 📁 Project Structure

```
classy-sync/
├── classy_transactions_sync.py  # Main sync script
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── setup_google_auth.md         # Google API setup guide
├── install.sh                   # Installation script
├── test_sync.py                 # Connection test script
├── run_sync.sh                  # Cron job wrapper
├── credentials.json             # Google service account credentials (you create this)
├── logs/
│   ├── classy_sync.log         # Application logs
│   └── cron.log                # Cron job logs
└── README.md                   # This file
```

## ⚙️ Configuration

The script is pre-configured with your Classy API credentials and Google Sheet ID. You can modify settings in `config.py`:

- **Classy API**: Campaign ID, client credentials
- **Google Sheets**: Sheet ID, worksheet name
- **Logging**: Log file location and format
- **Performance**: Batch sizes, timeouts, rate limits

## 📊 Data Fields

The script extracts and syncs the following transaction data:

| Field | Description |
|-------|-------------|
| Transaction ID | Unique transaction identifier |
| Amount | Gross transaction amount |
| Currency | Transaction currency (USD) |
| Fee Amount | Processing fees |
| Net Amount | Net amount after fees |
| Status | Transaction status |
| Type | Transaction type |
| Payment Method | Payment method used |
| Created Date | When transaction was created |
| Updated Date | When transaction was last updated |
| Member Name | Donor's full name |
| Member Email | Donor's email address |
| Fundraising Page Title | Associated fundraising page |
| Fundraising Team Name | Associated team |
| Campaign Title | Campaign name |
| Designation | Fund designation |
| Comment | Donor comment |
| Anonymous | Whether donation is anonymous |
| Recurring | Whether it's a recurring donation |
| Tribute Type | Type of tribute (if any) |
| Tribute Name | Name of tribute (if any) |

## 🔄 Automation

### Cron Job
The installation script sets up a daily cron job that runs at 6:00 AM:
```bash
0 6 * * * /path/to/classy-sync/run_sync.sh
```

### Manual Operations
```bash
# View current cron jobs
crontab -l

# Edit cron jobs
crontab -e

# Run sync manually
python3 classy_transactions_sync.py

# Test connections
python3 test_sync.py

# View logs
tail -f logs/classy_sync.log
tail -f logs/cron.log
```

## 📝 Logging

The script provides comprehensive logging:

- **Application logs**: `logs/classy_sync.log`
  - API requests and responses
  - Data processing progress
  - Error details and stack traces
  
- **Cron logs**: `logs/cron.log`
  - Cron job execution output
  - System-level errors

## 🔧 Troubleshooting

### Common Issues

1. **"credentials.json not found"**
   - Follow `setup_google_auth.md` to create the file
   - Ensure it's in the correct directory

2. **"Permission denied" on Google Sheet**
   - Share the sheet with your service account email
   - Grant "Editor" permissions

3. **Classy API authentication failed**
   - Check your client ID and secret in `config.py`
   - Verify the API endpoint is accessible

4. **Cron job not running**
   - Check cron service: `sudo service cron status`
   - Verify cron job exists: `crontab -l`
   - Check cron logs: `tail -f logs/cron.log`

### Debug Mode

Run with verbose logging:
```bash
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
exec(open('classy_transactions_sync.py').read())
"
```

## 🔒 Security

- **Credentials**: Never commit `credentials.json` to version control
- **API Keys**: Stored in `config.py` - consider using environment variables for production
- **Permissions**: Service account only has access to explicitly shared sheets
- **Logs**: May contain sensitive data - secure appropriately

## 📈 Performance

The script is optimized for large datasets:
- **Pagination**: Handles 14,000+ transactions automatically
- **Rate Limiting**: Respects API limits with delays between requests
- **Batch Processing**: Efficient Google Sheets updates
- **Error Recovery**: Retries failed requests automatically

## 🆘 Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Run `python3 test_sync.py` to diagnose connection issues
3. Review the setup guide in `setup_google_auth.md`
4. Verify your configuration in `config.py`

## 📄 License

This script is created for Velosano's internal use for syncing Classy API data to Google Sheets.
