# Evaluation Protocol

## Objective Questions

Objective questions evaluate conceptual recognition and domain knowledge coverage across five carbon-neutrality subdomains:

1. CCUS
2. Negative emission technologies
3. Low- and zero-carbon technologies
4. Carbon neutrality strategy and policy
5. Carbon accounting and market mechanisms

Recommended reporting:

- number of questions per subdomain
- model prediction
- reference answer
- correctness
- bootstrap 95% confidence interval
- paired statistical test where model predictions are paired question by question

## Open-Ended Questions

Open-ended questions evaluate synthesis, explanation, and decision-relevant knowledge organization.

Recommended automated metrics:

- F1 / token overlap
- BERTScore
- METEOR
- Keyword Coverage Rate (KCR)

Known limitation: KCR may be affected by response length and should be interpreted with length-aware caution.

## LLM-as-Judge

LLM-as-judge evaluation should report:

- evaluator model and exact version when available
- API provider
- inference date
- temperature and other decoding settings
- full evaluation prompt
- scoring dimensions
- parsing and failure-handling rules

API keys must be read from environment variables and must never be committed.

## Human Expert Evaluation

For revised submission, expert evaluation should report:

- number of evaluators
- expertise and institutional role, anonymized if needed
- blind or non-blind procedure
- scoring rubric
- inter-rater agreement, such as Cohen's kappa, Krippendorff's alpha, or ICC
- disagreement resolution process

## Error Taxonomy

Recommended failure categories:

- retrieval mismatch
- unsupported factual claim
- numerical inconsistency
- policy or regulation misinterpretation
- terminology confusion
- incomplete engineering workflow reasoning
- over-generalized decarbonization recommendation

