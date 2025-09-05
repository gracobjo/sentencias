# 🧠 Modelos de IA - Analizador de Sentencias IPP/INSS

## 📋 Descripción

Este directorio contiene los modelos de inteligencia artificial pre-entrenados para el análisis de documentos legales.

## 🔧 Configuración del Modelo

### 📁 Estructura Esperada

```
models/
├── modelo_legal.pkl          # Modelo principal (requerido)
├── frases_clave.json         # Configuración de frases clave
└── README.md                 # Este archivo
```

### 🎯 Modelo Principal (`modelo_legal.pkl`)

El archivo `modelo_legal.pkl` debe contener un diccionario con la siguiente estructura:

```python
{
    'modelo': modelo_entrenado,           # Modelo de scikit-learn
    'vectorizador': vectorizador_texto,   # TF-IDF o similar
    'clasificador': clasificador_binario  # Clasificador binario
}
```

### 📊 Formato del Modelo

#### Vectorizador
- **Tipo**: TF-IDF, CountVectorizer, o similar
- **Funcionalidad**: Convertir texto a vectores numéricos
- **Entrada**: Texto plano (string)
- **Salida**: Vector numérico

#### Clasificador
- **Tipo**: Clasificador binario (RandomForest, SVM, etc.)
- **Funcionalidad**: Clasificar documentos como favorables/desfavorables
- **Entrada**: Vector numérico del texto
- **Salida**: 0 (desfavorable) o 1 (favorable)

## 🚀 Creación del Modelo

### 📝 Ejemplo de Entrenamiento

```python
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

# Crear pipeline
pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer(max_features=5000)),
    ('classifier', RandomForestClassifier(n_estimators=100))
])

# Entrenar modelo (con datos de ejemplo)
textos = ["texto1", "texto2", "texto3"]
etiquetas = [1, 0, 1]  # 1=favorable, 0=desfavorable

pipeline.fit(textos, etiquetas)

# Guardar modelo
modelo_data = {
    'modelo': pipeline,
    'vectorizador': pipeline.named_steps['vectorizer'],
    'clasificador': pipeline.named_steps['classifier']
}

with open('models/modelo_legal.pkl', 'wb') as f:
    pickle.dump(modelo_data, f)
```

### 🔍 Datos de Entrenamiento

Para entrenar un modelo efectivo, necesitarás:

1. **Documentos legales**: Sentencias, resoluciones, demandas
2. **Etiquetas**: Clasificación manual (favorable/desfavorable)
3. **Balance**: Mismo número de casos favorables y desfavorables
4. **Calidad**: Documentos bien estructurados y legibles

### 📊 Métricas de Evaluación

- **Precisión**: > 80%
- **Recall**: > 75%
- **F1-Score**: > 0.8
- **Validación cruzada**: 5-fold

## 🔄 Fallback Automático

Si no hay modelo disponible, la aplicación usa automáticamente:

- **Análisis basado en reglas**
- **Patrones de frases clave**
- **Predicción por palabras clave**
- **Extracción de argumentos legales**

## 🧪 Testing del Modelo

### 📋 Verificar Funcionamiento

```python
# Cargar y probar modelo
with open('models/modelo_legal.pkl', 'rb') as f:
    modelo_data = pickle.load(f)

# Probar predicción
texto_prueba = "Estimamos procedente la reclamación..."
vector = modelo_data['vectorizador'].transform([texto_prueba])
prediccion = modelo_data['clasificador'].predict(vector)
probabilidad = modelo_data['clasificador'].predict_proba(vector)

print(f"Predicción: {prediccion[0]}")
print(f"Probabilidad: {probabilidad[0]}")
```

### ✅ Validación

- **Formato**: El archivo debe ser un pickle válido
- **Estructura**: Debe contener las claves esperadas
- **Funcionalidad**: Debe poder hacer predicciones
- **Rendimiento**: Tiempo de respuesta < 1 segundo

## 🔧 Personalización

### 📝 Modificar Frases Clave

Edita `frases_clave.json` para agregar nuevas categorías:

```json
{
  "nueva_categoria": [
    "frase1",
    "frase2",
    "frase3"
  ]
}
```

### 🎯 Ajustar Umbrales

En `backend/analisis.py`, puedes modificar:

- **Confianza mínima**: Para predicciones
- **Contexto**: Ventana de caracteres para frases clave
- **Patrones**: Expresiones regulares para argumentos

## 🚨 Solución de Problemas

### ❌ Errores Comunes

#### 1. Modelo no encontrado
```
Error: No se pudo cargar el modelo
Solución: Verificar que existe models/modelo_legal.pkl
```

#### 2. Formato incorrecto
```
Error: El modelo no tiene la estructura esperada
Solución: Verificar que contiene 'modelo', 'vectorizador', 'clasificador'
```

#### 3. Dependencias faltantes
```
Error: scikit-learn no está instalado
Solución: pip install scikit-learn
```

### 🔍 Debugging

#### 1. Verificar archivo
```bash
ls -la models/
file models/modelo_legal.pkl
```

#### 2. Verificar contenido
```python
import pickle
with open('models/modelo_legal.pkl', 'rb') as f:
    data = pickle.load(f)
print(data.keys())
```

#### 3. Verificar logs
```bash
tail -f logs/app.log
```

## 📚 Recursos Adicionales

- **Scikit-learn**: https://scikit-learn.org/
- **TF-IDF**: https://en.wikipedia.org/wiki/Tf%E2%80%93idf
- **Machine Learning**: https://scikit-learn.org/stable/tutorial/
- **NLP**: https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction

## 🤝 Contribución

Para contribuir con mejoras al modelo:

1. **Fork** el repositorio
2. **Entrena** un modelo mejorado
3. **Evalúa** el rendimiento
4. **Documenta** el proceso
5. **Crea** un Pull Request

---

**¿Necesitas ayuda con el modelo?** ¡Abre un issue o únete a las discusiones del proyecto!


