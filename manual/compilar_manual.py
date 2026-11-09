import os
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

DIR_MANUAL = Path("/home/mapik/lab-fotos-vity/manual")

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
                                    fo:margin-top="10mm" fo:margin-bottom="10mm"
                                    fo:margin-left="15mm" fo:margin-right="15mm"/>
      <style:header-style>
        <style:header-footer-properties fo:min-height="6mm" fo:margin-bottom="4mm"/>
      </style:header-style>
      <style:footer-style>
        <style:header-footer-properties fo:min-height="6mm" fo:margin-top="4mm" fo:border-top="0.5pt solid #cbd5e1"/>
      </style:footer-style>
    </style:page-layout>

    <style:style style:name="HeaderP" style:family="paragraph">
      <style:text-properties fo:font-size="8pt" fo:font-family="Segoe UI" fo:color="#94a3b8"/>
      <style:paragraph-properties fo:text-align="end"/>
    </style:style>

    <style:style style:name="FooterP" style:family="paragraph">
      <style:text-properties fo:font-size="8pt" fo:font-family="Segoe UI" fo:color="#64748b"/>
    </style:style>

    <!-- Saltos de página -->
    <style:style style:name="PageBreak" style:family="paragraph">
      <style:paragraph-properties fo:break-before="page" fo:margin-top="0mm" fo:margin-bottom="2mm"/>
    </style:style>

    <!-- Tipografía de Párrafos -->
    <style:style style:name="TitleMain" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="1mm"/>
      <style:text-properties fo:font-size="20pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#ffffff"/>
    </style:style>

    <style:style style:name="SubtitleMain" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="3mm"/>
      <style:text-properties fo:font-size="10.5pt" fo:font-family="Segoe UI" fo:color="#94a3b8" fo:font-style="italic"/>
    </style:style>

    <style:style style:name="CoverMeta" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0mm"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-family="Segoe UI" fo:color="#cbd5e1"/>
    </style:style>

    <style:style style:name="SectionTitle" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="3mm" fo:margin-bottom="2mm" fo:border-bottom="1.5pt solid #0f172a" fo:padding-bottom="1mm"/>
      <style:text-properties fo:font-size="12.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#0f172a"/>
    </style:style>

    <style:style style:name="BodyP" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="2mm" fo:line-height="130%"/>
      <style:text-properties fo:font-size="9pt" fo:font-family="Segoe UI" fo:color="#334155"/>
    </style:style>

    <style:style style:name="BodySmall" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="1mm" fo:line-height="120%"/>
      <style:text-properties fo:font-size="8pt" fo:font-family="Segoe UI" fo:color="#475569"/>
    </style:style>

    <style:style style:name="BulletP" style:family="paragraph">
      <style:paragraph-properties fo:margin-left="4mm" fo:margin-top="0.5mm" fo:margin-bottom="1mm" fo:line-height="120%"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-family="Segoe UI" fo:color="#334155"/>
    </style:style>

    <style:style style:name="CaptionP" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="1mm" fo:margin-bottom="2mm" fo:text-align="center"/>
      <style:text-properties fo:font-size="7.5pt" fo:font-style="italic" fo:font-family="Segoe UI" fo:color="#64748b"/>
    </style:style>

    <style:style style:name="CenterP" style:family="paragraph">
      <style:paragraph-properties fo:text-align="center" fo:margin-top="1mm" fo:margin-bottom="1mm"/>
    </style:style>

    <!-- Párrafos dentro de cajas -->
    <style:style style:name="BoxTitleGreen" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="1mm"/>
      <style:text-properties fo:font-size="9.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#065f46"/>
    </style:style>

    <style:style style:name="BoxTextGreen" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="1mm" fo:line-height="125%"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-family="Segoe UI" fo:color="#047857"/>
    </style:style>

    <style:style style:name="BoxTitleBlue" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="1mm"/>
      <style:text-properties fo:font-size="9.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#0369a1"/>
    </style:style>

    <style:style style:name="BoxTextBlue" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="1mm" fo:line-height="125%"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-family="Segoe UI" fo:color="#0c4a6e"/>
    </style:style>

    <style:style style:name="BoxTitleIndigo" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="1mm"/>
      <style:text-properties fo:font-size="9.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#4338ca"/>
    </style:style>

    <style:style style:name="BoxTextIndigo" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="1mm" fo:line-height="125%"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-family="Segoe UI" fo:color="#3730a3"/>
    </style:style>

    <style:style style:name="BoxTitleRose" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="1mm"/>
      <style:text-properties fo:font-size="9.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#9f1239"/>
    </style:style>

    <style:style style:name="BoxTextRose" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="1mm" fo:line-height="125%"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-family="Segoe UI" fo:color="#881337"/>
    </style:style>

    <style:style style:name="BoxTitleDark" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="1mm"/>
      <style:text-properties fo:font-size="9.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#0f172a"/>
    </style:style>

    <!-- Tablas y Celdas de estilo -->
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
    <style:style style:name="ColAtajo1" style:family="table-column">
      <style:table-column-properties style:column-width="25mm"/>
    </style:style>
    <style:style style:name="ColAtajo2" style:family="table-column">
      <style:table-column-properties style:column-width="50mm"/>
    </style:style>
    <style:style style:name="ColAtajo3" style:family="table-column">
      <style:table-column-properties style:column-width="105mm"/>
    </style:style>
    <style:style style:name="ColAprob1" style:family="table-column">
      <style:table-column-properties style:column-width="45mm"/>
    </style:style>
    <style:style style:name="ColAprob2" style:family="table-column">
      <style:table-column-properties style:column-width="20mm"/>
    </style:style>
    <style:style style:name="ColAprob3" style:family="table-column">
      <style:table-column-properties style:column-width="115mm"/>
    </style:style>
    <style:style style:name="ColMet1" style:family="table-column">
      <style:table-column-properties style:column-width="45mm"/>
    </style:style>
    <style:style style:name="ColMet2" style:family="table-column">
      <style:table-column-properties style:column-width="65mm"/>
    </style:style>
    <style:style style:name="ColMet3" style:family="table-column">
      <style:table-column-properties style:column-width="70mm"/>
    </style:style>

    <!-- Celdas -->
    <style:style style:name="CellDarkCover" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#0f172a" fo:padding="4mm" fo:border="1pt solid #1e293b"/>
    </style:style>

    <style:style style:name="CellAccentGreen" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#ecfdf5" fo:padding="3mm" fo:border="1pt solid #10b981"/>
    </style:style>

    <style:style style:name="CellAccentBlue" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#f0f9ff" fo:padding="3mm" fo:border="1pt solid #0284c7"/>
    </style:style>

    <style:style style:name="CellAccentIndigo" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#eef2ff" fo:padding="3mm" fo:border="1pt solid #6366f1"/>
    </style:style>

    <style:style style:name="CellAccentRose" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#fff1f2" fo:padding="3mm" fo:border="1pt solid #f43f5e"/>
    </style:style>

    <style:style style:name="CellGray" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#f8fafc" fo:padding="3mm" fo:border="0.5pt solid #cbd5e1"/>
    </style:style>

    <style:style style:name="CellTableHeader" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#0f172a" fo:padding="2.5mm" fo:border="0.5pt solid #334155"/>
    </style:style>

    <style:style style:name="CellTableRowA" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#ffffff" fo:padding="2mm" fo:border-bottom="0.5pt solid #e2e8f0"/>
    </style:style>

    <style:style style:name="CellTableRowB" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#f8fafc" fo:padding="2mm" fo:border-bottom="0.5pt solid #e2e8f0"/>
    </style:style>

    <style:style style:name="CellTableRowGreen" style:family="table-cell">
      <style:table-cell-properties fo:background-color="#ecfdf5" fo:padding="2mm" fo:border-bottom="0.5pt solid #10b981"/>
    </style:style>

    <!-- Textos en tablas -->
    <style:style style:name="TableHeadP" style:family="paragraph">
      <style:text-properties fo:font-size="8.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#ffffff"/>
    </style:style>

    <style:style style:name="TableCellP" style:family="paragraph">
      <style:paragraph-properties fo:line-height="120%" fo:margin-top="0mm" fo:margin-bottom="0mm"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-family="Segoe UI" fo:color="#334155"/>
    </style:style>

    <style:style style:name="TableCellBold" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0mm" fo:margin-bottom="0mm"/>
      <style:text-properties fo:font-size="8.5pt" fo:font-weight="bold" fo:font-family="Segoe UI" fo:color="#0f172a"/>
    </style:style>

    <!-- Spans inline -->
    <style:style style:name="BadgeSpan" style:family="text">
      <style:text-properties fo:font-family="Segoe UI" fo:font-weight="bold" fo:font-size="8pt" fo:background-color="#10b981" fo:color="#ffffff"/>
    </style:style>

    <style:style style:name="KbdSpan" style:family="text">
      <style:text-properties fo:font-family="Consolas" fo:font-weight="bold" fo:font-size="8pt" fo:background-color="#e2e8f0" fo:color="#0f172a"/>
    </style:style>

    <style:style style:name="Bold" style:family="text">
      <style:text-properties fo:font-weight="bold"/>
    </style:style>

    <style:style style:name="GreenBold" style:family="text">
      <style:text-properties fo:font-weight="bold" fo:color="#047857"/>
    </style:style>

    <style:style style:name="Mono" style:family="text">
      <style:text-properties fo:font-family="Consolas" fo:font-weight="bold"/>
    </style:style>

    <style:style style:name="MonoGreen" style:family="text">
      <style:text-properties fo:font-family="Consolas" fo:font-weight="bold" fo:color="#047857"/>
    </style:style>

    <style:style style:name="MonoBlue" style:family="text">
      <style:text-properties fo:font-family="Consolas" fo:font-weight="bold" fo:color="#0284c7"/>
    </style:style>

    <style:style style:name="MonoIndigo" style:family="text">
      <style:text-properties fo:font-family="Consolas" fo:font-weight="bold" fo:color="#4f46e5"/>
    </style:style>

    <style:style style:name="MonoRose" style:family="text">
      <style:text-properties fo:font-family="Consolas" fo:font-weight="bold" fo:color="#be123c"/>
    </style:style>
  </office:automatic-styles>

  <office:master-styles>
    <style:master-page style:name="Standard" style:page-layout-name="PM_A4">
      <style:header>
        <text:p text:style-name="HeaderP">DESKTOPIA LAB 2.0 • MANUAL DEL OPERADOR DE LABORATORIO</text:p>
      </style:header>
      <style:footer>
        <text:p text:style-name="FooterP">Estación de Digitalización e Inteligencia Artificial • Página <text:page-number/> de <text:page-count/></text:p>
      </style:footer>
    </style:master-page>
  </office:master-styles>

  <office:body>
    <office:text>

      <!-- ========================================================= -->
      <!-- PÁGINA 1: PORTADA & FLUJO GENERAL                         -->
      <!-- ========================================================= -->
      <table:table table:name="CoverBox" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col180"/>
        <table:table-row>
          <table:table-cell table:style-name="CellDarkCover">
            <text:p text:style-name="CoverMeta"><text:span text:style-name="BadgeSpan"> VERSIÓN 2.0 DUAL ENGINE IA </text:span></text:p>
            <text:p text:style-name="TitleMain">Desktopia Lab (Core AI)</text:p>
            <text:p text:style-name="SubtitleMain">Manual Esquemático para el Operador de Laboratorio Fotográfico</text:p>
            <text:p text:style-name="CoverMeta">Dirigido al equipo de operadores • Flujo: Escaneo → OpenCV → Dual IA (GPU + CPU) → EXIF → NAS</text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="BodyP"/>

      <table:table table:name="BoxMision" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col180"/>
        <table:table-row>
          <table:table-cell table:style-name="CellAccentGreen">
            <text:p text:style-name="BoxTitleGreen">🎯 ¿Cuál es la misión de este laboratorio?</text:p>
            <text:p text:style-name="BoxTextGreen">
              Nuestra misión es <text:span text:style-name="Bold">rescatar y preservar álbumes familiares e históricos</text:span>. Mediante este sistema, una fotografía antigua dañada o borrosa se digitaliza, se restaura facialmente con redes neuronales y se escala 4x a calidad cristalina, quedando catalogada en el servidor NAS central con su año y fecha para siempre.
            </text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="SectionTitle">El Flujo General de Trabajo en 6 Pasos</text:p>

      <text:p text:style-name="CenterP">
        <draw:frame draw:name="ImgFlujo" text:anchor-type="as-char" svg:width="178mm" svg:height="30mm">
          <draw:image xlink:href="{DIR_MANUAL}/diagrama_flujo.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
        </draw:frame>
      </text:p>
      <text:p text:style-name="CaptionP">Figura 1.1: Secuencia esquemática paso a paso desde el escáner físico hasta el servidor NAS.</text:p>

      <table:table table:name="GridResumen" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col60"/>
        <table:table-column table:style-name="Col60"/>
        <table:table-column table:style-name="Col60"/>
        <table:table-row>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold">1. Simple y en 1 Clic</text:p>
            <text:p text:style-name="BodySmall">El sistema se inicia con 1 botón directo. Sin comandos ni complicaciones.</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold">2. Mesa de Control Visual</text:p>
            <text:p text:style-name="BodySmall">Comparador interactivo con slider, lupa 2x y atajos de teclado rápidos.</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold">3. Archivo Permanente</text:p>
            <text:p text:style-name="BodySmall">Inyección automática de metadatos EXIF descriptivos hacia el disco NAS.</text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>


      <!-- ========================================================= -->
      <!-- PÁGINA 2: ARRANQUE, SESIÓN, MÓVIL Y CAPTURA               -->
      <!-- ========================================================= -->
      <text:p text:style-name="PageBreak"/>
      
      <text:p text:style-name="SectionTitle">Paso 1: Poner en Marcha la Estación de Trabajo</text:p>

      <table:table table:name="BoxInicio" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col180"/>
        <table:table-row>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold">🚀 Cómo encender Desktopia Lab en 1 solo paso:</text:p>
            <text:p text:style-name="BulletP">• Hacé doble clic en el acceso directo del escritorio: <text:span text:style-name="Bold">"Iniciar Desktopia Lab"</text:span> (o ejecutá <text:span text:style-name="KbdSpan">./iniciar_desktopia.sh</text:span>).</text:p>
            <text:p text:style-name="BulletP">• El lanzador limpia instancias viejas, arranca el servidor en segundo plano y abre Google Chrome automáticamente.</text:p>
            <text:p text:style-name="BulletP">• Verificá en la esquina superior que el indicador diga <text:span text:style-name="GreenBold">● Activo</text:span>.</text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="BodyP"/>

      <table:table table:name="GridPaso1y2" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col90"/>
        <table:table-column table:style-name="Col90"/>
        <table:table-row>
          <table:table-cell table:style-name="CellAccentBlue">
            <text:p text:style-name="BoxTitleBlue">📱 Operar desde el Celular (Móvil)</text:p>
            <text:p text:style-name="BoxTextBlue">Podés trabajar de pie frente al escáner sin ir y venir al teclado:</text:p>
            <text:p text:style-name="BulletP">1. Tocá el botón <text:span text:style-name="Bold">"Móvil"</text:span> en la barra superior.</text:p>
            <text:p text:style-name="BulletP">2. Escaneá el <text:span text:style-name="Bold">Código QR</text:span> con tu celular (Wi-Fi local).</text:p>
            <text:p text:style-name="BulletP">3. ¡Listo! Tendrás la mesa completa en tu pantalla táctil.</text:p>
          </table:table-cell>
          <table:table-cell table:style-name="CellAccentGreen">
            <text:p text:style-name="BoxTitleGreen">📋 Paso 2: Crear el Lote / Álbum</text:p>
            <text:p text:style-name="BoxTextGreen">Completá los 3 campos obligatorios iniciales:</text:p>
            <text:p text:style-name="BulletP">• <text:span text:style-name="Bold">Operador:</text:span> Tu nombre para tus estadísticas.</text:p>
            <text:p text:style-name="BulletP">• <text:span text:style-name="Bold">Nombre Álbum:</text:span> Ej: <text:span text:style-name="Mono">Vacaciones_Bariloche</text:span>.</text:p>
            <text:p text:style-name="BulletP">• <text:span text:style-name="Bold">Año Histórico:</text:span> Ej: <text:span text:style-name="Mono">1985</text:span> (se graba en EXIF).</text:p>
            <text:p text:style-name="BoxTextGreen"><text:span text:style-name="Bold">Presioná "Iniciar Lote" para comenzar.</text:span></text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="SectionTitle">Paso 3: Métodos de Captura de Fotografías</text:p>

      <table:table table:name="TableMetodos" table:style-name="TableWidth100">
        <table:table-column table:style-name="ColMet1"/>
        <table:table-column table:style-name="ColMet2"/>
        <table:table-column table:style-name="ColMet3"/>
        <table:table-header-rows>
          <table:table-row>
            <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">MÉTODO</text:p></table:table-cell>
            <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">INSTRUCCIONES DE USO</text:p></table:table-cell>
            <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">PROCESO AUTOMÁTICO</text:p></table:table-cell>
          </table:table-row>
        </table:table-header-rows>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Escáner Xerox (Platina)</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Colocá de 1 a 4 fotos sobre el vidrio separadas por 1 cm. Pulsá <text:span text:style-name="Bold">"Escanear"</text:span> (300 DPI).</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">OpenCV detecta los contornos de cada foto, recorta y endereza cada imagen por separado.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">Importar Foto Directa</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Pulsá <text:span text:style-name="Bold">"Importar"</text:span> y elegí fotos tomadas con el celular o desde la PC.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Corrige orientación EXIF, normaliza resolución inteligente y crea su tarjeta de IA.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Simulador de Pruebas</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Pulsá <text:span text:style-name="Bold">"Simulador"</text:span> para cargar una foto de prueba sin usar el escáner.</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Ideal para capacitar a nuevos operadores y practicar los atajos de teclado.</text:p></table:table-cell>
        </table:table-row>
      </table:table>


      <!-- ========================================================= -->
      <!-- PÁGINA 3: EL MOTOR DE IA DUAL                             -->
      <!-- ========================================================= -->
      <text:p text:style-name="PageBreak"/>
      
      <text:p text:style-name="SectionTitle">Paso 4: El Motor de Inteligencia Artificial (Dual Engine)</text:p>
      
      <text:p text:style-name="BodyP">
        Apenas la foto ingresa a Desktopia Lab, dos motores de Inteligencia Artificial de última generación trabajan en paralelo para restaurar cada detalle visual:
      </text:p>

      <text:p text:style-name="CenterP">
        <draw:frame draw:name="ImgIA" text:anchor-type="as-char" svg:width="178mm" svg:height="55mm">
          <draw:image xlink:href="{DIR_MANUAL}/diagrama_ia.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
        </draw:frame>
      </text:p>
      <text:p text:style-name="CaptionP">Figura 3.1: Fusión entre GFPGAN (CPU) y Real-ESRGAN Vulkan (GPU RX 580).</text:p>

      <table:table table:name="GridIA" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col60"/>
        <table:table-column table:style-name="Col60"/>
        <table:table-column table:style-name="Col60"/>
        <table:table-row>
          <table:table-cell table:style-name="CellAccentBlue">
            <text:p text:style-name="BoxTitleBlue">1. Rostros: GFPGAN (CPU)</text:p>
            <text:p text:style-name="BodySmall">• Especializado en rostros humanos.</text:p>
            <text:p text:style-name="BodySmall">• Reconstruye ojos, boca y piel.</text:p>
            <text:p text:style-name="BodySmall"><text:span text:style-name="MonoBlue">caras.png (1x)</text:span></text:p>
          </table:table-cell>
          <table:table-cell table:style-name="CellAccentIndigo">
            <text:p text:style-name="BoxTitleIndigo">2. Nitidez: Real-ESRGAN (GPU)</text:p>
            <text:p text:style-name="BodySmall">• Corre en la placa AMD RX 580.</text:p>
            <text:p text:style-name="BodySmall">• Multiplica píxeles x4 sin deformar.</text:p>
            <text:p text:style-name="BodySmall"><text:span text:style-name="MonoIndigo">ia.png (4x Ultra)</text:span></text:p>
          </table:table-cell>
          <table:table-cell table:style-name="CellAccentGreen">
            <text:p text:style-name="BoxTitleGreen">3. Fusión Total ⭐</text:p>
            <text:p text:style-name="BodySmall">• Combina ambas mejoras en 1 archivo.</text:p>
            <text:p text:style-name="BodySmall">• Rostros humanos 4K + fondo nítido.</text:p>
            <text:p text:style-name="BodySmall"><text:span text:style-name="MonoGreen">completa.png</text:span></text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="BodyP"/>

      <table:table table:name="BoxAutoRot" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col180"/>
        <table:table-row>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold">🔄 Auto-Orientación Inteligente de Rostros:</text:p>
            <text:p text:style-name="TableCellP">
              Si una foto fue colocada acostada en el escáner, la IA mide la posición y ángulo de los ojos y la boca. Si detecta personas con inclinación, <text:span text:style-name="Bold">la rota automáticamente</text:span> para que quede vertical antes de presentártela. Si la foto es un paisaje o un auto sin personas, respeta la orientación original para evitar giros erróneos.
            </text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>


      <!-- ========================================================= -->
      <!-- PÁGINA 4: MESA DE CONTROL Y VISOR COMPARADOR              -->
      <!-- ========================================================= -->
      <text:p text:style-name="PageBreak"/>

      <text:p text:style-name="SectionTitle">Paso 5: La Mesa de Control y el Visor Comparador</text:p>
      
      <text:p text:style-name="BodyP">
        Cada foto procesada se presenta en una tarjeta interactiva de alta precisión con un visor dividido:
      </text:p>

      <text:p text:style-name="CenterP">
        <draw:frame draw:name="ImgVisor" text:anchor-type="as-char" svg:width="178mm" svg:height="68mm">
          <draw:image xlink:href="{DIR_MANUAL}/diagrama_visor.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
        </draw:frame>
      </text:p>
      <text:p text:style-name="CaptionP">Figura 4.1: Componentes del visor comparador, selector de capas y botonera de control.</text:p>

      <table:table table:name="GridVisorTools" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col90"/>
        <table:table-column table:style-name="Col90"/>
        <table:table-row>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold">↔️ El Slider de Comparación</text:p>
            <text:p text:style-name="TableCellP">
              • Arrastrá la línea verde divisoria: a la izquierda ves la foto <text:span text:style-name="Bold">Original</text:span> y a la derecha la versión <text:span text:style-name="GreenBold">Mejorada por IA</text:span>.
            </text:p>
            <text:p text:style-name="TableCellP">
              • Pestañas superiores: pulsá <text:span text:style-name="KbdSpan">1</text:span> para Total, <text:span text:style-name="KbdSpan">2</text:span> para Solo 4x o <text:span text:style-name="KbdSpan">3</text:span> para Facial.
            </text:p>
          </table:table-cell>
          <table:table-cell table:style-name="CellAccentIndigo">
            <text:p text:style-name="BoxTitleIndigo">🔍 La Herramienta Lupa 2x (Zoom)</text:p>
            <text:p text:style-name="BoxTextIndigo">
              • Pulsá el botón <text:span text:style-name="Bold">"Lupa 2x"</text:span> en la esquina o en la barra inferior.
            </text:p>
            <text:p text:style-name="BoxTextIndigo">
              • La foto se agranda 2.2x. <text:span text:style-name="Bold">Arrastrá con el dedo o mouse</text:span> para recorrer bordes y rostros libremente sin salirte del marco.
            </text:p>
            <text:p text:style-name="BoxTextIndigo">
              • Tocá <text:span text:style-name="Bold">"Salir 1x"</text:span> para volver a la vista normal.
            </text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="BodyP"/>

      <table:table table:name="BoxRotar" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col180"/>
        <table:table-row>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold">🔄 Botón Rotar 90°:</text:p>
            <text:p text:style-name="TableCellP">
              Si la foto quedó de costado, pulsá el botón <text:span text:style-name="Bold">"Rotar"</text:span>. Gira en sentido horario todas las variantes al mismo tiempo (Original, Caras, 4x e IA Completa), manteniéndolas en sincronía sin descalibrar el visor.
            </text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>


      <!-- ========================================================= -->
      <!-- PÁGINA 5: RECORTE Y CRITERIOS DE APROBACIÓN               -->
      <!-- ========================================================= -->
      <text:p text:style-name="PageBreak"/>

      <text:p text:style-name="SectionTitle">Paso 6: Herramienta de Recorte y Criterios de Aprobación</text:p>

      <text:p text:style-name="BodyP">
        Para encuadrar bordes o dividir fotos múltiples, hacé clic en <text:span text:style-name="KbdSpan">✂️ Recortar</text:span>:
      </text:p>

      <text:p text:style-name="CenterP">
        <draw:frame draw:name="ImgRecorte" text:anchor-type="as-char" svg:width="178mm" svg:height="44mm">
          <draw:image xlink:href="{DIR_MANUAL}/diagrama_recorte.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
        </draw:frame>
      </text:p>
      <text:p text:style-name="CaptionP">Figura 5.1: Modal de recorte con guías de composición y cruz de precisión central.</text:p>

      <table:table table:name="GridRecorteOpciones" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col90"/>
        <table:table-column table:style-name="Col90"/>
        <table:table-row>
          <table:table-cell table:style-name="CellAccentGreen">
            <text:p text:style-name="BoxTitleGreen">Opción 1: [ Aplicar Recorte ]</text:p>
            <text:p text:style-name="BoxTextGreen">
              Se usa para emprolijar la foto actual. Corta los bordes negros y sincroniza el recorte en todas las capas de IA. Aparece un botón <text:span text:style-name="Bold">"Deshacer"</text:span> por si te equivocás.
            </text:p>
          </table:table-cell>
          <table:table-cell table:style-name="CellAccentIndigo">
            <text:p text:style-name="BoxTitleIndigo">Opción 2: [ Extraer como foto nueva ]</text:p>
            <text:p text:style-name="BoxTextIndigo">
              Se usa cuando dos fotos estaban pegadas y el escáner las tomó juntas. Encuadrá la segunda foto y tocalo: se creará una tarjeta nueva y la IA la procesará de forma independiente.
            </text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="SectionTitle">Guía de Decisiones: ¿Qué Opción Aprobar?</text:p>

      <table:table table:name="TableAprobaciones" table:style-name="TableWidth100">
        <table:table-column table:style-name="ColAprob1"/>
        <table:table-column table:style-name="ColAprob2"/>
        <table:table-column table:style-name="ColAprob3"/>
        <table:table-header-rows>
          <table:table-row>
            <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">BOTÓN</text:p></table:table-cell>
            <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">TECLA</text:p></table:table-cell>
            <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">¿CUÁNDO SE DEBE USAR?</text:p></table:table-cell>
          </table:table-row>
        </table:table-header-rows>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellBold"><text:span text:style-name="GreenBold">⭐ Aprobar Total</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellP"><text:span text:style-name="KbdSpan"> A </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellP"><text:span text:style-name="Bold">RECOMENDADO (90% de los casos):</text:span> siempre que la foto tenga personas y la IA haya mejorado los rostros y la nitidez.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold"><text:span text:style-name="MonoIndigo">Solo 4x (IA)</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP"><text:span text:style-name="KbdSpan"> I </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Para fotos de paisajes, casas, autos o retratos donde los rostros no lucieron naturales.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold"><text:span text:style-name="MonoBlue">Facial (Caras)</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP"><text:span text:style-name="KbdSpan"> C </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Para restaurar rostros conservando la resolución nativa sin aplicar reescalado 4x.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Original</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP"><text:span text:style-name="KbdSpan"> O </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Si el escaneo ya estaba perfecto y la intervención de la IA no aportó beneficio.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold"><text:span text:style-name="MonoRose">🗑️ Descartar</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP"><text:span text:style-name="KbdSpan"> D </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Elimina y borra la foto si salió movida, cortada, borrosa o duplicada.</text:p></table:table-cell>
        </table:table-row>
      </table:table>


      <!-- ========================================================= -->
      <!-- PÁGINA 6: ENVÍO AL NAS Y APAGADO LIMPIO                   -->
      <!-- ========================================================= -->
      <text:p text:style-name="PageBreak"/>

      <text:p text:style-name="SectionTitle">Paso 7: Envío Seguro al Servidor NAS y Metadatos</text:p>

      <text:p text:style-name="BodyP">
        Las fotos aprobadas no se guardan en la PC local, sino que se transfieren de forma cifrada al servidor NAS:
      </text:p>

      <text:p text:style-name="CenterP">
        <draw:frame draw:name="ImgRed" text:anchor-type="as-char" svg:width="178mm" svg:height="36mm">
          <draw:image xlink:href="{DIR_MANUAL}/diagrama_red.png" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
        </draw:frame>
      </text:p>
      <text:p text:style-name="CaptionP">Figura 6.1: Enlace de red y sincronización hacia el servidor NAS central (192.168.1.80).</text:p>

      <table:table table:name="BoxExif" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col180"/>
        <table:table-row>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold">🏷️ Inyección Automática de Metadatos EXIF:</text:p>
            <text:p text:style-name="TableCellP">
              Antes de enviar las fotos, Desktopia Lab inyecta internamente con <text:span text:style-name="KbdSpan">exiftool</text:span>:
            </text:p>
            <text:p text:style-name="BulletP">• <text:span text:style-name="Bold">Fecha Original:</text:span> El año histórico que pusiste al crear el lote (ej: <text:span text:style-name="Mono">1985:01:01 12:00:00</text:span>).</text:p>
            <text:p text:style-name="BulletP">• <text:span text:style-name="Bold">Software:</text:span> Nombre del modelo de IA que aprobaste (ej: <text:span text:style-name="Mono">Desktopia Lab - GFPGAN + Real-ESRGAN</text:span>).</text:p>
            <text:p text:style-name="BulletP">• <text:span text:style-name="Bold">Descripción:</text:span> Resumen de la digitalización para que el archivo sea ordenado de por vida.</text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="BodyP"/>

      <table:table table:name="GridNasBtns" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col90"/>
        <table:table-column table:style-name="Col90"/>
        <table:table-row>
          <table:table-cell table:style-name="CellAccentBlue">
            <text:p text:style-name="BoxTitleBlue">📤 Enviar Lote (Parcial)</text:p>
            <text:p text:style-name="BoxTextBlue">
              Transfiere al NAS las fotos aprobadas hasta ese momento, pero <text:span text:style-name="Bold">mantiene el álbum abierto</text:span> para que puedas continuar escaneando más páginas.
            </text:p>
          </table:table-cell>
          <table:table-cell table:style-name="CellAccentGreen">
            <text:p text:style-name="BoxTitleGreen">🏁 Cerrar Álbum</text:p>
            <text:p text:style-name="BoxTextGreen">
              Se usa cuando terminaste todo el sobre o libro de fotos. Envía las últimas fotos, suma tu total a las estadísticas de operadores y limpia la mesa.
            </text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="SectionTitle">Paso 8: Apagar el Servidor Correctamente</text:p>

      <table:table table:name="BoxApagado" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col180"/>
        <table:table-row>
          <table:table-cell table:style-name="CellAccentRose">
            <text:p text:style-name="BoxTitleRose">🛑 Procedimiento de Apagado Limpio:</text:p>
            <text:p text:style-name="BulletP">1. <text:span text:style-name="Bold">No cierres el navegador directamente</text:span>. Hacé clic en el botón rojo <text:span text:style-name="KbdSpan">Apagar</text:span> en la barra superior.</text:p>
            <text:p text:style-name="BulletP">2. Tildá la casilla <text:span text:style-name="Bold">"Limpiar fotos de la sesión activa al salir"</text:span> para dejar la mesa vacía para el próximo operador.</text:p>
            <text:p text:style-name="BulletP">3. Presioná <text:span text:style-name="Bold">"Apagar y Salir"</text:span>. Se cerrarán los procesos en segundo plano y se liberará la tarjeta gráfica (GPU RX 580).</text:p>
            <text:p text:style-name="BulletP">4. Cuando veas la pantalla negra de confirmación, ya podés cerrar la pestaña.</text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>


      <!-- ========================================================= -->
      <!-- PÁGINA 7: ATAJOS DE TECLADO Y PREGUNTAS FRECUENTES        -->
      <!-- ========================================================= -->
      <text:p text:style-name="PageBreak"/>

      <text:p text:style-name="SectionTitle">⚡ Atajos de Teclado (Cheat Sheet para Operadores)</text:p>

      <table:table table:name="TableAtajos" table:style-name="TableWidth100">
        <table:table-column table:style-name="ColAtajo1"/>
        <table:table-column table:style-name="ColAtajo2"/>
        <table:table-column table:style-name="ColAtajo3"/>
        <table:table-header-rows>
          <table:table-row>
            <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">TECLA</text:p></table:table-cell>
            <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">ACCIÓN</text:p></table:table-cell>
            <table:table-cell table:style-name="CellTableHeader"><text:p text:style-name="TableHeadP">DESCRIPCIÓN</text:p></table:table-cell>
          </table:table-row>
        </table:table-header-rows>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP"><text:span text:style-name="KbdSpan"> 1 </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Capa Total (Rostros+4x)</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Compara la foto Original contra la Restauración Total.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP"><text:span text:style-name="KbdSpan"> 2 </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">Capa Solo 4x</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Compara la foto Original contra el escalado Real-ESRGAN.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP"><text:span text:style-name="KbdSpan"> 3 </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Capa Facial</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Compara la foto Original contra los rostros GFPGAN a 1x.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellP"><text:span text:style-name="KbdSpan"> A </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellBold"><text:span text:style-name="GreenBold">Aprobar Total ⭐</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowGreen"><text:p text:style-name="TableCellP"><text:span text:style-name="Bold">Aprueba y prepara para el NAS la versión completa recomendada.</text:span></text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP"><text:span text:style-name="KbdSpan"> I </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Aprobar Solo 4x</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Aprueba la versión con reescalado sin modificación facial.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP"><text:span text:style-name="KbdSpan"> C </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold">Aprobar Facial</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Aprueba la versión con mejora facial a tamaño original.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP"><text:span text:style-name="KbdSpan"> O </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellBold">Aprobar Original</text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowA"><text:p text:style-name="TableCellP">Aprueba el archivo digital sin intervención de inteligencia artificial.</text:p></table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP"><text:span text:style-name="KbdSpan"> D </text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellBold"><text:span text:style-name="MonoRose">Descartar</text:span></text:p></table:table-cell>
          <table:table-cell table:style-name="CellTableRowB"><text:p text:style-name="TableCellP">Elimina de forma permanente la foto seleccionada.</text:p></table:table-cell>
        </table:table-row>
      </table:table>

      <text:p text:style-name="SectionTitle">Preguntas Frecuentes y Solución Rápida (FAQ)</text:p>

      <table:table table:name="TableFaq" table:style-name="TableWidth100">
        <table:table-column table:style-name="Col180"/>
        <table:table-row>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold">1. ¿Qué hago si una foto quedó acostada o al revés?</text:p>
            <text:p text:style-name="TableCellP">Tocá el botón <text:span text:style-name="KbdSpan">Rotar</text:span>. Cada pulsación gira 90° hacia la derecha y mantiene alineadas todas las capas.</text:p>
          </table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold">2. ¿Por qué una foto dice "Incompleto"?</text:p>
            <text:p text:style-name="TableCellP">Si la GPU estaba ocupada o la foto era gigante, verás un botón amarillo <text:span text:style-name="KbdSpan">Reintentar</text:span>. Tocalo para reprocesarla al instante.</text:p>
          </table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold">3. ¿Cómo veo mi puntaje y cuántas fotos procesé?</text:p>
            <text:p text:style-name="TableCellP">Tocá el botón <text:span text:style-name="KbdSpan">Estadísticas</text:span> en la barra superior. Verás tu total de fotos aprobadas y el desglose de modelos de IA utilizados.</text:p>
          </table:table-cell>
        </table:table-row>
        <table:table-row>
          <table:table-cell table:style-name="CellGray">
            <text:p text:style-name="TableCellBold">4. ¿Dónde quedan las fotos en el servidor NAS?</text:p>
            <text:p text:style-name="TableCellP">Quedan ordenadas en la ruta de red: <text:span text:style-name="Mono">/srv/dev-disk-by-uuid-69fe1c68-291a-4766-8e61-bdc74f584e89/Fotos_escaneadas/[Nombre_Lote]_[Año]/</text:span>.</text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>

    </office:text>
  </office:body>
</office:document>
'''

(DIR_MANUAL / "manual_documento.fodt").write_text(fodt_content, encoding="utf-8")
print("Validando XML con ElementTree...")
ET.fromstring(fodt_content)
print("✅ XML 100% válido!")

print("Compilando .fodt a PDF con LibreOffice...")
cmd = [
    "libreoffice",
    "-env:UserInstallation=file:///tmp/lo_user",
    "--headless",
    "--convert-to", "pdf",
    str(DIR_MANUAL / "manual_documento.fodt"),
    "--outdir", str(DIR_MANUAL)
]
subprocess.run(cmd, check=True)

pdf_orig = DIR_MANUAL / "manual_documento.pdf"
pdf_dest = DIR_MANUAL / "Manual_Operador_Desktopia_Lab.pdf"
if pdf_orig.exists():
    if pdf_dest.exists():
        pdf_dest.unlink()
    pdf_orig.rename(pdf_dest)
    print("✅ PDF generado con éxito en:", pdf_dest)
