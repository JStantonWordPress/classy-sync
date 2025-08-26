#!/usr/bin/env python3
"""
Classy API to JSON File Sync Script - Transactions Only

This script fetches transaction data from the Classy API and saves it to a JSON file.
It performs a full refresh of transaction data via cron job.

- Transactions are saved to team-funds-export.json in the WordPress theme directory

Author: Auto-generated for Velosano
Date: 2025-01-08
Updated: 2025-08-21 - Removed registrations processing, replaced Google Sheets with JSON output
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import requests

# Import configuration
from config import (
    CLASSY_CLIENT_ID,
    CLASSY_CLIENT_SECRET,
    CLASSY_TOKEN_URL,
    CLASSY_API_BASE_URL,
    CAMPAIGN_ID,
    OUTPUT_FILE_PATH,
    LOG_FILE_PATH,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_BACKOFF_FACTOR,
    INITIAL_RETRY_DELAY,
    RATE_LIMIT_DELAY
)


class ClassyAPIClient:
    """Client for interacting with the Classy API"""
    
    def __init__(self):
        self.access_token = None
        self.token_expires_at = 0
        
    def get_access_token(self) -> Optional[str]:
        """Get a valid access token for the Classy API"""
        # Check if current token is still valid
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
            
        # Request new token
        try:
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
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            # Set expiration with 60 second buffer
            self.token_expires_at = time.time() + token_data['expires_in'] - 60
            
            logging.info("Successfully obtained new access token")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get access token: {e}")
            return None
        except KeyError as e:
            logging.error(f"Invalid token response format: {e}")
            return None
    
    def fetch_transactions(self) -> List[Dict[str, Any]]:
        """Fetch all transactions from the Classy API with pagination and retry logic"""
        access_token = self.get_access_token()
        if not access_token:
            raise Exception("Unable to obtain access token")
        
        headers = {'Authorization': f'Bearer {access_token}'}
        all_transactions = []
        page = 1
        per_page = 100  # Classy API default/max per page
        
        while True:
            url = f"{CLASSY_API_BASE_URL}/campaigns/{CAMPAIGN_ID}/transactions"
            params = {
                'page': page,
                'per_page': per_page,
                'with': 'fundraising_team,fundraising_page,member'  # Include related data
            }
            
            # Retry logic for this page
            success = False
            for attempt in range(MAX_RETRIES + 1):  # +1 for initial attempt
                try:
                    if attempt == 0:
                        logging.info(f"Fetching page {page} of transactions...")
                    else:
                        logging.info(f"Retrying page {page} (attempt {attempt + 1}/{MAX_RETRIES + 1})...")
                    
                    response = requests.get(
                        url, 
                        headers=headers, 
                        params=params, 
                        timeout=REQUEST_TIMEOUT
                    )
                    response.raise_for_status()
                    
                    data = response.json()
                    transactions = data.get('data', [])
                    
                    # Success! Break out of retry loop
                    success = True
                    break
                    
                except requests.exceptions.Timeout as e:
                    if attempt < MAX_RETRIES:
                        retry_delay = INITIAL_RETRY_DELAY * (RETRY_BACKOFF_FACTOR ** attempt)
                        logging.warning(f"Timeout on page {page}, retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                    else:
                        logging.error(f"Final timeout on page {page} after {MAX_RETRIES + 1} attempts: {e}")
                        raise
                        
                except requests.exceptions.RequestException as e:
                    if attempt < MAX_RETRIES:
                        retry_delay = INITIAL_RETRY_DELAY * (RETRY_BACKOFF_FACTOR ** attempt)
                        logging.warning(f"Request error on page {page}, retrying in {retry_delay} seconds: {e}")
                        time.sleep(retry_delay)
                    else:
                        logging.error(f"Final error on page {page} after {MAX_RETRIES + 1} attempts: {e}")
                        raise
            
            if not success:
                raise Exception(f"Failed to fetch page {page} after {MAX_RETRIES + 1} attempts")
            
            # Process successful response
            if not transactions:
                break
                
            all_transactions.extend(transactions)
            logging.info(f"Successfully fetched {len(transactions)} transactions from page {page}")
            
            # Check if there are more pages
            if len(transactions) < per_page:
                break
                
            page += 1
            
            # Rate limiting - be respectful to the API
            time.sleep(RATE_LIMIT_DELAY)
        
        logging.info(f"Total transactions fetched: {len(all_transactions)}")
        return all_transactions
    


class JSONFileClient:
    """Client for writing transaction data to JSON file"""
    
    def __init__(self):
        self.output_path = OUTPUT_FILE_PATH
        logging.info(f"JSON file output configured for: {self.output_path}")
    
    def write_transactions(self, transactions_data: List[Dict[str, Any]]):
        """Write transaction data to JSON file"""
        try:
            # Create directory if it doesn't exist (only if there's a directory path)
            dir_path = os.path.dirname(self.output_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            
            # Prepare JSON data with metadata
            json_data = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'total_transactions': len(transactions_data),
                    'script_version': '2025-08-21'
                },
                'transactions': transactions_data
            }
            
            # Write to JSON file
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Successfully wrote {len(transactions_data)} transactions to {self.output_path}")
            
        except Exception as e:
            logging.error(f"Error writing JSON file: {e}")
            raise


class TransactionProcessor:
    """Process and transform transaction data for JSON output"""
    
    @staticmethod
    def process_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and filter transaction data for JSON output"""
        processed_transactions = []
        filtered_count = 0
        
        for transaction in transactions:
            try:
                # Skip canceled and incomplete transactions
                status = transaction.get('status', '').lower()
                if status in ['canceled', 'incomplete']:
                    filtered_count += 1
                    continue
                
                # Extract member information with fallback handling
                member = transaction.get('member')
                if member and isinstance(member, dict):
                    # Use member object data
                    first_name = member.get('first_name', '')
                    last_name = member.get('last_name', '')
                    member_name = f"{first_name} {last_name}".strip()
                    member_email = member.get('email_address', '')
                else:
                    # Fallback to top-level transaction fields
                    member_name = transaction.get('member_name', '')
                    member_email = transaction.get('member_email_address', '')
                
                # Use "Anonymous" if no name is available
                if not member_name:
                    member_name = "Anonymous"
                
                # Use empty string if no email is available
                if not member_email:
                    member_email = ""
                
                # Extract fundraising page information
                fundraising_page = transaction.get('fundraising_page', {})
                fundraising_page_id = transaction.get('fundraising_page_id', '')
                fundraising_page_title = fundraising_page.get('title', f'Page ID: {fundraising_page_id}' if fundraising_page_id else '')
                
                # Extract fundraising team information
                fundraising_team = transaction.get('fundraising_team', {})
                fundraising_team_id = transaction.get('fundraising_team_id', '')
                fundraising_team_name = fundraising_team.get('name', f'Team ID: {fundraising_team_id}' if fundraising_team_id else '')
                
                # Create processed transaction object
                processed_transaction = {
                    'transaction_id': transaction.get('id', ''),
                    'amount': transaction.get('total_gross_amount', 0),
                    'currency': transaction.get('currency_code', 'USD'),
                    'fee_amount': transaction.get('fees_amount', 0),
                    'net_amount': transaction.get('donation_net_amount', 0),
                    'status': transaction.get('status', ''),
                    'type': transaction.get('payment_type', ''),
                    'payment_method': transaction.get('payment_method', ''),
                    'created_date': TransactionProcessor._format_date(transaction.get('created_at')),
                    'updated_date': TransactionProcessor._format_date(transaction.get('updated_at')),
                    'member_name': member_name,
                    'member_email': member_email,
                    'fundraising_page_title': fundraising_page_title,
                    'fundraising_team_name': fundraising_team_name,
                    'campaign_id': transaction.get('campaign_id', ''),
                    'designation_id': transaction.get('designation_id', ''),
                    'comment': transaction.get('comment', ''),
                    'is_anonymous': transaction.get('is_anonymous', False),
                    'is_recurring': bool(transaction.get('recurring_donation_plan_id')),
                    'tribute_info': transaction.get('in_honor_of', '')
                }
                
                processed_transactions.append(processed_transaction)
                
            except Exception as e:
                logging.warning(f"Error processing transaction {transaction.get('id', 'unknown')}: {e}")
                continue
        
        processed_count = len(processed_transactions)
        logging.info(f"Processed {processed_count} transactions for JSON output")
        if filtered_count > 0:
            logging.info(f"Filtered out {filtered_count} transactions with 'canceled' or 'incomplete' status")
        
        return processed_transactions
    
    @staticmethod
    def _format_date(date_string: Optional[str]) -> str:
        """Format date string for better readability"""
        if not date_string:
            return ''
        
        try:
            # Parse ISO format date
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, AttributeError):
            return date_string


def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main execution function"""
    setup_logging()
    
    try:
        logging.info("Starting Classy transactions sync...")
        start_time = time.time()
        
        # Initialize clients
        classy_client = ClassyAPIClient()
        json_client = JSONFileClient()
        
        # Fetch and process transactions
        logging.info("Fetching transactions from Classy API...")
        transactions = classy_client.fetch_transactions()
        
        if transactions:
            # Process transaction data for JSON output
            logging.info("Processing transaction data...")
            processed_transactions = TransactionProcessor.process_transactions(transactions)
            
            # Write to JSON file
            logging.info("Writing transactions to JSON file...")
            json_client.write_transactions(processed_transactions)
            logging.info(f"Successfully saved {len(processed_transactions)} transactions to JSON file")
        else:
            logging.warning("No transactions found")
        
        # Log completion
        duration = time.time() - start_time
        logging.info(f"Sync completed successfully in {duration:.2f} seconds")
        
        # Summary
        transaction_count = len(transactions) if transactions else 0
        processed_count = len(processed_transactions) if transactions else 0
        logging.info(f"Total fetched: {transaction_count} transactions, processed: {processed_count} transactions")
        
    except Exception as e:
        logging.error(f"Sync failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
