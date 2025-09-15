#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API FastAPI para análisis de resoluciones administrativas
Proporciona endpoint para analizar sentencias y renderizar resultados
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from pathlib import Path

# Importar funciones de análisis
from analisis import analizar_sentencias

# Crear aplicación FastAPI
app = FastAPI(
    title="Analizador de Resoluciones IPP/INSS",
    description="API para analizar resoluciones administrativas en busca de frases clave",
    version="1.0.0"
)

# Configurar templates y archivos estáticos
templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")

# Obtener ruta absoluta de la carpeta sentencias
BASE_DIR = Path(__file__).resolve().parent.parent
SENTENCIAS_DIR = BASE_DIR / "sentencias"


@app.get("/", response_class=HTMLResponse)
async def analizar_y_mostrar(request: Request):
    """
    Endpoint principal que analiza las sentencias y renderiza la página HTML
    
    Args:
        request (Request): Objeto de solicitud FastAPI
        
    Returns:
        HTMLResponse: Página HTML con resultados del análisis
    """
    try:
        # Analizar sentencias usando ruta relativa desde el directorio del proyecto
        resultado = analizar_sentencias(str(SENTENCIAS_DIR))
        
        # Renderizar template con resultados
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "resultado": resultado,
                "error": resultado.get("error"),
                "archivos_analizados": resultado.get("archivos_analizados", 0),
                "total_apariciones": resultado.get("total_apariciones", 0),
                "resultados_por_archivo": resultado.get("resultados_por_archivo", {}),
                "ranking_global": resultado.get("ranking_global", {})
            }
        )
        
    except Exception as e:
        # En caso de error, mostrar página con mensaje de error
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"Error al analizar sentencias: {str(e)}",
                "archivos_analizados": 0,
                "total_apariciones": 0,
                "resultados_por_archivo": {},
                "ranking_global": {}
            }
        )


@app.get("/api/analizar")
async def api_analizar():
    """
    Endpoint API que devuelve solo los datos del análisis en formato JSON
    
    Returns:
        dict: Resultados del análisis en formato JSON
    """
    try:
        resultado = analizar_sentencias(str(SENTENCIAS_DIR))
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar sentencias: {str(e)}")


@app.get("/health")
async def health_check():
    """
    Endpoint de verificación de salud de la API
    
    Returns:
        dict: Estado de la API
    """
    return {
        "status": "ok",
        "version": "1.0.0",
        "sentencias_dir": str(SENTENCIAS_DIR),
        "sentencias_dir_exists": SENTENCIAS_DIR.exists()
    }


if __name__ == "__main__":
    import uvicorn
    
    print("Iniciando servidor de análisis de resoluciones...")
    print(f"Directorio de sentencias: {SENTENCIAS_DIR}")
    print("Ejecuta: uvicorn backend.main:app --reload")
    
    # Solo para desarrollo local
    uvicorn.run(app, host="0.0.0.0", port=8000)
