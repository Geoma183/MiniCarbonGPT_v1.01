# Results Directory

Expected revision evidence files:

| file | purpose |
|---|---|
| `objective_results.csv` | Objective-question accuracy by model and subdomain |
| `subjective_metric_results.csv` | F1, BERTScore, METEOR, and KCR results |
| `llm_judge_results.csv` | LLM-as-judge scores with model/date/prompt settings |
| `efficiency_benchmark.csv` | GPU memory, training time, latency, throughput, and cost/energy estimates |
| `rag_weight_ablation.csv` | Core/supplementary corpus weighting sensitivity analysis |
| `statistical_significance.csv` | Bootstrap confidence intervals and paired tests |
| `groundedness_analysis.csv` | Unsupported-claim rate, attribution accuracy, and faithfulness |
| `error_taxonomy_summary.csv` | Failure modes such as retrieval mismatch, numerical inconsistency, hallucination, and terminology confusion |

Raw logs should normally not be committed. Extract auditable metrics into CSV or Markdown summaries.

