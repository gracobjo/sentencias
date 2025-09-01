#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path

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
    
    def _leer_archivo(self, ruta: str):
        """Lee el contenido de un archivo con manejo de errores"""
        try:
            if ruta.endswith('.txt'):
                # Intentar diferentes encodings
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        with open(ruta, 'r', encoding=encoding) as f:
                            contenido = f.read().strip()
                            print(f"✅ Archivo leído con encoding {encoding}: {len(contenido)} caracteres")
                            return contenido
                    except UnicodeDecodeError:
                        print(f"❌ Error con encoding {encoding}")
                        continue
                return None
            else:
                return "Contenido del archivo no disponible en formato de texto"
        except Exception as e:
            print(f"❌ Error leyendo archivo {ruta}: {e}")
            return None
    
    def _contar_frases_clave(self, texto: str, nombre_archivo: str):
        """Cuenta las ocurrencias de frases clave"""
        if not texto:
            print("❌ No hay texto para analizar")
            return {}
        
        print(f"🔍 Analizando texto de {len(texto)} caracteres")
        print(f"📝 Primeros 200 caracteres: {texto[:200]}...")
        
        resultados = {}
        for categoria, variantes in self.frases_clave.items():
            total = 0
            ocurrencias = []
            
            print(f"\n🔍 Buscando categoría: {categoria}")
            for variante in variantes:
                print(f"  - Buscando: '{variante}'")
                patron = re.compile(re.escape(variante), re.IGNORECASE)
                matches = list(patron.finditer(texto))
                print(f"    Encontrados: {len(matches)} matches")
                
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
                print(f"  ✅ Categoría {categoria}: {total} ocurrencias")
            else:
                print(f"  ❌ Categoría {categoria}: 0 ocurrencias")
        
        return resultados

# Probar el análisis
if __name__ == "__main__":
    print("🧪 TEST: Analizador Básico")
    
    analizador = AnalizadorBasico()
    archivo_test = "sentencias/ejemplo_sentencia.txt"
    
    print(f"📁 Archivo de prueba: {archivo_test}")
    
    # Leer archivo
    contenido = analizador._leer_archivo(archivo_test)
    if contenido:
        print(f"✅ Contenido leído: {len(contenido)} caracteres")
        
        # Analizar frases clave
        frases_encontradas = analizador._contar_frases_clave(contenido, "ejemplo_sentencia.txt")
        
        print(f"\n📊 RESULTADOS:")
        print(f"Total categorías encontradas: {len(frases_encontradas)}")
        for categoria, datos in frases_encontradas.items():
            print(f"  - {categoria}: {datos['total']} ocurrencias")
    else:
        print("❌ No se pudo leer el archivo")
