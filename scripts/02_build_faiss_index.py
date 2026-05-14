"""Build a FAISS vector index from cleaned text chunks."""

from __future__ import annotations

import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from common_config import add_config_arg, ensure_dir, load_config


def iter_texts(input_dir: Path) -> list[str]:
    texts: list[str] = []
    for txt_path in sorted(input_dir.glob("*.txt")):
        text = txt_path.read_text(encoding="utf-8", errors="ignore")
        texts.extend(chunk_text(text))
    return [t for t in texts if t.strip()]


def chunk_text(text: str, max_chars: int = 800) -> list[str]:
    chunks: list[str] = []
    for para in text.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if len(para) <= max_chars:
            chunks.append(para)
        else:
            chunks.extend(para[i : i + max_chars] for i in range(0, len(para), max_chars))
    return chunks


def build_index(texts: list[str], model_name: str, normalize: bool) -> tuple[faiss.Index, np.ndarray]:
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)
    embeddings = np.asarray(embeddings, dtype="float32")
    if normalize:
        faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings


def save_index(index: faiss.Index, texts: list[str], out_dir: Path) -> None:
    ensure_dir(out_dir)
    faiss.write_index(index, str(out_dir / "index.faiss"))
    with (out_dir / "text_map.pkl").open("wb") as f:
        pickle.dump(texts, f)


def main() -> None:
    parser = add_config_arg("Build FAISS indexes for core and supplementary corpora.")
    args = parser.parse_args()
    cfg = load_config(args.config)

    model_name = cfg["models"]["embedding_model"]
    normalize = bool(cfg["retrieval"].get("normalize_embeddings", True))

    corpus_pairs = [
        (Path(cfg["paths"]["core_corpus_dir"]), Path(cfg["paths"]["core_faiss_dir"])),
        (Path(cfg["paths"]["supplementary_corpus_dir"]), Path(cfg["paths"]["supplementary_faiss_dir"])),
    ]

    for input_dir, out_dir in corpus_pairs:
        texts = iter_texts(input_dir)
        index, _ = build_index(texts, model_name, normalize)
        save_index(index, texts, out_dir)
        print(f"indexed {len(texts)} chunks -> {out_dir}")


if __name__ == "__main__":
    main()

