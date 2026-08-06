import json
import os
import re

for file_path in ["tools_data_updated.json", "tools_data.json"]:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            db = json.load(f)

        updated = False
        for t in db.get("tools", []):
            if t.get("id") == "raygun" or "raygun" in t.get("name", "").lower():
                t["name"] = "Raygun"
                t["repo"] = "rohitsinghlab/raygun"
                t["category"] = "Protein Design"
                t["parent"] = "alphafold2"
                t["usage"] = "AI framework for template-guided protein miniaturization (shrinkage), length modification, and sequence insertion/deletion while preserving 3D structure and biological function."
                t["strengths"] = "Length-independent probabilistic autoencoder representation; shrinks natural proteins by 10–50% while preserving active site geometry and folding stability."
                t["weaknesses"] = "Template-guided design requires existing structural or sequence seed."
                t["date"] = "2026-07-29"
                t["paper_doi"] = "10.1038/s41586-026-09345-z"
                t["doi_link"] = "https://doi.org/10.1038/s41586-026-09345-z"
                t["publication_type"] = "published"
                updated = True

        if updated:
            db["metadata"]["last_updated"] = "2026-08-06"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(db, f, indent=2, ensure_ascii=False)
            print(f"Updated Raygun record in {file_path}")
