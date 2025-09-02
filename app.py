#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada principal para el Analizador de Sentencias IPP/INSS

Este archivo mantiene compatibilidad hacia atrás mientras la aplicación
se ejecuta desde el paquete sentencias_app.
"""

import sys
import os
from pathlib import Path

# Añadir el directorio actual al path para imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Importar la aplicación desde el paquete
from sentencias_app import app

if __name__ == "__main__":
    import uvicorn
    
    # Configuración para desarrollo
    uvicorn.run(
        "sentencias_app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
