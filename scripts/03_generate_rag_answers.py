"""Generate answers with GLM, LoRA, RAG, or LoRA+RAG modes."""

from __future__ import annotations

import argparse
import pickle
from pathlib import Path

import faiss
import numpy as np
import pandas as pd
import torch
from peft import PeftModel
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from common_config import add_config_arg, ensure_dir, load_config


def load_index(index_dir: Path) -> tuple[faiss.Index, list[str]]:
    index = faiss.read_index(str(index_dir / "index.faiss"))
    with (index_dir / "text_map.pkl").open("rb") as f:
        texts = pickle.load(f)
    return index, texts


def retrieve(query: str, cfg: dict, embedder: SentenceTransformer) -> list[str]:
    top_k = int(cfg["retrieval"]["top_k"])
    weights = [float(cfg["retrieval"]["core_weight"]), float(cfg["retrieval"]["supplementary_weight"])]
    index_dirs = [Path(cfg["paths"]["core_faiss_dir"]), Path(cfg["paths"]["supplementary_faiss_dir"])]
    q = embedder.encode([query]).astype("float32")
    if cfg["retrieval"].get("normalize_embeddings", True):
        faiss.normalize_L2(q)

    results: list[tuple[float, str]] = []
    for weight, index_dir in zip(weights, index_dirs):
        index, texts = load_index(index_dir)
        scores, ids = index.search(q, top_k)
        for score, idx in zip(scores[0], ids[0]):
            if idx >= 0:
                results.append((float(score) * weight, texts[idx]))
    results.sort(key=lambda item: item[0], reverse=True)
    return [text for _, text in results[:top_k]]


def load_generator(cfg: dict, use_lora: bool):
    model_path = cfg["models"]["base_model_name_or_path"]
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    if use_lora:
        model = PeftModel.from_pretrained(model, cfg["models"]["lora_weights_path"])
    model.eval()
    return model, tokenizer


def build_prompt(question: str, contexts: list[str]) -> str:
    context_block = "\n\n".join(contexts)
    return (
        "Answer the carbon-neutrality question using the provided evidence when available.\n\n"
        f"[Evidence]\n{context_block}\n\n[Question]\n{question}\n\n[Answer]"
    )


def generate(model, tokenizer, prompt: str, cfg: dict) -> str:
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=int(cfg["generation"]["max_new_tokens"]),
            temperature=float(cfg["generation"]["temperature"]),
            top_p=float(cfg["generation"]["top_p"]),
            repetition_penalty=float(cfg["generation"]["repetition_penalty"]),
        )
    return tokenizer.decode(output[0], skip_special_tokens=True)


def main() -> None:
    parser = add_config_arg("Generate answers for objective or subjective questions.")
    parser.add_argument("--mode", choices=["base", "finetune", "rag", "fine_rag"], required=True)
    parser.add_argument("--input", default=None, help="Optional question file path.")
    parser.add_argument("--out", default=None, help="Optional output CSV path.")
    args = parser.parse_args()
    cfg = load_config(args.config)

    use_lora = args.mode in {"finetune", "fine_rag"}
    use_rag = args.mode in {"rag", "fine_rag"}
    question_path = Path(args.input or cfg["paths"]["objective_questions"])
    out_path = Path(args.out or Path(cfg["paths"]["outputs_dir"]) / f"{args.mode}_answers.csv")
    ensure_dir(out_path.parent)

    df = pd.read_excel(question_path)
    question_col = "question" if "question" in df.columns else df.columns[0]

    embedder = SentenceTransformer(cfg["models"]["embedding_model"]) if use_rag else None
    model, tokenizer = load_generator(cfg, use_lora)

    answers = []
    for question in df[question_col].fillna("").astype(str):
        contexts = retrieve(question, cfg, embedder) if use_rag and embedder else []
        prompt = build_prompt(question, contexts)
        answers.append(generate(model, tokenizer, prompt, cfg))

    df["prediction"] = answers
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()

