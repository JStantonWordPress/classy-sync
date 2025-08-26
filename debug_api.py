#!/usr/bin/env python3
"""
Debug script to examine the actual Classy API response structure
"""

import json
import requests
from config import (
    CLASSY_CLIENT_ID,
    CLASSY_CLIENT_SECRET,
    CLASSY_TOKEN_URL,
    CLASSY_API_BASE_URL,
    CAMPAIGN_ID
)

def get_access_token():
    """Get access token"""
    response = requests.post(
        CLASSY_TOKEN_URL,
        data={
            'grant_type': 'client_credentials',
            'client_id': CLASSY_CLIENT_ID,
            'client_secret': CLASSY_CLIENT_SECRET,
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        timeout=30
    )
    response.raise_for_status()
    return response.json()['access_token']

def examine_api_response():
    """Fetch and examine a sample API response"""
    token = get_access_token()
    headers = {'Authorization': f'Bearer {token}'}
    
    # Fetch first page with all related data
    url = f"{CLASSY_API_BASE_URL}/campaigns/{CAMPAIGN_ID}/transactions"
    params = {
        'page': 1,
        'per_page': 2,  # Just get 2 transactions for examination
        'with': 'fundraising_team,fundraising_page,member,campaign'
    }
    
    response = requests.get(url, headers=headers, params=params, timeout=60)
    response.raise_for_status()
    
    data = response.json()
    
    print("=== API RESPONSE STRUCTURE ===")
    print(f"Total transactions available: {data.get('total', 'unknown')}")
    print(f"Transactions in this response: {len(data.get('data', []))}")
    print()
    
    if data.get('data'):
        transaction = data['data'][0]  # First transaction
        print("=== SAMPLE TRANSACTION STRUCTURE ===")
        print(json.dumps(transaction, indent=2))
        print()
        
        print("=== AVAILABLE TOP-LEVEL FIELDS ===")
        for key in sorted(transaction.keys()):
            value = transaction[key]
            if isinstance(value, dict):
                print(f"{key}: {type(value).__name__} with keys: {list(value.keys())}")
            elif isinstance(value, list):
                print(f"{key}: {type(value).__name__} with {len(value)} items")
            else:
                print(f"{key}: {value} ({type(value).__name__})")

if __name__ == "__main__":
    examine_api_response()
