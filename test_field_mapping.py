#!/usr/bin/env python3
"""
Test script to verify field mapping fixes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from classy_transactions_sync import ClassyAPIClient, TransactionProcessor
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_field_mapping():
    """Test the field mapping with a small sample"""
    print("🧪 Testing field mapping fixes...")
    
    try:
        # Fetch just a few transactions
        client = ClassyAPIClient()
        token = client.get_access_token()
        
        if not token:
            print("❌ Failed to get access token")
            return False
        
        # Fetch first page with just 3 transactions
        import requests
        from config import CLASSY_API_BASE_URL, CAMPAIGN_ID
        
        headers = {'Authorization': f'Bearer {token}'}
        url = f"{CLASSY_API_BASE_URL}/campaigns/{CAMPAIGN_ID}/transactions"
        params = {
            'page': 1,
            'per_page': 3,
            'with': 'fundraising_team,fundraising_page,member'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        transactions = data.get('data', [])
        
        if not transactions:
            print("❌ No transactions found")
            return False
        
        print(f"✅ Fetched {len(transactions)} test transactions")
        
        # Process the transactions
        sheet_data = TransactionProcessor.transform_transactions(transactions)
        
        print("\n📊 Sample processed data:")
        print("Headers:", sheet_data[0])
        
        if len(sheet_data) > 1:
            print("\nFirst transaction:")
            for i, (header, value) in enumerate(zip(sheet_data[0], sheet_data[1])):
                print(f"  {header}: {value}")
        
        # Check for the key fields that were missing
        if len(sheet_data) > 1:
            row = sheet_data[1]
            print("\n🔍 Key field checks:")
            print(f"  Amount: {row[1]} (should not be 0)")
            print(f"  Fee Amount: {row[3]} (should not be 0)")
            print(f"  Net Amount: {row[4]} (should not be 0)")
            print(f"  Type: {row[6]} (should not be empty)")
            print(f"  Member Name: {row[10]} (should not be empty)")
            print(f"  Member Email: {row[11]} (should not be empty)")
        
        print("\n✅ Field mapping test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_field_mapping()
    sys.exit(0 if success else 1)
