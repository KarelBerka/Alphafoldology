import json

with open('scraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '"id": "rosettafold"' in line:
        for j in range(max(0, i - 2), min(len(lines), i + 15)):
            print(f"{j+1}: {lines[j].rstrip()}")
