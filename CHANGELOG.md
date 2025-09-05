# 📋 Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Funcionalidades en desarrollo para futuras versiones

### Changed
- Mejoras en curso

### Deprecated
- Funcionalidades que serán removidas en futuras versiones

### Removed
- Funcionalidades removidas

### Fixed
- Correcciones en curso

### Security
- Mejoras de seguridad en curso

## [2.0.0] - 2024-01-15

### Added
- **Dashboard Interactivo**: Nueva interfaz web moderna con Bootstrap 5
- **Análisis Automático**: Procesamiento inteligente de documentos legales
- **7 Categorías de Análisis**: IPP, RAP, INSS, LPNI, Limpieza, Lesiones de Hombro, Procedimientos Legales
- **API REST**: Endpoints para integración con sistemas externos
- **Event Delegation**: Sistema robusto de manejo de eventos JavaScript
- **Modales Interactivos**: Visualización detallada de estadísticas y frases
- **Navegación a Archivos**: Funcionalidad completa para ver archivos con frases resaltadas
- **Sistema de Logging**: Logs estructurados con diferentes niveles
- **Configuración Docker**: Contenedores para despliegue simplificado
- **Monitoreo**: Endpoint de salud y métricas del sistema

### Changed
- **Arquitectura Frontend**: Migración completa a Bootstrap 5 y JavaScript moderno
- **Manejo de Eventos**: Implementación de event delegation para elementos dinámicos
- **Sistema de Templates**: Mejoras en Jinja2 con mejor manejo de datos
- **Análisis de IA**: Sistema de fallback robusto entre IA y análisis básico
- **Interfaz de Usuario**: Rediseño completo del dashboard y modales

### Fixed
- **Botones "Ver Detalles"**: Corrección de funcionalidad en tarjetas de estadísticas
- **Parsing JSON**: Solución de errores de parsing en JavaScript
- **Event Listeners**: Implementación correcta para elementos generados dinámicamente
- **Navegación**: Funcionalidad completa de "Ver archivo completo"
- **Caracteres Especiales**: Manejo correcto de acentos y caracteres especiales en español

### Security
- **Validación de Archivos**: Sistema robusto de validación de archivos subidos
- **Sanitización de Datos**: Limpieza de datos antes de renderizar en templates
- **Manejo de Errores**: Sistema robusto de manejo de excepciones

## [1.0.0] - 2024-01-01

### Added
- **Análisis Básico**: Sistema de análisis basado en reglas para documentos legales
- **Soporte de Formatos**: Lectura de archivos .txt, .pdf, .doc, .docx
- **Identificación de Frases**: Detección de frases clave en 7 categorías
- **API Básica**: Endpoints para análisis de documentos
- **Interfaz Web**: Templates HTML básicos con Bootstrap
- **Docker**: Configuración básica de contenedores

### Changed
- **Versión Inicial**: Primera versión estable del proyecto

---

## 📝 Notas de Versión

### Versionado

- **MAJOR**: Cambios incompatibles con versiones anteriores
- **MINOR**: Nuevas funcionalidades compatibles hacia atrás
- **PATCH**: Correcciones de bugs compatibles hacia atrás

### Convenciones de Commits

Este proyecto sigue [Conventional Commits](https://www.conventionalcommits.org/):

- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato
- `refactor`: Refactorización de código
- `test`: Agregar o corregir tests
- `chore`: Cambios en build, configuraciones, etc.

### Proceso de Release

1. **Desarrollo**: Cambios en rama `develop`
2. **Testing**: Tests y validaciones en rama `develop`
3. **Release**: Merge a `main` con tag de versión
4. **Hotfix**: Correcciones críticas directamente en `main`

---

## 🔗 Enlaces Útiles

- [README.md](README.md) - Documentación completa del proyecto
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guía de contribución
- [GitHub Releases](https://github.com/tu-usuario/analizador-sentencias-ipp/releases) - Historial de releases
- [GitHub Issues](https://github.com/tu-usuario/analizador-sentencias-ipp/issues) - Reportar bugs y solicitar funcionalidades
