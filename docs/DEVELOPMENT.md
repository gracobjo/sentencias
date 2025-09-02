# 🛠️ Guía de Desarrollo

## Configuración del Entorno

### Prerrequisitos
- Python 3.8+
- pipenv
- Git
- Docker (opcional)

### Instalación
```bash
# Clonar repositorio
git clone https://github.com/gracobjo/sentencias.git
cd sentencias

# Instalar dependencias
pipenv install --dev

# Instalar pre-commit hooks
pipenv run pre-commit install
```

## Estructura del Proyecto

```
sentencias/
├── sentencias_app/           # Paquete principal
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI
│   ├── config.py            # Configuración
│   ├── security.py          # Validación de archivos
│   ├── observability.py     # Logging y métricas
│   └── backend/             # Módulos de análisis
├── tests/                   # Tests
├── templates/               # Templates HTML
├── static/                  # Archivos estáticos
├── docs/                    # Documentación
├── .github/workflows/       # CI/CD
└── requirements.DOCKER.txt  # Dependencias para Docker
```

## Estándares de Código

### Formateo
```bash
# Formatear código
pipenv run black sentencias_app/ tests/

# Verificar formato
pipenv run black --check sentencias_app/ tests/
```

### Linting
```bash
# Ejecutar linting
pipenv run flake8 sentencias_app/ tests/

# Type checking
pipenv run mypy sentencias_app/
```

### Seguridad
```bash
# Verificar seguridad
pipenv run bandit -r sentencias_app/
pipenv run safety check
```

## Testing

### Ejecutar Tests
```bash
# Todos los tests
pipenv run pytest tests/ -v

# Tests específicos
pipenv run pytest tests/test_api.py -v

# Con cobertura
pipenv run pytest tests/ --cov=sentencias_app --cov-report=html
```

### Escribir Tests
```python
# Ejemplo de test
def test_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

## Desarrollo de Funcionalidades

### 1. Crear Rama
```bash
git checkout -b feature/nueva-funcionalidad
```

### 2. Desarrollar
- Escribir código
- Añadir tests
- Actualizar documentación

### 3. Validar
```bash
# Pre-commit hooks
git add .
git commit -m "feat: nueva funcionalidad"

# Tests
pipenv run pytest tests/ -v
```

### 4. Pull Request
- Crear PR en GitHub
- Revisar CI/CD
- Obtener aprobación

## Debugging

### Logs
```bash
# Ver logs en tiempo real
tail -f logs/app.log

# Logs estructurados
cat logs/app.log | jq
```

### Métricas
```bash
# Ver métricas
curl http://localhost:8000/metrics

# Health check
curl http://localhost:8000/health
```

## Docker

### Build Local
```bash
# Build imagen
docker build -t sentencias:local .

# Ejecutar
docker run -p 8000:8000 sentencias:local
```

### Docker Compose
```bash
# Desarrollo
docker-compose up

# Producción
docker-compose -f docker-compose.prod.yml up
```

## Deployment

### Staging
- Push a rama `develop`
- Deployment automático via GitHub Actions

### Production
- Push a rama `main`
- Deployment automático via GitHub Actions

## Troubleshooting

### Problemas Comunes

#### Error de dependencias
```bash
# Limpiar cache
pipenv --rm
pipenv install
```

#### Error de tests
```bash
# Verificar configuración
pipenv run pytest --collect-only
```

#### Error de Docker
```bash
# Limpiar imágenes
docker system prune -a
```

## Contribución

1. Fork el repositorio
2. Crear rama de feature
3. Desarrollar con tests
4. Crear Pull Request
5. Obtener review y merge

### Commits
- Usar [Conventional Commits](https://conventionalcommits.org/)
- `feat:` para nuevas funcionalidades
- `fix:` para correcciones
- `docs:` para documentación
- `test:` para tests
- `refactor:` para refactoring
