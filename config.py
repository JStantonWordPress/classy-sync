"""
Configuration file for Classy API to JSON File sync

This file contains all the configuration settings for the sync script.
Update the values below according to your setup.
"""

# Classy API Configuration
CLASSY_CLIENT_ID = '9fCzIkFOECuYvRmG'
CLASSY_CLIENT_SECRET = 'bZeoonSSBRE2L55V'
CLASSY_TOKEN_URL = 'https://api.classy.org/oauth2/auth'
CLASSY_API_BASE_URL = 'https://api.classy.org/2.0'
ORGANIZATION_ID = '70653'
CAMPAIGN_ID = '656775'  # Kept for reference, but using organization-level endpoints

# JSON File Output Configuration
# Output to classy-sync directory for better organization
OUTPUT_FILE_PATH = 'team-funds-export.json'

# Logging Configuration
LOG_FILE_PATH = 'logs/classy_sync.log'

# Script Configuration
REQUEST_TIMEOUT = 120  # Timeout for API requests in seconds (increased for large datasets)
RATE_LIMIT_DELAY = 0.5  # Delay between API requests in seconds
MAX_RETRIES = 3  # Maximum number of retry attempts for failed requests
RETRY_BACKOFF_FACTOR = 2  # Exponential backoff multiplier for retries
INITIAL_RETRY_DELAY = 1  # Initial delay before first retry (seconds)
