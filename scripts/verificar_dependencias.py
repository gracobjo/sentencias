#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación de dependencias para modelos de IA.

Este script verifica que todas las librerías necesarias estén instaladas
con las versiones correctas para el funcionamiento del sistema.

Uso:
    python scripts/verificar_dependencias.py [--verbose] [--produccion]
"""

import argparse
import sys
import importlib
from pathlib import Path

# Configurar logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def verificar_libreria(nombre, version_esperada=None, opcional=False):
    """Verifica si una librería está instalada y su versión"""
    try:
        modulo = importlib.import_module(nombre)
        version_actual = getattr(modulo, '__version__', 'Desconocida')
        
        if version_esperada and version_actual != version_esperada:
            logger.warning(f"⚠️ {nombre}: {version_actual} (esperada: {version_esperada})")
            return False
        else:
            logger.info(f"✅ {nombre}: {version_actual}")
            return True
            
    except ImportError:
        if opcional:
            logger.warning(f"⚠️ {nombre}: No instalado (opcional)")
            return False
        else:
            logger.error(f"❌ {nombre}: No instalado (requerido)")
            return False


def verificar_dependencias_core():
    """Verifica dependencias core del sistema"""
    logger.info("🔍 Verificando dependencias core...")
    
    dependencias_core = {
        'numpy': '1.26.4',
        'sklearn': '1.7.0',
        'fastapi': '0.109.2',
        'uvicorn': '0.27.1',
        'jinja2': '3.1.2',
        'PyPDF2': '3.0.1',
        'python-docx': '1.2.0',
        'lxml': '6.0.1',
        'requests': '2.31.0',
        'tqdm': '4.66.1'
    }
    
    resultados = {}
    for lib, version in dependencias_core.items():
        resultados[lib] = verificar_libreria(lib, version)
    
    return resultados


def verificar_dependencias_ml():
    """Verifica dependencias de machine learning"""
    logger.info("🧠 Verificando dependencias de machine learning...")
    
    dependencias_ml = {
        'numpy': '1.26.4',
        'sklearn': '1.7.0',
        'scipy': '1.16.0',
        'sentence_transformers': '2.7.0',
        'transformers': '4.49.0',
        'torch': '2.7.1'
    }
    
    resultados = {}
    for lib, version in dependencias_ml.items():
        resultados[lib] = verificar_libreria(lib, version)
    
    return resultados


def verificar_dependencias_nlp():
    """Verifica dependencias de procesamiento de lenguaje natural"""
    logger.info("📝 Verificando dependencias de NLP...")
    
    dependencias_nlp = {
        'nltk': '3.8.1',
        'spacy': '3.7.2',
        'regex': '2024.11.6',
        'tokenizers': '0.21.2'
    }
    
    resultados = {}
    for lib, version in dependencias_nlp.items():
        resultados[lib] = verificar_libreria(lib, version)
    
    return resultados


def verificar_modelos_sbert():
    """Verifica que los modelos SBERT estén disponibles"""
    logger.info("🤖 Verificando modelos SBERT...")
    
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
        
        # Verificar modelo principal
        try:
            encoder = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("✅ Modelo all-MiniLM-L6-v2: Disponible")
            
            # Probar encoding
            test_text = ["Este es un texto de prueba"]
            embeddings = encoder.encode(test_text)
            logger.info(f"✅ Encoding funcional: {embeddings.shape}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error con modelo all-MiniLM-L6-v2: {e}")
            return False
            
    except ImportError:
        logger.error("❌ Sentence-Transformers no disponible")
        return False


def verificar_modelos_spacy():
    """Verifica que los modelos de spaCy estén disponibles"""
    logger.info("🌍 Verificando modelos de spaCy...")
    
    try:
        import spacy
        
        modelos = ['es_core_news_sm', 'en_core_web_sm']
        resultados = {}
        
        for modelo in modelos:
            try:
                nlp = spacy.load(modelo)
                logger.info(f"✅ {modelo}: Disponible")
                resultados[modelo] = True
            except OSError:
                logger.warning(f"⚠️ {modelo}: No instalado")
                resultados[modelo] = False
        
        return resultados
        
    except ImportError:
        logger.error("❌ spaCy no disponible")
        return {}


def verificar_recursos_nltk():
    """Verifica que los recursos de NLTK estén disponibles"""
    logger.info("📚 Verificando recursos de NLTK...")
    
    try:
        import nltk
        
        recursos = ['punkt', 'stopwords', 'wordnet']
        resultados = {}
        
        for recurso in recursos:
            try:
                nltk.data.find(f'tokenizers/{recurso}')
                logger.info(f"✅ {recurso}: Disponible")
                resultados[recurso] = True
            except LookupError:
                logger.warning(f"⚠️ {recurso}: No instalado")
                resultados[recurso] = False
        
        return resultados
        
    except ImportError:
        logger.error("❌ NLTK no disponible")
        return {}


def verificar_memoria_sistema():
    """Verifica recursos del sistema"""
    logger.info("💾 Verificando recursos del sistema...")
    
    try:
        import psutil  # type: ignore
        
        # Memoria RAM
        memoria = psutil.virtual_memory()
        memoria_gb = memoria.total / (1024**3)
        memoria_disponible_gb = memoria.available / (1024**3)
        
        logger.info(f"💾 RAM Total: {memoria_gb:.1f} GB")
        logger.info(f"💾 RAM Disponible: {memoria_disponible_gb:.1f} GB")
        
        # CPU
        cpu_count = psutil.cpu_count()
        logger.info(f"🖥️ CPUs: {cpu_count}")
        
        # Espacio en disco
        disco = psutil.disk_usage('/')
        disco_gb = disco.total / (1024**3)
        disco_disponible_gb = disco.free / (1024**3)
        
        logger.info(f"💿 Disco Total: {disco_gb:.1f} GB")
        logger.info(f"💿 Disco Disponible: {disco_disponible_gb:.1f} GB")
        
        return {
            'ram_total': memoria_gb,
            'ram_disponible': memoria_disponible_gb,
            'cpu_count': cpu_count,
            'disco_total': disco_gb,
            'disco_disponible': disco_disponible_gb
        }
        
    except ImportError:
        logger.warning("⚠️ psutil no disponible - no se puede verificar recursos del sistema")
        return {}


def main():
    parser = argparse.ArgumentParser(
        description="Verificar dependencias del sistema de análisis legal"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Mostrar información detallada"
    )
    parser.add_argument(
        "--produccion", 
        action="store_true",
        help="Verificar solo dependencias de producción"
    )
    parser.add_argument(
        "--ml", 
        action="store_true",
        help="Verificar solo dependencias de machine learning"
    )
    parser.add_argument(
        "--nlp", 
        action="store_true",
        help="Verificar solo dependencias de NLP"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("🚀 Iniciando verificación de dependencias")
    
    # Verificar dependencias core
    if not args.ml and not args.nlp:
        resultados_core = verificar_dependencias_core()
        core_ok = all(resultados_core.values())
    else:
        core_ok = True
    
    # Verificar dependencias de ML
    if args.ml or (not args.produccion and not args.nlp):
        resultados_ml = verificar_dependencias_ml()
        ml_ok = all(resultados_ml.values())
        
        # Verificar modelos SBERT
        sbert_ok = verificar_modelos_sbert()
    else:
        ml_ok = True
        sbert_ok = True
    
    # Verificar dependencias de NLP
    if args.nlp or (not args.produccion and not args.ml):
        resultados_nlp = verificar_dependencias_nlp()
        nlp_ok = all(resultados_nlp.values())
        
        # Verificar modelos específicos
        modelos_spacy = verificar_modelos_spacy()
        recursos_nltk = verificar_recursos_nltk()
    else:
        nlp_ok = True
    
    # Verificar recursos del sistema
    recursos = verificar_memoria_sistema()
    
    # Resumen final
    logger.info("\n📊 Resumen de verificación:")
    
    if not args.ml and not args.nlp:
        logger.info(f"🔧 Dependencias Core: {'✅ OK' if core_ok else '❌ ERROR'}")
    
    if args.ml or (not args.produccion and not args.nlp):
        logger.info(f"🧠 Machine Learning: {'✅ OK' if ml_ok else '❌ ERROR'}")
        logger.info(f"🤖 Modelos SBERT: {'✅ OK' if sbert_ok else '❌ ERROR'}")
    
    if args.nlp or (not args.produccion and not args.ml):
        logger.info(f"📝 Procesamiento NLP: {'✅ OK' if nlp_ok else '❌ ERROR'}")
    
    # Verificar si el sistema está listo
    sistema_listo = core_ok and ml_ok and sbert_ok and nlp_ok
    
    if sistema_listo:
        logger.info("\n🎉 Sistema listo para usar!")
        logger.info("💡 Todas las dependencias están instaladas correctamente")
        return 0
    else:
        logger.error("\n❌ Sistema no está listo")
        logger.error("💡 Instala las dependencias faltantes antes de continuar")
        return 1


if __name__ == "__main__":
    exit(main())
