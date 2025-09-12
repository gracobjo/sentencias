#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Versión mínima de la aplicación para diagnosticar problemas de despliegue
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Analizador de Sentencias IPP/INSS - Minimal",
    description="Versión mínima para diagnosticar problemas",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Página principal"""
    return """
    <html>
        <head><title>Analizador de Sentencias - Test</title></head>
        <body>
            <h1>✅ Aplicación funcionando correctamente</h1>
            <p>Versión mínima desplegada exitosamente</p>
            <ul>
                <li><a href="/health">Health Check</a></li>
                <li><a href="/test">Test Endpoint</a></li>
            </ul>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Aplicación funcionando"}

@app.get("/test")
async def test_endpoint():
    """Endpoint de prueba"""
    return {"message": "Test endpoint funcionando", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
