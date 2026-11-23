#!/usr/bin/env python3
"""
Compilador de Documento Word (.docx) de Presentación Académica e Informe Técnico:
"Diseño e Integración del Ciclo de Vida de un Sistema con IA - Desktopia Lab 2.0"

Genera FODT con imágenes PNG embebidas en Base64 (<office:binary-data>),
valida el XML y exporta a Microsoft Word (.docx) mediante LibreOffice Writer
garantizando portabilidad 100% autocontenida (todas las imágenes dentro de word/media/).
"""
import base64
import html
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

DIR_SRC = Path(__file__).parent
DIR_MANUAL = DIR_SRC.parent
DIR_OUT = DIR_MANUAL / "Presentacion_Ciclo_de_Vida_IA_Desktopia_Lab.docx"
FODT_PATH = DIR_SRC / "presentacion_documento.fodt"


def embed_img(name: str, img_path: Path, width_mm: str, height_mm: str) -> str:
    if not img_path.exists():
        raise FileNotFoundError(f"No se encontró la imagen requerida: {img_path}")
    b64 = base64.b64encode(img_path.read_bytes()).decode("ascii")
    return (
        f'<text:p text:style-name="CenterP">'
        f'<draw:frame draw:name="{html.escape(name)}" text:anchor-type="as-char" '
        f'svg:width="{width_mm}" svg:height="{height_mm}">'
        f'<draw:image><office:binary-data>{b64}</office:binary-data></draw:image>'
        f'</draw:frame>'
        f'</text:p>'
    )


img_flujo = embed_img("ImgFlujo", DIR_MANUAL / "diagrama_flujo.png", "174mm", "29.0mm")
img_articulacion = embed_img("ImgArticulacion", DIR_SRC / "diagrama_ciclos_articulacion.png", "174mm", "64.3mm")
img_visor = embed_img("ImgVisor", DIR_MANUAL / "diagrama_visor.png", "158mm", "61.1mm")
img_recorte = embed_img("ImgRecorte", DIR_MANUAL / "diagrama_recorte.png", "158mm", "39.5mm")
img_ia = embed_img("ImgIA", DIR_MANUAL / "diagrama_ia.png", "170mm", "52.2mm")
img_mlops_drift = embed_img("ImgMLOpsDrift", DIR_SRC / "diagrama_mlops_drift.png", "174mm", "51.1mm")
img_dlm_eda = embed_img("ImgDLM", DIR_SRC / "diagrama_dlm_eda.png", "174mm", "47.3mm")
img_red = embed_img("ImgRed", DIR_MANUAL / "diagrama_red.png", "168mm", "34.4mm")


fodt_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
                 xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
                 xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
                 xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
                 xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
                 xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
                 xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"
                 xmlns:xlink="http://www.w3.org/1999/xlink"
                 office:version="1.3" office:mimetype="application/vnd.oasis.opendocument.text">
  <office:font-face-decls>
    <style:font-face style:name="Segoe UI" svg:font-family="'Segoe UI', Arial, sans-serif"/>
    <style:font-face style:name="Consolas" svg:font-family="'Consolas', 'Courier New', monospace"/>
  </office:font-face-decls>

  <office:automatic-styles>
    <style:page-layout style:name="PM_A4">
      <style:page-layout-properties fo:page-width="210mm" fo:page-height="297mm"
                                    fo:margin-top="12mm" fo:margin-bottom="12mm"
                                    fo:margin-left="15mm" fo:margin-right="15mm"/>
      <style:header-style>
        <style:header-footer-properties fo:min-height="6mm" fo:margin-bottom="3mm"/>
      </style:header-style>
      <style:footer-style>
        <style:header-footer-properties fo:min-height="6mm" fo:margin-top="3mm" fo:border-top="0.5pt solid #cbd5e1"/>
      </style:footer-style>
    </style:page-layout>

    <style:style style:name="HeaderP" style:family="paragraph">
      <style:text-properties fo:font-size="8pt" fo:font-family="Segoe UI" fo:color="#64748b"/>
      <style:paragraph-properties fo:text-align="end"/>
    </style:style>

    <style:style style:name="FooterP" style:family="paragraph">
      <style:text-properties fo:font-size="8pt" fo:font-family="Segoe UI" fo:color="#64748b"/>
    </style:style>

    <style:style style:name="PageBreak" style:family="paragraph">
      <style:paragraph-properties fo:break-before="page" fo:margin-top="0mm" fo:margin-bottom="1mm"/>
    </style:style>

    <!-- Tipografía Principal -->
    <style:style style:name="TitleMain" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="1mm" fo:margin-bottom="1.5mm"/>
      <style:text-properties fo:font-size="19pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#ffffff"/>
    </style:style>

    <style:style style:name="SubtitleMain" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="2.5mm"/>
      <style:text-properties fo:font-size="10.5pt" fo:font-family="Segoe UI" fo:color="#cbd5e1" fo:font-style="italic"/>
    </style:style>

    <style:style style:name="CoverMeta" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0.5mm" fo:margin-bottom="0.5mm"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-family="Segoe UI" fo:color="#94a3b8"/>
    </style:style>

    <style:style style:name="SectionTitle" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="2.5mm" fo:margin-bottom="2mm" fo:border-bottom="1.5pt solid #0f172a" fo:padding-bottom="1mm" fo:keep-with-next="always"/>
      <style:text-properties fo:font-size="12.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#0f172a"/>
    </style:style>

    <style:style style:name="SubSectionTitle" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="2.5mm" fo:margin-bottom="1mm" fo:keep-with-next="always"/>
      <style:text-properties fo:font-size="10pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#1e40af"/>
    </style:style>

    <style:style style:name="SubSectionPurple" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="2.5mm" fo:margin-bottom="1mm" fo:keep-with-next="always"/>
      <style:text-properties fo:font-size="10pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#6d28d9"/>
    </style:style>

    <style:style style:name="SubSectionGreen" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="2.5mm" fo:margin-bottom="1mm" fo:keep-with-next="always"/>
      <style:text-properties fo:font-size="10pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#065f46"/>
    </style:style>

    <style:style style:name="BodyP" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="1.8mm" fo:line-height="125%"/>
      <style:text-properties fo:font-size="9pt" fo:font-family="Segoe UI" fo:color="#334155"/>
    </style:style>

    <style:style style:name="BodySmall" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="1mm" fo:line-height="118%"/>
      <style:text-properties fo:font-size="8pt" fo:font-family="Segoe UI" fo:color="#475569"/>
    </style:style>

    <style:style style:name="BulletP" style:family="paragraph">
      <style:paragraph-properties fo:margin-left="4mm" fo:margin-top="0.4mm" fo:margin-bottom="1mm" fo:line-height="120%"/>
      <style:text-properties fo:font-size="8.6pt" fo:font-family="Segoe UI" fo:color="#334155"/>
    </style:style>

    <style:style style:name="CaptionP" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0.8mm" fo:margin-bottom="2mm" fo:text-align="center"/>
      <style:text-properties fo:font-size="7.8pt" fo:font-style="italic" fo:font-family="Segoe UI" fo:color="#64748b"/>
    </style:style>

    <style:style style:name="CenterP" style:family="paragraph">
      <style:paragraph-properties fo:text-align="center" fo:margin-top="1mm" fo:margin-bottom="0.5mm" fo:keep-with-next="always"/>
    </style:style>

    <!-- Cajas de Colores -->
    <style:style style:name="BoxTitleGreen" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0.8mm"/>
      <style:text-properties fo:font-size="9.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#065f46"/>
    </style:style>
    <style:style style:name="BoxTextGreen" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0.8mm" fo:line-height="120%"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-family="Segoe UI" fo:color="#047857"/>
    </style:style>

    <style:style style:name="BoxTitleBlue" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0.8mm"/>
      <style:text-properties fo:font-size="9.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#1e40af"/>
    </style:style>
    <style:style style:name="BoxTextBlue" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0.8mm" fo:line-height="120%"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-family="Segoe UI" fo:color="#1e3a8a"/>
    </style:style>

    <style:style style:name="BoxTitlePurple" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0.8mm"/>
      <style:text-properties fo:font-size="9.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#5b21b6"/>
    </style:style>
    <style:style style:name="BoxTextPurple" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0.8mm" fo:line-height="120%"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-family="Segoe UI" fo:color="#4c1d95"/>
    </style:style>

    <style:style style:name="BoxTitleAmber" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0.8mm"/>
      <style:text-properties fo:font-size="9.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#92400e"/>
    </style:style>
    <style:style style:name="BoxTextAmber" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0.8mm" fo:line-height="120%"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-family="Segoe UI" fo:color="#78350f"/>
    </style:style>

    <style:style style:name="BoxTitleRose" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0.8mm"/>
      <style:text-properties fo:font-size="9.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#9f1239"/>
    </style:style>
    <style:style style:name="BoxTextRose" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0.8mm" fo:line-height="120%"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-family="Segoe UI" fo:color="#881337"/>
    </style:style>

    <!-- Tablas y Columnas (ancho total = 180mm) -->
    <style:style style:name="TableWidth100" style:family="table">
      <style:table-properties style:width="180mm" table:align="margins"/>
    </style:style>

    <style:style style:name="Col180" style:family="table-column">
      <style:table-column-properties style:column-width="180mm"/>
    </style:style>
    <style:style style:name="Col90" style:family="table-column">
      <style:table-column-properties style:column-width="90mm"/>
    </style:style>
    <style:style style:name="Col60" style:family="table-column">
      <style:table-column-properties style:column-width="60mm"/>
    </style:style>
    <style:style style:name="Col35" style:family="table-column">
      <style:table-column-properties style:column-width="35mm"/>
    </style:style>
    <style:style style:name="Col45" style:family="table-column">
      <style:table-column-properties style:column-width="45mm"/>
    </style:style>
    <style:style style:name="Col50" style:family="table-column">
      <style:table-column-properties style:column-width="50mm"/>
    </style:style>
    <style:style style:name="Col55" style:family="table-column">
      <style:table-column-properties style:column-width="55mm"/>
    </style:style>
    <style:style style:name="Col65" style:family="table-column">
      <style:table-column-properties style:column-width="65mm"/>
    </style:style>
    <style:style style:name="Col70" style:family="table-column">
      <style:table-column-properties style:column-width="70mm"/>
    </style:style>
    <style:style style:name="Col75" style:family="table-column">
      <style:table-column-properties style:column-width="75mm"/>
    </style:style>
    <style:style style:name="Col80" style:family="table-column">
      <style:table-column-properties style:column-width="80mm"/>
    </style:style>
    <style:style style:name="Col85" style:family="table-column">
      <style:table-column-properties style:column-width="85mm"/>
    </style:style>
    <style:style style:name="Col95" style:family="table-column">
      <style:table-column-properties style:column-width="95mm"/>
    </style:style>
    <style:style style:name="Col100" style:family="table-column">
      <style:table-column-properties style:column-width="100mm"/>
    </style:style>
    <style:style style:name="Col110" style:family="table-column">
      <style:table-column-properties style:column-width="110mm"/>
    </style:style>
    <style:style style:name="Col25" style:family="table-column">
      <style:table-column-properties style:column-width="25mm"/>
    </style:style>
    <style:style style:name="Col20" style:family="table-column">
      <style:table-column-properties style:column-width="20mm"/>
    </style:style>
    <style:style style:name="Col40" style:family="table-column">
      <style:table-column-properties style:column-width="40mm"/>
    </style:style>
    <style:style style:name="Col115" style:family="table-column">
      <style:table-column-properties style:column-width="115mm"/>
    </style:style>
    <style:style style:name="Col120" style:family="table-column">
      <style:table-column-properties style:column-width="120mm"/>
    </style:style>

    <!-- Celdas -->
    <style:style style:name="CellDarkCover" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#0f172a" fo:padding="4.5mm" fo:border="1pt solid #1e293b"/>
    </style:style>
    <style:style style:name="CellAccentGreen" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#ecfdf5" fo:padding="2.8mm" fo:border="1pt solid #10b981"/>
    </style:style>
    <style:style style:name="CellAccentBlue" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#eff6ff" fo:padding="2.8mm" fo:border="1pt solid #3b82f6"/>
    </style:style>
    <style:style style:name="CellAccentPurple" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#f5f3ff" fo:padding="2.8mm" fo:border="1pt solid #8b5cf6"/>
    </style:style>
    <style:style style:name="CellAccentAmber" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#fffbeb" fo:padding="2.8mm" fo:border="1pt solid #f59e0b"/>
    </style:style>
    <style:style style:name="CellAccentRose" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#fff1f2" fo:padding="2.8mm" fo:border="1pt solid #f43f5e"/>
    </style:style>
    <style:style style:name="CellGray" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#f8fafc" fo:padding="2.5mm" fo:border="0.5pt solid #cbd5e1"/>
    </style:style>
    <style:style style:name="CellTableHeader" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#0f172a" fo:padding="2.2mm" fo:border="0.5pt solid #334155"/>
    </style:style>
    <style:style style:name="CellTableRowA" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#ffffff" fo:padding="2mm" fo:border-bottom="0.5pt solid #e2e8f0" fo:border-left="0.5pt solid #e2e8f0" fo:border-right="0.5pt solid #e2e8f0"/>
    </style:style>
    <style:style style:name="CellTableRowB" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#f8fafc" fo:padding="2mm" fo:border-bottom="0.5pt solid #e2e8f0" fo:border-left="0.5pt solid #e2e8f0" fo:border-right="0.5pt solid #e2e8f0"/>
    </style:style>
    <style:style style:name="CellTableRowGreen" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#ecfdf5" fo:padding="2mm" fo:border-bottom="0.5pt solid #10b981" fo:border-left="0.5pt solid #e2e8f0" fo:border-right="0.5pt solid #e2e8f0"/>
    </style:style>

    <!-- Textos en tablas -->
    <style:style style:name="TableHeadP" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0mm"/>
      <style:text-properties fo:font-size="8pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#ffffff"/>
    </style:style>
    <style:style style:name="TableCellP" style:family="paragraph">
      <style:paragraph-properties fo:line-height="118%" fo:margin-top="0mm" fo:margin-bottom="0mm"/>
      <style:text-properties fo:font-size="8pt" fo:font-family="Segoe UI" fo:color="#334155"/>
    </style:style>
    <style:style style:name="TableCellBold" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0.4mm"/>
      <style:text-properties fo:font-size="8pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#0f172a"/>
    </style:style>

    <!-- Spans inline -->
    <style:style style:name="BadgeSpan" style:family="text">
      <style:text-properties fo:font-family="Segoe UI" fo:font-weight="bold" fo:font-size="7.5pt" fo:background-color="#10b981" fo:color="#ffffff"/>
    </style:style>
    <style:style style:name="BadgeBlueSpan" style:family="text">
      <style:text-properties fo:font-family="Segoe UI" fo:font-weight="bold" fo:font-size="7.5pt" fo:background-color="#2563eb" fo:color="#ffffff"/>
    </style:style>
    <style:style style:name="BadgePurpleSpan" style:family="text">
      <style:text-properties fo:font-family="Segoe UI" fo:font-weight="bold" fo:font-size="7.5pt" fo:background-color="#7c3aed" fo:color="#ffffff"/>
    </style:style>
    <style:style style:name="KbdSpan" style:family="text">
      <style:text-properties fo:font-family="Consolas" fo:font-weight="bold" fo:font-size="8pt" fo:background-color="#e2e8f0" fo:color="#0f172a"/>
    </style:style>
    <style:style style:name="Bold" style:family="text">
      <style:text-properties fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="Italic" style:family="text">
      <style:text-properties fo:font-style="italic"/>
    </style:style>
    <style:style style:name="GreenBold" style:family="text">
      <style:text-properties fo:font-weight="bold" fo:color="#047857"/>
    </style:style>
    <style:style style:name="BlueBold" style:family="text">
      <style:text-properties fo:font-weight="bold" fo:color="#1d4ed8"/>
    </style:style>
    <style:style style:name="PurpleBold" style:family="text">
      <style:text-properties fo:font-weight="bold" fo:color="#6d28d9"/>
    </style:style>
    <style:style style:name="RoseBold" style:family="text">
      <style:text-properties fo:font-weight="bold" fo:color="#be123c"/>
    </style:style>
    <style:style style:name="Mono" style:family="text">
      <style:text-properties fo:font-family="Consolas" fo:font-weight="bold" fo:font-size="8pt"/>
    </style:style>
  </office:automatic-styles>

  <office:master-styles>
    <style:master-page style:name="Standard" style:page-layout-name="PM_A4">
      <style:header>
        <text:p text:style-name="HeaderP">INTRODUCCIÓN A LA INTELIGENCIA ARTIFICIAL • DESKTOPIA LAB 2.0 (CORE AI)</text:p>
      </style:header>
      <style:footer>
        <text:p text:style-name="FooterP">Diseño e Integración del Ciclo de Vida de un Sistema con IA • Página <text:page-number/> de <text:page-count/></text:p>
      </style:footer>
    </style:master-page>
  </office:master-styles>

  <office:body>
    <office:text>

      <!-- ======================================================================= -->
      <!-- PÁGINA 1: PORTADA EJECUTIVA Y VISIÓN GENERAL                            -->
      <!-- ======================================================================= -->
      <table:table table:name="PortadaCover" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col180"/>
        <table:table-row>
          <table:table-cell table:style-name="CellDarkCover">
            <text:p text:style-name="CoverMeta"><text:span text:style-name="BadgeSpan"> INTRODUCCIÓN A LA INTELIGENCIA ARTIFICIAL • ACTIVIDAD PRÁCTICA INDIVIDUAL </text:span></text:p>
            <text:p text:style-name="TitleMain">Diseño e Integración del Ciclo de Vida de un Sistema con IA</text:p>
            <text:p text:style-name="SubtitleMain">Caso de Estudio Real Aplicado: Desktopia Lab 2.0 (Core AI) — Estación de Digitalización, Restauración Dual con Inteligencia Artificial y Archivo Histórico en Red NAS</text:p>
            <text:p text:style-name="CoverMeta">Articulación integral: Ciclo Tradicional (SDLC) + Ciclo de IA (MLOps) + Ciclo del Dato (DLM &amp; EDA) + Manual Esquemático del Operador</text:p>
            <text:p text:style-name="CoverMeta">Repositorio: https://github.com/MapikGodoy/lab-fotos-vity • Entregable: Soporte Visual e Informe de Presentación</text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="BodyP"/>

      <table:table table:name="ObjetivoBox" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col180"/>
        <table:table-row>
          <table:table-cell table:style-name="CellAccentGreen">
            <text:p text:style-name="BoxTitleGreen">🎯 Propósito de la Presentación y Sistema Seleccionado</text:p>
            <text:p text:style-name="BoxTextGreen">
              Este documento presenta el diseño arquitectónico y la integración completa de los tres ciclos de vida de un sistema productivo real: <text:span text:style-name="Bold">Desktopia Lab 2.0 (Core AI)</text:span>. Su misión es rescatar álbumes familiares e históricos deteriorados mediante digitalización multicapa, visión por computadora (OpenCV), restauración generativa facial (GFPGAN v1.4), superresolución 4x acelerada por GPU (Real-ESRGAN Vulkan), catalogación histórica con metadatos EXIF y resguardo en servidor NAS privado, operado mediante un <text:span text:style-name="Bold">Manual Esquemático del Operador de 7 páginas</text:span> orientado a jóvenes operadores sin formación informática.
            </text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="SectionTitle">Ficha Técnica de la Arquitectura Implementada</text:p>

      <table:table table:name="FichaGrid" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col60"/>
        <table:table-column table:style-name="Col60"/>
        <table:table-column table:style-name="Col60"/>
        <table:table-row>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold"><text:span text:style-name="BlueBold">1. Sistema Tradicional (SDLC)</text:span></text:p>
            <text:p text:style-name="BodySmall">• Backend FastAPI + Uvicorn (puerto 7777)</text:p>
            <text:p text:style-name="BodySmall">• Interfaz SPA oscura + QR Móvil SVG</text:p>
            <text:p text:style-name="BodySmall">• Lanzador 1-clic &amp; apagado seguro GPU</text:p>
            <text:p text:style-name="BodySmall">• Manual PDF esquemático (7 páginas)</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold"><text:span text:style-name="PurpleBold">2. Módulo de IA (MLOps)</text:span></text:p>
            <text:p text:style-name="BodySmall">• OpenCV: auto-recorte hasta 4 fotos</text:p>
            <text:p text:style-name="BodySmall">• RetinaFace: auto-giro por ojos</text:p>
            <text:p text:style-name="BodySmall">• GFPGAN v1.4 (CPU) + Real-ESRGAN (GPU)</text:p>
            <text:p text:style-name="BodySmall">• Fusión Total + Validación HITL</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold"><text:span text:style-name="GreenBold">3. Datos y Gobernanza (DLM)</text:span></text:p>
            <text:p text:style-name="BodySmall">• Ingesta SANE 300 DPI / JPG / Simulador</text:p>
            <text:p text:style-name="BodySmall">• Inyección EXIF (año real e IA usada)</text:p>
            <text:p text:style-name="BodySmall">• SSH rsync a NAS + Bóveda bkporiginal</text:p>
            <text:p text:style-name="BodySmall">• 100% On-Premise + Purga efímera</text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="BodyP"/>
      {img_flujo}
      <text:p text:style-name="CaptionP">Figura 1 (Manual del Operador): Secuencia operativa completa en 6 pasos desde el lanzador en 1 clic hasta el almacenamiento permanente en el NAS.</text:p>

      <!-- ======================================================================= -->
      <!-- PÁGINA 2: DOMINIO Y USO RIGUROSO DE HERRAMIENTAS DE IA                  -->
      <!-- ======================================================================= -->
      <text:p text:style-name="PageBreak"/>

      <text:p text:style-name="SectionTitle">Indicaciones Generales: Dominio Elegido y Uso de Herramientas de IA</text:p>

      <text:p text:style-name="SubSectionTitle">A. Elección del Dominio: Preservación Patrimonial y Archivo Fotográfico Inteligente</text:p>
      <text:p text:style-name="BodyP">
        El dominio elegido corresponde a la <text:span text:style-name="Bold">gestión operativa de digitalización documental, restauración fotográfica y preservación de archivos históricos/familiares</text:span>. A diferencia de un editor gráfico convencional, el volumen de fotografías físicas en deterioro exige automatizar el recorte múltiple en platina, reconstruir rostros degradados sin distorsionar paisajes, recuperar el año histórico en metadatos EXIF y ofrecer una interfaz lo suficientemente visual e intuitiva como para que jóvenes operadores ("los chicos") puedan operar toda la cadena sin conocimientos técnicos de Linux ni inteligencia artificial.
      </text:p>

      <text:p text:style-name="SubSectionTitle">B. Uso Riguroso y Trazable de Herramientas de IA Asociadas (Criterio de Rúbrica: 25%)</text:p>
      <text:p text:style-name="BodyP">
        Durante todo el ciclo de análisis, diseño, prototipado e implantación del proyecto se emplearon asistentes de IA generativa de forma estructurada y verificable:
      </text:p>

      <table:table table:name="TablaHerramientasIA" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col40"/>
        <table:table-column table:style-name="Col55"/>
        <table:table-column table:style-name="Col85"/>
        <table:table-row>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">HERRAMIENTA IA</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">ROL EN EL PROYECTO</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">APORTE CONCRETO AL DESARROLLO</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Perplexity AI / Search AI</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Investigación de dominio, estado del arte y marco normativo.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Comparativa de modelos de restauración facial (<text:span text:style-name="Mono">GFPGAN v1.4</text:span>) y superresolución GPU AMD RX 580 sin CUDA (<text:span text:style-name="Mono">realesrgan-ncnn-vulkan</text:span> con mesa RADV). Relevamiento de estándares EXIF y <text:span text:style-name="Bold">Ley 25.326</text:span> sobre datos biométricos.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">Gemini / ChatGPT</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Coprocesamiento de requerimientos, historias de usuario y EDA.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Diseño UX para jóvenes operadores (lupa móvil libre en límites, QR, atajos, modo Fusión Total), resolución de bloqueos Vulkan (<text:span text:style-name="Mono">tile=200</text:span>, normalización JPG 1800 px), formulación de preguntas EDA y creación del Manual del Operador.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Generadores de Diagramas y Código</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Diagramación técnica y prototipado de pipelines.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Generación programática de diagramas SVG/PNG a 300 DPI (<text:span text:style-name="Mono">generar_diagramas.py</text:span>), prototipado modular de endpoints FastAPI asíncronos y compilador automatizado de documentación.</text:p></table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="SubSectionTitle">Evidencia de Prompts Clave Empleados y Decisiones Técnicas Derivadas</text:p>

      <table:table table:name="TablaPrompts" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col80"/>
        <table:table-column table:style-name="Col100"/>
        <table:table-row>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">CONSULTA / PROMPT ESTRUCTURADO A LA IA</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">DECISIÓN ARQUITECTÓNICA RESULTANTE EN EL SISTEMA</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP"><text:span text:style-name="Italic">"¿Cómo ejecutar restauración facial y upscaling 4x en una AMD RX 580 bajo Linux evitando cuelgues de Vulkan al 0.00% y sin saturar VRAM con fotos JPG de celular?"</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Separación híbrida CPU (<text:span text:style-name="Mono">GFPGAN v1.4</text:span>) + GPU (<text:span text:style-name="Mono">Vulkan ncnn</text:span> con <text:span text:style-name="Mono">tile=200, threads=1:1:1</text:span>), semáforo <text:span text:style-name="Mono">_gpu_lock</text:span> y normalización LANCZOS a <text:span text:style-name="Mono">MAX_DIM=1800px</text:span>.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP"><text:span text:style-name="Italic">"¿Qué preguntas EDA debemos responder antes de aplicar OpenCV y auto-rotación sobre álbumes mixtos de retratos y paisajes sin introducir giros erróneos?"</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Calibración de <text:span text:style-name="Mono">area_minima=100000</text:span>, limpieza de sombra de tapa (10 px) y auto-rotación condicional basada en 5 landmarks oculares que se inhibe si <text:span text:style-name="Mono">caras == 0</text:span>.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP"><text:span text:style-name="Italic">"¿Cómo diseñar una experiencia de aprobación visual donde jóvenes operadores puedan combinar lo mejor de GFPGAN y Real-ESRGAN o rechazar alucinaciones faciales?"</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Creación de variante <text:span text:style-name="Mono">completa</text:span> (Fusión Total), comparador dividido con lupa 2.2x táctil/mouse, atajos <text:span text:style-name="KbdSpan">A/I/C/0/D</text:span> y registro estadístico por modelo para monitorear drift.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP"><text:span text:style-name="Italic">"¿Cómo distribuir el sistema en GitHub sin subir 600 MB de pesos .pth/.bin ni exponer contraseñas del NAS, y capacitar operadores en minutos?"</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Creación de <text:span text:style-name="Mono">.gitignore</text:span> + <text:span text:style-name="Mono">.env.example</text:span>, script automático <text:span text:style-name="Mono">descargar_modelos.sh</text:span> acoplado al lanzador 1-clic y generación del Manual PDF esquemático.</text:p></table:table-cell>
        </table:table-row>
      </table:table>

      <!-- ======================================================================= -->
      <!-- PÁGINA 3: ARTICULACIÓN SISTÉMICA (COHERENCIA 30%)                       -->
      <!-- ======================================================================= -->
      <text:p text:style-name="PageBreak"/>

      <text:p text:style-name="SectionTitle">Coherencia Sistémica: Articulación SDLC ↔ MLOps ↔ DLM (Rúbrica: 30%)</text:p>
      <text:p text:style-name="BodyP">
        El valor arquitectónico central de Desktopia Lab reside en que los tres ciclos de vida no funcionan de manera aislada: cada evento operativo en la interfaz tradicional (SDLC) dispara una transformación gobernada sobre los datos (DLM) y un punto de control o inferencia sobre los modelos de IA (MLOps).
      </text:p>

      {img_articulacion}
      <text:p text:style-name="CaptionP">Figura 2: Matriz de articulación sistémica entre el Ciclo de Vida del Software (SDLC), el Ciclo de Vida de IA (MLOps) y el Ciclo de Vida del Dato (DLM).</text:p>

      <table:table table:name="TablaArticulacion" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col40"/>
        <table:table-column table:style-name="Col45"/>
        <table:table-column table:style-name="Col45"/>
        <table:table-column table:style-name="Col50"/>
        <table:table-row>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">PUNTO DE ENCUENTRO</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">ROL DEL SDLC</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">ROL DE MLOPS (IA)</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">ROL DEL DLM (DATO)</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">1. Apertura e Ingesta</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Formulario Lote, QR móvil (<text:span text:style-name="Mono">/api/qr.svg</text:span>), driver SANE.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Detección de contornos y rectificación (<text:span text:style-name="Mono">OpenCV</text:span>).</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Captura cruda + contexto histórico; purga inmediata de platina.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">2. Inferencia Dual</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Endpoint asíncrono con locks de concurrencia y estado F5.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Auto-giro ojos + GFPGAN + Vulkan 4x + Fusión Total.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Normalización 1800 px, 4 variantes en <text:span text:style-name="Mono">sesion_activa/</text:span>.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">3. Revisión Humana</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Visor comparador, lupa 2.2x, rotación y modal recorte.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Evaluación HITL: filtra alucinaciones eligiendo variante óptima.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Descarte de versiones no elegidas y backups temporales.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellBold">4. Envío y Cierre</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellP">Dashboard estadístico, botón <text:span text:style-name="Mono">Cerrar Álbum</text:span> y <text:span text:style-name="Mono">Apagar</text:span>.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellP">KPIs de aceptación por modelo para detectar Drift.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellP">Inyección EXIF + SSH rsync a NAS + purga total local.</text:p></table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="BodyP"/>
      <table:table table:name="BoxValorSist" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col180"/>
        <table:table-row>
          <table:table-cell table:style-name="CellAccentBlue">
            <text:p text:style-name="BoxTitleBlue">💡 Clave de la Integración Sistémica</text:p>
            <text:p text:style-name="BoxTextBlue">
              El software tradicional no es un mero contenedor pasivo de la IA: actúa como <text:span text:style-name="Bold">árbitro de concurrencia hardware</text:span> (locks GPU/CPU), <text:span text:style-name="Bold">plataforma de auditoría humana</text:span> (visor comparador HITL del Manual) y <text:span text:style-name="Bold">recolector silencioso de telemetría MLOps/DLM</text:span> (registro histórico de qué modelo aceptan los operadores).
            </text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <!-- ======================================================================= -->
      <!-- PÁGINA 4: PARTE I — CICLO DE VIDA TRADICIONAL (SDLC)                    -->
      <!-- ======================================================================= -->
      <text:p text:style-name="PageBreak"/>

      <text:p text:style-name="SectionTitle">Parte I: Ciclo de Vida del Sistema Tradicional (SDLC)</text:p>

      <text:p text:style-name="SubSectionTitle">1.1 Planificación y Requerimientos (Diagnóstico del Problema)</text:p>
      <text:p text:style-name="BodyP">
        El problema operativo a resolver es la <text:span text:style-name="Bold">digitalización masiva y preservación de archivos fotográficos físicos antiguos</text:span> que sufren degradación química y pérdida de contexto cronológico. Los flujos tradicionales (escanear con drivers de sistema + abrir Photoshop + renombrar manualmente carpetas + copiar al servidor) resultan lentos, propensos a error humano y prohibitivos para operadores jóvenes sin capacitación técnica.
      </text:p>

      <table:table table:name="TablaReq" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col25"/>
        <table:table-column table:style-name="Col55"/>
        <table:table-column table:style-name="Col100"/>
        <table:table-row>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">ID</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">REQUERIMIENTO</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">MATERIALIZACIÓN EN DESKTOPIA LAB + MANUAL</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">RF-01</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Arranque y apagado en 1 clic</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Script <text:span text:style-name="Mono">iniciar_desktopia.sh</text:span> + acceso directo; botón rojo <text:span text:style-name="Bold">Apagar</text:span> (<text:span text:style-name="Mono">/api/apagar-servidor</text:span>) que libera puerto 7777 y VRAM.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">RF-02</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Gestión de lotes e historia</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Apertura obligatoria con <text:span text:style-name="Bold">Operador</text:span>, <text:span text:style-name="Bold">Nombre del Álbum</text:span> y <text:span text:style-name="Bold">Año Histórico</text:span>; envío parcial o cierre completo.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">RF-03</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Captura multivía y Móvil QR</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Escáner Xerox SANE (1-4 fotos en platina), carga directa PC/celular (<text:span text:style-name="Mono">/api/cargar-fotos</text:span>), Simulador y control remoto QR.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">RF-04</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Mesa visual, recorte y rotación</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Slider divisor, Lupa 2.2x draggable, rotación 90° sincronizada en 4 capas y recorte (<text:span text:style-name="Italic">Aplicar</text:span> + Deshacer / <text:span text:style-name="Italic">Extraer nueva</text:span>).</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">RNF-01</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Resiliencia ante F5 y offline</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Persistencia en <text:span text:style-name="Mono">session_meta.json</text:span> y <text:span text:style-name="Mono">aprobadas.json</text:span>; ejecución 100% en LAN local sin dependencia de internet en operación.</text:p></table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="SubSectionTitle">1.2 Análisis y Diseño: Módulos, Roles e Integración Visual del Manual</text:p>
      <text:p text:style-name="BodyP">
        El sistema sigue una arquitectura modular en 3 capas sobre <text:span text:style-name="Mono">FastAPI + Python 3.11+</text:span>: <text:span text:style-name="Bold">Frontend SPA responsivo</text:span> (<text:span text:style-name="Mono">static/</text:span>), <text:span text:style-name="Bold">API Routers</text:span> (<text:span text:style-name="Mono">scanning, photos, processing, sessions</text:span>) y <text:span text:style-name="Bold">Capa de Servicios</text:span> (<text:span text:style-name="Mono">ImageProcessor, AIService, ScannerService</text:span>). Se definen dos roles claros: <text:span text:style-name="Bold">Operador de Laboratorio</text:span> (ejecuta todo el flujo mediante el Manual PDF y la Mesa de Control) y <text:span text:style-name="Bold">Administrador Técnico</text:span> (gestiona hardware SANE, credenciales <text:span text:style-name="Mono">.env</text:span> y servidor NAS).
      </text:p>

      {img_visor}
      <text:p text:style-name="CaptionP">Figura 3 (Manual del Operador, pág. 4): Mesa de Control y Visor Comparador donde el software tradicional expone los 4 resultados del ciclo de IA.</text:p>

      <!-- ======================================================================= -->
      <!-- PÁGINA 5: SDLC CONTINUACIÓN — RECORTE E IMPLANTACIÓN                    -->
      <!-- ======================================================================= -->
      <text:p text:style-name="PageBreak"/>

      <text:p text:style-name="SubSectionTitle">Puntos de Integración UI ↔ IA y Herramienta de Recorte</text:p>
      <text:p text:style-name="BodyP">
        Un ejemplo sobresaliente de diseño SDLC acoplado a IA es la <text:span text:style-name="Bold">Herramienta de Recorte y Encuadre</text:span> (Manual, pág. 5). Frente al problema real de fotografías pegadas en álbumes que OpenCV capturaba como una sola unidad, el sistema tradicional provee guías de composición, cruz central táctil/mouse y dos acciones diferenciadas:
      </text:p>

      {img_recorte}
      <text:p text:style-name="CaptionP">Figura 4 (Manual del Operador, pág. 5): Modal de Recorte con sincronización geométrica multivisión y extracción independiente hacia el motor de IA.</text:p>

      <table:table table:name="TablaRecorte" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col90"/>
        <table:table-column table:style-name="Col90"/>
        <table:table-row>
          <table:table-cell table:style-name="CellAccentGreen">
            <text:p text:style-name="BoxTitleGreen">Opción 1: Aplicar Recorte (Sincronizado)</text:p>
            <text:p text:style-name="BoxTextGreen">Recorta proporcionalmente en porcentaje (<text:span text:style-name="Mono">_porcentaje_a_pixeles</text:span>) las 4 variantes (<text:span text:style-name="Mono">original, caras, ia, completa</text:span>) conservando respaldo para el botón <text:span text:style-name="Bold">Deshacer</text:span>.</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="CellAccentBlue">
            <text:p text:style-name="BoxTitleBlue">Opción 2: Extraer como Foto Nueva</text:p>
            <text:p text:style-name="BoxTextBlue">Cuando dos fotos salieron juntas en la platina, genera un nuevo archivo <text:span text:style-name="Mono">_original.png</text:span> independiente y dispara desde cero el pipeline Dual Engine de IA sin borrar la foto previa.</text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="SubSectionTitle">1.3 Metodología de Desarrollo, Implantación y Puesta en Marcha</text:p>
      <text:p text:style-name="BulletP">• <text:span text:style-name="Bold">Metodología Ágil Iterativa (Kanban / Sprints cortos):</text:span> El desarrollo evolucionó en ciclos incrementales guiados directamente por pruebas operativas reales con operadores jóvenes: (1) persistencia en disco tras recarga F5, (2) inclusión de variante híbrida "Completa Rostros + 4x", (3) sincronización de rotación en las 4 capas, (4) diseño SaaS oscuro profesional con acceso QR móvil responsivo, (5) normalización de JPGs de celular, lupa panable dentro del visor y botón de apagado limpio.</text:p>
      <text:p text:style-name="BulletP">• <text:span text:style-name="Bold">Estrategia de Despliegue y Portabilidad (GitHub):</text:span> El proyecto se versiona en <text:span text:style-name="Mono">github.com/MapikGodoy/lab-fotos-vity</text:span> (~4.7 MB) excluyendo pesos pesados (&gt;100 MB) y secretos (<text:span text:style-name="Mono">.env</text:span>). En cualquier estación Linux nueva, <text:span text:style-name="Mono">./instalar.sh</text:span> o el primer arranque con <text:span text:style-name="Mono">./iniciar_desktopia.sh</text:span> ejecuta <text:span text:style-name="Mono">descargar_modelos.sh</text:span> para bajar automáticamente los pesos de IA.</text:p>
      <text:p text:style-name="BulletP">• <text:span text:style-name="Bold">Compatibilidad Multi-Escáner:</text:span> Aunque opera con Xerox Phaser 3100MFP vía SANE (<text:span text:style-name="Mono">/usr/sbin/scanimage</text:span>), el patrón de dispositivo es parametrizable en <text:span text:style-name="Mono">.env</text:span> (<text:span text:style-name="Mono">SCANNER_DEVICE_PATTERN</text:span>), admite <text:span text:style-name="Mono">sane-airscan</text:span> y opera al 100% con cualquier escáner externo vía carga directa (<text:span text:style-name="Bold">Importar</text:span>).</text:p>

      <!-- ======================================================================= -->
      <!-- PÁGINA 6: PARTE II — CICLO DE VIDA DE LA IA (MLOPS)                     -->
      <!-- ======================================================================= -->
      <text:p text:style-name="PageBreak"/>

      <text:p text:style-name="SectionTitle">Parte II: Ciclo de Vida del Sistema de IA (MLOps)</text:p>

      <text:p text:style-name="SubSectionPurple">2.1 Definición del Problema Inteligente y Matriz de KPIs</text:p>
      <text:p text:style-name="BodyP">
        El problema de Visión por Computadora consiste en ejecutar <text:span text:style-name="Bold">restauración ciega híbrida</text:span> (corrección de geometría de platina, detección de orientación anatómica facial, reconstrucción de rostros degradados y superresolución 4x de fondos) sobre imágenes heterogéneas en hardware de consumo (CPU + GPU AMD Radeon RX 580 de 8 GB VRAM vía Vulkan), evitando alucinaciones faciales en paisajes.
      </text:p>

      <table:table table:name="TablaKPIs" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col35"/>
        <table:table-column table:style-name="Col65"/>
        <table:table-column table:style-name="Col80"/>
        <table:table-row>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">TIPO KPI</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">MÉTRICA / INDICADOR</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">OBJETIVO Y MEDICIÓN EN EL SISTEMA</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold"><text:span text:style-name="PurpleBold">Técnico</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Tasa de Éxito de Inferencia</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">&gt; 98% sin timeout (&lt; 300s) verificando <text:span text:style-name="Mono">exito_ia / exito_completa</text:span> y archivo &gt; 1 KB.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold"><text:span text:style-name="PurpleBold">Técnico</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Precisión Auto-Orientación sin Falsos Giros</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">0% rotación errónea en paisajes (<text:span text:style-name="Mono">caras == 0</text:span>); umbral interocular <text:span text:style-name="Mono">&gt;= 5 px</text:span>.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold"><text:span text:style-name="PurpleBold">Técnico</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Consistencia Geométrica Multicapa</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">100% coincidencia vertical/horizontal entre <text:span text:style-name="Mono">original, caras, ia, completa</text:span>.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellBold"><text:span text:style-name="GreenBold">Negocio (HITL)</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellP">Tasa de Aceptación por Variante IA</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellP">Calculada en <text:span text:style-name="Mono">/api/estadisticas</text:span>: <text:span text:style-name="Mono">% Completa</text:span> (meta &gt;75%), <text:span text:style-name="Mono">% Solo 4x</text:span>, <text:span text:style-name="Mono">% Rostros</text:span>, <text:span text:style-name="Mono">% Original</text:span>.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold"><text:span text:style-name="GreenBold">Negocio</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Rendimiento Operativo por Lote</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Hasta 4 fotos por escaneo simultáneo; trazabilidad de fotos y álbumes por operador.</text:p></table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="SubSectionPurple">2.2 Modelado, Enfoque Algorítmico Dual Engine y Estrategia de Validación</text:p>
      {img_ia}
      <text:p text:style-name="CaptionP">Figura 5 (Manual del Operador, pág. 3): Pipeline paralelo entre GFPGAN v1.4 (CPU) y Real-ESRGAN Vulkan 4x (GPU RX 580) convergiendo en Fusión Total.</text:p>

      <table:table table:name="TablaModelos" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col45"/>
        <table:table-column table:style-name="Col50"/>
        <table:table-column table:style-name="Col85"/>
        <table:table-row>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">COMPONENTE IA</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">ALGORITMO / MODELO</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">FUNCIÓN Y CONFIGURACIÓN DE VALIDACIÓN</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">1. Segmentación Platina</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">OpenCV Visión Clásica</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP"><text:span text:style-name="Mono">GaussianBlur(5,5)</text:span> + <text:span text:style-name="Mono">Threshold(220)</text:span> + <text:span text:style-name="Mono">minAreaRect</text:span> + <text:span text:style-name="Mono">warpPerspective</text:span>. Fallback a imagen completa si no detecta contornos.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">2. Auto-Giro Anatómico</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">RetinaFace ResNet50 (5 landmarks)</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Calcula vector <text:span text:style-name="Mono">(dx, dy)</text:span> entre centro de ojos y boca por votación mayoritaria en 0°/90°/270°. Respeta paisajes (<text:span text:style-name="Mono">caras == 0</text:span>).</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">3. Restauración Facial</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">GFPGAN v1.4 + ParseNet (CPU)</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">GAN pre-entrenada (<text:span text:style-name="Mono">arch="clean", channel_multiplier=2</text:span>) a escala 1x sin competir con la VRAM de la GPU.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">4. Superresolución 4x</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Real-ESRGAN x4plus Vulkan</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Binario C++/ncnn en GPU RX 580 (<text:span text:style-name="Mono">tile=200, threads=1:1:1</text:span>). Si <text:span text:style-name="Mono">caras &gt; 0</text:span>, escala <text:span text:style-name="Mono">_caras.png</text:span> para producir <text:span text:style-name="Mono">_completa.png</text:span>.</text:p></table:table-cell>
        </table:table-row>
      </table:table>

      <!-- ======================================================================= -->
      <!-- PÁGINA 7: MLOPS — DESPLIEGUE, MONITOREO Y CONTROL DE DRIFT              -->
      <!-- ======================================================================= -->
      <text:p text:style-name="PageBreak"/>

      <text:p text:style-name="SubSectionPurple">2.3 Despliegue (Deployment) y Control de Robustez</text:p>
      <text:p text:style-name="BodyP">
        El módulo inteligente está encapsulado en <text:span text:style-name="Mono">AIService</text:span> y expuesto vía API REST (<text:span text:style-name="Mono">POST /api/procesar-ia/{{base}}</text:span>). Para evitar bloqueos del event loop de FastAPI, la inferencia corre en hilos secundarios (<text:span text:style-name="Mono">asyncio.to_thread</text:span>) serializados con bloqueos <text:span text:style-name="Mono">_gpu_lock</text:span> y <text:span text:style-name="Mono">_gfpgan_lock</text:span>. La robustez ante entradas imprevistas o falsos positivos se garantiza mediante cuatro barreras: (1) reescalado LANCZOS previo a <text:span text:style-name="Mono">MAX_DIM=1800px</text:span> para fotos móviles de alta resolución, (2) verificación de integridad de archivo (&gt;1 KB) con fallback determinístico de <text:span text:style-name="Mono">_completa</text:span> a <text:span text:style-name="Mono">_ia</text:span>, (3) recuperación manual mediante botón amarillo <text:span text:style-name="Bold">Reintentar</text:span>, y (4) filtro <text:span text:style-name="Bold">Human-in-the-Loop</text:span> en el comparador visual.
      </text:p>

      {img_mlops_drift}
      <text:p text:style-name="CaptionP">Figura 6: Arquitectura MLOps completa con guardas de entrada, serving serializado, evaluación humana (HITL) y lazo de detección de Drift.</text:p>

      <text:p text:style-name="SubSectionPurple">2.4 Monitoreo Continuo, Detección de Drift y Estrategia de Actualización</text:p>

      <table:table table:name="TablaDrift" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col40"/>
        <table:table-column table:style-name="Col70"/>
        <table:table-column table:style-name="Col70"/>
        <table:table-row>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">FENÓMENO</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">SEÑALES DE DETECCIÓN EN EL SISTEMA</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">ACCIÓN CORRECTIVA / REENTRENAMIENTO</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Data Drift (Cambio en entradas)</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">• Paso de escaneos PNG 300 DPI a fotos JPG sacadas con celular (etiquetas EXIF de giro, 4000+ px).<text:span text:style-name="Bold"> </text:span>• Errores o timeouts Vulkan en <text:span text:style-name="Mono">desktopia.log</text:span>.<text:span text:style-name="Bold"> </text:span>• Fotos pegadas sin margen blanco.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Normalización automática (<text:span text:style-name="Mono">exif_transpose</text:span> + LANCZOS 1800 px), recalibración de umbral OpenCV y opción manual <text:span text:style-name="Bold">Extraer como foto nueva</text:span>.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">Concept Drift (Pérdida de calidad percibida)</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">• Caída del KPI <text:span text:style-name="Mono">% Aprobadas Completa</text:span> y aumento de <text:span text:style-name="Mono">% Solo 4x</text:span> o <text:span text:style-name="Mono">% Original</text:span> en <text:span text:style-name="Mono">/api/estadisticas</text:span> ante álbumes sepia, negativos o ilustraciones.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP"><text:span text:style-name="Bold">Model Swapping modular</text:span> vía <text:span text:style-name="Mono">.env</text:span> (<text:span text:style-name="Mono">VULKAN_MODEL</text:span>: <text:span text:style-name="Mono">realesrgan-x4plus-anime</text:span>, <text:span text:style-name="Mono">animevideov3</text:span>) o sustitución de pesos faciales (<text:span text:style-name="Mono">CodeFormer</text:span> / nuevo checkpoint GFPGAN) sin tocar la interfaz de usuario.</text:p></table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="BodyP"/>
      <table:table table:name="BoxMLOpsNote" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col180"/>
        <table:table-row>
          <table:table-cell table:style-name="CellAccentPurple">
            <text:p text:style-name="BoxTitlePurple">📈 Trazabilidad del Feedback Humano para Futura Calibración</text:p>
            <text:p text:style-name="BoxTextPurple">
              Cada cierre de lote guarda en <text:span text:style-name="Mono">registro_operadores.json</text:span> exactamente cuántas fotos eligió el humano con <text:span text:style-name="Bold">Completa, Solo 4x, Rostros u Original</text:span>. Este historial actúa como sensor cuantitativo continuo de desempeño real sobre los archivos históricos del dominio.
            </text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <!-- ======================================================================= -->
      <!-- PÁGINA 8: PARTE III — CICLO DE VIDA DEL DATO (DLM) Y EDA                -->
      <!-- ======================================================================= -->
      <text:p text:style-name="PageBreak"/>

      <text:p text:style-name="SectionTitle">Parte III: Ciclo de Vida del Dato (DLM) y Análisis Exploratorio (EDA)</text:p>

      <text:p text:style-name="SubSectionGreen">3.1 Fases Continuas del Dato (De la Captura a la Destrucción Segura)</text:p>
      {img_dlm_eda}
      <text:p text:style-name="CaptionP">Figura 7: Mapeo continuo DLM desde la captura física/digital hasta el archivo permanente cifrado y purga local de datos sensibles.</text:p>

      <text:p text:style-name="BulletP">1. <text:span text:style-name="Bold">Captura / Creación:</text:span> Digitalización SANE 300 DPI PNG (<text:span text:style-name="Mono">platina_*.png</text:span>), importación JPG/PNG/WEBP/TIFF móvil o modo Simulador, vinculada a los atributos del lote (<text:span text:style-name="Mono">operador, nombre_lote, fecha_historica</text:span>).</text:p>
      <text:p text:style-name="BulletP">2. <text:span text:style-name="Bold">Procesamiento / Normalización y Anonimización:</text:span> Recorte OpenCV (<text:span text:style-name="Mono">_original.png</text:span>), rotación EXIF, escalado LANCZOS a 1800 px (<text:span text:style-name="Mono">.temp_input.jpg</text:span>), generación de variantes sin almacenar vectores biométricos en BD (solo RAM) y respaldos (<text:span text:style-name="Mono">.backup.png</text:span>).</text:p>
      <text:p text:style-name="BulletP">3. <text:span text:style-name="Bold">Almacenamiento Temporal, Uso y Enriquecimiento EXIF:</text:span> Reside en <text:span text:style-name="Mono">sesion_activa/</text:span> con estado JSON persistente. Al aprobar, <text:span text:style-name="Mono">exiftool</text:span> inyecta <text:span text:style-name="Mono">DateTimeOriginal</text:span> (año histórico), <text:span text:style-name="Mono">CreateDate</text:span>, <text:span text:style-name="Mono">ImageDescription</text:span> y <text:span text:style-name="Mono">Software</text:span> (trazabilidad del modelo).</text:p>
      <text:p text:style-name="BulletP">4. <text:span text:style-name="Bold">Archivado Permanente y Bóveda Local:</text:span> Transferencia cifrada <text:span text:style-name="Mono">sshpass + rsync</text:span> hacia el NAS (<text:span text:style-name="Mono">192.168.1.80</text:span>, ruta <text:span text:style-name="Mono">.../Fotos_escaneadas/[Nombre_Lote]_[Año]/</text:span>) y resguardo simultáneo de la toma original (recortada/rotada con EXIF) en la bóveda local <text:span text:style-name="Mono">bkporiginal/[Nombre_Lote]_[Año]/</text:span>.</text:p>
      <text:p text:style-name="BulletP">5. <text:span text:style-name="Bold">Destrucción Segura / Purga Efímera:</text:span> Borrado inmediato de platina cruda y <text:span text:style-name="Mono">.temp_input.jpg</text:span>; eliminación de variantes no aprobadas y backups tras envío (<text:span text:style-name="Mono">_limpiar_base</text:span>); purga total al cerrar lote conservando intactos el NAS y la bóveda <text:span text:style-name="Mono">bkporiginal/</text:span>.</text:p>

      {img_red}
      <text:p text:style-name="CaptionP">Figura 8 (Manual del Operador, pág. 6): Topología física de transferencia segura hacia la nueva ruta UUID en el servidor NAS.</text:p>

      <!-- ======================================================================= -->
      <!-- PÁGINA 9: EDA, MATRIZ DE ATRIBUTOS Y GOBERNANZA ÉTICA / PII             -->
      <!-- ======================================================================= -->
      <text:p text:style-name="PageBreak"/>

      <text:p text:style-name="SubSectionGreen">3.2 Análisis Exploratorio de Datos (EDA) — Preguntas Esenciales y Matriz de Atributos</text:p>
      <text:p text:style-name="BodyP">
        Refinado mediante asistentes conversacionales (Gemini), el EDA formuló 5 preguntas críticas sobre las imágenes reales antes de consolidar el pipeline: (1) <text:span text:style-name="Bold">¿Cuál es la distribución de resoluciones entre escaneos 300 DPI y cámaras de celular?</text:span> → originó <text:span text:style-name="Mono">umbral_bypass=1400</text:span> y el tope <text:span text:style-name="Mono">MAX_DIM=1800</text:span>; (2) <text:span text:style-name="Bold">¿Qué variabilidad de brillo produce sombras falsas en la tapa del escáner?</text:span> → limpieza de bordes de 10 px y <text:span text:style-name="Mono">threshold=220</text:span>; (3) <text:span text:style-name="Bold">¿Cómo tratar valores atípicos (fotos truncadas, pegadas o EXIF invertido)?</text:span> → flags <text:span text:style-name="Mono">LOAD_TRUNCATED_IMAGES</text:span>, <text:span text:style-name="Mono">exif_transpose</text:span> y herramienta <text:span text:style-name="Italic">Extraer como foto nueva</text:span>; (4) <text:span text:style-name="Bold">¿Qué proporción presenta rostros diminutos o nulos?</text:span> → filtro interocular &gt;= 5 px; (5) <text:span text:style-name="Bold">¿Qué atributos predicen rechazo de la IA?</text:span> → seguimiento de tasas por variante.
      </text:p>

      <table:table table:name="TablaAtributosEDA" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col40"/>
        <table:table-column table:style-name="Col40"/>
        <table:table-column table:style-name="Col50"/>
        <table:table-column table:style-name="Col50"/>
        <table:table-row>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">ATRIBUTO / DATO</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">ORIGEN / TIPO</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">LIMPIEZA Y PREPROCESO</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">RETENCIÓN / POLÍTICA</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Platina Escaneada</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">PNG RGB 300 DPI</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Blur + Threshold 220 + purga bordes 10 px.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Efímera: se borra al instante tras recorte.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">Foto Importada Móvil</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">JPG/WEBP/TIFF + EXIF</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Transposición EXIF + LANCZOS máx. 1800 px.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Temporal en sesión hasta envío al NAS.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Landmarks Faciales</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Coordenadas (ojos/boca)</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Filtro distancia ocular &gt;= 5 px; descarte si caras=0.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Solo en RAM durante inferencia (no se persiste PII).</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">Contexto Histórico</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Operador, Álbum, Año</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Sanitizado espacios (<text:span text:style-name="Mono">_</text:span>) y formato año EXIF.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Permanente en EXIF del NAS y en JSON métricas.</text:p></table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="SubSectionGreen">3.3 Gobernanza, Ética, Protección PII y Plan de Pilotaje (Rúbrica: 20%)</text:p>

      <table:table table:name="TablaEtica" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col90"/>
        <table:table-column table:style-name="Col90"/>
        <table:table-row>
          <table:table-cell table:style-name="CellAccentRose">
            <text:p text:style-name="BoxTitleRose">🛡️ Privacidad PII, Biometría y Sesgos Algorítmicos</text:p>
            <text:p text:style-name="BoxTextRose">• <text:span text:style-name="Bold">Privacidad por Diseño (Ley 25.326):</text:span> Las fotos contienen datos personales y rasgos biométricos familiares/menores. Todo el procesamiento corre <text:span text:style-name="Bold">100% On-Premise</text:span> sin enviar imágenes a APIs externas en la nube. Secretos NAS protegidos en <text:span text:style-name="Mono">.env</text:span> fuera de Git.</text:p>
            <text:p text:style-name="BoxTextRose">• <text:span text:style-name="Bold">Mitigación de Sesgos:</text:span> GFPGAN puede introducir suavizado artificial o alterar rasgos faciales de adultos mayores o etnias poco representadas. Se mitiga mediante <text:span text:style-name="Bold">revisión humana obligatoria</text:span>, disponibilidad permanente de <text:span text:style-name="Bold">Solo 4x / Original</text:span> y registro transparente de qué IA modificó el archivo en <text:span text:style-name="Mono">EXIF:Software</text:span>.</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="CellAccentAmber">
            <text:p text:style-name="BoxTitleAmber">🚀 Gestión del Cambio y Plan de Pilotaje en 3 Fases</text:p>
            <text:p text:style-name="BoxTextAmber">• <text:span text:style-name="Bold">Fase 1 (Capacitación sin riesgo):</text:span> Lectura del <text:span text:style-name="Italic">Manual Esquemático del Operador (7 págs.)</text:span> y práctica libre con el botón <text:span text:style-name="Bold">Simulador</text:span> (<text:span text:style-name="Mono">prueba.png</text:span>) aprendiendo atajos <text:span text:style-name="KbdSpan">A/I/C/0/D</text:span>.</text:p>
            <text:p text:style-name="BoxTextAmber">• <text:span text:style-name="Bold">Fase 2 (Piloto asistido):</text:span> Digitalización de álbumes de prueba usando lanzador 1-clic y operación táctil con <text:span text:style-name="Bold">QR Móvil</text:span> frente al escáner.</text:p>
            <text:p text:style-name="BoxTextAmber">• <text:span text:style-name="Bold">Fase 3 (Producción continua):</text:span> Seguimiento de métricas de calidad y ranking de operadores en Estadísticas para reducir resistencia al cambio.</text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <!-- ======================================================================= -->
      <!-- PÁGINA 10: SÍNTESIS DEL MANUAL, MATRIZ DE ENTREGABLES Y GUION ORAL      -->
      <!-- ======================================================================= -->
      <text:p text:style-name="PageBreak"/>

      <text:p text:style-name="SectionTitle">Anexo Operativo del Manual, Matriz de Entregables y Guion de Presentación</text:p>

      <text:p text:style-name="SubSectionTitle">4. Guía de Decisiones y Protocolos del Manual del Operador (Págs. 5–7 del Manual)</text:p>
      <table:table table:name="TablaManual" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col40"/>
        <table:table-column table:style-name="Col20"/>
        <table:table-column table:style-name="Col120"/>
        <table:table-row>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">DECISIÓN / BOTÓN</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">TECLA</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">CRITERIO OPERATIVO Y CONTROL DE CALIDAD HUMANO (HITL)</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellBold"><text:span text:style-name="GreenBold">Aprobar Total ★</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellBold"><text:span text:style-name="KbdSpan"> A </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellP">Recomendado (~90% casos): fotos con personas donde GFPGAN mejoró rostros y Real-ESRGAN dio nitidez 4x.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Solo 4x (IA)</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold"><text:span text:style-name="KbdSpan"> I </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Paisajes, vehículos, arquitectura o retratos donde la restauración facial alteró identidad natural.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">Facial (Caras) / Original</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold"><text:span text:style-name="KbdSpan"> C </text:span> / <text:span text:style-name="KbdSpan"> 0 </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP"><text:span text:style-name="Bold">[C]</text:span> Conserva grano original mejorado facialmente a 1x; <text:span text:style-name="Bold">[0]</text:span> Resguarda archivo fiel sin intervención IA.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold"><text:span text:style-name="RoseBold">Descartar / Apagar</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold"><text:span text:style-name="KbdSpan"> D </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP"><text:span text:style-name="Bold">[D]</text:span> Purga inmediata de duplicadas o movidas. Al terminar: botón rojo <text:span text:style-name="Bold">Apagar</text:span> para liberar GPU RX 580.</text:p></table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="SubSectionTitle">5. Matriz de Entregables (Punto 4 de la Consigna) Aplicada al Sistema</text:p>
      <table:table table:name="TablaMatrizConsigna" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col40"/>
        <table:table-column table:style-name="Col90"/>
        <table:table-column table:style-name="Col50"/>
        <table:table-row>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">DIMENSIÓN</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">CONTENIDO APLICADO EN DESKTOPIA LAB 2.0</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">HERRAMIENTA IA USADA</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Dominio y Requerimientos</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Diagnóstico de preservación histórica, hardware AMD sin CUDA, arquitectura FastAPI + Manual PDF 7 págs.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Perplexity AI (Benchmark GFPGAN/Vulkan y Ley 25.326)</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">Estructura y Flujo (Modelado a Monitoreo)</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Diagramas Dual Engine, guardas 1800 px, validación HITL y detección de Data/Concept Drift vía <text:span text:style-name="Mono">/estadisticas</text:span>.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Gemini / ChatGPT + Inkscape SVG programático</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Gestión del Dato (DLM &amp; EDA)</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Matriz de atributos, 5 preguntas EDA, EXIF <text:span text:style-name="Mono">exiftool</text:span>, <text:span text:style-name="Mono">rsync</text:span> NAS y purga automática local.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Prompts estructurados EDA + asistencia de código</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">Ética e Implantación</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Biometría 100% On-Premise, trazabilidad EXIF de IA, lanzador 1-clic, QR móvil y pilotaje por fases.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Asistentes conversacionales y Manual de Operador</text:p></table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="SubSectionTitle">6. Guion Recomendado para la Exposición Oral (10–12 minutos)</text:p>
      <text:p text:style-name="BulletP">• <text:span text:style-name="Bold">Min 0–2 (Dominio + Uso de IA Generativa - 25%):</text:span> Presentar el problema real de digitalización de archivos familiares/históricos y mostrar la tabla de cómo Perplexity, Gemini e Inkscape definieron el stack RX 580 + manual operativo.</text:p>
      <text:p text:style-name="BulletP">• <text:span text:style-name="Bold">Min 2–5 (Coherencia Sistémica + SDLC - 30%):</text:span> Apoyarse en la <text:span text:style-name="Italic">Figura 2</text:span> para explicar cómo la UI tradicional (Mesa de Control, QR, Recorte) se conecta con los modelos y el NAS, sin exigir conocimientos técnicos a los chicos.</text:p>
      <text:p text:style-name="BulletP">• <text:span text:style-name="Bold">Min 5–8 (MLOps + Drift - 25%):</text:span> Mostrar las <text:span text:style-name="Italic">Figuras 5 y 6</text:span>: explicar OpenCV, auto-giro condicional (paisajes = 0 giros), Dual Engine (CPU + GPU), filtro HITL y cómo la caída de <text:span text:style-name="Mono">% Completa</text:span> dispara la detección de Drift.</text:p>
      <text:p text:style-name="BulletP">• <text:span text:style-name="Bold">Min 8–11 (DLM, EDA, Ética y Cierre - 20%):</text:span> Mostrar las <text:span text:style-name="Italic">Figuras 7 y 8</text:span>: trazabilidad EXIF, privacidad biométrica local (Ley 25.326), purga automática y el plan de pilotaje con el Manual PDF de 7 páginas.</text:p>

    </office:text>
  </office:body>
</office:document>
'''

FODT_PATH.write_text(fodt_content, encoding="utf-8")
print("Validando XML con ElementTree...")
ET.fromstring(fodt_content)
print("✅ XML 100% válido!")

print("Compilando .fodt a Microsoft Word (.docx) con LibreOffice...")
cmd = [
    "libreoffice",
    "-env:UserInstallation=file:///tmp/lo_presentacion",
    "--headless",
    "--convert-to", "docx",
    "--outdir", str(DIR_MANUAL),
    str(FODT_PATH),
]
subprocess.run(cmd, check=True)

docx_generated = DIR_MANUAL / "presentacion_documento.docx"
if docx_generated.exists():
    if DIR_OUT.exists():
        DIR_OUT.unlink()
    docx_generated.rename(DIR_OUT)
    print(f"✅ Word generado con éxito en: {DIR_OUT} ({DIR_OUT.stat().st_size / 1024:.1f} KB)")
else:
    raise FileNotFoundError("No se generó presentacion_documento.docx")
