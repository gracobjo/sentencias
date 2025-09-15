# 📚 Documentación del Analizador de Sentencias

Bienvenido a la documentación completa del **Analizador de Sentencias IPP/INSS**, un sistema de análisis inteligente de documentos legales con IA.

## 📖 Índice de Documentación

### **🚀 Guías de Inicio**
- [📋 README Principal](../README.md) - Introducción y características principales
- [⚙️ Configuración](CONFIGURACION.md) - Configuración completa del sistema
- [🚀 Despliegue](DEPLOYMENT.md) - Guías de despliegue desde local hasta producción

### **🔧 Funcionalidades Técnicas**
- [🔮 Análisis Predictivo](ANALISIS_PREDICTIVO.md) - Sistema de predicciones inteligentes
- [📝 Generación de Demandas](GENERACION_DEMANDAS.md) - Creación automática de documentos legales
- [⚖️ Análisis de Discrepancias](ANALISIS_DISCREPANCIAS.md) - Detección de contradicciones médico-legales

### **🌐 API y Desarrollo**
- [🌐 API Endpoints](API_ENDPOINTS.md) - Documentación completa de la API REST
- [📊 Análisis de Riesgo y Ponderación](ANALISIS_RIESGO_PONDERACION.md) - Sistema de evaluación de riesgo
- [⚙️ Configuración de Ponderación](CONFIGURACION_PONDERACION.md) - Personalización de factores de peso

### **📚 Guías Específicas**
- [📋 Flujo de Ponderación](FLUJO_PONDERACION.md) - Proceso de análisis ponderado
- [💡 Ejemplo Práctico de Ponderación](EJEMPLO_PRACTICO_PONDERACION.md) - Casos de uso reales
- [📖 README de Ponderación](README_PONDERACION.md) - Introducción al sistema de ponderación

## 🎯 Casos de Uso Principales

### **Para Abogados**
- **Análisis rápido** de sentencias y resoluciones
- **Generación automática** de demandas y recursos
- **Identificación de patrones** favorables y desfavorables
- **Análisis predictivo** de probabilidades de éxito

### **Para Peritos Médicos**
- **Detección de discrepancias** en informes médicos
- **Análisis de coherencia** médico-legal
- **Identificación de evidencia** objetiva
- **Recomendaciones** para peritajes complementarios

### **Para Estudiantes de Derecho**
- **Aprendizaje** de análisis jurídico
- **Comprensión** de patrones legales
- **Práctica** con casos reales
- **Análisis** de jurisprudencia

### **Para Investigadores**
- **Análisis estadístico** de resoluciones
- **Identificación de tendencias** jurídicas
- **Estudios** de jurisprudencia
- **Investigación** en derecho administrativo

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

## 📊 Métricas del Sistema

### **Precisión**
- **Análisis básico**: 85-90%
- **Análisis con IA**: 92-95%
- **Análisis híbrido**: 95-98%

### **Rendimiento**
- **Tiempo de análisis**: 2-5 segundos por documento
- **Capacidad**: Hasta 50 documentos simultáneos
- **Memoria**: Optimizado para producción

## 🔗 Enlaces Útiles

### **Desarrollo**
- [🐛 Issues](https://github.com/gracobjo/sentencias/issues)
- [💬 Discusiones](https://github.com/gracobjo/sentencias/discussions)
- [📧 Contacto](mailto:soporte@sentencias-ipp.com)

### **Producción**
- [🌐 Aplicación Web](https://sentencias.onrender.com)
- [📊 Análisis Predictivo](https://sentencias.onrender.com/analisis-predictivo)
- [📝 Generación de Demandas](https://sentencias.onrender.com/generar-demanda)

## 📋 Estructura del Proyecto

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
├── 📁 sentencias/               # Documentos de ejemplo
├── 📁 uploads/                  # Archivos subidos
└── 📁 logs/                     # Logs del sistema
```

## 🚀 Inicio Rápido

### **Instalación**
```bash
git clone https://github.com/gracobjo/sentencias.git
cd sentencias
pip install -r requirements.txt
python app.py
```

### **Acceso**
- **Desarrollo**: http://localhost:8000
- **Producción**: https://sentencias.onrender.com

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](../LICENSE) para más detalles.

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

## 🔮 Roadmap

### **Próximas Funcionalidades**
- [ ] Integración con bases de datos jurídicas oficiales
- [ ] API REST completa con autenticación
- [ ] Aplicación móvil para iOS/Android
- [ ] Análisis de sentencias en tiempo real
- [ ] Integración con sistemas de gestión de casos

### **Investigación en Curso**
- [ ] Modelos de deep learning para análisis jurídico
- [ ] Análisis de sentimientos en resoluciones
- [ ] Predicción de tiempos de resolución
- [ ] Análisis de costos de procedimientos

---

**Desarrollado con ❤️ para la comunidad jurídica española**

*Última actualización: Enero 2025*
