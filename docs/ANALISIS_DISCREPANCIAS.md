# Análisis de Discrepancias Médicas-Legales

## Descripción

El módulo de análisis de discrepancias médicas-legales es una funcionalidad avanzada que identifica automáticamente contradicciones entre diagnósticos médicos y calificaciones legales, especialmente en casos de **Lesiones Permanentes No Incapacitantes (LPNI)** vs **Incapacidad Permanente Parcial (IPP)**.

## Características Principales

### 🔍 Detección Automática de Discrepancias

El sistema identifica automáticamente:

1. **Lesiones Graves vs Calificación LPNI**
   - Rotura completa del manguito rotador
   - Cirugía reconstructiva con anclajes
   - Lesiones estructurales graves confirmadas por RMN

2. **Limitaciones Funcionales vs Alta Médica**
   - Flexión activa limitada (<90°)
   - Fuerza insuficiente para vencer la gravedad
   - Discinesia escapular y atrofia muscular

3. **Evidencia Objetiva vs Conclusión Subjetiva**
   - Informes de biomecánica vs síntomas menores
   - Datos objetivos vs conclusiones subjetivas

### ⚖️ Argumentos Jurídicos Generados

El sistema genera automáticamente argumentos basados en:

- **Art. 194.2 LGSS**: Criterio de disminución ≥33% en rendimiento
- **Profesión específica**: Requisitos funcionales de limpiadora
- **Evidencia médica**: Informes técnicos y objetivaciones

### 🎯 Recomendaciones de Defensa

Proporciona recomendaciones específicas:

- Enfoque en contradicciones detectadas
- Utilización de evidencia objetiva
- Argumentos jurídicos estructurados
- Acciones recomendadas por prioridad

## Cómo Usar

### 1. Acceso desde la Interfaz Principal

1. Ve a la página principal del analizador
2. En la lista de documentos, busca el archivo que deseas analizar
3. Haz clic en el botón rojo con icono de búsqueda (🔍)
4. Se abrirá una nueva pestaña con el análisis de discrepancias

### 2. Interpretación de Resultados

#### Resumen Ejecutivo
- **Discrepancias Detectadas**: Número de contradicciones encontradas
- **Elementos de Evidencia**: Puntos favorables para IPP
- **Puntuación de Discrepancia**: Score de 0-100
- **Probabilidad de IPP**: Porcentaje de probabilidad

#### Secciones del Análisis

1. **Discrepancias Detectadas** (🔴)
   - Contradicciones específicas encontradas
   - Severidad de cada discrepancia
   - Argumentos jurídicos asociados

2. **Evidencia Favorable** (🟢)
   - Elementos que apoyan IPP
   - Relevancia de cada elemento
   - Argumentos de soporte

3. **Argumentos Jurídicos** (🔵)
   - Argumentos estructurados para la defensa
   - Basados en legislación vigente
   - Evidencia de soporte incluida

4. **Recomendaciones de Defensa** (🟡)
   - Estrategias específicas
   - Acciones recomendadas
   - Prioridades establecidas

5. **Contradicciones Internas** (⚫)
   - Inconsistencias dentro del informe
   - Texto específico detectado
   - Argumentos de debilidad

## Ejemplo Práctico

### Caso: Informe de Mutua con LPNI

**Discrepancias Detectadas:**
- ✅ Lesión estructural grave (rotura completa supraespinoso)
- ✅ Cirugía reconstructiva con anclajes
- ✅ Limitaciones activas persistentes
- ✅ Informe de biomecánica objetivo

**Argumentos Generados:**
- Art. 194.2 LGSS: Disminución ≥33% en rendimiento
- Profesión de limpiadora requiere movimientos por encima del hombro
- Limitación activa <90° impide trabajo habitual
- Evidencia objetiva prevalece sobre conclusiones subjetivas

**Recomendaciones:**
- Enfocar defensa en contradicciones detectadas
- Presentar evidencia objetiva como prueba principal
- Argumentar incompatibilidad LPNI con lesiones graves

## Patrones Detectados

### Lesiones Graves
- `rotura de espesor completo`
- `retracción fibrilar [X] mm`
- `tenopatía severa`
- `artropatía acromioclavicular severa`
- `anclajes corkscrew`
- `cirugía reconstructiva`

### Limitaciones Funcionales
- `flexión activa solo [X]°`
- `abducción activa [X]°`
- `fuerza insuficiente para vencer la gravedad`
- `balance muscular [X]/5`
- `fuerza de garra solo [X] kg`
- `discinesia escapular`
- `atrofia periescapular`

### Contradicciones Internas
- `no presenta limitación importante.*limitación activa`
- `no impide actividades.*limitación activa`
- `alta médica.*limitaciones persistentes`
- `recuperación.*secuelas permanentes`

## Configuración Técnica

### Archivos Principales
- `backend/analisis_discrepancias.py`: Módulo principal
- `templates/analisis_discrepancias.html`: Interfaz web
- `app.py`: Ruta `/analisis-discrepancias/{archivo_id}`

### Integración
El módulo se integra automáticamente en el análisis principal:
- Se ejecuta en cada análisis de documento
- Los resultados se incluyen en `analisis_discrepancias`
- Accesible desde la interfaz principal

## Limitaciones y Consideraciones

### Limitaciones Actuales
- Optimizado para casos de hombro/manguito rotador
- Patrones específicos para profesión de limpiadora
- Requiere texto extraído correctamente del PDF

### Mejoras Futuras
- Expansión a otras lesiones (columna, rodilla, etc.)
- Más profesiones específicas
- Integración con modelos de IA más avanzados
- Análisis de jurisprudencia específica

## Soporte y Desarrollo

Para reportar problemas o solicitar mejoras:
1. Revisar los logs de la aplicación
2. Verificar que el PDF se extrae correctamente
3. Comprobar que los patrones coinciden con el caso específico

El sistema está diseñado para ser extensible y puede adaptarse a nuevos tipos de casos y patrones específicos.

