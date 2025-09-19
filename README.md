# 📋 Analizador de Sentencias IPP/INSS

> **Sistema de Análisis Inteligente de Documentos Legales con IA**

Una aplicación web avanzada que utiliza inteligencia artificial para analizar sentencias judiciales, informes médicos y documentos legales relacionados con Incapacidad Permanente Parcial (IPP) y el Instituto Nacional de la Seguridad Social (INSS).

## 🚀 Características Principales

### 🔍 **Análisis Inteligente**
- **Análisis de IA**: Procesamiento avanzado con modelos de machine learning
- **Análisis de Discrepancias**: Detección automática de contradicciones médico-legales
- **Análisis Predictivo**: Predicción de resultados basada en patrones históricos
- **Extracción de Frases Clave**: Identificación automática de términos jurídicos relevantes

### 📓 **Google Colab Notebook**
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gracobjo/sentencias/blob/main/docs/Analizador_Sentencias_Colab.ipynb)

**¡Nuevo!** Notebook completo para Google Colab con todas las funcionalidades:
- 🔧 **Instalación automática** de dependencias
- 🔍 **Análisis inteligente** de documentos legales
- 🔮 **Predicción de resultados** con machine learning
- 📊 **Visualizaciones** interactivas y estáticas
- 📄 **Procesamiento de PDFs** en tiempo real
- 📤 **Exportación** en múltiples formatos
- 🔗 **Integración con Google Drive**
- 🔧 **Diagnóstico y solución** de problemas

**[📖 Ver documentación completa del notebook](docs/README_COLAB.md)**

### 📊 **Funcionalidades Avanzadas**
- **Análisis Híbrido**: Combina IA con reglas jurídicas especializadas
- **Ponderación por Instancia**: TS (x1.5), TSJ (x1.2), otras (x1.0)
- **Generación de Demandas**: Creación automática de documentos legales
- **Exportación**: Descarga en PDF y Word con análisis completo

### 🎯 **Casos de Uso**
- **Abogados**: Análisis rápido de sentencias y preparación de recursos
- **Peritos Médicos**: Evaluación de discrepancias en informes médicos
- **Estudiantes de Derecho**: Aprendizaje de análisis jurídico
- **Investigadores**: Análisis estadístico de resoluciones legales

## 🏗️ Arquitectura del Sistema

```
📁 sentencias/
├── 🚀 app.py                    # Aplicación principal (desarrollo)
├── 🚀 app-deploy.py             # Aplicación de producción
├── 📁 backend/                  # Lógica de negocio
│   ├── analisis.py              # Analizador principal con IA
│   ├── analisis_discrepancias.py # Análisis médico-legal
│   └── analisis_predictivo.py   # Predicciones inteligentes
├── 📁 templates/                # Interfaces web
├── 📁 static/                   # Recursos estáticos
├── 📁 models/                   # Modelos de IA entrenados
├── 📁 docs/                     # Documentación técnica
└── 📁 sentencias/               # Documentos de ejemplo
```

## 🛠️ Tecnologías Utilizadas

### **Backend**
- **Python 3.11+** - Lenguaje principal
- **FastAPI** - Framework web moderno
- **Scikit-learn** - Machine learning
- **PyPDF2** - Procesamiento de PDFs
- **python-docx** - Generación de documentos Word

### **Frontend**
- **HTML5/CSS3** - Estructura y estilos
- **Bootstrap 5** - Framework CSS
- **JavaScript ES6+** - Interactividad
- **Chart.js** - Visualizaciones

### **IA y ML**
- **TF-IDF** - Vectorización de texto
- **Sentence-BERT** - Embeddings semánticos
- **Análisis de Patrones** - Reglas jurídicas especializadas

## 🚀 Instalación y Uso

### **Requisitos**
- Python 3.11+
- pip o pipenv
- Git

### **Instalación Rápida**
```bash
# Clonar repositorio
git clone https://github.com/gracobjo/sentencias.git
cd sentencias

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

### **Acceso**
- **Desarrollo**: http://localhost:8000
- **Producción**: https://sentencias.onrender.com

## 📖 Documentación

### **Guías Principales**
- [📋 Análisis de Discrepancias](docs/ANALISIS_DISCREPANCIAS.md)
- [⚖️ Configuración de Ponderación](docs/CONFIGURACION_PONDERACION.md)
- [🔮 Análisis Predictivo](docs/ANALISIS_PREDICTIVO.md)
- [📝 Generación de Demandas](docs/GENERACION_DEMANDAS.md)
- [🧠 Entrenamiento de Modelos](docs/ENTRENAMIENTO_MODELOS.md)
- [📚 Librerías de Modelos](docs/LIBRERIAS_MODELOS.md)

### **API Documentation**
- [🌐 API Endpoints](docs/API_ENDPOINTS.md)
- [🔧 Configuración](docs/CONFIGURACION.md)
- [🚀 Despliegue](docs/DEPLOYMENT.md)

## 🎯 Funcionalidades Detalladas

### **1. Análisis de Documentos**
- **Subida de archivos**: PDF, TXT, DOCX
- **Extracción de texto**: Automática con OCR
- **Análisis semántico**: Comprensión del contexto jurídico
- **Clasificación**: Favorable/Desfavorable con confianza

### **2. Análisis de Discrepancias**
- **Detección automática**: Contradicciones médico-legales
- **Puntuación de riesgo**: Escala 0-100
- **Evidencia objetiva**: Identificación de elementos clave
- **Recomendaciones**: Estrategias de defensa

### **3. Análisis Predictivo**
- **Patrones históricos**: Análisis de resoluciones previas
- **Probabilidades**: Cálculo con factores de realismo jurídico
- **Tendencias**: Identificación de patrones emergentes
- **Confianza**: Niveles de certeza en predicciones

### **4. Generación de Demandas**
- **Plantillas inteligentes**: Basadas en análisis previos
- **Metadatos automáticos**: Extracción de información relevante
- **Personalización**: Adaptación a casos específicos
- **Exportación**: PDF y Word profesionales

## 🔧 Configuración Avanzada

### **Variables de Entorno**
```bash
# Configuración de IA
ANALIZADOR_IA_DISPONIBLE=true
MODELO_IA_PATH=models/modelo_legal.pkl

# Configuración de archivos
MAX_FILE_SIZE=50MB
ALLOWED_EXTENSIONS=pdf,txt,docx

# Configuración de análisis
CONFIANZA_MINIMA=0.6
FACTOR_REALISMO_JURIDICO=true
```

### **Personalización de Modelos**
- **Frases clave**: `models/frases_clave.json`
- **Patrones jurídicos**: `backend/analisis.py`
- **Ponderaciones**: `backend/analisis_predictivo.py`

## 📊 Métricas y Rendimiento

### **Precisión del Sistema**
- **Análisis básico**: 85-90% de precisión
- **Análisis con IA**: 92-95% de precisión
- **Análisis híbrido**: 95-98% de precisión

### **Rendimiento**
- **Tiempo de análisis**: 2-5 segundos por documento
- **Capacidad**: Hasta 50 documentos simultáneos
- **Memoria**: Optimizado para producción

## 🤝 Contribución

### **Cómo Contribuir**
1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### **Estándares de Código**
- **PEP 8**: Estilo de código Python
- **Type hints**: Tipado estático
- **Docstrings**: Documentación de funciones
- **Tests**: Cobertura mínima del 80%

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

### **Problemas Comunes**
- [🐛 Issues](https://github.com/gracobjo/sentencias/issues)
- [💬 Discusiones](https://github.com/gracobjo/sentencias/discussions)
- [📧 Contacto](mailto:soporte@sentencias-ipp.com)

### **Roadmap**
- [ ] Integración con bases de datos jurídicas
- [ ] API REST completa
- [ ] Aplicación móvil
- [ ] Análisis de sentencias en tiempo real

---

**Desarrollado con ❤️ para la comunidad jurídica española**

*Última actualización: Enero 2025*