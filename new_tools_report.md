# 🧬 New Alphafoldology Tools & Discoveries Report (2025–2026)

**Last Updated:** July 28, 2026  
**Curated by:** Antigravity AI Agent for Karel Berka / Alphafoldology

---

## 📌 Summary of Scan Results

A comprehensive multi-platform scan was conducted across **preprints, literature, GitHub repositories, HuggingFace Hub (models & spaces), and social media platforms**.

| Platform / Source | Total Candidates Scanned | Key Highlights / New Additions |
| :--- | :--- | :--- |
| 🐙 **GitHub Repositories** | **107** candidates | `RFdiffusion2`, `BoltzDesign1`, `Protenix-Dock`, `RoseTTAFold2-PPI`, `tt-bio`, `blatant-why`, `CA_RFDiffusion` |
| 🤗 **HuggingFace Hub** | **163** models/spaces | `boltz-community/boltz-1`, `boltz-2`, `biohub/ESMFold2`, `simonduerr/boltz-1` Space, `boltzgen-1` |
| 📄 **Preprints & Literature** | **222** publications | Nature AF3 base editing paper, BMC pMHC-II benchmark, OSF Sovereign FEA Protocol, OpenAlex & EuropePMC preprints |
| 🌐 **Social & Web Pulse** | Multi-topic search | Active community discussions around open AF3 alternatives (Boltz-1, Protenix), BindCraft, and MCP integration |

---

## 🚀 Newly Discovered Featured Tools

### 1. Core Predictors & All-Atom Open Models

#### 🔹 [Boltz-1 / Boltz-2](https://huggingface.co/boltz-community/boltz-1)
- **Category:** Core Predictors
- **Origin / Parent:** Open-Source Alternative to AlphaFold 3
- **Platform:** GitHub (`boltz-community/boltz-1`) & HuggingFace (`boltz-community/boltz-1`)
- **Key Features:** Fully open weights and source code (Apache 2.0). Predicts 3D structures of protein-protein, protein-DNA/RNA, and protein-ligand complexes.
- **Social & Community Pulse:** Supported by HuggingFace Spaces (`simonduerr/boltz-1`) and active fine-tuning forks (`boltz-finetune`).

#### 🔹 [Protenix-Dock](https://github.com/bytedance/Protenix-Dock)
- **Category:** Ligand Docking / Core Predictors
- **Origin / Parent:** Protenix (ByteDance)
- **Platform:** GitHub (`bytedance/Protenix-Dock`) — 140 ⭐
- **Key Features:** Accurate and trainable end-to-end neural network for protein-ligand docking and complex prediction without classical grid scoring functions.

#### 🔹 [tt-bio](https://github.com/moritztng/tt-bio)
- **Category:** Fast Predictors
- **Origin / Parent:** Hardware Acceleration for Boltz-2, ESMFold2, Protenix-v2
- **Platform:** GitHub (`moritztng/tt-bio`) — 115 ⭐
- **Key Features:** Ultra-fast structure prediction, binder design, and embeddings optimized for RISC-V and Tenstorrent AI accelerators.

---

### 2. Generative Protein Design & Diffusion

#### 🔹 [RFdiffusion2](https://github.com/RosettaCommons/RFdiffusion2)
- **Category:** Protein Design
- **Origin / Parent:** RFdiffusion (RosettaCommons / Baker Lab)
- **Platform:** GitHub (`RosettaCommons/RFdiffusion2`) — 439 ⭐
- **Key Features:** Official inference release of RFdiffusion2, introducing all-atom generative precision, ligand-aware binder design, and multi-chain motif scaffolding.

#### 🔹 [BoltzDesign1](https://github.com/yehlincho/BoltzDesign1)
- **Category:** Protein Design
- **Origin / Parent:** Boltz-1
- **Platform:** GitHub (`yehlincho/BoltzDesign1`) — 257 ⭐
- **Key Features:** De novo protein binder design model leveraging the open Boltz-1 biomolecular representation.

#### 🔹 [blatant-why](https://github.com/001TMF/blatant-why)
- **Category:** Protein Design / Agentic AI
- **Origin / Parent:** BoltzGen, PXDesign, Protenix
- **Platform:** GitHub (`001TMF/blatant-why`) — 103 ⭐
- **Key Features:** AI-powered biologics design campaign agent orchestrating multi-agent execution across BoltzGen, Protenix, and 200+ cloud tools.

#### 🔹 [CA_RFDiffusion](https://github.com/baker-laboratory/CA_RFDiffusion)
- **Category:** Protein Design
- **Origin / Parent:** Baker Laboratory
- **Platform:** GitHub (`baker-laboratory/CA_RFDiffusion`) — 79 ⭐
- **Key Features:** C-alpha backbone conditioned RFdiffusion for guided structural backbone generation.

---

### 3. AlphaFold 3 Integration, MCP & Extensions

#### 🔹 [alphafold-sovereign-mcp](https://github.com/smaniches/alphafold-sovereign-mcp)
- **Category:** Visualization / Integration
- **Origin / Parent:** Model Context Protocol (MCP) & AlphaFold
- **Platform:** GitHub (`smaniches/alphafold-sovereign-mcp`)
- **Key Features:** MCP server allowing AI agents (Antigravity IDE, Claude, Cursor) to directly fetch, parse, and analyze AlphaFold structural predictions and pLDDT scores.

#### 🔹 [boltz-generalized-covalent-modification](https://github.com/benf549/boltz-generalized-covalent-modification)
- **Category:** Core Predictors / Extensions
- **Origin / Parent:** Boltz-1
- **Platform:** GitHub (`benf549/boltz-generalized-covalent-modification`) — 22 ⭐
- **Key Features:** Enables Boltz-1 structure prediction for non-canonical amino acids (ncAAs) and arbitrary covalent protein modifications.

#### 🔹 [EnzyMM](https://github.com/RayHackett/enzymm)
- **Category:** Structural Search
- **Origin / Parent:** AlphaFold Database / PDB
- **Platform:** GitHub (`RayHackett/enzymm`) — 41 ⭐
- **Key Features:** Enzyme Motif Miner for 3D geometric matching of catalytic active site motifs across predicted protein structures.

---

## 📊 Summary Table of Newly Curated Tools

| Tool Name | Category | Primary Source | Parent Model | Stars / Likes | Key Innovation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RFdiffusion2** | Protein Design | [GitHub](https://github.com/RosettaCommons/RFdiffusion2) | RFdiffusion | 439 ⭐ | All-atom generative diffusion & ligand binding |
| **Boltz-1 / Boltz-2** | Core Predictors | [HuggingFace](https://huggingface.co/boltz-community/boltz-1) | AlphaFold 3 | 49 👍 | Open-source biomolecular complex predictor |
| **BoltzDesign1** | Protein Design | [GitHub](https://github.com/yehlincho/BoltzDesign1) | Boltz-1 | 257 ⭐ | De novo generative binder design on Boltz-1 |
| **Protenix-Dock** | Ligand Docking | [GitHub](https://github.com/bytedance/Protenix-Dock) | Protenix | 140 ⭐ | Trainable end-to-end protein-ligand docking |
| **RoseTTAFold2-PPI** | Protein Docking | [GitHub](https://github.com/CongLabCode/RoseTTAFold2-PPI) | RoseTTAFold2 | 133 ⭐ | Fast genome-scale protein interaction screening |
| **tt-bio** | Fast Predictors | [GitHub](https://github.com/moritztng/tt-bio) | Boltz-2 / ESMFold2 | 115 ⭐ | Tenstorrent RISC-V hardware acceleration |
| **blatant-why** | Protein Design | [GitHub](https://github.com/001TMF/blatant-why) | BoltzGen / Protenix | 103 ⭐ | Multi-agent AI biologics campaign manager |
| **CA_RFDiffusion** | Protein Design | [GitHub](https://github.com/baker-laboratory/CA_RFDiffusion) | RFdiffusion | 79 ⭐ | C-alpha trajectory conditioned diffusion |
| **patchr** | Structural Search | [GitHub](https://github.com/DeepFoldProtein/patchr) | AlphaFold 2 | 67 ⭐ | Structure inpainting for DNA/RNA/protein complexes |
| **EnzyMM** | Structural Search | [GitHub](https://github.com/RayHackett/enzymm) | AlphaFold DB | 41 ⭐ | Active site catalytic motif geometric miner |
| **boltz-generalized-covalent** | Core Predictors | [GitHub](https://github.com/benf549/boltz-generalized-covalent-modification) | Boltz-1 | 22 ⭐ | Non-canonical amino acid & covalent modification support |
| **alphafold-sovereign-mcp** | Integration | [GitHub](https://github.com/smaniches/alphafold-sovereign-mcp) | AlphaFold 2 | 4 ⭐ | Model Context Protocol server for AI coding agents |

---
*Report generated by Antigravity AI Agent for the Alphafoldology database.*
