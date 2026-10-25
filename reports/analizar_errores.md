# Análisis de errores · Clasificador de texto (SMS Spam Collection)

## Resultado principal

La regresión logística obtuvo el mejor F1 macro de prueba (0.951), por encima de Naive Bayes (0.928) y muy por encima del baseline `DummyClassifier` (0.466, que predice siempre `ham` y no detecta ningún `spam`). Ambos pipelines comparables superan ampliamente el baseline, confirmando que el vocabulario por sí solo (TF-IDF con unigramas y bigramas) separa razonablemente bien las dos clases en este corpus.

| Modelo | F1 macro (prueba) |
|---|---|
| logistic | 0.951 |
| naive_bayes | 0.928 |
| dummy (baseline) | 0.466 |

## Clase con mayor dificultad

La clase `spam` tiene el menor recall (0.93 en logística, frente a 0.99 en `ham`), como es esperable en un dataset desbalanceado (86.6 % ham / 13.4 % spam): hay muchas menos señales de entrenamiento para los patrones de spam. De los 28 errores sobre 1,293 casos de prueba, 12 son falsos negativos (spam real clasificado como ham) y 16 son falsos positivos (ham real clasificado como spam).

## Tipo de error más frecuente

Categorizando los 28 errores de la regresión logística (ver `reports/error_analysis.csv`):

| Categoría | Casos | Descripción |
|---|---|---|
| `vocabulario_de_llamada_ambiguo` | 7 | Mensajes `ham` legítimos que piden o mencionan una llamada ("call me", "are you free now?") y comparten vocabulario con el spam de líneas telefónicas de pago. |
| `spam_explicito_no_detectado` | 4 | Spam de contenido sexual/adulto que el modelo no detecta (falso negativo); vocabulario explícito pero con pocas repeticiones en el corpus de entrenamiento. |
| `vocabulario_promocional_en_mensaje_personal` | 3 | Mensajes `ham` que usan palabras típicas de promociones ("free download", "offer", "daily text") en un contexto personal. |
| `spam_promocional_sin_marcadores_clasicos` | 3 | Spam promocional (concursos, noticias falsas, ofertas de restaurantes) sin los marcadores típicos (números de teléfono, mayúsculas, símbolos de moneda) que el modelo aprendió a asociar con spam. |
| `texto_demasiado_corto` | 3 | Mensajes muy breves (menos de 25 caracteres) con poca señal léxica para TF-IDF. |
| `spam_disfrazado_de_notificacion_benigna` | 2 | Spam redactado como una notificación neutra ("missed call alert", mensaje personal con tarifa oculta al final) que el modelo lee como `ham`. |
| `mensaje_alarmista_no_comercial` | 2 | Mensajes `ham` de advertencia o cadena (alertas de seguridad, bulos) con tono urgente que comparte vocabulario con el spam. |
| `etiqueta_discutible` | 2 | Casos donde la etiqueta original del corpus es cuestionable (una queja personal etiquetada como spam; un aviso de servicio etiquetado como ham que en realidad tiene estructura de spam promocional). |
| `spam_con_errores_ortograficos` | 1 | Spam con errores de ortografía deliberados que reduce la coincidencia de n-gramas con el vocabulario de entrenamiento. |
| `vocabulario_financiero_en_contexto_personal` | 1 | Mensaje `ham` sobre una transferencia de dinero entre conocidos, con vocabulario financiero que el modelo asocia a spam. |

La categoría más frecuente, `vocabulario_de_llamada_ambiguo` (7 de 28, 25 %), implica que palabras como "call", "free" y "ring" son señales fuertes de spam en el corpus (muchas líneas de pago las usan), pero también aparecen en conversaciones cotidianas perfectamente legítimas. El modelo no distingue el contexto, solo el vocabulario.

## Impacto en el contexto

- Los **falsos positivos** (`ham`→`spam`, 16 casos) implican el riesgo de que un filtro automático bloquee o archive mensajes personales legítimos — el costo típico de un filtro de spam demasiado agresivo.
- Los **falsos negativos** (`spam`→`ham`, 12 casos) son más preocupantes en este dominio: 4 de ellos (`spam_explicito_no_detectado`) son contenido sexual explícito que llegaría sin filtrar al usuario. En un sistema de producción, este tipo de error pesaría más que un falso positivo ocasional.

## Limitación del dataset

El corpus tiene 403 textos duplicados (excluidos del entrenamiento y la prueba para evitar fuga de información) y está fuertemente desbalanceado (13.4 % spam). Es un corpus en inglés de 2011-2012, por lo que patrones de spam más recientes (enlaces cortos, códigos QR, deepfakes de voz) no están representados y el modelo no debe asumirse vigente para ese tipo de amenazas.

## Decisión antes del despliegue

Por ello proponemos **no publicar este modelo como filtro automático sin supervisión humana**, especialmente para los mensajes que caen en vocabulario ambiguo de llamada ("call", "free", "ring"). Antes de un uso real convendría: (a) ampliar el corpus con ejemplos recientes y en el idioma de destino; (b) ajustar el umbral de decisión para priorizar el recall de `spam` dado el costo asimétrico de los falsos negativos; y (c) mantener una revisión manual para los casos de confianza baja del modelo.
