# 🌐 API Endpoints - Analizador de Sentencias

## Descripción General

La API REST del Analizador de Sentencias proporciona endpoints para análisis de documentos legales, generación de demandas y análisis predictivo. Todos los endpoints devuelven respuestas en formato JSON.

## 🔗 Base URL

- **Desarrollo**: `http://localhost:8000`
- **Producción**: `https://sentencias.onrender.com`

## 📋 Endpoints Principales

### **1. Análisis de Documentos**

#### **POST** `/upload`
Sube y analiza un documento legal.

**Request:**
```http
POST /upload
Content-Type: multipart/form-data

file: [archivo PDF/TXT/DOCX]
```

**Response:**
```json
{
  "archivo_id": "sentencia_20250115_143022_a1b2c3d4",
  "nombre_archivo": "STS_1234_2024.pdf",
  "tipo_documento": "sentencia",
  "ruta_archivo": "/sentencias/sentencia_20250115_143022_a1b2c3d4.pdf",
  "procesado": true,
  "prediccion": {
    "es_favorable": true,
    "confianza": 0.85,
    "interpretacion": "Favorable"
  },
  "frases_clave": {
    "incapacidad_permanente_parcial": {
      "total": 5,
      "frases": ["IPP", "incapacidad permanente parcial"]
    }
  },
  "argumentos": [
    {
      "tipo": "argumento_legal",
      "texto": "Por lo que se estima la demanda...",
      "confianza": 0.9
    }
  ],
  "insights_juridicos": [
    "El documento presenta argumentos sólidos a favor del caso"
  ],
  "modelo_ia": true,
  "metodo_analisis": "IA (Híbrido Avanzado)"
}
```

#### **GET** `/resultado/{archivo_id}`
Obtiene el resultado del análisis de un documento específico.

**Response:** Mismo formato que `/upload`

#### **GET** `/listar-archivos`
Lista todos los documentos disponibles.

**Response:**
```json
{
  "documentos": [
    {
      "archivo_id": "sentencia_20250115_143022_a1b2c3d4",
      "nombre_archivo": "STS_1234_2024.pdf",
      "tipo_documento": "sentencia",
      "fecha_subida": "2025-01-15T14:30:22",
      "tamaño": 1024000
    }
  ],
  "total": 1
}
```

### **2. Análisis de Discrepancias**

#### **GET** `/analisis-discrepancias/{archivo_id}`
Realiza análisis específico de discrepancias médico-legales.

**Response:**
```json
{
  "archivo_id": "sentencia_20250115_143022_a1b2c3d4",
  "analisis_discrepancias": {
    "discrepancias_detectadas": [
      {
        "tipo": "contradiccion_medica",
        "descripcion": "Inconsistencia entre informe médico y exploración",
        "severidad": "alta",
        "evidencia": "Diferencia en movilidad activa vs pasiva"
      }
    ],
    "evidencia_favorable": [
      {
        "tipo": "evidencia_estructural",
        "descripcion": "Lesión anatómica permanente",
        "severidad": "alta",
        "evidencia": "Rotura del manguito rotador confirmada por RMN"
      }
    ],
    "puntuacion_discrepancia": 75,
    "probabilidad_ipp": 0.85,
    "recomendaciones": [
      "Solicitar peritaje biomecánico complementario",
      "Documentar limitaciones funcionales objetivas"
    ]
  }
}
```

### **3. Análisis Predictivo**

#### **GET** `/api/analisis-predictivo`
Realiza análisis predictivo basado en todos los documentos disponibles.

**Response:**
```json
{
  "resumen_ejecutivo": {
    "total_documentos": 6,
    "total_frases_clave": 45,
    "categorias_identificadas": 8,
    "confianza_analisis": 0.75
  },
  "analisis_predictivo": {
    "predicciones": {
      "probabilidad_favorable": 85.0,
      "probabilidad_desfavorable": 15.0,
      "confianza_datos": 60.0,
      "explicacion_calculo": {
        "metodologia": "Análisis predictivo basado en patrones históricos",
        "datos_analizados": {
          "total_documentos": 6,
          "documentos_favorables": 6,
          "documentos_desfavorables": 0,
          "confianza_datos": 60.0
        },
        "calculo_probabilidad": {
          "metodo": "Factor de realismo jurídico aplicado",
          "probabilidad_base": "100%",
          "probabilidad_final": "85%",
          "justificacion": "Probabilidad base >90% ajustada a 85% por realismo jurídico"
        },
        "factores_aplicados": [
          "Factor de realismo jurídico: límites 15%-85%",
          "Ponderación por instancia: TS (x1.5), TSJ (x1.2)"
        ]
      }
    },
    "analisis_riesgo": {
      "riesgo_general": {
        "valor": 1464.29,
        "nivel": "alto",
        "interpretacion": "Alto riesgo legal. Se recomienda revisión exhaustiva"
      },
      "recomendaciones_riesgo": [
        "Revisar exhaustivamente todos los fundamentos jurídicos",
        "Consultar con especialista en derecho administrativo"
      ]
    }
  }
}
```

### **4. Generación de Demandas**

#### **GET** `/api/documentos`
Obtiene lista de documentos para selección en demanda.

**Response:**
```json
{
  "documentos": [
    {
      "archivo_id": "sentencia_20250115_143022_a1b2c3d4",
      "nombre_archivo": "STS_1234_2024.pdf",
      "tipo_documento": "sentencia",
      "instancia": "TS",
      "fecha_subida": "2025-01-15T14:30:22"
    }
  ]
}
```

#### **POST** `/api/extract/demanda`
Extrae metadatos para generación de demanda.

**Request:**
```json
{
  "nombres_archivo": ["STS_1234_2024.pdf", "informe_medico_001.pdf"]
}
```

**Response:**
```json
{
  "metadatos_sugeridos": {
    "informacion_demandante": {
      "nombre_completo": "Juan Pérez García",
      "dni": "12345678A",
      "domicilio": "Calle Mayor 123, Madrid"
    },
    "informacion_laboral": {
      "empresa": "Empresa de Limpieza SL",
      "profesion": "Personal de limpieza",
      "mutua": "FREMAP"
    },
    "hechos": {
      "relacion_laboral": "Trabajador de limpieza desde 2010...",
      "contingencia": "Accidente laboral el 15/03/2024...",
      "actuaciones_administrativas": "EVI, inicio IP, audiencia...",
      "cuadro_clinico": "Lesión del manguito rotador..."
    },
    "informacion_demanda": {
      "grado_principal": "IPP",
      "grado_subsidiario": "IPT",
      "base_reguladora": "1200.00",
      "indemnizacion_parcial": "24 mensualidades"
    }
  }
}
```

#### **POST** `/api/generate/demanda/docx`
Genera demanda en formato Word.

**Request:**
```json
{
  "metadatos": {
    "informacion_demandante": { ... },
    "informacion_laboral": { ... },
    "hechos": { ... },
    "informacion_demanda": { ... }
  },
  "documentos_seleccionados": ["STS_1234_2024.pdf"]
}
```

**Response:** Archivo Word descargable

#### **POST** `/api/generate/demanda/txt`
Genera demanda en formato texto.

**Request:** Mismo formato que `/docx`

**Response:** Archivo TXT descargable

### **5. Descarga de Informes**

#### **GET** `/descargar-informe/{archivo_id}`
Descarga informe completo en PDF.

**Response:** Archivo PDF descargable

#### **GET** `/descargar-informe-discrepancias/{archivo_id}`
Descarga informe de discrepancias en Word.

**Response:** Archivo DOCX descargable

## 🔧 Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| **200** | OK - Solicitud exitosa |
| **201** | Created - Recurso creado exitosamente |
| **400** | Bad Request - Solicitud malformada |
| **404** | Not Found - Recurso no encontrado |
| **422** | Unprocessable Entity - Error de validación |
| **500** | Internal Server Error - Error del servidor |

## 📝 Ejemplos de Uso

### **Ejemplo 1: Análisis Completo de Documento**

```python
import requests

# Subir documento
with open('sentencia.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/upload', files=files)
    resultado = response.json()

# Obtener análisis de discrepancias
archivo_id = resultado['archivo_id']
response = requests.get(f'http://localhost:8000/analisis-discrepancias/{archivo_id}')
discrepancias = response.json()

# Análisis predictivo
response = requests.get('http://localhost:8000/api/analisis-predictivo')
predictivo = response.json()
```

### **Ejemplo 2: Generación de Demanda**

```python
import requests

# Obtener documentos disponibles
response = requests.get('http://localhost:8000/api/documentos')
documentos = response.json()

# Extraer metadatos
nombres_archivo = [doc['nombre_archivo'] for doc in documentos['documentos']]
response = requests.post('http://localhost:8000/api/extract/demanda', 
                        json={'nombres_archivo': nombres_archivo})
metadatos = response.json()

# Generar demanda
response = requests.post('http://localhost:8000/api/generate/demanda/docx',
                        json={
                            'metadatos': metadatos['metadatos_sugeridos'],
                            'documentos_seleccionados': nombres_archivo
                        })

# Guardar archivo
with open('demanda.docx', 'wb') as f:
    f.write(response.content)
```

## 🔒 Autenticación y Seguridad

### **Headers Requeridos**
```http
Content-Type: application/json
User-Agent: AnalizadorSentencias/1.0
```

### **Límites de Rate**
- **Análisis de documentos**: 10 por minuto
- **Análisis predictivo**: 5 por minuto
- **Generación de demandas**: 3 por minuto

### **Tamaños Máximos**
- **Archivos**: 50MB
- **Texto extraído**: 1MB
- **Respuestas**: 10MB

## 🐛 Manejo de Errores

### **Formato de Error**
```json
{
  "error": "Descripción del error",
  "codigo": "ERROR_CODE",
  "detalles": {
    "campo": "valor_problematico",
    "mensaje": "Descripción específica"
  },
  "timestamp": "2025-01-15T14:30:22Z"
}
```

### **Códigos de Error Comunes**
- `FILE_TOO_LARGE`: Archivo excede el tamaño máximo
- `UNSUPPORTED_FORMAT`: Formato de archivo no soportado
- `ANALYSIS_FAILED`: Error en el análisis del documento
- `INSUFFICIENT_DATA`: Datos insuficientes para análisis predictivo
- `GENERATION_FAILED`: Error en la generación de demanda

## 📊 Métricas y Monitoreo

### **Endpoints de Monitoreo**
- `GET /health` - Estado del sistema
- `GET /metrics` - Métricas de rendimiento
- `GET /logs` - Logs del sistema

### **Métricas Disponibles**
- **Documentos procesados**: Total y por tipo
- **Tiempo de análisis**: Promedio y percentiles
- **Precisión del modelo**: Por tipo de análisis
- **Uso de recursos**: CPU, memoria, almacenamiento

---

**Nota**: Esta API está en desarrollo activo. Algunos endpoints pueden cambiar en futuras versiones. Consulte la documentación más reciente para actualizaciones.
