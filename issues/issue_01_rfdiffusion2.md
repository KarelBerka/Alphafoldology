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
