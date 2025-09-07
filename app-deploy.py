#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de Sentencias IPP/INSS - Versión simplificada para despliegue
Versión optimizada sin dependencias pesadas como spaCy
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
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cache para análisis
ANALISIS_CACHE = {}
CACHE_TIMESTAMP = None
CACHE_DURATION = 300  # 5 minutos en segundos

# Crear aplicación FastAPI con configuración robusta
app = FastAPI(
    title="Analizador de Sentencias IPP/INSS",
    description="API robusta para análisis inteligente de documentos legales",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para desarrollo
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
BASE_DIR = Path(__file__).parent
SENTENCIAS_DIR = BASE_DIR / "sentencias"
UPLOAD_DIR = BASE_DIR / "uploads"

# Crear directorios si no existen
SENTENCIAS_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

# Lock para operaciones concurrentes
file_lock = Lock()

# Frases clave simplificadas para análisis básico
FRASES_CLAVE_BASICAS = {
    "procedimiento": [
        "procedimiento administrativo", "procedimiento sancionador", "procedimiento disciplinario",
        "procedimiento de responsabilidad patrimonial", "procedimiento de reclamación"
    ],
    "derechos": [
        "derecho a la tutela judicial efectiva", "derecho a la defensa", "derecho a la presunción de inocencia",
        "derecho a la intimidad", "derecho a la protección de datos"
    ],
    "sanciones": [
        "sanción disciplinaria", "sanción administrativa", "sanción pecuniaria",
        "sanción de separación del servicio", "sanción de suspensión"
    ],
    "recursos": [
        "recurso de alzada", "recurso de reposición", "recurso contencioso administrativo",
        "recurso de amparo", "recurso de casación"
    ]
}

class AnalizadorBasico:
    """Analizador básico sin dependencias pesadas"""
    
    def __init__(self):
        self.frases_clave = FRASES_CLAVE_BASICAS
    
    def analizar_documento(self, ruta_archivo: str, nombre_original: str = "") -> Dict[str, Any]:
        """Analiza un documento usando métodos básicos"""
        try:
            # Leer contenido del archivo
            contenido = self._leer_archivo(ruta_archivo)
            if not contenido:
                return self._crear_resultado_error("No se pudo leer el contenido del archivo")
            
            # Análisis básico
            frases_encontradas = self._contar_frases_clave(contenido, nombre_original)
            prediccion = self._prediccion_basica(contenido)
            argumentos = self._extraer_argumentos(contenido)
            
            return {
                "archivo": ruta_archivo,
                "nombre_archivo": nombre_original or Path(ruta_archivo).name,
                "procesado": True,
                "texto_extraido": contenido[:1000] + "..." if len(contenido) > 1000 else contenido,
                "longitud_texto": len(contenido),
                "prediccion": prediccion,
                "argumentos": argumentos,
                "frases_clave": frases_encontradas,
                "resumen_inteligente": self._generar_resumen(prediccion, frases_encontradas),
                "timestamp": datetime.now().isoformat(),
                "total_frases": sum(info.get("total", 0) for info in frases_encontradas.values())
            }
            
        except Exception as e:
            logger.error(f"Error analizando documento {ruta_archivo}: {e}")
            return self._crear_resultado_error(f"Error en análisis: {str(e)}")
    
    def _leer_archivo(self, ruta_archivo: str) -> str:
        """Lee el contenido de un archivo"""
        try:
            archivo = Path(ruta_archivo)
            if archivo.suffix.lower() == '.txt':
                with open(archivo, 'r', encoding='utf-8') as f:
                    return f.read()
            elif archivo.suffix.lower() == '.pdf':
                # Implementación básica de PDF sin PyPDF2 pesado
                return "Contenido PDF básico - requiere implementación completa"
            else:
                return ""
        except Exception as e:
            logger.error(f"Error leyendo archivo {ruta_archivo}: {e}")
            return ""
    
    def _contar_frases_clave(self, contenido: str, nombre_archivo: str) -> Dict[str, Any]:
        """Cuenta las apariciones de frases clave"""
        resultado = {}
        contenido_lower = contenido.lower()
        
        for categoria, frases in self.frases_clave.items():
            total_apariciones = 0
            ocurrencias = []
            
            for frase in frases:
                count = contenido_lower.count(frase.lower())
                if count > 0:
                    total_apariciones += count
                    ocurrencias.append({
                        "frase": frase,
                        "apariciones": count,
                        "archivo": nombre_archivo
                    })
            
            if total_apariciones > 0:
                resultado[categoria] = {
                    "total": total_apariciones,
                    "frases": [f["frase"] for f in ocurrencias],
                    "ocurrencias": ocurrencias
                }
        
        return resultado
    
    def _prediccion_basica(self, contenido: str) -> Dict[str, Any]:
        """Predicción básica basada en palabras clave"""
        contenido_lower = contenido.lower()
        
        # Palabras clave para diferentes tipos de resolución
        palabras_favorables = ["estimamos", "estimamos parcialmente", "estimamos la solicitud"]
        palabras_desfavorables = ["desestimamos", "desestimamos la solicitud", "denegamos"]
        
        favorables = sum(contenido_lower.count(p) for p in palabras_favorables)
        desfavorables = sum(contenido_lower.count(p) for p in palabras_desfavorables)
        
        if favorables > desfavorables:
            resultado = "Favorable"
            probabilidad = min(0.8, 0.5 + (favorables * 0.1))
        elif desfavorables > favorables:
            resultado = "Desfavorable"
            probabilidad = min(0.8, 0.5 + (desfavorables * 0.1))
        else:
            resultado = "Indeterminado"
            probabilidad = 0.5
        
        return {
            "resultado": resultado,
            "probabilidad": probabilidad,
            "razones": [
                f"Palabras favorables encontradas: {favorables}",
                f"Palabras desfavorables encontradas: {desfavorables}"
            ]
        }
    
    def _extraer_argumentos(self, contenido: str) -> List[str]:
        """Extrae argumentos básicos del contenido"""
        # Buscar patrones comunes de argumentación
        patrones = [
            r"por cuanto\s+([^.]{20,200})",
            r"considerando\s+([^.]{20,200})",
            r"en consecuencia\s+([^.]{20,200})"
        ]
        
        argumentos = []
        for patron in patrones:
            matches = re.findall(patron, contenido, re.IGNORECASE)
            argumentos.extend(matches)
        
        return argumentos[:5]  # Limitar a 5 argumentos
    
    def _generar_resumen(self, prediccion: Dict, frases_clave: Dict) -> str:
        """Genera un resumen básico"""
        resultado = prediccion.get("resultado", "Indeterminado")
        probabilidad = prediccion.get("probabilidad", 0.5)
        
        resumen = f"Análisis básico: {resultado} (probabilidad: {probabilidad:.1%})\n"
        resumen += f"Categorías encontradas: {len(frases_clave)}\n"
        
        if frases_clave:
            categoria_principal = max(frases_clave.items(), key=lambda x: x[1]["total"])
            resumen += f"Categoría principal: {categoria_principal[0]} ({categoria_principal[1]['total']} apariciones)"
        
        return resumen
    
    def _crear_resultado_error(self, mensaje: str) -> Dict[str, Any]:
        """Crea un resultado de error"""
        return {
            "procesado": False,
            "error": mensaje,
            "timestamp": datetime.now().isoformat()
        }

# Instanciar analizador
analizador_basico = AnalizadorBasico()

# Rutas principales
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal con análisis de sentencias"""
    try:
        # Obtener análisis de sentencias existentes
        datos_analisis = analizar_sentencias_existentes()
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "resultados_por_archivo": datos_analisis.get("resultados_por_archivo", {}),
            "ranking_global": datos_analisis.get("ranking_global", {}),
            "total_apariciones": datos_analisis.get("total_apariciones", 0),
            "archivos_analizados": datos_analisis.get("archivos_analizados", 0)
        })
    except Exception as e:
        logger.error(f"Error en página principal: {e}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "resultados_por_archivo": {},
            "ranking_global": {},
            "total_apariciones": 0,
            "archivos_analizados": 0,
            "error": f"Error cargando datos: {str(e)}"
        })

def analizar_sentencias_existentes() -> Dict[str, Any]:
    """Analiza las sentencias existentes en la carpeta con caché"""
    global CACHE_TIMESTAMP, ANALISIS_CACHE
    
    # Verificar si el caché es válido
    if (CACHE_TIMESTAMP and 
        (datetime.now() - CACHE_TIMESTAMP).total_seconds() < CACHE_DURATION and 
        ANALISIS_CACHE):
        logger.info("📋 Usando análisis desde caché")
        return ANALISIS_CACHE
    
    try:
        logger.info(f"🔍 Iniciando análisis de sentencias existentes en: {SENTENCIAS_DIR}")
        
        if not SENTENCIAS_DIR.exists():
            logger.warning(f"❌ La carpeta '{SENTENCIAS_DIR}' no existe")
            resultado = {
                "error": f"La carpeta '{SENTENCIAS_DIR}' no existe",
                "archivos_analizados": 0,
                "total_apariciones": 0,
                "resultados_por_archivo": {},
                "ranking_global": {}
            }
            ANALISIS_CACHE = resultado
            CACHE_TIMESTAMP = datetime.now()
            return resultado
        
        # Buscar archivos de texto y PDF
        archivos_soportados = [f for f in SENTENCIAS_DIR.iterdir() 
                              if f.suffix.lower() in ['.txt', '.pdf']]
        
        logger.info(f"📁 Archivos encontrados: {[f.name for f in archivos_soportados]}")
        
        if not archivos_soportados:
            logger.warning(f"❌ No se encontraron archivos .txt o .pdf en '{SENTENCIAS_DIR}'")
            resultado = {
                "error": f"No se encontraron archivos .txt o .pdf en '{SENTENCIAS_DIR}'",
                "archivos_analizados": 0,
                "total_apariciones": 0,
                "resultados_por_archivo": {},
                "ranking_global": {}
            }
            ANALISIS_CACHE = resultado
            CACHE_TIMESTAMP = datetime.now()
            return resultado
        
        resultados_por_archivo = {}
        ranking_global = {}
        total_apariciones = 0
        
        for archivo in archivos_soportados:
            try:
                logger.info(f"🔍 Analizando archivo: {archivo.name}")
                
                # Usar analizador básico
                resultado = analizador_basico.analizar_documento(str(archivo), archivo.name)
                resultados_por_archivo[archivo.name] = resultado
                
                # Agregar al ranking global
                if resultado.get("frases_clave"):
                    for categoria, info in resultado["frases_clave"].items():
                        if categoria not in ranking_global:
                            ranking_global[categoria] = {"total": 0, "ocurrencias": []}
                        ranking_global[categoria]["total"] += info["total"]
                        ranking_global[categoria]["ocurrencias"].extend(info.get("ocurrencias", []))
                        total_apariciones += info["total"]
                
                logger.info(f"✅ Archivo {archivo.name} analizado correctamente")
                
            except Exception as e:
                logger.error(f"❌ Error analizando {archivo.name}: {e}")
                resultados_por_archivo[archivo.name] = {
                    "procesado": False,
                    "error": f"Error analizando archivo: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }
        
        # Ordenar ranking
        ranking_ordenado = dict(sorted(ranking_global.items(), key=lambda x: x[1]["total"], reverse=True))
        
        logger.info(f"📊 RESUMEN FINAL:")
        logger.info(f"  - Archivos analizados: {len(archivos_soportados)}")
        logger.info(f"  - Total apariciones: {total_apariciones}")
        logger.info(f"  - Categorías encontradas: {list(ranking_ordenado.keys())}")
        
        resultado = {
            "archivos_analizados": len(archivos_soportados),
            "total_apariciones": total_apariciones,
            "resultados_por_archivo": resultados_por_archivo,
            "ranking_global": ranking_ordenado
        }
        
        # Guardar en caché
        ANALISIS_CACHE = resultado
        CACHE_TIMESTAMP = datetime.now()
        logger.info("💾 Análisis guardado en caché")
        
        return resultado
        
    except Exception as e:
        logger.error(f"❌ Error analizando sentencias: {e}")
        return {
            "error": f"Error al analizar sentencias: {str(e)}",
            "archivos_analizados": 0,
            "total_apariciones": 0,
            "resultados_por_archivo": {},
            "ranking_global": {}
        }

# API endpoints
@app.get("/api/analizar")
async def api_analizar():
    """Endpoint API para análisis"""
    try:
        return analizar_sentencias_existentes()
    except Exception as e:
        logger.error(f"Error en API: {e}")
        return {"error": f"Error al analizar: {str(e)}"}

@app.post("/api/limpiar-cache")
async def limpiar_cache():
    """Endpoint para limpiar el caché de análisis"""
    global CACHE_TIMESTAMP, ANALISIS_CACHE
    ANALISIS_CACHE = {}
    CACHE_TIMESTAMP = None
    logger.info("🗑️ Caché limpiado")
    return JSONResponse(content={"mensaje": "Caché limpiado correctamente"})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
