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
