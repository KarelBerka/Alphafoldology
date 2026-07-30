import json
import os

# New curated tools to insert/update in database with validated parent IDs
new_tools = [
    {
        "id": "rfdiffusion2",
        "name": "RFdiffusion2",
        "repo": "RosettaCommons/RFdiffusion2",
        "category": "Protein Design",
        "status": "Active",
        "parent": "rfdiffusion",
        "usage": "Next-generation generative protein design pipeline supporting all-atom diffusion, ligand-aware binder design, and complex multi-chain scaffolding.",
        "strengths": "State-of-the-art all-atom generative precision, expanded motif scaffolding, ligand-conditioned backbone design.",
        "weaknesses": "Requires substantial compute resources and GPU memory for large complex generation.",
        "date": "2024-11-15",
        "github_stars": 439,
        "github_forks": 69,
        "github_description": "Inference code for RFdiffusion2 all-atom generative protein design.",
        "doi_link": "https://github.com/RosettaCommons/RFdiffusion2",
        "publication_type": "code_repository"
    },
    {
        "id": "boltz1",
        "name": "Boltz-1 / Boltz-2",
        "repo": "boltz-community/boltz-1",
        "category": "Core Predictors",
        "status": "Active",
        "parent": "alphafold3",
        "usage": "Fully open-source biomolecular structure prediction model predicting 3D structures of proteins, RNA, DNA, and small molecule complexes.",
        "strengths": "Fully open weights and code under Apache 2.0; supports multi-entity complex prediction including small molecules and modified residues.",
        "weaknesses": "Slightly higher compute requirement for complex ligand poses compared to AF2.",
        "date": "2024-12-01",
        "github_stars": 320,
        "github_forks": 45,
        "github_description": "Open-source biomolecular structure prediction model by Boltz Community.",
        "doi_link": "https://huggingface.co/boltz-community/boltz-1",
        "publication_type": "code_repository"
    },
    {
        "id": "protenix_dock",
        "name": "Protenix-Dock",
        "repo": "bytedance/Protenix-Dock",
        "category": "Ligand Docking",
        "status": "Active",
        "parent": "alphafold3",
        "usage": "Trainable end-to-end deep learning framework for protein-ligand docking and complex structure prediction.",
        "strengths": "High binding pose accuracy; trainable end-to-end without requiring classical grid scoring functions.",
        "weaknesses": "Optimized primarily for protein-ligand pairs.",
        "date": "2025-01-20",
        "github_stars": 140,
        "github_forks": 17,
        "github_description": "An accurate and trainable end-to-end protein-ligand docking framework by ByteDance.",
        "doi_link": "https://github.com/bytedance/Protenix-Dock",
        "publication_type": "code_repository"
    },
    {
        "id": "boltzdesign1",
        "name": "BoltzDesign1",
        "repo": "yehlincho/BoltzDesign1",
        "category": "Protein Design",
        "status": "Active",
        "parent": "boltz1",
        "usage": "Generative protein design model utilizing the Boltz-1 biomolecular architecture for target-focused binder design.",
        "strengths": "Direct integration with open biomolecular prediction representations for generative sequence-structure co-design.",
        "weaknesses": "Emerging community adoption.",
        "date": "2025-02-10",
        "github_stars": 257,
        "github_forks": 46,
        "github_description": "De novo generative protein design model based on Boltz-1.",
        "doi_link": "https://github.com/yehlincho/BoltzDesign1",
        "publication_type": "code_repository"
    },
    {
        "id": "rosettafold2_ppi",
        "name": "RoseTTAFold2-PPI",
        "repo": "CongLabCode/RoseTTAFold2-PPI",
        "category": "Protein Docking",
        "status": "Active",
        "parent": "rosettafold",
        "usage": "Accelerated deep learning framework for large-scale protein-protein interaction screening and complex structure prediction.",
        "strengths": "High throughput for genome-scale PPI screening; reduced memory footprint.",
        "weaknesses": "Designed primarily for binary protein interactions.",
        "date": "2024-10-05",
        "github_stars": 133,
        "github_forks": 23,
        "github_description": "Fast deep learning methods for large-scale protein-protein interaction screening.",
        "doi_link": "https://github.com/CongLabCode/RoseTTAFold2-PPI",
        "publication_type": "code_repository"
    },
    {
        "id": "tt_bio",
        "name": "tt-bio",
        "repo": "moritztng/tt-bio",
        "category": "Fast Predictors",
        "status": "Active",
        "parent": "boltz1",
        "usage": "High-performance inference engine for protein structure prediction, binder design, and embeddings running on Tenstorrent AI hardware (Boltz-2, ESMFold2, Protenix-v2).",
        "strengths": "Hardware-agnostic/RISC-V acceleration, ultra-fast embedding and structure generation.",
        "weaknesses": "Targeted at specific hardware acceleration platforms.",
        "date": "2025-03-01",
        "github_stars": 115,
        "github_forks": 11,
        "github_description": "Run protein structure prediction, binder design, and embeddings on Tenstorrent hardware.",
        "doi_link": "https://github.com/moritztng/tt-bio",
        "publication_type": "code_repository"
    },
    {
        "id": "blatant_why",
        "name": "blatant-why",
        "repo": "001TMF/blatant-why",
        "category": "Protein Design",
        "status": "Active",
        "parent": "boltz1",
        "usage": "AI-powered biologics design campaign agent providing multi-agent orchestration across BoltzGen, PXDesign, Protenix, and 200+ cloud tools.",
        "strengths": "Autonomous multi-agent orchestration for biologics campaigns.",
        "weaknesses": "Requires cloud API keys and multi-tool configuration.",
        "date": "2025-04-12",
        "github_stars": 103,
        "github_forks": 10,
        "github_description": "AI-powered biologics design campaign agent - multi-agent orchestration.",
        "doi_link": "https://github.com/001TMF/blatant-why",
        "publication_type": "code_repository"
    },
    {
        "id": "ca_rfdiffusion",
        "name": "CA_RFDiffusion",
        "repo": "baker-laboratory/CA_RFDiffusion",
        "category": "Protein Design",
        "status": "Active",
        "parent": "rfdiffusion",
        "usage": "C-alpha backbone conditioned RFdiffusion for controlled protein backbone design.",
        "strengths": "Allows granular C-alpha path conditioning during diffusion generation.",
        "weaknesses": "Requires downstream sequence design (ProteinMPNN).",
        "date": "2024-09-18",
        "github_stars": 79,
        "github_forks": 14,
        "github_description": "C-alpha conditioned RFdiffusion model by Baker Laboratory.",
        "doi_link": "https://github.com/baker-laboratory/CA_RFDiffusion",
        "publication_type": "code_repository"
    },
    {
        "id": "patchr",
        "name": "patchr",
        "repo": "DeepFoldProtein/patchr",
        "category": "Structural Search",
        "status": "Active",
        "parent": "alphafold2",
        "usage": "3D structure inpainting and simulation-ready setup for proteins, DNA, RNA, and molecular complexes.",
        "strengths": "Fixes missing loops and gaps in predicted biomolecular assemblies.",
        "weaknesses": "Requires clean input PDB/mmCIF coordinates.",
        "date": "2025-02-01",
        "github_stars": 67,
        "github_forks": 9,
        "github_description": "Structure inpainting and simulation-ready setup for biomolecular complexes.",
        "doi_link": "https://github.com/DeepFoldProtein/patchr",
        "publication_type": "code_repository"
    },
    {
        "id": "alphafold_sovereign_mcp",
        "name": "alphafold-sovereign-mcp",
        "repo": "smaniches/alphafold-sovereign-mcp",
        "category": "Visualization",
        "status": "Active",
        "parent": "alphafold2",
        "usage": "Model Context Protocol (MCP) server allowing AI agents to query AlphaFold structures, pLDDT scores, and structural predictions directly.",
        "strengths": "Seamless integration with LLM agentic frameworks (Antigravity, Claude, Cursor).",
        "weaknesses": "Requires MCP client setup.",
        "date": "2025-05-10",
        "github_stars": 4,
        "github_forks": 1,
        "github_description": "AlphaFold Sovereign MCP Server for agentic AI workflows.",
        "doi_link": "https://github.com/smaniches/alphafold-sovereign-mcp",
        "publication_type": "code_repository"
    },
    {
        "id": "boltz_generalized_covalent",
        "name": "boltz-generalized-covalent-modification",
        "repo": "benf549/boltz-generalized-covalent-modification",
        "category": "Core Predictors",
        "status": "Active",
        "parent": "boltz1",
        "usage": "Extension enabling Boltz-1/1x to predict the 3D structure of arbitrary covalent modifications and Non-Canonical Amino Acids (ncAAs).",
        "strengths": "Handles unnatural amino acids, post-translational modifications, and covalent adducts.",
        "weaknesses": "Requires custom input SMILES/MOL specifications.",
        "date": "2025-03-15",
        "github_stars": 22,
        "github_forks": 8,
        "github_description": "Structure prediction of arbitrary covalent modifications and non-canonical amino acids.",
        "doi_link": "https://github.com/benf549/boltz-generalized-covalent-modification",
        "publication_type": "code_repository"
    },
    {
        "id": "enzymm",
        "name": "EnzyMM",
        "repo": "RayHackett/enzymm",
        "category": "Structural Search",
        "status": "Active",
        "parent": "alphafold2",
        "usage": "Enzyme Motif Miner - Geometric matching and discovery of catalytic active site motifs in predicted protein structures.",
        "strengths": "Fast catalytic triad/motif matching across millions of AlphaFold Database structures.",
        "weaknesses": "Focuses on static sidechain geometry.",
        "date": "2025-01-10",
        "github_stars": 41,
        "github_forks": 2,
        "github_description": "Geometric matching of catalytic motifs in protein structures.",
        "doi_link": "https://github.com/RayHackett/enzymm",
        "publication_type": "code_repository"
    }
]

# Update tools_data_updated.json
if os.path.exists("tools_data_updated.json"):
    with open("tools_data_updated.json", "r", encoding="utf-8") as f:
        db = json.load(f)

    tool_dict = {t["id"]: t for t in db.get("tools", [])}
    for nt in new_tools:
        tool_dict[nt["id"]] = nt

    db["tools"] = list(tool_dict.values())
    db["metadata"]["last_updated"] = "2026-07-30"
    db["metadata"]["total_tools"] = len(db["tools"])

    with open("tools_data_updated.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    print(f"Updated tools_data_updated.json: total tools = {len(db['tools'])}.")

# Update tools_data.json
if os.path.exists("tools_data.json"):
    with open("tools_data.json", "r", encoding="utf-8") as f:
        db_main = json.load(f)

    tool_dict_main = {t["id"]: t for t in db_main.get("tools", [])}
    for nt in new_tools:
        tool_dict_main[nt["id"]] = nt

    db_main["tools"] = list(tool_dict_main.values())
    db_main["metadata"]["last_updated"] = "2026-07-30"
    db_main["metadata"]["total_tools"] = len(db_main["tools"])

    with open("tools_data.json", "w", encoding="utf-8") as f:
        json.dump(db_main, f, indent=2, ensure_ascii=False)

    print(f"Updated tools_data.json: total tools = {len(db_main['tools'])}.")
