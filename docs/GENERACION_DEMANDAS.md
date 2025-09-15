# 📝 Generación Inteligente de Demandas

## Descripción General

El sistema de **Generación de Demandas** utiliza inteligencia artificial para crear documentos legales profesionales basándose en el análisis previo de sentencias y casos similares. Combina plantillas jurídicas con datos específicos del caso.

## 🎯 Funcionalidades Principales

### **1. Análisis Automático de Documentos**
- **Extracción de metadatos**: Información relevante del caso
- **Identificación de patrones**: Elementos jurídicos clave
- **Clasificación de casos**: Tipo de demanda y grado de incapacidad
- **Análisis de evidencia**: Fortalezas y debilidades del caso

### **2. Generación de Contenido**
- **Hechos**: Descripción automática de la situación laboral y médica
- **Fundamentos de Derecho**: Argumentos jurídicos basados en jurisprudencia
- **Solicitudes**: Peticiones específicas según el análisis
- **Anexos**: Documentos de respaldo identificados

### **3. Personalización Inteligente**
- **Adaptación al caso**: Contenido específico según las circunstancias
- **Metadatos del demandante**: Información personal y laboral
- **Grado de incapacidad**: IPP, IPT, IPAB, GCI según análisis
- **Base reguladora**: Cálculo automático de indemnizaciones

## 🏗️ Proceso de Generación

### **Paso 1: Selección de Documentos**
```
1. Análisis de documentos disponibles
2. Identificación de casos similares
3. Selección automática de precedentes relevantes
4. Validación de coherencia jurídica
```

### **Paso 2: Extracción de Metadatos**
```python
# Información del Demandante
- Nombre completo
- DNI/NIE
- Domicilio completo
- Empresa/Entidad
- Profesión/Categoría
- Mutua de Accidentes

# Información del Caso
- Relación laboral
- Contingencia y evolución
- Actuaciones administrativas
- Cuadro clínico y limitaciones
- Grado principal y subsidiario
- Base reguladora
- Indemnización parcial
```

### **Paso 3: Generación de Contenido**

#### **HECHOS**
```markdown
PRIMERO.- Relación Laboral
[Descripción automática basada en análisis]

SEGUNDO.- Contingencia y Evolución
[Descripción médica y temporal]

TERCERO.- Actuaciones Administrativas
[Historial de procedimientos]

CUARTO.- Cuadro Clínico y Limitaciones
[Análisis médico-legal]
```

#### **FUNDAMENTOS DE DERECHO**
```markdown
PRIMERO.- [Fundamento jurídico principal]
[Argumentación basada en jurisprudencia]

SEGUNDO.- [Fundamento jurídico secundario]
[Análisis de precedentes similares]

TERCERO.- [Fundamento jurídico complementario]
[Evidencia médica y legal]
```

#### **SOLICITUDES**
```markdown
Que Vuestra Señoría tenga a bien:

PRIMERO.- [Solicitud principal]
SEGUNDO.- [Solicitud subsidiaria]
TERCERO.- [Costas procesales]
```

## 📋 Plantillas Disponibles

### **1. Demanda IPP (Incapacidad Permanente Parcial)**
- **Objetivo**: Reconocimiento de IPP
- **Indemnización**: 24 mensualidades de base reguladora
- **Elementos clave**: Lesiones permanentes, limitaciones funcionales

### **2. Demanda IPT (Incapacidad Permanente Total)**
- **Objetivo**: Reconocimiento de IPT
- **Indemnización**: Pensión vitalicia
- **Elementos clave**: Imposibilidad total para trabajo habitual

### **3. Demanda IPAB (Incapacidad Permanente Absoluta)**
- **Objetivo**: Reconocimiento de IPAB
- **Indemnización**: Pensión vitalicia aumentada
- **Elementos clave**: Imposibilidad para cualquier trabajo

### **4. Demanda GCI (Gran Invalidez)**
- **Objetivo**: Reconocimiento de GCI
- **Indemnización**: Pensión + complemento
- **Elementos clave**: Necesidad de asistencia de tercera persona

## 🔧 Configuración del Sistema

### **Parámetros de Generación**

```python
# Configuración de análisis
ANALISIS_DOCUMENTOS = True
EXTRAER_METADATOS = True
IDENTIFICAR_PATRONES = True

# Configuración de contenido
GENERAR_HECHOS = True
GENERAR_FUNDAMENTOS = True
GENERAR_SOLICITUDES = True

# Configuración de formato
FORMATO_DOCX = True
FORMATO_PDF = True
FORMATO_TXT = True
```

### **Plantillas Personalizables**

```python
PLANTILLAS = {
    "ipp": "templates/demanda_ipp.docx",
    "ipt": "templates/demanda_ipt.docx",
    "ipab": "templates/demanda_ipab.docx",
    "gci": "templates/demanda_gci.docx"
}
```

## 📊 Análisis de Calidad

### **Métricas de Evaluación**
- **Completitud**: Porcentaje de campos completados
- **Coherencia**: Consistencia entre hechos y fundamentos
- **Precisión**: Exactitud de datos extraídos
- **Relevancia**: Pertinencia de argumentos jurídicos

### **Validación Automática**
```python
def validar_demanda(demanda):
    """Valida la calidad de la demanda generada"""
    
    # Verificar completitud
    campos_requeridos = ["hechos", "fundamentos", "solicitudes"]
    completitud = verificar_completitud(demanda, campos_requeridos)
    
    # Verificar coherencia
    coherencia = verificar_coherencia(demanda)
    
    # Verificar precisión
    precision = verificar_precision(demanda)
    
    return {
        "completitud": completitud,
        "coherencia": coherencia,
        "precision": precision,
        "calidad_general": (completitud + coherencia + precision) / 3
    }
```

## 🎨 Personalización Avanzada

### **Estilos de Escritura**
- **Formal**: Lenguaje jurídico tradicional
- **Moderno**: Lenguaje más accesible
- **Técnico**: Terminología especializada
- **Personalizado**: Según preferencias del usuario

### **Elementos Opcionales**
- **Citas jurisprudenciales**: Referencias a sentencias específicas
- **Análisis económico**: Cálculos detallados de indemnizaciones
- **Anexos**: Documentos de respaldo
- **Notas al pie**: Aclaraciones adicionales

## 📤 Formatos de Exportación

### **1. Documento Word (.docx)**
- **Ventajas**: Editable, formato profesional
- **Uso**: Presentación en juzgados
- **Características**: Estilos jurídicos, numeración automática

### **2. Documento PDF (.pdf)**
- **Ventajas**: Formato fijo, fácil de compartir
- **Uso**: Archivo definitivo, presentación digital
- **Características**: Firmas digitales, protección de contenido

### **3. Texto Plano (.txt)**
- **Ventajas**: Compatible con cualquier sistema
- **Uso**: Integración con otros sistemas
- **Características**: Formato simple, fácil de procesar

## 🔍 Casos de Uso Específicos

### **Caso 1: Accidente Laboral con Lesión de Hombro**
```
Análisis: Rotura del manguito rotador
Grado: IPP
Base reguladora: 1.200€
Indemnización: 24 mensualidades = 28.800€
Argumentos: Art. 194.2 LGSS, jurisprudencia TS
```

### **Caso 2: Enfermedad Profesional**
```
Análisis: Enfermedad por exposición laboral
Grado: IPT
Base reguladora: 1.500€
Indemnización: Pensión vitalicia
Argumentos: Art. 195 LGSS, prevención de riesgos
```

### **Caso 3: Recaída de Incapacidad**
```
Análisis: Agravamiento de lesiones previas
Grado: IPAB
Base reguladora: 1.800€
Indemnización: Pensión vitalicia aumentada
Argumentos: Art. 196 LGSS, evolución del cuadro
```

## ⚠️ Limitaciones y Consideraciones

### **Limitaciones Técnicas**
- **Dependencia de datos**: Calidad depende de documentos analizados
- **Contexto específico**: Cada caso puede tener circunstancias únicas
- **Actualización normativa**: Cambios legales pueden afectar plantillas
- **Validación humana**: Requiere revisión profesional

### **Recomendaciones de Uso**
- **Revisar contenido**: Siempre validar antes de presentar
- **Personalizar según caso**: Adaptar a circunstancias específicas
- **Mantener actualizado**: Revisar plantillas periódicamente
- **Consultar especialistas**: Para casos complejos

## 🚀 Mejoras Futuras

### **Funcionalidades Planificadas**
- [ ] Integración con bases de datos jurídicas
- [ ] Análisis de jurisprudencia en tiempo real
- [ ] Generación de recursos y alegaciones
- [ ] Análisis de costos procesales
- [ ] Integración con sistemas de gestión

### **Investigación en Curso**
- [ ] Generación de contenido con GPT
- [ ] Análisis de sentimientos en resoluciones
- [ ] Predicción de tiempos de resolución
- [ ] Análisis de éxito por tipo de demanda

---

**Nota**: Las demandas generadas son plantillas que requieren revisión y personalización profesional. Siempre consulte con un abogado especializado antes de presentar documentos legales.
