#!/usr/bin/env python3
"""
OWASP ZAP Full Scan Automation Script
Performs Spider + Active Scan on the target URL
"""

import time
import sys
from zapv2 import ZAPv2

# ZAP Configuration
ZAP_API_KEY = 'changeme'  # Default API key
ZAP_PROXY = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
TARGET_URL = 'http://localhost:5173'

print('🔍 OWASP ZAP Full Scan Starting...')
print(f'Target: {TARGET_URL}')
print('=' * 60)

try:
    # Connect to ZAP
    zap = ZAPv2(apikey=ZAP_API_KEY, proxies=ZAP_PROXY)
    
    # Test connection
    print('\n✓ Connected to ZAP')
    print(f'  ZAP Version: {zap.core.version}')
    
    # Access the URL
    print(f'\n📡 Accessing target URL: {TARGET_URL}')
    zap.urlopen(TARGET_URL)
    time.sleep(2)
    
    # Spider Scan
    print('\n🕷️  Starting Spider Scan...')
    scan_id = zap.spider.scan(TARGET_URL)
    print(f'  Spider Scan ID: {scan_id}')
    
    # Wait for spider to complete
    while int(zap.spider.status(scan_id)) < 100:
        progress = int(zap.spider.status(scan_id))
        print(f'  Spider Progress: {progress}%', end='\r')
        time.sleep(2)
    
    print(f'\n✓ Spider Scan Complete')
    print(f'  URLs Found: {len(zap.spider.results(scan_id))}')
    
    # Active Scan
    print('\n⚡ Starting Active Scan...')
    print('  This may take 30-60 minutes...')
    scan_id = zap.ascan.scan(TARGET_URL)
    print(f'  Active Scan ID: {scan_id}')
    
    # Wait for active scan to complete
    while int(zap.ascan.status(scan_id)) < 100:
        progress = int(zap.ascan.status(scan_id))
        print(f'  Active Scan Progress: {progress}%', end='\r')
        time.sleep(5)
    
    print(f'\n✓ Active Scan Complete')
    
    # Get alerts
    alerts = zap.core.alerts(baseurl=TARGET_URL)
    print(f'\n📊 Scan Results:')
    print(f'  Total Alerts: {len(alerts)}')
    
    # Count by risk
    risk_counts = {'High': 0, 'Medium': 0, 'Low': 0, 'Informational': 0}
    for alert in alerts:
        risk = alert.get('risk', 'Informational')
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
    
    print(f'\n  🔴 High: {risk_counts["High"]}')
    print(f'  🟠 Medium: {risk_counts["Medium"]}')
    print(f'  🟡 Low: {risk_counts["Low"]}')
    print(f'  🔵 Informational: {risk_counts["Informational"]}')
    
    # Generate HTML Report
    print(f'\n📄 Generating HTML Report...')
    report_html = zap.core.htmlreport()
    
    report_path = '/home/yj437/coding/aagag_clone/zap-full-scan-report.html'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_html)
    
    print(f'✓ Report saved: {report_path}')
    
    # Generate JSON Report
    import json
    report_json_path = '/home/yj437/coding/aagag_clone/zap-full-scan-report.json'
    with open(report_json_path, 'w', encoding='utf-8') as f:
        json.dump(alerts, f, indent=2)
    
    print(f'✓ JSON Report saved: {report_json_path}')
    
    print('\n' + '=' * 60)
    print('✅ Full Scan Complete!')
    print('=' * 60)
    
except Exception as e:
    print(f'\n❌ Error: {e}')
    print('\nMake sure ZAP is running with API enabled:')
    print('  zaproxy -daemon -port 8080 -config api.key=changeme')
    sys.exit(1)
