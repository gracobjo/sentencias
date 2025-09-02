# 📋 Tareas de Auditoría y Refactorización

## 🎯 Objetivo
Realizar auditoría completa y refactorización del repositorio `sentencias` para mejorar estructura, dependencias, Docker, seguridad, tests y CI/CD.

## 📝 Checklist de Tareas

### ✅ **Paso 0: Preparación**
- [x] Crear rama `audit/refactor-pipenv-docker`
- [x] Crear archivo TASKS.md con lista de tareas

### 🔧 **Paso 1: Unificar Dependencias**
- [ ] Eliminar drift entre Pipfile / requirements / pyproject
- [ ] Eliminar o marcar como generados los requirements*.txt
- [ ] Regenerar Pipfile.lock con versiones fijadas
- [ ] Crear requirements.DOCKER.txt generado desde Pipfile
- [ ] Verificar compatibilidad de dependencias

### 🏗️ **Paso 2: Reestructurar Aplicación**
- [ ] Mover `app.py` a paquete `sentencias/`
- [ ] Crear `sentencias/__init__.py`
- [ ] Crear `sentencias/main.py` como punto de entrada
- [ ] Reorganizar estructura de directorios
- [ ] Actualizar imports y referencias

### 🐳 **Paso 3: Mejorar Docker**
- [ ] Actualizar Dockerfile para nueva estructura
- [ ] Optimizar layers de Docker
- [ ] Usar requirements.DOCKER.txt
- [ ] Mejorar multi-stage build
- [ ] Actualizar docker-compose.yml

### 🔒 **Paso 4: Seguridad de Uploads**
- [ ] Implementar validación robusta de archivos
- [ ] Añadir sanitización de nombres de archivo
- [ ] Implementar límites de tamaño
- [ ] Añadir verificación de tipos MIME
- [ ] Crear directorio seguro para uploads

### 🧪 **Paso 5: Tests con Jinja2**
- [ ] Crear tests para templates
- [ ] Implementar tests de integración
- [ ] Añadir tests de validación de formularios
- [ ] Crear tests de API endpoints
- [ ] Configurar pytest con fixtures

### 📊 **Paso 6: Observabilidad**
- [ ] Implementar logging estructurado
- [ ] Añadir métricas con Prometheus
- [ ] Crear health checks
- [ ] Implementar tracing
- [ ] Añadir monitoreo de performance

### 🚀 **Paso 7: CI/CD**
- [ ] Crear GitHub Actions workflow
- [ ] Implementar tests automáticos
- [ ] Añadir build de Docker
- [ ] Configurar deployment
- [ ] Añadir linting y formatting

### 📚 **Paso 8: Documentación**
- [ ] Actualizar README.md
- [ ] Crear documentación de API
- [ ] Añadir guías de desarrollo
- [ ] Documentar configuración
- [ ] Crear ejemplos de uso

## 🔍 **Análisis Inicial**

### Estructura Actual
```
sentencias/
├── app.py                    # Punto de entrada principal
├── backend/                  # Módulos de análisis
├── templates/               # Templates Jinja2
├── static/                  # Archivos estáticos
├── models/                  # Modelos de IA
├── sentencias/             # Documentos de ejemplo
├── uploads/                # Archivos subidos
├── logs/                   # Logs de aplicación
├── Pipfile                 # Dependencias Pipenv
├── requirements.txt        # Dependencias pip
├── pyproject.toml         # Configuración del proyecto
├── Dockerfile             # Imagen Docker
└── docker-compose.yml     # Orquestación Docker
```

### Problemas Identificados
1. **Drift de dependencias**: Múltiples archivos de dependencias
2. **Estructura plana**: Todo en raíz, falta organización
3. **Docker básico**: Sin optimizaciones
4. **Seguridad**: Validación básica de uploads
5. **Tests**: Falta cobertura de tests
6. **Observabilidad**: Logging básico
7. **CI/CD**: Sin automatización

## 🎯 **Criterios de Éxito**
- [ ] Todos los tests pasan
- [ ] Docker build exitoso
- [ ] Pipenv lock sin conflictos
- [ ] Estructura de paquetes clara
- [ ] Seguridad de uploads implementada
- [ ] Observabilidad completa
- [ ] CI/CD funcionando

## 📅 **Timeline Estimado**
- **Paso 1-2**: 2-3 horas (Dependencias + Estructura)
- **Paso 3-4**: 2-3 horas (Docker + Seguridad)
- **Paso 5-6**: 3-4 horas (Tests + Observabilidad)
- **Paso 7-8**: 2-3 horas (CI/CD + Documentación)
- **Total**: 9-13 horas

## 🔄 **Proceso de Validación**
1. **Después de cada paso**: Ejecutar tests y build
2. **Commits atómicos**: Un commit por tarea
3. **Mensajes claros**: Describir cambios específicos
4. **Validación continua**: No avanzar si hay errores
5. **Documentación**: Actualizar en cada paso

---

**Última actualización**: $(date)  
**Rama**: `audit/refactor-pipenv-docker`  
**Estado**: En progreso
