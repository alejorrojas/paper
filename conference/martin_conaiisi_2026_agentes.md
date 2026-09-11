# Extract: Artículo CONAIISI 20260805.pdf

Pages: 8

## Page 1

ARIA: Un Enfoque Inteligente para la Gestión y Mejora de 
Requerimientos en Entornos Ágiles  
 
Paula Kozak Riehme, Denise Martínez, Joaquín Bianciotto, Valentino Honnorat, Martín Lopez 
Soto, Jerónimo Zapata, Noelia Pinto, Gabriela Tomaselli 
Centro de Investigación Aplicada en Tecnologías de la Información y Comunicación 
(CInApTIC) 
Facultad Regional Resistencia – Universidad Tecnológica Nacional 
French 414, Resistencia, Chaco, Argentina 
{paulakozakr,deniseutn,bianciottojoaquin03,valentinohonnorat2,jerozapata13,martinlopezsoto08,ns.p
into, gabriela.tomaselli}@gmail.com 
 
Resumen 
Este trabajo presenta ARIA (Agile Requirements 
Intelligent Assistant), una plataforma inteligente orientada 
a la gestión y mejora de requerimientos en entornos ágiles. 
A partir de un modelo de calidad estructurado en tres 
componentes conceptuales: Clasific ador, Validador y 
Priorizador, ARIA operacionaliza dichos componentes 
mediante una arquitectura multiagente coordinada por un 
kernel orquestador, apoyada en modelos de lenguaje de 
gran escala y una memoria semántica compartida que 
garantiza consistencia histórica y aprendizaje 
incremental. La plataforma incorpora además un Agente 
Enriquecedor orientado a transformar los resultados del 
análisis en sugerencias concretas y revisables de mejora 
sobre los requerimientos. A diferencia de las herramientas 
tradicionales de gestión de proyectos, ARIA introduce una 
lógica de curación activa del backlog que permite detectar 
problemas semánticos, identificar discrepancias entre la 
prioridad asignada por el equipo y la estimada por la 
plataforma, y proponer mejoras contextualizadas antes de 
que los requerimientos avancen hacia etapas de 
desarrollo. La propuesta no busca reemplazar el juicio del 
equipo, sino asistirlo con evidencia cuantificable, 
trazabilidad y recomendaciones accionables para mejorar 
la calidad del backlog desde las etapas tempranas del 
desarrollo. La validación empírica de la plataforma en 
contextos reales y la incorporación de mecanismos de 
feedback y aprendizaje continuo constituyen los pasos 
siguientes para consolidar su impacto en la calidad de los 
procesos y productos de software ágiles.  
1. Introducción 
El Desarrollo Ágil de Software (ASD, por sus siglas 
en inglés Agile Software Development ) ha sido 
ampliamente adoptado en la industria debido a su 
flexibilidad, su carácter iterativo y su énfasis en la entrega 
temprana de valor. Sin embargo, a pesar de su 
popularidad, la gestión de requerimientos en estos 
entornos continúa presentando desafíos significativos, 
particularmente en áreas críticas como la completitud, 
trazabilidad y priorización de los requerimientos [1, 2]. 
En numerosos casos, las organizaciones implementan 
prácticas ágiles de manera intuitiva o parcial, sin realizar 
una evaluació n sistemática de su impacto en la calidad 
tanto del proceso como del producto [3, 12]. 
En paralelo, el avance de los modelos de lenguaje de 
gran escala (LLM, por sus siglas en inglés Large 
Language Models ) ha abierto nuevas posibilidades para 
automatizar tareas complejas en ingeniería de software. 
Investigaciones recientes han demostrado que los LLM 
pueden actuar como colaboradores activos en actividades 
de ingeniería de requerimientos, incluyendo la 
elicitación, clasificación, verificación y especificación, 
superando en velocidad y consistencia a enfoques 
tradicionales [4, 5]. En este contexto, los Sistemas 
Multiagente basados en LLM emergen como una 
arquitectura especialmente adecuada para abordar 
procesos complejos de análisis, al permitir delegar 
responsabilidades específicas en agentes especializados 
coordinados por un orquestador central [6, 7]. Trabajos 
como MARE han demostrado que la colaboración entre 
múltiples agentes LLM a lo largo del proceso de 
ingeniería de requerimientos puede mejorar 
significativamente la calidad de los modelos generados 
respecto de enfoques basados en un único modelo [8]. 
Esta línea de investigación se inserta en ese contexto, 
consolidándose a lo largo de sucesivas etapas que 
articulan revisión bibliográfica, relevamiento empírico y 
formulación conceptual, y que se han plasmado en 
distintos trabajos previos que fueron ampli ando 
progresivamente el alcance de la propuesta. A partir de 
una Revisión Sistemática de la Literatura (RSL), una 
encuesta a profesionales de la industria y el diseño de un 
modelo de calidad para requerimientos ágiles [9, 10, 18], 
se desarrolló ARIA ( Agile Requirements Intelligent 
Assistant), una plataforma que operacionaliza dicho 
modelo mediante una arquitectura multiagente 
coordinada por un kernel orquestador. El sistema 

## Page 2

operacionaliza un modelo conceptual estructurado 
estrictamente en tres componentes: Clasificador, 
Validador y Priorizador. Para su implementación, la 
plataforma incorpora agentes especializados para cada 
uno de ellos y suma un cuarto agente denominado 
Enriquecedor, operando todos bajo una arquitectura 
coordinada por un kernel orquestador, apoyada en 
modelos de lenguaje de gran escala y una memoria 
semántica compar tida que garantiza consistencia 
histórica y aprendizaje incremental. ARIA no busca 
reemplazar el juicio del equipo, sino asistirlo con 
evidencia cuantificable, trazabilidad y recomendaciones 
accionables para mejorar la calidad del backlog desde las 
etapas tempranas del desarrollo. 
El resto del trabajo se estructura de la siguiente 
manera: la Sección 2 presenta las motivaciones que 
justifican el desarrollo de la plataforma; la Sección 3 
resume el modelo de calidad que sirve de base para la 
implementación; la Sección 4 describe la arq uitectura de 
ARIA y sus componentes principales; la Sección 5 detalla 
las funcionalidades implementadas;  la Sección 6 discute 
las limitaciones de la propuesta; la Sección 7 presenta el 
diseño de validación previsto; y la Sección 8 presenta las 
conclusiones y líneas de trabajo futuro. 
2. Motivaciones 
Estudios previos en el marco de esta línea de 
investigación evidenciaron de manera consistente la 
presencia de deficiencias estructurales en la gestión de 
requerimientos en entornos ágiles, particularmente en lo 
relativo a incompletitud, ambigüedad, baja trazabilidad y 
dificultades para priorizar [9, 10, 18]. Estos hallazgos, 
obtenidos mediante una RSL y una encuesta a 40 
profesionales de la industria, señalaron además la 
ausencia de herramientas automatizadas de apoyo como 
uno de los impedimentos más frecu entes en los equipos 
relevados. 
Sin embargo, el problema no se limita a la falta de 
automatización. Las herramientas ampliamente 
adoptadas en la industria permiten registrar y hacer 
seguimiento de requerimientos, pero carecen de 
mecanismos para evaluar su calidad semántica, detectar 
ambigüedades o inconsistencias, y asistir activamente en 
su mejora [1, 2]. Esta limitación obliga a los equipos a 
depender del criterio individual de analistas y Product 
Owners, sin soporte sistemático ni trazabilidad de las 
decisiones tomadas [3]. En consecue ncia, los problemas 
de calidad identificados en etapas tempranas no se 
resuelven con más documentación, sino con mecanismos 
que ayuden a articular criterios compartidos, evidencia 
cuantificable y toma de decisiones contextualizada. 
En este sentido, trabajos recientes han mostrado que 
los LLM pueden evaluar atributos específicos de calidad 
como completitud, singularidad y verificabilidad con alta 
precisión, y que sus sugerencias de mejora sobre 
requerimientos concretos son valoradas positivamente 
por analistas y equipos de desarrollo [4 , 11]. Este 
potencial, combinado con la capacidad de los sistemas 
multiagente para modularizar responsabilidades y 
coordinar análisis complejos, abre una oportunidad 
concreta para el diseño de herramientas inteligentes de 
soporte a la gestión de requerimientos que vayan más allá 
del registro y el seguimiento [8]. 
A partir de este diagnóstico, la motivación central de 
este trabajo es presentar ARIA, una plataforma que 
operacionaliza el modelo de calidad propuesto en trabajos 
anteriores [10] mediante agentes especializados 
coordinados por un kernel orquestador, incor porando 
además un Agente Enriquecedor orientado a transformar 
los resultados del análisis en sugerencias concretas y 
revisables de mejora sobre los requerimientos. 
3. Modelo conceptual de ARIA 
El modelo de calidad que sirve de base para ARIA fue 
formulado en investigaciones anteriores como respuesta 
a los problemas recurrentes identificados en la RSL y el 
relevamiento empírico [10]. Su propósito es evaluar y 
mejorar la calidad de los requerimien tos ágiles de forma 
sistemática, considerando cada requerimiento no de 
manera aislada sino dentro del contexto del backlog 
completo, donde la coherencia global y las relaciones 
entre ítems son determinantes para la calidad del 
producto. El modelo se organi za en tres componentes 
secuenciales e interrelacionados: Clasificador, Validador 
y Priorizador, cuyas salidas funcionan como insumos 
encadenados a lo largo del flujo de análisis. 
3.1. Componente Clasificador 
El Clasificador constituye la primera instancia de 
análisis del modelo. Su propósito es caracterizar los 
requerimientos del set analizado a partir de dimensiones 
que permitan reconocer sus condiciones iniciales dentro 
del flujo propuesto. Esta caracterización no busca evaluar 
la calidad del requerimiento en términos normativos, sino 
registrar aspectos operativos que pueden incidir en su 
tratamiento posterior: complejidad, dependencias, 
factibilidad, estado e información disponible. 
La complejidad refiere al grado de dificultad asociado 
al tratamiento del requerimiento dentro del proyecto, 
permitiendo anticipar riesgos y organizar su 
incorporación al flujo de trabajo. Las dependencias 
expresan las relaciones que un requerimiento manti ene 
con otros elementos del backlog, componentes o 
condiciones externas, lo que resulta clave para sostener la 

## Page 3

trazabilidad y evitar bloqueos. La factibilidad aporta una 
valoración preliminar de viabilidad en función de 
recursos, capacidades técnicas y restricciones 
organizacionales disponibles. El estado registra la 
situación del requerimiento dentro del flujo de trabajo, 
mientras que la información disponible indica el nivel de 
datos y antecedentes con que se cuenta para su análisis. 
La salida del Clasificador es una matriz de 
caracterización estructurada que organiza esta 
información para cada requerimiento del set, 
constituyendo la base contextual sobre la que operan los 
componentes siguientes. 
3.2. Componente Validador 
El Validador se centra en la evaluación sistemática de 
la calidad de los requerimientos mediante un modelo de 
evaluación organizado en tres características: Adecuación 
funcional, Especificación y Mantenibilidad. Cada 
característica agrupa atributos observa bles a nivel de 
requerimiento individual, cuya valoración se expresa de 
manera agregada sobre el total del set analizado [13, 14, 
15]. 
La Adecuación funcional evalúa la correspondencia 
entre los requerimientos y las necesidades reales del 
usuario, del negocio y del dominio del sistema, 
considerando atributos de conformidad, correctitud y 
prescindibilidad. La Especificación evalúa la calidad con 
que los requerimientos están formulados como unidades 
comunicacionales y técnicas, a través de atributos de 
completitud, consistencia y multiplicidad. La 
Mantenibilidad evalúa la capacidad de los requerimientos 
para ser comprendidos, verificados, modificados y 
sostenidos durante la evolución del producto, mediante 
atributos de trazabilidad, verificabilidad y ambigüedad. 
Cada característica combina dos atributos positivos, 
valorados en una escala de 0 a 4, y uno negativo, valorado 
de 0 a -4. Los valores se normalizan en una escala de 0% 
a 100% para permitir comparaciones entre características, 
y se agrega un valor global d e calidad del set como 
promedio simple de las tres características normalizadas. 
La salida del Validador combina esta dimensión sintética 
con una dimensión diagnóstica que identifica los atributos 
con menor desempeño y mayor incidencia negativa, 
constituyendo el insumo principal para el Agente 
Enriquecedor en la arquitectura de ARIA. 
3.3. Componente Priorizador 
El Priorizador aborda la dimensión decisional del 
modelo. Su función no consiste en evaluar si un 
requerimiento está bien especificado, sino en analizar si 
la prioridad asignada cuenta con criterios explícitos de 
fundamentación vinculados con valor de nego cio, 
impacto estratégico, urgencia, dependencias, esfuerzo 
estimado y restricciones del proyecto . Esta distinción es 
relevante: un requerimiento puede estar correctamente 
formulado y no ser prioritario, o ser urgente y estratégico 
aun presentando deficiencias de especificación que 
requieran atención previa. 
A nivel conceptual, la salida del Priorizador expresa 
el grado en que el ordenamiento del set se encuentra 
fundamentado en criterios explícitos y trazables, valorado 
en una escala de 0 a 4. Sin embargo , en su 
operacionalización dentro de la arquitectura de ARIA, 
este componente se traduce en un Índice de Alineación de 
Prioridad (IAP) que asume valores continuos entre 0 y 1 
(donde 1 indica una alineación perfecta y 0 representa la 
discrepancia máxima). E ste índice contrasta la prioridad 
asignada por el equipo con la estimada por la plataforma 
a partir del análisis del set, identificando discrepancias 
que funcionan como alertas para la revisión colaborativa 
del backlog sin reemplazar la decisión del Product Owner 
ni del equipo de desarrollo.  
4. ARIA: arquitectura y componentes 
ARIA implementa el modelo conceptual descrito en 
la sección anterior mediante una arquitectura multiagente 
coordinada por un kernel orquestador. Tal como se 
observa en la Figura 1, el diseño se organiza en capas que 
reflejan la separación de responsabilidades y favorecen la 
modularidad y escalabilidad del sistema. En ella, los 
procesos de caracterización, evaluación, priorización y 
enriquecimiento de requerimientos se distribuyen en tre 
agentes especializados que operan de forma coordinada, 
apoyados en modelos de lenguaje de gran escala y una 
memoria semántica compartida [6, 7]. 
   
Figura 1. Arquitectura general de ARIA. 


## Page 4

El principio rector de esta arquitectura es la 
colaboración entre agentes autónomos y componentes 
cognitivos, orientada a transformar un requerimiento 
inicial en un requerimiento enriquecido, acompañado de 
métricas e indicadores de calidad. De este modo, l a 
arquitectura combina la eficiencia del procesamiento 
distribuido con las capacidades interpretativas y 
generativas de la inteligencia artificial, dando lugar a un 
sistema dinámico centrado en la mejora continua de la 
calidad del backlog. 
4.1. Interfaz de entrada y salida 
La interfaz de entrada y salida constituye el punto de 
interacción entre los usuarios y ARIA. A través de ella, 
los requerimientos ingresan al sistema mediante carga 
manual, con integración planificada a futuro con 
herramientas de gestión ágil de uso exten dido en la 
industria, como Jira o Azure DevOps, lo que permitirá 
incorporar el enfoque propuesto a flujos de trabajo ya 
existentes sin requerir un cambio de herramienta . En 
sentido inverso, la interfaz devuelve los resultados 
generados por el flujo de análisis, incluyendo métricas de 
calidad, observaciones sobre las condiciones de cada 
requerimiento y sugerencias revisables de mejora 
producidas por el Agente Enriquecedor , presentados de 
manera que puedan ser interpretados y discutidos por el 
equipo de desarrollo, el Product Owner y los 
stakeholders, de modo que la plataforma apoye el análisis 
sin desplazar el juicio ni la decisión del equipo. 
4.2. Kernel orquestador 
El kernel orquestador constituye el núcleo operativo 
de ARIA. Su función es coordinar el ciclo de análisis  de 
cada requerimiento desde su ingreso hasta su 
consolidación final en el backlog, dirigiendo el flujo de 
análisis y consolidando los resultados parciales en una 
salida integrada y coherente. El kernel no ejecuta tareas 
de evaluación por sí mismo, sino que actúa como un 
motor de enrutamiento inteligente que gestiona la 
secuencia de activación de los agentes según el estado y 
las características del requerimiento procesado. 
Adicionalmente, el kernel cumple un rol de gestor de 
contexto y trazabilidad, conservando los resultados 
intermedios de cada análisis e integrándolos en una línea 
de tiempo trazable. Esto permite a los equipos visualizar 
no solo la evaluación final de cada requerimiento, sino 
también cómo cada criterio del modelo fue aplicado y qué 
modificaciones se propusieron en cada ciclo. El flujo no 
es rígido: el kernel habilita tanto rutas secuenciales como 
paralelas según las condiciones del requerimiento, lo que 
garantiza eficiencia y flexibilidad operativa [10]. 
Un aspecto central de esta orquestación es la 
interacción dinámica entre los agentes. El kernel utiliza 
los resultados del Validador como una condición 
necesaria para el análisis del Priorizador. Si el set de 
requerimientos presenta una calidad aceptable, el flujo de 
priorización se ejecuta normalmente. Sin embargo, si se 
detectan deficiencias severas, como alta ambigüedad, 
incompletitud o falta de verificabilidad, el sistema puede 
recomendar que los requerimientos pasen primero por el 
Agente Enriquecedor antes de someterse a revisión de 
prioridad. Esta lógica dinámica evita priorizar a ciegas 
requerimientos mal definidos y conserva el principio ágil 
de decisión situada.  
4.3. Agentes especializados 
ARIA incorpora cuatro agentes especializados para 
ejecutar el flujo de análisis y mejora. Los tres primeros 
operacionalizan directamente los componentes 
conceptuales descritos en la sección 3, mientras que el 
cuarto constituye una capacidad adicional de la  
plataforma orientada al refinamiento activo del backlog. 
El Agente Clasificador recibe el requerimiento en su 
estado inicial y produce una caracterización estructurada 
en función de las dimensiones definidas por el 
componente Clasificador: complejidad, dependencias, 
factibilidad, estado e información disponible.  Esta 
caracterización no evalúa calidad en sentido normativo, 
sino que registra condiciones operativas que orientan el 
análisis de los agentes siguientes y permite al kernel 
tomar decisiones de enrutamiento más precisas. 
El Agente Validador implementa el modelo de 
evaluación de calidad definido por el componente 
Validador, evaluando las tres características del modelo: 
Adecuación funcional, Especificación y Mantenibilidad. 
Su salida combina un valor global de calidad del s et 
analizado con una dimensión diagnóstica que identifica 
los atributos con menor desempeño, señalando 
concretamente qué aspectos de cada requerimiento 
requieren intervención antes de avanzar en el flujo. 
El Agente Priorizador toma como insumo la prioridad 
inicialmente asignada por el equipo y la contrasta con una 
prioridad estimada por ARIA a partir del análisis del set 
y los criterios disponibles: valor de negocio, impacto 
estratégico, urgencia, dependenc ias y esfuerzo estimado. 
Esta comparación se expresa mediante el Índice de 
Alineación de Prioridad (IAP), que permite identificar 
discrepancias entre ambas prioridades como alertas para 
la revisión colaborativa del backlog, sin sustituir la 
decisión del Product Owner ni del equipo de desarrollo. 
El Agente Enriquecedor opera como instancia final 
del flujo, tomando como insumos los resultados 
producidos por los tres agentes anteriores para proponer 
mejoras concretas y revisables sobre los requerimientos 
analizados. Su función abarca tres tipos de 
enriquecimiento: textual, orientado a reducir ambigüedad 

## Page 5

y mejorar precisión en la redacción; estructural, orientado 
a completar información faltante y criterios de 
aceptación; y contextual, orientado a detectar 
redundancias, solapamientos e inconsistencias con otros 
elementos del backlog. Las propuestas generadas por este 
agente no constituyen versiones finales de los 
requerimientos sino sugerencias sujetas a revisión por 
parte del equipo, preservando el carácter de asistencia 
cognitiva de la plataforma. 
4.4. LLMs y memoria semántica 
Los modelos de lenguaje de gran escala constituyen el 
núcleo cognitivo del sistema, proporcionando a los 
agentes la capacidad de interpretar lenguaje natural, 
razonar sobre dependencias semánticas y generar 
propuestas de mejora textual. Cada agente se comu nica 
con los LLMs mediante prompts estructurados que 
encapsulan las reglas de análisis y los criterios de 
evaluación definidos por el modelo de calidad, 
asegurando que las capacidades generativas de los 
modelos operen dentro del marco conceptual establecid o 
[4, 16, 17]. 
La memoria semántica funciona como repositorio 
contextual compartido entre los agentes, almacenando 
requerimientos históricos, plantillas estandarizadas, 
patrones de calidad y decisiones previas. En su versión 
actual, ARIA opera principalmente sobre sets o  paquetes 
de requerimientos seleccionados por el equipo, lo que 
permite mantener coherencia y trazabilidad dentro del 
conjunto analizado. Este componente garantiza 
consistencia histórica en los resultados y habilita un 
aprendizaje incremental a lo largo de l tiempo, sentando 
las bases para una evolución futura hacia el acceso a 
backlogs históricos completos de mayor escala. 
5. Funcionalidades de ARIA 
ARIA se operacionaliza a través de una plataforma 
web, en fase inicial de implementación, que permite 
aplicar los componentes de clasificación, validación, 
priorización y enriquecimiento en un entorno integrado y 
trazable. Su propuesta central no es solo a lmacenar 
requerimientos, sino curarlos, evaluarlos y optimizarlos 
en tiempo real con asistencia de inteligencia artificial. Las 
funcionalidades descritas a continuación se encuentran 
implementadas en esta primera versión de la plataforma, 
que se organiza en torno a un conjunto de módulos 
integrados que cubren el ciclo completo de gestión, 
evaluación y mejora de requerimientos. 
5.1. Dashboard de calidad global 
La pantalla principal de ARIA ofrece una visión 
ejecutiva del estado del backlog mediante una métrica 
agregada de calidad calculada a partir de los resultados 
del Validador. Esta métrica se desagrega en las tres 
dimensiones del modelo: Adecuación funcional, 
Especificación y Mantenibilidad, permitiendo identificar 
de manera inmediata qué aspectos del conjunto de 
requerimientos presentan mayor incidencia de problemas. 
El dashboard incluye además la evolución de la calidad 
respecto a períodos anteriores, lo que habilita el 
seguimiento del impacto de las decisiones de 
refinamiento a lo largo del ciclo de desarrollo. 
5.2. Requirements Hub 
El Requirements Hub constituye el centro de gestión 
del backlog dentro de ARIA. Presenta un listado 
centralizado de requerimientos con su identificador, 
descripción, tipo, score de calidad individual, criticidad y 
estado dentro del flujo de trabajo. El hub incorpora filtros 
por estado, criticidad y tipo de requerimiento, junto con 
indicadores visuales que permiten identificar rápidamente 
los ítems que requieren atención. Desde este módulo los 
usuarios pueden iniciar el análisis de un requerimiento 
individual o de un conjunto, exportar resultados e 
incorporar nuevos requerimientos al sistema de manera 
manual o mediante integración planificada a futuro con 
herramientas externas como Jira o Azure DevOps. 
5.3. Motor de análisis automático 
El motor de análisis constituye la capa de inteligencia 
central de ARIA. A partir de los agentes descritos en la 
sección anterior, el sistema detecta automáticamente 
problemas de calidad semántica en los requerimientos: 
ambigüedad, incompletitud, multiplic idad, baja 
verificabilidad, redundancias y solapamientos con otros 
elementos del backlog. Cada problema detectado se 
presenta con una descripción específica que explica por 
qué el requerimiento presenta esa condición, superando la 
lógica de los linters sin tácticos tradicionales al operar 
sobre el contenido semántico del requerimiento en su 
contexto. 
El motor también calcula el score de calidad 
individual de cada requerimiento, expresado como un 
valor porcentual acompañado de una clasificación de 
severidad: crítica, moderada o baja. Esta combinación 
permite a los equipos priorizar no solo por valor de 
negocio sino también por riesgo de mala definición, 
incorporando una dimensión objetiva al proceso de 
refinamiento del backlog. 
5.4. Flujo de análisis y enriquecimiento 
Una vez procesado por el motor de análisis, cada 
requerimiento accede a una vista de detalle que presenta 
de manera integrada los resultados del Clasificador, el 
Validador y el Priorizador, junto con la propuesta de 
mejora generada por el Agente Enriqueced or. Esta 

## Page 6

propuesta incluye una versión reformulada del 
requerimiento en formato estructurado, una justificación 
de cada cambio aplicado y, cuando corresponde, criterios 
de aceptación sugeridos. 
El usuario puede aceptar la propuesta, rechazarla o 
ajustarla manualmente mediante un campo de interacción 
directa con el sistema. Esta lógica de aceptar, ajustar o 
rechazar preserva el juicio del equipo como instancia final 
de decisión y refuerza el carác ter de asistencia cognitiva 
de ARIA. El requerimiento resultante, una vez aprobado, 
se incorpora al backlog refinado con sus métricas e 
indicadores de calidad asociados. 
5.5. Insights contextuales 
ARIA incorpora una capa de recomendaciones 
proactivas basadas en patrones identificados dentro del 
set de requerimientos analizado. A medida que el sistema 
procesa más requerimientos, la memoria semántica 
acumula información sobre recurrencias y decisiones  
previas, de modo que ante nuevos requerimientos con 
características similares el sistema cuenta con evidencia 
acumulada que enriquece y precisa su análisis . Con la 
evolución hacia el acceso a backlogs históricos completos 
mencionada en la Sección 4.4, este componente sentará 
las bases para una plataforma de aprendizaje 
organizacional capaz de adaptarse progresivamente a las 
características particulares de cada proyecto y equipo. 
6. Limitaciones 
La propuesta presentada en este trabajo se encuentra 
en una fase inicial de implementación, lo que implica un 
conjunto de limitaciones que deben considerarse al 
interpretar sus alcances. En primer lugar, el modelo de 
calidad y la arquitectura multiagente n o han sido 
validados empíricamente en contextos reales de 
desarrollo, por lo que los criterios de evaluación y las 
métricas operativas propuestas representan una 
fundamentación teórica sujeta a ajuste. En segundo lugar, 
la versión actual de ARIA opera sobr e sets acotados de 
requerimientos seleccionados por el equipo, lo que limita 
su aplicabilidad directa a backlogs de gran escala o con 
alta densidad histórica. En tercer lugar, la calidad de los 
resultados generados por los agentes depende en parte de 
las capacidades y limitaciones inherentes a los modelos 
de lenguaje utilizados, incluyendo posibles alucinaciones, 
sesgos en la interpretación semántica o variabilidad en las 
sugerencias ante requerimientos similares. Finalmente, la 
integración con herramientas externas como Jira o Azure 
DevOps se encuentra planificada pero no implementada 
en esta versión, lo que acota el flujo de trabajo a la interfaz 
propia de la plataforma.  
7. Diseño de validación 
La validación empírica de ARIA se plantea en dos 
niveles complementarios. A nivel conceptual, se prevé la 
aplicación del modelo de evaluación en estudios de caso 
controlados con equipos ágiles reales, utilizando como 
referencia el Agile Quality Framework ( AQF) [19] para 
contrastar los resultados obtenidos por el Validador con 
evaluaciones realizadas por expertos. Las métricas de 
interés incluirán el grado de coincidencia entre el 
diagnóstico automático y el juicio experto, la utilidad 
percibida de las suger encias del Enriquecedor y el 
impacto del Índice de Alineación de Prioridad en las 
decisiones de refinamiento del equipo. 
A nivel de plataforma , se diseñará un protocolo de 
evaluación con usuarios que permita medir la usabilidad 
de la plataforma, la confianza de los equipos en las 
recomendaciones generadas y el impacto en la calidad del 
backlog antes y después de su uso. Este protocolo 
contemplará sesiones de refinamiento asistido con 
Product Owners y analistas, recolección de feedback 
estructurado y análisis comparativo de la calidad de los 
requerimientos procesados. Los resultados de esta 
validación permitirán ajustar tanto el modelo conceptual 
como los parámetros operativos de los agentes, 
consolidando la propuesta en una plataforma robusta y 
aplicable en entornos industriales reales. 
8. Conclusiones y trabajos futuros 
Este trabajo presentó ARIA, una plataforma 
inteligente para la gestión y mejora de requerimientos 
ágiles que operacionaliza un modelo de calidad 
estructurado en tres componentes conceptuales: 
Clasificador, Validador y Priorizador, mediante una 
arquitectura multiagente coordinada por un kernel 
orquestador. La plataforma incorpora además un Agente 
Enriquecedor que transforma los resultados del análisis 
en sugerencias concretas y revisables de mejora, cerrando 
el ciclo entre diagnóstico y refinamiento activo del 
backlog. 
El aporte central de ARIA respecto de trabajos previos 
de esta línea de investigación reside en la transición desde 
un modelo conceptual hacia una implementación concreta 
que articula evidencia empírica, criterios de calidad 
formalizados, métricas operativ as y asistencia cognitiva 
basada en inteligencia artificial. A diferencia de las 
herramientas disponibles actualmente en la industria, 
ARIA no se limita a registrar y hacer seguimiento de 
requerimientos, sino que introduce una lógica de curación 
activa del  backlog que permite detectar problemas 
semánticos, identificar discrepancias entre la prioridad 
asignada por el equipo y la estimada por la plataforma, y 
proponer mejoras contextualizadas antes de que los 
requerimientos avancen hacia etapas de desarrollo [1, 2, 8]. 

## Page 7

La propuesta se distingue además por su carácter no 
sustitutivo: ARIA actúa como asistente cognitivo para 
Product Owners, analistas y equipos de desarrollo, 
aportando evidencia cuantificable y recomendaciones 
accionables sin reemplazar el juicio experto de l equipo. 
Esta distinción es central para su adopción en contextos 
ágiles reales, donde la velocidad de las decisiones y la 
confianza en el criterio del equipo son valores 
fundamentales. 
Entre los trabajos futuros se destacan cuatro líneas 
prioritarias. En primer lugar, la ejecución del protocolo 
de validación empírica descrito en la Sección 7, cuyos 
resultados permitirán ajustar el modelo de calidad y 
extender su aplicación a equipos, organizaciones y 
dominios adicionales más allá de los casos de estudio  
iniciales. En segundo lugar, la implementación del patrón 
RAG (Retrieval -Augmented Generation) para que los 
agentes accedan al backlog completo y a los 
requerimientos históricos almacenados en la memoria 
semántica como contexto extendido antes de generar 
respuestas o sugerencias. En tercer lugar, el ajuste y 
optimización de los prompts utilizados por cada agente, 
junto con el desarrollo de nuevas habilidades que mejoren 
su desempeño y capacidad de adaptación dentro del flujo 
operativo. Finalmente, el diseño e impleme ntación de un 
módulo de feedback que permita a los usuarios 
retroalimentar el sistema, fortaleciendo el aprendizaje 
continuo de la memoria semántica y la capacidad de 
adaptación de los agentes a lo largo del tiempo. 
En síntesis, ARIA representa un paso concreto hacia 
ecosistemas inteligentes de gestión de requerimientos con 
aprendizaje incremental, trazabilidad avanzada y análisis 
semántico integrado al ciclo ágil, contribuyendo a cerrar 
la brecha entre investigación académica y práctica 
industrial en ingeniería de requerimientos. 
Agradecimientos 
Este trabajo se enmarca en las actividades 
relacionadas con el Proyecto de Investigación “Métodos, 
técnicas y herramientas para mejorar y evaluar la calidad 
de requisitos en proyectos ágiles de Software” (PID 
SIECRE0008643) financiado por la Secretaría de Ciencia 
y Tecnología de la Universidad Tecnológica Nacional, 
ambos en la órbita del Centr o de Investigación Aplicada 
en Tecnologías de la Información y Comunicación 
(CInApTIC) de la Facultad Regional Resistencia de la 
Universidad Tecnológica Nacional. 
Agradecemos el invaluable aporte de los docentes 
investigadores, miembros del proyecto nombrado 
anteriormente, Dr. César Acuña y al Ing. Nicolás Tortosa. 
Referencias 
[1] Gupta, A., Poels, G., & Bera, P., "Using Conceptual Models 
in Agile Software Development: A Possible Solution to 
Requirements Engineering Challenges in Agile Projects", IEEE 
Access, 10, 2022, pp. 119745-119766. 
[2] Franch, X., Palomares, C., Quer, C., Chatzipetrou, P., & 
Gorschek, T., "The state -of-practice in requirements 
specification: an extended interview study at 12 companies", 
Requirements Engineering, 28(3), 2023, pp. 377-409. 
[3] digital.ai, "17th State of Agile Report", 2024, 
https://info.digital.ai/rs/981-LQX-968/images/RE-SA-17th-
Annual-State-Of-Agile-Report.pdf 
[4] Arora, C., Grundy, J., & Abdelrazek, M., "Advancing 
Requirements Engineering through Generative AI: Assessing 
the Role of LLMs", en Generative AI for Effective Software 
Development, Springer Nature Switzerland, 2024, pp. 129–148. 
[5] Khan, J. A., Qayyum, S., & Dar, H. S., "Large Language 
Model for Requirements Engineering: A Systematic Literature 
Review", Research Square (preprint), 2025. 
https://doi.org/10.21203/rs.3.rs-5589929/v1 
[6] Liu, J., et al., "Large Language Model -Based Agents for 
Software Engineering: A Survey", arXiv preprint 
arXiv:2409.02977, 2024. 
[7] He, J., Treude, C., & Lo, D., "LLM -Based Multi -Agent 
Systems for Software Engineering: Literature Review, Vision 
and the Road Ahead", arXiv preprint arXiv:2404.04834, 2024. 
[8] Jin, D., Jin, Z., Chen, X., & Wang, C., "MARE: Multi -
Agents Collaboration Framework for Requirements 
Engineering", arXiv preprint arXiv:2405.03256, 2024. 
[9] Tomaselli, G., Pinto, N., Acuña, C., Martínez, D., & 
Ferrazzano, A., "Aplicación de Técnicas de Ingeniería de 
Software Empírica para Relevar Prácticas Actuales en la 
Gestión de Requerimientos Ágiles", CONAIISI 2024, pp. 627–
637. 
[10] Tomaselli, G., Pinto, N., Martínez, D., et al., "Marco de 
trabajo para mejorar la calidad de requerimientos ágiles: una 
primera aproximación", CONAIISI 2025. 
[11] Lubos, S., Felfernig, A., Tran, T.N.T., et al., "Leveraging 
LLMs for the Quality Assurance of Software Requirements", en 
IEEE 32nd International Requirements Engineering Conference 
(RE), IEEE, 2024, pp. 389–397. 
[12] Meckenstock, J. N., "Shedding light on the dark side – A 
systematic literature review of the issues in agile software 
development methodology use", Journal of Systems and 
Software, 211, 2024, p. 111966. 
[13] IEEE, "IEEE Std 830-1998 - IEEE Recommended Practice 
for Software Requirements Specifications", Institute of 
Electrical and Electronics Engineers, 1998. 

## Page 8

[14] ISO/IEC, "ISO/IEC 25010:2023 - Systems and software 
engineering — Systems and software Quality Requirements and 
Evaluation (SQuaRE) — Product quality model", International 
Organization for Standardization, Geneva, Switzerland, 2023. 
[15] ISO/IEC/IEEE, "ISO/IEC/IEEE 29148:2018 - Systems and 
software engineering — Life cycle processes — Requirements 
engineering", Geneva, Switzerland, 2018. 
[16] Wu, Q., Bansal, G., Zhang, J., et al., "AutoGen: Enabling 
Next-Gen LLM Applications via Multi -Agent Conversations", 
en Proceedings of the First Conference on Language Modeling 
(COLM 2024), 2024. 
[17] LangChain, "LangChain: Building applications with LLMs 
through composability", 2024. Disponible: 
https://www.langchain.com 
[18] Tomaselli, G.P., Pinto, N.S., Acuña, C., "Requirements 
management methods and practices for improving the quality of 
agile software development processes: a review of the 
literature", Requirements Engineering, 2025. 
https://doi.org/10.1007/s00766-025-00448-3 
[19] Pinto, N., Tortosa, N., Geat, B. C., Ibáñez, L., & Bollati, 
V., "Quality evaluation of agile processes: Measurement of 
requirements management using AQF v2", in 11th International 
Conference on the Quality of Information and Communications 
Technology (QUATIC 2018), IEEE, 2018, pp. 15-20. 
 
