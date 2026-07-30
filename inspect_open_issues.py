import json

with open("open_issues.json", "r", encoding="utf-8") as f:
    issues = json.load(f)

for i in issues:
    print(f"=== ISSUE #{i['number']}: {i['title']} ===")
    print(f"Author: {i['user']['login']}")
    print(f"URL: {i['html_url']}")
    print("Body:")
    print(i.get('body', 'No body'))
    print("=" * 60 + "\n")
