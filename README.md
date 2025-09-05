# Analizador de Sentencias IPP/INSS

Sistema de análisis inteligente de resoluciones legales con IA para identificar patrones, argumentos clave y predicciones de resultados.

## 🚀 Despliegue en Servidor

### Opción 1: Render (Recomendado - Gratis)

1. **Crear cuenta en Render:**
   - Ve a [render.com](https://render.com)
   - Regístrate con GitHub

2. **Conectar repositorio:**
   - Haz clic en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Selecciona este proyecto

3. **Configuración automática:**
   - Render detectará automáticamente que es una app Python
   - Usará el archivo `requirements.txt` para instalar dependencias
   - Usará el `Procfile` para iniciar la aplicación

4. **Variables de entorno (opcional):**
   ```
   PYTHON_VERSION=3.11.0
   ```

5. **Desplegar:**
   - Haz clic en "Create Web Service"
   - Render construirá y desplegará automáticamente
   - Obtendrás una URL como: `https://tu-app.onrender.com`

### Opción 2: Railway

1. **Crear cuenta en Railway:**
   - Ve a [railway.app](https://railway.app)
   - Regístrate con GitHub

2. **Conectar proyecto:**
   - "New Project" → "Deploy from GitHub repo"
   - Selecciona este repositorio

3. **Configuración:**
   - Railway detectará automáticamente Python
   - Configurará el despliegue automáticamente

### Opción 3: Heroku

1. **Instalar Heroku CLI:**
   ```bash
   # Windows
   winget install Heroku.HerokuCLI
   
   # O descargar desde: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login y crear app:**
   ```bash
   heroku login
   heroku create tu-app-sentencias
   ```

3. **Desplegar:**
   ```bash
   git push heroku main
   ```

## 📁 Estructura del Proyecto

```
sentencias/
├── app.py                 # Aplicación principal FastAPI
├── requirements.txt       # Dependencias Python
├── Procfile              # Comando de inicio para servidores
├── runtime.txt           # Versión de Python
├── render.yaml           # Configuración para Render
├── templates/            # Templates HTML
│   ├── index.html
│   └── archivo.html
├── static/               # Archivos estáticos
│   └── style.css
└── sentencias/           # Directorio de PDFs (local)
```

## 🔧 Características

- **Análisis de PDFs:** Extracción automática de texto
- **IA Integrada:** Identificación de frases clave y argumentos
- **Análisis Predictivo:** Predicción de resultados legales
- **Interfaz Web:** Dashboard intuitivo con Bootstrap
- **Búsqueda Avanzada:** Localización de argumentos específicos
- **Exportación:** Generación de documentos Word

## 🛠️ Desarrollo Local

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/sentencias.git
cd sentencias

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

## 📝 Notas Importantes

- **Archivos PDF:** El directorio `sentencias/` contiene los PDFs a analizar
- **Modelos IA:** Se cargan automáticamente desde archivos `.pkl`
- **Base de Datos:** Se usa SQLite para almacenar análisis
- **Puerto:** La app se ejecuta en puerto 8000 por defecto

## 🔗 URLs Importantes

- **Aplicación:** `http://localhost:8000`
- **Documentación API:** `http://localhost:8000/docs`
- **Subir documentos:** `http://localhost:8000/subir`
- **Análisis predictivo:** `http://localhost:8000/api/analisis-predictivo`