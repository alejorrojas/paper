# Cómo armar un .docx con el formato estudiantil CoNaIISI

Plantilla oficial: **Formato Papers Estudiantes** (`Formato_Estudiantes`). En este repo hay una copia en `research/reddit_japan_pilot/Formato_Estudiantes.docx`. En Drive, carpeta Conaiisi 2026, el Doc y el `.doc` de la plantilla.

El envío tiene que ser **Word**. Google Docs tira las dos columnas. No editar el paper final ahí.

## Qué pide la plantilla

1. **A4**, retrato.
2. Márgenes **2,5 cm** en los cuatro lados.
3. **Times New Roman**.
4. **Sin números de página** (`pgNumType` = none).
5. Bloque de título a **una columna**. Desde **Abstract** en adelante, **dos columnas iguales**.
6. Versión ciega para evaluación. Autores vacíos. Se completan en camera ready.

Medidas que calzan con el export de la plantilla (twips):

| Cosa | Valor |
|---|---|
| Ancho de página | 11907 |
| Alto de página | 16840 |
| Margen 2,5 cm | 1418 |
| Cada columna | 4252 |
| Gutter entre columnas | 567 (1 cm) |

En python-docx eso es `Twips(...)`. No uses “dos columnas” del menú de Word sobre todo el documento. El título queda aplastado.

## Orden de bloques

**Sección 0 (una columna)**

- Título, 16 pt, negrita, centrado.
- Subtítulo, 16 pt, negrita, centrado.
- Línea de autores o un párrafo en blanco (ciego).
- Universidad, 12 pt, negrita + itálica, centrado.
- Nota de versión ciega, 10 pt, itálica, justificada.

**Sección 1 (continua, dos columnas)**

- Abstract, 10 pt, itálica, justificado.
- Palabras clave, 10 pt.
- Introducción y el resto del cuerpo, 12 pt, justificado.
- Subsecciones tipo 2.1 a 12 pt, negrita.
- Tablas centradas, encabezado sombreado `#E8E8E8`, 9–10 pt.
- Agradecimientos, Referencias, Datos de contacto a 10 pt.

Espaciado que usamos: interlineado 1.0. Cuerpo `space_after` 6 pt. Títulos `space_before` 10 pt.

El salto de sección es **continuo** (`WD_SECTION.CONTINUOUS`). Si es “página siguiente”, el Abstract arranca en la hoja 2.

## Cómo lo generamos acá

El paper vivo se construye con:

```bash
/tmp/docxenv/bin/python research/reddit_japan_pilot/build_conaiisi_docx.py
```

Sale `research/reddit_japan_pilot/conaiisi_2026_reddit_nla.docx`. Copia de trabajo en el Escritorio: `Reddit_como_fuente_de_verdad_IA.docx`.

El script (`build_conaiisi_docx.py`) hace esto:

1. `Document()` vacío.
2. `set_title_block_section` en `sections[0]`.
3. Párrafos del título.
4. `doc.add_section(WD_SECTION.CONTINUOUS)` y `set_two_equal_columns`.
5. Abstract y cuerpo con helpers `heading` / `body`.

Dependencia: `python-docx`. El venv del lab está en `/tmp/docxenv`. Si no está:

```bash
python3 -m venv /tmp/docxenv
/tmp/docxenv/bin/pip install python-docx
```

## Si lo armás a mano en Word

1. Abrí la plantilla, no un documento en blanco “parecido”.
2. Pegá el título en el bloque de una columna.
3. No toques el salto de sección que precede al Abstract.
4. Cuerpo justificado, TNR, 12 pt.
5. Guardá como `.docx`.
6. Revisá en **vista de impresión** que Abstract ya va en dos columnas y el título no.

Si Word te pregunta convertir a Doc de Google, no.

## Columnas en python-docx

La API de alto nivel no deja dos anchos fijos bien. Hay que escribir el XML:

```python
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Twips

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
section._sectPr.append(cols)
```

Antes, borrá `w:cols` y `w:pgNumType` viejos del `sectPr`.

## Qué no hacer

- Subir el paper a Drive **como Google Doc**. Se pierde el formato. Subí el `.docx` y dejaló como archivo.
- Poner autores en la copia de evaluación.
- Inventar márgenes “un poco menos” para que entre. Si no entra, recortá texto.
- Mezclar Arial o Calibri.

## Checklist antes de enviar

- [ ] A4, 2,5 cm, TNR.
- [ ] Título a una columna. Abstract en dos.
- [ ] Sin número de página.
- [ ] Ciego.
- [ ] Archivo `.docx` abierto en Word o LibreOffice, no en Docs.
- [ ] Impresión: las dos columnas llegan al pie sin saltar el título.
