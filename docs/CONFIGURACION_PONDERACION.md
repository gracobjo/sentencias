# Configuración del Sistema de Ponderación

## Parámetros del Sistema

### Pesos por Nivel de Riesgo

```json
{
  "pesos_riesgo": {
    "alto": 3,
    "medio": 2,
    "bajo": 1
  }
}
```

### Categorías por Nivel

```json
{
  "categorias_riesgo": {
    "alto": [
      "reclamacion_administrativa",
      "procedimiento_legal", 
      "fundamentos_juridicos"
    ],
    "medio": [
      "lesiones_permanentes",
      "accidente_laboral",
      "prestaciones"
    ],
    "bajo": [
      "inss",
      "personal_limpieza",
      "lesiones_hombro"
    ]
  }
}
```

### Factores de Instancia

```json
{
  "factores_instancia": {
    "tribunal_supremo": 0.5,
    "tribunal_superior": 0.2,
    "otros": 0.0
  }
}
```

### Umbrales de Clasificación

```json
{
  "umbrales_riesgo": {
    "alto": 100,
    "medio": 50,
    "bajo": 0
  }
}
```

## Justificación de Parámetros

### Pesos de Categorías

#### Alto Riesgo (×3)
- **Justificación**: Aspectos críticos que determinan el resultado del caso
- **Impacto**: Errores en estas áreas pueden ser fatales para el caso
- **Ejemplos**: Procedimientos administrativos, fundamentos jurídicos

#### Medio Riesgo (×2)  
- **Justificación**: Aspectos importantes pero con menor impacto directo
- **Impacto**: Importantes para el contexto pero no determinantes
- **Ejemplos**: Evaluación médica, contexto del accidente

#### Bajo Riesgo (×1)
- **Justificación**: Información contextual y de soporte
- **Impacto**: Necesaria para el contexto pero no crítica
- **Ejemplos**: Referencias institucionales, categorías laborales

### Factores de Instancia

#### Tribunal Supremo (+0.5)
- **Justificación**: Máxima autoridad judicial
- **Precedente**: Vinculante para todos los tribunales
- **Complejidad**: Casos de máxima complejidad legal

#### Tribunal Superior (+0.2)
- **Justificación**: Alta autoridad regional
- **Precedente**: Vinculante para tribunales de la región
- **Complejidad**: Casos de alta complejidad

#### Otros Tribunales (+0.0)
- **Justificación**: Autoridad estándar
- **Precedente**: Limitado al caso específico
- **Complejidad**: Casos de complejidad estándar

### Umbrales de Clasificación

#### Alto Riesgo (>100)
- **Criterio**: Casos que requieren atención especializada
- **Recursos**: Revisión exhaustiva, consulta especialista
- **Tiempo**: Procesamiento prioritario

#### Medio Riesgo (50-100)
- **Criterio**: Casos que requieren atención especial
- **Recursos**: Revisión detallada, monitoreo
- **Tiempo**: Procesamiento estándar

#### Bajo Riesgo (<50)
- **Criterio**: Casos de procesamiento estándar
- **Recursos**: Revisión rutinaria
- **Tiempo**: Procesamiento normal

## Calibración del Sistema

### Método de Calibración

1. **Análisis Histórico**: Revisar casos pasados y sus resultados
2. **Validación Experta**: Consulta con especialistas legales
3. **Ajuste Iterativo**: Refinamiento basado en feedback
4. **Monitoreo Continuo**: Seguimiento de efectividad

### Parámetros Ajustables

#### Pesos de Categorías
- **Frecuencia de ajuste**: Trimestral
- **Criterio**: Evolución jurisprudencial
- **Proceso**: Análisis de tendencias legales

#### Factores de Instancia
- **Frecuencia de ajuste**: Anual
- **Criterio**: Cambios en la estructura judicial
- **Proceso**: Revisión de autoridad de tribunales

#### Umbrales de Clasificación
- **Frecuencia de ajuste**: Semestral
- **Criterio**: Efectividad del sistema
- **Proceso**: Análisis de precisión predictiva

## Validación del Modelo

### Métricas de Validación

#### Precisión
- **Objetivo**: >85% de precisión en clasificación
- **Método**: Comparación con evaluación experta
- **Frecuencia**: Mensual

#### Consistencia
- **Objetivo**: <10% de variación entre evaluaciones
- **Método**: Análisis de casos duplicados
- **Frecuencia**: Semanal

#### Relevancia
- **Objetivo**: Correlación >0.7 con resultados reales
- **Método**: Análisis retrospectivo de casos
- **Frecuencia**: Trimestral

### Casos de Prueba

#### Caso Tipo 1: Bajo Riesgo
```
Entrada: 2 alto, 5 medio, 20 bajo
Cálculo: (2×3) + (5×2) + (20×1) = 36
Resultado: BAJO (<50)
```

#### Caso Tipo 2: Medio Riesgo
```
Entrada: 8 alto, 15 medio, 25 bajo
Cálculo: (8×3) + (15×2) + (25×1) = 79
Resultado: MEDIO (50-100)
```

#### Caso Tipo 3: Alto Riesgo
```
Entrada: 15 alto, 25 medio, 30 bajo
Cálculo: (15×3) + (25×2) + (30×1) = 125
Resultado: ALTO (>100)
```

## Mantenimiento del Sistema

### Actualizaciones Regulares

#### Diccionario de Frases Clave
- **Frecuencia**: Mensual
- **Proceso**: Revisión de nuevas jurisprudencias
- **Responsable**: Equipo legal

#### Parámetros de Ponderación
- **Frecuencia**: Trimestral
- **Proceso**: Análisis de efectividad
- **Responsable**: Equipo técnico

#### Validación del Modelo
- **Frecuencia**: Semestral
- **Proceso**: Evaluación completa del sistema
- **Responsable**: Equipo multidisciplinario

### Monitoreo Continuo

#### Alertas del Sistema
- **Cambios significativos**: >20% en distribución de riesgo
- **Errores de clasificación**: Casos mal clasificados
- **Rendimiento**: Degradación de métricas

#### Reportes Regulares
- **Diario**: Resumen de casos procesados
- **Semanal**: Análisis de tendencias
- **Mensual**: Reporte de efectividad
- **Trimestral**: Evaluación completa del sistema
