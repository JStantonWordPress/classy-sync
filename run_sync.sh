#!/bin/bash
# Wrapper script for cron job
cd "/Users/josephcstanton/Desktop/WordPress/velosanomain/classy-sync"
/usr/bin/python3 "/Users/josephcstanton/Desktop/WordPress/velosanomain/classy-sync/classy_transactions_sync.py" >> "/Users/josephcstanton/Desktop/WordPress/velosanomain/classy-sync/logs/cron.log" 2>&1
