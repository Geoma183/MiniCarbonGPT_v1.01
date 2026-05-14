"""Evaluate objective-question predictions."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from common_config import add_config_arg, ensure_dir, load_config


def normalize_answer(value: object) -> str:
    text = str(value).strip().upper()
    for token in ["A", "B", "C", "D", "E"]:
        if text.startswith(token):
            return token
    return text


def main() -> None:
    parser = add_config_arg("Evaluate objective-question accuracy.")
    parser.add_argument("--predictions", required=True, help="CSV/XLSX with reference and prediction columns.")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    cfg = load_config(args.config)

    path = Path(args.predictions)
    df = pd.read_excel(path) if path.suffix.lower() in {".xlsx", ".xls"} else pd.read_csv(path)
    ref_col = cfg["evaluation"]["objective_answer_column"]
    pred_col = cfg["evaluation"]["objective_prediction_column"]
    if ref_col not in df.columns or pred_col not in df.columns:
        raise ValueError(f"Required columns missing: {ref_col}, {pred_col}")

    df["reference_norm"] = df[ref_col].map(normalize_answer)
    df["prediction_norm"] = df[pred_col].map(normalize_answer)
    df["correct"] = df["reference_norm"] == df["prediction_norm"]

    group_cols = [c for c in ["model", "subdomain"] if c in df.columns]
    summary = df.groupby(group_cols)["correct"].agg(["count", "mean"]).reset_index() if group_cols else pd.DataFrame(
        [{"count": len(df), "mean": df["correct"].mean()}]
    )
    summary = summary.rename(columns={"mean": "accuracy"})

    out_path = Path(args.out or Path(cfg["paths"]["outputs_dir"]) / "objective_results.csv")
    ensure_dir(out_path.parent)
    summary.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()

