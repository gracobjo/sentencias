#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de Sentencias IPP/INSS - Versión restaurada paso a paso
"""

import os
import json
import re
import uuid
import shutil
import logging
from pathlib import Path
from threading import Lock
from typing import Optional, Dict, List, Any
from datetime import datetime
from io import BytesIO

from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Analizador de Sentencias IPP/INSS",
    description="Sistema de análisis de sentencias y documentos legales",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar archivos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configuración de directorios
BASE_DIR = Path(__file__).resolve().parent
SENTENCIAS_DIR = BASE_DIR / "sentencias"
UPLOADS_DIR = BASE_DIR / "uploads"

# Crear directorios si no existen
SENTENCIAS_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)

# Variables globales
analizador_cache = {}
cache_lock = Lock()

@app.get("/", response_class=HTMLResponse)
async def pagina_principal(request: Request):
    """Página principal con lista de documentos"""
    try:
        # Obtener lista de documentos
        documentos = []
        
        # Buscar en directorio sentencias
        for archivo in SENTENCIAS_DIR.glob("*"):
            if archivo.is_file() and archivo.suffix.lower() in ['.pdf', '.txt', '.docx']:
                documentos.append({
                    "nombre": archivo.name,
                    "ruta": str(archivo),
                    "tamaño": archivo.stat().st_size,
                    "fecha": datetime.fromtimestamp(archivo.stat().st_mtime)
                })
        
        # Buscar en directorio uploads
        for archivo in UPLOADS_DIR.glob("*"):
            if archivo.is_file() and archivo.suffix.lower() in ['.pdf', '.txt', '.docx']:
                documentos.append({
                    "nombre": archivo.name,
                    "ruta": str(archivo),
                    "tamaño": archivo.stat().st_size,
                    "fecha": datetime.fromtimestamp(archivo.stat().st_mtime)
                })
        
        # Ordenar por fecha (más recientes primero)
        documentos.sort(key=lambda x: x["fecha"], reverse=True)
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "documentos": documentos,
            "total_documentos": len(documentos)
        })
        
    except Exception as e:
        logger.error(f"Error en página principal: {e}")
        return HTMLResponse(f"<h1>Error</h1><p>{str(e)}</p>", status_code=500)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Aplicación funcionando", "version": "1.0.0"}

@app.get("/test")
async def test_endpoint():
    """Endpoint de prueba"""
    return {"message": "Test endpoint funcionando", "version": "1.0.0"}

@app.get("/listar-archivos")
async def listar_archivos_disponibles():
    """Endpoint para listar todos los archivos disponibles para análisis"""
    try:
        archivos_sentencias = [f.name for f in SENTENCIAS_DIR.glob("*") if f.is_file()]
        archivos_uploads = [f.name for f in UPLOADS_DIR.glob("*") if f.is_file()]
        
        return {
            "archivos_sentencias": archivos_sentencias,
            "archivos_uploads": archivos_uploads,
            "total_sentencias": len(archivos_sentencias),
            "total_uploads": len(archivos_uploads),
            "directorio_actual": str(Path.cwd()),
            "directorio_sentencias": str(SENTENCIAS_DIR.resolve()),
            "directorio_uploads": str(UPLOADS_DIR.resolve()),
            "existe_sentencias": SENTENCIAS_DIR.exists(),
            "existe_uploads": UPLOADS_DIR.exists()
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/analisis-discrepancias/{archivo_id}")
async def pagina_analisis_discrepancias(request: Request, archivo_id: str):
    """Página web para mostrar análisis de discrepancias de un archivo específico"""
    try:
        logger.info(f"🔍 Buscando archivo para análisis de discrepancias: {archivo_id}")
        
        # Buscar el archivo en ambos directorios
        archivo_path = None
        
        # Buscar en directorio sentencias (PDF y otros formatos)
        for extension in ["*.pdf", "*.txt", "*.docx"]:
            for archivo in SENTENCIAS_DIR.glob(extension):
                if archivo_id in archivo.name or archivo.name in archivo_id:
                    archivo_path = archivo
                    logger.info(f"✅ Archivo encontrado en sentencias/: {archivo}")
                    break
            if archivo_path:
                break
        
        # Si no se encuentra, buscar en directorio uploads
        if not archivo_path:
            for extension in ["*.pdf", "*.txt", "*.docx"]:
                for archivo in UPLOADS_DIR.glob(extension):
                    if archivo_id in archivo.name or archivo.name in archivo_id:
                        archivo_path = archivo
                        logger.info(f"✅ Archivo encontrado en uploads/: {archivo}")
                        break
                if archivo_path:
                    break
        
        # Búsqueda más flexible: buscar por partes del nombre
        if not archivo_path:
            logger.info(f"🔍 Búsqueda flexible para: {archivo_id}")
            # Extraer partes del ID que podrían ser el nombre real
            partes_id = archivo_id.split('_')
            posibles_nombres = [p for p in partes_id if len(p) > 5 and not p.isdigit()]
            
            for nombre_posible in posibles_nombres:
                logger.info(f"🔍 Buscando archivos que contengan: {nombre_posible}")
                for extension in ["*.pdf", "*.txt", "*.docx"]:
                    for archivo in SENTENCIAS_DIR.glob(extension):
                        if nombre_posible in archivo.name:
                            archivo_path = archivo
                            logger.info(f"✅ Archivo encontrado por búsqueda flexible en sentencias/: {archivo}")
                            break
                    if archivo_path:
                        break
                    
                    for archivo in UPLOADS_DIR.glob(extension):
                        if nombre_posible in archivo.name:
                            archivo_path = archivo
                            logger.info(f"✅ Archivo encontrado por búsqueda flexible en uploads/: {archivo}")
                            break
                    if archivo_path:
                        break
                if archivo_path:
                    break
        
        # Búsqueda final: buscar archivos que contengan 'informe' y parte del hash
        if not archivo_path and 'informe' in archivo_id:
            logger.info("🔍 Búsqueda final por archivos de informe...")
            hash_parts = [p for p in archivo_id.split('_') if len(p) == 8 and p.isalnum()]
            for hash_part in hash_parts:
                for archivo in SENTENCIAS_DIR.glob("*informe*.pdf"):
                    if hash_part in archivo.name:
                        archivo_path = archivo
                        logger.info(f"✅ Archivo encontrado por búsqueda de informe en sentencias/: {archivo}")
                        break
                if archivo_path:
                    break
                    
                for archivo in UPLOADS_DIR.glob("*informe*.pdf"):
                    if hash_part in archivo.name:
                        archivo_path = archivo
                        logger.info(f"✅ Archivo encontrado por búsqueda de informe en uploads/: {archivo}")
                        break
                if archivo_path:
                    break
        
        if not archivo_path:
            logger.error(f"❌ Archivo no encontrado: {archivo_id}")
            # Listar archivos disponibles para debug
            archivos_sentencias = list(SENTENCIAS_DIR.glob("*"))
            archivos_uploads = list(UPLOADS_DIR.glob("*"))
            logger.info(f"Archivos en sentencias/: {[f.name for f in archivos_sentencias]}")
            logger.info(f"Archivos en uploads/: {[f.name for f in archivos_uploads]}")
            raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {archivo_id}")
        
        # Crear resultado de análisis básico (sin IA por ahora)
        resultado = {
            "nombre_archivo": archivo_path.name,
            "ruta_archivo": str(archivo_path),
            "procesado": True,
            "analisis_discrepancias": {
                "discrepancias_detectadas": [
                    {
                        "tipo": "ejemplo",
                        "descripcion": "Análisis básico funcionando",
                        "texto": "Este es un análisis de prueba",
                        "posicion": 0,
                        "severidad": "media",
                        "argumento": "Sistema funcionando correctamente"
                    }
                ],
                "evidencia_favorable": [
                    "Sistema de análisis funcionando",
                    "Búsqueda de archivos operativa"
                ],
                "argumentos_juridicos": [
                    "El sistema está funcionando correctamente",
                    "Análisis básico disponible"
                ],
                "contradicciones_internas": [],
                "recomendaciones_defensa": [
                    "Sistema operativo y listo para análisis completo"
                ],
                "puntuacion_discrepancia": 50,
                "probabilidad_ipp": 0.5,
                "resumen_ejecutivo": "Sistema funcionando correctamente. Análisis básico disponible."
            }
        }
        
        return templates.TemplateResponse("analisis_discrepancias.html", {
            "request": request,
            "resultado": resultado
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en análisis de discrepancias: {e}")
        raise HTTPException(status_code=500, detail=f"Error procesando archivo: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
