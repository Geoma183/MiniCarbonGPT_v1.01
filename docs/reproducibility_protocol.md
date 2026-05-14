# Reproducibility Protocol

## Workflow

1. Collect legally accessible carbon-neutrality literature and auxiliary public knowledge sources.
2. Extract and clean text from PDF documents.
3. Split text into paragraph-aware chunks.
4. Encode chunks with `paraphrase-multilingual-MiniLM-L12-v2`.
5. Build separate FAISS indexes for the core corpus and supplementary corpus.
6. Generate answers under four paths:
   - `base`: GLM-4-9B only
   - `finetune`: GLM-4-9B + LoRA
   - `rag`: GLM-4-9B + retrieval
   - `fine_rag`: GLM-4-9B + LoRA + retrieval
7. Evaluate objective questions with exact or normalized answer matching.
8. Evaluate open-ended questions with text metrics, keyword coverage, LLM-as-judge scoring, and expert review where available.
9. Run revision analyses: efficiency benchmark, retrieval-weight ablation, statistical testing, groundedness analysis, and error taxonomy.

## Minimum Reporting Requirements

For each experiment, record:

- commit or release tag
- model name and version
- LoRA checkpoint identifier
- embedding model
- corpus version
- question set version
- prompt template
- decoding settings
- hardware and software environment
- run date

## Reproducibility Limits

Exact reproduction may be limited by restricted third-party documents, changing commercial model APIs, and local hardware differences. These limits should be stated explicitly in the manuscript and response letter.

