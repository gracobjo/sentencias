# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al **Analizador de Sentencias IPP/INSS**! Este documento te guiará a través del proceso de contribución.

## 📋 Tabla de Contenidos

- [Cómo Contribuir](#cómo-contribuir)
- [Configuración del Entorno de Desarrollo](#configuración-del-entorno-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Reportar Bugs](#reportar-bugs)
- [Solicitar Funcionalidades](#solicitar-funcionalidades)
- [Preguntas y Discusiones](#preguntas-y-discusiones)

## 🚀 Cómo Contribuir

### Tipos de Contribuciones

Aceptamos varios tipos de contribuciones:

- 🐛 **Reportar bugs** - Ayúdanos a encontrar y solucionar problemas
- 💡 **Solicitar funcionalidades** - Sugiere nuevas características
- 📝 **Mejorar documentación** - Ayuda a que otros entiendan mejor el proyecto
- 🔧 **Corregir bugs** - Soluciona problemas existentes
- ✨ **Agregar funcionalidades** - Implementa nuevas características
- 🧪 **Mejorar tests** - Aumenta la cobertura y calidad de los tests
- 🎨 **Mejorar la interfaz** - Haz la aplicación más atractiva y usable

### Antes de Empezar

1. **Revisa los issues existentes** para evitar duplicar trabajo
2. **Únete a las discusiones** para entender mejor el contexto
3. **Lee la documentación** del proyecto
4. **Asegúrate de que tu contribución esté alineada** con los objetivos del proyecto

## 🛠️ Configuración del Entorno de Desarrollo

### Requisitos Previos

- Python 3.8 o superior
- Git
- Un editor de código (VS Code, PyCharm, etc.)

### Configuración Inicial

1. **Fork del repositorio**
   ```bash
   # Ve a GitHub y haz fork del repositorio
   # Luego clona tu fork
   git clone https://github.com/tu-usuario/analizador-sentencias-ipp.git
   cd analizador-sentencias-ipp
   ```

2. **Configura el repositorio remoto**
   ```bash
   git remote add upstream https://github.com/original/analizador-sentencias-ipp.git
   git fetch upstream
   ```

3. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

4. **Instala dependencias de desarrollo**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

5. **Instala pre-commit hooks**
   ```bash
   pre-commit install
   ```

### Estructura del Proyecto

```
analizador-sentencias-ipp/
├── app.py                          # Aplicación principal
├── backend/                        # Módulos del backend
│   ├── analisis.py                # Análisis de IA
│   └── main.py                    # Backend alternativo
├── templates/                      # Templates HTML
├── static/                         # Archivos estáticos
├── tests/                          # Tests del proyecto
├── docs/                           # Documentación
└── scripts/                        # Scripts de utilidad
```

## 📝 Estándares de Código

### Python

- **Versión**: Python 3.8+
- **Formato**: Black con línea de 88 caracteres
- **Linting**: Flake8
- **Type Checking**: MyPy
- **Imports**: isort

### JavaScript/HTML/CSS

- **Formato**: Prettier
- **Linting**: ESLint (cuando esté configurado)
- **HTML**: HTML5 válido
- **CSS**: Bootstrap 5 con personalizaciones mínimas

### Estructura de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Tipos de Commits

- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato (espacios, punto y coma, etc.)
- `refactor`: Refactorización de código
- `test`: Agregar o corregir tests
- `chore`: Cambios en build, configuraciones, etc.

#### Ejemplos

```bash
feat: agregar nueva categoría de análisis IPP
fix: corregir error en parsing de PDF
docs: actualizar documentación de API
style: mejorar diseño del dashboard
refactor: optimizar algoritmo de búsqueda
test: agregar tests para análisis de frases
```

### Naming Conventions

- **Funciones y variables**: `snake_case`
- **Clases**: `PascalCase`
- **Constantes**: `UPPER_SNAKE_CASE`
- **Archivos**: `snake_case.py`
- **Directorios**: `snake_case/`

## 🔄 Proceso de Pull Request

### 1. Crear una Rama

```bash
# Asegúrate de estar en main y actualizado
git checkout main
git pull upstream main

# Crea una nueva rama
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correccion-bug
```

### 2. Desarrollar la Funcionalidad

- **Escribe código limpio** y bien documentado
- **Agrega tests** para nuevas funcionalidades
- **Actualiza documentación** si es necesario
- **Sigue los estándares** del proyecto

### 3. Commits

```bash
# Haz commits frecuentes y descriptivos
git add .
git commit -m "feat: agregar análisis de nuevas frases clave

- Implementar detector de IPP avanzado
- Agregar tests unitarios
- Actualizar documentación"

# Si necesitas hacer cambios menores
git commit --amend
```

### 4. Push y Pull Request

```bash
# Push a tu fork
git push origin feature/nueva-funcionalidad

# Ve a GitHub y crea un Pull Request
```

### 5. Template del Pull Request

```markdown
## 📝 Descripción

Describe brevemente los cambios realizados.

## 🔍 Tipo de Cambio

- [ ] Bug fix (cambio que corrige un problema)
- [ ] Nueva funcionalidad (cambio que agrega funcionalidad)
- [ ] Breaking change (cambio que rompe funcionalidad existente)
- [ ] Documentación (cambio en documentación)

## 🧪 Tests

- [ ] Tests unitarios agregados/actualizados
- [ ] Tests de integración agregados/actualizados
- [ ] Todos los tests pasan localmente

## 📋 Checklist

- [ ] Mi código sigue los estándares del proyecto
- [ ] He revisado mi propio código
- [ ] He comentado mi código donde sea necesario
- [ ] He hecho los cambios correspondientes en la documentación
- [ ] Mis cambios no generan nuevos warnings
- [ ] He agregado tests que prueban que mi corrección funciona
- [ ] Tests nuevos y existentes pasan con mis cambios
- [ ] Cualquier cambio dependiente ha sido documentado y actualizado

## 🔗 Issues Relacionados

Closes #123
Relates to #456
```

## 🐛 Reportar Bugs

### Antes de Reportar

1. **Busca en issues existentes** para ver si ya fue reportado
2. **Verifica que el bug no sea intencional**
3. **Asegúrate de que estés usando la última versión**

### Template de Bug Report

```markdown
## 🐛 Descripción del Bug

Descripción clara y concisa del bug.

## 🔄 Pasos para Reproducir

1. Ve a '...'
2. Haz clic en '...'
3. Desplázate hacia abajo hasta '...'
4. Ve el error

## ✅ Comportamiento Esperado

Descripción clara de lo que debería pasar.

## 📱 Comportamiento Actual

Descripción clara de lo que está pasando.

## 🖼️ Capturas de Pantalla

Si es aplicable, agrega capturas de pantalla.

## 💻 Información del Sistema

- **OS**: [ej. Windows 10, macOS 12.0, Ubuntu 20.04]
- **Navegador**: [ej. Chrome 91, Safari 14, Firefox 89]
- **Versión**: [ej. 2.0.0]

## 📝 Información Adicional

Cualquier otra información relevante sobre el problema.
```

## 💡 Solicitar Funcionalidades

### Template de Feature Request

```markdown
## 🚀 Descripción de la Funcionalidad

Descripción clara y concisa de la funcionalidad solicitada.

## 🎯 Problema que Resuelve

Descripción clara del problema que esta funcionalidad resolvería.

## 💭 Solución Propuesta

Descripción de la solución que te gustaría ver implementada.

## 🔄 Alternativas Consideradas

Descripción de cualquier alternativa o funcionalidad relacionada que hayas considerado.

## 📱 Información Adicional

Cualquier otra información o capturas de pantalla sobre la funcionalidad solicitada.
```

## 💬 Preguntas y Discusiones

### GitHub Discussions

Para preguntas generales, sugerencias o discusiones sobre el proyecto:

1. Ve a la pestaña **Discussions** en GitHub
2. Busca si tu pregunta ya fue respondida
3. Si no, crea una nueva discusión

### GitHub Issues

Para problemas específicos, bugs o funcionalidades:

1. Ve a la pestaña **Issues** en GitHub
2. Busca si ya existe un issue similar
3. Si no, crea uno nuevo usando los templates

## 🏆 Reconocimiento

### Contribuidores

Todos los contribuidores serán reconocidos en:

- **README.md** del proyecto
- **CHANGELOG.md** para cambios significativos
- **GitHub Contributors** automáticamente

### Criterios para ser Contribuidor

- **Contribuciones significativas** al proyecto
- **Participación activa** en la comunidad
- **Mantenimiento de estándares** de calidad

## 📞 Contacto

Si tienes preguntas sobre cómo contribuir:

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/analizador-sentencias-ipp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tu-usuario/analizador-sentencias-ipp/discussions)
- **Email**: tu-email@ejemplo.com

## 🙏 Agradecimientos

¡Gracias por considerar contribuir a este proyecto! Tu tiempo y esfuerzo son muy apreciados.

---

**¿Listo para contribuir?** ¡Empieza por hacer fork del repositorio y crear tu primera rama!
