"""Enable verified sites in config.py"""
import re

# Read config.py
with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Sites to enable
sites_to_enable = ['clien', 'humoruniv', 'dogdrip', 'todayhumor', 'ppomppu']

# Replace enabled: False with enabled: True for these sites
for site in sites_to_enable:
    # Find the site block and replace enabled status
    pattern = rf'("{site}":\s*{{[^}}]*?"enabled":\s*)False'
    replacement = r'\1True'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open('config.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Enabled sites:")
for site in sites_to_enable:
    print(f"  - {site}")
