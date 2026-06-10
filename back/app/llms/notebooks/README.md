# 🧠 Notebooks de Machine Learning - IRCA

Documentación y experimentos de modelos de Machine Learning para predicción del Índice de Riesgo de Calidad del Agua (IRCA).

## 📁 Estructura de Directorios

```
notebooks/
├── exploracion/              # Análisis exploratorio y pruebas iniciales
│   ├── 01_clasificacion_irca.ipynb
│   └── 02_prediccion_irca.ipynb
│
├── experimentos/             # Experimentación y comparación de modelos
│   └── 01_experimentos_mlp.ipynb
│
└── modelos_finales/          # Modelos entrenados y listos para producción
    ├── 01_modelo_mlp_final.ipynb
    └── modelo_irca_best.joblib
```

---

## 📚 Descripción de Notebooks

### 🔍 **Exploración** (`exploracion/`)

#### `01_clasificacion_irca.ipynb`
- **Objetivo**: Clasificación de la calidad del agua basada en rangos IRCA
- **Contenido**: 
  - 18 celdas de código, 5 de markdown
  - Instalación de librerías (pandas, scikit-learn, seaborn, matplotlib, scipy)
  - Análisis exploratorio de datos
  - Modelos de clasificación
- **Estado**: Experimentos iniciales

#### `02_prediccion_irca.ipynb`
- **Objetivo**: Predicción numérica del valor IRCA
- **Contenido**: 
  - 19 celdas de código, 5 de markdown
  - Similar a clasificación pero enfocado en regresión
  - Predicción de valores continuos
- **Estado**: Experimentos iniciales

---

### 🧪 **Experimentación** (`experimentos/`)

#### `01_experimentos_mlp.ipynb`
- **Título**: Entrenamiento, comparación y análisis visual de modelos MLPRegressor
- **Objetivo**: Comparación sistemática de arquitecturas de redes neuronales
- **Contenido**: 
  - 30 celdas de código, 6 de markdown
  - Pruebas con diferentes configuraciones de capas ocultas
  - Análisis de hiperparámetros (learning rate, activación, solver)
  - Visualizaciones de rendimiento
  - Métricas de evaluación (MAE, RMSE, R²)
- **Modelos probados**: Múltiples arquitecturas MLPRegressor
- **Estado**: Experimentos completos

---

### ✅ **Modelos Finales** (`modelos_finales/`)

#### `01_modelo_mlp_final.ipynb`
- **Título**: Modelo Final IRCA - Red Neuronal MLP
- **Objetivo**: Modelo de producción optimizado
- **Contenido**: 
  - 21 celdas de código, 20 de markdown
  - Arquitectura final seleccionada
  - Entrenamiento con mejores hiperparámetros
  - Validación exhaustiva
  - Análisis de errores
  - Exportación del modelo
- **Modelo generado**: `modelo_irca_best.joblib`
- **Estado**: ✅ Modelo en producción

#### `modelo_irca_best.joblib`
- **Tipo**: Modelo MLPRegressor serializado (joblib)
- **Tamaño**: 30KB
- **Uso**: Cargado por el backend FastAPI para predicciones en tiempo real
- **Ruta en API**: `/home/juan/proyectos/back/app/llms/notebooks/modelos_finales/modelo_irca_best.joblib`

---

## 🚀 Cómo Usar los Notebooks

### 1. **Instalar Dependencias**

```bash
cd /home/juan/proyectos/back
poetry install
```

### 2. **Activar Entorno Virtual**

```bash
poetry shell
```

### 3. **Iniciar Jupyter**

```bash
cd app/llms/notebooks
jupyter notebook
```

### 4. **Orden de Ejecución Recomendado**

Para entender el proceso completo de desarrollo:

1. **Exploración** → `exploracion/01_clasificacion_irca.ipynb`
2. **Exploración** → `exploracion/02_prediccion_irca.ipynb`
3. **Experimentación** → `experimentos/01_experimentos_mlp.ipynb`
4. **Modelo Final** → `modelos_finales/01_modelo_mlp_final.ipynb`

---

## 📊 Flujo de Trabajo

```
┌─────────────────────────────────────────────────────────────┐
│  1. EXPLORACIÓN                                             │
│  • Análisis de datos                                        │
│  • Pruebas iniciales de clasificación y regresión          │
│  • Identificación de features importantes                  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  2. EXPERIMENTACIÓN                                         │
│  • Comparación de múltiples arquitecturas MLP              │
│  • Grid search de hiperparámetros                          │
│  • Validación cruzada                                      │
│  • Selección del mejor modelo                              │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  3. MODELO FINAL                                            │
│  • Entrenamiento con arquitectura óptima                   │
│  • Validación exhaustiva                                   │
│  • Exportación: modelo_irca_best.joblib                    │
│  • Documentación completa                                  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  4. PRODUCCIÓN (FastAPI)                                    │
│  • Carga de modelo con joblib.load()                       │
│  • Endpoint: POST /api/predictions                         │
│  • Predicciones en tiempo real                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 Métricas del Modelo Final

| Métrica | Valor | Descripción |
|---------|-------|-------------|
| **R² Score** | Ver notebook | Coeficiente de determinación |
| **MAE** | Ver notebook | Error Absoluto Medio |
| **RMSE** | Ver notebook | Raíz del Error Cuadrático Medio |
| **Tamaño modelo** | 30KB | Modelo serializado |

---

## 🔧 Mantenimiento

### Reentrenar el Modelo

Si necesitas actualizar el modelo con nuevos datos:

1. Abrir `modelos_finales/01_modelo_mlp_final.ipynb`
2. Actualizar la fuente de datos (conexión a DB)
3. Ejecutar todas las celdas
4. Verificar métricas de evaluación
5. Guardar nuevo modelo como `modelo_irca_best.joblib`
6. Reiniciar el backend FastAPI para cargar el nuevo modelo

### Agregar Nuevos Experimentos

1. Crear nuevo notebook en `experimentos/`
2. Usar nomenclatura: `0X_nombre_experimento.ipynb`
3. Documentar objetivo, metodología y resultados
4. Si supera al modelo actual, mover a `modelos_finales/`

---

## 📝 Notas Importantes

- **NO eliminar** `modelo_irca_best.joblib` - usado por el backend en producción
- Los notebooks en `exploracion/` son referencia histórica
- El notebook `experimentos/01_experimentos_mlp.ipynb` contiene la investigación principal
- El modelo final fue seleccionado basándose en métricas de validación cruzada

---

## 🛠️ Dependencias Principales

```python
pandas>=2.2.3
scikit-learn>=1.6.1
seaborn>=0.13.2
matplotlib>=3.10.6
scipy>=1.15.2
numpy>=2.2.5
joblib>=1.4.2
jupyter
```

---

## 📞 Soporte

Para dudas o mejoras en los modelos de ML:
- Revisar notebooks en orden secuencial
- Consultar métricas en `modelos_finales/01_modelo_mlp_final.ipynb`
- Verificar logs de entrenamiento en cada notebook

---

**Última actualización**: Mayo 7, 2026
**Modelo en producción**: MLPRegressor (modelo_irca_best.joblib)
**Framework**: scikit-learn 1.6.1
