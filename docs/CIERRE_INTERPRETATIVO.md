# Cierre interpretativo

## LAB04 — Localización, aprobación y auditoría del corpus

**Resultado principal:** se evaluaron dos datasets candidatos (`docs/dataset_candidates.csv`) y se aprobó SMS Spam Collection (UCI, CC BY 4.0) frente a IMDB, descartado por no tener licencia identificada en su ficha oficial.

**Evidencia de calidad y procedencia:** 5,572 mensajes tras limpieza (5,574 filas crudas, 0 valores nulos), con 403 duplicados de texto identificados y excluidos antes de dividir en entrenamiento/prueba. SHA-256 del archivo auditado: `d368d659ea5fa1c2cbf9f6be756622b4329ef8c3bf105572c03eb0741f908701`. Fuente, licencia, diccionario de datos y procedimiento de obtención documentados en `docs/DATASET_CARD.md`.

**Riesgo o sesgo identificado:** desbalance de clases (86.6 % ham / 13.4 % spam) y corpus en inglés de 2011-2012, por lo que no cubre patrones de spam más recientes (enlaces cortos, QR, fraude por voz) ni otros idiomas.

**Decisión de aprobación o rechazo:** aprobado para este ejercicio académico, con la salvedad de que no representa el spam actual ni debe usarse para decisiones automatizadas sin supervisión.

**Limitación que debe comunicarse:** los resultados de este modelo no deben extrapolarse a mensajes fuera del dominio (otro idioma, otro canal, spam posterior a 2012).

**Siguiente verificación:** ampliar el corpus con ejemplos recientes antes de cualquier uso fuera del contexto académico.

## LAB05 — Clasificación de texto: TF-IDF, Naive Bayes y modelo lineal

**Resultado principal:** la regresión logística superó a Naive Bayes y al baseline en F1 macro de prueba (0.951 vs. 0.928 vs. 0.466).

**Modelo seleccionado y evidencia:** regresión logística con `TfidfVectorizer(ngram_range=(1,2))` y `class_weight="balanced"`, evaluada con una sola partición estratificada 75/25 (`random_state=42`). Métricas completas en `reports/text_metrics.csv`; matriz de confusión en `reports/confusion_text.png`.

**Clase con mayor dificultad:** `spam`, con recall de 0.93 frente a 0.99 de `ham` — consistente con el desbalance de clases.

**Tipo de error más frecuente:** `vocabulario_de_llamada_ambiguo` (7 de 28 errores categorizados): mensajes personales legítimos que mencionan "call"/"free" se confunden con spam de líneas de pago. Detalle completo en `reports/analizar_errores.md`.

**Impacto en el contexto:** los falsos negativos de spam explícito (4 casos) son más costosos que los falsos positivos, porque dejarían pasar contenido no deseado sin filtrar.

**Limitación del dataset:** corpus pequeño y desbalanceado para la clase minoritaria (`spam`), lo que limita la capacidad del modelo de generalizar a formas de spam poco representadas en el entrenamiento.

**Decisión antes del despliegue:** no publicar como filtro automático sin supervisión humana; antes de un uso real, ajustar el umbral de decisión para priorizar el recall de `spam` y ampliar el corpus de entrenamiento.
