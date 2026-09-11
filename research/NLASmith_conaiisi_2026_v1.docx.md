**NLASmith: Un Framework para la Evaluación Sistemática de Natural Language Activations**

&nbsp;

***Universidad Tecnológica Nacional, Facultad Regional Resistencia***

&nbsp;

**Abstract**

*El análisis de Natural Language Activations, o NLA, ofrece una nueva forma de estudiar qué información representan internamente los modelos de lenguaje. Herramientas como Neuronpedia facilitan la exploración de estas verbalizaciones mediante una interfaz web accesible y también ofrecen mecanismos programáticos para automatizar su procesamiento. Sin embargo, las interfaces disponibles están principalmente orientadas a la exploración de activaciones individuales, mientras que la ejecución de experimentos sistemáticos sobre múltiples ejemplos requiere coordinar de manera explícita la selección de posiciones, la recolección de verbalizaciones, su evaluación y la agregación de resultados. En este trabajo presentamos NLASmith, un framework orientado a integrar estas etapas dentro de una infraestructura general de experimentación. La propuesta permite ejecutar múltiples pruebas bajo una misma configuración, evaluar automáticamente las verbalizaciones mediante criterios definidos por el investigador y agregar los resultados para facilitar su comparación y análisis. De este modo, un mismo flujo puede utilizarse para estudiar distintas hipótesis sobre las representaciones internas de los modelos sin quedar limitado a un único fenómeno o dominio. Como primera prueba de viabilidad, desarrollamos un prototipo funcional que integra las principales etapas del proceso propuesto. Nuestro objetivo es reducir el trabajo necesario para configurar este tipo de experimentos, mejorar su reproducibilidad y facilitar nuevas investigaciones basadas en NLA.*

**Palabras Clave**

Natural Language Activations, Natural Language Autoencoders, interpretabilidad, LLM-as-a-judge, Neuronpedia, evaluación reproducible.

**1\. Introducción**

Las aplicaciones basadas en modelos de lenguaje de gran escala (LLM) presentan desafíos de evaluación distintos de los sistemas de software tradicionales. En un sistema determinístico es habitual definir una entrada y verificar que la salida coincida con un valor esperado. En una aplicación generativa, en cambio, una misma entrada puede producir respuestas diferentes sin que esa variación implique necesariamente un error. Esta característica vuelve necesario evaluar comportamientos sobre múltiples ejecuciones y mediante criterios que excedan la comparación exacta de salidas.

En la evaluación de aplicaciones basadas en LLM ya existen herramientas que sistematizan este enfoque. LangSmith, por ejemplo, organiza experimentos alrededor de datasets, múltiples ejecuciones, evaluadores automáticos y vistas comparativas entre resultados \[3\]. Entre sus mecanismos se encuentra el uso de LLM-as-a-judge, donde un modelo de lenguaje actúa como evaluador de las respuestas producidas según una rúbrica previamente definida. Este enfoque permite convertir observaciones cualitativas en métricas agregadas y comparar configuraciones bajo condiciones consistentes.

El estudio de Natural Language Activations presenta una necesidad análoga. Los Natural Language Autoencoders (NLA), introducidos por Fraser-Taliente et al., transforman activaciones internas de un modelo en descripciones en lenguaje natural mediante un Activation Verbalizer y reconstruyen posteriormente la activación a partir de ese texto \[1\]. Estas verbalizaciones ofrecen una representación interpretable de la activación, aunque no deben entenderse como una descripción literal o infalible del estado interno del modelo.

Neuronpedia es una plataforma abierta de interpretabilidad que permite explorar activaciones y artefactos asociados a distintos modelos mediante una interfaz web accesible. Entre esos recursos se incluyen NLA publicados por la comunidad. La plataforma también ofrece una API que permite automatizar la generación de respuestas y la recuperación de verbalizaciones correspondientes a posiciones concretas \[2\]. Estas capacidades hacen posible construir experimentos programáticos, aunque la definición y coordinación del flujo experimental quedan fuera del alcance de la interfaz de exploración.

Este trabajo propone NLASmith, un framework orientado a cubrir esa brecha metodológica. Su contribución no consiste en introducir una nueva técnica de interpretabilidad ni en entrenar un nuevo NLA, sino en proporcionar infraestructura para definir, ejecutar y comparar experimentos reproducibles sobre verbalizaciones existentes. NLASmith integra datasets, políticas de selección de tokens, acceso a NLA, evaluadores configurables y métricas agregadas dentro de un único flujo experimental.

El resto del trabajo se organiza de la siguiente manera. La Sección 2 presenta las motivaciones y delimita el problema metodológico. La Sección 3 describe el modelo conceptual de NLASmith. La Sección 4 desarrolla su arquitectura y componentes. La Sección 5 presenta las funcionalidades y el prototipo implementado. La Sección 6 introduce un caso de uso y el diseño de validación. La Sección 7 analiza trabajos relacionados, la Sección 8 explicita las principales limitaciones y la Sección 9 presenta las conclusiones y líneas de trabajo futuro.

**2\. Motivación**

**2.1. De la inspección individual al experimento sistemático**

Las herramientas disponibles permiten inspeccionar activaciones y verbalizaciones concretas de forma accesible. Sin embargo, estudiar patrones sobre múltiples ejemplos requiere coordinar de manera explícita varias decisiones experimentales, entre ellas qué prompts ejecutar, qué posiciones observar, cómo conservar las verbalizaciones obtenidas, con qué criterio evaluarlas y cómo agregar los resultados. NLASmith parte de esta diferencia entre explorar una activación individual y conducir un experimento sistemático y reproducible.

El desafío se acentúa por el carácter no determinístico de los modelos generativos. Una única ejecución puede no ser representativa del comportamiento que se desea estudiar, por lo que resulta necesario observar múltiples ejemplos o repeticiones bajo una misma configuración. Esta necesidad es equivalente, en términos metodológicos, a la que llevó al desarrollo de plataformas de evaluación de aplicaciones con LLM, donde los resultados se analizan a partir de datasets, evaluadores y métricas agregadas en lugar de casos aislados.

**2.2. Flujo manual en experimentos con NLA**

Una exploración individual puede realizarse desde una interfaz como Neuronpedia o mediante llamadas programáticas a su API. Para convertir esa exploración en un experimento comparable entre múltiples ejemplos es necesario fijar previamente una política de posiciones, conservar la configuración de cada ejecución, recuperar las verbalizaciones correspondientes y aplicar criterios de evaluación consistentes. Cuando estas decisiones no forman parte de una misma definición experimental, la comparación entre corridas se vuelve más difícil de reproducir y auditar.

El problema, por lo tanto, no es la imposibilidad técnica de automatizar estas operaciones. Las piezas necesarias ya existen y pueden combinarse mediante scripts o infraestructura propia. El desafío que aborda este trabajo es integrarlas en un flujo explícito y configurable que conserve las decisiones del experimento, aplique evaluadores de manera consistente y produzca resultados agregados comparables.

**2.3. Oportunidad metodológica**

La oportunidad metodológica consiste en integrar estas capacidades dentro de un flujo experimental común. El investigador debería poder definir previamente el dataset, las posiciones de tokens a observar y el criterio con el que se evaluarán las verbalizaciones, ejecutar esa configuración sobre múltiples ejemplos y conservar tanto los resultados individuales como las métricas agregadas. Este enfoque busca hacer explícitas decisiones que, de otro modo, deben resolverse por separado en cada implementación experimental.

La motivación central de NLASmith es, por lo tanto, facilitar experimentos sistemáticos y reproducibles sobre NLA mediante una infraestructura común. La plataforma no pretende determinar el significado definitivo de una activación ni reemplazar el juicio del investigador. Su propósito es ofrecer un mecanismo configurable para ejecutar, evaluar, registrar y comparar experimentos manteniendo visibles las decisiones que producen cada resultado.

**3\. Modelo conceptual de NLASmith**

NLASmith organiza el experimento alrededor de cinco elementos principales: el dataset, la configuración de ejecución, la política de selección de tokens, los evaluadores y los resultados. La Figura 1 resume el flujo conceptual. Cada ejemplo del dataset se ejecuta bajo una configuración fija, las posiciones seleccionadas se envían al servicio de NLA y las verbalizaciones obtenidas son evaluadas según criterios definidos previamente. Finalmente, los resultados individuales se agregan para facilitar su análisis y comparación.

![][image1]

*Figura 1\. Pipeline conceptual de NLASmith.*

**3.1. Definición de un experimento**

Un experimento vincula un dataset de prompts con una fuente NLA, una política de selección de tokens y uno o más evaluadores. Esta definición debe persistirse y poder ejecutarse nuevamente sin reconstruir manualmente cada paso. Para cada ejemplo se conservan, como mínimo, el prompt, la respuesta del modelo, las posiciones analizadas, las verbalizaciones obtenidas y el feedback generado por los evaluadores.

**3.2. Política de selección de tokens**

La posición observada forma parte de la definición experimental y no debería decidirse después de inspeccionar cada respuesta. NLASmith permite expresar reglas relativas, como el último token de contenido del usuario, el primer token del asistente o una ventana de posiciones alrededor de un límite conversacional. Mantener esta política constante permite comparar observaciones bajo un criterio homogéneo.

**3.3. Evaluadores configurables**

El framework separa la obtención del NLA de su evaluación. Un evaluador puede consistir en una regla léxica o utilizar un LLM-as-a-judge con una rúbrica definida por el investigador. El formato de salida puede ser booleano, numérico o categórico. De este modo, el mismo mecanismo puede utilizarse para estudiar fenómenos diferentes sin modificar la lógica central de la plataforma.

Esta separación es relevante porque el evaluador automático no se considera una fuente de verdad sobre la activación, sino un instrumento de medición configurable. La rúbrica, el modelo utilizado como juez y la salida producida deben conservarse junto con la ejecución para que los resultados puedan auditarse, compararse y reproducirse.

**3.4. Métricas y reproducibilidad**

A partir del feedback producido para cada ejemplo, NLASmith calcula métricas agregadas como tasa de presencia, score medio, distribución por categoría y resultados segmentados por posición de token o subconjunto del dataset. Cuando la información de reconstrucción está disponible, puede presentarse junto con la verbalización como una señal adicional sobre la calidad del NLA. Estas métricas permiten desplazar el análisis desde observaciones aisladas hacia patrones cuantificables.

**4\. Arquitectura y componentes**

La arquitectura de NLASmith separa las responsabilidades de configuración, ejecución, acceso a NLA, evaluación, persistencia y visualización. El sistema no reimplementa ni entrena los autoencoders. Utiliza los NLA disponibles a través de Neuronpedia y coordina las operaciones necesarias para transformar un dataset en un conjunto trazable de observaciones y métricas.

![][image2]

*Figura 2\. Arquitectura general propuesta para NLASmith.*

**4.1. Interfaz de configuración**

La interfaz concentra los elementos que definen el experimento, incluidos el dataset, la fuente NLA, la política de tokens, el número de ejecuciones y los evaluadores. El objetivo es que estas decisiones queden establecidas antes de iniciar el proceso. La misma interfaz permite revisar experimentos previos y reutilizar configuraciones para favorecer comparaciones consistentes.

**4.2. Orquestador de experimentos**

El orquestador coordina el ciclo de cada ejemplo. Primero solicita la generación del modelo, luego resuelve las posiciones indicadas por la política de tokens y recupera las verbalizaciones correspondientes. Finalmente, envía los artefactos a los evaluadores configurados y persiste tanto los resultados finales como la información intermedia necesaria para reconstruir la ejecución.

**4.3. Integración con Neuronpedia**

Neuronpedia \[2\] concentra la infraestructura de inferencia utilizada por NLASmith. La plataforma aloja tanto los modelos de lenguaje empleados para generar las completions como los modelos NLA responsables de producir las verbalizaciones de las activaciones internas. Mediante sus endpoints de completion y explain, NLASmith puede ejecutar consultas y recuperar las explicaciones correspondientes a posiciones específicas de tokens sin necesidad de alojar localmente estos modelos.

NLASmith encapsula estas operaciones en un módulo de integración específico con Neuronpedia. Este módulo administra los identificadores del modelo y del NLA, realiza las solicitudes necesarias y transforma las respuestas obtenidas a un esquema interno común que luego utilizan los demás componentes de la plataforma. De esta manera, la lógica encargada de ejecutar experimentos, aplicar evaluadores y generar métricas puede trabajar sobre una representación uniforme, sin depender directamente de la estructura particular de las respuestas de la API.

**4.4. Capa de evaluación**

Los evaluadores reciben, para cada ejemplo, el prompt, la respuesta, el token, la posición y la verbalización. En LLM-as-a-judge, una rúbrica con marcadores se completa con esas variables y se envía a un modelo de OpenAI, que debe devolver una salida estructurada booleana, numérica o categórica, con justificación opcional.

NLASmith no aloja el juez. El usuario introduce su clave de API de OpenAI y elige el modelo. Neuronpedia produce completions y verbalizaciones; el juez las puntúa. Esa evaluación es un instrumento de medición, no una lectura infalible de la activación.

**4.5. Persistencia, agregación y visualización**

Cada ejecución experimental se almacena como una unidad identificable. La capa de persistencia conserva su configuración y los resultados por ejemplo, la capa de agregación calcula métricas a partir de las claves de feedback y el dashboard presenta tablas y gráficos que permiten inspeccionar casos individuales sin perder la perspectiva global del experimento.

**5\. Funcionalidades e implementación**

NLASmith se implementa como una plataforma web centrada en el ciclo experimental. La primera versión prioriza las capacidades necesarias para transformar una inspección manual en un proceso reproducible y evita incorporar funciones que no contribuyan directamente a ese objetivo.

**5.1. Gestión de datasets**

El investigador puede crear un dataset de prompts, identificar cada ejemplo y, cuando resulte útil, asociar metadatos o una referencia esperada. El dataset funciona como unidad de comparación. Dos experimentos que utilizan el mismo conjunto pueden contrastarse tanto a nivel de cada ejemplo como mediante métricas agregadas.

**5.2. Configuración de evaluadores**

Los evaluadores se definen mediante un nombre, una rúbrica, un modelo juez y un esquema de salida. Un investigador puede crear un evaluador temático sin modificar el código del framework. Por ejemplo, puede definir un criterio que detecte referencias explícitas a Reddit o una evaluación semántica sobre la presencia de una temática más general. Esta configurabilidad permite reutilizar la plataforma para preguntas de investigación diferentes.

**5.3. Ejecución y seguimiento**

Al iniciar una ejecución, el sistema recorre el dataset utilizando una configuración previamente definida y registra el progreso por ejemplo. Esto permite distinguir fallos de API de evaluaciones negativas, conservar un historial de experimentos y volver a inspeccionar los artefactos utilizados en cada decisión automática.

**5.4. Resultados y comparación**

La vista de resultados combina dos niveles de análisis. El nivel individual presenta el prompt, la respuesta generada, el token, la verbalización y el feedback. El nivel agregado resume las métricas por evaluador y permite segmentarlas según la posición o la configuración utilizada. Cuando existen ejecuciones comparables, la plataforma presenta sus resultados de manera conjunta para facilitar el contraste.

**5.5. Prototipo funcional**

Como prueba de viabilidad de la propuesta, se desarrolló un prototipo funcional de NLASmith que integra las principales etapas del flujo experimental. La versión actual permite configurar experimentos, trabajar con datasets de prompts, definir evaluadores, ejecutar consultas y presentar resultados individuales y agregados dentro de una misma interfaz.

Esta primera implementación constituye una base operativa para validar las decisiones de diseño y obtener retroalimentación de potenciales usuarios. La Figura 3 reserva el espacio destinado a mostrar la interfaz del prototipo. En esta versión del documento se utiliza una captura temporal como referencia visual hasta incorporar la interfaz definitiva de NLASmith.

&nbsp;

*Figura 3\. Captura temporal utilizada como referencia para el espacio destinado a la interfaz del prototipo de NLASmith.*

**6\. Caso de uso y diseño de validación**

**6.1. Caso de uso. Asociaciones con foros de Internet**

Como demostración inicial, NLASmith puede utilizarse para sistematizar una observación surgida durante exploraciones manuales. En determinadas preguntas abiertas, algunas verbalizaciones parecían estar relacionadas con Reddit o con géneros discursivos propios de foros, aun cuando la respuesta generada no mencionaba explícitamente esa fuente. Este escenario resulta útil como caso de uso porque permite transformar una observación cualitativa en una hipótesis medible mediante un evaluador configurable.

El objetivo de este caso no es establecer que Reddit constituya una fuente causal del modelo ni asumir que una verbalización describa de manera literal su estado interno. Su función es mostrar cómo una pregunta de investigación puede formalizarse como una configuración experimental que incluye un conjunto de prompts, una posición observada, una fuente NLA, un criterio de evaluación y métricas agregadas.

**6.2. Validación del evaluador y de la plataforma**

La validación se plantea en dos niveles complementarios. En primer lugar, debe evaluarse la señal producida por el juez automático. Para ello se propone construir una muestra de verbalizaciones etiquetada manualmente y medir el grado de acuerdo entre las decisiones humanas y las evaluaciones automáticas. Un evaluador léxico puede utilizarse además como línea de base para distinguir coincidencias explícitas de asociaciones semánticas más amplias.

En segundo lugar, debe evaluarse la utilidad del framework como infraestructura experimental. Se propone medir el tiempo necesario para configurar y reproducir un experimento frente al procedimiento manual, la capacidad de un tercero para repetir la misma configuración y la consistencia de los artefactos obtenidos. Como siguiente etapa, se buscará difundir el prototipo entre investigadores vinculados con interpretabilidad y NLA para recopilar retroalimentación sobre su utilidad, configurabilidad y aplicabilidad a distintos escenarios de investigación.

**7\. Trabajos relacionados**

Los Natural Language Autoencoders proponen una forma de comprimir activaciones en descripciones de lenguaje natural y reconstruir posteriormente la representación original a partir de esas descripciones \[1\]. El trabajo introduce además precauciones relevantes para su interpretación y utiliza modelos de lenguaje auxiliares dentro de protocolos experimentales para extraer y evaluar propiedades de las explicaciones. Este antecedente muestra que la evaluación automática de verbalizaciones NLA es viable, aunque se presenta como parte de experimentos específicos y no como una infraestructura general destinada a configurar nuevas evaluaciones.

Neuronpedia proporciona una interfaz pública para explorar distintos métodos y artefactos de interpretabilidad, incluidos NLA, y ofrece además una API que permite automatizar su acceso \[2\]. Estas capacidades constituyen la base técnica sobre la que NLASmith organiza la ejecución y recuperación de verbalizaciones, sin reemplazar ni reimplementar los modelos NLA disponibles.

En el ámbito de evaluación de aplicaciones basadas en LLM, LangSmith organiza el trabajo alrededor de datasets, experimentos, evaluadores y comparación de resultados \[3\]. NLASmith adopta una lógica metodológica similar para un objeto de evaluación diferente, ya que el elemento analizado no es únicamente la respuesta visible del modelo, sino la verbalización NLA asociada a posiciones determinadas por la configuración experimental.

La contribución de NLASmith no radica en introducir componentes completamente nuevos, sino en integrar capacidades ya disponibles dentro de una infraestructura general de experimentación. El framework busca hacer explícitas y reutilizables las decisiones necesarias para configurar, ejecutar, evaluar y comparar experimentos sobre NLA.

**8\. Limitaciones**

NLASmith hereda las limitaciones de los instrumentos sobre los que opera. Una verbalización NLA no constituye una lectura infalible de una activación y puede contener simplificaciones o detalles espurios \[1\]. Del mismo modo, un LLM-as-a-judge puede ser sensible a la formulación de la rúbrica, al modelo seleccionado y a la información incluida en el contexto. Por este motivo, las evaluaciones automáticas deben interpretarse como mediciones sujetas a validación y no como evidencia definitiva sobre el estado interno del modelo.

La cobertura del framework también depende de la disponibilidad de NLA y de las capacidades de las APIs utilizadas. Las comparaciones entre modelos pueden involucrar capas, autoencoders o configuraciones que no sean estrictamente equivalentes. Además, incrementar el número de prompts, posiciones y evaluadores eleva el costo y el tiempo de ejecución. Estas restricciones deberán considerarse al diseñar experimentos y al interpretar comparaciones entre configuraciones.

**9\. Conclusión y trabajos futuros**

Este trabajo presentó NLASmith, un framework para la evaluación sistemática de Natural Language Activations. La propuesta integra en un mismo flujo capacidades que ya pueden utilizarse de manera independiente, como la ejecución programática de prompts, la selección de posiciones, la recuperación de verbalizaciones NLA, su evaluación automática y la agregación de resultados. El objetivo es hacer que estas decisiones formen parte de una configuración experimental explícita, reproducible y comparable.

El aporte central de NLASmith no consiste en introducir una nueva técnica de interpretabilidad ni en hacer posible una operación que antes no pudiera automatizarse. Su contribución es proporcionar una infraestructura experimental que permita pasar de la exploración individual de activaciones a la evaluación sistemática de patrones sobre múltiples ejemplos, conservando las configuraciones, criterios de evaluación y resultados necesarios para reproducir el análisis.

Como líneas de trabajo futuro se plantea completar la validación empírica mediante experimentos propios, incluyendo la comparación entre evaluaciones automáticas y anotaciones humanas, la repetición de ejecuciones para estimar variabilidad y el análisis de distintas políticas de selección de tokens. También se prevé difundir el prototipo entre investigadores vinculados con interpretabilidad y NLA para obtener retroalimentación sobre su utilidad, configurabilidad y capacidad para adaptarse a preguntas de investigación diferentes. Estos resultados permitirán refinar tanto la plataforma como el protocolo experimental propuesto.

**Agradecimientos**

\[Completar en camera ready con nombres y apellidos de los docentes tutores.\]

**Referencias**

\[1\] K. Fraser-Taliente et al., “Natural Language Autoencoders Produce Unsupervised Explanations of LLM Activations”, Transformer Circuits Thread, 2026\. https://transformer-circuits.pub/2026/nla/

\[2\] Neuronpedia, “Natural Language Autoencoders: demo and API”, 2026\. https://www.neuronpedia.org/nla

\[3\] LangChain, “LangSmith: evaluation and experiment tracking for LLM applications”. https://docs.smith.langchain.com/

\[4\] Anthropic, “Natural Language Autoencoders”, 2026\. https://www.anthropic.com/research/natural-language-autoencoders

\[5\] kitft, “natural\_language\_autoencoders”, GitHub. https://github.com/kitft/natural\_language\_autoencoders

**Datos de Contacto**

*Completar en camera ready. Nombre y Apellido. Universidad Tecnológica Nacional, Facultad Regional Resistencia. Dirección postal. E-mail.*

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,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>