# Sistema de Ponderación del Análisis de Riesgo Legal

## Resumen Ejecutivo

El sistema de análisis de riesgo legal utiliza una **fórmula ponderada** que asigna diferentes pesos a las categorías de frases clave según su criticidad legal. El valor final se multiplica por un factor de instancia que refleja la autoridad del tribunal emisor.

## Fórmula Principal

```
Riesgo_Total = (Categorías_Alto × 3) + (Categorías_Medio × 2) + (Categorías_Bajo × 1) × Factor_Instancia
```

## Clasificación de Categorías por Nivel de Riesgo

### 1. Categorías de ALTO RIESGO (Peso × 3)

Estas categorías indican aspectos críticos que requieren atención especializada:

- **`reclamacion_administrativa`**: Procedimientos administrativos complejos
- **`procedimiento_legal`**: Aspectos procesales críticos
- **`fundamentos_juridicos`**: Base legal del caso

**Justificación del peso × 3**: Estas categorías representan los aspectos más críticos del caso legal, donde errores pueden tener consecuencias graves.

### 2. Categorías de RIESGO MEDIO (Peso × 2)

Aspectos importantes pero con menor criticidad:

- **`lesiones_permanentes`**: Evaluación médica-jurídica
- **`accidente_laboral`**: Contexto del accidente
- **`prestaciones`**: Aspectos económicos

**Justificación del peso × 2**: Importantes para el caso pero con menor impacto en la resolución final.

### 3. Categorías de RIESGO BAJO (Peso × 1)

Información contextual y de soporte:

- **`inss`**: Referencias institucionales
- **`personal_limpieza`**: Categoría laboral específica
- **`lesiones_hombro`**: Lesión específica

**Justificación del peso × 1**: Información de contexto que no determina directamente el resultado.

## Factor de Instancia

El factor de instancia refleja la autoridad y precedente legal del tribunal:

### Cálculo del Factor

```python
def calcular_factor_instancia(resultados_por_archivo):
    total_documentos = len(documentos_válidos)
    ts_count = contar_documentos_ts()
    tsj_count = contar_documentos_tsj()
    
    ratio_ts = ts_count / total_documentos
    ratio_tsj = tsj_count / total_documentos
    
    factor = 1.0 + (0.5 × ratio_ts) + (0.2 × ratio_tsj)
    return factor
```

### Valores del Factor

- **Tribunal Supremo (TS)**: +0.5 (factor máximo ~1.5)
- **Tribunal Superior de Justicia (TSJ)**: +0.2 (factor máximo ~1.2)
- **Otros tribunales**: +0.0 (factor = 1.0)

**Justificación**: Los documentos de instancias superiores tienen mayor precedente legal y autoridad, por lo que requieren mayor atención.

## Umbrales de Clasificación

### Niveles de Riesgo

- **ALTO**: > 100 puntos
- **MEDIO**: 50-100 puntos
- **BAJO**: < 50 puntos

### Justificación de Umbrales

Los umbrales se basan en análisis empírico de casos legales:

- **> 100 puntos**: Casos que requieren revisión exhaustiva y posible consulta especializada
- **50-100 puntos**: Casos que requieren atención especial en áreas críticas
- **< 50 puntos**: Casos con procedimiento estándar

## Ejemplo Práctico

### Datos de Entrada
```
Categorías Alto: 18 apariciones
Categorías Medio: 38 apariciones  
Categorías Bajo: 113 apariciones
Factor Instancia: 1.33 (TSJ)
```

### Cálculo Paso a Paso

1. **Cálculo base**:
   ```
   Riesgo_Base = (18 × 3) + (38 × 2) + (113 × 1)
   Riesgo_Base = 54 + 76 + 113 = 243
   ```

2. **Aplicación del factor de instancia**:
   ```
   Riesgo_Final = 243 × 1.33 = 324
   ```

3. **Clasificación**:
   ```
   324 > 100 → RIESGO ALTO
   ```

## Implementación Técnica

### Código Fuente

```python
def analizar_riesgo_legal(ranking_global, resultados_por_archivo):
    # Definir categorías por nivel
    categorias_riesgo = {
        "alto": ["reclamacion_administrativa", "procedimiento_legal", "fundamentos_juridicos"],
        "medio": ["lesiones_permanentes", "accidente_laboral", "prestaciones"],
        "bajo": ["inss", "personal_limpieza", "lesiones_hombro"]
    }
    
    # Calcular factor de instancia
    factor_instancia = calcular_factor_instancia(resultados_por_archivo)
    
    # Calcular riesgo por nivel
    riesgo_general = (
        analisis_riesgo.get("alto", {}).get("total_apariciones", 0) * 3 +
        analisis_riesgo.get("medio", {}).get("total_apariciones", 0) * 2 +
        analisis_riesgo.get("bajo", {}).get("total_apariciones", 0)
    ) * factor_instancia
    
    # Clasificar nivel
    nivel_riesgo = "alto" if riesgo_general > 100 else "medio" if riesgo_general > 50 else "bajo"
    
    return {
        "valor": riesgo_general,
        "nivel": nivel_riesgo,
        "factor_instancia": factor_instancia
    }
```

## Validación y Calibración

### Métodos de Validación

1. **Análisis retrospectivo**: Comparación con casos históricos
2. **Validación experta**: Revisión por especialistas legales
3. **Ajuste iterativo**: Refinamiento basado en feedback

### Parámetros Ajustables

- **Pesos de categorías**: Modificables según evolución jurisprudencial
- **Umbrales de clasificación**: Ajustables según experiencia
- **Factor de instancia**: Calibrable según autoridad de tribunales

## Limitaciones y Consideraciones

### Limitaciones del Modelo

1. **Dependencia de frases clave**: El modelo depende de la calidad del diccionario de frases
2. **Contexto limitado**: No considera el contexto completo del caso
3. **Evolución legal**: Requiere actualización periódica

### Mejoras Futuras

1. **Análisis semántico**: Incorporar análisis de contexto
2. **Machine Learning**: Modelos predictivos más sofisticados
3. **Integración jurisprudencial**: Incorporar bases de datos legales

## Conclusiones

El sistema de ponderación proporciona una **métrica objetiva** para evaluar la complejidad y criticidad de casos legales, combinando:

- **Frecuencia de términos críticos** (pesos diferenciados)
- **Autoridad del tribunal** (factor de instancia)
- **Umbrales empíricos** (clasificación por niveles)

Esta metodología permite una **evaluación consistente y escalable** del riesgo legal, facilitando la priorización de casos y la asignación de recursos especializados.
