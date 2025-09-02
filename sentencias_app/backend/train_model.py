#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrenador rápido de modelo legal (scikit-learn) para AnalizadorLegal.

Construye un clasificador binario (favorable vs desfavorable) usando TF-IDF
sobre los textos disponibles en las carpetas de documentos. Si existe
"models/labels.json" con etiquetas manuales por archivo, las usa; si no,
aplica un etiquetado débil por palabras clave.

Salida: models/modelo_legal.pkl con claves: modelo, vectorizador, clasificador
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Palabras clave para etiquetado débil
PALABRAS_POSITIVAS = [
    "procedente",
    "estimamos",
    "estimamos procedente",
    "accedemos",
    "concedemos",
    "reconocemos",
    "favorable",
    "fundada",
]

PALABRAS_NEGATIVAS = [
    "desestimamos",
    "infundada",
    "rechazamos",
    "denegamos",
    "desfavorable",
    "no procedente",
]


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
    except Exception as e:
        logger.warning(f"No se pudo leer PDF {path}: {e}")
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


def _weak_label(texto: str) -> int:
    tl = texto.lower()
    pos = any(p in tl for p in PALABRAS_POSITIVAS)
    neg = any(n in tl for n in PALABRAS_NEGATIVAS)
    if pos and not neg:
        return 1
    if neg and not pos:
        return 0
    # Empate o ninguno: neutral como favorable leve
    return 1


def _load_labels(labels_path: Path) -> Dict[str, int]:
    if not labels_path.exists():
        return {}
    try:
        data = json.loads(labels_path.read_text(encoding="utf-8"))
        # normalizar a 0/1
        norm = {}
        for k, v in data.items():
            if isinstance(v, bool):
                norm[k] = 1 if v else 0
            elif isinstance(v, (int, float)):
                norm[k] = 1 if v >= 0.5 else 0
            elif isinstance(v, str):
                norm[k] = 1 if v.lower() in {"1", "true", "favorable", "yes", "y"} else 0
        return norm
    except Exception as e:
        logger.warning(f"No se pudieron cargar etiquetas manuales: {e}")
        return {}


def train_and_save(
    base_dir: Path,
    uploads_dir: Path,
    models_dir: Path,
    labels_path: Path | None = None,
) -> Dict[str, str]:
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
            y.append(_weak_label(text))

    # Si todas las etiquetas son iguales, forzar presencia de dos clases
    if len(set(y)) == 1:
        # Marcar como negativos (0) un 30% de textos sin palabras positivas
        nuevos_y: List[int] = []
        for text in X_texts:
            tl = text.lower()
            if not any(p in tl for p in PALABRAS_POSITIVAS) and np.random.rand() < 0.3:
                nuevos_y.append(0)
            else:
                nuevos_y.append(1)
        if len(set(nuevos_y)) < 2:
            # Como último recurso, alternar 0/1
            nuevos_y = [0 if i % 2 == 0 else 1 for i in range(len(X_texts))]
        y = nuevos_y

    # Vectorizador + Clasificador
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_df=0.95)
    X = vectorizer.fit_transform(X_texts)

    clf = LogisticRegression(max_iter=1000, n_jobs=None)
    # Ajustar tamaño de test para conjuntos pequeños
    y_arr = np.array(y)
    n_samples = y_arr.shape[0]
    n_classes = len(set(y))
    test_size = max(0.2, min(0.4, n_classes / max(4, n_samples)))
    # Si alguna clase tiene < 2 muestras, no estratificar y usar holdout mínimo
    stratify_arr = None
    if n_samples >= 4:
        unique, counts = np.unique(y_arr, return_counts=True)
        if counts.min() >= 2:
            stratify_arr = y_arr
        else:
            test_size = min(0.5, max(0.2, 1.0 / n_samples))
    Xtr, Xte, ytr, yte = train_test_split(X, y_arr, test_size=test_size, random_state=42, stratify=stratify_arr)
    clf.fit(Xtr, ytr)
    try:
        ypred = clf.predict(Xte)
        logger.info("\n" + classification_report(yte, ypred, digits=3))
    except Exception:
        pass

    models_dir.mkdir(parents=True, exist_ok=True)
    out_path = models_dir / "modelo_legal.pkl"
    with open(out_path, "wb") as f:
        pickle.dump({
            "modelo": "scikit-learn",
            "vectorizador": vectorizer,
            "clasificador": clf,
        }, f)

    return {"status": "ok", "path": str(out_path)}


if __name__ == "__main__":
    # Entrenamiento CLI rápido
    BASE_DIR = Path(__file__).resolve().parents[1] / "sentencias"
    UPLOADS_DIR = Path(__file__).resolve().parents[1] / "uploads"
    MODELS_DIR = Path(__file__).resolve().parents[1] / "models"
    LABELS = MODELS_DIR / "labels.json"

    res = train_and_save(BASE_DIR, UPLOADS_DIR, MODELS_DIR, LABELS)
    print(res)


