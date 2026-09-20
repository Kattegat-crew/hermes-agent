#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convierte un informe markdown a .docx con membrete NeuralCrew.

Uso:
    python3 md2docx.py <entrada.md> <salida.docx>

Soporta: #/##/### headings, tablas markdown (cabecera + separador '|---|---|'),
listas -/1., negritas (**texto**), bloques de código ```, hr (---), párrafos.
Requiere: python-docx (pip install python-docx).
"""
import re
import sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

AZUL = RGBColor(0x1F, 0x3B, 0x6E)
GRIS = RGBColor(0x55, 0x55, 0x55)


def add_membrete(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("NEURALCREW LABS")
    r.bold = True
    r.font.size = Pt(22)
    r.font.color.rgb = AZUL
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("División IA de Digital Expressions · Agentes especializados Hermes")
    r2.italic = True
    r2.font.color.rgb = GRIS
    r2.font.size = Pt(10)
    doc.add_paragraph()


def render_table(doc, lines):
    rows = []
    for ln in lines:
        ln = ln.strip().strip("|")
        rows.append([c.strip() for c in ln.split("|")])
    if not rows:
        return
    ncol = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=ncol)
    table.style = "Light Grid Accent 1"
    for i, r in enumerate(rows):
        for j in range(ncol):
            cell = table.cell(i, j)
            cell.text = r[j] if j < len(r) else ""
            for par in cell.paragraphs:
                for run in par.runs:
                    run.font.size = Pt(8.5)
                    if i == 0:
                        run.bold = True


def convert(src, out):
    doc = Document()
    add_membrete(doc)
    lines = open(src, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            cp = doc.add_paragraph()
            cr = cp.add_run("\n".join(buf))
            cr.font.name = "Consolas"
            cr.font.size = Pt(8)
            cr.font.color.rgb = GRIS
            continue
        # tabla: linea header + linea separador |---|---|
        if ln.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:\-|]+\|?$", lines[i + 1].strip()):
            j = i + 2
            body = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                body.append(lines[j])
                j += 1
            render_table(doc, [ln] + body)
            i = j
            continue
        if ln.startswith("### "):
            doc.add_heading(ln[4:], level=3)
        elif ln.startswith("## "):
            doc.add_heading(ln[3:], level=2)
        elif ln.startswith("# "):
            doc.add_heading(ln[2:], level=1)
        elif re.match(r"\s*[-*] (.+)", ln):
            doc.add_paragraph(re.sub(r"\*\*(.+?)\*\*", r"\1", ln), style="List Bullet")
        elif re.match(r"^\s*\d+\.\s+(.+)$", ln):
            doc.add_paragraph(re.sub(r"\*\*(.+?)\*\*", r"\1", ln), style="List Number")
        elif re.match(r"^\s*-{3,}\s*$", ln) or not ln.strip():
            pass
        else:
            p = doc.add_paragraph(re.sub(r"\*\*(.+?)\*\*", r"\1", ln))
            for run in p.runs:
                run.font.size = Pt(10.5)
        i += 1
    doc.save(out)
    print("OK ->", out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 md2docx.py <entrada.md> <salida.docx>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])