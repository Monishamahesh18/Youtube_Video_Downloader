"""
Keep-alive script to prevent Railway from sleeping
Run this as a separate process or use Railway's cron job
"""
import requests
import time
import os

RAILWAY_URL = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')
if not RAILWAY_URL:
    # Try to get from environment
    RAILWAY_URL = os.environ.get('RAILWAY_STATIC_URL', '')

if RAILWAY_URL and not RAILWAY_URL.startswith('http'):
    RAILWAY_URL = f'https://{RAILWAY_URL}'

def ping_health():
    """Ping health endpoint"""
    try:
        if RAILWAY_URL:
            response = requests.get(f'{RAILWAY_URL}/health', timeout=5)
            print(f"Health check: {response.status_code}")
        else:
            print("RAILWAY_URL not set, skipping ping")
    except Exception as e:
        print(f"Error pinging: {e}")

if __name__ == '__main__':
    print("Keep-alive service started")
    print(f"Pinging: {RAILWAY_URL}/health")
    while True:
        ping_health()
        time.sleep(240)  # Ping every 4 minutes
