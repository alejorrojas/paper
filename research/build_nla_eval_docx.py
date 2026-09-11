#!/usr/bin/env python3
"""Build CoNaIISI student paper: NLA Eval."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Twips

OUT = Path(__file__).resolve().parent / "conaiisi_2026_nla_eval.docx"
TNR = "Times New Roman"


def _rfonts(run, name: str = TNR) -> None:
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), name)
    rFonts.set(qn("w:hAnsi"), name)
    rFonts.set(qn("w:cs"), name)
    rFonts.set(qn("w:eastAsia"), name)


def set_run(run, size: int, *, bold=False, italic=False) -> None:
    run.font.name = TNR
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)
    _rfonts(run)


def add_p(
    doc,
    text: str,
    size: int,
    *,
    bold=False,
    italic=False,
    align="left",
    space_after=6,
    space_before=0,
    justify=False,
):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    pf.line_spacing = 1.0
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    elif align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "right":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    set_run(run, size, bold=bold, italic=italic)
    return p


def heading(doc, text: str, size: int = 12) -> None:
    add_p(doc, text, size, bold=True, space_before=10, space_after=6)


def body(doc, text: str, size: int = 12) -> None:
    add_p(doc, text, size, justify=True, space_after=6)


def set_a4(section) -> None:
    section.page_width = Twips(11907)
    section.page_height = Twips(16840)
    section.orientation = WD_ORIENT.PORTRAIT
    section.top_margin = Twips(1418)
    section.bottom_margin = Twips(1418)
    section.left_margin = Twips(1418)
    section.right_margin = Twips(1418)
    section.header_distance = Cm(0)
    section.footer_distance = Cm(0)


def _strip_cols_and_page_num(sect_pr) -> None:
    for child in list(sect_pr):
        if child.tag in (qn("w:cols"), qn("w:pgNumType")):
            sect_pr.remove(child)


def set_title_block_section(section) -> None:
    set_a4(section)
    _strip_cols_and_page_num(section._sectPr)
    pg_num = OxmlElement("w:pgNumType")
    pg_num.set(qn("w:fmt"), "none")
    section._sectPr.append(pg_num)


def set_two_equal_columns(section) -> None:
    set_a4(section)
    sect_pr = section._sectPr
    _strip_cols_and_page_num(sect_pr)
    cols = OxmlElement("w:cols")
    cols.set(qn("w:equalWidth"), "0")
    cols.set(qn("w:num"), "2")
    col0 = OxmlElement("w:col")
    col0.set(qn("w:space"), "567")
    col0.set(qn("w:w"), "4252")
    col1 = OxmlElement("w:col")
    col1.set(qn("w:space"), "0")
    col1.set(qn("w:w"), "4252")
    cols.append(col0)
    cols.append(col1)
    sect_pr.append(cols)
    pg_num = OxmlElement("w:pgNumType")
    pg_num.set(qn("w:fmt"), "none")
    sect_pr.append(pg_num)


def shade_header_cells(row) -> None:
    for cell in row.cells:
        tc = cell._tc
        tc_pr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), "E8E8E8")
        shd.set(qn("w:val"), "clear")
        tc_pr.append(shd)


def fig_caption(doc, text: str) -> None:
    add_p(doc, text, 10, italic=True, align="center", space_before=8, space_after=8)


def add_table(doc, headers: list[str], rows: list[tuple[str, ...]]) -> None:
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h)
        set_run(run, 9, bold=True)
    shade_header_cells(table.rows[0])
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            cell = table.rows[i].cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(val)
            set_run(run, 8)



def main() -> None:
    doc = Document()
    set_title_block_section(doc.sections[0])

    add_p(
        doc,
        "Un marco de evaluación para Natural Language Autoencoders",
        16,
        bold=True,
        align="center",
        space_after=2,
    )
    add_p(
        doc,
        "De la inspección puntual al experimento reproducible",
        16,
        bold=True,
        align="center",
        space_after=12,
    )
    add_p(doc, " ", 14, bold=True, align="center", space_after=0)
    add_p(
        doc,
        "Universidad Tecnológica Nacional, [Unidad académica a completar]",
        12,
        bold=True,
        italic=True,
        align="center",
        space_after=6,
    )
    add_p(
        doc,
        "Nota. La versión para evaluación debe ser ciega. La sección Autores se deja en blanco y se completa solo en camera ready si el trabajo es aceptado.",
        10,
        italic=True,
        justify=True,
        space_after=10,
    )

    section1 = doc.add_section(WD_SECTION.CONTINUOUS)
    set_two_equal_columns(section1)

    heading(doc, "Abstract", 10)
    add_p(
        doc,
        (
            "Este trabajo presenta NLA Eval, una plataforma orientada a la evaluación "
            "sistemática de verbalizaciones de activación producidas por Natural "
            "Language Autoencoders (NLA). Un NLA comprime el vector de activación de "
            "un modelo de lenguaje en un texto breve y reconstruye ese vector a partir "
            "del texto. Ese texto, llamado Activation Verbalizer (AV), es un "
            "señalizador interpretable, no una lectura literal de las creencias del "
            "modelo. Neuronpedia permite inspeccionar un chat y un token a la vez, "
            "pero no cubre el ciclo completo de experimento sobre NLA públicos. "
            "Anthropic aplica un LLM como juez sobre AVs en un estudio de awareness "
            "de evaluación, como método interno de un paper, no como herramienta "
            "reutilizable. NLA Eval operacionaliza ese ciclo mediante datasets de "
            "prompts, una política de tokens, llamadas a la API de Neuronpedia, "
            "evaluadores configurables y una vista de comparación de corridas. El "
            "objeto evaluado es el AV en una posición de token, no la respuesta "
            "pública del modelo. La validación empírica en contextos de investigación "
            "y el acuerdo humano-juez sobre un corpus etiquetado constituyen los pasos "
            "siguientes para consolidar su impacto."
        ),
        10,
        italic=True,
        justify=True,
        space_after=8,
    )

    heading(doc, "Palabras Clave", 10)
    add_p(
        doc,
        "Natural Language Autoencoders, interpretabilidad, LLM-as-judge, Neuronpedia, evaluación de modelos de lenguaje",
        10,
        space_after=12,
    )

    heading(doc, "1. Introducción")
    body(
        doc,
        "Los modelos de lenguaje de gran escala (LLM) se evalúan, en la práctica "
        "industrial, sobre lo que dicen. Suites de prompts, métricas y jueces "
        "automáticos comparan respuestas, costos y tasas de error. Ese enfoque "
        "alcanza cuando el objeto de interés es la salida. Quiebra cuando el "
        "fenómeno vive en las activaciones internas y no aparece en el texto que el "
        "usuario lee.",
    )
    body(
        doc,
        "Los Natural Language Autoencoders, introducidos por Fraser-Taliente y "
        "colaboradores en Transformer Circuits [1], atacan exactamente ese hueco. Un "
        "NLA es un autoencoder cuyo cuello de botella es texto en lenguaje natural. "
        "El Activation Verbalizer produce una verbalización. El Activation "
        "Reconstructor intenta recuperar el vector. El error de reconstrucción "
        "(MSE o RMSE) indica cuán leíble es esa verbalización, no si una frase "
        "aislada es verdadera.",
    )
    body(
        doc,
        "Neuronpedia, en colaboración con Anthropic, hostea checkpoints públicos "
        "(por ejemplo Llama 3.3 70B con kitft-l53 y Gemma 3 27B con kitft-l41) y "
        "una API de completion y explain [2]. El producto es un microscopio. Un "
        "prompt, un modelo, una pestaña. Quien investiga un tema (un prior de foro, "
        "un riesgo, una awareness de evaluación) termina exportando capturas, "
        "eligiendo a mano el último token del usuario y el primero del asistente, "
        "y pegando verbalizaciones en otro chat para que un segundo modelo encuentre "
        "el patrón. Ese flujo no es un experimento. Es artesanía.",
    )
    body(
        doc,
        "El presente trabajo presenta NLA Eval, una plataforma que cierra ese ciclo "
        "sobre NLA públicos. No se inventa el LLM-as-judge sobre verbalizaciones. "
        "Anthropic lo usó para marcar awareness de evaluación no verbalizada, con un "
        "grader sobre 50 tokens de respuesta y un 97 % de acuerdo con los autores en "
        "186 ítems [1]. Se cambia el objeto evaluado y se materializa el laboratorio "
        "que hoy falta. El resto del artículo se organiza así. La Sección 2 formula "
        "las motivaciones. La Sección 3 resume el modelo conceptual. La Sección 4 "
        "describe la arquitectura. La Sección 5 detalla las funcionalidades de la "
        "plataforma. La Sección 6 diseña la validación. La Sección 7 discute "
        "limitaciones. La Sección 8 concluye. La Sección 9 sitúa las referencias de "
        "diseño que orientaron el recorte funcional.",
    )

    heading(doc, "2. Motivaciones")
    body(
        doc,
        "Tres tensiones justifican la plataforma. Primero, el no determinismo. Un "
        "test clásico de API afirma que, dado un input, el output es uno. Un NLA, "
        "como el modelo que explica, no se presta a esa igualdad. Hace falta una "
        "política fija de tokens, un juez con rúbrica, y tasas a lo largo de un "
        "dataset, no una captura. Segundo, la escala. El límite de explain de "
        "Neuronpedia (del orden de 16 posiciones por pedido y un tope horario) "
        "convierte cada comparación entre fuentes NLA en un trabajo de scripts y "
        "JSON. Sin un orquestador, el investigador elige el token interesante en cada "
        "corrida y destruye la comparabilidad. Tercero, el vacío de herramienta. "
        "Las plataformas de evaluación de aplicaciones con IA operan sobre la "
        "salida visible. Neuronpedia no conoce datasets, claves de feedback ni "
        "gráficos de hit rate. Los jueces opcionales usados al entrenar un NLA "
        "puntúan calidad de entrenamiento (coherencia, unicidad), no hipótesis "
        "experimentales sobre AVs ya desplegados [1].",
    )
    body(
        doc,
        "El motivo es fomentar investigación sobre NLA, no el entrenamiento de NLA "
        "nuevos, sistematizando lo que hoy se hace a mano con capturas y un chat.",
    )

    heading(doc, "3. Modelo conceptual")
    body(
        doc,
        "NLA Eval se organiza en torno a cinco objetos. La Tabla 1 resume el recorte.",
    )
    fig_caption(doc, "Tabla 1. Objetos de NLA Eval.")
    add_table(
        doc,
        ["Objeto", "Rol"],
        [
            ("Dataset", "Lista de prompts. Referencia opcional para el juez"),
            ("Política de tokens", "Qué posiciones se explican en cada corrida"),
            ("Experimento", "Corrida sobre un dataset, una fuente y evaluadores"),
            ("Artefacto", "completion, AVs, mse y token"),
            ("Claves de feedback", "Boolean, score o categoría"),
        ],
    )
    body(
        doc,
        "Una política de tokens, por defecto, fija el último token de contenido del "
        "mensaje de usuario y el primer token de la respuesta del asistente. El "
        "investigador puede elegir una, la otra, o ambas. El MSE actúa como "
        "compuerta. Un AV con error alto no se lee como evidencia. Se reporta como "
        "verbalización poco reconstruible.",
    )
    body(
        doc,
        "El juez no puntúa la creencia del modelo. Produce una señal interpretable. "
        "Si la rúbrica pide tema de foro o comunidad, un true no prueba un origen de "
        "corpus. Apoya una hipótesis que el output solo no mostraba, a validar con "
        "más tests [1].",
    )
    heading(doc, "3.1 Tipos de evaluador", 12)
    body(
        doc,
        "Léxico o código. Subcadena. Barato y honesto. No captura tema. "
        "LLM-as-judge, sin referencia. Rúbrica Mustache sobre el AV. Boolean, score "
        "o categoría, más un campo opcional de razonamiento. Omisión, específico de "
        "NLA. El tema está en el AV y no en la completion. Es el análogo del "
        "awareness verbalizado frente al medido por NLA en [1]. Un evaluador "
        "pairwise (cuál de dos AVs se prefiere) forma parte del diseño y se "
        "implementa como extensión del núcleo.",
    )

    heading(doc, "4. Arquitectura")
    body(
        doc,
        "NLA Eval no entrena NLA. Orquesta APIs. La Figura 1 describe el ciclo de "
        "una fila. El dataset aporta el example. El run produce la completion y las "
        "verbalizaciones en las posiciones elegidas. El evaluador consume input, AV "
        "de entrada, AV de salida y, si hace falta, la completion, y calcula métricas.",
    )
    fig_caption(
        doc,
        "Figura 1. El evaluador compara el ejemplo del dataset con las verbalizaciones NLA del token de entrada y del token de salida.",
    )
    add_table(
        doc,
        ["Bloque", "Rol"],
        [
            ("Example", "Input = prompt del dataset"),
            ("Run", "Modelo + NLA. Output = completion"),
            ("NLA usuario", "Verbalización del último token de contenido"),
            ("NLA asistente", "Verbalización del primer token de respuesta"),
            ("Evaluator", "Métricas sobre AVs (y omisión frente a completion)"),
        ],
    )
    body(
        doc,
        "La Figura 2 muestra el uso que organiza la plataforma. Dos configuraciones "
        "recorren el mismo dataset. Los evaluadores agregan tasas por experimento.",
    )
    fig_caption(
        doc,
        "Figura 2. Varias versiones (modelo, capa, política de tokens) sobre un único dataset. Los evaluadores agregan métricas por experimento.",
    )
    add_table(
        doc,
        ["Versión", "Ejemplo"],
        [
            ("v1", "Llama 3.3 70B Instruct, kitft-l53, último token de usuario"),
            ("v2", "Gemma 3 27B Instruct, kitft-l41, misma política"),
            ("Dataset", "Misma lista de prompts para ambas corridas"),
            ("Evaluadores", "Hit rate, score medio, categoría, MSE medio"),
        ],
    )

    heading(doc, "4.1 Interfaz de entrada y salida", 12)
    body(
        doc,
        "La interfaz es el punto de interacción entre el investigador y NLA Eval. "
        "Por ella ingresan datasets, rúbricas y claves de API hacia un proxy. En "
        "sentido inverso, devuelve filas de experimento, celdas de feedback y "
        "gráficos, de modo que la plataforma apoye el análisis sin pretender que el "
        "AV reemplace el juicio sobre el instrumento.",
    )
    heading(doc, "4.2 Orquestador de experimento", 12)
    body(
        doc,
        "El orquestador coordina el ciclo de cada ejemplo desde su ingreso hasta la "
        "persistencia de la fila. No ejecuta el NLA. Enruta tres pasos. POST de "
        "completion en Neuronpedia, con modelo e identificador de NLA. Selección de "
        "posiciones según la política y POST de explain. Para cada evaluador, un "
        "LLM u operación de código sobre el artefacto. El esquema JSON de salida lo "
        "dictan las claves de feedback.",
    )
    body(
        doc,
        "El orquestador conserva resultados intermedios. Un GET posterior, en otro "
        "proceso, no pierde la corrida. En servidor local el almacén es un JSON. En "
        "despliegue el almacén es compartido. El filesystem efímero de una función "
        "serverless no es un laboratorio.",
    )
    heading(doc, "4.3 Capa NLA", 12)
    body(
        doc,
        "Esta capa es un cliente. No reimplementa el autoencoder. Encapsula rate "
        "limits y el recorte de posiciones. Si explain falla, la fila queda con error "
        "y no se inventa un AV. Las fuentes previstas son Llama 3.3 70B Instruct "
        "con kitft-l53 y Gemma 3 27B Instruct con kitft-l41 como contraste, no como "
        "par equivalente de claim científico.",
    )
    heading(doc, "4.4 Capa juez", 12)
    body(
        doc,
        "Los prompts del juez son plantillas Mustache. El mapeo fija qué variable "
        "es el AV agregado, el AV de último token de usuario, el de primer token de "
        "asistente, el prompt, la completion, el token, el MSE o una referencia "
        "humana. El formato de respuesta (boolean, score con min y max, categorías "
        "con descripción) estructura el JSON. El razonamiento es opcional. El juez "
        "se aplica al AV, no a la respuesta pública, salvo que la rúbrica lo pida "
        "(omisión).",
    )
    heading(doc, "4.5 Capa de comparación", 12)
    body(
        doc,
        "La tabla de un run expone input, referencia, output (el AV) y una columna "
        "por clave de feedback. Boolean se muestra como 1.00 o 0.00 con color. "
        "Score se colorea entre mínimo y máximo. Categórica muestra el nombre. El "
        "encabezado informa el promedio. La comparación de dos experimentos reusa las "
        "mismas claves sobre el mismo dataset. El evaluador pairwise (Figura 3) "
        "opera sobre dos AVs del mismo example.",
    )
    fig_caption(
        doc,
        "Figura 3. Evaluación pairwise. El juez elige entre dos verbalizaciones del mismo example (preferred en 0 o 1).",
    )
    add_table(
        doc,
        ["Paso", "Descripción"],
        [
            ("v1 y v2", "Dos corridas sobre el mismo dataset"),
            ("Par", "AVs del mismo example"),
            ("Juez pairwise", "preferred = 0 o 1, más razonamiento opcional"),
        ],
    )

    heading(doc, "5. Funcionalidades de NLA Eval")
    body(
        doc,
        "NLA Eval se operacionaliza a través de una plataforma web que aplica "
        "política de tokens, evaluación y comparación en un entorno integrado. Su "
        "propuesta central no es almacenar chats, sino curar corridas, puntuar AVs "
        "y contrastar experimentos. Las funcionalidades siguientes cubren el ciclo "
        "completo que el módulo debe ejecutar.",
    )
    heading(doc, "5.1 Laboratorio y onboarding", 12)
    body(
        doc,
        "La pantalla inicial describe el flujo. Claves de API, dataset, evaluador, "
        "corrida, comparación. El investigador ve de entrada qué objeto se puntúa "
        "(el AV) y qué no (la creencia del modelo).",
    )
    heading(doc, "5.2 Datasets", 12)
    body(
        doc,
        "El módulo de datasets concentra la lista de prompts con identificador, "
        "texto y referencia opcional. Permite alta de ejemplos, edición y selección "
        "del conjunto sobre el que se dispara un experimento. Desde aquí se inicia "
        "la corrida y se accede a los runs ya persistidos.",
    )
    heading(doc, "5.3 Evaluadores", 12)
    body(
        doc,
        "El módulo de evaluadores concentra rúbricas. Cada evaluador declara "
        "modelo de juez, plantilla, mapeo de variables y configuración de feedback. "
        "El formato de respuesta admite boolean, score (mínimo, máximo y "
        "descripciones de extremos) y categoría (nombre y descripción, con alta y "
        "baja de categorías). Include reasoning pide una justificación breve junto al "
        "score. Advanced reserva opciones de esquema. El investigador puede definir "
        "un juez de foro, de peligro o de evaluación sin modificar Neuronpedia.",
    )
    heading(doc, "5.4 Motor de corrida", 12)
    body(
        doc,
        "El motor de corrida constituye la capa de ejecución. Elige fuente NLA, "
        "política de tokens y evaluadores, recorre el dataset, persiste cada fila y "
        "muestra el progreso. Si una explicación falla, la fila registra el error. El "
        "motor no reentrena el NLA. Encadena completion, explain y juez.",
    )
    heading(doc, "5.5 Tabla de filas y gráficos", 12)
    body(
        doc,
        "Cada run se presenta como tabla. Columnas de input, referencia, output y "
        "claves de feedback, con celdas coloreadas según cumpla o no, según el score, "
        "o según la categoría. El encabezado informa el promedio de cada clave. El "
        "módulo de comparación agrupa dos o más experimentos del mismo dataset y "
        "produce gráficos de hit rate del juez y de MSE medio, de modo que se vea "
        "de inmediato si una fuente o una política cambia el señalizador interno.",
    )
    heading(doc, "5.6 Flujo pairwise", 12)
    body(
        doc,
        "Una vez materializado el núcleo, cada par de AVs del mismo example accede "
        "a un juez de preferencia. La salida es preferred en 0 o 1 más "
        "razonamiento opcional. Ese flujo cubre el caso en que no basta un score "
        "absoluto y hace falta elegir entre dos verbalizaciones.",
    )

    heading(doc, "6. Diseño de validación")
    body(
        doc,
        "La validación empírica de NLA Eval se plantea en dos niveles "
        "complementarios. A nivel de señal, se prevé un conjunto fijo de prompts "
        "(familia consejo, how-to, enciclopedia, un ítem en español), dos fuentes NLA "
        "(Llama 70B kitft-l53 y Gemma 27B kitft-l41), una política de tokens "
        "congelada, un juez booleano de tema de foro y un evaluador léxico. Las "
        "métricas de interés incluyen hit rate del juez, tasa léxica, tasa de "
        "omisión (AV sí, completion no), MSE medio, y el grado de coincidencia entre "
        "el juez y etiquetado humano sobre una muestra de AVs, en el espíritu del "
        "acuerdo reportado en [1], sin copiar ese número.",
    )
    body(
        doc,
        "A nivel de plataforma, se diseñará un protocolo con investigadores que "
        "permita medir el tiempo para reproducir una comparación que hoy exige "
        "pestañas, la capacidad de un tercero de definir un juez distinto sin tocar "
        "Neuronpedia, y la confianza en las celdas de feedback. Los resultados "
        "permitirán ajustar rúbricas, política de tokens y parámetros del "
        "orquestador.",
    )

    heading(doc, "7. Limitaciones")
    body(
        doc,
        "El marco hereda los límites del instrumento. El NLA se entrena en una capa "
        "fija. El AV es un señalizador. El juez puede sesgarse hacia lexemas o hacia "
        "el propio prompt. Neuronpedia impone cupos. El pairwise y los jueces de "
        "código más allá del léxico quedan como extensión del núcleo. No hay NLA "
        "públicos sobre modelos base, así que no se replica el eje base frente a "
        "SFT de otros estudios de sesgo cultural [5]. Nada de esto autoriza a leer "
        "un AV como pensamiento.",
    )

    heading(doc, "8. Conclusiones y trabajos futuros")
    body(
        doc,
        "Este trabajo presentó NLA Eval, una plataforma para la evaluación de "
        "verbalizaciones NLA que operacionaliza datasets, política de tokens, "
        "evaluadores y comparación de corridas mediante un orquestador sobre la API "
        "de Neuronpedia. El aporte no es un método nuevo de interpretabilidad. Es "
        "convertir la inspección puntual y el grader ocasional de un paper en un "
        "laboratorio reutilizable.",
    )
    body(
        doc,
        "Entre los trabajos futuros se destacan la ejecución del protocolo de la "
        "Sección 6, la implementación plena del flujo pairwise y la persistencia "
        "compartida en despliegue. Neuronpedia fomentó el acceso a NLA. NLA Eval "
        "apunta a fomentar investigaciones que los usen.",
    )

    heading(doc, "9. Referencias de diseño")
    body(
        doc,
        "El recorte de funcionalidades de NLA Eval no parte de una lista ad hoc. Se "
        "tomó como referencia la manera de trabajar de un framework altamente popular "
        "en la evaluación de aplicaciones basadas en LLM, organizado en datasets, "
        "experimentos, evaluadores con claves de feedback y vistas de comparación "
        "entre corridas [3]. Ese modo de trabajo, pensado para salidas de "
        "aplicaciones no deterministas, sirvió para diseñar los módulos de la "
        "plataforma. Dataset, rúbrica, corrida, tabla de filas y gráficos. El objeto "
        "evaluado cambia. No es la respuesta pública del modelo, sino el AV en una "
        "posición de token, con MSE y, cuando corresponde, omisión frente a la "
        "completion. La referencia es de método de laboratorio, no de identidad "
        "de producto.",
    )

    heading(doc, "Agradecimientos", 10)
    add_p(
        doc,
        "[Nombres y apellidos de los docentes tutores. Completar en camera ready.]",
        10,
        space_after=8,
    )

    heading(doc, "Referencias", 10)
    refs = [
        "[1] K. Fraser-Taliente et al., “Natural Language Autoencoders,” Transformer Circuits, may. 2026. https://transformer-circuits.pub/2026/nla/",
        "[2] Neuronpedia, “Natural Language Autoencoders demo and API.” https://www.neuronpedia.org/nla",
        "[3] LangChain, “LangSmith: evaluation and experiment tracking for LLM applications.” https://docs.smith.langchain.com/",
        "[4] P. Kozak Riehme et al., “ARIA: Un Enfoque Inteligente para la Gestión y Mejora de Requerimientos en Entornos Ágiles,” CoNaIISI, 2026.",
        "[5] J. Fernandez de Landa et al., “Why are all LLMs Obsessed with Japanese Culture? On the Hidden Cultural and Regional Biases of LLMs,” Findings of EMNLP, 2026. arXiv:2604.21751.",
        "[6] Anthropic, “Natural Language Autoencoders,” 2026. https://www.anthropic.com/research/natural-language-autoencoders",
        "[7] kitft, “natural_language_autoencoders,” GitHub. https://github.com/kitft/natural_language_autoencoders",
    ]
    for t in refs:
        add_p(doc, t, 10, justify=True, space_after=4)

    heading(doc, "Datos de Contacto", 10)
    add_p(
        doc,
        "Completar en camera ready. Nombre y Apellido. Universidad Tecnológica Nacional, [unidad académica]. Dirección postal. E-mail.",
        10,
        italic=True,
        justify=True,
    )

    doc.save(OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
