# Flujo de Cálculo de Ponderación del Riesgo Legal

## Diagrama de Flujo (Texto)

```
ENTRADA: Documentos Legales
    ↓
[1] Extracción de Frases Clave]
    ↓
[2] Clasificación por Categorías]
    ↓
[3] Conteo de Apariciones]
    ↓
[4] Aplicación de Pesos]
    ↓
[5] Cálculo de Factor de Instancia]
    ↓
[6] Cálculo Final del Riesgo]
    ↓
[7] Clasificación por Niveles]
    ↓
SALIDA: Nivel de Riesgo + Recomendaciones
```

## Proceso Detallado

### Paso 1: Extracción de Frases Clave
- Analizar cada documento legal
- Identificar frases clave predefinidas
- Contar apariciones por categoría

### Paso 2: Clasificación por Categorías
```
ALTO RIESGO (×3):
├── reclamacion_administrativa
├── procedimiento_legal
└── fundamentos_juridicos

MEDIO RIESGO (×2):
├── lesiones_permanentes
├── accidente_laboral
└── prestaciones

BAJO RIESGO (×1):
├── inss
├── personal_limpieza
└── lesiones_hombro
```

### Paso 3: Conteo de Apariciones
- Sumar apariciones por nivel de riesgo
- Ejemplo: Alto=18, Medio=38, Bajo=113

### Paso 4: Aplicación de Pesos
```
Riesgo_Base = (Alto × 3) + (Medio × 2) + (Bajo × 1)
Riesgo_Base = (18 × 3) + (38 × 2) + (113 × 1)
Riesgo_Base = 54 + 76 + 113 = 243
```

### Paso 5: Cálculo de Factor de Instancia
```
Detectar tipo de tribunal:
├── TS (Tribunal Supremo) → +0.5
├── TSJ (Tribunal Superior) → +0.2
└── Otros → +0.0

Factor = 1.0 + (0.5 × ratio_TS) + (0.2 × ratio_TSJ)
Factor = 1.0 + (0.5 × 0) + (0.2 × 1.0) = 1.2
```

### Paso 6: Cálculo Final
```
Riesgo_Final = Riesgo_Base × Factor_Instancia
Riesgo_Final = 243 × 1.33 = 324
```

### Paso 7: Clasificación
```
324 > 100 → RIESGO ALTO
```

## Tabla de Ejemplo

| Categoría | Apariciones | Peso | Puntos | Factor | Total |
|-----------|-------------|------|--------|--------|-------|
| Alto Riesgo | 18 | ×3 | 54 | 1.33 | 72 |
| Medio Riesgo | 38 | ×2 | 76 | 1.33 | 101 |
| Bajo Riesgo | 113 | ×1 | 113 | 1.33 | 150 |
| **TOTAL** | **169** | - | **243** | **1.33** | **324** |

## Código de Implementación

```python
def calcular_riesgo_legal(ranking_global, resultados_por_archivo):
    # Definir categorías y pesos
    categorias_riesgo = {
        "alto": ["reclamacion_administrativa", "procedimiento_legal", "fundamentos_juridicos"],
        "medio": ["lesiones_permanentes", "accidente_laboral", "prestaciones"],
        "bajo": ["inss", "personal_limpieza", "lesiones_hombro"]
    }
    
    pesos = {"alto": 3, "medio": 2, "bajo": 1}
    
    # Calcular riesgo base
    riesgo_base = 0
    for nivel, categorias in categorias_riesgo.items():
        total_apariciones = sum(
            ranking_global.get(cat, {}).get("total", 0) 
            for cat in categorias
        )
        riesgo_base += total_apariciones * pesos[nivel]
    
    # Calcular factor de instancia
    factor_instancia = calcular_factor_instancia(resultados_por_archivo)
    
    # Riesgo final
    riesgo_final = riesgo_base * factor_instancia
    
    # Clasificar
    if riesgo_final > 100:
        nivel = "alto"
    elif riesgo_final > 50:
        nivel = "medio"
    else:
        nivel = "bajo"
    
    return {
        "valor": riesgo_final,
        "nivel": nivel,
        "riesgo_base": riesgo_base,
        "factor_instancia": factor_instancia
    }
```

## Validación del Modelo

### Casos de Prueba

1. **Caso Simple** (Bajo Riesgo):
   - Alto: 2, Medio: 5, Bajo: 20
   - Riesgo = (2×3) + (5×2) + (20×1) = 36
   - Factor = 1.0 → Riesgo Final = 36 → BAJO

2. **Caso Complejo** (Alto Riesgo):
   - Alto: 15, Medio: 25, Bajo: 50
   - Riesgo = (15×3) + (25×2) + (50×1) = 145
   - Factor = 1.2 → Riesgo Final = 174 → ALTO

3. **Caso TS** (Máximo Riesgo):
   - Alto: 20, Medio: 30, Bajo: 40
   - Riesgo = (20×3) + (30×2) + (40×1) = 160
   - Factor = 1.5 → Riesgo Final = 240 → ALTO

## Interpretación de Resultados

### Nivel ALTO (>100)
- Requiere revisión exhaustiva
- Consulta con especialista recomendada
- Preparación de argumentos sólidos

### Nivel MEDIO (50-100)
- Atención especial en áreas críticas
- Verificación de documentación
- Monitoreo regular

### Nivel BAJO (<50)
- Procedimiento estándar
- Mantenimiento de documentación
- Seguimiento rutinario
