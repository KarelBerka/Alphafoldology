import json
import random
import os
import datetime

def generate_database():
    random.seed(42)  # For reproducibility

    # Path to original tools_data.json
    gather_dir = "e:/Dropbox/Antigravity/Alphafoldology gather"
    input_path = os.path.join(gather_dir, "tools_data.json")
    
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    original_tools = data["tools"]
    
    # 1. Update rosettafold's parent to alphafold1
    # 2. Divide category Docking to Ligand Docking and Protein Docking
    # 3. Add date field to existing tools
    
    ligand_docking_ids = {
        "diffdock", "diffdock_l", "flowdock", "dynamicbind", "equibind", 
        "tankbind", "fabind", "unidock"
    }
    protein_docking_ids = {
        "diffdock_pp", "af2complex", "folddock", "alphapulldown"
    }

    # Set historical release dates for key tools
    historical_dates = {
        "alphafold1": "2019-12-05",
        "alphafold2": "2021-07-15",
        "rosettafold": "2021-07-15",
        "openfold": "2021-11-15",
        "colabfold": "2022-03-30",
        "foldseek": "2022-05-08",
        "esmfold": "2022-07-20",
        "esm2": "2022-07-20",
        "proteinmpnn": "2022-09-15",
        "rfdiffusion": "2023-07-11",
        "alphamissense": "2023-09-19",
        "alphafold3": "2024-05-08",
        "chai1": "2024-09-05",
        "boltz1": "2024-10-15",
    }

    start_date = datetime.date(2021, 8, 1)
    end_date = datetime.date(2026, 5, 1)
    
    def random_date(parent_date_str=None):
        if parent_date_str:
            parts = [int(x) for x in parent_date_str.split("-")]
            p_date = datetime.date(parts[0], parts[1], parts[2])
            s_date = p_date + datetime.timedelta(days=15)
            if s_date >= end_date:
                s_date = end_date - datetime.timedelta(days=30)
        else:
            s_date = start_date
        
        days_between = (end_date - s_date).days
        if days_between <= 0:
            days_between = 30
        random_days = random.randint(0, days_between)
        return (s_date + datetime.timedelta(days=random_days)).isoformat()

    updated_tools = []
    for tool in original_tools:
        tid = tool["id"]
        
        # parent fix
        if tid == "rosettafold":
            tool["parent"] = "alphafold1"
            
        # category split
        if tool["category"] == "Docking":
            if tid in ligand_docking_ids:
                tool["category"] = "Ligand Docking"
            elif tid in protein_docking_ids:
                tool["category"] = "Protein Docking"
            else:
                # default fallback
                tool["category"] = "Ligand Docking"
        
        # date assignment
        if tid in historical_dates:
            tool["date"] = historical_dates[tid]
        else:
            # Let's find parent date if available
            parent_date = None
            parent_id = tool.get("parent")
            if parent_id and parent_id in historical_dates:
                parent_date = historical_dates[parent_id]
            tool["date"] = random_date(parent_date)
            
        updated_tools.append(tool)

    # 4. Generate 900 new tools to make exactly 1001 tools
    num_to_generate = 1001 - len(updated_tools)
    print(f"Generating {num_to_generate} additional tools...")
    
    prefixes = [
        "Alpha", "Deep", "Fold", "RF", "ESM", "Uni", "Pro", "Prot", "Bio", "Gen", 
        "Helix", "Ligand", "Pocket", "Dock", "Diff", "Flow", "Cryo", "Phenix", "Open",
        "Opt", "Struct", "Model", "Quick", "Smart", "Chem", "Interact", "Affinity", "Seq",
        "Residue", "Multi", "Target", "Active", "Binding", "Symmetry", "Dynamic", "Geom"
    ]
    suffixes = [
        "Fold", "Dock", "Design", "Predict", "Align", "Search", "EM", "Fill", "Charge",
        "Find", "Scan", "Net", "Model", "Refine", "MPNN", "VAE", "GAN", "Diffusion", "BERT",
        "GPT", "TCR", "Ab", "Ig", "Link", "Map", "Score", "Metrics", "Bench", "Filter", 
        "Optimizer", "Graph", "Complex", "Solver", "Sim", "Screen", "Sense"
    ]
    
    categories = [
        "Core Predictors", "Fast Predictors", "Protein Design", "Variant Predictors",
        "Structural Search", "Ligand Docking", "Protein Docking", "Databases", "Visualization"
    ]
    
    # Track generated IDs to prevent duplicates
    existing_ids = {t["id"] for t in updated_tools}
    
    tool_counter = 0
    while len(updated_tools) < 1001:
        # Construct a unique name
        pref = random.choice(prefixes)
        suff = random.choice(suffixes)
        
        # Sometimes add a suffix number or version
        ver = ""
        if random.random() < 0.25:
            ver = f" {random.randint(2, 4)}"
            
        name = f"{pref}{suff}{ver}"
        tid = name.lower().replace(" ", "_").replace("-", "_")
        
        if tid in existing_ids:
            # Add salt to make it unique
            tool_counter += 1
            name = f"{pref}{suff} v{tool_counter}"
            tid = f"{tid}_v{tool_counter}"
            
        existing_ids.add(tid)
        
        # Select category
        category = random.choice(categories)
        
        # Select parent tool from existing list
        # To maintain lineage coherence, we select a parent in a related category
        related_parents = [t for t in updated_tools if t["category"] == category or t["category"] == "Core Predictors"]
        if not related_parents:
            related_parents = updated_tools
        parent_tool = random.choice(related_parents)
        parent_id = parent_tool["id"]
        
        # Date must be after parent date
        parent_date_str = parent_tool.get("date", "2021-07-15")
        t_date = random_date(parent_date_str)
        
        # Simulated metrics
        stars = random.randint(5, 800)
        forks = random.randint(1, 150)
        open_issues = random.randint(0, 30)
        citations = random.randint(0, 180)
        
        status = "Active" if random.random() > 0.15 else "Completed"
        
        # Simulated text properties
        usage_templates = [
            "Predicts {category} tasks using geometric deep learning and structural transformers.",
            "GPU-accelerated tool for high-throughput {category} optimization.",
            "De novo framework designed for advanced {category} pipelines.",
            "Integrates sequence embeddings with structural coordinates to enhance {category} workflow.",
            "A machine learning classifier built for robust {category} diagnostics."
        ]
        usage = random.choice(usage_templates).format(category=category.lower())
        
        strengths = random.choice([
            "Extremely fast inference time, highly optimized memory layout.",
            "State-of-the-art accuracy on target datasets, robust handling of multi-chain complexes.",
            "User-friendly API, seamless integration with structural visualizers like PyMOL.",
            "No alignment preparation steps required, supports diverse ligand libraries.",
            "Open source weights, runs locally on standard consumer GPUs."
        ])
        
        weaknesses = random.choice([
            "Reduced accuracy for disordered proteins or long flexible loop regions.",
            "High memory consumption during assembly prediction steps.",
            "Limited training dataset representation for rare post-translational modifications.",
            "Sensitive to input sequence alignment quality and MSA depth.",
            "Requires third-party solvers or pre-installed physics pipelines."
        ])
        
        new_tool = {
            "id": tid,
            "name": name,
            "repo": f"alpha-biology/{tid}",
            "category": category,
            "status": status,
            "paper_doi": None,
            "preprint_doi": None,
            "preprint_link": None,
            "parent": parent_id,
            "usage": usage,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "date": t_date,
            "github_stars": stars,
            "github_forks": forks,
            "github_open_issues": open_issues,
            "github_description": f"Official repository of {name} for advanced {category.lower()} application.",
            "github_top_forks": [
                {
                    "name": f"fork-{random.randint(1,99)}/{tid}",
                    "url": f"https://github.com/fork-{random.randint(1,99)}/{tid}",
                    "description": f"Custom fork of {name} optimizing GPU parallelization.",
                    "stars": random.randint(1, 15)
                }
            ] if random.random() > 0.5 else [],
            "citations_count": 0,
            "citing_papers": []
        }
        
        updated_tools.append(new_tool)
        
    # Re-calculate totals
    total_stars = sum(t.get("github_stars", 0) for t in updated_tools)
    total_citations = sum(t.get("citations_count", 0) for t in updated_tools)
    
    # Save the output
    database = {
        "metadata": {
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_tools": len(updated_tools),
            "total_github_stars": total_stars,
            "total_citations": total_citations
        },
        "tools": updated_tools,
        "social_posts": data.get("social_posts", [])
    }
    
    # Write back to gather tools_data.json
    with open(input_path, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
        
    print(f"Success! Saved {len(updated_tools)} tools to {input_path}")
    print(f"Total Stars: {total_stars}, Total Citations: {total_citations}")

if __name__ == "__main__":
    generate_database()
