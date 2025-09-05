#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de análisis inteligente para documentos legales
Implementa extracción de texto, predicción de casos favorables y extracción de argumentos clave
"""

import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import numpy as np
import pandas as pd

# Importaciones condicionales para evitar errores si no están instaladas
try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logging.warning("pdfplumber no disponible. No se pueden procesar archivos PDF.")

try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logging.warning("TensorFlow no disponible. No se pueden hacer predicciones de IA.")

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("Transformers no disponible. No se pueden extraer entidades.")

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalizadorLegal:
    """Clase principal para análisis inteligente de documentos legales"""
    
    def __init__(self, modelo_path: str = "modelo/clasificador_ipp", tokenizer_path: str = "modelo/tokenizer.pkl"):
        """
        Inicializa el analizador legal
        
        Args:
            modelo_path: Ruta al modelo TensorFlow entrenado
            tokenizer_path: Ruta al tokenizer guardado
        """
        self.modelo_path = Path(modelo_path)
        self.tokenizer_path = Path(tokenizer_path)
        self.modelo = None
        self.tokenizer = None
        self.ner_pipeline = None
        
        # Inicializar componentes de IA
        self._inicializar_ia()
        
        # Frases clave para análisis básico (como respaldo)
        self.frases_clave = {
            "incapacidad permanente parcial": ["incapacidad permanente parcial", "IPP", "permanente parcial"],
            "reclamación administrativa previa": ["reclamación administrativa previa", "RAP", "recurso previo"],
            "INSS": ["INSS", "Instituto Nacional de la Seguridad Social", "Seguridad Social"],
            "lesiones permanentes no incapacitantes": ["lesiones permanentes no incapacitantes", "LPNI", "lesiones no incapacitantes"],
            "limpiadora": ["limpiadora", "personal de limpieza", "servicios de limpieza"],
            "rotura del manguito rotador": ["rotura del manguito rotador", "supraespinoso", "hombro derecho", "manguito rotador"]
        }
    
    def _inicializar_ia(self):
        """Inicializa los componentes de inteligencia artificial"""
        try:
            # Inicializar modelo TensorFlow si está disponible
            if TENSORFLOW_AVAILABLE and self.modelo_path.exists():
                self.modelo = tf.keras.models.load_model(str(self.modelo_path))
                logger.info("Modelo TensorFlow cargado correctamente")
            else:
                logger.warning("Modelo TensorFlow no disponible o no encontrado")
            
            # Inicializar pipeline de NER si está disponible
            if TRANSFORMERS_AVAILABLE:
                try:
                    # Usar modelo en español para extracción de entidades
                    self.ner_pipeline = pipeline(
                        "ner",
                        model="nlptown/bert-base-multilingual-uncased-ner",
                        aggregation_strategy="simple"
                    )
                    logger.info("Pipeline de NER inicializado correctamente")
                except Exception as e:
                    logger.warning(f"No se pudo inicializar NER: {e}")
            
        except Exception as e:
            logger.error(f"Error al inicializar IA: {e}")
    
    def extraer_texto(self, ruta_archivo: str) -> str:
        """
        Extrae texto de archivos PDF o TXT
        
        Args:
            ruta_archivo: Ruta al archivo a procesar
            
        Returns:
            Texto extraído del archivo
        """
        try:
            ruta = Path(ruta_archivo)
            extension = ruta.suffix.lower()
            
            if extension == '.pdf':
                return self._extraer_texto_pdf(ruta)
            elif extension == '.txt':
                return self._extraer_texto_txt(ruta)
            else:
                raise ValueError(f"Formato de archivo no soportado: {extension}")
                
        except Exception as e:
            logger.error(f"Error al extraer texto de {ruta_archivo}: {e}")
            return f"Error: {str(e)}"
    
    def _extraer_texto_pdf(self, ruta: Path) -> str:
        """Extrae texto de archivos PDF usando pdfplumber"""
        if not PDF_AVAILABLE:
            return "Error: pdfplumber no está disponible para procesar PDFs"
        
        try:
            texto_completo = ""
            with pdfplumber.open(ruta) as pdf:
                for pagina in pdf.pages:
                    texto_pagina = pagina.extract_text()
                    if texto_pagina:
                        texto_completo += texto_pagina + "\n"
            
            return texto_completo.strip()
            
        except Exception as e:
            logger.error(f"Error al procesar PDF {ruta}: {e}")
            return f"Error al procesar PDF: {str(e)}"
    
    def _extraer_texto_txt(self, ruta: Path) -> str:
        """Extrae texto de archivos TXT"""
        try:
            # Intentar diferentes encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(ruta, 'r', encoding=encoding) as archivo:
                        return archivo.read().strip()
                except UnicodeDecodeError:
                    continue
            
            # Si ningún encoding funciona, usar binary y decodificar
            with open(ruta, 'rb') as archivo:
                contenido = archivo.read()
                return contenido.decode('utf-8', errors='ignore').strip()
                
        except Exception as e:
            logger.error(f"Error al procesar TXT {ruta}: {e}")
            return f"Error al procesar TXT: {str(e)}"
    
    def predecir_favorable(self, texto: str) -> Tuple[bool, float]:
        """
        Predice si un caso es favorable usando el modelo de IA
        
        Args:
            texto: Texto del documento a analizar
            
        Returns:
            Tupla (es_favorable, confianza)
        """
        if not TENSORFLOW_AVAILABLE or self.modelo is None:
            # Fallback: análisis basado en reglas
            return self._analisis_basado_reglas(texto)
        
        try:
            # Preprocesar texto para el modelo
            texto_procesado = self._preprocesar_texto(texto)
            
            # Hacer predicción
            prediccion = self.modelo.predict([texto_procesado])
            confianza = float(prediccion[0][0])
            es_favorable = confianza > 0.5
            
            return es_favorable, confianza
            
        except Exception as e:
            logger.error(f"Error en predicción de IA: {e}")
            # Fallback a análisis basado en reglas
            return self._analisis_basado_reglas(texto)
    
    def _preprocesar_texto(self, texto: str) -> str:
        """Preprocesa el texto para el modelo de IA"""
        # Limpiar y normalizar texto
        texto_limpio = re.sub(r'\s+', ' ', texto.lower())
        texto_limpio = re.sub(r'[^\w\s]', '', texto_limpio)
        return texto_limpio[:1000]  # Limitar longitud
    
    def _analisis_basado_reglas(self, texto: str) -> Tuple[bool, float]:
        """Análisis basado en reglas como fallback"""
        texto_lower = texto.lower()
        
        # Palabras positivas que indican caso favorable
        palabras_positivas = [
            "estimamos", "estimamos procedente", "procedente", "favorable",
            "accedemos", "concedemos", "reconocemos", "declaramos procedente"
        ]
        
        # Palabras negativas que indican caso desfavorable
        palabras_negativas = [
            "desestimamos", "desestimamos la reclamación", "desfavorable",
            "no procedente", "rechazamos", "denegamos"
        ]
        
        # Contar ocurrencias
        positivas = sum(1 for palabra in palabras_positivas if palabra in texto_lower)
        negativas = sum(1 for palabra in palabras_negativas if palabra in texto_lower)
        
        # Calcular confianza basada en la diferencia
        total = positivas + negativas
        if total == 0:
            return True, 0.5  # Neutral si no hay indicadores claros
        
        confianza = positivas / total if positivas > negativas else negativas / total
        es_favorable = positivas > negativas
        
        return es_favorable, confianza
    
    def extraer_argumentos_favorables(self, texto: str) -> List[Dict[str, Any]]:
        """
        Extrae argumentos clave usados en sentencias favorables
        
        Args:
            texto: Texto del documento
            
        Returns:
            Lista de argumentos extraídos
        """
        argumentos = []
        
        try:
            # Extraer argumentos usando patrones de texto
            patrones_argumentos = [
                r"por\s+(?:lo\s+)?que\s+([^.]*?\.)",
                r"fundamentos?\s+(?:de\s+)?(?:derecho|derecho\s+por\s+lo\s+que)\s+([^.]*?\.)",
                r"considerando\s+que\s+([^.]*?\.)",
                r"en\s+consecuencia\s+([^.]*?\.)"
            ]
            
            for patron in patrones_argumentos:
                matches = re.finditer(patron, texto, re.IGNORECASE)
                for match in matches:
                    argumento = match.group(1).strip()
                    if len(argumento) > 20:  # Filtrar argumentos muy cortos
                        argumentos.append({
                            "tipo": "argumento_legal",
                            "texto": argumento,
                            "posicion": match.start(),
                            "confianza": 0.8
                        })
            
            # Extraer referencias legales
            referencias = self._extraer_referencias_legales(texto)
            argumentos.extend(referencias)
            
            # Extraer entidades nombradas si está disponible
            if TRANSFORMERS_AVAILABLE and self.ner_pipeline:
                entidades = self._extraer_entidades_ner(texto)
                argumentos.extend(entidades)
            
        except Exception as e:
            logger.error(f"Error al extraer argumentos: {e}")
        
        return argumentos
    
    def _extraer_referencias_legales(self, texto: str) -> List[Dict[str, Any]]:
        """Extrae referencias legales del texto"""
        referencias = []
        
        # Patrones para referencias legales
        patrones = [
            r"(?:artículo|art\.)\s+(\d+[^\s]*)\s+(?:de\s+)?(?:la\s+)?([^,.\n]+)",
            r"(?:STS|Sentencia|Resolución)\s+(\d+/\d{4})",
            r"(?:Ley|LGSS|Ley\s+General\s+de\s+la\s+Seguridad\s+Social)",
            r"(?:Real\s+Decreto|RD)\s+(\d+/\d{4})"
        ]
        
        for patron in patrones:
            matches = re.finditer(patron, texto, re.IGNORECASE)
            for match in matches:
                referencias.append({
                    "tipo": "referencia_legal",
                    "texto": match.group(0),
                    "posicion": match.start(),
                    "confianza": 0.9
                })
        
        return referencias
    
    def _extraer_entidades_ner(self, texto: str) -> List[Dict[str, Any]]:
        """Extrae entidades nombradas usando el modelo NER"""
        try:
            # Dividir texto en chunks para evitar límites de token
            chunks = [texto[i:i+500] for i in range(0, len(texto), 500)]
            entidades = []
            
            for i, chunk in enumerate(chunks):
                if len(chunk.strip()) < 10:
                    continue
                    
                try:
                    resultados = self.ner_pipeline(chunk)
                    for resultado in resultados:
                        entidades.append({
                            "tipo": "entidad_nombrada",
                            "texto": resultado["word"],
                            "categoria": resultado["entity_group"],
                            "posicion": i * 500 + resultado["start"],
                            "confianza": resultado["score"]
                        })
                except Exception as e:
                    logger.warning(f"Error en chunk {i}: {e}")
                    continue
            
            return entidades
            
        except Exception as e:
            logger.error(f"Error en extracción NER: {e}")
            return []
    
    def analizar_documento(self, ruta_archivo: str) -> Dict[str, Any]:
        """
        Analiza completamente un documento legal
        
        Args:
            ruta_archivo: Ruta al archivo a analizar
            
        Returns:
            Diccionario con análisis completo
        """
        try:
            # Extraer texto
            texto = self.extraer_texto(ruta_archivo)
            if texto.startswith("Error:"):
                return {
                    "error": texto,
                    "archivo": ruta_archivo,
                    "procesado": False
                }
            
            # Predicción de caso favorable
            es_favorable, confianza = self.predecir_favorable(texto)
            
            # Extraer argumentos
            argumentos = self.extraer_argumentos_favorables(texto)
            
            # Análisis de frases clave (funcionalidad existente)
            frases_encontradas = self._contar_frases_clave(texto, Path(ruta_archivo).name)
            
            # Generar resumen inteligente
            resumen = self._generar_resumen_inteligente(
                es_favorable, confianza, argumentos, frases_encontradas
            )
            
            return {
                "archivo": ruta_archivo,
                "procesado": True,
                "texto_extraido": texto[:500] + "..." if len(texto) > 500 else texto,
                "longitud_texto": len(texto),
                "prediccion": {
                    "es_favorable": es_favorable,
                    "confianza": confianza,
                    "interpretacion": "Favorable" if es_favorable else "Desfavorable"
                },
                "argumentos": argumentos,
                "frases_clave": frases_encontradas,
                "resumen_inteligente": resumen,
                "insights_juridicos": self._generar_insights_juridicos(
                    es_favorable, argumentos, frases_encontradas
                )
            }
            
        except Exception as e:
            logger.error(f"Error en análisis completo: {e}")
            return {
                "error": f"Error en análisis: {str(e)}",
                "archivo": ruta_archivo,
                "procesado": False
            }
    
    def _contar_frases_clave(self, texto: str, nombre_archivo: str = "") -> Dict[str, Any]:
        """Mantiene la funcionalidad existente de conteo de frases"""
        if not texto or texto.startswith("Error:"):
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
                    
                    # Obtener contexto
                    context_start = max(0, start_pos - 50)
                    context_end = min(len(texto), end_pos + 50)
                    contexto = texto[context_start:context_end]
                    
                    ocurrencias.append({
                        "frase": variante,
                        "posicion": start_pos,
                        "contexto": contexto,
                        "linea": texto[:start_pos].count('\n') + 1,
                        "archivo": nombre_archivo
                    })
            
            if total > 0:
                resultados[categoria] = {
                    "total": total,
                    "ocurrencias": ocurrencias
                }
        
        return resultados
    
    def _generar_resumen_inteligente(self, es_favorable: bool, confianza: float, 
                                   argumentos: List[Dict], frases_clave: Dict) -> str:
        """Genera un resumen inteligente del análisis"""
        if es_favorable:
            base = f"El documento presenta indicadores favorables (confianza: {confianza:.1%}). "
        else:
            base = f"El documento presenta indicadores desfavorables (confianza: {confianza:.1%}). "
        
        if argumentos:
            base += f"Se identificaron {len(argumentos)} argumentos legales clave. "
        
        if frases_clave:
            total_frases = sum(datos["total"] for datos in frases_clave.values())
            base += f"Se encontraron {total_frases} menciones de frases clave relevantes. "
        
        return base
    
    def _generar_insights_juridicos(self, es_favorable: bool, argumentos: List[Dict], 
                                   frases_clave: Dict) -> List[str]:
        """Genera insights jurídicos basados en el análisis"""
        insights = []
        
        if es_favorable:
            insights.append("El documento presenta argumentos sólidos a favor del caso.")
        else:
            insights.append("El documento presenta argumentos que pueden ser desfavorables.")
        
        if argumentos:
            insights.append(f"Se identificaron {len(argumentos)} argumentos legales que pueden ser relevantes.")
        
        if frases_clave:
            categorias = list(frases_clave.keys())
            insights.append(f"Las categorías más mencionadas son: {', '.join(categorias[:3])}.")
        
        return insights


# Función de conveniencia para uso directo
def analizar_documento(ruta_archivo: str) -> Dict[str, Any]:
    """
    Función de conveniencia para analizar un documento
    
    Args:
        ruta_archivo: Ruta al archivo a analizar
        
    Returns:
        Resultado del análisis
    """
    analizador = AnalizadorLegal()
    return analizador.analizar_documento(ruta_archivo)
