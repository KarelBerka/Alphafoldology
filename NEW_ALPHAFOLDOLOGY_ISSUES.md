# 🧬 Alphafoldology New Projects & Tools GitHub Issues

This document contains **12 curated GitHub Issues** prepared for the **[KarelBerka/Alphafoldology](https://github.com/KarelBerka/Alphafoldology)** repository.

The issues cover newly discovered projects, preprints, repositories, models, and literature identified across **GitHub, GitLab, HuggingFace, bioRxiv, OpenAlex, and EuropePMC**.

---

## 📋 Table of Prepared Issues

| # | Title | Category | Primary Platform | Parent / Predecessor | Key Tags |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **01** | [RFdiffusion2 - All-Atom Generative Design](#issue-1-rfdiffusion2---next-gen-all-atom-generative-protein-design-pipeline) | Protein Design | GitHub (439⭐) | RFdiffusion | `all-atom`, `diffusion`, `binder-design` |
| **02** | [Boltz-1 / Boltz-2 & BoltzGen](#issue-2-boltz-1--boltz-2--boltzgen---open-source-biomolecular-complex-predictor) | Core Predictors | HuggingFace / GitHub | AlphaFold 3 | `open-weights`, `alphafold3`, `all-atom` |
| **03** | [Protenix-Dock](#issue-3-protenix-dock---end-to-end-trainable-protein-ligand-docking-framework) | Ligand Docking | GitHub (140⭐) | Protenix | `docking`, `end-to-end`, `ligand` |
| **04** | [BoltzDesign1](#issue-4-boltzdesign1---de-novo-generative-binder-design-model-based-on-boltz-1) | Protein Design | GitHub (257⭐) | Boltz-1 | `de-novo`, `binder-design`, `boltz-1` |
| **05** | [tt-bio RISC-V Acceleration](#issue-5-tt-bio---high-performance-hardware-accelerated-inference-engine) | Fast Predictors | GitHub (115⭐) | Boltz-2 / ESMFold2 | `hardware-acceleration`, `risc-v` |
| **06** | [blatant-why Biologics Agent](#issue-6-blatant-why---multi-agent-ai-biologics-design-campaign-orchestrator) | Agents & Workflows | GitHub (103⭐) | BoltzGen / Protenix | `agentic-ai`, `multi-agent`, `biologics` |
| **07** | [alphafold-sovereign-mcp](#issue-7-alphafold-sovereign-mcp---model-context-protocol-mcp-server) | MCP / Integration | GitHub | AlphaFold 2 / MCP | `mcp-server`, `agentic-ai`, `antigravity` |
| **08** | [biohub/ESMFold2](#issue-8-biohubesmfold2---next-gen-ultra-fast-protein-folding-models) | Fast Predictors | HuggingFace (388k dl) | ESMFold | `esmfold2`, `huggingface`, `single-sequence` |
| **09** | [GitLab Pipelines (HT-Colabfold & binder_design)](#issue-9-gitlab-alphafold-pipelines-ht-colabfold--binder_design) | Pipelines | GitLab | ColabFold / ESM-1b | `gitlab`, `ht-colabfold`, `binder-design` |
| **10** | [bioRxiv VR & Prosculpt Interfaces](#issue-10-biorxiv-breakthroughs-proteinsketch-vr--prosculpt-design-interfaces) | Preprints / VR | bioRxiv | De Novo Design | `biorxiv`, `vr-interface`, `proteinsketch` |
| **11** | [AntiConf & Antibody Benchmarks](#issue-11-anticonf--deep-learning-structure-evaluation-on-antibody-antigen-complexes) | Literature | EuropePMC / OpenAlex | AF Multimer | `europepmc`, `openalex`, `antibody` |
| **12** | [EnzyMM & patchr Utilities](#issue-12-enzymm--patchr---catalytic-motif-miner-and-biomolecular-inpainting-utilities) | Structural Utilities | GitHub | AlphaFold DB | `catalytic-motifs`, `inpainting`, `alphafold-db` |

---

# Issue #1: [Tool Submission]: RFdiffusion2 - Next-Gen All-Atom Generative Protein Design Pipeline

**Platform Source:** GitHub  
**Category:** Protein Design  
**Parent Node / Genealogy:** RFdiffusion (Baker Lab / RosettaCommons)  
**Target Tags:** `protein-design`, `all-atom`, `diffusion`, `binder-design`, `de-novo`  

---

## 📌 Description & Context
RFdiffusion2 is the next-generation inference release for generative protein design from RosettaCommons and the Baker Laboratory. It advances beyond backbone-only diffusion to support full all-atom generative precision, ligand-aware binder design, and complex multi-chain motif scaffolding.

## 🔗 Key Links & References
- **Primary Link:** [https://github.com/RosettaCommons/RFdiffusion2](https://github.com/RosettaCommons/RFdiffusion2)
- **Reference / DOI:** [https://github.com/RosettaCommons/RFdiffusion2](https://github.com/RosettaCommons/RFdiffusion2)

## ✨ Key Features & Innovations
- Full all-atom generative diffusion replacing classical backbone-only generation.
- Ligand-conditioned protein binder design capability.
- Advanced multi-chain motif scaffolding for active site engineering.

## ⚖️ Strengths & Limitations
- **Strengths:** State-of-the-art accuracy; direct all-atom generation without mandatory separate sidechain repacking.
- **Limitations:** High GPU memory requirements for multi-chain all-atom diffusion.

## 📋 Suggested Action Items for Alphafoldology Repository
- [ ] Add tool entry to `tools_data_updated.json` under `Protein Design`.
- [ ] Connect parent edge to `RFdiffusion (Baker Lab / RosettaCommons)` in `index.js` interactive genealogy map.
- [ ] Update badge indicators (GitHub stars, HuggingFace downloads, DOI links).
- [ ] Tag entry with: `protein-design`, `all-atom`, `diffusion`, `binder-design`, `de-novo`.

---

# Issue #2: [Tool Submission]: Boltz-1 / Boltz-2 & BoltzGen - Open-Source Biomolecular Complex Predictor and Design Framework

**Platform Source:** HuggingFace & GitHub  
**Category:** Core Predictors  
**Parent Node / Genealogy:** AlphaFold 3  
**Target Tags:** `open-weights`, `alphafold3-alternative`, `biomolecular-complexes`, `protein-ligand`, `huggingface`  

---

## 📌 Description & Context
Boltz-1 and Boltz-2 are fully open-source biomolecular structure prediction models licensed under Apache 2.0. They predict 3D structures of proteins, RNA, DNA, and small molecule complexes with performance competitive to AlphaFold 3. Accompanied by BoltzGen-1 on HuggingFace Hub for generative target-conditioned binder design.

## 🔗 Key Links & References
- **Primary Link:** [https://huggingface.co/boltz-community/boltz-1](https://huggingface.co/boltz-community/boltz-1)
- **Reference / DOI:** [https://huggingface.co/boltzgen/boltzgen-1](https://huggingface.co/boltzgen/boltzgen-1)

## ✨ Key Features & Innovations
- 100% open weights, open training dataset pipeline, and Apache 2.0 code.
- Supports protein, nucleic acid, small molecule, and post-translational modification complexes.
- Ecosystem support including HuggingFace Spaces (`simonduerr/boltz-1`) and `boltzgen-1` design model.

## ⚖️ Strengths & Limitations
- **Strengths:** Completely open for commercial and academic use; rich community extensions.
- **Limitations:** Inference time for large multi-ligand complexes requires modern GPU hardware.

## 📋 Suggested Action Items for Alphafoldology Repository
- [ ] Add tool entry to `tools_data_updated.json` under `Core Predictors`.
- [ ] Connect parent edge to `AlphaFold 3` in `index.js` interactive genealogy map.
- [ ] Update badge indicators (GitHub stars, HuggingFace downloads, DOI links).
- [ ] Tag entry with: `open-weights`, `alphafold3-alternative`, `biomolecular-complexes`, `protein-ligand`, `huggingface`.

---

# Issue #3: [Tool Submission]: Protenix-Dock - End-to-End Trainable Protein-Ligand Docking Framework

**Platform Source:** GitHub  
**Category:** Ligand Docking  
**Parent Node / Genealogy:** Protenix (ByteDance)  
**Target Tags:** `protein-docking`, `ligand-binding`, `deep-learning`, `end-to-end`  

---

## 📌 Description & Context
Protenix-Dock is ByteDance's accurate, end-to-end trainable deep learning framework for protein-ligand docking and complex structure prediction. It circumvents traditional grid search scoring functions by directly learning docking poses from biomolecular representations.

## 🔗 Key Links & References
- **Primary Link:** [https://github.com/bytedance/Protenix-Dock](https://github.com/bytedance/Protenix-Dock)
- **Reference / DOI:** [https://github.com/bytedance/Protenix-Dock](https://github.com/bytedance/Protenix-Dock)

## ✨ Key Features & Innovations
- Trainable end-to-end deep learning framework for protein-ligand docking.
- Outperforms classical docking programs on flexible binding pocket scenarios.
- Integrated into ByteDance's open structural biology stack.

## ⚖️ Strengths & Limitations
- **Strengths:** Eliminates rigid receptor assumptions and classical scoring function grid errors.
- **Limitations:** Requires pre-computed protein structure or co-prediction.

## 📋 Suggested Action Items for Alphafoldology Repository
- [ ] Add tool entry to `tools_data_updated.json` under `Ligand Docking`.
- [ ] Connect parent edge to `Protenix (ByteDance)` in `index.js` interactive genealogy map.
- [ ] Update badge indicators (GitHub stars, HuggingFace downloads, DOI links).
- [ ] Tag entry with: `protein-docking`, `ligand-binding`, `deep-learning`, `end-to-end`.

---

# Issue #4: [Tool Submission]: BoltzDesign1 - De Novo Generative Binder Design Model Based on Boltz-1

**Platform Source:** GitHub  
**Category:** Protein Design  
**Parent Node / Genealogy:** Boltz-1  
**Target Tags:** `de-novo`, `binder-design`, `boltz-1`, `generative-ai`  

---

## 📌 Description & Context
BoltzDesign1 is a de novo generative protein binder design architecture built on top of the Boltz-1 biomolecular representation. It enables target-focused binder sequence and structure co-design using open-weights biomolecular embeddings.

## 🔗 Key Links & References
- **Primary Link:** [https://github.com/yehlincho/BoltzDesign1](https://github.com/yehlincho/BoltzDesign1)
- **Reference / DOI:** [https://github.com/yehlincho/BoltzDesign1](https://github.com/yehlincho/BoltzDesign1)

## ✨ Key Features & Innovations
- Direct generative design using Boltz-1 all-atom embeddings.
- Sequence-structure co-design optimized for target surface binding.
- Full compatibility with open biomolecular prediction stacks.

## ⚖️ Strengths & Limitations
- **Strengths:** Fast binder candidate generation without relying on proprietary AF3 servers.
- **Limitations:** Emerging repository; relies on Boltz-1 backbone checkpoint.

## 📋 Suggested Action Items for Alphafoldology Repository
- [ ] Add tool entry to `tools_data_updated.json` under `Protein Design`.
- [ ] Connect parent edge to `Boltz-1` in `index.js` interactive genealogy map.
- [ ] Update badge indicators (GitHub stars, HuggingFace downloads, DOI links).
- [ ] Tag entry with: `de-novo`, `binder-design`, `boltz-1`, `generative-ai`.

---

# Issue #5: [Tool Submission]: tt-bio - High-Performance Hardware-Accelerated Inference Engine for Boltz-2 & ESMFold2

**Platform Source:** GitHub  
**Category:** Fast Predictors  
**Parent Node / Genealogy:** Boltz-2 / ESMFold2  
**Target Tags:** `hardware-acceleration`, `risc-v`, `tenstorrent`, `fast-inference`, `embeddings`  

---

## 📌 Description & Context
tt-bio is a dedicated high-performance inference engine for running protein structure prediction (Boltz-2, ESMFold2, Protenix-v2), binder design, and protein embeddings on Tenstorrent RISC-V AI hardware.

## 🔗 Key Links & References
- **Primary Link:** [https://github.com/moritztng/tt-bio](https://github.com/moritztng/tt-bio)
- **Reference / DOI:** [https://github.com/moritztng/tt-bio](https://github.com/moritztng/tt-bio)

## ✨ Key Features & Innovations
- RISC-V and specialized AI hardware acceleration for structural biology models.
- Sub-second protein embedding and rapid batch structure prediction.
- Open hardware-software stack for bio-compute clusters.

## ⚖️ Strengths & Limitations
- **Strengths:** Dramatic cost and energy reduction for ultra-high-throughput protein screening.
- **Limitations:** Optimized specifically for Tenstorrent RISC-V hardware architecture.

## 📋 Suggested Action Items for Alphafoldology Repository
- [ ] Add tool entry to `tools_data_updated.json` under `Fast Predictors`.
- [ ] Connect parent edge to `Boltz-2 / ESMFold2` in `index.js` interactive genealogy map.
- [ ] Update badge indicators (GitHub stars, HuggingFace downloads, DOI links).
- [ ] Tag entry with: `hardware-acceleration`, `risc-v`, `tenstorrent`, `fast-inference`, `embeddings`.

---

# Issue #6: [Tool Submission]: blatant-why - Multi-Agent AI Biologics Design Campaign Orchestrator

**Platform Source:** GitHub  
**Category:** Agents & Workflows  
**Parent Node / Genealogy:** BoltzGen / Protenix / RFdiffusion  
**Target Tags:** `agentic-ai`, `multi-agent`, `biologics-design`, `automation`, `campaign-manager`  

---

## 📌 Description & Context
blatant-why is an autonomous AI-powered biologics design campaign agent. It orchestrates multi-agent execution across BoltzGen, PXDesign, Protenix, RFdiffusion, and over 200 cloud computational biology tools.

## 🔗 Key Links & References
- **Primary Link:** [https://github.com/001TMF/blatant-why](https://github.com/001TMF/blatant-why)
- **Reference / DOI:** [https://github.com/001TMF/blatant-why](https://github.com/001TMF/blatant-why)

## ✨ Key Features & Innovations
- Autonomous multi-agent campaign planning for therapeutic antibody and binder design.
- Unified tool wrapper integrating modern open-source models with cloud execution.
- Automated filtering, docking verification, and candidate prioritization.

## ⚖️ Strengths & Limitations
- **Strengths:** Reduces manual orchestration effort in multi-step protein engineering campaigns.
- **Limitations:** Requires configuration of API keys and compute backend nodes.

## 📋 Suggested Action Items for Alphafoldology Repository
- [ ] Add tool entry to `tools_data_updated.json` under `Agents & Workflows`.
- [ ] Connect parent edge to `BoltzGen / Protenix / RFdiffusion` in `index.js` interactive genealogy map.
- [ ] Update badge indicators (GitHub stars, HuggingFace downloads, DOI links).
- [ ] Tag entry with: `agentic-ai`, `multi-agent`, `biologics-design`, `automation`, `campaign-manager`.

---

# Issue #7: [Tool Submission]: alphafold-sovereign-mcp - Model Context Protocol (MCP) Server for AlphaFold Structures

**Platform Source:** GitHub  
**Category:** Visualization & MCP  
**Parent Node / Genealogy:** AlphaFold 2 / MCP Protocol  
**Target Tags:** `mcp-server`, `agentic-ai`, `alphafold-db`, `plddt`, `antigravity`  

---

## 📌 Description & Context
alphafold-sovereign-mcp is a Model Context Protocol (MCP) server enabling AI coding agents (such as Antigravity IDE, Claude, Cursor) to directly search, fetch, parse, and analyze AlphaFold structural predictions, pLDDT scores, and domain boundaries within conversational sessions.

## 🔗 Key Links & References
- **Primary Link:** [https://github.com/smaniches/alphafold-sovereign-mcp](https://github.com/smaniches/alphafold-sovereign-mcp)
- **Reference / DOI:** [https://github.com/smaniches/alphafold-sovereign-mcp](https://github.com/smaniches/alphafold-sovereign-mcp)

## ✨ Key Features & Innovations
- Native MCP tool integration for structural biology AI agents.
- Direct query interface for AlphaFold Database coordinates and quality metrics.
- Facilitates automated structure analysis in agentic pairs.

## ⚖️ Strengths & Limitations
- **Strengths:** Clean agentic protocol implementation for modern AI assistant workflows.
- **Limitations:** Requires MCP-compliant client environment.

## 📋 Suggested Action Items for Alphafoldology Repository
- [ ] Add tool entry to `tools_data_updated.json` under `Visualization & MCP`.
- [ ] Connect parent edge to `AlphaFold 2 / MCP Protocol` in `index.js` interactive genealogy map.
- [ ] Update badge indicators (GitHub stars, HuggingFace downloads, DOI links).
- [ ] Tag entry with: `mcp-server`, `agentic-ai`, `alphafold-db`, `plddt`, `antigravity`.

---

# Issue #8: [Tool Submission]: biohub/ESMFold2 - Next-Gen Ultra-Fast Protein Folding Models on HuggingFace Hub

**Platform Source:** HuggingFace Hub  
**Category:** Fast Predictors  
**Parent Node / Genealogy:** ESMFold (Meta AI / Chan Zuckerberg Biohub)  
**Target Tags:** `esmfold2`, `huggingface-model`, `ultra-fast`, `single-sequence`, `open-weights`  

---

## 📌 Description & Context
biohub/ESMFold2 and its family of experimental variants (ESMFold2-Fast, ESMFold2-Experimental-Cutoff2025) represent the next-generation single-sequence protein structure prediction model hosted on HuggingFace Hub. With nearly 400,000 downloads, it delivers ultra-fast monomer predictions directly from language model embeddings.

## 🔗 Key Links & References
- **Primary Link:** [https://huggingface.co/biohub/ESMFold2](https://huggingface.co/biohub/ESMFold2)
- **Reference / DOI:** [https://huggingface.co/biohub/ESMFold2](https://huggingface.co/biohub/ESMFold2)

## ✨ Key Features & Innovations
- Significantly improved accuracy over original ESMFold v1 while maintaining single-sequence speed.
- Available in multiple model sizes (300M, 600M parameters) and speed-optimized checkpoints.
- Direct integration with HuggingFace `transformers` ecosystem.

## ⚖️ Strengths & Limitations
- **Strengths:** Extremely fast single-sequence prediction; high community adoption.
- **Limitations:** Limited complex multi-mer support compared to AF3/Boltz.

## 📋 Suggested Action Items for Alphafoldology Repository
- [ ] Add tool entry to `tools_data_updated.json` under `Fast Predictors`.
- [ ] Connect parent edge to `ESMFold (Meta AI / Chan Zuckerberg Biohub)` in `index.js` interactive genealogy map.
- [ ] Update badge indicators (GitHub stars, HuggingFace downloads, DOI links).
- [ ] Tag entry with: `esmfold2`, `huggingface-model`, `ultra-fast`, `single-sequence`, `open-weights`.

---

# Issue #9: [Tool Submission]: GitLab AlphaFold Pipelines: HT-Colabfold & binder_design

**Platform Source:** GitLab  
**Category:** Workflows & Pipelines  
**Parent Node / Genealogy:** ColabFold / ESM-1b  
**Target Tags:** `gitlab-repository`, `high-throughput`, `colabfold`, `binder-design`, `esm-1b`  

---

## 📌 Description & Context
A collection of curated high-throughput structural biology pipelines hosted on GitLab: `BrenneckeLab/ht-colabfold` (High-Throughput AlphaFold2 Screening Pipeline) and `patrickbryant1/binder_design` (Evolutionary guided sequence search from ESM-1b for target binder design).

## 🔗 Key Links & References
- **Primary Link:** [https://gitlab.com/BrenneckeLab/ht-colabfold](https://gitlab.com/BrenneckeLab/ht-colabfold)
- **Reference / DOI:** [https://gitlab.com/patrickbryant1/binder_design](https://gitlab.com/patrickbryant1/binder_design)

## ✨ Key Features & Innovations
- Automated high-throughput screening pipeline utilizing ColabFold backends.
- Evolutionary sequence optimization conditioned on ESM language model likelihoods.
- Expands Alphafoldology coverage beyond GitHub into GitLab open repositories.

## ⚖️ Strengths & Limitations
- **Strengths:** Tested in experimental laboratory screening campaigns.
- **Limitations:** Smaller GitLab star visibility compared to GitHub repositories.

## 📋 Suggested Action Items for Alphafoldology Repository
- [ ] Add tool entry to `tools_data_updated.json` under `Workflows & Pipelines`.
- [ ] Connect parent edge to `ColabFold / ESM-1b` in `index.js` interactive genealogy map.
- [ ] Update badge indicators (GitHub stars, HuggingFace downloads, DOI links).
- [ ] Tag entry with: `gitlab-repository`, `high-throughput`, `colabfold`, `binder-design`, `esm-1b`.

---

# Issue #10: [Preprint Submission]: bioRxiv Breakthroughs: ProteinSketch VR & Prosculpt Design Interfaces

**Platform Source:** bioRxiv  
**Category:** Preprints & Design Interfaces  
**Parent Node / Genealogy:** De Novo Protein Design / VR Interfaces  
**Target Tags:** `biorxiv-preprint`, `vr-interface`, `proteinsketch`, `prosculpt`, `interactive-design`  

---

## 📌 Description & Context
Featured 2026 bioRxiv preprints pushing the boundaries of interactive protein design: 1) *ProteinSketch translates spatial intuition into protein design with bimanual interaction in VR* (DOI: 10.64898/2026.07.19.739460), and 2) *Prosculpt: Lowering the Barrier to Computational Protein Design* (DOI: 10.64898/2026.06.25.732351).

## 🔗 Key Links & References
- **Primary Link:** [https://doi.org/10.64898/2026.07.19.739460](https://doi.org/10.64898/2026.07.19.739460)
- **Reference / DOI:** [10.64898/2026.07.19.739460](10.64898/2026.07.19.739460)

## ✨ Key Features & Innovations
- Bimanual Virtual Reality (VR) interface for intuitive spatial protein backbone manipulation.
- Prosculpt streamlined user interface reducing technical barriers for experimental biologists.
- Direct integration of deep learning structure prediction feedback loops into design sessions.

## ⚖️ Strengths & Limitations
- **Strengths:** Bridges complex generative AI models with intuitive human spatial interaction.
- **Limitations:** Requires specialized VR hardware (Meta Quest / Vision Pro) for ProteinSketch.

## 📋 Suggested Action Items for Alphafoldology Repository
- [ ] Add tool entry to `tools_data_updated.json` under `Preprints & Design Interfaces`.
- [ ] Connect parent edge to `De Novo Protein Design / VR Interfaces` in `index.js` interactive genealogy map.
- [ ] Update badge indicators (GitHub stars, HuggingFace downloads, DOI links).
- [ ] Tag entry with: `biorxiv-preprint`, `vr-interface`, `proteinsketch`, `prosculpt`, `interactive-design`.

---

# Issue #11: [Literature Submission]: AntiConf & Deep Learning Structure Evaluation on Antibody-Antigen Complexes

**Platform Source:** EuropePMC & OpenAlex  
**Category:** Benchmarks & Literature  
**Parent Node / Genealogy:** AlphaFold Multimer / Antibody Benchmarks  
**Target Tags:** `europepmc`, `openalex`, `anticonf`, `antibody-antigen`, `benchmarking`  

---

## 📌 Description & Context
Key 2026 peer-reviewed literature indexed in EuropePMC and OpenAlex evaluating deep learning protein structure prediction accuracy on complex targets: 1) *Confidence scoring for deep learning-predicted antibody-antigen complexes: AntiConf as a precision-driven framework* (Brief Bioinform 2026, DOI: 10.1093/bib/bbag137), and 2) *Evaluating deep learning based structure prediction methods on antibody-antigen complexes* (Bioinformatics 2026, DOI: 10.1093/bioinformatics/btag136).

## 🔗 Key Links & References
- **Primary Link:** [https://doi.org/10.1093/bib/bbag137](https://doi.org/10.1093/bib/bbag137)
- **Reference / DOI:** [10.1093/bib/bbag137](10.1093/bib/bbag137)

## ✨ Key Features & Innovations
- AntiConf precision confidence scoring framework dedicated to antibody-antigen interface evaluation.
- Comprehensive benchmarking of AF2, AF3, ESMFold, and RoseTTAFold on complex paratope-epitope prediction.
- Identifies key confidence metrics distinguishing true binders from false positives.

## ⚖️ Strengths & Limitations
- **Strengths:** Rigorously benchmarked metric framework for therapeutic antibody evaluation.
- **Limitations:** Specifically tailored to immunoglobulins and nanobodies.

## 📋 Suggested Action Items for Alphafoldology Repository
- [ ] Add tool entry to `tools_data_updated.json` under `Benchmarks & Literature`.
- [ ] Connect parent edge to `AlphaFold Multimer / Antibody Benchmarks` in `index.js` interactive genealogy map.
- [ ] Update badge indicators (GitHub stars, HuggingFace downloads, DOI links).
- [ ] Tag entry with: `europepmc`, `openalex`, `anticonf`, `antibody-antigen`, `benchmarking`.

---

# Issue #12: [Tool Submission]: EnzyMM & patchr - Catalytic Motif Miner and Biomolecular Inpainting Utilities

**Platform Source:** GitHub  
**Category:** Structural Utilities & Search  
**Parent Node / Genealogy:** AlphaFold DB / PDB Search  
**Target Tags:** `catalytic-motifs`, `enzyme-mining`, `inpainting`, `structure-repair`, `alphafold-db`  

---

## 📌 Description & Context
Two essential structural biology software tools: 1) `RayHackett/enzymm` (Enzyme Motif Miner - Geometric matching and discovery of catalytic active site motifs across predicted protein structures), and 2) `DeepFoldProtein/patchr` (3D structure inpainting and simulation-ready setup for proteins, DNA, RNA, and molecular complexes).

## 🔗 Key Links & References
- **Primary Link:** [https://github.com/RayHackett/enzymm](https://github.com/RayHackett/enzymm)
- **Reference / DOI:** [https://github.com/DeepFoldProtein/patchr](https://github.com/DeepFoldProtein/patchr)

## ✨ Key Features & Innovations
- 3D geometric active site motif searching across millions of AlphaFold DB models.
- Biomolecular structure inpainting for missing loops, sidechains, and multi-entity complex gaps.
- Prepares predicted models for molecular dynamics (MD) simulation.

## ⚖️ Strengths & Limitations
- **Strengths:** Direct utility for enzyme design and computational biophysics simulation prep.
- **Limitations:** EnzyMM relies on accurate sidechain predictions for active site geometry.

## 📋 Suggested Action Items for Alphafoldology Repository
- [ ] Add tool entry to `tools_data_updated.json` under `Structural Utilities & Search`.
- [ ] Connect parent edge to `AlphaFold DB / PDB Search` in `index.js` interactive genealogy map.
- [ ] Update badge indicators (GitHub stars, HuggingFace downloads, DOI links).
- [ ] Tag entry with: `catalytic-motifs`, `enzyme-mining`, `inpainting`, `structure-repair`, `alphafold-db`.

---

