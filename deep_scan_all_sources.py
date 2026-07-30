import os
import sys
import json
import time
import re
import ssl
import urllib.request
import urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

ssl_context = ssl._create_unverified_context()

# Load GITHUB_TOKEN from .env
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("GITHUB_TOKEN="):
                os.environ["GITHUB_TOKEN"] = line.strip().split("=", 1)[1].strip()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Load existing database tools for exact matching
existing_file = "tools_data_updated.json"
existing_repos = set()
existing_names = set()
existing_dois = set()
existing_urls = set()

if os.path.exists(existing_file):
    with open(existing_file, "r", encoding="utf-8") as f:
        db = json.load(f)
        for t in db.get("tools", []):
            if t.get("name"):
                existing_names.add(t["name"].strip().lower())
            if t.get("repo"):
                repo_clean = t["repo"].strip().lower().rstrip(".git")
                existing_repos.add(repo_clean)
                if not repo_clean.startswith("http"):
                    existing_repos.add(f"https://github.com/{repo_clean}")
                    existing_repos.add(f"https://gitlab.com/{repo_clean}")
                else:
                    for host in ["github.com/", "gitlab.com/"]:
                        parts = repo_clean.split(host)
                        if len(parts) > 1:
                            existing_repos.add(parts[1])
            if t.get("paper_doi"):
                existing_dois.add(t["paper_doi"].strip().lower().replace("https://doi.org/", ""))
            if t.get("preprint_doi"):
                existing_dois.add(t["preprint_doi"].strip().lower().replace("https://doi.org/", ""))
            if t.get("doi_link"):
                existing_urls.add(t["doi_link"].strip().lower())
            if t.get("preprint_link"):
                existing_urls.add(t["preprint_link"].strip().lower())

print(f"Loaded existing database filter: {len(existing_names)} names, {len(existing_repos)} repos, {len(existing_dois)} DOIs.", flush=True)

def http_get_json(url, headers=None, timeout=10):
    if headers is None:
        headers = {}
    headers.setdefault("User-Agent", "AlphafoldologyBot/1.0 (https://github.com/KarelBerka/Alphafoldology)")
    
    if "api.github.com" in url and GITHUB_TOKEN and "Authorization" not in headers:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
        
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ssl_context, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return None

# 1. GitHub fetcher
def fetch_github(q):
    url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}+stars:>=2&sort=updated&order=desc&per_page=30"
    data = http_get_json(url)
    results = []
    if data and "items" in data:
        for item in data["items"]:
            repo_url = item["html_url"].lower()
            full_name = item["full_name"].lower()
            name = item["name"]
            desc = item.get("description") or ""
            stars = item.get("stargazers_count", 0)
            
            if full_name in existing_repos or repo_url in existing_repos:
                continue
            if name.lower() in existing_names:
                continue
                
            text = f"{name} {desc} {' '.join(item.get('topics', []))}".lower()
            relevant_keywords = ["alphafold", "protein", "folding", "structure", "docking", "binder", "residue", "pdb", "rosetta", "esm", "chai", "boltz", "antibody", "design", "diff"]
            if any(kw in text for kw in relevant_keywords):
                results.append({
                    "platform": "GitHub",
                    "name": item["name"],
                    "full_name": item["full_name"],
                    "url": item["html_url"],
                    "description": desc,
                    "stars": stars,
                    "forks": item.get("forks_count", 0),
                    "created_at": item.get("created_at")[:10],
                    "updated_at": item.get("updated_at")[:10],
                    "topics": item.get("topics", [])
                })
    return results

# 2. GitLab fetcher
def fetch_gitlab(q):
    url = f"https://gitlab.com/api/v4/projects?search={urllib.parse.quote(q)}&order_by=updated_at&per_page=20"
    data = http_get_json(url)
    results = []
    if data and isinstance(data, list):
        for item in data:
            web_url = item.get("web_url", "").lower()
            full_name = item.get("path_with_namespace", "").lower()
            name = item.get("name", "")
            desc = item.get("description") or ""
            stars = item.get("star_count", 0)
            
            if full_name in existing_repos or web_url in existing_repos:
                continue
            if name.lower() in existing_names:
                continue
                
            text = f"{name} {desc}".lower()
            relevant_keywords = ["alphafold", "protein", "folding", "structure", "docking", "binder", "residue", "pdb", "rosetta", "esm", "chai", "boltz", "antibody", "design"]
            if any(kw in text for kw in relevant_keywords):
                results.append({
                    "platform": "GitLab",
                    "name": item.get("name"),
                    "full_name": item.get("path_with_namespace"),
                    "url": item.get("web_url"),
                    "description": desc,
                    "stars": stars,
                    "forks": item.get("forks_count", 0),
                    "created_at": item.get("created_at", "")[:10],
                    "updated_at": item.get("last_activity_at", "")[:10]
                })
    return results

# 3. HuggingFace fetcher
def fetch_huggingface(q):
    results = []
    # Models
    url_models = f"https://huggingface.co/api/models?search={urllib.parse.quote(q)}&limit=30"
    data_models = http_get_json(url_models)
    if data_models and isinstance(data_models, list):
        for m in data_models:
            m_id = m.get("id")
            if not m_id:
                continue
            hf_url = f"https://huggingface.co/{m_id}"
            if hf_url.lower() in existing_urls or m_id.lower() in existing_names:
                continue
            results.append({
                "platform": "HuggingFace Model",
                "name": m_id,
                "url": hf_url,
                "downloads": m.get("downloads", 0),
                "likes": m.get("likes", 0),
                "pipeline_tag": m.get("pipeline_tag"),
                "tags": m.get("tags", [])
            })
            
    # Spaces
    url_spaces = f"https://huggingface.co/api/spaces?search={urllib.parse.quote(q)}&limit=20"
    data_spaces = http_get_json(url_spaces)
    if data_spaces and isinstance(data_spaces, list):
        for s in data_spaces:
            s_id = s.get("id")
            if not s_id:
                continue
            hf_url = f"https://huggingface.co/spaces/{s_id}"
            if hf_url.lower() in existing_urls:
                continue
            results.append({
                "platform": "HuggingFace Space",
                "name": s_id,
                "url": hf_url,
                "likes": s.get("likes", 0),
                "sdk": s.get("sdk")
            })
    return results

# 4. bioRxiv fetcher (via EuropePMC and OpenAlex bioRxiv queries)
def fetch_biorxiv(q):
    results = []
    # EuropePMC bioRxiv specific filter
    eq = f'("{q}") AND SRC:PPR AND (PUBLISHER:"bioRxiv" OR "biorxiv")'
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={urllib.parse.quote(eq)}%20AND%20FIRST_PDATE:[2024-01-01%20TO%202026-12-31]&format=json&pageSize=25"
    data = http_get_json(url)
    if data and "resultList" in data and "result" in data["resultList"]:
        for item in data["resultList"]["result"]:
            doi = item.get("doi")
            doi_clean = doi.strip().lower() if doi else None
            title = item.get("title", "")
            
            if doi_clean and doi_clean in existing_dois:
                continue
            if title.lower() in existing_names:
                continue
                
            results.append({
                "platform": "bioRxiv",
                "title": title,
                "doi": doi_clean,
                "url": f"https://doi.org/{doi_clean}" if doi_clean else f"https://www.biorxiv.org/content/{item.get('id')}",
                "venue": "bioRxiv",
                "pub_date": item.get("firstPublicationDate"),
                "authors": item.get("authorString", "Unknown"),
                "is_preprint": True
            })
    return results

# 5. OpenAlex fetcher
def fetch_openalex(kw):
    results = []
    encoded = urllib.parse.quote(kw)
    url = f"https://api.openalex.org/works?filter=title_and_abstract.search:{encoded},from_publication_date:2024-01-01&sort=publication_date:desc&per_page=25"
    data = http_get_json(url)
    if data and "results" in data:
        for work in data["results"]:
            doi = work.get("doi")
            doi_clean = doi.replace("https://doi.org/", "").strip().lower() if doi else None
            title = work.get("title") or ""
            
            if doi_clean and doi_clean in existing_dois:
                continue
            if title.lower() in existing_names:
                continue
                
            primary_loc = work.get("primary_location") or {}
            source = primary_loc.get("source") or {}
            venue_name = source.get("display_name") or "Academic Venue"
            
            authors = []
            for a in work.get("authorships", []):
                aname = a.get("author", {}).get("display_name")
                if aname:
                    authors.append(aname)
            authors_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "")
            
            results.append({
                "platform": "OpenAlex",
                "title": title,
                "doi": doi_clean,
                "url": doi or f"https://openalex.org/{work['id'].split('/')[-1]}",
                "venue": venue_name,
                "pub_date": work.get("publication_date"),
                "citations": work.get("cited_by_count", 0),
                "authors": authors_str,
                "is_preprint": "biorxiv" in venue_name.lower() or "arxiv" in venue_name.lower() or "medrxiv" in venue_name.lower() or work.get("type") == "preprint"
            })
    return results

# 6. EuropePMC fetcher
def fetch_europepmc(eq):
    results = []
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={urllib.parse.quote(eq)}%20AND%20FIRST_PDATE:[2024-01-01%20TO%202026-12-31]&format=json&pageSize=25"
    data = http_get_json(url)
    if data and "resultList" in data and "result" in data["resultList"]:
        for item in data["resultList"]["result"]:
            doi = item.get("doi")
            doi_clean = doi.strip().lower() if doi else None
            title = item.get("title", "")
            
            if doi_clean and doi_clean in existing_dois:
                continue
            if title.lower() in existing_names:
                continue
                
            results.append({
                "platform": "EuropePMC",
                "title": title,
                "doi": doi_clean,
                "url": f"https://doi.org/{doi_clean}" if doi_clean else f"https://europepmc.org/article/{item.get('source')}/{item.get('id')}",
                "venue": item.get("journalTitle") or item.get("bookTitle") or "Preprint / Journal",
                "pub_date": item.get("firstPublicationDate"),
                "authors": item.get("authorString", "Unknown"),
                "is_preprint": item.get("pubType") == "preprint" or "biorxiv" in (item.get("journalTitle") or "").lower()
            })
    return results

def run_deep_scan():
    gh_queries = [
        "alphafold", "alphafold3", "protein-design", "rosettafold",
        "esmfold", "boltz-1", "chai-1", "protenix", "rfdiffusion",
        "protein-structure", "protein-docking", "antibody-design", "alphafold-mcp", "bindcraft"
    ]
    gl_queries = ["alphafold", "protein design", "protein prediction", "rosettafold", "esmfold", "rfdiffusion"]
    hf_queries = ["alphafold", "protein-design", "esmfold", "boltz", "chai-1", "rosettafold", "structure-prediction", "protenix"]
    biorxiv_queries = ["alphafold", "protein design", "alphafold 3", "boltz", "rfdiffusion", "structure prediction"]
    openalex_queries = ["alphafold", "protein design", "alphafold3", "chai-1", "boltz-1", "rosettafoldallatom", "antibody design"]
    epmc_queries = ['"alphafold 3"', '"protein design" AND "neural network"', '"boltz-1"', '"chai-1"', '"rfdiffusion"']

    gh_res, gl_res, hf_res, bx_res, oa_res, ep_res = [], [], [], [], [], []

    print("Running parallel queries across 6 platforms...", flush=True)

    with ThreadPoolExecutor(max_workers=12) as executor:
        gh_futures = [executor.submit(fetch_github, q) for q in gh_queries]
        gl_futures = [executor.submit(fetch_gitlab, q) for q in gl_queries]
        hf_futures = [executor.submit(fetch_huggingface, q) for q in hf_queries]
        bx_futures = [executor.submit(fetch_biorxiv, q) for q in biorxiv_queries]
        oa_futures = [executor.submit(fetch_openalex, q) for q in openalex_queries]
        ep_futures = [executor.submit(fetch_europepmc, q) for q in epmc_queries]

        for f in as_completed(gh_futures):
            res = f.result()
            if res: gh_res.extend(res)
        for f in as_completed(gl_futures):
            res = f.result()
            if res: gl_res.extend(res)
        for f in as_completed(hf_futures):
            res = f.result()
            if res: hf_res.extend(res)
        for f in as_completed(bx_futures):
            res = f.result()
            if res: bx_res.extend(res)
        for f in as_completed(oa_futures):
            res = f.result()
            if res: oa_res.extend(res)
        for f in as_completed(ep_futures):
            res = f.result()
            if res: ep_res.extend(res)

    # Deduplicate each source
    def dedup_by_key(items, key_fn):
        seen = set()
        out = []
        for item in items:
            k = key_fn(item)
            if k and k not in seen:
                seen.add(k)
                out.append(item)
        return out

    gh_final = dedup_by_key(gh_res, lambda x: x["url"].lower())
    gl_final = dedup_by_key(gl_res, lambda x: x["url"].lower())
    hf_final = dedup_by_key(hf_res, lambda x: x["url"].lower())
    bx_final = dedup_by_key(bx_res, lambda x: (x.get("doi") or x.get("title")).lower())
    oa_final = dedup_by_key(oa_res, lambda x: (x.get("doi") or x.get("title")).lower())
    ep_final = dedup_by_key(ep_res, lambda x: (x.get("doi") or x.get("title")).lower())

    scan_summary = {
        "timestamp": datetime.now().isoformat(),
        "counts": {
            "github": len(gh_final),
            "gitlab": len(gl_final),
            "huggingface": len(hf_final),
            "biorxiv": len(bx_final),
            "openalex": len(oa_final),
            "europepmc": len(ep_final)
        },
        "results": {
            "github": gh_final,
            "gitlab": gl_final,
            "huggingface": hf_final,
            "biorxiv": bx_final,
            "openalex": oa_final,
            "europepmc": ep_final
        }
    }

    with open("deep_scan_raw_results.json", "w", encoding="utf-8") as f:
        json.dump(scan_summary, f, indent=2, ensure_ascii=False)

    print(f"\nScan complete!\n - GitHub: {len(gh_final)}\n - GitLab: {len(gl_final)}\n - HuggingFace: {len(hf_final)}\n - bioRxiv: {len(bx_final)}\n - OpenAlex: {len(oa_final)}\n - EuropePMC: {len(ep_final)}", flush=True)

if __name__ == "__main__":
    run_deep_scan()
