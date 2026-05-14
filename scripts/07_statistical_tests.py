"""Bootstrap confidence intervals and paired tests for objective predictions."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest


def bootstrap_ci(values: np.ndarray, n_boot: int = 5000, seed: int = 42) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    means = [rng.choice(values, size=len(values), replace=True).mean() for _ in range(n_boot)]
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Compute accuracy CI and paired sign tests.")
    parser.add_argument("--predictions", required=True, help="CSV with columns: question_id, model, correct.")
    parser.add_argument("--baseline", default=None, help="Optional baseline model for paired tests.")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.predictions)
    rows = []
    for model, group in df.groupby("model"):
        values = group["correct"].astype(int).to_numpy()
        lo, hi = bootstrap_ci(values)
        rows.append({"model": model, "n": len(values), "accuracy": values.mean(), "ci95_low": lo, "ci95_high": hi})

    if args.baseline:
        pivot = df.pivot(index="question_id", columns="model", values="correct")
        if args.baseline not in pivot.columns:
            raise ValueError(f"Baseline not found: {args.baseline}")
        for model in pivot.columns:
            if model == args.baseline:
                continue
            paired = pivot[[args.baseline, model]].dropna().astype(int)
            wins = int(((paired[model] == 1) & (paired[args.baseline] == 0)).sum())
            losses = int(((paired[model] == 0) & (paired[args.baseline] == 1)).sum())
            n = wins + losses
            p = binomtest(wins, n, 0.5).pvalue if n else float("nan")
            rows.append({"model": f"{model} vs {args.baseline}", "n": n, "accuracy": np.nan, "ci95_low": np.nan, "ci95_high": np.nan, "paired_sign_p": p})

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()

