import json
import re
import sys
from datetime import datetime

def validate_database(file_path="tools_data.json"):
    print(f"=== Starting Data Validation for {file_path} ===")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find database file '{file_path}'")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON: {e}")
        sys.exit(1)
        
    tools = data.get("tools", [])
    metadata = data.get("metadata", {})
    
    print(f"Loaded {len(tools)} tools from database.")
    print(f"Metadata Count: {metadata.get('total_tools')} tools declared.")
    
    errors = []
    warnings = []
    
    # Track collections for uniqueness checks
    seen_ids = {}
    seen_repos = {}
    seen_paper_dois = {}
    seen_preprint_dois = {}
    
    # DOI regex (basic checks, usually starts with 10. and has a slash)
    doi_pattern = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", re.IGNORECASE)
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    
    # Phase 1: Collect mappings and check unique ID / structure
    for idx, tool in enumerate(tools):
        tool_name = tool.get("name", f"Unnamed (Index {idx})")
        tool_id = tool.get("id")
        
        # 1. Check ID presence
        if not tool_id:
            errors.append(f"Tool at index {idx} ({tool_name}) is missing an 'id'")
            continue
            
        # 2. Check ID uniqueness
        if tool_id in seen_ids:
            errors.append(f"Duplicate Tool ID found: '{tool_id}' (first seen at index {seen_ids[tool_id]}, duplicate at index {idx})")
        else:
            seen_ids[tool_id] = idx
            
        # Collect repos (ignore null or empty)
        repo = tool.get("repo")
        if repo:
            repo_lower = repo.lower().strip()
            if repo_lower in seen_repos:
                warnings.append(f"Duplicate repository: '{repo}' is shared by tool '{tool_id}' and tool '{seen_repos[repo_lower]}'")
            else:
                seen_repos[repo_lower] = tool_id
                
        # Collect paper DOIs
        paper_doi = tool.get("paper_doi")
        if paper_doi:
            doi_clean = paper_doi.strip().lower()
            if doi_clean in seen_paper_dois:
                warnings.append(f"Duplicate Journal Paper DOI: '{paper_doi}' is shared by tool '{tool_id}' and tool '{seen_paper_dois[doi_clean]}'")
            else:
                seen_paper_dois[doi_clean] = tool_id
                
        # Collect preprint DOIs
        preprint_doi = tool.get("preprint_doi")
        if preprint_doi:
            doi_clean = preprint_doi.strip().lower()
            if doi_clean in seen_preprint_dois:
                warnings.append(f"Duplicate Preprint DOI: '{preprint_doi}' is shared by tool '{tool_id}' and tool '{seen_preprint_dois[doi_clean]}'")
            else:
                seen_preprint_dois[doi_clean] = tool_id

    # Phase 2: Detailed Field Validations
    for tool in tools:
        tool_id = tool.get("id")
        if not tool_id:
            continue
        tool_name = tool.get("name", tool_id)
        
        # 3. Check Parent existence
        parent = tool.get("parent")
        if parent and parent not in seen_ids:
            errors.append(f"Tool '{tool_id}' ({tool_name}) references non-existent parent: '{parent}'")
            
        # 4. Check Date format & timeline logic
        date_str = tool.get("date")
        date_valid = False
        if date_str:
            if not date_pattern.match(date_str):
                errors.append(f"Tool '{tool_id}' has invalid date format: '{date_str}' (expected YYYY-MM-DD)")
            else:
                try:
                    tool_date = datetime.strptime(date_str, "%Y-%m-%d")
                    date_valid = True
                except ValueError:
                    errors.append(f"Tool '{tool_id}' has invalid date calendar values: '{date_str}'")
                    
        # Parent-child chronological order validation
        if parent and parent in seen_ids and date_valid:
            parent_tool = tools[seen_ids[parent]]
            parent_date_str = parent_tool.get("date")
            if parent_date_str and date_pattern.match(parent_date_str):
                try:
                    parent_date = datetime.strptime(parent_date_str, "%Y-%m-%d")
                    if tool_date < parent_date:
                        warnings.append(f"Chronology warning: Tool '{tool_id}' (released {date_str}) is dated BEFORE its parent '{parent}' (released {parent_date_str})")
                except ValueError:
                    pass
                    
        # 5. DOI Format validations
        paper_doi = tool.get("paper_doi")
        if paper_doi:
            if not doi_pattern.match(paper_doi.strip()):
                warnings.append(f"Tool '{tool_id}' has poorly formatted paper_doi: '{paper_doi}' (does not match expected DOI structure)")
                
        preprint_doi = tool.get("preprint_doi")
        if preprint_doi:
            if not doi_pattern.match(preprint_doi.strip()):
                warnings.append(f"Tool '{tool_id}' has poorly formatted preprint_doi: '{preprint_doi}' (does not match expected DOI structure)")
                
        # 6. Publication Type Consistency
        pub_type = tool.get("publication_type")
        if pub_type == "published" and not paper_doi:
            warnings.append(f"Consistency: Tool '{tool_id}' is marked as 'published' but is missing 'paper_doi'")
        elif pub_type == "preprint" and not preprint_doi:
            warnings.append(f"Consistency: Tool '{tool_id}' is marked as 'preprint' but is missing 'preprint_doi'")
        elif pub_type == "unknown" and (paper_doi or preprint_doi):
            warnings.append(f"Consistency: Tool '{tool_id}' has publication_type 'unknown' but contains DOIs (Paper: {paper_doi}, Preprint: {preprint_doi})")

        # 7. Check links matching DOIs
        preprint_link = tool.get("preprint_link")
        if preprint_doi and preprint_link and preprint_doi not in preprint_link:
            warnings.append(f"Link mismatch: Tool '{tool_id}' preprint_link ('{preprint_link}') does not contain preprint_doi ('{preprint_doi}')")

    # Output Summary Report
    print("\n" + "="*50)
    print(f"VALIDATION COMPLETED: {len(errors)} Errors, {len(warnings)} Warnings found.")
    print("="*50)
    
    if errors:
        print("\n[!] ERRORS (Require immediate fix to prevent bugs or crashes):")
        for err in errors:
            print(f"  - {err}")
    else:
        print("\n[OK] No critical structural errors found.")
        
    if warnings:
        print("\n[WARN] WARNINGS (Review for data accuracy and quality):")
        # Print top 60 warnings to avoid spamming the screen, let user know if there are more
        max_warns = 60
        for i, warn in enumerate(warnings[:max_warns]):
            print(f"  - {warn}")
        if len(warnings) > max_warns:
            print(f"  ... and {len(warnings) - max_warns} more warnings.")
    else:
        print("\n[OK] No data quality warnings found.")
        
    return len(errors) == 0

if __name__ == "__main__":
    validate_database()
