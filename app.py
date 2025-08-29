#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de Sentencias IPP/INSS - Aplicación FastAPI
Aplicación robusta para análisis de documentos legales con modelo de IA pre-entrenado
"""

import os
import re
import uuid
import shutil
import logging
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime

from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

# Configurar templates y archivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración de directorios
BASE_DIR = Path(__file__).parent
SENTENCIAS_DIR = BASE_DIR / "sentencias"
UPLOADS_DIR = BASE_DIR / "uploads"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# Crear directorios necesarios
for directory in [SENTENCIAS_DIR, UPLOADS_DIR, MODELS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Configuración de archivos permitidos
ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.doc', '.docx'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Importar el analizador de IA (asumiendo que ya está entrenado)
try:
    from backend.analisis import AnalizadorLegal
    ANALIZADOR_IA_DISPONIBLE = True
    logger.info("✅ Módulo de IA cargado correctamente")
except ImportError as e:
    ANALIZADOR_IA_DISPONIBLE = False
    logger.warning(f"⚠️ Módulo de IA no disponible: {e}")
    logger.info("Se usará análisis básico como fallback")


class AnalizadorBasico:
    """Analizador básico como fallback cuando no hay IA disponible"""
    
    def __init__(self):
        self.frases_clave = {
            "incapacidad_permanente_parcial": [
                "incapacidad permanente parcial", "IPP", "permanente parcial",
                "incapacidad parcial permanente", "secuela permanente"
            ],
            "reclamacion_administrativa": [
                "reclamación administrativa previa", "RAP", "reclamación previa",
                "vía administrativa", "recurso administrativo"
            ],
            "inss": [
                "INSS", "Instituto Nacional de la Seguridad Social", "Seguridad Social",
                "Instituto Nacional"
            ],
            "lesiones_permanentes": [
                "lesiones permanentes no incapacitantes", "LPNI", "secuelas",
                "lesiones permanentes", "secuelas permanentes"
            ],
            "personal_limpieza": [
                "limpiadora", "personal de limpieza", "servicios de limpieza",
                "trabajador de limpieza", "empleada de limpieza"
            ],
            "lesiones_hombro": [
                "rotura del manguito rotador", "supraespinoso", "hombro derecho",
                "lesión de hombro", "manguito rotador", "tendón supraespinoso"
            ]
        }
    
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
            insights = self._generar_insights(prediccion, frases_encontradas)
            
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
                "insights_juridicos": insights,
                "archivo_id": Path(ruta_archivo).name,
                "tipo_documento": "sentencia",
                "extract_entities": False,
                "analyze_arguments": False,
                "modelo_ia": False,
                "total_frases_clave": sum(datos["total"] for datos in frases_encontradas.values()),
                "timestamp": datetime.now().isoformat(),
                "ruta_archivo": ruta_archivo
            }
            
        except Exception as e:
            logger.error(f"Error en análisis básico: {e}")
            return self._crear_resultado_error(f"Error en análisis: {str(e)}")
    
    def _leer_archivo(self, ruta: str) -> Optional[str]:
        """Lee el contenido de un archivo con manejo de errores"""
        try:
            if ruta.endswith('.txt'):
                # Intentar diferentes encodings
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        with open(ruta, 'r', encoding=encoding) as f:
                            return f.read().strip()
                    except UnicodeDecodeError:
                        continue
                return None
            else:
                # Para otros formatos, usar función de lectura genérica
                return self._leer_archivo_generico(ruta)
        except Exception as e:
            logger.error(f"Error leyendo archivo {ruta}: {e}")
            return None
    
    def _leer_archivo_generico(self, ruta: str) -> Optional[str]:
        """Lee archivos de diferentes formatos"""
        try:
            # Por ahora solo manejamos texto, pero aquí se podría extender
            # para PDF, DOC, etc. usando librerías como PyPDF2, python-docx
            return "Contenido del archivo no disponible en formato de texto"
        except Exception as e:
            logger.error(f"Error leyendo archivo genérico {ruta}: {e}")
            return None
    
    def _contar_frases_clave(self, texto: str, nombre_archivo: str) -> Dict[str, Any]:
        """Cuenta las ocurrencias de frases clave"""
        if not texto:
            return {}
        
        resultados = {}
        for categoria, variantes in self.frases_clave.items():
            total = 0
            ocurrencias = []
            
            for variante in variantes:
                patron = re.compile(re.escape(variante), re.IGNORECASE)
                matches = patron.finditer(texto)
                
                for match in matches:
                    total += 1
                    start_pos = match.start()
                    end_pos = match.end()
                    
                    # Obtener contexto (100 caracteres antes y después)
                    context_start = max(0, start_pos - 100)
                    context_end = min(len(texto), end_pos + 100)
                    contexto = texto[context_start:context_end]
                    
                    # Marcar la frase encontrada
                    frase_encontrada = texto[start_pos:end_pos]
                    contexto_marcado = contexto.replace(frase_encontrada, f"**{frase_encontrada}**")
                    
                    ocurrencias.append({
                        "frase": variante,
                        "posicion": start_pos,
                        "contexto": contexto_marcado,
                        "linea": texto[:start_pos].count('\n') + 1,
                        "archivo": nombre_archivo
                    })
            
            if total > 0:
                # Obtener frases únicas encontradas
                frases_encontradas = list(set([oc["frase"] for oc in ocurrencias]))
                
                resultados[categoria] = {
                    "total": total,
                    "ocurrencias": ocurrencias,
                    "frases": frases_encontradas
                }
        
        return resultados
    
    def _prediccion_basica(self, texto: str) -> Dict[str, Any]:
        """Predicción básica basada en palabras clave"""
        texto_lower = texto.lower()
        
        palabras_positivas = [
            "estimamos", "estimamos procedente", "procedente", "favorable",
            "accedemos", "concedemos", "reconocemos", "declaramos procedente",
            "estimamos fundada", "fundada", "estimamos parcialmente"
        ]
        
        palabras_negativas = [
            "desestimamos", "desestimamos la reclamación", "desfavorable",
            "no procedente", "rechazamos", "denegamos", "estimamos infundada",
            "infundada", "desestimamos parcialmente"
        ]
        
        positivas = sum(1 for palabra in palabras_positivas if palabra in texto_lower)
        negativas = sum(1 for palabra in palabras_negativas if palabra in texto_lower)
        
        total = positivas + negativas
        if total == 0:
            return {
                "es_favorable": True,
                "confianza": 0.5,
                "interpretacion": "Neutral - No hay indicadores claros"
            }
        
        confianza = min(0.95, max(0.1, (positivas + negativas) / (total + 1)))
        es_favorable = positivas > negativas
        
        if es_favorable:
            interpretacion = f"Favorable - {positivas} indicadores positivos encontrados"
        else:
            interpretacion = f"Desfavorable - {negativas} indicadores negativos encontrados"
        
        return {
            "es_favorable": es_favorable,
            "confianza": confianza,
            "interpretacion": interpretacion
        }
    
    def _extraer_argumentos(self, texto: str) -> List[Dict[str, Any]]:
        """Extrae argumentos legales del texto"""
        argumentos = []
        
        patrones = [
            r"por\s+(?:lo\s+)?que\s+([^.]*?\.)",
            r"fundamentos?\s+(?:de\s+)?(?:derecho|derecho\s+por\s+lo\s+que)\s+([^.]*?\.)",
            r"considerando\s+que\s+([^.]*?\.)",
            r"vistos\s+([^.]*?\.)",
            r"resultando\s+([^.]*?\.)"
        ]
        
        for patron in patrones:
            matches = re.finditer(patron, texto, re.IGNORECASE)
            for match in matches:
                argumento = match.group(1).strip()
                if len(argumento) > 20:
                    argumentos.append({
                        "tipo": "argumento_legal",
                        "texto": argumento,
                        "posicion": match.start(),
                        "confianza": 0.7,
                        "categoria": "fundamento_juridico"
                    })
        
        return argumentos
    
    def _generar_insights(self, prediccion: Dict, frases_clave: Dict) -> List[str]:
        """Genera insights jurídicos básicos"""
        insights = []
        
        if prediccion["es_favorable"]:
            insights.append("El documento presenta argumentos sólidos a favor del caso.")
            insights.append("La resolución favorece al reclamante.")
        else:
            insights.append("El documento presenta argumentos que pueden ser desfavorables.")
            insights.append("La resolución no favorece al reclamante.")
        
        if frases_clave:
            categorias = list(frases_clave.keys())
            insights.append(f"Se identificaron {len(categorias)} categorías de frases clave.")
            insights.append(f"Las categorías más relevantes son: {', '.join(categorias[:3])}.")
        
        insights.append(f"Confianza del análisis: {prediccion['confianza']:.1%}")
        
        return insights
    
    def _generar_resumen(self, prediccion: Dict, frases_clave: Dict) -> str:
        """Genera un resumen inteligente del análisis"""
        if prediccion["es_favorable"]:
            base = "Análisis favorable del documento legal. "
        else:
            base = "Análisis desfavorable del documento legal. "
        
        if frases_clave:
            total_frases = sum(datos["total"] for datos in frases_clave.values())
            base += f"Se identificaron {total_frases} frases clave relevantes. "
        
        base += f"Confianza del análisis: {prediccion['confianza']:.1%}."
        
        return base
    
    def _crear_resultado_error(self, mensaje: str) -> Dict[str, Any]:
        """Crea un resultado de error estandarizado"""
        return {
            "error": mensaje,
            "procesado": False,
            "nombre_archivo": "archivo_desconocido",
            "prediccion": {"es_favorable": False, "confianza": 0.0},
            "frases_clave": {},
            "argumentos": [],
            "insights_juridicos": [f"Error: {mensaje}"],
            "longitud_texto": 0,
            "total_frases_clave": 0
        }


# Instanciar analizador básico
analizador_basico = AnalizadorBasico()


def validar_archivo(archivo: UploadFile) -> Dict[str, Any]:
    """Valida un archivo subido"""
    errores = []
    
    # Validar nombre
    if not archivo.filename:
        errores.append("No se seleccionó ningún archivo")
    
    # Validar extensión
    if archivo.filename:
        extension = Path(archivo.filename).suffix.lower()
        if extension not in ALLOWED_EXTENSIONS:
            errores.append(f"Extensión no permitida: {extension}. Permitidas: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Validar tamaño
    if archivo.size and archivo.size > MAX_FILE_SIZE:
        errores.append(f"Archivo demasiado grande: {archivo.size / (1024*1024):.1f}MB. Máximo: {MAX_FILE_SIZE / (1024*1024)}MB")
    
    return {
        "valido": len(errores) == 0,
        "errores": errores
    }


@app.get("/", response_class=HTMLResponse)
async def pagina_principal(request: Request):
    """Página principal de la aplicación"""
    try:
        # Analizar sentencias existentes
        resultado = analizar_sentencias_existentes()
        
        # DEBUG: Log del resultado
        logger.info(f"Resultado de analizar_sentencias_existentes: {resultado}")
        logger.info(f"ranking_global keys: {list(resultado.get('ranking_global', {}).keys())}")
        logger.info(f"ranking_global length: {len(resultado.get('ranking_global', {}))}")
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "archivos_analizados": resultado.get("archivos_analizados", 0),
            "total_apariciones": resultado.get("total_apariciones", 0),
            "resultados_por_archivo": resultado.get("resultados_por_archivo", {}),
            "ranking_global": resultado.get("ranking_global", {}),
            "ia_disponible": ANALIZADOR_IA_DISPONIBLE
        })
    except Exception as e:
        logger.error(f"Error en página principal: {e}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Error al cargar la página: {str(e)}",
            "ia_disponible": ANALIZADOR_IA_DISPONIBLE
        })


@app.get("/subir", response_class=HTMLResponse)
async def formulario_subida(request: Request):
    """Formulario para subir documentos"""
    return templates.TemplateResponse("subir.html", {
        "request": request,
        "ia_disponible": ANALIZADOR_IA_DISPONIBLE
    })


@app.post("/upload")
async def subir_documento(
    file: UploadFile = File(...),
    document_type: str = Form("sentencia"),
    extract_entities: bool = Form(True),
    analyze_arguments: bool = Form(True)
):
    """Procesa la subida de un documento"""
    try:
        # Validar archivo
        validacion = validar_archivo(file)
        if not validacion["valido"]:
            raise HTTPException(status_code=400, detail="; ".join(validacion["errores"]))
        
        # Generar nombre único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        extension = Path(file.filename).suffix
        nuevo_nombre = f"{document_type}_{timestamp}_{unique_id}{extension}"
        
        # Guardar archivo
        ruta_archivo = UPLOADS_DIR / nuevo_nombre
        with open(ruta_archivo, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Archivo subido: {nuevo_nombre}")
        
        # Analizar documento
        if ANALIZADOR_IA_DISPONIBLE:
            try:
                analizador = AnalizadorLegal()
                resultado = analizador.analizar_documento(str(ruta_archivo))
                resultado["modelo_ia"] = True
                logger.info("Análisis con IA completado")
            except Exception as e:
                logger.warning(f"Fallback a análisis básico: {e}")
                resultado = analizador_basico.analizar_documento(str(ruta_archivo), file.filename)
                resultado["modelo_ia"] = False
        else:
            resultado = analizador_basico.analizar_documento(str(ruta_archivo), file.filename)
            resultado["modelo_ia"] = False
        
        # Agregar metadatos
        resultado.update({
            "nombre_archivo": file.filename,
            "archivo_id": nuevo_nombre,
            "tipo_documento": document_type,
            "extract_entities": extract_entities,
            "analyze_arguments": analyze_arguments,
            "timestamp": timestamp,
            "ruta_archivo": str(ruta_archivo)
        })
        
        # Mover a carpeta de sentencias si es apropiado
        if document_type == "sentencia":
            destino = SENTENCIAS_DIR / nuevo_nombre
            shutil.move(str(ruta_archivo), str(destino))
            resultado["ruta_archivo"] = str(destino)
        
        return JSONResponse(content=resultado)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error procesando archivo: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.get("/resultado/{archivo_id}", response_class=HTMLResponse)
async def mostrar_resultados(request: Request, archivo_id: str):
    """Muestra los resultados del análisis"""
    try:
        # Buscar archivo
        ruta_archivo = UPLOADS_DIR / archivo_id
        if not ruta_archivo.exists():
            ruta_archivo = SENTENCIAS_DIR / archivo_id
        
        if not ruta_archivo.exists():
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        
        # Analizar si es necesario
        if archivo_id.startswith(("sentencia_", "demanda_", "informe_")):
            if ANALIZADOR_IA_DISPONIBLE:
                try:
                    analizador = AnalizadorLegal()
                    resultado = analizador.analizar_documento(str(ruta_archivo))
                    resultado["modelo_ia"] = True
                except Exception as e:
                    logger.warning(f"Fallback a análisis básico: {e}")
                    resultado = analizador_basico.analizar_documento(str(ruta_archivo), archivo_id)
                    resultado["modelo_ia"] = False
            else:
                resultado = analizador_basico.analizar_documento(str(ruta_archivo), archivo_id)
                resultado["modelo_ia"] = False
        else:
            # Usar análisis existente
            resultado = {
                "nombre_archivo": archivo_id,
                "procesado": True,
                "prediccion": {"es_favorable": True, "confianza": 0.8},
                "resumen_inteligente": "Análisis del documento existente.",
                "argumentos": [],
                "frases_clave": {},
                "insights_juridicos": ["Documento analizado previamente."],
                "longitud_texto": 0,
                "total_frases_clave": 0,
                "modelo_ia": False
            }
        
        return templates.TemplateResponse("resultado.html", {
            "request": request,
            "resultado": resultado
        })
        
    except Exception as e:
        logger.error(f"Error mostrando resultados: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/archivo/{archivo_id}", response_class=HTMLResponse)
async def ver_archivo(request: Request, archivo_id: str, highlight: str = None, pos: int = None, index: int = None):
    """Muestra el contenido completo de un archivo con frases clave resaltadas y opcionalmente resalta una aparición específica"""
    try:
        # Buscar el archivo en la carpeta de sentencias
        archivo_path = SENTENCIAS_DIR / archivo_id
        
        if not archivo_path.exists():
            raise HTTPException(status_code=404, detail=f"Archivo '{archivo_id}' no encontrado")
        
        # Analizar el archivo para obtener frases clave
        if ANALIZADOR_IA_DISPONIBLE:
            try:
                analizador = AnalizadorLegal()
                resultado = analizador.analizar_documento(str(archivo_path))
            except Exception as e:
                logger.warning(f"Fallback a análisis básico: {e}")
                resultado = analizador_basico.analizar_documento(str(archivo_path), archivo_id)
        else:
            resultado = analizador_basico.analizar_documento(str(archivo_path), archivo_id)
        
        if not resultado.get("procesado"):
            raise HTTPException(status_code=500, detail="No se pudo procesar el archivo")
        
        # Preparar datos para el template
        datos_archivo = {
            "nombre": archivo_id,
            "contenido": resultado.get("texto_extraido", ""),
            "longitud": resultado.get("longitud_texto", 0),
            "frases_clave": resultado.get("frases_clave", {}),
            "prediccion": resultado.get("prediccion", {}),
            "argumentos": resultado.get("argumentos", []),
            "insights": resultado.get("insights_juridicos", []),
            "total_frases": resultado.get("total_frases_clave", 0),
            "highlight_info": {
                "frase": highlight,
                "posicion": pos,
                "index": index
            } if highlight else None
        }
        
        return templates.TemplateResponse("archivo.html", {
            "request": request,
            "archivo": datos_archivo
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error mostrando archivo {archivo_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.get("/api/analizar")
async def api_analizar():
    """Endpoint API para análisis"""
    try:
        return analizar_sentencias_existentes()
    except Exception as e:
        logger.error(f"Error en API: {e}")
        return {"error": f"Error al analizar: {str(e)}"}


@app.get("/api/analisis-predictivo")
async def api_analisis_predictivo():
    """Endpoint API para análisis predictivo e inteligente de resoluciones"""
    try:
        # Importar funciones del módulo de análisis predictivo
        from backend.analisis_predictivo import (
            realizar_analisis_predictivo,
            generar_insights_juridicos,
            identificar_patrones_favorables,
            extraer_factores_clave,
            generar_recomendaciones,
            calcular_confianza_analisis
        )
        
        # Obtener datos base
        resultado_base = analizar_sentencias_existentes()
        
        # Realizar análisis predictivo avanzado
        analisis_predictivo = realizar_analisis_predictivo(resultado_base)
        
        # Generar insights y recomendaciones
        insights = generar_insights_juridicos(resultado_base, analisis_predictivo)
        
        # Crear respuesta estructurada para UX mejorada
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "resumen_ejecutivo": {
                "total_documentos": resultado_base.get("archivos_analizados", 0),
                "total_frases_clave": resultado_base.get("total_apariciones", 0),
                "categorias_identificadas": len(resultado_base.get("ranking_global", {})),
                "confianza_analisis": calcular_confianza_analisis(resultado_base)
            },
            "analisis_predictivo": analisis_predictivo,
            "insights_juridicos": insights,
            "patrones_favorables": identificar_patrones_favorables(resultado_base),
            "factores_clave": extraer_factores_clave(resultado_base),
            "recomendaciones": generar_recomendaciones(resultado_base, analisis_predictivo),
            "datos_estadisticos": resultado_base,
            "metadata": {
                "modelo_ia": ANALIZADOR_IA_DISPONIBLE,
                "version_analisis": "2.0.0",
                "fecha_ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        
    except Exception as e:
        logger.error(f"Error en análisis predictivo: {e}")
        return {
            "status": "error",
            "error": f"Error en análisis predictivo: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


@app.get("/analisis-predictivo")
async def pagina_analisis_predictivo():
    """Página web para el análisis predictivo"""
    return templates.TemplateResponse("analisis_predictivo.html", {"request": {}})


@app.get("/health")
async def health_check():
    """Endpoint de salud del sistema"""
    return {
        "status": "ok",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "ia_disponible": ANALIZADOR_IA_DISPONIBLE,
        "directorios": {
            "sentencias": str(SENTENCIAS_DIR),
            "uploads": str(UPLOADS_DIR),
            "models": str(MODELS_DIR)
        }
    }


@app.get("/api/documento/{nombre_archivo}")
async def obtener_documento(nombre_archivo: str):
    """Obtiene detalles de un documento específico"""
    try:
        # Decodificar el nombre del archivo
        nombre_decodificado = nombre_archivo
        
        # Buscar el archivo en el directorio de sentencias
        archivo_path = SENTENCIAS_DIR / nombre_decodificado
        
        if not archivo_path.exists():
            raise HTTPException(status_code=404, detail=f"Documento '{nombre_decodificado}' no encontrado")
        
        # Obtener información del archivo
        stat = archivo_path.stat()
        tamaño = f"{stat.st_size / 1024:.1f} KB"
        fecha_modificacion = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        
        # Intentar analizar el documento si no ha sido analizado
        try:
            if ANALIZADOR_IA_DISPONIBLE:
                from backend.analisis import AnalizadorLegal
                analizador = AnalizadorLegal()
                resultado = analizador.analizar_documento(str(archivo_path))
            else:
                resultado = analizador_basico.analizar_documento(str(archivo_path), nombre_decodificado)
            
            if resultado.get("procesado"):
                return {
                    "nombre": nombre_decodificado,
                    "procesado": True,
                    "tamaño": tamaño,
                    "fecha_procesamiento": fecha_modificacion,
                    "frases_clave": resultado.get("frases_clave", {}),
                    "total_frases": sum(info["total"] for info in resultado.get("frases_clave", {}).values()),
                    "resumen": resultado.get("resumen", ""),
                    "tipo_documento": resultado.get("tipo_documento", "desconocido")
                }
            else:
                return {
                    "nombre": nombre_decodificado,
                    "procesado": False,
                    "tamaño": tamaño,
                    "fecha_procesamiento": fecha_modificacion,
                    "error": resultado.get("error", "Error desconocido en el procesamiento"),
                    "frases_clave": {},
                    "total_frases": 0
                }
                
        except Exception as e:
            logger.error(f"Error analizando documento {nombre_decodificado}: {e}")
            return {
                "nombre": nombre_decodificado,
                "procesado": False,
                "tamaño": tamaño,
                "fecha_procesamiento": fecha_modificacion,
                "error": f"Error en el análisis: {str(e)}",
                "frases_clave": {},
                "total_frases": 0
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo documento {nombre_archivo}: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


def analizar_sentencias_existentes() -> Dict[str, Any]:
    """Analiza las sentencias existentes en la carpeta"""
    try:
        logger.info(f"🔍 Iniciando análisis de sentencias existentes en: {SENTENCIAS_DIR}")
        
        if not SENTENCIAS_DIR.exists():
            logger.warning(f"❌ La carpeta '{SENTENCIAS_DIR}' no existe")
            return {
                "error": f"La carpeta '{SENTENCIAS_DIR}' no existe",
                "archivos_analizados": 0,
                "total_apariciones": 0,
                "resultados_por_archivo": {},
                "ranking_global": {}
            }
        
        # Buscar archivos de texto y PDF
        archivos_soportados = [f for f in SENTENCIAS_DIR.iterdir() 
                              if f.suffix.lower() in ['.txt', '.pdf']]
        
        logger.info(f"📁 Archivos encontrados: {[f.name for f in archivos_soportados]}")
        
        if not archivos_soportados:
            logger.warning(f"❌ No se encontraron archivos .txt o .pdf en '{SENTENCIAS_DIR}'")
            return {
                "error": f"No se encontraron archivos .txt o .pdf en '{SENTENCIAS_DIR}'",
                "archivos_analizados": 0,
                "total_apariciones": 0,
                "resultados_por_archivo": {},
                "ranking_global": {}
            }
        
        resultados_por_archivo = {}
        ranking_global = {}
        total_apariciones = 0
        
        for archivo in archivos_soportados:
            try:
                logger.info(f"🔍 Analizando archivo: {archivo.name}")
                
                # Usar el analizador de IA si está disponible, sino el básico
                if ANALIZADOR_IA_DISPONIBLE:
                    logger.info(f"🤖 Usando analizador de IA para: {archivo.name}")
                    from backend.analisis import AnalizadorLegal
                    analizador = AnalizadorLegal()
                    resultado = analizador.analizar_documento(str(archivo))
                else:
                    logger.info(f"🔧 Usando analizador básico para: {archivo.name}")
                    resultado = analizador_basico.analizar_documento(str(archivo), archivo.name)
                
                logger.info(f"📊 Resultado para {archivo.name}: procesado={resultado.get('procesado')}")
                
                if resultado.get("procesado"):
                    resultados_por_archivo[archivo.name] = resultado
                    
                    # Procesar frases clave encontradas
                    frases_clave = resultado.get("frases_clave", {})
                    logger.info(f"🔑 Frases clave encontradas en {archivo.name}: {list(frases_clave.keys())}")
                    
                    for categoria, datos in frases_clave.items():
                        if categoria in ranking_global:
                            ranking_global[categoria]["total"] += datos["total"]
                            ranking_global[categoria]["ocurrencias"].extend(datos["ocurrencias"])
                            logger.info(f"📈 Actualizando {categoria}: total={ranking_global[categoria]['total']}")
                        else:
                            ranking_global[categoria] = {
                                "total": datos["total"],
                                "ocurrencias": datos["ocurrencias"]
                            }
                            logger.info(f"🆕 Nueva categoría {categoria}: total={datos['total']}")
                        total_apariciones += datos["total"]
                else:
                    logger.warning(f"⚠️ Archivo {archivo.name} no se pudo procesar")
                    resultados_por_archivo[archivo.name] = {"error": "No se pudo procesar"}
                    
            except Exception as e:
                logger.error(f"❌ Error analizando {archivo}: {e}")
                resultados_por_archivo[archivo.name] = {"error": f"Error: {str(e)}"}
        
        # Ordenar ranking
        ranking_ordenado = dict(sorted(ranking_global.items(), key=lambda x: x[1]["total"], reverse=True))
        
        logger.info(f"📊 RESUMEN FINAL:")
        logger.info(f"  - Archivos analizados: {len(archivos_soportados)}")
        logger.info(f"  - Total apariciones: {total_apariciones}")
        logger.info(f"  - Categorías encontradas: {list(ranking_ordenado.keys())}")
        logger.info(f"  - Ranking global: {ranking_ordenado}")
        
        return {
            "archivos_analizados": len(archivos_soportados),
            "total_apariciones": total_apariciones,
            "resultados_por_archivo": resultados_por_archivo,
            "ranking_global": ranking_ordenado
        }
        
    except Exception as e:
        logger.error(f"❌ Error analizando sentencias: {e}")
        return {
            "error": f"Error al analizar sentencias: {str(e)}",
            "archivos_analizados": 0,
            "total_apariciones": 0,
            "resultados_por_archivo": {},
            "ranking_global": {}
        }


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Iniciando Analizador de Sentencias IPP/INSS...")
    print(f"📁 Directorio de sentencias: {SENTENCIAS_DIR}")
    print(f"🤖 IA disponible: {'✅ Sí' if ANALIZADOR_IA_DISPONIBLE else '❌ No'}")
    print(f"🌐 URL: http://localhost:8000")
    print(f"📚 Documentación: http://localhost:8000/docs")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )
