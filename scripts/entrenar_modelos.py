#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de entrenamiento completo de modelos de IA para el sistema de análisis legal.

Este script entrena tanto el modelo TF-IDF como el modelo SBERT,
generando los archivos .pkl necesarios para el funcionamiento del sistema.

Uso:
    python scripts/entrenar_modelos.py [--etiquetas] [--verbose]
"""

import argparse
import logging
import sys
from pathlib import Path

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from backend.train_model import train_and_save as train_tfidf
from backend.train_embeddings import train_and_save as train_sbert

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Entrenar modelos de IA para análisis legal"
    )
    parser.add_argument(
        "--etiquetas", 
        action="store_true",
        help="Usar etiquetas manuales si están disponibles"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Mostrar información detallada del proceso"
    )
    parser.add_argument(
        "--solo-tfidf", 
        action="store_true",
        help="Entrenar solo el modelo TF-IDF"
    )
    parser.add_argument(
        "--solo-sbert", 
        action="store_true",
        help="Entrenar solo el modelo SBERT"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Configurar directorios
    base_dir = Path(__file__).parent.parent / "sentencias"
    uploads_dir = Path(__file__).parent.parent / "uploads"
    models_dir = Path(__file__).parent.parent / "models"
    labels_path = models_dir / "labels.json" if args.etiquetas else None
    
    logger.info("🚀 Iniciando entrenamiento de modelos de IA")
    logger.info(f"📁 Directorio base: {base_dir}")
    logger.info(f"📁 Directorio uploads: {uploads_dir}")
    logger.info(f"📁 Directorio modelos: {models_dir}")
    
    # Verificar que existen documentos
    documentos_encontrados = 0
    for directorio in [base_dir, uploads_dir]:
        if directorio.exists():
            documentos_encontrados += len(list(directorio.glob("*.pdf")))
            documentos_encontrados += len(list(directorio.glob("*.txt")))
    
    if documentos_encontrados == 0:
        logger.error("❌ No se encontraron documentos para entrenar")
        logger.error("   Asegúrate de tener archivos PDF o TXT en:")
        logger.error(f"   - {base_dir}")
        logger.error(f"   - {uploads_dir}")
        return 1
    
    logger.info(f"📄 Documentos encontrados: {documentos_encontrados}")
    
    # Crear directorio de modelos si no existe
    models_dir.mkdir(parents=True, exist_ok=True)
    
    resultados = {}
    
    # Entrenar modelo TF-IDF
    if not args.solo_sbert:
        try:
            logger.info("🔤 Entrenando modelo TF-IDF...")
            resultado_tfidf = train_tfidf(base_dir, uploads_dir, models_dir, labels_path)
            resultados["tfidf"] = resultado_tfidf
            logger.info(f"✅ Modelo TF-IDF entrenado: {resultado_tfidf['path']}")
        except Exception as e:
            logger.error(f"❌ Error entrenando modelo TF-IDF: {e}")
            resultados["tfidf"] = {"error": str(e)}
    
    # Entrenar modelo SBERT
    if not args.solo_tfidf:
        try:
            logger.info("🧠 Entrenando modelo SBERT...")
            resultado_sbert = train_sbert(base_dir, uploads_dir, models_dir, labels_path)
            resultados["sbert"] = resultado_sbert
            logger.info(f"✅ Modelo SBERT entrenado: {resultado_sbert['path']}")
        except Exception as e:
            logger.error(f"❌ Error entrenando modelo SBERT: {e}")
            resultados["sbert"] = {"error": str(e)}
    
    # Resumen final
    logger.info("\n📊 Resumen del entrenamiento:")
    for modelo, resultado in resultados.items():
        if "error" in resultado:
            logger.error(f"❌ {modelo.upper()}: {resultado['error']}")
        else:
            logger.info(f"✅ {modelo.upper()}: {resultado['path']}")
    
    # Verificar archivos generados
    modelo_tfidf = models_dir / "modelo_legal.pkl"
    modelo_sbert = models_dir / "modelo_legal_sbert.pkl"
    
    logger.info("\n📁 Archivos generados:")
    if modelo_tfidf.exists():
        size_mb = modelo_tfidf.stat().st_size / (1024 * 1024)
        logger.info(f"✅ {modelo_tfidf.name} ({size_mb:.2f} MB)")
    else:
        logger.warning(f"⚠️ {modelo_tfidf.name} no encontrado")
    
    if modelo_sbert.exists():
        size_mb = modelo_sbert.stat().st_size / (1024 * 1024)
        logger.info(f"✅ {modelo_sbert.name} ({size_mb:.2f} MB)")
    else:
        logger.warning(f"⚠️ {modelo_sbert.name} no encontrado")
    
    logger.info("\n🎉 Entrenamiento completado!")
    logger.info("💡 Los modelos están listos para usar en el sistema")
    
    return 0


if __name__ == "__main__":
    exit(main())
