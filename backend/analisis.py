#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Análisis de IA para Documentos Legales
Asume que el modelo ya está entrenado y guardado
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import json
import pickle

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalizadorLegal:
    """
    Analizador legal basado en IA pre-entrenada
    Asume que el modelo ya está entrenado y guardado
    """
    
    def __init__(self, modelo_path: str = "models/modelo_legal.pkl"):
        """
        Inicializa el analizador con el modelo pre-entrenado
        
        Args:
            modelo_path: Ruta al archivo del modelo guardado
        """
        self.modelo_path = Path(modelo_path)
        self.modelo = None
        self.vectorizador = None
        self.clasificador = None
        self.frases_clave = self._cargar_frases_clave()
        
        # Intentar cargar el modelo
        self._cargar_modelo()
    
    def _cargar_frases_clave(self) -> Dict[str, List[str]]:
        """Carga las frases clave desde archivo de configuración"""
        frases_default = {
            "incapacidad_permanente_parcial": [
                "incapacidad permanente parcial", "IPP", "permanente parcial",
                "incapacidad parcial permanente", "secuela permanente",
                "incapacidad permanente", "secuelas permanentes"
            ],
            "reclamacion_administrativa": [
                "reclamación administrativa previa", "RAP", "reclamación previa",
                "vía administrativa", "recurso administrativo", "reclamación"
            ],
            "inss": [
                "INSS", "Instituto Nacional de la Seguridad Social", "Seguridad Social",
                "Instituto Nacional", "Seguridad Social"
            ],
            "lesiones_permanentes": [
                "lesiones permanentes no incapacitantes", "LPNI", "secuelas",
                "lesiones permanentes", "secuelas permanentes", "lesiones"
            ],
            "personal_limpieza": [
                "limpiadora", "personal de limpieza", "servicios de limpieza",
                "trabajador de limpieza", "empleada de limpieza", "limpieza"
            ],
            "lesiones_hombro": [
                "rotura del manguito rotador", "supraespinoso", "hombro derecho",
                "lesión de hombro", "manguito rotador", "tendón supraespinoso",
                "hombro", "manguito"
            ],
            "procedimiento_legal": [
                "procedente", "desestimamos", "estimamos", "fundada",
                "infundada", "accedemos", "concedemos", "reconocemos"
            ]
        }
        
        # Intentar cargar desde archivo de configuración
        config_path = Path("models/frases_clave.json")
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"No se pudo cargar configuración de frases clave: {e}")
        
        return frases_default
    
    def _cargar_modelo(self):
        """Carga el modelo pre-entrenado"""
        try:
            if self.modelo_path.exists():
                with open(self.modelo_path, 'rb') as f:
                    modelo_data = pickle.load(f)
                    self.modelo = modelo_data.get('modelo')
                    self.vectorizador = modelo_data.get('vectorizador')
                    self.clasificador = modelo_data.get('clasificador')
                    logger.info("✅ Modelo de IA cargado correctamente")
            else:
                logger.warning(f"⚠️ Modelo no encontrado en {self.modelo_path}")
                logger.info("Se usará análisis basado en reglas")
        except Exception as e:
            logger.error(f"❌ Error cargando modelo: {e}")
            logger.info("Se usará análisis basado en reglas")
    
    def analizar_documento(self, ruta_archivo: str) -> Dict[str, Any]:
        """
        Analiza un documento legal usando IA
        
        Args:
            ruta_archivo: Ruta al archivo a analizar
            
        Returns:
            Diccionario con resultados del análisis
        """
        try:
            # Leer contenido del archivo
            contenido = self._leer_archivo(ruta_archivo)
            if not contenido:
                return self._crear_resultado_error("No se pudo leer el contenido del archivo")
            
            # Extraer nombre del archivo de la ruta
            nombre_archivo = Path(ruta_archivo).name
            
            # Análisis con IA si está disponible
            if self.modelo and self.vectorizador and self.clasificador:
                resultado = self._analisis_con_ia(contenido, nombre_archivo)
            else:
                resultado = self._analisis_basado_reglas(contenido, nombre_archivo)
            
            # Agregar metadatos
            resultado.update({
                "archivo": ruta_archivo,
                "nombre_archivo": Path(ruta_archivo).name,
                "procesado": True,
                "texto_extraido": contenido[:1000] + "..." if len(contenido) > 1000 else contenido,
                "longitud_texto": len(contenido),
                "timestamp": self._obtener_timestamp(),
                "ruta_archivo": ruta_archivo
            })
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error analizando documento: {e}")
            return self._crear_resultado_error(f"Error en análisis: {str(e)}")
    
    def _leer_archivo(self, ruta: str) -> Optional[str]:
        """Lee el contenido de un archivo"""
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
            elif ruta.endswith('.pdf'):
                # Leer archivo PDF
                return self._leer_pdf(ruta)
            else:
                # Para otros formatos, usar función genérica
                return self._leer_archivo_generico(ruta)
        except Exception as e:
            logger.error(f"Error leyendo archivo {ruta}: {e}")
            return None
    
    def _leer_archivo_generico(self, ruta: str) -> str:
        """Lee archivos de diferentes formatos"""
        # Por ahora solo manejamos texto
        # Aquí se podría extender para PDF, DOC, etc.
        return "Contenido del archivo no disponible en formato de texto"
    
    def _leer_pdf(self, ruta: str) -> Optional[str]:
        """Lee archivos PDF y extrae el texto"""
        try:
            # Intentar importar PyPDF2
            try:
                import PyPDF2
            except ImportError:
                logger.warning("PyPDF2 no está instalado. Instala: pip install PyPDF2")
                return "Error: PyPDF2 no está instalado. Ejecuta: pip install PyPDF2"
            
            texto = ""
            with open(ruta, 'rb') as archivo:
                lector = PyPDF2.PdfReader(archivo)
                
                for pagina in lector.pages:
                    texto += pagina.extract_text() + "\n"
                
                return texto.strip()
                
        except Exception as e:
            logger.error(f"Error leyendo PDF {ruta}: {e}")
            return f"Error leyendo PDF: {str(e)}"
    
    def _analisis_con_ia(self, contenido: str, nombre_archivo: str = None) -> Dict[str, Any]:
        """Análisis usando el modelo de IA"""
        try:
            # Vectorizar el texto
            texto_vectorizado = self.vectorizador.transform([contenido])
            
            # Predicción
            prediccion = self.clasificador.predict(texto_vectorizado)[0]
            probabilidades = self.clasificador.predict_proba(texto_vectorizado)[0]
            
            # Obtener confianza
            confianza = max(probabilidades)
            
            # Análisis de frases clave
            frases_encontradas = self._analizar_frases_clave(contenido, nombre_archivo)
            
            # Extraer argumentos
            argumentos = self._extraer_argumentos_avanzados(contenido)
            
            # Generar insights
            insights = self._generar_insights_avanzados(prediccion, frases_encontradas, confianza)
            
            return {
                "prediccion": {
                    "es_favorable": bool(prediccion),
                    "confianza": float(confianza),
                    "interpretacion": "Favorable" if prediccion else "Desfavorable",
                    "probabilidades": {
                        "favorable": float(probabilidades[1] if len(probabilidades) > 1 else 0.5),
                        "desfavorable": float(probabilidades[0] if len(probabilidades) > 1 else 0.5)
                    }
                },
                "argumentos": argumentos,
                "frases_clave": frases_encontradas,
                "resumen_inteligente": self._generar_resumen_ia(prediccion, confianza, frases_encontradas),
                "insights_juridicos": insights,
                "total_frases_clave": sum(datos["total"] for datos in frases_encontradas.values()),
                "modelo_ia": True,
                "metodo_analisis": "IA pre-entrenada"
            }
            
        except Exception as e:
            logger.error(f"Error en análisis con IA: {e}")
            # Fallback a análisis basado en reglas
            return self._analisis_basado_reglas(contenido, nombre_archivo)
    
    def _analisis_basado_reglas(self, contenido: str, nombre_archivo: str = None) -> Dict[str, Any]:
        """Análisis basado en reglas y patrones"""
        # Análisis de frases clave
        frases_encontradas = self._analizar_frases_clave(contenido, nombre_archivo)
        
        # Predicción basada en reglas
        prediccion = self._prediccion_basada_reglas(contenido)
        
        # Extraer argumentos
        argumentos = self._extraer_argumentos_basicos(contenido)
        
        # Generar insights
        insights = self._generar_insights_basicos(prediccion, frases_encontradas)
        
        return {
            "prediccion": prediccion,
            "argumentos": argumentos,
            "frases_clave": frases_encontradas,
            "resumen_inteligente": self._generar_resumen_reglas(prediccion, frases_encontradas),
            "insights_juridicos": insights,
            "total_frases_clave": sum(datos["total"] for datos in frases_encontradas.values()),
            "modelo_ia": False,
            "metodo_analisis": "Reglas y patrones"
        }
    
    def _analizar_frases_clave(self, texto: str, nombre_archivo: str = None) -> Dict[str, Any]:
        """Analiza las frases clave en el texto"""
        if not texto:
            return {}
        
        # Usar el nombre del archivo real o un valor por defecto
        archivo_nombre = nombre_archivo or "archivo_desconocido"
        
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
                    
                    # Obtener contexto (150 caracteres antes y después)
                    context_start = max(0, start_pos - 150)
                    context_end = min(len(texto), end_pos + 150)
                    contexto = texto[context_start:context_end]
                    
                    # Marcar la frase encontrada
                    frase_encontrada = texto[start_pos:end_pos]
                    contexto_marcado = contexto.replace(frase_encontrada, f"**{frase_encontrada}**")
                    
                    ocurrencias.append({
                        "frase": variante,
                        "posicion": start_pos,
                        "contexto": contexto_marcado,
                        "linea": texto[:start_pos].count('\n') + 1,
                        "archivo": archivo_nombre
                    })
            
            if total > 0:
                resultados[categoria] = {
                    "total": total,
                    "ocurrencias": ocurrencias
                }
        
        return resultados
    
    def _prediccion_basada_reglas(self, texto: str) -> Dict[str, Any]:
        """Predicción basada en reglas y patrones"""
        texto_lower = texto.lower()
        
        palabras_positivas = [
            "estimamos", "estimamos procedente", "procedente", "favorable",
            "accedemos", "concedemos", "reconocemos", "declaramos procedente",
            "estimamos fundada", "fundada", "estimamos parcialmente",
            "estimamos fundada en parte", "estimamos parcialmente fundada"
        ]
        
        palabras_negativas = [
            "desestimamos", "desestimamos la reclamación", "desfavorable",
            "no procedente", "rechazamos", "denegamos", "estimamos infundada",
            "infundada", "desestimamos parcialmente", "estimamos infundada en parte"
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
        
        # Calcular confianza basada en la diferencia
        diferencia = abs(positivas - negativas)
        confianza = min(0.95, max(0.1, 0.5 + (diferencia / (total + 1)) * 0.4))
        
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
    
    def _extraer_argumentos_avanzados(self, texto: str) -> List[Dict[str, Any]]:
        """Extrae argumentos legales avanzados"""
        argumentos = []
        
        patrones_avanzados = [
            r"por\s+(?:lo\s+)?que\s+([^.]*?\.)",
            r"fundamentos?\s+(?:de\s+)?(?:derecho|derecho\s+por\s+lo\s+que)\s+([^.]*?\.)",
            r"considerando\s+que\s+([^.]*?\.)",
            r"vistos\s+([^.]*?\.)",
            r"resultando\s+([^.]*?\.)",
            r"en\s+su\s+virtud\s+([^.]*?\.)",
            r"por\s+ello\s+([^.]*?\.)"
        ]
        
        for patron in patrones_avanzados:
            matches = re.finditer(patron, texto, re.IGNORECASE)
            for match in matches:
                argumento = match.group(1).strip()
                if len(argumento) > 20:
                    # Calcular confianza basada en la longitud y complejidad
                    confianza = min(0.95, 0.6 + (len(argumento) / 1000) * 0.3)
                    
                    argumentos.append({
                        "tipo": "argumento_legal",
                        "texto": argumento,
                        "posicion": match.start(),
                        "confianza": confianza,
                        "categoria": "fundamento_juridico",
                        "longitud": len(argumento)
                    })
        
        return argumentos
    
    def _extraer_argumentos_basicos(self, texto: str) -> List[Dict[str, Any]]:
        """Extrae argumentos legales básicos"""
        argumentos = []
        
        patrones = [
            r"por\s+(?:lo\s+)?que\s+([^.]*?\.)",
            r"fundamentos?\s+(?:de\s+)?(?:derecho|derecho\s+por\s+lo\s+que)\s+([^.]*?\.)",
            r"considerando\s+que\s+([^.]*?\.)"
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
    
    def _generar_insights_avanzados(self, prediccion: bool, frases_clave: Dict, confianza: float) -> List[str]:
        """Genera insights jurídicos avanzados"""
        insights = []
        
        if prediccion:
            insights.append("El documento presenta argumentos sólidos a favor del caso.")
            insights.append("La resolución favorece al reclamante basándose en evidencia legal.")
        else:
            insights.append("El documento presenta argumentos que pueden ser desfavorables.")
            insights.append("La resolución no favorece al reclamante según el análisis legal.")
        
        if frases_clave:
            categorias = list(frases_clave.keys())
            insights.append(f"Se identificaron {len(categorias)} categorías de frases clave relevantes.")
            
            # Análisis de categorías más importantes
            if "incapacidad_permanente_parcial" in frases_clave:
                insights.append("El caso involucra aspectos de incapacidad permanente parcial.")
            
            if "reclamacion_administrativa" in frases_clave:
                insights.append("Se identificaron elementos de reclamación administrativa previa.")
        
        insights.append(f"Confianza del análisis: {confianza:.1%}")
        insights.append("Análisis realizado con modelo de IA pre-entrenado.")
        
        return insights
    
    def _generar_insights_basicos(self, prediccion: Dict, frases_clave: Dict) -> List[str]:
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
        insights.append("Análisis realizado con reglas y patrones.")
        
        return insights
    
    def _generar_resumen_ia(self, prediccion: bool, confianza: float, frases_clave: Dict) -> str:
        """Genera resumen inteligente usando IA"""
        if prediccion:
            base = "Análisis favorable del documento legal usando IA. "
        else:
            base = "Análisis desfavorable del documento legal usando IA. "
        
        if frases_clave:
            total_frases = sum(datos["total"] for datos in frases_clave.values())
            base += f"Se identificaron {total_frases} frases clave relevantes. "
        
        base += f"Confianza del análisis: {confianza:.1%}. "
        base += "Análisis realizado con modelo de IA pre-entrenado."
        
        return base
    
    def _generar_resumen_reglas(self, prediccion: Dict, frases_clave: Dict) -> str:
        """Genera resumen basado en reglas"""
        if prediccion["es_favorable"]:
            base = "Análisis favorable del documento legal. "
        else:
            base = "Análisis desfavorable del documento legal. "
        
        if frases_clave:
            total_frases = sum(datos["total"] for datos in frases_clave.values())
            base += f"Se identificaron {total_frases} frases clave relevantes. "
        
        base += f"Confianza del análisis: {prediccion['confianza']:.1%}. "
        base += "Análisis realizado con reglas y patrones."
        
        return base
    
    def _obtener_timestamp(self) -> str:
        """Obtiene el timestamp actual"""
        from datetime import datetime
        return datetime.now().isoformat()
    
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
            "total_frases_clave": 0,
            "modelo_ia": False
        }


# Función de conveniencia para crear instancia
def crear_analizador() -> AnalizadorLegal:
    """Crea una instancia del analizador legal"""
    return AnalizadorLegal()


if __name__ == "__main__":
    # Prueba del analizador
    analizador = AnalizadorLegal()
    print(f"Modelo cargado: {'Sí' if analizador.modelo else 'No'}")
    print(f"Frases clave disponibles: {len(analizador.frases_clave)}")
