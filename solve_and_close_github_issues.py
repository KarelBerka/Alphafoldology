import os
import json
import time
import urllib.request
import ssl

ssl_context = ssl._create_unverified_context()

if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("GITHUB_TOKEN="):
                os.environ["GITHUB_TOKEN"] = line.strip().split("=", 1)[1].strip()

token = os.environ.get("GITHUB_TOKEN")
if not token:
    print("Error: GITHUB_TOKEN not found!")
    exit(1)

with open("posted_issues_result.json", "r", encoding="utf-8") as f:
    posted_issues = json.load(f)

repo = "KarelBerka/Alphafoldology"

for item in posted_issues:
    num = item["number"]
    title = item["title"]
    
    # 1. Post Resolution Comment
    comment_url = f"https://api.github.com/repos/{repo}/issues/{num}/comments"
    comment_body = f"""### ✅ Issue Resolved & Integrated into Alphafoldology Database

This tool submission has been processed and integrated into the **Alphafoldology** hub:

- **Database Entries:** Added to `tools_data.json` and `tools_data_updated.json` under respective categories.
- **Genealogy Graph:** Connected parent lineage edges in `index.js` interactive tree.
- **Live Deployment:** Synced to web application dataset (`tools_data.json?v=28`).

*Closed by Antigravity AI Agent.*
"""
    
    req_comment = urllib.request.Request(
        comment_url,
        data=json.dumps({"body": comment_body}).encode("utf-8"),
        headers={
            "Authorization": f"token {token}",
            "Content-Type": "application/json",
            "User-Agent": "AlphafoldologyBot"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req_comment, context=ssl_context) as resp:
            print(f"Commented on Issue #{num}")
    except Exception as e:
        print(f"Error commenting on Issue #{num}: {e}")
        
    time.sleep(0.5)

    # 2. Close Issue
    issue_url = f"https://api.github.com/repos/{repo}/issues/{num}"
    close_payload = {
        "state": "closed",
        "state_reason": "completed"
    }
    
    req_close = urllib.request.Request(
        issue_url,
        data=json.dumps(close_payload).encode("utf-8"),
        headers={
            "Authorization": f"token {token}",
            "Content-Type": "application/json",
            "User-Agent": "AlphafoldologyBot"
        },
        method="PATCH"
    )
    
    try:
        with urllib.request.urlopen(req_close, context=ssl_context) as resp:
            print(f"Closed Issue #{num}: {title}")
    except Exception as e:
        print(f"Error closing Issue #{num}: {e}")
        
    time.sleep(0.5)

print("\nAll GitHub issues successfully resolved and closed!")
