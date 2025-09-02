# 📚 API Reference

## Base URL
```
http://localhost:8000
```

## Autenticación
Actualmente no se requiere autenticación. En producción se recomienda implementar JWT o API keys.

## Endpoints

### 🏥 Health & Status

#### GET /health
Health check básico de la aplicación.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-02T12:00:00Z",
  "uptime_seconds": 3600,
  "directories": {
    "uploads": {"exists": true, "writable": true},
    "models": {"exists": true, "writable": true}
  },
  "files": {
    "models/frases_clave.json": {"exists": true, "readable": true}
  },
  "system": {
    "memory_usage_percent": 45.2,
    "cpu_usage_percent": 12.5,
    "disk_usage_percent": 67.8
  }
}
```

#### GET /status
Estado detallado de la aplicación.

**Response:**
```json
{
  "application": "Analizador de Sentencias IPP/INSS",
  "version": "2.0.0",
  "environment": "production",
  "health": { /* health check data */ },
  "timestamp": "2025-09-02T12:00:00Z"
}
```

#### GET /metrics
Métricas de Prometheus.

**Response:** Texto plano con métricas de Prometheus

### 📄 Documentos

#### GET /api/documentos
Listar todos los documentos disponibles.

**Response:**
```json
{
  "documentos": [
    {
      "nombre": "sentencia_20250828_125152_a5d084f8.pdf",
      "tamaño": 1024000,
      "fecha_modificacion": "2025-08-28T12:51:52Z",
      "instancia": "TS"
    }
  ]
}
```

#### POST /upload
Subir un nuevo documento.

**Request:**
- `file`: Archivo (multipart/form-data)
- `document_type`: Tipo de documento (form data)
- `extract_entities`: Extraer entidades (boolean)
- `analyze_arguments`: Analizar argumentos (boolean)

**Response:**
```json
{
  "resultado": {
    "frases_clave": ["incapacidad permanente"],
    "categorias": ["ipp"],
    "confianza": 0.85,
    "modelo_ia": true
  },
  "nombre_archivo": "documento.pdf",
  "archivo_id": "documento_20250902_120000_abc123.pdf",
  "tipo_documento": "sentencia",
  "timestamp": "2025-09-02T12:00:00Z"
}
```

#### DELETE /api/documentos/{nombre}
Eliminar un documento.

**Response:**
```json
{
  "mensaje": "Documento eliminado correctamente",
  "archivo": "documento.pdf"
}
```

### 🔍 Análisis

#### GET /api/analisis-predictivo
Análisis predictivo completo de todos los documentos.

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-09-02T12:00:00Z",
  "resumen_ejecutivo": {
    "total_documentos": 5,
    "total_frases_clave": 150,
    "categorias_identificadas": 8,
    "confianza_analisis": 0.87
  },
  "analisis_predictivo": {
    "tendencias": ["aumento_ipp", "estabilidad_inss"],
    "patrones": ["lesiones_hombro", "personal_limpieza"]
  },
  "insights_juridicos": {
    "recomendaciones": ["revisar_fundamentos"],
    "riesgo_legal": "medio"
  },
  "metadata": {
    "modelo_ia": true,
    "version_analisis": "2.0.0"
  }
}
```

#### POST /api/analizar
Analizar un documento específico.

**Request:**
```json
{
  "ruta_archivo": "/path/to/document.pdf"
}
```

**Response:**
```json
{
  "resultado": {
    "frases_clave": ["incapacidad permanente"],
    "categorias": ["ipp"],
    "confianza": 0.85,
    "modelo_ia": true
  }
}
```

### 📝 Frases Clave

#### GET /api/frases-clave
Obtener todas las frases clave.

**Response:**
```json
{
  "frases_clave": {
    "ipp": {
      "frases": ["incapacidad permanente parcial"],
      "total": 1
    },
    "inss": {
      "frases": ["instituto nacional"],
      "total": 1
    }
  }
}
```

#### POST /api/frases-clave
Actualizar frases clave.

**Request:**
```json
{
  "frases_clave": {
    "ipp": {
      "frases": ["incapacidad permanente parcial"],
      "total": 1
    }
  }
}
```

### 📋 Generación de Demandas

#### POST /api/demanda-base/txt
Generar demanda en formato TXT.

**Request:**
```json
{
  "documentos": ["sentencia1.pdf", "sentencia2.pdf"],
  "metadatos": {
    "nombre": "Juan Pérez",
    "dni": "12345678A",
    "domicilio": "Calle Mayor 1, Madrid",
    "grado_principal": "IPP",
    "grado_subsidiario": "IPT",
    "base_reguladora": "1200.00 €",
    "empresa": "Empresa Municipal",
    "profesion": "Personal de limpieza",
    "letrado": "Dr. García"
  }
}
```

**Response:** Archivo TXT descargable

#### POST /api/extract/demanda
Extraer metadatos de documentos para demanda.

**Request:**
```json
{
  "documentos": ["sentencia1.pdf", "sentencia2.pdf"]
}
```

**Response:**
```json
{
  "sugerencias": {
    "profesion": "Personal de limpieza",
    "empresa": "Empresa Municipal",
    "grado_principal": "IPP"
  },
  "metadatos": {
    "documentos_analizados": 2,
    "confianza": 0.85
  }
}
```

## Códigos de Error

### 400 Bad Request
```json
{
  "detail": "Error de validación: Archivo demasiado grande"
}
```

### 404 Not Found
```json
{
  "detail": "Documento no encontrado"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "file"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error interno del servidor"
}
```

## Rate Limiting
Actualmente no implementado. Se recomienda implementar en producción.

## CORS
Configurado para permitir todos los orígenes en desarrollo. En producción, especificar dominios exactos.

## Ejemplos de Uso

### cURL
```bash
# Health check
curl http://localhost:8000/health

# Listar documentos
curl http://localhost:8000/api/documentos

# Subir archivo
curl -X POST -F "file=@documento.pdf" http://localhost:8000/upload

# Análisis predictivo
curl http://localhost:8000/api/analisis-predictivo
```

### Python
```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Subir archivo
with open("documento.pdf", "rb") as f:
    files = {"file": f}
    data = {"document_type": "sentencia"}
    response = requests.post("http://localhost:8000/upload", files=files, data=data)
    print(response.json())
```

### JavaScript
```javascript
// Health check
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Subir archivo
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('document_type', 'sentencia');

fetch('http://localhost:8000/upload', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```
