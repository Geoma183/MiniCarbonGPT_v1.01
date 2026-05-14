# Legacy File Map

This table maps local legacy scripts to the cleaned public repository structure.

| Legacy file | Public file | Action |
|---|---|---|
| `1文档处理1.py` | `scripts/01_pdf_to_text.py` | Parameterize paths and document extraction tools |
| `2向量化.py`, `2向量化2.py` | `scripts/02_build_faiss_index.py` | Merge duplicate vectorization scripts |
| `3检索.py`, `3检索2.py` | `scripts/03_generate_rag_answers.py` or retrieval helper | Expose `top_k`, `core_weight`, `supplementary_weight` |
| `4问答.py`, `3.py` | `scripts/03_generate_rag_answers.py` | Remove local model paths and keep decoding config explicit |
| `Objective/*.py` | `scripts/04_evaluate_objective.py` | Merge model-specific scripts into one configurable evaluator |
| `Subjective/*.py` | `scripts/05_evaluate_subjective_metrics.py` | Merge model-specific scripts into one configurable evaluator |
| `GPT评估.py` | `scripts/06_llm_judge_evaluation.py` | Remove hard-coded API key; use environment variable |
| `关键词覆盖*.py` | `scripts/05_evaluate_subjective_metrics.py` | Integrate KCR calculation |
| `*.log` | `results/*.csv` | Extract metrics; do not commit raw logs by default |

