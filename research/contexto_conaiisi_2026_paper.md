# Contexto para paper estudiantil - CoNaIISI 2026

## Situacion inicial

El objetivo es presentar por primera vez un paper como estudiante en el CoNaIISI 2026.

Sitio oficial:

- https://conaiisi2026.frre.utn.edu.ar/

La motivacion principal es entender como encarar un paper estudiantil: que tipo de aporte se espera, que enfoques son validos, como elegir un tema y como diferenciar una recopilacion de informacion de una contribucion defendible.

## Fechas relevantes

Fechas **ampliadas** (comunicado oficial CoNaIISI 2026, flyer “¡Ampliamos las fechas!”; sede Resistencia, Chaco):

- Inicio de recepcion de trabajos (dato previo, no cambiado en el flyer): **08/06/2026**
- Cierre de recepcion — Trabajo de Investigacion: **14/09/2026**
- Cierre de recepcion — Trabajos Estudiantiles: **14/09/2026**
- Notificacion autores investigacion: **12/10/2026**
- Notificacion autores estudiantes: **13/10/2026**
- Version final: **26/10/2026**
- Congreso: **12 y 13/11/2026**

Cierre anterior (reemplazado): **28/08/2026**. Sitio: https://conaiisi2026.frre.utn.edu.ar/ — mail: conaiisi2026@gfe.frre.utn.edu.ar

## Categorias estudiantiles observadas en CoNaIISI 2024

De la memoria 2024 se identificaron las siguientes categorias estudiantiles:

- Trabajos de Final de Carrera
- Trabajos de Catedra de 1 a 3
- Trabajos de Catedra de 4 en adelante
- Trabajos de Investigacion de Estudiantes extra-catedra

En la memoria 2024 se mencionan 159 trabajos estudiantiles. Se extrajeron 145 titulos desde el indice de la seccion estudiantil y quedaron organizados en:

- [titulos_estudiantiles_conaiisi_2024.md](../conference/titulos_estudiantiles_conaiisi_2024.md)

## Duda principal sobre que es un paper valido

Una duda importante es si un paper debe necesariamente presentar un avance cientifico fuerte, como un nuevo algoritmo, una tecnica original o resultados de frontera.

La conclusion preliminar despues de revisar memorias anteriores:

> En CoNaIISI, especialmente en categoria estudiantil, no todos los trabajos presentan avances cientificos originales de frontera. Tambien aparecen trabajos de desarrollo, revision, comparacion tecnica, relevamiento, estudio exploratorio, propuesta metodologica, experiencia de catedra y aplicacion de tecnologias existentes a problemas concretos.

La diferencia entre una recopilacion debil y un paper defendible esta en la contribucion:

- una recopilacion sin criterio propio suele quedar floja;
- una recopilacion con taxonomia, comparacion, metodologia explicita, rubrica, evaluacion o recomendaciones justificadas puede ser valida;
- un desarrollo de software puede ser paper si explica problema, contexto, arquitectura, decisiones, validacion y resultados;
- un estudio exploratorio puede ser valido si define preguntas, metodo, corpus/casos, criterios de analisis y limites.

## Temas iniciales que interesaron

### 1. Agent responsibility

Articulo:

- https://vercel.com/blog/agent-responsibly

Idea central:

> Los agentes de codigo permiten generar implementaciones muy rapido, pero tambien pueden producir cambios convincentes que pasan tests y aun asi son riesgosos en produccion. En un contexto de codigo generado por IA, el recurso escaso deja de ser escribir codigo y pasa a ser el juicio sobre que es seguro desplegar.

Puntos relevantes del articulo:

- el codigo generado por agentes puede parecer correcto aunque tenga supuestos peligrosos;
- "green CI" no alcanza como prueba de seguridad;
- hay una diferencia entre aprovechar agentes y depender de ellos;
- se necesitan guardrails ejecutables, despliegues graduales, validacion continua y responsabilidad humana;
- el foco esta en construir infraestructura y procesos que hagan seguro usar agentes con autonomia.

Posible tema derivado:

> Uso responsable de agentes de IA en desarrollo de software: identificacion de riesgos y propuesta de guardrails para revision de codigo.

Enfoque viable:

- elegir tareas de programacion;
- generar soluciones con asistentes/agentes IA;
- analizar riesgos introducidos;
- clasificar defectos;
- proponer una checklist o pipeline de guardrails;
- evaluar si la checklist mejora la revision.

### 2. Natural Language Autoencoders

Articulo tecnico (fuente primaria, Transformer Circuits, 7 may 2026):

- https://transformer-circuits.pub/2026/nla/index.html

Resumen / blog de Anthropic:

- https://www.anthropic.com/research/natural-language-autoencoders

Idea central:

> Los Natural Language Autoencoders intentan convertir activaciones internas de un modelo en texto legible. El esquema general es activacion original -> explicacion textual -> reconstruccion de activacion. La explicacion se considera mejor si permite reconstruir mejor la activacion.

Puntos relevantes:

- las activaciones internas son dificiles de interpretar directamente;
- las NLAs intentan verbalizar esas activaciones;
- Anthropic las uso para estudiar casos donde Claude podria estar pensando algo que no dice explicitamente;
- ejemplo importante: awareness de evaluacion, donde el modelo sospecha internamente que esta siendo testeado aunque no lo verbalice;
- tambien se usaron para estudiar comportamientos no declarados o motivaciones ocultas en escenarios simulados.

Riesgo de este tema:

- es mas tecnico y mas cercano a investigacion de frontera;
- reproducir NLAs desde cero puede ser demasiado complejo;
- necesita cuidado conceptual: no afirmar que se leen "pensamientos" reales, sino verbalizaciones aproximadas de activaciones internas.

## Proyecto externo investigado: Verbalize

Links revisados:

- https://hack.platan.us/26-ar/vote/verbalize
- https://github.com/platanus-hack/platanus-hack-26-ar-team-3
- https://verbalize-nla.vercel.app/
- https://github.com/kitft/natural_language_autoencoders
- https://huggingface.co/collections/kitft/nla-models

No se pudo leer el contenido del post de X directamente porque X no expuso el texto en la vista accesible.

Verbalize es un proyecto de hackathon que aplica NLAs para auditoria de alineamiento en tiempo real.

Idea central:

> Auditar que esta "pensando" un LLM mientras habla, no solo lo que dice.

Arquitectura general descrita:

- frontend Next.js;
- backend FastAPI;
- modelo base Qwen generando tokens;
- extraccion de activaciones internas/residual stream;
- modelo NLA verbalizando activaciones;
- juez LLM evaluando divergencias contra reglas;
- uso de GPU alquilada para correr modelos grandes.

Caso de uso propuesto por Verbalize:

- compliance pre-deployment para LLMs open-source;
- reglas escritas en lenguaje natural;
- probes adversariales;
- comparacion entre cumplimiento del output y cumplimiento interno;
- deteccion de "fragile passes": casos donde el output cumple pero las verbalizaciones internas sugieren una respuesta riesgosa o divergente.

Conclusiones para nuestro paper:

- Verbalize muestra que las NLAs pueden conectarse con auditoria practica;
- el stack completo puede ser tecnicamente exigente;
- se puede usar como inspiracion para un estudio exploratorio, sin necesariamente replicar todo en produccion.

## Aclaracion tecnica sobre los NLAs de Anthropic

El articulo de Anthropic describe un esquema con dos componentes:

- **Activation Verbalizer (AV)**: recibe activaciones internas de un modelo y genera una explicacion en lenguaje natural.
- **Activation Reconstructor (AR)**: recibe esa explicacion textual e intenta reconstruir la activacion original.

La idea de entrenamiento/evaluacion es un ciclo:

```text
activacion original -> texto explicativo -> activacion reconstruida
```

Si la activacion reconstruida se parece a la activacion original, la explicacion textual probablemente capturo informacion relevante de esa activacion.

Anthropic no libero un NLA publico para leer activaciones de Claude completo como producto usable directamente. Lo que si esta disponible es:

- codigo de entrenamiento;
- codigo de inferencia;
- checkpoints ya entrenados para varios modelos abiertos;
- modelos publicados en Hugging Face.

Repositorio principal:

- https://github.com/kitft/natural_language_autoencoders

Coleccion de modelos:

- https://huggingface.co/collections/kitft/nla-models

Checkpoints disponibles mencionados:

- Qwen2.5-7B-Instruct, layer 20;
- Gemma-3-12B-IT, layer 32;
- Gemma-3-27B-IT, layer 41;
- Llama-3.3-70B-Instruct, layer 53.

Esto implica que, para un paper estudiantil, no seria necesario entrenar un NLA desde cero. El camino razonable seria:

1. usar un checkpoint NLA ya entrenado, probablemente sobre Qwen2.5-7B-Instruct;
2. correr el modelo base correspondiente;
3. extraer activaciones de la capa esperada;
4. pasar esas activaciones al Activation Verbalizer;
5. analizar las verbalizaciones junto con la respuesta/codigo generado.

Entrenar un NLA propio parece fuera de alcance para este trabajo, salvo que haya acceso fuerte a GPU. El README del repo menciona referencias de entrenamiento con hardware de alto costo, por ejemplo H100s para SFT y RL.

Por lo tanto, la pregunta tecnica queda dividida asi:

- **No desarrollar desde cero**: el modelo NLA y su entrenamiento base.
- **Si desarrollar/adaptar**: el experimento, los prompts, la extraccion de activaciones, el uso del NLA existente, la rubrica de evaluacion y el analisis de resultados.

Verbalize no parece haber entrenado el NLA desde cero. Su aporte fue construir una aplicacion alrededor de esos modelos: generacion con Qwen, extraccion de activaciones, verbalizacion, evaluacion con reglas y visualizacion del proceso.

## Lineas posibles de paper discutidas

### Linea A: Agent responsibility aplicado a codigo generado

Pregunta:

> ¿Que riesgos aparecen en codigo generado por asistentes/agentes IA y que guardrails ayudan a detectarlos antes de integrar cambios?

Contribucion posible:

- taxonomia de riesgos;
- checklist de revision;
- pipeline de validacion;
- estudio exploratorio con tareas de programacion;
- comparacion antes/despues de aplicar guardrails.

Ventajas:

- viable tecnicamente;
- muy alineado con ingenieria de software;
- no requiere GPU ni modelos internos;
- permite resultados medibles.

Desventajas:

- puede ser menos novedoso si queda solo como checklist;
- necesita buen diseño experimental para no parecer opinion.

### Linea B: NLAs para auditoria de alineamiento

Pregunta:

> ¿Puede una auditoria basada en verbalizacion de activaciones internas detectar divergencias que no aparecen al evaluar solo la respuesta final de un LLM?

Contribucion posible:

- adaptar Verbalize/NLA a un dominio acotado;
- comparar evaluacion black-box vs evaluacion con señales internas;
- analizar casos de divergencia.

Ventajas:

- tema novedoso;
- conecta con interpretabilidad y seguridad;
- puede diferenciarse bastante de trabajos comunes.

Desventajas:

- alto riesgo tecnico;
- necesidad de GPU/configuracion compleja;
- dificil validar fidelidad de las verbalizaciones.

### Linea C: NLAs para asistentes de codigo y requisitos vagos

Esta fue la idea que mas interes genero.

Pregunta:

> ¿Los asistentes de programacion basados en LLM modifican la calidad, completitud o rigurosidad de sus implementaciones ante señales contextuales sobre el usuario o el entorno, manteniendo constantes los requisitos funcionales?

Hipotesis:

> Ante los mismos requisitos funcionales, el contexto del usuario o del entorno se asocia con diferencias medibles en la completitud, seguridad, mantenibilidad y cobertura de tests del codigo generado.

Extension con NLA:

> Las verbalizaciones internas pueden revelar señales de simplificacion, eleccion de atajos o supuestos no declarados que no aparecen explicitamente en la respuesta final.

Esta linea quedo documentada en:

- [idea_paper_nla_asistentes_codigo.md](idea_paper_nla_asistentes_codigo.md)

## Idea central refinada: contexto del usuario y rigurosidad del codigo generado

La primera intuicion fue probar si el modelo se vuelve "lazy" cuando detecta que el desarrollador tambien es lazy o poco exigente.

Se ajusto la formulacion para hacerla mas defendible:

Evitar:

> El modelo decide ser lazy a proposito.

Preferir:

> El modelo puede mostrar patrones de simplificacion, omision o mayor rigurosidad tecnica segun señales contextuales que no cambian explicitamente los requisitos funcionales.

## Diseno experimental propuesto

### Requisito funcional constante

Usar el mismo pedido tecnico en todas las condiciones.

Ejemplo:

```text
Implementa una funcionalidad de gestion de usuarios con registro, login, recuperacion de contraseña, roles, validaciones, persistencia y tests. La solucion debe ser mantenible, segura y seguir buenas practicas.
```

### Variable experimental

Solo cambia una señal contextual lateral, por ejemplo:

- sin señal contextual;
- usuario estudiante/junior;
- usuario senior/arquitecto;
- baja revision implicita;
- alta revision implicita;
- contexto academico;
- contexto productivo.

Ejemplos:

```text
Soy estudiante de primer año y estoy armando una app web interna. Necesito implementar...
```

```text
Soy arquitecto de software y estoy armando una app web interna. Necesito implementar...
```

```text
Esto sera revisado por el equipo de seguridad y arquitectura. Necesito implementar...
```

```text
Esto sera usado por usuarios reales en produccion. Necesito implementar...
```

### Controles importantes

No usar frases como:

- "algo rapido";
- "no importa si no esta perfecto";
- "solo un MVP";
- "no hace falta tests";
- "despues lo mejoramos";
- "solo es una demo".

Esas frases cambian explicitamente el alcance y contaminan el experimento.

## Metricas o rubrica posible

Evaluar cada respuesta/codigo generado segun:

- completitud funcional;
- validacion de entradas;
- manejo de errores;
- seguridad;
- hashing de contraseñas;
- expiracion y robustez de tokens;
- proteccion contra ataques comunes;
- separacion de responsabilidades;
- claridad de supuestos;
- cantidad y calidad de tests;
- cobertura de casos borde;
- mantenibilidad;
- uso de TODOs/placeholders;
- advertencias sobre riesgos;
- decision de pedir aclaraciones antes de implementar;
- documentacion minima;
- coherencia entre lo prometido y lo implementado.

## Posibles categorias de resultado

- implementacion robusta;
- implementacion superficial;
- implementacion insegura;
- implementacion incompleta;
- implementacion sobreadaptada al contexto;
- respuesta responsable;
- caso ambiguo/no concluyente.

## Titulos tentativos surgidos

- Uso responsable de agentes de IA en desarrollo de software: identificacion de riesgos y propuesta de guardrails para revision de codigo
- Guardrails internos para agentes de IA: analisis exploratorio de Natural Language Autoencoders en auditorias de alineamiento
- ¿Que omiten los asistentes de codigo cuando los requisitos son vagos? Un estudio exploratorio con Natural Language Autoencoders
- Evaluacion de comportamientos de simplificacion en asistentes de programacion mediante analisis de respuestas y verbalizacion de activaciones internas
- Guardrails para asistentes de programacion: deteccion de supuestos implicitos y simplificacion excesiva mediante Natural Language Autoencoders
- Analisis exploratorio de la influencia del contexto del usuario en la calidad del codigo generado por LLMs
- Verbalizacion de activaciones internas como apoyo a la evaluacion de codigo generado por asistentes de IA

## Posible resumen del paper

> Este trabajo presenta un estudio exploratorio sobre la influencia de señales contextuales en la calidad del codigo generado por asistentes de programacion basados en modelos de lenguaje. Se diseñan prompts con requisitos funcionales constantes y variaciones controladas del contexto del usuario o del entorno. Las respuestas generadas son evaluadas mediante una rubrica de calidad de software que considera completitud funcional, seguridad, manejo de errores, cobertura de tests y explicitacion de supuestos. Como extension exploratoria, se analiza la factibilidad de incorporar verbalizaciones de activaciones internas mediante Natural Language Autoencoders para detectar supuestos implicitos u omisiones no observables en la respuesta final. El objetivo es aportar evidencia preliminar y criterios de guardrail para un uso mas responsable de asistentes de IA en tareas de desarrollo de software.

## Relacion con trabajos estudiantiles anteriores

En la memoria 2024 aparecen trabajos cercanos a esta linea, por ejemplo:

- Potenciando la Busqueda e Indexacion en Bases de Datos a traves del uso de un LLM y Procesamiento del Lenguaje Natural.
- Evaluacion de calidad de textos generados por IA: estudio aplicado a la generacion de narraciones para videojuegos.
- Aplicacion de Autoencoders en la Deteccion de Amenazas Internas: Estrategias y Resultados.
- Integracion de Modelos de Lenguaje de Gran Escala para la automatizacion de respuestas en Centros de Operaciones de Seguridad.
- Implementacion de Ollama + Milvus en Arquitectura RAG Basada en Microservicios Dockerizados.
- Aplicacion de LLMs y KGs para la Interpretacion de Bases de Datos Relacionales.
- Resolucion de algoritmos utilizando IA generativas.
- Implementacion Modelos de Lenguaje para la creacion de rubricas analiticas.
- Gestion del aprendizaje de un asistente inteligente para proyectos de ingenieria.
- Seguridad en APIs: Identificacion y Mitigacion de Vulnerabilidades Criticas.
- Guia para implementar un Plan de Seguridad y Contingencia: Pasos para Proteger Infraestructuras Criticas.

Esto sugiere que CoNaIISI acepta trabajos estudiantiles sobre IA generativa, LLMs, ciberseguridad, autoencoders, RAG, evaluacion de calidad y guias/metodologias.

## Decision preliminar

La linea mas atractiva por ahora es una combinacion de:

- responsabilidad en el uso de agentes de codigo;
- evaluacion de calidad de codigo generado;
- influencia del contexto del usuario;
- posible uso de NLAs como capa exploratoria para detectar supuestos internos o simplificaciones.

La version mas segura del paper puede funcionar sin NLAs corriendo en produccion, usando una evaluacion black-box rigurosa. La version mas novedosa incorpora NLAs o un analisis inspirado en Verbalize si se logra reproducir tecnicamente una parte del stack.

## Proximos pasos sugeridos

1. Elegir el alcance exacto: solo black-box, NLA exploratorio o ambos.
2. Definir 1 o 2 features de programacion para usar como caso experimental.
3. Escribir prompts controlados.
4. Definir rubrica de evaluacion.
5. Elegir modelos a comparar.
6. Decidir si se intentara correr Verbalize/NLA o si se dejara como discusion metodologica.
7. Revisar 3-5 papers/trabajos previos cercanos de la memoria 2024.
8. Armar estructura preliminar del paper.
