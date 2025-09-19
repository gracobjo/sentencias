# 📖 Instrucciones Detalladas para Google Colab

## 🚀 Guía Paso a Paso

### **Paso 1: Acceder al Notebook**

#### Opción A: Enlace Directo
1. Haz clic en este enlace: [Open In Colab](https://colab.research.google.com/github/gracobjo/sentencias/blob/main/docs/Analizador_Sentencias_Colab.ipynb)
2. Se abrirá automáticamente en Google Colab
3. Si es la primera vez, acepta los términos de servicio

#### Opción B: Desde Google Colab
1. Ve a [Google Colab](https://colab.research.google.com/)
2. Haz clic en "GitHub" en la pestaña de fuentes
3. Pega esta URL: `https://github.com/gracobjo/sentencias`
4. Busca y selecciona: `docs/Analizador_Sentencias_Colab.ipynb`

### **Paso 2: Configurar el Entorno**

#### Ejecutar Celdas de Instalación
1. **Celda 1**: Instalación de dependencias
   - Haz clic en el botón ▶️ o presiona `Shift + Enter`
   - Espera a que se instalen todas las librerías
   - Verás mensajes como "✅ Dependencias instaladas correctamente"

2. **Celda 2**: Creación de modelos
   - Ejecuta para crear el directorio `models/`
   - Se generará el archivo `frases_clave.json`

3. **Celda 3**: Clases de análisis
   - Se crearán las clases `AnalizadorLegalColab` y `AnalizadorPredictivoColab`
   - Verás "✅ Analizador Legal para Colab inicializado correctamente"

### **Paso 3: Probar Funcionalidades Básicas**

#### Análisis de Documento de Ejemplo
1. Ejecuta la celda con el texto de ejemplo
2. Verás el resultado del análisis:
   ```
   🔍 RESULTADO DEL ANÁLISIS:
   📊 Clasificación: Sentencia Judicial
   📈 Confianza: 85.00%
   🏛️ Instancia: Tribunal Supremo
   🔑 Frases clave encontradas: 5
   ```

#### Análisis Predictivo
1. Ejecuta las celdas de entrenamiento del modelo
2. Prueba las predicciones de ejemplo
3. Verás resultados como:
   ```
   🎯 Predicción: Favorable
   📊 Probabilidad favorable: 75.5%
   🎲 Confianza del modelo: 78.2%
   ```

### **Paso 4: Visualizaciones**

#### Gráficos Estáticos (Matplotlib)
1. Ejecuta las celdas de visualización
2. Si matplotlib no está disponible, verás mensajes informativos
3. Los gráficos se mostrarán debajo de las celdas

#### Visualizaciones Interactivas (Plotly)
1. Ejecuta las celdas de Plotly
2. Los gráficos interactivos se mostrarán en línea
3. Puedes hacer zoom, hover y explorar los datos

### **Paso 5: Procesamiento de PDFs**

#### Subir Archivo PDF
1. Ejecuta la celda de procesamiento de PDF
2. Haz clic en "Subir archivo PDF para analizar"
3. Selecciona un archivo PDF desde tu computadora
4. El sistema extraerá el texto y lo analizará

#### Crear PDF de Ejemplo
1. Ejecuta la celda de creación de PDF
2. Se generará un archivo `sentencia_ejemplo.pdf`
3. Puedes descargarlo o procesarlo

### **Paso 6: Exportación de Resultados**

#### Exportar a JSON
```python
# Ejemplo de exportación
resultado = analizador_colab.analizar_texto(tu_texto)
archivo_json = exportador.exportar_a_json(resultado, "mi_analisis.json")
```

#### Exportar a Word
```python
# Crear documento Word
archivo_word = exportador.exportar_a_word(resultado, "mi_analisis.docx")
```

#### Descargar Archivos
1. Haz clic derecho en el archivo generado
2. Selecciona "Descargar"
3. O usa el comando: `files.download('archivo.docx')`

### **Paso 7: Integración con Google Drive**

#### Conectar Google Drive
1. Ejecuta: `conectar_google_drive()`
2. Autoriza el acceso en la ventana emergente
3. Los archivos estarán disponibles en `/content/drive/MyDrive/`

#### Guardar en Drive
```python
# Guardar resultado en Drive
ruta_drive = guardar_en_drive(resultado, "analisis_drive.json")
```

## 🔧 Solución de Problemas

### **Problemas Comunes**

#### **Error: "ModuleNotFoundError"**
```python
# Solución: Ejecutar celda de instalación
%pip install nombre_del_modulo
```

#### **Error: "FileNotFoundError"**
```python
# Solución: Verificar que ejecutaste las celdas de instalación
diagnosticar_sistema()
```

#### **Error: "Memory Error"**
1. Ve a Runtime → Restart runtime
2. Ejecuta las celdas en orden
3. Usa datasets más pequeños

#### **Error: "Permission Denied"**
```python
# Solución: Verificar permisos de Google Drive
conectar_google_drive()
```

### **Comandos de Diagnóstico**

#### Verificar Sistema
```python
# Ejecutar diagnóstico completo
problemas = diagnosticar_sistema()
if problemas:
    solucionar_problemas()
```

#### Verificar Librerías
```python
# Verificar librerías específicas
try:
    import matplotlib.pyplot as plt
    print("✅ matplotlib disponible")
except ImportError:
    print("⚠️ matplotlib no disponible")
```

#### Verificar Archivos
```python
# Verificar archivos creados
import os
if os.path.exists('models/frases_clave.json'):
    print("✅ Archivo de frases clave existe")
else:
    print("❌ Archivo de frases clave no encontrado")
```

## 📊 Casos de Uso Avanzados

### **Análisis de Lote de Documentos**
```python
# Analizar múltiples documentos
documentos = ["texto1", "texto2", "texto3"]
resultados = []

for i, doc in enumerate(documentos):
    resultado = analizador_colab.analizar_texto(doc)
    resultados.append(resultado)
    print(f"Documento {i+1}: {resultado['clasificacion']}")
```

### **Análisis Comparativo**
```python
# Comparar múltiples casos
casos = [
    {"instancia": "TS", "tipo_lesion": "manguito_rotador", "edad": 45},
    {"instancia": "JS", "tipo_lesion": "hernia_discal", "edad": 38}
]

for caso in casos:
    prediccion = analizador_predictivo.predecir_caso(**caso)
    print(f"Caso: {prediccion['prediccion']} ({prediccion['probabilidad_favorable']}%)")
```

### **Personalización de Frases Clave**
```python
# Agregar frases clave personalizadas
frases_personalizadas = {
    "mi_especialidad": [
        "término específico 1",
        "término específico 2",
        "término específico 3"
    ]
}

# Cargar en el analizador
analizador_colab.frases_clave.update(frases_personalizadas)
```

## 🎯 Mejores Prácticas

### **Rendimiento**
1. Ejecuta las celdas en orden secuencial
2. No ejecutes múltiples celdas simultáneamente
3. Usa datasets pequeños para pruebas iniciales
4. Reinicia el runtime si hay problemas de memoria

### **Organización**
1. Guarda tus resultados regularmente
2. Usa nombres descriptivos para archivos
3. Documenta tus análisis con comentarios
4. Exporta resultados importantes

### **Colaboración**
1. Comparte el notebook con otros usuarios
2. Usa Google Drive para archivos compartidos
3. Documenta cambios y mejoras
4. Reporta problemas en GitHub Issues

## 📞 Soporte Adicional

### **Recursos de Ayuda**
- [Documentación de Google Colab](https://colab.research.google.com/notebooks/intro.ipynb)
- [Tutorial de Python](https://docs.python.org/3/tutorial/)
- [Documentación de Scikit-learn](https://scikit-learn.org/stable/user_guide.html)

### **Comunidad**
- [GitHub Issues](https://github.com/gracobjo/sentencias/issues)
- [GitHub Discussions](https://github.com/gracobjo/sentencias/discussions)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-colaboratory)

### **Contacto Directo**
- **Email**: Ver repositorio principal
- **GitHub**: [@gracobjo](https://github.com/gracobjo)
- **Web**: [sentencias.onrender.com](https://sentencias.onrender.com)

---

**¡Disfruta explorando el análisis inteligente de documentos legales! 🚀**
