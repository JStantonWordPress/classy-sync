#!/usr/bin/env python3
"""
Test script to verify handling of transactions with missing member data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from classy_transactions_sync import ClassyAPIClient, TransactionProcessor
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_missing_member_handling():
    """Test handling of transactions with missing member data"""
    print("🧪 Testing missing member data handling...")
    
    try:
        # Fetch a larger sample to find transactions with missing member data
        client = ClassyAPIClient()
        token = client.get_access_token()
        
        if not token:
            print("❌ Failed to get access token")
            return False
        
        # Fetch multiple pages to find problematic transactions
        import requests
        from config import CLASSY_API_BASE_URL, CAMPAIGN_ID
        
        headers = {'Authorization': f'Bearer {token}'}
        all_transactions = []
        
        # Fetch a few pages to get a good sample
        for page in range(1, 4):  # Pages 1, 2, 3
            url = f"{CLASSY_API_BASE_URL}/campaigns/{CAMPAIGN_ID}/transactions"
            params = {
                'page': page,
                'per_page': 100,
                'with': 'fundraising_team,fundraising_page,member'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            transactions = data.get('data', [])
            all_transactions.extend(transactions)
            
            if len(transactions) < 100:
                break
        
        print(f"✅ Fetched {len(all_transactions)} test transactions")
        
        # Analyze member data availability
        with_member = 0
        without_member = 0
        with_top_level_data = 0
        
        for transaction in all_transactions:
            member = transaction.get('member')
            if member and isinstance(member, dict):
                with_member += 1
            else:
                without_member += 1
                # Check if top-level member data exists
                if transaction.get('member_name') or transaction.get('member_email_address'):
                    with_top_level_data += 1
        
        print(f"\n📊 Member data analysis:")
        print(f"  Transactions with member object: {with_member}")
        print(f"  Transactions without member object: {without_member}")
        print(f"  Transactions with top-level member data: {with_top_level_data}")
        
        # Process the transactions with the new logic
        sheet_data = TransactionProcessor.transform_transactions(all_transactions)
        
        print(f"\n✅ Successfully processed {len(sheet_data) - 1} transactions (including those with missing member data)")
        
        # Show some examples of how missing member data is handled
        print("\n🔍 Sample processed transactions:")
        for i in range(1, min(6, len(sheet_data))):  # Show first 5 transactions
            row = sheet_data[i]
            print(f"  Transaction {row[0]}: Name='{row[10]}', Email='{row[11]}'")
        
        print("\n✅ Missing member data handling test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_missing_member_handling()
    sys.exit(0 if success else 1)
