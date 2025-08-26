#!/bin/bash

# Classy API to Google Sheets Sync - Installation Script
# This script sets up the Python environment and cron job

set -e  # Exit on any error

echo "🚀 Setting up Classy API to Google Sheets Sync..."

# Get the absolute path of the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 Installation directory: $SCRIPT_DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p "$SCRIPT_DIR/logs"

# Check if credentials.json exists
if [ ! -f "$SCRIPT_DIR/credentials.json" ]; then
    echo "⚠️  WARNING: credentials.json not found!"
    echo "   Please follow the setup guide in setup_google_auth.md to create this file."
    echo "   The script will not work without Google API credentials."
fi

# Make the Python script executable
chmod +x "$SCRIPT_DIR/classy_transactions_sync.py"

# Test the script (dry run)
echo "🧪 Testing the script configuration..."
python3 -c "
import sys
sys.path.append('$SCRIPT_DIR')
try:
    from config import *
    print('✅ Configuration loaded successfully')
    print(f'   - Classy Campaign ID: {CAMPAIGN_ID}')
    print(f'   - Google Sheet ID: {GOOGLE_SHEET_ID}')
except Exception as e:
    print(f'❌ Configuration error: {e}')
    sys.exit(1)
"

# Set up cron job
echo "⏰ Setting up daily cron job..."

# Create a wrapper script for cron
cat > "$SCRIPT_DIR/run_sync.sh" << EOF
#!/bin/bash
# Wrapper script for cron job
cd "$SCRIPT_DIR"
/usr/bin/python3 "$SCRIPT_DIR/classy_transactions_sync.py" >> "$SCRIPT_DIR/logs/cron.log" 2>&1
EOF

chmod +x "$SCRIPT_DIR/run_sync.sh"

# Add cron job (runs daily at 6 AM)
CRON_JOB="0 6 * * * $SCRIPT_DIR/run_sync.sh"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "$SCRIPT_DIR/run_sync.sh"; then
    echo "⚠️  Cron job already exists. Skipping cron setup."
else
    # Add the cron job
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ Cron job added: Daily sync at 6:00 AM"
fi

# Create a test script
cat > "$SCRIPT_DIR/test_sync.py" << 'EOF'
#!/usr/bin/env python3
"""
Test script to verify the Classy API and Google Sheets connection
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from classy_transactions_sync import ClassyAPIClient, GoogleSheetsClient
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_classy_api():
    """Test Classy API connection"""
    print("🔍 Testing Classy API connection...")
    try:
        client = ClassyAPIClient()
        token = client.get_access_token()
        if token:
            print("✅ Classy API connection successful")
            return True
        else:
            print("❌ Failed to get Classy API token")
            return False
    except Exception as e:
        print(f"❌ Classy API error: {e}")
        return False

def test_google_sheets():
    """Test Google Sheets connection"""
    print("🔍 Testing Google Sheets connection...")
    try:
        client = GoogleSheetsClient()
        print("✅ Google Sheets connection successful")
        return True
    except Exception as e:
        print(f"❌ Google Sheets error: {e}")
        return False

def main():
    print("🧪 Running connection tests...\n")
    
    classy_ok = test_classy_api()
    sheets_ok = test_google_sheets()
    
    print("\n📊 Test Results:")
    print(f"   Classy API: {'✅ PASS' if classy_ok else '❌ FAIL'}")
    print(f"   Google Sheets: {'✅ PASS' if sheets_ok else '❌ FAIL'}")
    
    if classy_ok and sheets_ok:
        print("\n🎉 All tests passed! The sync script is ready to run.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check your configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
EOF

chmod +x "$SCRIPT_DIR/test_sync.py"

echo ""
echo "🎉 Installation completed!"
echo ""
echo "📋 Next steps:"
echo "   1. Follow setup_google_auth.md to set up Google API credentials"
echo "   2. Run: python3 test_sync.py (to test connections)"
echo "   3. Run: python3 classy_transactions_sync.py (to run a full sync)"
echo ""
echo "⏰ Cron job scheduled:"
echo "   - Runs daily at 6:00 AM"
echo "   - Logs saved to: $SCRIPT_DIR/logs/"
echo "   - To view cron jobs: crontab -l"
echo "   - To remove cron job: crontab -e (then delete the line)"
echo ""
echo "📁 Files created:"
echo "   - $SCRIPT_DIR/run_sync.sh (cron wrapper)"
echo "   - $SCRIPT_DIR/test_sync.py (connection tester)"
echo "   - $SCRIPT_DIR/logs/ (log directory)"
