#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de Sentencias IPP/INSS - Aplicación FastAPI
Aplicación robusta para análisis de documentos legales con modelo de IA pre-entrenado
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

from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Importar módulo de seguridad
from .security import validate_and_save_file, FileSecurityError

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
FRASES_FILE = BASE_DIR / "models" / "frases_clave.json"
frases_lock = Lock()

# Crear directorios necesarios
for directory in [SENTENCIAS_DIR, UPLOADS_DIR, MODELS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Configuración de archivos permitidos
ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.doc', '.docx'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Frases por defecto en caso de que no exista el archivo o sea inválido
DEFAULT_FRASES_CLAVE: Dict[str, List[str]] = {
    "procedimiento_legal": ["procedente", "desestimamos", "estimamos"],
}


def load_frases_clave() -> Dict[str, List[str]]:
    """Carga el JSON de frases clave de disco con validación básica."""
    try:
        if not FRASES_FILE.exists():
            logger.warning(f"Archivo de frases no encontrado en {FRASES_FILE}")
            return DEFAULT_FRASES_CLAVE
        with open(FRASES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            logger.warning("Formato inválido en frases_clave.json (no es dict)")
            return DEFAULT_FRASES_CLAVE
        # Normalizar valores a listas de strings únicas
        normalizado: Dict[str, List[str]] = {}
        for categoria, frases in data.items():
            if not isinstance(categoria, str):
                continue
            if isinstance(frases, list):
                solo_texto = [str(x).strip() for x in frases if str(x).strip()]
                # quitar duplicados preservando orden
                seen = set()
                unicos: List[str] = []
                for s in solo_texto:
                    if s.lower() not in seen:
                        seen.add(s.lower())
                        unicos.append(s)
                # Incluir también categorías vacías (permitimos crear primero y rellenar después)
                normalizado[categoria] = unicos
        return normalizado or DEFAULT_FRASES_CLAVE
    except Exception as e:
        logger.error(f"Error cargando frases_clave.json: {e}")
        return DEFAULT_FRASES_CLAVE


def save_frases_clave(data: Dict[str, List[str]]) -> None:
    """Guarda el JSON de frases clave de forma atómica y segura."""
    if not isinstance(data, dict):
        raise ValueError("El payload debe ser un objeto {categoria: [frases]}")
    for categoria, frases in data.items():
        if not isinstance(categoria, str) or not isinstance(frases, list):
            raise ValueError("Formato inválido: claves str, valores lista de str")
    MODELS_DIR.mkdir(exist_ok=True)
    temp_path = FRASES_FILE.with_suffix(".tmp")
    with frases_lock:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(temp_path, FRASES_FILE)

# Importar el analizador de IA (asumiendo que ya está entrenado)
try:
    from .backend.analisis import AnalizadorLegal
    ANALIZADOR_IA_DISPONIBLE = True
    logger.info("✅ Módulo de IA cargado correctamente")
except ImportError as e:
    ANALIZADOR_IA_DISPONIBLE = False
    logger.warning(f"⚠️ Módulo de IA no disponible: {e}")
    logger.info("Se usará análisis básico como fallback")


class AnalizadorBasico:
    """Analizador básico como fallback cuando no hay IA disponible"""
    
    def __init__(self):
        self.frases_clave = {}
        self.cargar_frases_desde_modelo()

    def cargar_frases_desde_modelo(self) -> None:
        """Carga frases clave desde models/frases_clave.json o usa un conjunto por defecto."""
        try:
            datos = load_frases_clave()
            if isinstance(datos, dict) and datos:
                self.frases_clave = datos
            else:
                self.frases_clave = DEFAULT_FRASES_CLAVE
                logger.warning("Usando frases por defecto; archivo vacío o inválido")
        except Exception as e:
            logger.warning(f"No se pudo cargar frases_clave.json: {e}. Usando valores por defecto")
            self.frases_clave = DEFAULT_FRASES_CLAVE
    
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
            
            # Calcular tiempo de procesamiento
            tiempo_inicio = getattr(self, '_tiempo_inicio', None)
            tiempo_procesamiento = None
            if tiempo_inicio:
                tiempo_procesamiento = f"{(datetime.now() - tiempo_inicio).total_seconds():.2f}s"
            
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
                "tiempo_procesamiento": tiempo_procesamiento or "N/A",
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
                # Permitir espacios/guiones/underscores intercambiables entre palabras
                flexible = re.escape(variante)
                flexible = flexible.replace("\\ ", "\\s+")
                flexible = flexible.replace("\\_", "[\\s_\-]+")
                flexible = flexible.replace("\\-", "[\\s_\-]+")
                patron = re.compile(flexible, re.IGNORECASE)
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


# ====== MODELOS Pydantic para CRUD ======
class FrasesPayload(BaseModel):
    categorias: Dict[str, List[str]]

class CategoriaPayload(BaseModel):
    nombre: str
    frases: List[str] = []

class FrasePayload(BaseModel):
    categoria: str
    frase: str

class RenameCategoryPayload(BaseModel):
    old_name: str
    new_name: str

class UpdatePhrasePayload(BaseModel):
    categoria: str
    old_frase: str
    new_frase: str


class DeleteDocumentPayload(BaseModel):
    nombre_archivo: str


# ====== ENDPOINTS CRUD DE FRASES CLAVE ======
@app.get("/api/frases")
async def listar_frases():
    """Lista todas las categorías y frases clave actuales."""
    datos = load_frases_clave()
    return {"categorias": datos}


@app.post("/api/frases")
async def reemplazar_frases(payload: FrasesPayload):
    """Reemplaza completamente el set de frases clave."""
    save_frases_clave(payload.categorias)
    analizador_basico.cargar_frases_desde_modelo()
    return {"status": "ok"}


@app.post("/api/frases/categoria")
async def crear_categoria(payload: CategoriaPayload):
    datos = load_frases_clave()
    nombre = payload.nombre.strip()
    if not nombre:
        raise HTTPException(status_code=400, detail="Nombre de categoría requerido")
    if nombre in datos:
        raise HTTPException(status_code=409, detail="La categoría ya existe")
    datos[nombre] = [s.strip() for s in payload.frases if s and s.strip()]
    save_frases_clave(datos)
    analizador_basico.cargar_frases_desde_modelo()
    return {"status": "ok", "categoria": nombre}


@app.delete("/api/frases/categoria/{nombre}")
async def eliminar_categoria(nombre: str):
    datos = load_frases_clave()
    if nombre not in datos:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    datos.pop(nombre)
    save_frases_clave(datos)
    analizador_basico.cargar_frases_desde_modelo()
    return {"status": "ok"}


@app.patch("/api/frases/categoria")
async def renombrar_categoria(payload: RenameCategoryPayload):
    datos = load_frases_clave()
    old_name = payload.old_name.strip()
    new_name = payload.new_name.strip()
    if not old_name or not new_name:
        raise HTTPException(status_code=400, detail="Nombres requeridos")
    if old_name not in datos:
        raise HTTPException(status_code=404, detail="Categoría original no encontrada")
    if new_name in datos and new_name != old_name:
        raise HTTPException(status_code=409, detail="La categoría destino ya existe")
    if new_name == old_name:
        return {"status": "ok", "categoria": new_name}
    datos[new_name] = datos.pop(old_name)
    save_frases_clave(datos)
    analizador_basico.cargar_frases_desde_modelo()
    return {"status": "ok", "categoria": new_name}


@app.post("/api/frases/frase")
async def agregar_frase(payload: FrasePayload):
    datos = load_frases_clave()
    categoria = payload.categoria
    frase = payload.frase.strip()
    if not frase:
        raise HTTPException(status_code=400, detail="Frase requerida")
    if categoria not in datos:
        datos[categoria] = []
    # evitar duplicados case-insensitive
    if frase.lower() not in [f.lower() for f in datos[categoria]]:
        datos[categoria].append(frase)
    save_frases_clave(datos)
    analizador_basico.cargar_frases_desde_modelo()
    return {"status": "ok"}


@app.delete("/api/frases/frase")
async def eliminar_frase(payload: FrasePayload):
    datos = load_frases_clave()
    categoria = payload.categoria
    frase = payload.frase.strip()
    if categoria not in datos:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    datos[categoria] = [f for f in datos[categoria] if f.lower() != frase.lower()]
    save_frases_clave(datos)
    analizador_basico.cargar_frases_desde_modelo()
    return {"status": "ok"}


@app.patch("/api/frases/frase")
async def actualizar_frase(payload: UpdatePhrasePayload):
    datos = load_frases_clave()
    categoria = payload.categoria
    old_frase = payload.old_frase.strip()
    new_frase = payload.new_frase.strip()
    if not new_frase:
        raise HTTPException(status_code=400, detail="Nueva frase requerida")
    if categoria not in datos:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    frases = datos[categoria]
    indices = [i for i, f in enumerate(frases) if f.lower() == old_frase.lower()]
    if not indices:
        raise HTTPException(status_code=404, detail="Frase original no encontrada")
    # Evitar duplicado de destino
    if any(f.lower() == new_frase.lower() for f in frases):
        # si ya existe exacta, eliminar la vieja
        frases = [f for f in frases if f.lower() != old_frase.lower()]
    else:
        # reemplazar el primero y eliminar duplicados del resto
        idx = indices[0]
        frases[idx] = new_frase
        # limpiar duplicados case-insensitive preservando orden
        seen = set()
        dedup: List[str] = []
        for f in frases:
            key = f.lower()
            if key not in seen:
                seen.add(key)
                dedup.append(f)
        frases = dedup
    datos[categoria] = frases
    save_frases_clave(datos)
    analizador_basico.cargar_frases_desde_modelo()
    return {"status": "ok"}


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
    """Procesa la subida de un documento con validación de seguridad"""
    try:
        # Validar y guardar archivo de forma segura
        try:
            secure_filename, secure_path = validate_and_save_file(file)
            logger.info(f"Archivo validado y guardado de forma segura: {secure_filename}")
        except FileSecurityError as e:
            logger.warning(f"Error de seguridad en upload: {e}")
            raise HTTPException(status_code=400, detail=f"Error de seguridad: {str(e)}")
        
        # Usar el archivo guardado de forma segura
        ruta_archivo = Path(secure_path)
        
        logger.info(f"Archivo subido de forma segura: {secure_filename}")
        
        # Analizar documento
        if ANALIZADOR_IA_DISPONIBLE:
            try:
                analizador = AnalizadorLegal()
                resultado = analizador.analizar_documento(str(ruta_archivo))
                resultado["modelo_ia"] = True
                logger.info("Análisis con IA completado")
            except Exception as e:
                logger.warning(f"Fallback a análisis básico: {e}")
                resultado = analizador_basico.analizar_documento(str(ruta_archivo), secure_filename)
                resultado["modelo_ia"] = False
        else:
            resultado = analizador_basico.analizar_documento(str(ruta_archivo), secure_filename)
            resultado["modelo_ia"] = False
        
        # Agregar metadatos
        resultado.update({
            "nombre_archivo": file.filename,  # Nombre original
            "archivo_id": secure_filename,    # Nombre seguro
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
        from .backend.analisis_predictivo import (
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
async def pagina_analisis_predictivo(request: Request):
    """Página web para el análisis predictivo"""
    return templates.TemplateResponse("analisis_predictivo.html", {"request": request})


# ====== DEMANDA BASE: generación desde fallos y fundamentos ======
def _leer_texto_archivo_simple(path: Path) -> str:
    try:
        if path.suffix.lower() == '.txt':
            for enc in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    return path.read_text(encoding=enc)
                except UnicodeDecodeError:
                    continue
            return path.read_text(errors='ignore')
        else:
            # Delegar a analizador para extraer texto
            if ANALIZADOR_IA_DISPONIBLE:
                from .backend.analisis import AnalizadorLegal
                analizador = AnalizadorLegal()
                res = analizador.analizar_documento(str(path))
            else:
                res = analizador_basico.analizar_documento(str(path), path.name)
            return res.get('texto_extraido', '') or ''
    except Exception:
        return ''


def _extraer_seccion(texto: str, encabezados: List[str], fin_encabezados: List[str]) -> str:
    if not texto:
        return ''
    t = texto
    import re as _re
    # Construir regex de inicio y fin
    ini = r"|".join([_re.escape(h) for h in encabezados])
    fin = r"|".join([_re.escape(h) for h in fin_encabezados])
    patron_ini = _re.compile(rf"(?i)(?:^|\n)\s*(?:{ini})\b[:\-\s]*", _re.MULTILINE)
    patron_fin = _re.compile(rf"(?i)(?:^|\n)\s*(?:{fin})\b", _re.MULTILINE)
    m = patron_ini.search(t)
    if not m:
        return ''
    start = m.end()
    m2 = patron_fin.search(t, start)
    end = m2.start() if m2 else len(t)
    seccion = t[start:end].strip()
    # Limpiar artefactos HTML simples
    seccion = _re.sub(r"<[^>]+>", " ", seccion)
    seccion = _re.sub(r"\s+", " ", seccion).strip()
    return seccion


def _generar_demanda_base_para(paths: List[Path], meta: Dict[str, Any] = None) -> Dict[str, Any]:
    documentos: List[Dict[str, Any]] = []
    for p in paths:
        texto = _leer_texto_archivo_simple(p)
        fallo = _extraer_seccion(
            texto,
            encabezados=["FALLO", "PARTE DISPOSITIVA", "RESUELVO", "RESOLVEMOS"],
            fin_encabezados=["FUNDAMENTOS", "FUNDAMENTOS DE HECHO", "HECHOS", "FUNDAMENTOS DE DERECHO", "ANTECEDENTES", "SEGUNDO", "TERCERO"]
        )
        fundamentos = _extraer_seccion(
            texto,
            encabezados=["FUNDAMENTOS DE HECHO", "HECHOS PROBADOS", "ANTECEDENTES DE HECHO"],
            fin_encabezados=["FUNDAMENTOS DE DERECHO", "PARTE DISPOSITIVA", "FALLO", "RESUELVO", "RESOLVEMOS"]
        )
        # Resumenes breves
        fundamentos_resumen = _resumir_fundamentos(texto)
        fallo_breve = (fallo or "").strip()
        if len(fallo_breve) > 400:
            fallo_breve = fallo_breve[:400].rstrip() + "…"
        documentos.append({
            "nombre": p.name,
            "fallo": fallo,
            "fundamentos": fundamentos,
            "fallo_breve": fallo_breve,
            "fundamentos_resumen": fundamentos_resumen
        })

    meta = meta or {}
    nombre = meta.get("nombre", "[NOMBRE DEMANDANTE]")
    dni = meta.get("dni", "[DNI]")
    domicilio = meta.get("domicilio", "[DOMICILIO A EFECTOS]")
    letrado = meta.get("letrado", "[LETRADO/A]")
    empresa = meta.get("empresa", "[EMPRESA]")
    profesion = meta.get("profesion", "[PROFESIÓN HABITUAL]")
    grado_principal = meta.get("grado_principal", "Incapacidad Permanente Total")
    grado_subsidiario = meta.get("grado_subsidiario", "Incapacidad Permanente Parcial")
    base_reguladora = meta.get("base_reguladora", "[BASE REGULADORA]")
    indemnizacion_parcial = meta.get("indemnizacion_parcial", "24 mensualidades")
    mutua = meta.get("mutua", "[MUTUA]")

    # Plantilla base de demanda (formal)
    cuerpo = {
        "encabezado": "AL JUZGADO DE LO SOCIAL QUE POR TURNO CORRESPONDA\n\n",
        "parte": (
            f"D./Dña. {nombre}, con DNI {dni}, y domicilio a efectos de notificaciones en {domicilio}, "
            f"representado/a por Letrado/a {letrado}, ante el Juzgado comparece y DICE:\n\n"
        ),
        "hechos": None,  # se compone más abajo
        "fundamentos_derecho": (
            "FUNDAMENTOS DE DERECHO\n"
            "I. Jurisdicción y competencia (arts. 2 y 6 LRJS).\n"
            "II. Legitimación activa y pasiva (LRJS).\n"
            "III. Fondo del asunto. Arts. 193 y 194 LGSS (grados de incapacidad). Art. 194.2 LGSS (IPP = 24 mensualidades).\n"
            "IV. Doctrina jurisprudencial aplicable (STS 04-07-2025, rec. 1096/2024, sobre IPP subsidiaria; TSJ Castilla y León sobre limitaciones en limpiadoras).\n"
            "V. Principios y derechos constitucionales (art. 24 CE tutela judicial efectiva; 9.3 CE interdicción de la arbitrariedad).\n\n"
        ),
        "peticion": (
            "SUPLICO AL JUZGADO:\n"
            f"Primero.- Que, estimando la demanda, se declare a la actora afecta a {grado_principal} para su profesión habitual de {profesion}, derivada de [contingencia], con derecho a la prestación correspondiente sobre una base reguladora de {base_reguladora}.\n"
            f"Subsidiariamente.- Que, para el caso de no apreciarse lo anterior, se declare la {grado_subsidiario}, con derecho a la indemnización de {indemnizacion_parcial} de la base reguladora, a cargo de la Mutua {mutua} en caso de accidente de trabajo.\n"
            "Con expresa condena en costas a la parte demandada en los términos legalmente procedentes.\n\n"
        ),
    }

    # HECHOS (limpios y propios)
    cuerpo["hechos"] = (
        "HECHOS\n"
        f"1. Relación laboral. La demandante presta servicios como {profesion} para la empresa {empresa}.\n"
        "2. Contingencia y evolución. [Accidente de trabajo / enfermedad común], con periodos de IT y secuelas actuales.\n"
        "3. Actuaciones administrativas. (EVI, inicio IP, audiencia, resolución del INSS y Reclamación Previa).\n"
        "4. Cuadro clínico y limitaciones. [Describir secuelas relevantes y su impacto en las tareas fundamentales].\n\n"
    )

    # Resumen de fallos extraídos
    resumen_fallos = []
    for d in documentos:
        if d["fallo"]:
            resumen_fallos.append(f"— {d['nombre']}: {d['fallo']}")

    anexos = []
    for i, d in enumerate(documentos, start=1):
        if d["fallo"]:
            anexos.append(f"Documento nº {i}: Parte dispositiva de {d['nombre']}")

    # Jurisprudencia de apoyo (extractada)
    juris = []
    for d in documentos:
        linea = f"— {d['nombre']}: {d.get('fallo_breve','').strip()}"
        if d.get("fundamentos_resumen"):
            linea += "\n   Fundamentos: " + "; ".join(d["fundamentos_resumen"][:2])
        juris.append(linea.strip())

    doc_txt = (
        cuerpo["encabezado"] +
        cuerpo["parte"] +
        ("JURISPRUDENCIA DE APOYO (extracto de fallos)\n" + "\n\n".join(juris) + "\n\n" if juris else "") +
        cuerpo["hechos"] +
        cuerpo["fundamentos_derecho"] +
        cuerpo["peticion"] +
        ("ANEXO: Relación de documentos adjuntos\n" + "\n".join(anexos) + "\n" if anexos else "")
    )

    return {
        "documentos": documentos,
        "texto": doc_txt
    }


# ====== EXTRACTOR ESTRUCTURADO PARA DEMANDA ======
def _inferir_instancia_desde_texto(texto: str) -> str:
    t = (texto or '').lower()
    if 'tribunal supremo' in t:
        return 'TS'
    if 'tribunal superior de justicia' in t or 'tsj' in t:
        return 'TSJ'
    return 'otra'


def _extraer_primera_fecha(texto: str) -> Optional[str]:
    import re as _re
    for patron in [r"\b\d{1,2}[\-/\.\s]\d{1,2}[\-/\.\s]\d{2,4}\b", r"\b\d{4}[\-/\.]\d{1,2}[\-/\.]\d{1,2}\b"]:
        m = _re.search(patron, texto)
        if m:
            return m.group(0)
    return None


def _extraer_por_regex(texto: str, regex: str, group: int = 1) -> Optional[str]:
    import re as _re
    m = _re.search(regex, texto, _re.IGNORECASE)
    return m.group(group).strip() if m else None


def _resumir_fundamentos(texto: str) -> List[str]:
    seccion = _extraer_seccion(
        texto,
        ["FUNDAMENTOS DE DERECHO", "FUNDAMENTOS"],
        ["FALLO", "PARTE DISPOSITIVA", "RESUELVO", "RESOLVEMOS", "SUPLICO", "HECHOS"]
    )
    if not seccion:
        return []
    # dividir en frases y tomar las 3 primeras relevantes
    import re as _re
    frases = [f.strip() for f in _re.split(r"(?<=[\.!?])\s+", seccion) if len(f.strip()) > 30]
    return frases[:3]


@app.post("/api/extract/demanda")
async def api_extract_demanda(payload: Dict[str, Any]):
    try:
        nombres: List[str] = payload.get("nombres_archivo") or []
        if not isinstance(nombres, list) or not nombres:
            raise HTTPException(status_code=400, detail="Debe indicar 'nombres_archivo' (lista)")
        paths = [SENTENCIAS_DIR / n for n in nombres if (SENTENCIAS_DIR / n).exists()]
        if not paths:
            raise HTTPException(status_code=404, detail="No se encontraron los archivos indicados")

        docs_out: List[Dict[str, Any]] = []
        sugerencias: Dict[str, Any] = {"profesion": None, "empresa": None, "mutua": None, "base_reguladora": None}

        for p in paths:
            texto = _leer_texto_archivo_simple(p)
            fallo = _extraer_seccion(texto, ["FALLO", "PARTE DISPOSITIVA", "RESUELVO", "RESOLVEMOS"], ["FUNDAMENTOS", "HECHOS", "ANTECEDENTES"]) or ""
            fundamentos_resumen = _resumir_fundamentos(texto)
            instancia = _inferir_instancia_desde_texto(texto)
            fecha = _extraer_primera_fecha(texto)
            organo = None
            # aproximación al órgano
            for k in ["TRIBUNAL SUPREMO", "TRIBUNAL SUPERIOR DE JUSTICIA", "AUDIENCIA", "JUZGADO DE LO SOCIAL"]:
                if k.lower() in (texto or '').lower():
                    organo = k.title()
                    break

            # sugerencias globales
            profesion = _extraer_por_regex(texto, r"profesi[oó]n\s+habitual\s+(de|:)?\s*([A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+)", 2)
            if profesion and not sugerencias.get("profesion"):
                sugerencias["profesion"] = profesion
            empresa = _extraer_por_regex(texto, r"emplead[oa]\s+por\s+([A-ZÁÉÍÓÚÜÑa-záéíóúüñ0-9 .,&;-]+)")
            if empresa and not sugerencias.get("empresa"):
                sugerencias["empresa"] = empresa
            mutua = _extraer_por_regex(texto, r"mutua\s+([A-ZÁÉÍÓÚÜÑ][A-Za-zÁÉÍÓÚÜÑ ]+)")
            if mutua and not sugerencias.get("mutua"):
                sugerencias["mutua"] = mutua
            br = _extraer_por_regex(texto, r"base\s+reguladora[^0-9]*([0-9\.,]+)")
            if br and not sugerencias.get("base_reguladora"):
                sugerencias["base_reguladora"] = br

            docs_out.append({
                "archivo": p.name,
                "instancia": instancia,
                "fecha": fecha,
                "organo": organo,
                "fallo": fallo,
                "fundamentos_resumen": fundamentos_resumen
            })

        return {"documentos": docs_out, "sugerencias_meta": sugerencias}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en extracción de demanda: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/demanda-base")
async def api_demanda_base(payload: Dict[str, Any]):
    try:
        nombres: List[str] = payload.get("nombres_archivo") or []
        if not isinstance(nombres, list) or not nombres:
            raise HTTPException(status_code=400, detail="Debe indicar 'nombres_archivo' (lista)")
        paths: List[Path] = []
        for n in nombres:
            p = SENTENCIAS_DIR / n
            if p.exists():
                paths.append(p)
        if not paths:
            raise HTTPException(status_code=404, detail="No se encontraron los archivos indicados")
        meta = payload.get("meta") if isinstance(payload.get("meta"), dict) else {}
        doc = _generar_demanda_base_para(paths, meta)
        return doc
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generando demanda base: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/demanda-base/txt")
async def api_demanda_base_txt(payload: Dict[str, Any]):
    try:
        nombres: List[str] = payload.get("nombres_archivo") or []
        if not isinstance(nombres, list) or not nombres:
            raise HTTPException(status_code=400, detail="Debe indicar 'nombres_archivo' (lista)")
        paths = [SENTENCIAS_DIR / n for n in nombres if (SENTENCIAS_DIR / n).exists()]
        if not paths:
            raise HTTPException(status_code=404, detail="No se encontraron los archivos indicados")
        meta = payload.get("meta") if isinstance(payload.get("meta"), dict) else {}
        doc = _generar_demanda_base_para(paths, meta)
        filename = f"demanda_base_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        headers = {"Content-Disposition": f"attachment; filename={filename}"}
        return PlainTextResponse(content=doc.get("texto", ""), headers=headers)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generando TXT demanda base: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ====== LISTAR / ELIMINAR DOCUMENTOS ======
@app.get("/api/documentos")
async def listar_documentos():
    """Lista documentos disponibles en sentencias/ y uploads/."""
    docs = []
    for carpeta in [SENTENCIAS_DIR, UPLOADS_DIR]:
        if carpeta.exists():
            for f in carpeta.iterdir():
                if f.is_file() and f.suffix.lower() in ['.pdf', '.txt']:
                    docs.append({
                        "nombre": f.name,
                        "ruta": str(f),
                        "carpeta": 'sentencias' if carpeta == SENTENCIAS_DIR else 'uploads',
                        "tamaño": f.stat().st_size,
                        "modificado": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                    })
    return {"documentos": sorted(docs, key=lambda x: x["modificado"], reverse=True)}


@app.delete("/api/documentos")
async def eliminar_documento_api(payload: DeleteDocumentPayload):
    """Elimina un documento por nombre desde sentencias/ o uploads/."""
    nombre = payload.nombre_archivo
    if not nombre:
        raise HTTPException(status_code=400, detail="Nombre de archivo requerido")
    candidatos = [SENTENCIAS_DIR / nombre, UPLOADS_DIR / nombre]
    encontrado = None
    for p in candidatos:
        if p.exists() and p.is_file():
            encontrado = p
            break
    if not encontrado:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    try:
        encontrado.unlink()
        return {"status": "ok", "eliminado": nombre}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo eliminar: {e}")


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
                from .backend.analisis import AnalizadorLegal
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


# Ruta de compatibilidad: redirige a la vista de archivo
@app.get("/documento/{nombre_archivo}")
async def redirigir_documento(nombre_archivo: str):
    return RedirectResponse(url=f"/archivo/{nombre_archivo}")


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
                
                # Marcar tiempo de inicio para este archivo
                tiempo_inicio = datetime.now()
                
                # Usar el analizador de IA si está disponible, sino el básico
                if ANALIZADOR_IA_DISPONIBLE:
                    logger.info(f"🤖 Usando analizador de IA para: {archivo.name}")
                    from .backend.analisis import AnalizadorLegal
                    analizador = AnalizadorLegal()
                    analizador._tiempo_inicio = tiempo_inicio
                    resultado = analizador.analizar_documento(str(archivo))
                else:
                    logger.info(f"🔧 Usando analizador básico para: {archivo.name}")
                    analizador_basico._tiempo_inicio = tiempo_inicio
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
    
    def safe_print(text: str) -> None:
        try:
            print(text)
        except Exception:
            try:
                # Remove non-encodable characters for Windows consoles
                print(text.encode("cp1252", "ignore").decode("cp1252"))
            except Exception:
                try:
                    print(text.encode("utf-8", "ignore").decode("utf-8"))
                except Exception:
                    print("Inicio de servidor FastAPI")
    
    safe_print("🚀 Iniciando Analizador de Sentencias IPP/INSS...")
    safe_print(f"📁 Directorio de sentencias: {SENTENCIAS_DIR}")
    safe_print(f"🤖 IA disponible: {'✅ Sí' if ANALIZADOR_IA_DISPONIBLE else '❌ No'}")
    safe_print(f"🌐 URL: http://localhost:8000")
    safe_print(f"📚 Documentación: http://localhost:8000/docs")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )
