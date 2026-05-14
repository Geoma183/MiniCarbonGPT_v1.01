# Data Directory

This directory documents the data required to reproduce the MiniCarbonGPT v1.01 workflow.

## Uploaded Benchmark Files

The repository currently includes two benchmark files used in the manuscript:

- `objective_questions.xlsx`: 700 multiple-choice questions with domain labels, options, reference answers, model outputs, and correctness labels.
- `subjective_questions.xlsx`: 249 open-ended questions with reference answers, model responses, automatic metrics, keyword coverage rates, and judge scores.

These files improve transparency by exposing the evaluation questions, reference answers, model responses, and scoring outputs used in the manuscript. However, because some items were screened or adapted from third-party educational sources, users should treat them as academic reproducibility materials and verify source-specific redistribution rights before reuse beyond peer review or research validation.

Additional documentation:

- `benchmark_composition.csv`: benchmark size by subset and subdomain.
- `data_source_metadata.csv`: source-type, license, and redistribution notes.
- `../results/benchmark_quality_control.csv`: quality-control stages and retained public counts.
- `../results/contamination_check_template.csv`: template for documenting leakage/contamination checks.

## Publicly Redistributable Materials

Place public or sample files here:

- `objective_questions_sample.xlsx`
- `subjective_questions_sample.xlsx`
- `data_source_metadata.csv`

## Restricted Materials

The following materials may be restricted by third-party licenses and should not be redistributed without permission:

- Full-text papers downloaded from CNKI, Web of Science, publisher platforms, or institutional subscriptions.
- Full benchmark items derived from third-party educational platforms if their licenses do not allow redistribution.
- Commercial model outputs if service terms restrict redistribution.

For restricted materials, provide metadata, source descriptions, sampling rules, and scripts so that readers can reproduce the workflow with legally obtained data.

## Recommended Metadata Fields

`data_source_metadata.csv` should include:

| field | description |
|---|---|
| source_id | Stable source identifier |
| source_type | literature, wikipedia, standard, policy, question_bank, expert_authored |
| title_or_topic | Title or topic label |
| source_url_or_database | URL or database name when allowed |
| license_status | public, restricted, permission_required, unknown |
| used_for | training, retrieval, objective_eval, subjective_eval |
| redistribution | full, sample_only, metadata_only, not_redistributed |
