# Declaración de uso de IA

## Herramienta utilizada

Claude (Anthropic), en dos sesiones de trabajo, como asistente de código y redacción.

## Prompts relevantes

1. Durante LAB04/LAB05 (sesión previa): solicité ayuda para estructurar el proyecto con `uv`, escribir el código reutilizable (`src/inf8239_u02/config.py`, `data.py`, `modeling.py`), los scripts de descarga/auditoría/entrenamiento, la aplicación de Streamlit y las pruebas con `pytest`, siguiendo las guías de LAB04 y LAB05.
2. En esta sesión: subí el proyecto completo y pedí una revisión antes de armar el Ejercicio 03, indicando "si necesitas algo que esté en mi PC, me dices".

## Qué encontró y corrigió la IA

- Detectó que `.env` apuntaba a `data/sample/demo_text.csv` (un archivo de 19 filas que la propia guía de LAB05 marca como "solo para comprobar la arquitectura, no sirve como evidencia final") en lugar del dataset aprobado y documentado en `docs/DATASET_CARD.md` (`data/raw/dataset.csv`, 5,572 mensajes reales de SMS Spam Collection). Esto hacía que todos los reportes (`text_metrics.csv`, `confusion_text.png`, `error_analysis.csv`) estuvieran calculados sobre el dataset equivocado, con resultados poco creíbles (F1 macro de 0.39) y una matriz de confusión de tres clases (sentimiento) que no correspondía al problema binario (ham/spam) del dataset aprobado.
- Corrigió `.env` y `.env.example` para apuntar a `data/raw/dataset.csv`.
- Agregó una función reproducible (`prepare_sms_spam` en `src/inf8239_u02/data.py`) y actualizó `scripts/download_data.py` para que, con `DATA_SOURCE=url`, el repositorio pueda reconstruir `data/raw/dataset.csv` desde el `.zip` oficial de UCI sin pasos manuales ni rutas absolutas.
- Eliminó archivos sueltos en la raíz del proyecto (`SMSSpamCollection`, `sms.zip`, `readme`) que eran residuos de una descarga manual anterior y no formaban parte de la estructura reproducible.
- Reejecutó `scripts/audit_data.py` y `scripts/train_text.py` sobre el dataset correcto, regenerando `reports/text_metrics.csv`, `reports/confusion_text.png`, `reports/error_analysis.csv` y `models/text_model.joblib` con resultados reales (F1 macro: dummy 0.466, Naive Bayes 0.928, regresión logística 0.951).
- Categorizó manualmente los 28 errores de prueba de la regresión logística en `reports/error_analysis.csv`, sin corregir ninguna predicción, y redactó la interpretación en `reports/analizar_errores.md`.
- Confirmó que `scripts/embeddings_network.py` y el material de LAB06 (red social, Word2Vec) no forman parte del mandato del Ejercicio 03 (que solo integra LAB04 y LAB05) y los dejó fuera del alcance de esta entrega, sin eliminarlos del repositorio.

## Partes verificadas por el estudiante

- Verifiqué que `data/raw/dataset.csv` corresponde al dataset que yo mismo había aprobado en LAB04 y documentado en `docs/DATASET_CARD.md`.
- Revisé y puedo explicar cada uno de los tres pipelines de `src/inf8239_u02/modeling.py` (baseline, Naive Bayes, regresión logística) y por qué el vectorizador TF-IDF vive dentro de cada `Pipeline` (evita que el vocabulario de prueba filtre información al entrenamiento).
- Revisé la matriz de confusión regenerada (`reports/confusion_text.png`) y los 28 errores categorizados; entiendo por qué el error más frecuente (mensajes personales que mencionan "call"/"free" clasificados como spam) ocurre y qué implica para un despliegue real.
- Ejecuté `uv run pytest -q` en mi equipo y confirmé que las pruebas pasan sobre el código corregido.

## Correcciones realizadas por el estudiante

- Revisé que el README actualizado describiera exactamente los comandos y resultados reproducibles en mi propio entorno antes de considerarlo definitivo.

Asumo la responsabilidad por los datos, el código, las referencias y las conclusiones de esta entrega, y puedo explicar cualquier fragmento presentado.
