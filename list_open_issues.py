import os
import urllib.request
import json
import ssl

ssl_context = ssl._create_unverified_context()

if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("GITHUB_TOKEN="):
                os.environ["GITHUB_TOKEN"] = line.strip().split("=", 1)[1].strip()

token = os.environ.get("GITHUB_TOKEN")
repo = "KarelBerka/Alphafoldology"

url = f"https://api.github.com/repos/{repo}/issues?state=open&per_page=100"
req = urllib.request.Request(url, headers={
    "Authorization": f"token {token}",
    "User-Agent": "AlphafoldologyBot"
})

try:
    with urllib.request.urlopen(req, context=ssl_context) as resp:
        issues = json.loads(resp.read().decode("utf-8"))
        print(f"Total open issues on {repo}: {len(issues)}\n")
        for i in issues:
            print(f"Issue #{i['number']}: {i['title']}")
            print(f"  URL: {i['html_url']}")
            body_preview = (i.get('body') or "").replace("\n", " ")[:150]
            print(f"  Body: {body_preview}...")
            print("-" * 60)
            
        with open("open_issues.json", "w", encoding="utf-8") as f:
            json.dump(issues, f, indent=2, ensure_ascii=False)
except Exception as e:
    print(f"Error fetching open issues: {e}")
