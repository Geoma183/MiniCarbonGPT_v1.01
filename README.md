# MiniCarbonGPT v1.01

Code and reproducibility materials for:

**Mini-CarbonGPT: A Resource-Efficient Knowledge-Augmented Framework for Environmental Decision Support in Carbon Neutrality Engineering**

Manuscript: `ENVSOFT-D-26-01060`

> Revision note: this repository is organized to support reproducibility review for the revised submission. It documents the processing pipeline, retrieval and generation modules, evaluation protocols, and revision-related analyses requested during peer review.

## Repository Contents

```text
configs/
  example_config.yaml              # Path-free configuration template
scripts/
  01_pdf_to_text.py                # PDF text extraction and cleaning entry point
  02_build_faiss_index.py          # Embedding and FAISS index construction
  03_generate_rag_answers.py       # GLM/LoRA/RAG answer generation
  04_evaluate_objective.py         # Objective-question accuracy evaluation
  05_evaluate_subjective_metrics.py# F1, BERTScore, METEOR and KCR metrics
  06_llm_judge_evaluation.py       # LLM-as-judge scoring; API key via environment variable
  07_statistical_tests.py          # Bootstrap CI and paired significance tests
  08_groundedness_analysis.py      # Evidence attribution and unsupported-claim analysis
data/
  README.md                        # Data availability and redistribution boundaries
results/
  README.md                        # Expected result tables and revision evidence
docs/
  reproducibility_protocol.md      # End-to-end workflow
  evaluation_protocol.md           # Objective, subjective, expert, and LLM-judge evaluation
  data_statement.md                # Public data statement for the manuscript
  reviewer_response_note.md        # Suggested response-letter wording
```

## Reproducibility Status

| Component | Status | Notes |
|---|---|---|
| Source code | Public | Processing, indexing, retrieval, generation, and evaluation scripts are provided. |
| Configuration | Public template | Local absolute paths and private credentials are not included. |
| Objective and subjective evaluation data | Partially public | Redistribution depends on the license of third-party educational/question sources. Sample files and metadata should be provided where full redistribution is restricted. |
| CNKI/WoS paper full text | Not redistributed | Full text may be protected by database or publisher licenses. The repository provides processing scripts and corpus metadata instead. |
| GLM-4-9B base model | External | Users should obtain it under the original model license. |
| LoRA weights | To be specified | If redistributable, provide a release asset or external model link; otherwise provide training instructions. |
| API-based commercial model outputs | Partially reproducible | Results depend on model version, API date, prompt, and decoding settings. |

## Quick Start

1. Create a Python environment.

```bash
pip install -r requirements.txt
```

2. Copy the configuration template and edit local paths.

```bash
cp configs/example_config.yaml configs/local_config.yaml
```

3. Run the workflow steps.

```bash
python scripts/01_pdf_to_text.py --config configs/local_config.yaml
python scripts/02_build_faiss_index.py --config configs/local_config.yaml
python scripts/03_generate_rag_answers.py --config configs/local_config.yaml --mode fine_rag
python scripts/04_evaluate_objective.py --config configs/local_config.yaml
python scripts/05_evaluate_subjective_metrics.py --config configs/local_config.yaml
```

4. Run revision-related checks.

```bash
python scripts/07_statistical_tests.py --predictions results/objective_predictions.csv --out results/statistical_significance.csv
python scripts/08_groundedness_analysis.py --claims results/generated_claims.csv --out results/groundedness_analysis.csv
```

## Security and Privacy

No API keys, passwords, personal machine paths, or private credentials should be committed to this repository. API-based evaluation scripts read credentials from environment variables such as `OPENAI_API_KEY`.

If a credential was accidentally committed in an earlier local script, revoke or rotate it before publication.

## Data Availability Statement

The source code, evaluation scripts, configuration templates, and reproducibility materials are publicly available in this repository. Due to licensing restrictions, third-party full-text documents and some benchmark items derived from external educational platforms are not redistributed in full; instead, this repository provides metadata, sample files, processing scripts, and evaluation protocols needed to reproduce the workflow with legally obtained data.

## Citation

If you use this repository, please cite the manuscript/preprint and this repository version. A `CITATION.cff` file is provided for citation metadata.

