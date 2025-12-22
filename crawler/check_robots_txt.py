"""
Check robots.txt for blocked sites
"""
import requests

sites = {
    "fmkorea": "https://www.fmkorea.com/robots.txt",
    "mlbpark": "https://www.mlbpark.com/robots.txt",
    "clien": "https://www.clien.net/robots.txt",
    "humoruniv": "https://www.humoruniv.com/robots.txt",
    "dogdrip": "https://www.dogdrip.net/robots.txt",
}

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Bot/1.0)'
}

for name, url in sites.items():
    print(f"\n{'='*80}")
    print(f"{name.upper()}: {url}")
    print('='*80)
    
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            content = r.text
            print(f"Content length: {len(content)} bytes\n")
            
            # Show content
            if len(content) < 2000:
                print(content)
            else:
                print(content[:2000])
                print("\n... (truncated)")
        else:
            print("No robots.txt or not accessible")
            
    except Exception as e:
        print(f"Error: {str(e)[:100]}")

print("\n" + "="*80)
print("Done!")
