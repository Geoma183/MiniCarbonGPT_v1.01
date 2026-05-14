"""LLM-as-judge evaluation without hard-coded credentials."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from openai import OpenAI

from common_config import add_config_arg, ensure_dir, load_config


PROMPT_TEMPLATE = """You are an impartial evaluator for carbon-neutrality engineering answers.
Score the model response against the reference answer using three criteria:
Accuracy, Completeness, and Clarity. Use integer scores from 1 to 5.

Question:
{question}

Reference answer:
{reference}

Model response:
{prediction}

Return only JSON with keys: accuracy, completeness, clarity, rationale.
"""


def main() -> None:
    parser = add_config_arg("Evaluate responses with an API-based LLM judge.")
    parser.add_argument("--responses", required=True)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    cfg = load_config(args.config)

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY environment variable is required; do not hard-code API keys.")

    client = OpenAI()
    path = Path(args.responses)
    df = pd.read_excel(path) if path.suffix.lower() in {".xlsx", ".xls"} else pd.read_csv(path)
    question_col = "question"
    ref_col = cfg["evaluation"]["subjective_reference_column"]
    pred_col = cfg["evaluation"]["objective_prediction_column"]

    outputs = []
    for _, row in df.iterrows():
        prompt = PROMPT_TEMPLATE.format(
            question=row.get(question_col, ""),
            reference=row.get(ref_col, ""),
            prediction=row.get(pred_col, ""),
        )
        response = client.chat.completions.create(
            model=cfg["evaluation"]["llm_judge_model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=float(cfg["evaluation"]["llm_judge_temperature"]),
        )
        outputs.append(response.choices[0].message.content)

    df["llm_judge_raw_json"] = outputs
    df["llm_judge_model"] = cfg["evaluation"]["llm_judge_model"]
    df["llm_judge_api_date"] = cfg["evaluation"]["llm_judge_api_date"]

    out_path = Path(args.out or Path(cfg["paths"]["outputs_dir"]) / "llm_judge_results.csv")
    ensure_dir(out_path.parent)
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()

