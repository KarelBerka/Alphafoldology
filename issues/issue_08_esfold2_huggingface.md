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
