# Dataset Card

## Identificación

-Nombre: SMS Spam Collection
-Fuente original: https://archive.ics.uci.edu/dataset/228/sms+spam+collection (DOI: https://doi.org/10.24432/C5CC84)
-Responsable: Tiago A. Almeida y José María Gómez Hidalgo (creadores, según UCI). Responsable del uso en este proyecto: Jose Berroa
-Versión o fecha: publicado en UCI el 2012-06-21; descargado en octubre de 2026 (registrar fecha exacta y SHA-256 de SMSSpamCollection)
-Licencia: CC BY 4.0 (atribución obligatoria). Cita: Almeida, T. & Hidalgo, J. (2011). SMS Spam Collection [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84
-Idioma: inglés

## Propósito y variable objetivo

Uso académico en el curso INF8239 (Unidad 02, NLP): entrenar y evaluar un clasificador binario que determine si un mensaje de texto es spam o ham (legítimo). La variable objetivo es label. Los resultados derivados pueden publicarse citando la fuente, según CC BY 4.0.

## Diccionario de datos
Diccionario de datos
Archivo del proyecto: data/raw/dataset.csv (5,574 filas, 2 columnas).

| Columna | Tipo | Descripción | Valores o unidad |
|Label |Texto (Categorica)|(categórica)	Clase del mensaje; variable objetivo|ham (legítimo) o spam. Sin unidad|

|Text|texto|Contenido bruto del SMS, sin normalizar|Cadena libre en inglés. Sin unidad| 

## Procedimiento de obtención

-Descarga del ZIP original desde UCI (https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip) y extracción de SMSSpamCollection, un archivo de texto separado por tabulaciones, sin encabezado.

-Lectura con sep="\t", names=["label", "text"] y quoting=3 (sin interpretar comillas, para conservar las 5,574 líneas).

-Guardado como CSV UTF-8 en data/raw/dataset.csv. Configuración en .env: DATA_SOURCE=local, DATASET_PATH=data/raw/dataset.csv, TEXT_COLUMN=text, TARGET_COLUMN=label.

-No se limpió el texto, no se eliminaron duplicados ni se rebalancearon las clases. Solo los ejemplos de la sección anterior están enmascarados.

-Origen de los mensajes según UCI: spam de un foro británico (Grumbletext, 425) y del SMS Spam Corpus v0.1 Big (322); ham del NUS SMS Corpus, de voluntarios de la Universidad Nacional de Singapur que sabían que sus mensajes serían públicos (3,375), de una tesis doctoral (450) y del SMS Spam Corpus v0.1 Big (1,002).

## Calidad observada

-Observaciones: 5,574.
-Nulos: 0 (UCI declara que no hay valores faltantes).
-Clases: ham 4,827 (86.6 %) y spam 747 (13.4 %). La clase minoritaria es spam.
-Textos duplicados: unos 400 (403 en una lectura preliminar). Se conservan. Confirmar la cifra exacta con calidad_sms.py y actualizar este punto.
-Etiquetas binarias sin ambigüedad de definición. Las etiquetas vienen de la fuente y no se revalidaron.

## Población cubierta y excluida

-Cubierta: mensajes SMS en inglés de usuarios del Reino Unido (spam reportado en un foro) y de estudiantes de Singapur (ham), de una colección publicada entre 2011 y 2012.

-Excluida: otros idiomas (incluido el español), otros países y regiones, otros grupos de edad, canales distintos de SMS (WhatsApp, correo, redes sociales) y periodos posteriores a 2012.

## Riesgos, sesgos y usos prohibidos

Sesgos previsibles

- Fuentes distintas por clase: un modelo puede aprender el estilo de la fuente (vocabulario, ortografía, "Singlish") y no solo el spam.

-Desbalance: spam es el 13.4 % del total; la exactitud (accuracy) engaña, así que usar F1, recall y estratificación.

-Antigüedad: el spam actual (phishing, enlaces acortados, apps de mensajería) está poco representado.

-Los duplicados pueden inflar la evaluación si caen en train y test.

-Riesgos de privacidad: son mensajes reales de personas. UCI no declara cómo se anonimizaron, así que pueden contener nombres, teléfonos o datos personales dentro del texto.

Usos prohibidos

-Intentar identificar o contactar a remitentes o destinatarios.

-Publicar mensajes completos más allá de ejemplos mínimos y enmascarados.

-Usarlo como filtro de spam en producción sin validar con datos actuales y del idioma real de los usuarios.

-Inferir características personales o sensibles de quienes escribieron los mensajes.

-Vigilar o clasificar comunicaciones privadas reales.

-Redistribuirlo sin atribuir a los autores según CC BY 4.0.
