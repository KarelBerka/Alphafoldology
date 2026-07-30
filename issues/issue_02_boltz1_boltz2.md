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
