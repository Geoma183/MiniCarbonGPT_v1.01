"""Evaluate open-ended responses with lightweight text metrics and KCR."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from sklearn.metrics import f1_score

from common_config import add_config_arg, ensure_dir, load_config


TOKEN_RE = re.compile(r"[A-Za-z0-9_\-]+")


def tokens(text: object) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(str(text))]


def token_f1(reference: object, prediction: object) -> float:
    ref = set(tokens(reference))
    pred = set(tokens(prediction))
    if not ref and not pred:
        return 1.0
    if not ref or not pred:
        return 0.0
    precision = len(ref & pred) / len(pred)
    recall = len(ref & pred) / len(ref)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def keyword_coverage(reference_keywords: object, prediction: object) -> float:
    keywords = {k.strip().lower() for k in re.split(r"[,;，；]", str(reference_keywords)) if k.strip()}
    pred = set(tokens(prediction))
    if not keywords:
        return float("nan")
    return len(keywords & pred) / len(keywords)


def main() -> None:
    parser = add_config_arg("Evaluate subjective responses.")
    parser.add_argument("--responses", required=True, help="CSV/XLSX with reference and prediction columns.")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    cfg = load_config(args.config)

    path = Path(args.responses)
    df = pd.read_excel(path) if path.suffix.lower() in {".xlsx", ".xls"} else pd.read_csv(path)
    ref_col = cfg["evaluation"]["subjective_reference_column"]
    pred_col = cfg["evaluation"]["objective_prediction_column"]
    if ref_col not in df.columns or pred_col not in df.columns:
        raise ValueError(f"Required columns missing: {ref_col}, {pred_col}")

    df["token_f1"] = [token_f1(r, p) for r, p in zip(df[ref_col], df[pred_col])]
    if "reference_keywords" in df.columns:
        df["keyword_coverage_rate"] = [keyword_coverage(k, p) for k, p in zip(df["reference_keywords"], df[pred_col])]

    group_cols = [c for c in ["model", "subdomain"] if c in df.columns]
    metric_cols = [c for c in ["token_f1", "keyword_coverage_rate"] if c in df.columns]
    summary = df.groupby(group_cols)[metric_cols].mean().reset_index() if group_cols else df[metric_cols].mean().to_frame().T

    out_path = Path(args.out or Path(cfg["paths"]["outputs_dir"]) / "subjective_metric_results.csv")
    ensure_dir(out_path.parent)
    summary.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()

