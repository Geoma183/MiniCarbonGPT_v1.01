🌿 MiniCarbonGPT_v1.01

A Domain-Specific Large Language Model for Engineering-Oriented Carbon Neutrality Applications
Using GLM-4-9B, LoRA Fine-Tuning, and Retrieval-Augmented Generation (RAG)

📖 Citation and Preprint

🧾 Preprint Reference:
He, L.; Zhou, Y.; Liu, X.; Su, L. (2025).
Mini-CarbonGPT: A Domain-Specific Language Model for Engineering-Oriented Carbon Neutrality Applications.
SSRN Electronic Journal
DOI: 10.2139/ssrn.5280830

📘 Published as an open-access preprint on SSRN (June 11, 2025)
📜 License: CC BY 4.0 — for academic and non-commercial use only

If you use this repository in your research, please cite as:
@article{He2025MiniCarbonGPT,
  title   = {Mini-CarbonGPT: A Domain-Specific Language Model for Engineering-Oriented Carbon Neutrality Applications},
  author  = {He, Lu-hao and Zhou, Yongzhang and Liu, Xian and Su, Lu},
  journal = {SSRN Electronic Journal},
  year    = {2025},
  doi     = {10.2139/ssrn.5280830},
  url     = {https://ssrn.com/abstract=5280830}
}

🧩 Overview

MiniCarbonGPT_v1.01 extends our previous version (v1.00, Sustainability 2025)
by integrating LoRA parameter-efficient fine-tuning and Retrieval-Augmented Generation (RAG) mechanisms.
This version improves domain adaptability, factual grounding, and scalability for carbon neutrality applications, including:
CCUS technology simulation
Carbon emission tracking
Low-carbon material design
Policy analysis and carbon market evaluation


🧠 Key Enhancements in v1.01
| Component            | Description                          | Result                       |
| -------------------- | ------------------------------------ | ---------------------------- |
| **LoRA Fine-tuning** | 1.5B GLM-4-9B model, INT4 quantized  | +8.9% factual gain           |
| **RAG Integration**  | Dual-index FAISS retriever           | +6.3% semantic accuracy      |
| **Evaluation**       | 700 objective + 249 subjective tasks | 82.1% overall score          |
| **Deployment**       | 2× RTX 2080Ti compatible             | Reproducible and lightweight |

📦 Repository Linkage
| Resource                                                                   | Description                                            |
| -------------------------------------------------------------------------- | ------------------------------------------------------ |
| [**MiniCarbonGPT_v1.00**](https://github.com/Geoma183/MiniCarbonGPT_v1.00) | Initial version (Sustainability 2025)                  |
| [**MiniCarbonGPT_v1.01**](https://github.com/Geoma183/MiniCarbonGPT_v1.01) | SSRN preprint version (LoRA + RAG)                     |
| [**Upcoming v2.00**](#)                                                    | Multimodal + multilingual integration (in preparation) |


💬 Abstract (from SSRN)
Large language models (LLMs) provide substantial potential for engineering-oriented carbon neutrality tasks.
However, general-purpose models lack domain expertise.
To bridge this gap, we propose Mini-CarbonGPT, a domain-specific LLM integrating LoRA fine-tuning and RAG-based retrieval.
Evaluations on 949 QA tasks (700 objective, 249 subjective) across CCUS, policy, and emission domains show that MiniCarbonGPT outperforms GPT-4o and Gemini-1.5 in both accuracy and factual reliability.

📚 Citation Note (for Paper Submissions)
“The code and framework for Mini-CarbonGPT (v1.01) are publicly available at
https://github.com/Geoma183/MiniCarbonGPT_v1.01,
corresponding to the SSRN preprint DOI 10.2139/ssrn.5280830.”
