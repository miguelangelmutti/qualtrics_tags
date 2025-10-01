# Qualtrics Tags Transformer

Herramienta para transformar la jerarquía profunda de etiquetas (tags) generadas por Qualtrics en un formato tabular plano (CSV).

## 📋 Descripción

Qualtrics genera etiquetas para los comentarios de encuestas en un formato JSON con estructura jerárquica anidada. Este proyecto convierte esa jerarquía compleja en tablas CSV, donde cada nivel de profundidad se representa como una columna separada, facilitando el análisis en herramientas como Excel.

### Problema que resuelve

Qualtrics exporta las etiquetas de los comentarios en un formato JSON con operaciones de tipo:
- `insert_topic`: Define las etiquetas individuales
- `move_topics`: Establece las relaciones padre-hijo entre etiquetas
- `rootNodes`: Define los nodos raíz de la jerarquía

Este formato jerárquico anidado es difícil de analizar directamente. Esta herramienta lo transforma en un formato tabular plano donde:
- Cada fila representa una ruta completa desde el nodo raíz hasta una hoja
- Cada columna representa un nivel de profundidad (Nivel 1, Nivel 2, Nivel 3, etc.)

## 🚀 Características

- **Procesamiento recursivo**: Maneja jerarquías de cualquier profundidad
- **Interfaz interactiva**: Menú para seleccionar archivos JSON de la carpeta
- **Formato configurable**: Exportación a CSV con encoding UTF-8 y separador personalizable
- **Limpieza automática**: Elimina archivos JSON intermedios después del procesamiento
- **Manejo de errores**: Control de permisos, archivos faltantes y excepciones

## 📁 Estructura del Proyecto

```
qualtrics_tags/
├── Json/                    # Carpeta con archivos JSON de entrada
│   └── stackoverflow.json   # Ejemplo de estructura Qualtrics
├── csv/                     # Carpeta de salida para archivos CSV
├── tags.py                  # Versión inicial del transformador
├── tags_refactor.py         # Versión mejorada (PRINCIPAL)
├── pruebita.py              # Script de prueba/ejemplo
├── Pipfile                  # Dependencias del proyecto (pipenv)
├── Pipfile.lock             # Versiones bloqueadas de dependencias
├── requeriments.txt         # Dependencias alternativas (pip)
└── README.md                # Este archivo
```

## 🔧 Instalación

### Requisitos
- Python 3.7+
- pandas

### Instalación con pipenv (recomendado)
```bash
pipenv install
pipenv shell
```

### Instalación con pip
```bash
pip install -r requeriments.txt
```

## 💻 Uso

### Ejecución principal

```bash
python tags_refactor.py
```

El programa:
1. Lista todos los archivos `.json` en la carpeta `Json/`
2. Permite elegir el archivo a transformar
3. Genera un CSV en la carpeta `csv/` con el formato tabular

### Formato de entrada (JSON)

El archivo JSON debe tener la estructura de Qualtrics:

```json
{
  "version": "2.0",
  "operations": [
    {
      "operation": "insert_topic",
      "topic": {
        "topicId": "Topic_123",
        "label": "H1 Parent Topic A",
        "query": "apples",
        "baseQuery": "apples"
      }
    },
    {
      "operation": "move_topics",
      "parentLabel": "H1 Parent Topic A",
      "childLabels": ["H2 Topic A1", "H2 Topic A2"]
    }
  ],
  "rootNodes": ["H1 Parent Topic A", "H1 Parent Topic B"]
}
```

### Formato de salida (CSV)

El CSV resultante tiene columnas `nivel 1`, `nivel 2`, `nivel 3`, etc.:

| nivel 1           | nivel 2      | nivel 3       |
|-------------------|--------------|---------------|
| H1 Parent Topic A | H2 Topic A1  | H3 Topic A1   |
| H1 Parent Topic A | H2 Topic A1  | H3 Topic A2   |
| H1 Parent Topic A | H2 Topic A2  |               |
| H1 Parent Topic B | H2 Topic B1  |               |

## 🔍 Archivos del Proyecto

### `tags_refactor.py` ⭐ (Principal)
Versión mejorada y refactorizada con:
- Menú interactivo para selección de archivos
- Procesamiento recursivo de jerarquías
- Manejo robusto de errores
- Limpieza automática de archivos temporales

### `tags.py`
Versión inicial con lógica básica de transformación (sin recursión completa)

### `pruebita.py`
Script simple para pruebas y extracción básica de topics

## 🛠️ Funciones Principales

### En `tags_refactor.py`:

- `listar_archivos_json(carpetapath)`: Lista archivos JSON en una carpeta
- `elegir_archivo(archivos_json)`: Menú interactivo de selección
- `tags_to_json(archivo)`: Convierte JSON de Qualtrics a formato jerárquico
- `process_operations(node, operations)`: Procesa recursivamente la jerarquía
- `json_to_dataframe(data_in)`: Aplana la jerarquía a DataFrame
- `df_to_csv(df, filename)`: Exporta DataFrame a CSV con formato

## 📚 Referencia

Este proyecto está inspirado en la solución a este problema de StackOverflow:
https://stackoverflow.com/questions/75450146/create-flat-excel-table-from-json-file-that-includes-a-hierarchy-parent-and-chil

## 🤝 Contribuciones

Las mejoras y sugerencias son bienvenidas. El proyecto está en desarrollo activo.

## 📝 Notas

- Los archivos JSON intermedios (`*_jerarquia.json`) se eliminan automáticamente después del procesamiento
- El CSV se genera con encoding UTF-8 con BOM (`utf_8_sig`) para compatibilidad con Excel
- El separador predeterminado es punto y coma (`;`) para compatibilidad con Excel en configuraciones regionales que usan coma decimal

