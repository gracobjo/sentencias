# Documentación del Sistema de Ponderación del Riesgo Legal

## Índice de Documentación

Esta documentación explica cómo se calcula la ponderación del análisis de riesgo legal en el sistema de análisis de sentencias IPP/INSS.

### 📋 Documentos Principales

1. **[ANALISIS_RIESGO_PONDERACION.md](./ANALISIS_RIESGO_PONDERACION.md)**
   - Resumen ejecutivo del sistema
   - Fórmula principal y justificación
   - Clasificación de categorías por nivel de riesgo
   - Factor de instancia y umbrales de clasificación
   - Implementación técnica y validación

2. **[FLUJO_PONDERACION.md](./FLUJO_PONDERACION.md)**
   - Diagrama de flujo del proceso
   - Proceso detallado paso a paso
   - Tabla de ejemplo con cálculos
   - Código de implementación
   - Casos de prueba y validación

3. **[CONFIGURACION_PONDERACION.md](./CONFIGURACION_PONDERACION.md)**
   - Parámetros del sistema (JSON)
   - Justificación de cada parámetro
   - Métodos de calibración
   - Validación del modelo
   - Mantenimiento del sistema

4. **[EJEMPLO_PRACTICO_PONDERACION.md](./EJEMPLO_PRACTICO_PONDERACION.md)**
   - Caso de estudio real
   - Cálculo paso a paso
   - Desglose detallado
   - Comparación con otros casos
   - Validación del resultado

## 🎯 Resumen Ejecutivo

### Fórmula Principal
```
Riesgo_Total = (Categorías_Alto × 3) + (Categorías_Medio × 2) + (Categorías_Bajo × 1) × Factor_Instancia
```

### Clasificación de Riesgo
- **ALTO**: > 100 puntos
- **MEDIO**: 50-100 puntos  
- **BAJO**: < 50 puntos

### Factor de Instancia
- **Tribunal Supremo**: +0.5 (factor ~1.5)
- **Tribunal Superior**: +0.2 (factor ~1.2)
- **Otros**: +0.0 (factor 1.0)

## 📊 Ejemplo Práctico

### Datos de Entrada
- **Alto riesgo**: 18 apariciones
- **Medio riesgo**: 38 apariciones
- **Bajo riesgo**: 113 apariciones
- **Factor instancia**: 1.3 (TSJ)

### Cálculo
```
Riesgo_Base = (18 × 3) + (38 × 2) + (113 × 1) = 243
Riesgo_Final = 243 × 1.3 = 324
Clasificación: 324 > 100 → RIESGO ALTO
```

## 🔧 Implementación Técnica

### Archivos de Código
- `backend/analisis_predictivo.py` - Función `analizar_riesgo_legal()`
- `app.py` - Endpoint `/api/analisis-predictivo`

### Parámetros Configurables
- Pesos de categorías (3, 2, 1)
- Factores de instancia (0.5, 0.2, 0.0)
- Umbrales de clasificación (100, 50, 0)

## 📈 Validación y Calibración

### Métricas de Validación
- **Precisión**: >85% en clasificación
- **Consistencia**: <10% de variación
- **Relevancia**: Correlación >0.7 con resultados reales

### Mantenimiento
- **Diccionario de frases**: Actualización mensual
- **Parámetros**: Revisión trimestral
- **Validación**: Evaluación semestral

## 🎯 Casos de Uso

### Para Desarrolladores
- Entender la lógica del sistema
- Modificar parámetros de ponderación
- Implementar mejoras al algoritmo

### Para Usuarios Legales
- Interpretar resultados del análisis
- Entender recomendaciones del sistema
- Validar clasificaciones de riesgo

### Para Administradores
- Configurar parámetros del sistema
- Monitorear efectividad del modelo
- Calibrar según evolución jurisprudencial

## 📚 Referencias

### Documentación Técnica
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Logging](https://docs.python.org/3/library/logging.html)

### Contexto Legal
- Ley General de la Seguridad Social (LGSS)
- Jurisprudencia del Tribunal Supremo
- Procedimientos administrativos INSS

## 🔄 Actualizaciones

### Versión Actual: 2.0.0
- Sistema de ponderación implementado
- Factor de instancia añadido
- Validación del modelo completada

### Próximas Versiones
- Análisis semántico avanzado
- Machine learning predictivo
- Integración con bases de datos legales

---

**Última actualización**: Enero 2025  
**Mantenido por**: Equipo de Desarrollo Legal Tech  
**Contacto**: [Información de contacto del equipo]
