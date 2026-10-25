# INF-8239 · Unidad 02 · Ejercicio 03 — Corpus público y clasificador de texto reproducible

Autor: Jose Rafael Berroa Castillo

¿Puede un modelo distinguir, a partir únicamente del texto de un SMS, si es correo no deseado (`spam`) o un mensaje legítimo (`ham`)?

- **Dataset:** [SMS Spam Collection](https://doi.org/10.24432/C5CC84) (UCI, id 228, CC BY 4.0). 5,572 mensajes (tras limpieza de duplicados), 2 columnas (`label`, `text`). Detalle completo de procedencia, licencia y riesgos en `docs/DATASET_CARD.md`.
- **Resultado:** F1 macro en prueba de 0.466 (baseline) → 0.928 (Naive Bayes) → **0.951 (regresión logística, modelo elegido)**. Detalle en `reports/text_metrics.csv` y `reports/analizar_errores.md`.
- **Errores analizados:** 28 casos categorizados en `reports/error_analysis.csv` (ver interpretación en `reports/analizar_errores.md`).
- **Aviso:** ejercicio académico; no usar como filtro de producción sin supervisión humana (ver limitaciones en `reports/analizar_errores.md`).

## Instalación

Requiere Python 3.12 y [`uv`](https://docs.astral.sh/uv/). Desde la raíz del repositorio:

```bash
uv python install 3.12
uv sync
```

## Datos

El dataset aprobado y su ficha completa están en `data/raw/dataset.csv` y `docs/DATASET_CARD.md`. Si el archivo no está presente, se puede reconstruir de forma reproducible:

```bash
uv run python scripts/download_data.py
```

Con `DATA_SOURCE=url` en `.env`, el script descarga el `.zip` oficial de UCI, extrae `SMSSpamCollection` (texto separado por tabulador) y lo guarda como `data/raw/dataset.csv` con columnas `label,text`. Con `DATA_SOURCE=local` (valor por defecto una vez descargado), el script solo verifica que el archivo exista. Los datos no se versionan (`data/raw/*` está en `.gitignore`).

`data/sample/demo_text.csv` es un archivo de 19 filas que **solo sirve para comprobar la arquitectura** (LAB05); no se usa como evidencia final — toda la entrega corre sobre `data/raw/dataset.csv`.

## Auditoría y pruebas

```bash
uv run python scripts/audit_data.py
uv run pytest -q
```

La auditoría reporta ruta, SHA-256, forma, nulos, duplicados, distribución de clases y percentiles de longitud de texto (ver salida esperada en `docs/DATASET_CARD.md`).

## Entrenamiento y evaluación

```bash
uv run python scripts/train_text.py
```

Entrena tres pipelines (`DummyClassifier` como baseline, `ComplementNB`, regresión logística con `class_weight="balanced"`), todos con `TfidfVectorizer` (unigramas y bigramas) dentro del `Pipeline` para evitar fuga de datos. Usa una sola partición estratificada 75/25 (`random_state=42`); duplicados y nulos se eliminan antes de dividir. Genera:

- `reports/text_metrics.csv` — F1 macro por modelo.
- `reports/confusion_text.png` — matriz de confusión del modelo elegido (regresión logística).
- `reports/error_analysis.csv` — los 28 errores de prueba, categorizados manualmente.
- `models/text_model.joblib` — modelo serializado.

## Demostración local

```bash
uv run streamlit run app/streamlit_app.py
```

La interfaz advierte explícitamente que la predicción no constituye una decisión automática y que debe interpretarse dentro de las limitaciones documentadas del dataset.

## Estructura

```
src/inf8239_u02/   código reutilizable (config, data, modeling)
scripts/           descarga, auditoría y entrenamiento reproducibles
app/               demostración local en Streamlit
tests/             pruebas con pytest
docs/              ficha del dataset, candidatos evaluados
reports/           métricas, matriz de confusión, errores categorizados, análisis
data/raw/          dataset aprobado (no versionado)
data/sample/       archivo de 19 filas solo para verificar arquitectura
models/            modelo serializado (no versionado)
```

## Decisiones clave

- **Selección del dataset:** se evaluaron dos candidatos (`docs/dataset_candidates.csv`); se aprobó SMS Spam Collection por tener licencia clara (CC BY 4.0), tamaño adecuado y variable objetivo bien definida; se rechazó IMDB por licencia no identificada en la ficha oficial.
- **Prevención de fuga:** el `TfidfVectorizer` vive dentro de cada `Pipeline`, por lo que solo aprende vocabulario del conjunto de entrenamiento. Los 403 duplicados de texto se eliminan antes de dividir en entrenamiento/prueba.
- **Métrica principal:** F1 macro, por el desbalance de clases (86.6 % ham / 13.4 % spam).
- **Modelo elegido:** regresión logística, por su mejor F1 macro (0.951) y mejor recall de `spam` frente a Naive Bayes.
- **Análisis de errores:** los 28 errores de prueba se categorizaron manualmente sin corregir las predicciones; la categoría más frecuente (`vocabulario_de_llamada_ambiguo`, 7 casos) muestra que el modelo confunde mensajes personales que mencionan "call"/"free" con spam de líneas de pago. Detalle completo en `reports/analizar_errores.md`.

## Herramientas de IA utilizadas

Ver `docs/USO_DE_IA.md` para la declaración completa de asistencia de IA, partes verificadas y correcciones realizadas.

## Licencia y cita

Datos bajo CC BY 4.0. Cita: Almeida, T. y Hidalgo, J. (2011). *SMS Spam Collection* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84
