# 🧠 Entrenamiento de Modelos de IA - Guía Completa

## 📋 Descripción General

Este documento explica cómo entrenar y gestionar los modelos de inteligencia artificial utilizados en el sistema de análisis de sentencias jurídicas. Los modelos se almacenan como archivos `.pkl` (pickle) y utilizan técnicas de machine learning para clasificar documentos legales como favorables o desfavorables.

## 🏗️ Arquitectura de Modelos

### 📁 Estructura de Archivos

```
models/
├── modelo_legal.pkl          # Modelo TF-IDF + Logistic Regression
├── modelo_legal_sbert.pkl    # Modelo Sentence-BERT + Clasificador
├── labels.json              # Etiquetas manuales (opcional)
├── frases_clave.json        # Configuración de frases clave
└── README.md               # Documentación básica
```

### 🔧 Tipos de Modelos

#### 1. **Modelo TF-IDF (`modelo_legal.pkl`)**

**🎯 Tecnología:**
- **Vectorizador**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Clasificador**: Logistic Regression
- **Entrada**: Texto plano
- **Salida**: 0 (desfavorable) o 1 (favorable)

**📊 Estructura del archivo:**
```python
{
    'modelo': 'scikit-learn',
    'vectorizador': TfidfVectorizer,
    'clasificador': LogisticRegression
}
```

**✅ Ventajas:**
- Rápido de entrenar y ejecutar
- Funciona bien con textos jurídicos
- Requiere menos recursos computacionales
- Interpretable y explicable

#### 2. **Modelo SBERT (`modelo_legal_sbert.pkl`)**

**🎯 Tecnología:**
- **Encoder**: Sentence-Transformers (`all-MiniLM-L6-v2`)
- **Clasificador**: Logistic Regression
- **Entrada**: Embeddings semánticos
- **Salida**: 0 (desfavorable) o 1 (favorable)

**📊 Estructura del archivo:**
```python
{
    'encoder_name': 'all-MiniLM-L6-v2',
    'clasificador': LogisticRegression
}
```

**✅ Ventajas:**
- Comprensión semántica avanzada
- Mejor rendimiento con textos complejos
- Captura relaciones contextuales
- Más preciso en casos ambiguos

## 🚀 Proceso de Entrenamiento

### 📝 Preparación de Datos

#### 1. **Directorio de Documentos**

El sistema busca documentos en:
- `sentencias/` - Documentos de ejemplo y casos de referencia
- `uploads/` - Documentos subidos por usuarios

#### 2. **Formatos Soportados**

- **PDF**: Procesado con PyPDF2
- **TXT**: Texto plano
- **DOCX**: Procesamiento básico

#### 3. **Requisitos de Calidad**

- **Longitud mínima**: 50 caracteres
- **Encoding**: UTF-8, Latin-1, CP1252
- **Calidad**: Texto bien estructurado y legible

### 🏷️ Sistema de Etiquetado

#### 1. **Etiquetado Manual (Recomendado)**

Crear archivo `models/labels.json`:
```json
{
  "documento1.pdf": 1,
  "documento2.pdf": 0,
  "documento3.pdf": 1,
  "sentencia_favorable_2024.pdf": 1,
  "resolucion_desfavorable.pdf": 0
}
```

**Valores:**
- `1` = Favorable (procedente, estimado, concedido)
- `0` = Desfavorable (desestimado, rechazado, denegado)

#### 2. **Etiquetado Débil Automático**

Si no hay etiquetas manuales, el sistema usa palabras clave:

**✅ Palabras Positivas (Favorable):**
```python
PALABRAS_POSITIVAS = [
    "procedente",
    "estimamos",
    "estimamos procedente",
    "accedemos",
    "concedemos",
    "reconocemos",
    "favorable",
    "fundada"
]
```

**❌ Palabras Negativas (Desfavorable):**
```python
PALABRAS_NEGATIVAS = [
    "desestimamos",
    "infundada",
    "rechazamos",
    "denegamos",
    "desfavorable",
    "no procedente"
]
```

### 🔧 Comandos de Entrenamiento

#### 1. **Entrenamiento Básico**

```bash
# Entrenar modelo TF-IDF
python src/backend/train_model.py

# Entrenar modelo SBERT
python src/backend/train_embeddings.py
```

#### 2. **Entrenamiento con Etiquetas**

```bash
# 1. Crear archivo de etiquetas
echo '{"documento1.pdf": 1, "documento2.pdf": 0}' > models/labels.json

# 2. Ejecutar entrenamiento
python src/backend/train_model.py
python src/backend/train_embeddings.py
```

#### 3. **Entrenamiento Programático**

```python
from pathlib import Path
from src.backend.train_model import train_and_save
from src.backend.train_embeddings import train_and_save as train_sbert

# Configurar directorios
BASE_DIR = Path("sentencias")
UPLOADS_DIR = Path("uploads")
MODELS_DIR = Path("models")
LABELS = MODELS_DIR / "labels.json"

# Entrenar modelo TF-IDF
result_tfidf = train_and_save(BASE_DIR, UPLOADS_DIR, MODELS_DIR, LABELS)
print(f"Modelo TF-IDF: {result_tfidf}")

# Entrenar modelo SBERT
result_sbert = train_sbert(BASE_DIR, UPLOADS_DIR, MODELS_DIR, LABELS)
print(f"Modelo SBERT: {result_sbert}")
```

## 📊 Proceso Técnico Detallado

### 🔤 Vectorización TF-IDF

```python
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),  # Unigramas y bigramas
    min_df=1,            # Frecuencia mínima de términos
    max_df=0.95         # Frecuencia máxima (elimina muy comunes)
)
```

**Parámetros explicados:**
- `ngram_range=(1, 2)`: Captura palabras individuales y pares de palabras
- `min_df=1`: Incluye términos que aparecen al menos una vez
- `max_df=0.95`: Excluye términos que aparecen en más del 95% de documentos

### 🧠 Vectorización SBERT

```python
encoder = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = encoder.encode(
    texts, 
    batch_size=16, 
    show_progress_bar=False, 
    normalize_embeddings=True
)
```

**Parámetros explicados:**
- `all-MiniLM-L6-v2`: Modelo pre-entrenado optimizado para español
- `batch_size=16`: Procesa 16 documentos por lote
- `normalize_embeddings=True`: Normaliza vectores para mejor rendimiento

### 📈 Entrenamiento del Clasificador

```python
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)
```

**Validación automática:**
- Split 80/20 (entrenamiento/test)
- Estratificación por clases
- Reporte de clasificación automático

## 🎯 Evaluación y Métricas

### 📊 Métricas de Calidad

**🎯 Objetivos de rendimiento:**
- **Precisión**: > 80%
- **Recall**: > 75%
- **F1-Score**: > 0.8
- **Tiempo de respuesta**: < 1 segundo

### 📈 Reporte de Clasificación

El sistema genera automáticamente un reporte como:

```
              precision    recall  f1-score   support

           0       0.85      0.78      0.81        18
           1       0.82      0.88      0.85        17

    accuracy                           0.83        35
   macro avg       0.83      0.83      0.83        35
weighted avg       0.83      0.83      0.83        35
```

### 🧪 Testing del Modelo

```python
import pickle

# Cargar modelo
with open('models/modelo_legal.pkl', 'rb') as f:
    modelo = pickle.load(f)

# Probar predicción
texto_prueba = "Estimamos procedente la reclamación..."
vector = modelo['vectorizador'].transform([texto_prueba])
prediccion = modelo['clasificador'].predict(vector)
probabilidad = modelo['clasificador'].predict_proba(vector)

print(f"Predicción: {prediccion[0]}")  # 0 o 1
print(f"Probabilidad: {probabilidad[0]}")  # [prob_desfavorable, prob_favorable]
```

## 🔄 Sistema de Fallback

### 🛡️ Estrategia de Respaldo

Si los modelos no están disponibles, el sistema usa automáticamente:

1. **Análisis basado en reglas**
2. **Patrones de frases clave**
3. **Predicción por palabras clave**
4. **Extracción de argumentos legales**

### 🔧 Implementación del Fallback

```python
def _cargar_modelo(self):
    """Carga el modelo con fallback automático"""
    try:
        # Intentar cargar modelo TF-IDF
        with open(self.modelo_path, 'rb') as f:
            modelo_data = pickle.load(f)
            self.modelo = modelo_data.get('modelo')
            self.vectorizador = modelo_data.get('vectorizador')
            self.clasificador = modelo_data.get('clasificador')
    except Exception as e:
        logger.warning(f"Error cargando modelo: {e}")
        # Usar análisis basado en reglas
        self._crear_modelo_basico()
```

## 🚀 Mejores Prácticas

### 📚 Preparación de Datos

1. **Cantidad**: Mínimo 20-30 documentos por clase
2. **Balance**: Mismo número de casos favorables/desfavorables
3. **Calidad**: Documentos bien estructurados y legibles
4. **Diversidad**: Variedad de tipos de casos y tribunales

### 🏷️ Etiquetado

1. **Precisión**: Revisar manualmente las etiquetas automáticas
2. **Consistencia**: Usar criterios uniformes de clasificación
3. **Actualización**: Mantener etiquetas actualizadas
4. **Validación**: Verificar etiquetas con expertos jurídicos

### 🔄 Reentrenamiento

1. **Frecuencia**: Reentrenar con nuevos documentos
2. **Monitoreo**: Evaluar rendimiento en producción
3. **Versionado**: Mantener versiones anteriores de modelos
4. **Testing**: Probar nuevos modelos antes de desplegar

### 🛡️ Seguridad y Privacidad

1. **Anonimización**: Eliminar datos personales antes del entrenamiento
2. **Control de acceso**: Limitar acceso a modelos entrenados
3. **Auditoría**: Registrar cambios en modelos
4. **Backup**: Mantener copias de seguridad de modelos

## 📋 Checklist de Entrenamiento

### ✅ Antes del Entrenamiento

- [ ] Documentos anonimizados y sin datos sensibles
- [ ] Etiquetas manuales creadas y verificadas
- [ ] Balance de clases (favorable/desfavorable)
- [ ] Documentos de calidad suficiente (>50 caracteres)
- [ ] Directorios `sentencias/` y `uploads/` configurados

### ✅ Durante el Entrenamiento

- [ ] Ejecutar ambos scripts de entrenamiento
- [ ] Verificar métricas de rendimiento
- [ ] Revisar reportes de clasificación
- [ ] Probar modelos con casos de ejemplo
- [ ] Validar tiempo de respuesta

### ✅ Después del Entrenamiento

- [ ] Verificar archivos `.pkl` generados
- [ ] Probar predicciones en casos nuevos
- [ ] Documentar cambios en modelos
- [ ] Hacer backup de modelos anteriores
- [ ] Actualizar documentación

## 🚨 Solución de Problemas

### ❌ Problemas Comunes

#### 1. **Error: "No hay documentos suficientes"**

**Causa**: Menos de 2 documentos en directorios
**Solución**: Agregar más documentos o verificar rutas

#### 2. **Error: "Todas las etiquetas son iguales"**

**Causa**: Solo casos favorables o desfavorables
**Solución**: Agregar casos del otro tipo o revisar etiquetado

#### 3. **Error: "Modelo muy pequeño"**

**Causa**: Modelo SBERT incompleto o corrupto
**Solución**: Reentrenar modelo SBERT

#### 4. **Bajo rendimiento del modelo**

**Causas posibles**:
- Pocos datos de entrenamiento
- Etiquetas incorrectas
- Documentos de baja calidad
- Desbalance de clases

**Soluciones**:
- Aumentar datos de entrenamiento
- Revisar y corregir etiquetas
- Mejorar calidad de documentos
- Balancear clases

### 🔧 Comandos de Diagnóstico

```bash
# Verificar documentos disponibles
ls -la sentencias/ uploads/

# Verificar etiquetas
cat models/labels.json

# Probar carga de modelo
python -c "
import pickle
with open('models/modelo_legal.pkl', 'rb') as f:
    modelo = pickle.load(f)
print('Modelo cargado correctamente')
print(f'Componentes: {list(modelo.keys())}')
"
```

## 📚 Recursos Adicionales

### 🔗 Documentación Relacionada

- [📋 Análisis de Discrepancias](ANALISIS_DISCREPANCIAS.md)
- [⚖️ Configuración de Ponderación](CONFIGURACION_PONDERACION.md)
- [🔮 Análisis Predictivo](ANALISIS_PREDICTIVO.md)
- [📝 Generación de Demandas](GENERACION_DEMANDAS.md)

### 🛠️ Herramientas Recomendadas

- **Jupyter Notebook**: Para experimentación interactiva
- **scikit-learn**: Documentación oficial
- **Sentence-Transformers**: Documentación y ejemplos
- **PyPDF2**: Para procesamiento de PDFs

### 📖 Referencias Técnicas

- [TF-IDF en scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [Logistic Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
- [Sentence-Transformers](https://www.sbert.net/)
- [Pickle en Python](https://docs.python.org/3/library/pickle.html)

---

**Última actualización**: Enero 2025  
**Versión**: 2.0.0  
**Autor**: Sistema de Análisis Legal IPP/INSS
