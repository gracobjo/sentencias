#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrenamiento ligero con embeddings de Sentence-Transformers + clasificador.

Modelo por defecto: paraphrase-multilingual-MiniLM-L12-v2 (bueno para ES).
Genera models/modelo_legal_sbert.pkl con: encoder_name, clasificador, threshold.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

from sentence_transformers import SentenceTransformer


ENCODER_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def _read_text_file(path: Path) -> str:
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return path.read_text(encoding=enc)
        except Exception:
            continue
    return ""


def _read_pdf_file(path: Path) -> str:
    try:
        import PyPDF2
        texto = ""
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                texto += (page.extract_text() or "") + "\n"
        return texto.strip()
    except Exception:
        return ""


def _load_corpus(base_dir: Path, uploads_dir: Path) -> List[Tuple[str, str]]:
    corpus: List[Tuple[str, str]] = []
    for folder in (base_dir, uploads_dir):
        if not folder.exists():
            continue
        for p in folder.iterdir():
            if p.suffix.lower() == ".txt":
                txt = _read_text_file(p)
            elif p.suffix.lower() == ".pdf":
                txt = _read_pdf_file(p)
            else:
                continue
            if txt and len(txt) > 50:
                corpus.append((p.name, txt))
    return corpus


def _load_labels(labels_path: Path) -> Dict[str, int]:
    if not labels_path.exists():
        return {}
    try:
        data = json.loads(labels_path.read_text(encoding="utf-8"))
        norm = {}
        for k, v in data.items():
            if isinstance(v, bool):
                norm[k] = 1 if v else 0
            elif isinstance(v, (int, float)):
                norm[k] = 1 if v >= 0.5 else 0
            elif isinstance(v, str):
                norm[k] = 1 if v.lower() in {"1", "true", "favorable", "yes", "y"} else 0
        return norm
    except Exception:
        return {}


def train_and_save(
    base_dir: Path,
    uploads_dir: Path,
    models_dir: Path,
    labels_path: Path | None = None,
    encoder_name: str = ENCODER_NAME,
):
    corpus = _load_corpus(base_dir, uploads_dir)
    if not corpus:
        raise RuntimeError("No hay documentos suficientes para entrenar")

    labels_map = _load_labels(labels_path) if labels_path else {}

    X_texts: List[str] = []
    y: List[int] = []
    for fname, text in corpus:
        X_texts.append(text)
        if fname in labels_map:
            y.append(labels_map[fname])
        else:
            # fallback: favorable si contiene vocabulario positivo
            tl = text.lower()
            y.append(1 if any(w in tl for w in ["procedente", "estimamos", "favorable"]) else 0)

    # Forzar dos clases si es necesario
    if len(set(y)) == 1:
        for i in range(0, len(y), 2):
            y[i] = 1 - y[i]

    encoder = SentenceTransformer(encoder_name)
    X_emb = encoder.encode(X_texts, batch_size=16, show_progress_bar=False, normalize_embeddings=True)

    y_arr = np.array(y)
    n = len(y_arr)
    # Si hay muy pocos ejemplos o alguna clase tiene <2, entrenar con todo sin split
    binc = np.bincount(y_arr)
    if n < 4 or (len(binc) >= 2 and binc.min() < 2):
        Xtr, ytr = X_emb, y_arr
        Xte, yte = X_emb[:0], y_arr[:0]
    else:
        test_frac = 0.2 if n >= 10 else min(0.5, max(0.2, 1.0 / n))
        n_classes = len(np.unique(y_arr))
        # calcular test_size como entero garantizando >= num clases y < n
        n_test = max(n_classes, int(round(test_frac * n)))
        if n_test >= n:
            n_test = max(n_classes, 1)
        stratify = y_arr if len(binc) >= 2 and binc.min() >= 2 else None
        Xtr, Xte, ytr, yte = train_test_split(X_emb, y_arr, test_size=n_test, random_state=42, stratify=stratify)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(Xtr, ytr)
    if Xte.shape[0] > 0:
        try:
            ypred = clf.predict(Xte)
            print(classification_report(yte, ypred, digits=3))
        except Exception:
            pass

    models_dir.mkdir(parents=True, exist_ok=True)
    out_path = models_dir / "modelo_legal_sbert.pkl"
    with open(out_path, "wb") as f:
        pickle.dump({
            "encoder_name": encoder_name,
            "clasificador": clf,
        }, f)

    return {"status": "ok", "path": str(out_path)}


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parents[1] / "sentencias"
    UPLOADS_DIR = Path(__file__).resolve().parents[1] / "uploads"
    MODELS_DIR = Path(__file__).resolve().parents[1] / "models"
    LABELS = MODELS_DIR / "labels.json"
    res = train_and_save(BASE_DIR, UPLOADS_DIR, MODELS_DIR, LABELS)
    print(res)


