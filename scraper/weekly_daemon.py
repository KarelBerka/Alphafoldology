import json
import urllib.request
import urllib.error
import datetime
import os
import sys
import argparse

# Configuration
LOG_FILE = "discovered_candidates.json"
KEYWORDS = ["alphafold", "protein-folding", "structural-biology", "protein-design"]

def fetch_json(url, headers=None):
    if headers is None:
        headers = {}
    headers.setdefault("User-Agent", "AlphafoldologyWeeklyDaemon/1.0 (mailto:KarelBerka@users.noreply.github.com)")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} for URL: {url}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e} for URL: {url}", file=sys.stderr)
    return None

def check_github(since_date_str):
    print(f"Checking GitHub repositories created since {since_date_str}...")
    new_repos = []
    
    # We search for repositories matching keywords
    for keyword in KEYWORDS:
        query_url = f"https://api.github.com/search/repositories?q={keyword}+created:>={since_date_str}&sort=stars&order=desc"
        res = fetch_json(query_url)
        if res and "items" in res:
            for item in res["items"]:
                # Check duplicate
                if not any(r["url"] == item["html_url"] for r in new_repos):
                    new_repos.append({
                        "type": "github_repository",
                        "name": item["name"],
                        "full_name": item["full_name"],
                        "url": item["html_url"],
                        "description": item["description"],
                        "stars": item["stargazers_count"],
                        "forks": item["forks_count"],
                        "created_at": item["created_at"],
                        "discovered_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
    return new_repos

def check_literature(since_date_str):
    print(f"Checking new literature on OpenAlex published since {since_date_str}...")
    new_papers = []
    
    # Query OpenAlex works with search term alphafold
    query_url = f"https://api.openalex.org/works?filter=title_and_abstract.search:alphafold,from_publication_date:{since_date_str}&sort=cited_by_count:desc"
    res = fetch_json(query_url)
    if res and "results" in res:
        for item in res["results"]:
            doi = item.get("doi")
            doi_url = doi if doi else f"https://openalex.org/{item.get('id').split('/')[-1]}"
            
            # Extract authors list
            authors = []
            for authorship in item.get("memberships", []) or item.get("authorships", []):
                author_name = authorship.get("author", {}).get("display_name")
                if author_name:
                    authors.append(author_name)
            authors_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "")
            
            # Classify preprint vs peer-reviewed
            is_preprint = False
            primary_location = item.get("primary_location", {}) or {}
            host_venue = primary_location.get("source", {}) or {}
            host_name = (host_venue.get("display_name") or "").lower()
            if "biorxiv" in host_name or "arxiv" in host_name or "medrxiv" in host_name or "preprint" in host_name:
                is_preprint = True
                
            new_papers.append({
                "type": "preprint" if is_preprint else "peer-reviewed_publication",
                "title": item.get("title"),
                "url": doi_url,
                "doi": doi.replace("https://doi.org/", "") if doi else None,
                "authors": authors_str if authors_str else "Unknown Authors",
                "journal": host_venue.get("display_name") or "Preprint Server" if is_preprint else host_venue.get("display_name") or "Scientific Journal",
                "publication_date": item.get("publication_date"),
                "discovered_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    return new_papers

def main():
    parser = argparse.ArgumentParser(description="Weekly Alphafoldology candidate checker daemon.")
    parser.add_argument("--days", type=int, default=7, help="Number of days to check back (default: 7)")
    parser.add_argument("--install", action="store_true", help="Print instructions to schedule this script via Windows Task Scheduler")
    args = parser.parse_args()

    if args.install:
        script_path = os.path.abspath(__file__)
        python_executable = sys.executable
        print("\n=== Windows Task Scheduler Registration ===")
        print("To schedule this script to run automatically every Wednesday at 9:00 AM, run the following command in PowerShell as Administrator:\n")
        
        ps_cmd = f'$action = New-ScheduledTaskAction -Execute "{python_executable}" -Argument "{script_path} --days 7"\n'
        ps_cmd += '$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Wednesday -At 9am\n'
        ps_cmd += '$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnAutomatically\n'
        ps_cmd += 'Register-ScheduledTask -TaskName "AlphafoldologyWeeklyChecker" -Action $action -Trigger $trigger -Settings $settings -Description "Weekly scan for new AlphaFold related tools and papers."'
        
        print(ps_cmd)
        print("===========================================\n")
        return

    # Calculate search threshold date
    threshold_date = (datetime.date.today() - datetime.timedelta(days=args.days)).isoformat()
    print(f"Starting scan for candidates since {threshold_date}...")
    
    new_repos = check_github(threshold_date)
    new_papers = check_literature(threshold_date)
    
    all_discovered = new_repos + new_papers
    print(f"\nDiscovered {len(new_repos)} repositories and {len(new_papers)} papers.")
    
    if all_discovered:
        # Load existing log if available
        existing_logs = []
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    existing_logs = json.load(f)
            except Exception:
                pass
                
        # Merge avoiding duplicate URLs
        new_entries_count = 0
        for entry in all_discovered:
            if not any(log["url"] == entry["url"] for log in existing_logs):
                existing_logs.append(entry)
                new_entries_count += 1
                
        # Write back
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_logs, f, indent=2, ensure_ascii=False)
            
        print(f"Logged {new_entries_count} new entries to {LOG_FILE} (Total logged: {len(existing_logs)})")
    else:
        print("No new candidates discovered in this window.")

if __name__ == "__main__":
    main()
