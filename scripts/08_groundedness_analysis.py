"""Summarize claim-level groundedness annotations."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Summarize groundedness annotations.")
    parser.add_argument("--claims", required=True, help="CSV with model, claim_id, supported, attributed columns.")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.claims)
    required = {"model", "supported", "attributed"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    df["supported"] = df["supported"].astype(bool)
    df["attributed"] = df["attributed"].astype(bool)
    summary = df.groupby("model").agg(
        n_claims=("supported", "size"),
        unsupported_claim_rate=("supported", lambda x: 1 - x.mean()),
        retrieval_attribution_accuracy=("attributed", "mean"),
    ).reset_index()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()

