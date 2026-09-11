# Un marco de evaluación para Natural Language Autoencoders

**Versión ciega para CoNaIISI 2026 (trabajo estudiantil).**

Universidad Tecnológica Nacional

---

## Resumen

Este trabajo presenta NLA Eval, una plataforma orientada a la evaluación sistemática de verbalizaciones de activación producidas por Natural Language Autoencoders (NLA). Un NLA comprime el vector de activación de un modelo de lenguaje en un texto breve y reconstruye ese vector a partir del texto. Ese texto, llamado Activation Verbalizer (AV), es un señalizador interpretable, no una lectura literal de las creencias del modelo. Neuronpedia permite inspeccionar un chat y un token a la vez, pero no cubre el ciclo completo de experimento sobre NLA públicos. Anthropic aplica un LLM como juez sobre AVs en un estudio de awareness de evaluación, como método interno de un paper, no como herramienta reutilizable. NLA Eval operacionaliza ese ciclo mediante datasets de prompts, una política de tokens, llamadas a la API de Neuronpedia, evaluadores configurables y una vista de comparación de corridas. El objeto evaluado es el AV en una posición de token, no la respuesta pública del modelo. La validación empírica en contextos de investigación y el acuerdo humano-juez sobre un corpus etiquetado constituyen los pasos siguientes para consolidar su impacto.

**Palabras clave:** Natural Language Autoencoders, interpretabilidad, LLM-as-judge, Neuronpedia, evaluación de modelos de lenguaje.

---

## 1. Introducción

Los modelos de lenguaje de gran escala (LLM) se evalúan, en la práctica industrial, sobre lo que dicen. Suites de prompts, métricas y jueces automáticos comparan respuestas, costos y tasas de error. Ese enfoque alcanza cuando el objeto de interés es la salida. Quiebra cuando el fenómeno vive en las activaciones internas y no aparece en el texto que el usuario lee.

Los Natural Language Autoencoders, introducidos por Fraser-Taliente y colaboradores en Transformer Circuits [1], atacan exactamente ese hueco. Un NLA es un autoencoder cuyo cuello de botella es texto en lenguaje natural. El Activation Verbalizer produce una verbalización. El Activation Reconstructor intenta recuperar el vector. El error de reconstrucción (MSE o RMSE) indica cuán leíble es esa verbalización, no si una frase aislada es verdadera.

Neuronpedia, en colaboración con Anthropic, hostea checkpoints públicos (por ejemplo Llama 3.3 70B con kitft-l53 y Gemma 3 27B con kitft-l41) y una API de completion y explain [2]. El producto es un microscopio. Un prompt, un modelo, una pestaña. Quien investiga un tema (un prior de foro, un riesgo, una awareness de evaluación) termina exportando capturas, eligiendo a mano el último token del usuario y el primero del asistente, y pegando verbalizaciones en otro chat para que un segundo modelo encuentre el patrón. Ese flujo no es un experimento. Es artesanía.

El presente trabajo presenta NLA Eval, una plataforma que cierra ese ciclo sobre NLA públicos. No se inventa el LLM-as-judge sobre verbalizaciones. Anthropic lo usó para marcar awareness de evaluación no verbalizada, con un grader sobre 50 tokens de respuesta y un 97 % de acuerdo con los autores en 186 ítems [1]. Se cambia el objeto evaluado y se materializa el laboratorio que hoy falta. El resto del artículo se organiza así. La Sección 2 formula las motivaciones. La Sección 3 resume el modelo conceptual. La Sección 4 describe la arquitectura. La Sección 5 detalla las funcionalidades de la plataforma. La Sección 6 diseña la validación. La Sección 7 discute limitaciones. La Sección 8 concluye. La Sección 9 sitúa las referencias de diseño que orientaron el recorte funcional.

---

## 2. Motivaciones

Tres tensiones justifican la plataforma.

Primero, el no determinismo. Un test clásico de API afirma que, dado un input, el output es uno. Un NLA, como el modelo que explica, no se presta a esa igualdad. Hace falta una política fija de tokens, un juez con rúbrica, y tasas a lo largo de un dataset, no una captura.

Segundo, la escala. El límite de explain de Neuronpedia (del orden de 16 posiciones por pedido y un tope horario) convierte cada comparación entre fuentes NLA en un trabajo de scripts y JSON. Sin un orquestador, el investigador elige el token interesante en cada corrida y destruye la comparabilidad.

Tercero, el vacío de herramienta. Las plataformas de evaluación de aplicaciones con IA operan sobre la salida visible. Neuronpedia no conoce datasets, claves de feedback ni gráficos de hit rate. Los jueces opcionales usados al entrenar un NLA puntúan calidad de entrenamiento (coherencia, unicidad), no hipótesis experimentales sobre AVs ya desplegados [1].

El motivo es fomentar investigación sobre NLA, no el entrenamiento de NLA nuevos, sistematizando lo que hoy se hace a mano con capturas y un chat.

---

## 3. Modelo conceptual

NLA Eval se organiza en torno a cinco objetos.

| Objeto | Rol |
|---|---|
| Dataset | Lista de prompts. Cada ejemplo admite una referencia opcional para el juez |
| Política de tokens | Qué posiciones se explican en cada corrida |
| Experimento | Una corrida sobre un dataset, una fuente NLA y un conjunto de evaluadores |
| Artefacto | completion, AVs, mse y token en las posiciones elegidas |
| Claves de feedback | Boolean (cumple o no), score (mínimo y máximo) o categoría |

Una política de tokens, por defecto, fija el último token de contenido del mensaje de usuario y el primer token de la respuesta del asistente. El investigador puede elegir una, la otra, o ambas. El MSE actúa como compuerta. Un AV con error alto no se lee como evidencia. Se reporta como verbalización poco reconstruible.

El juez no puntúa la creencia del modelo. Produce una señal interpretable. Si la rúbrica pide tema de foro o comunidad, un true no prueba un origen de corpus. Apoya una hipótesis que el output solo no mostraba, a validar con más tests [1].

Se distinguen tres tipos de evaluador.

1. Léxico o código. Subcadena. Barato y honesto. No captura tema.
2. LLM-as-judge, sin referencia. Rúbrica Mustache sobre el AV. Boolean, score o categoría, más un campo opcional de razonamiento.
3. Omisión, específico de NLA. El tema está en el AV y no en la completion. Es el análogo del awareness verbalizado frente al medido por NLA en [1].

Un evaluador pairwise (cuál de dos AVs se prefiere) forma parte del diseño y se implementa como extensión del núcleo.

---

## 4. Arquitectura

NLA Eval no entrena NLA. Orquesta APIs. La Figura 1 describe el ciclo de una fila. El dataset aporta el example. El run produce la completion y las verbalizaciones en las posiciones elegidas. El evaluador consume input, AV de entrada, AV de salida y, si hace falta, la completion, y calcula métricas.

**Figura 1.** El evaluador compara el ejemplo del dataset con las verbalizaciones NLA del token de entrada y del token de salida.

| Bloque | Rol |
|---|---|
| Example | Input = prompt del dataset |
| Run | Modelo + NLA. Output = completion |
| NLA usuario | Verbalización del último token de contenido |
| NLA asistente | Verbalización del primer token de respuesta |
| Evaluator | Métricas sobre AVs (y omisión frente a completion) |

La Figura 2 muestra el uso que organiza la plataforma. Dos configuraciones recorren el mismo dataset. Los evaluadores agregan tasas por experimento.

**Figura 2.** Varias versiones (modelo, capa, política de tokens) sobre un único dataset. Los evaluadores agregan métricas por experimento.

| Versión | Ejemplo |
|---|---|
| v1 | Llama 3.3 70B Instruct, kitft-l53, último token de usuario |
| v2 | Gemma 3 27B Instruct, kitft-l41, misma política |
| Dataset | Misma lista de prompts para ambas corridas |
| Evaluadores | Hit rate, score medio, categoría, MSE medio |

### 4.1. Interfaz de entrada y salida

La interfaz es el punto de interacción entre el investigador y NLA Eval. Por ella ingresan datasets, rúbricas y claves de API hacia un proxy. En sentido inverso, devuelve filas de experimento, celdas de feedback y gráficos, de modo que la plataforma apoye el análisis sin pretender que el AV reemplace el juicio sobre el instrumento.

### 4.2. Orquestador de experimento

El orquestador coordina el ciclo de cada ejemplo desde su ingreso hasta la persistencia de la fila. No ejecuta el NLA. Enruta tres pasos. POST de completion en Neuronpedia, con modelo e identificador de NLA. Selección de posiciones según la política y POST de explain. Para cada evaluador, un LLM u operación de código sobre el artefacto. El esquema JSON de salida lo dictan las claves de feedback.

El orquestador conserva resultados intermedios. Un GET posterior, en otro proceso, no pierde la corrida. En servidor local el almacén es un JSON. En despliegue el almacén es compartido. El filesystem efímero de una función serverless no es un laboratorio.

### 4.3. Capa NLA

Esta capa es un cliente. No reimplementa el autoencoder. Encapsula rate limits y el recorte de posiciones. Si explain falla, la fila queda con error y no se inventa un AV. Las fuentes previstas son Llama 3.3 70B Instruct con kitft-l53 y Gemma 3 27B Instruct con kitft-l41 como contraste, no como par equivalente de claim científico.

### 4.4. Capa juez

Los prompts del juez son plantillas Mustache. El mapeo fija qué variable es el AV agregado, el AV de último token de usuario, el de primer token de asistente, el prompt, la completion, el token, el MSE o una referencia humana. El formato de respuesta (boolean, score con min y max, categorías con descripción) estructura el JSON. El razonamiento es opcional. El juez se aplica al AV, no a la respuesta pública, salvo que la rúbrica lo pida (omisión).

### 4.5. Capa de comparación

La tabla de un run expone input, referencia, output (el AV) y una columna por clave de feedback. Boolean se muestra como 1.00 o 0.00 con color. Score se colorea entre mínimo y máximo. Categórica muestra el nombre. El encabezado informa el promedio. La comparación de dos experimentos reusa las mismas claves sobre el mismo dataset. El evaluador pairwise (Figura 3) opera sobre dos AVs del mismo example.

**Figura 3.** Evaluación pairwise. El juez elige entre dos verbalizaciones del mismo example (`preferred` en 0 o 1).

---

## 5. Funcionalidades de NLA Eval

NLA Eval se operacionaliza a través de una plataforma web que aplica política de tokens, evaluación y comparación en un entorno integrado. Su propuesta central no es almacenar chats, sino curar corridas, puntuar AVs y contrastar experimentos. Las funcionalidades siguientes cubren el ciclo completo que el módulo debe ejecutar.

### 5.1. Laboratorio y onboarding

La pantalla inicial describe el flujo. Claves de API, dataset, evaluador, corrida, comparación. El investigador ve de entrada qué objeto se puntúa (el AV) y qué no (la creencia del modelo).

### 5.2. Datasets

El módulo de datasets concentra la lista de prompts con identificador, texto y referencia opcional. Permite alta de ejemplos, edición y selección del conjunto sobre el que se dispara un experimento. Desde aquí se inicia la corrida y se accede a los runs ya persistidos.

### 5.3. Evaluadores

El módulo de evaluadores concentra rúbricas. Cada evaluador declara modelo de juez, plantilla, mapeo de variables y configuración de feedback. El formato de respuesta admite boolean, score (mínimo, máximo y descripciones de extremos) y categoría (nombre y descripción, con alta y baja de categorías). Include reasoning pide una justificación breve junto al score. Advanced reserva opciones de esquema. El investigador puede definir un juez de foro, de peligro o de evaluación sin modificar Neuronpedia.

### 5.4. Motor de corrida

El motor de corrida constituye la capa de ejecución. Elige fuente NLA, política de tokens y evaluadores, recorre el dataset, persiste cada fila y muestra el progreso. Si una explicación falla, la fila registra el error. El motor no reentrena el NLA. Encadena completion, explain y juez.

### 5.5. Tabla de filas y gráficos

Cada run se presenta como tabla. Columnas de input, referencia, output y claves de feedback, con celdas coloreadas según cumpla o no, según el score, o según la categoría. El encabezado informa el promedio de cada clave. El módulo de comparación agrupa dos o más experimentos del mismo dataset y produce gráficos de hit rate del juez y de MSE medio, de modo que se vea de inmediato si una fuente o una política cambia el señalizador interno.

### 5.6. Flujo pairwise

Una vez materializado el núcleo, cada par de AVs del mismo example accede a un juez de preferencia. La salida es `preferred` en 0 o 1 más razonamiento opcional. Ese flujo cubre el caso en que no basta un score absoluto y hace falta elegir entre dos verbalizaciones.

---

## 6. Diseño de validación

La validación empírica de NLA Eval se plantea en dos niveles complementarios.

A nivel de señal, se prevé un conjunto fijo de prompts (familia consejo, how-to, enciclopedia, un ítem en español), dos fuentes NLA (Llama 70B kitft-l53 y Gemma 27B kitft-l41), una política de tokens congelada, un juez booleano de tema de foro y un evaluador léxico. Las métricas de interés incluyen hit rate del juez, tasa léxica, tasa de omisión (AV sí, completion no), MSE medio, y el grado de coincidencia entre el juez y etiquetado humano sobre una muestra de AVs, en el espíritu del acuerdo reportado en [1], sin copiar ese número.

A nivel de plataforma, se diseñará un protocolo con investigadores que permita medir el tiempo para reproducir una comparación que hoy exige pestañas, la capacidad de un tercero de definir un juez distinto sin tocar Neuronpedia, y la confianza en las celdas de feedback. Los resultados permitirán ajustar rúbricas, política de tokens y parámetros del orquestador.

---

## 7. Limitaciones

El marco hereda los límites del instrumento. El NLA se entrena en una capa fija. El AV es un señalizador. El juez puede sesgarse hacia lexemas o hacia el propio prompt. Neuronpedia impone cupos. El pairwise y los jueces de código más allá del léxico quedan como extensión del núcleo. No hay NLA públicos sobre modelos base, así que no se replica el eje base frente a SFT de otros estudios de sesgo cultural [5]. Nada de esto autoriza a leer un AV como pensamiento.

---

## 8. Conclusiones y trabajos futuros

Este trabajo presentó NLA Eval, una plataforma para la evaluación de verbalizaciones NLA que operacionaliza datasets, política de tokens, evaluadores y comparación de corridas mediante un orquestador sobre la API de Neuronpedia. El aporte no es un método nuevo de interpretabilidad. Es convertir la inspección puntual y el grader ocasional de un paper en un laboratorio reutilizable.

Entre los trabajos futuros se destacan la ejecución del protocolo de la Sección 6, la implementación plena del flujo pairwise y la persistencia compartida en despliegue. Neuronpedia fomentó el acceso a NLA. NLA Eval apunta a fomentar investigaciones que los usen.

---

## 9. Referencias de diseño

El recorte de funcionalidades de NLA Eval no parte de una lista ad hoc. Se tomó como referencia la manera de trabajar de un framework altamente popular en la evaluación de aplicaciones basadas en LLM, organizado en datasets, experimentos, evaluadores con claves de feedback y vistas de comparación entre corridas [3]. Ese modo de trabajo, pensado para salidas de aplicaciones no deterministas, sirvió para diseñar los módulos de la plataforma. Dataset, rúbrica, corrida, tabla de filas y gráficos. El objeto evaluado cambia. No es la respuesta pública del modelo, sino el AV en una posición de token, con MSE y, cuando corresponde, omisión frente a la completion. La referencia es de método de laboratorio, no de identidad de producto.

---

## Referencias

[1] K. Fraser-Taliente et al., “Natural Language Autoencoders,” Transformer Circuits, may. 2026. [Online]. Available: https://transformer-circuits.pub/2026/nla/

[2] Neuronpedia, “Natural Language Autoencoders demo and API.” [Online]. Available: https://www.neuronpedia.org/nla

[3] LangChain, “LangSmith: evaluation and experiment tracking for LLM applications.” [Online]. Available: https://docs.smith.langchain.com/

[4] P. Kozak Riehme et al., “ARIA: Un Enfoque Inteligente para la Gestión y Mejora de Requerimientos en Entornos Ágiles,” CoNaIISI, 2026.

[5] J. Fernandez de Landa et al., “Why are all LLMs Obsessed with Japanese Culture? On the Hidden Cultural and Regional Biases of LLMs,” Findings of EMNLP, 2026.

[6] Anthropic, “Natural Language Autoencoders,” 2026. [Online]. Available: https://www.anthropic.com/research/natural-language-autoencoders

[7] kitft, “natural_language_autoencoders,” GitHub. [Online]. Available: https://github.com/kitft/natural_language_autoencoders
