"""Construye documentos Word con el formato de la plantilla del curso (portada TEC, encabezado ATI)."""
import copy
import re

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor

import os
PLANTILLA = os.environ.get("PLANTILLA_CURSO", "/home/claude/ref2/pc4.docx")  # plantilla del curso (no se incluye en el repositorio)
ANCHO_UTIL = 10772  # dxa, A4 con márgenes de 1 cm


def _rpr(bold=False, size=22, italic=False, highlight=None):
    rpr = OxmlElement("w:rPr")
    f = OxmlElement("w:rFonts")
    for a in ("w:ascii", "w:hAnsi", "w:cs"):
        f.set(qn(a), "Arial")
    rpr.append(f)
    if bold:
        rpr.append(OxmlElement("w:b"))
    if italic:
        rpr.append(OxmlElement("w:i"))
    c = OxmlElement("w:color")
    c.set(qn("w:val"), "000000")
    rpr.append(c)
    if highlight:
        h = OxmlElement("w:highlight")
        h.set(qn("w:val"), highlight)
        rpr.append(h)
    s = OxmlElement("w:sz")
    s.set(qn("w:val"), str(size))
    rpr.append(s)
    s2 = OxmlElement("w:szCs")
    s2.set(qn("w:val"), str(size))
    rpr.append(s2)
    return rpr


def _run(texto, **kw):
    r = OxmlElement("w:r")
    r.append(_rpr(**kw))
    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = texto
    r.append(t)
    return r


def _segmentos(texto):
    """Interpreta **negrita** y [[pendiente]] (resaltado amarillo)."""
    partes = re.split(r"(\*\*.+?\*\*|\[\[.+?\]\])", texto)
    for p in partes:
        if not p:
            continue
        if p.startswith("**"):
            yield p[2:-2], {"bold": True}
        elif p.startswith("[["):
            yield p[2:-2], {"highlight": "yellow"}
        else:
            yield p, {}


class Documento:
    def __init__(self, titulo_trabajo, subtitulo, integrantes, fecha_entrega):
        self.doc = docx.Document(PLANTILLA)
        self.body = self.doc.element.body
        hijos = list(self.body.iterchildren())
        # Se conserva la portada (hasta "II Semestre 2026") y la sección final
        for el in hijos[35:]:
            if el.tag != qn("w:sectPr"):
                self.body.remove(el)
        hijos = list(self.body.iterchildren())
        self._texto(hijos[24], titulo_trabajo)
        self._texto(hijos[25], subtitulo)
        self._texto(hijos[31], f"Fecha de entrega: {fecha_entrega}")
        base = hijos[29]
        self._texto(base, integrantes[0])
        anterior = base
        for nombre in integrantes[1:]:
            nuevo = copy.deepcopy(base)
            self._texto(nuevo, nombre)
            anterior.addnext(nuevo)
            anterior = nuevo
        self.sectPr = self.body.find(qn("w:sectPr"))
        self.n_tabla = 0
        self.n_figura = 0

    @staticmethod
    def _texto(p, texto):
        runs = p.findall(qn("w:r"))
        rpr = copy.deepcopy(runs[0].find(qn("w:rPr"))) if runs else None
        if rpr is not None:
            for h in rpr.findall(qn("w:highlight")):
                rpr.remove(h)
        for r in runs:
            p.remove(r)
        for el in p.findall(qn("w:proofErr")):
            p.remove(el)
        for seg, kw in _segmentos(texto):
            r = OxmlElement("w:r")
            if rpr is not None:
                rp = copy.deepcopy(rpr)
                if kw.get("highlight"):
                    h = OxmlElement("w:highlight")
                    h.set(qn("w:val"), "yellow")
                    sz = rp.find(qn("w:sz"))
                    (sz.addprevious(h) if sz is not None else rp.append(h))
                r.append(rp)
            t = OxmlElement("w:t")
            t.set(qn("xml:space"), "preserve")
            t.text = seg
            r.append(t)
            p.append(r)

    def _p(self, estilo=None, jc=None, antes=0, despues=160, linea=360, sangria=None, salto=False, keep=False):
        p = OxmlElement("w:p")
        ppr = OxmlElement("w:pPr")
        if estilo:
            ps = OxmlElement("w:pStyle")
            ps.set(qn("w:val"), estilo)
            ppr.append(ps)
        if keep:
            ppr.append(OxmlElement("w:keepNext"))
        if salto:
            ppr.append(OxmlElement("w:pageBreakBefore"))
        sp = OxmlElement("w:spacing")
        sp.set(qn("w:before"), str(antes))
        sp.set(qn("w:after"), str(despues))
        sp.set(qn("w:line"), str(linea))
        sp.set(qn("w:lineRule"), "auto")
        ppr.append(sp)
        if sangria is not None:
            ind = OxmlElement("w:ind")
            ind.set(qn("w:firstLine"), str(sangria))
            ppr.append(ind)
        if jc:
            j = OxmlElement("w:jc")
            j.set(qn("w:val"), jc)
            ppr.append(j)
        p.append(ppr)
        self.sectPr.addprevious(p)
        return p

    # ------------------------------------------------------------------
    def h1(self, texto, salto=True):
        p = self._p("Ttulo1", jc="center", despues=120, salto=salto, keep=True)
        p.append(_run(texto, bold=True, size=24))

    def h2(self, texto):
        p = self._p("Ttulo2", antes=200, despues=100, keep=True)
        p.append(_run(texto, bold=True, size=22))

    def parrafo(self, texto, sangria=True, size=22, jc="both", despues=160, linea=360, antes=0):
        p = self._p("NormalWeb", jc=jc, antes=antes, despues=despues, linea=linea, sangria=360 if sangria else None)
        for seg, kw in _segmentos(texto):
            p.append(_run(seg, size=size, **kw))
        return p

    def nota(self, texto, size=18):
        p = self._p(jc="center", despues=160, linea=240)
        for seg, kw in _segmentos(texto):
            kw.setdefault("italic", True)
            p.append(_run(seg, size=size, **kw))

    def leyenda(self, texto, tipo="Tabla"):
        if tipo == "Tabla":
            self.n_tabla += 1
            n = self.n_tabla
        else:
            self.n_figura += 1
            n = self.n_figura
        p = self._p(jc="left", antes=80, despues=60, linea=240, keep=True)
        p.append(_run(f"{tipo} {n}. ", bold=True, size=20))
        p.append(_run(texto, size=20))

    def imagen(self, ruta, ancho_cm):
        p = self._p(jc="center", despues=120, linea=240)
        par = docx.text.paragraph.Paragraph(p, self.doc._body)
        par.add_run().add_picture(ruta, width=Cm(ancho_cm))

    def salto_pagina(self):
        p = self._p(despues=0)
        r = OxmlElement("w:r")
        br = OxmlElement("w:br")
        br.set(qn("w:type"), "page")
        r.append(br)
        p.append(r)

    # ------------------------------------------------------------------
    def tabla(self, encabezados, filas, anchos, size=20, negrita_col1=False):
        total = sum(anchos)
        anchos = [round(a * ANCHO_UTIL / total) for a in anchos]
        t = self.doc.add_table(rows=len(filas) + 1, cols=len(encabezados))
        t.style = self.doc.styles["Table Grid"]
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl = t._tbl
        self.sectPr.addprevious(tbl)
        self._fijar(t, anchos)
        for i, fila in enumerate([encabezados] + filas):
            tr = t.rows[i]._tr
            trpr = tr.get_or_add_trPr()
            trpr.append(OxmlElement("w:cantSplit"))
            if i == 0:
                trpr.append(OxmlElement("w:tblHeader"))
            for j, valor in enumerate(fila):
                celda = t.cell(i, j)
                if i == 0:
                    self._sombra(celda, "D9D9D9")
                self._llenar(celda, valor, size=size, bold=(i == 0) or (negrita_col1 and j == 0))
        return t

    def _fijar(self, t, anchos):
        tbl = t._tbl
        tblpr = tbl.tblPr
        lay = OxmlElement("w:tblLayout")
        lay.set(qn("w:type"), "fixed")
        tblpr.append(lay)
        w = tblpr.find(qn("w:tblW"))
        if w is None:
            w = OxmlElement("w:tblW")
            tblpr.append(w)
        w.set(qn("w:w"), str(sum(anchos)))
        w.set(qn("w:type"), "dxa")
        grid = tbl.tblGrid
        for g, a in zip(grid.findall(qn("w:gridCol")), anchos):
            g.set(qn("w:w"), str(a))
        for fila in t.rows:
            for c, a in zip(fila.cells, anchos):
                tcpr = c._tc.get_or_add_tcPr()
                tw = tcpr.find(qn("w:tcW"))
                if tw is None:
                    tw = OxmlElement("w:tcW")
                    tcpr.insert(0, tw)
                tw.set(qn("w:w"), str(a))
                tw.set(qn("w:type"), "dxa")

    @staticmethod
    def _sombra(celda, color):
        tcpr = celda._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), color)
        tcpr.append(shd)

    def _llenar(self, celda, valor, size=20, bold=False):
        lineas = valor if isinstance(valor, list) else [valor]
        tc = celda._tc
        for p in tc.findall(qn("w:p")):
            tc.remove(p)
        for k, linea in enumerate(lineas):
            p = OxmlElement("w:p")
            ppr = OxmlElement("w:pPr")
            sp = OxmlElement("w:spacing")
            sp.set(qn("w:before"), "0")
            sp.set(qn("w:after"), "40" if k < len(lineas) - 1 else "20")
            sp.set(qn("w:line"), "252")
            sp.set(qn("w:lineRule"), "auto")
            ppr.append(sp)
            p.append(ppr)
            for seg, kw in _segmentos(str(linea)):
                kw.setdefault("bold", bold)
                p.append(_run(seg, size=size, **kw))
            tc.append(p)

    def guardar(self, ruta):
        """Guarda quitando imágenes de la plantilla que ya no se usan en el documento."""
        self.doc.core_properties.title = ""
        parte = self.doc.part
        xml = self.body.xml
        usados = set(re.findall(r'r:(?:embed|id|link)="([^"]+)"', xml))
        for rid, rel in list(parte.rels.items()):
            if "image" in rel.reltype and rid not in usados:
                del parte.rels[rid]
        self.doc.save(ruta)
