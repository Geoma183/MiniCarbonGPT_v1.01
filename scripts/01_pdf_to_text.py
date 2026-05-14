"""Extract and clean text from PDF files.

This script is a public, path-free entry point corresponding to the manuscript's
PDF text extraction stage. Full-text documents are not redistributed here when
third-party licenses do not permit it.
"""

from __future__ import annotations

from pathlib import Path

import fitz

from common_config import add_config_arg, ensure_dir, load_config


def extract_pdf_text(pdf_path: Path) -> str:
    parts: list[str] = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            parts.append(page.get_text("text"))
    return "\n".join(parts)


def clean_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def main() -> None:
    parser = add_config_arg("Extract text from PDF files.")
    args = parser.parse_args()
    cfg = load_config(args.config)

    raw_dir = Path(cfg["paths"]["raw_pdf_dir"])
    out_dir = ensure_dir(cfg["paths"]["text_output_dir"])

    for pdf_path in sorted(raw_dir.glob("*.pdf")):
        text = clean_text(extract_pdf_text(pdf_path))
        out_path = out_dir / f"{pdf_path.stem}.txt"
        out_path.write_text(text, encoding="utf-8")
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()

