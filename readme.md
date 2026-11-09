# Desktopia Lab 2.0 (Core AI) 📸🤖
> **Estación de Digitalización, Restauración con Inteligencia Artificial y Archivo en Red para Fotografías Antiguas y Álbumes Históricos.**

![Versión](https://img.shields.io/badge/Versi%C3%B3n-2.0%20Dual%20Engine-emerald?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20Uvicorn-009688?style=for-the-badge&logo=fastapi)
![Vulkan GPU](https://img.shields.io/badge/GPU%20Engine-Real--ESRGAN%20(AMD%20RX%20580)-red?style=for-the-badge&logo=amd)
![GFPGAN CPU](https://img.shields.io/badge/CPU%20Engine-GFPGAN%20v1.4-blue?style=for-the-badge&logo=pytorch)
![Storage](https://img.shields.io/badge/NAS%20Storage-SSH%20%2F%20rsync%20%2B%20EXIF-orange?style=for-the-badge)

---

## 📋 Tabla de Contenidos
1. [Misión y Propósito](#-misión-y-propósito)
2. [Arquitectura del Sistema y Flujo de Procesamiento](#-arquitectura-del-sistema-y-flujo-de-procesamiento)
3. [Tecnologías y Motores de IA](#-tecnologías-y-motores-de-ia)
4. [Requisitos de Hardware y Sistema](#-requisitos-de-hardware-y-sistema)
5. [Instalación y Configuración](#-instalación-y-configuración)
6. [Puesta en Marcha](#-puesta-en-marcha)
7. [Guía de Operación para Operadores](#-guía-de-operación-para-operadores)
8. [Atajos de Teclado (Cheat Sheet)](#-atajos-de-teclado-cheat-sheet)
9. [Estructura del Proyecto](#-estructura-del-proyecto)
10. [Manual en PDF y Diagramas](#-manual-en-pdf-y-diagramas)
11. [Solución de Problemas Frecuentes (FAQ / Troubleshooting)](#-solución-de-problemas-frecuentes-faq--troubleshooting)

---

## 🎯 Misión y Propósito

**Desktopia Lab** es una estación de trabajo integral diseñada para **rescatar, digitalizar, restaurar y catalogar álbumes familiares y fotografías históricas**. 

El sistema está especialmente optimizado para que **jóvenes operadores** puedan trabajar con una experiencia de usuario ágil, visualmente intuitiva y de nivel profesional:
- **1 solo clic para iniciar y apagar**: Sin necesidad de interactuar con terminales Linux ni comandos complejos.
- **Mesa de control interactiva**: Visor de antes y después con línea divisoria (slider), zoom tipo lupa 2x con desplazamiento libre por bordes y rostros, y rotación en 90° sincronizada.
- **Operación remota desde celular (QR)**: Permite escanear y revisar de pie frente a la platina física del escáner sin desplazarse al teclado de la PC.
- **Archivo seguro y permanente**: Inyección automática de metadatos EXIF fotográficos (año histórico, software de IA y operador) y sincronización con el servidor de almacenamiento NAS.

---

## 🏗 Arquitectura del Sistema y Flujo de Procesamiento

El flujo de trabajo consta de 6 etapas automáticas y sincronizadas:

```
┌─────────────────┐       ┌────────────────────┐       ┌────────────────────────┐
│  1. CAPTURA     │       │  2. RECORTE OPENCV │       │  3. DUAL ENGINE IA     │
│  • Escáner USB  │ ────> │  • Detección autos │ ────> │  • CPU: GFPGAN v1.4    │
│  • Import JPG   │       │  • Auto-orientación│       │  • GPU: Real-ESRGAN 4x │
│  • Simulador    │       │  • Enderezado      │       │  • Fusión Total        │
└─────────────────┘       └────────────────────┘       └────────────────────────┘
                                                                    │
                                                                    ▼
┌─────────────────┐       ┌────────────────────┐       ┌────────────────────────┐
│  6. SERVIDOR NAS│       │  5. METADATOS EXIF │       │  4. REVISIÓN Y APROBAC.│
│  • rsync cifrado│ <──── │  • Año Histórico   │ <──── │  • Visor Slider + Lupa │
│  • 192.168.1.80 │       │  • Modelo de IA    │       │  • Atajos [A, I, C, 0] │
│  • Directorios  │       │  • Operador        │       │  • Recorte de precisión│
└─────────────────┘       └────────────────────┘       └────────────────────────┘
```

---

## 🧠 Tecnologías y Motores de IA

### 1. Reconstrucción Facial: GFPGAN v1.4 (PyTorch / CPU)
- **Función**: Localiza automáticamente rostros humanos mediante redes generativas antagónicas y restaura rasgos degradados (ojos empañados, arrugas perdidas, dientes, forma facial) a tamaño nativo ($1\times$).
- **Ejecución**: Corre en CPU multihilo sin competir por la VRAM de la tarjeta de video.
- **Auto-Orientación Inteligente**: Detecta el ángulo anatómico de los ojos. Si una persona fue escaneada de costado o de cabeza, la gira automáticamente a posición vertical antes de presentarla en pantalla. En fotografías de paisajes, autos o fachadas, no fuerza rotación para evitar falsos positivos.

### 2. Superresolución y Nitidez: Real-ESRGAN Vulkan ncnn (AMD Radeon RX 580 / GPU)
- **Función**: Cuadruplica la resolución de la foto ($4\times$), remueve el grano analógico estropeado y suprime el desenfoque óptico.
- **Ejecución de Alta Estabilidad**: Compilado nativo sobre Vulkan / RADV con pipeline optimizado (`tile: 200`, `threads: 1:1:1`). Evita saturaciones o congelamientos en placas AMD Polaris de 8 GB VRAM.

### 3. Fusión Total de Inteligencia Artificial (Rostros + $4\times$)
- Combina lo mejor de ambos mundos: toma los rostros ultra detallados de GFPGAN y los fusiona geométricamente con el fondo nítido y ampliado a $4\times$ de Real-ESRGAN.
- Produce un archivo maestro de resolución ultra alta listo para impresión o archivo histórico.

### 4. Detección y Separación de Platina con OpenCV
- Permite colocar entre **1 y 4 fotografías** sobre el vidrio del escáner al mismo tiempo.
- OpenCV analiza los contornos de alto contraste, aísla cada foto de forma independiente, corrige la inclinación y genera tarjetas fotográficas separadas en la mesa de control.

### 5. Inyección de Metadatos EXIF fotográficos (`exiftool`)
- Antes de enviar cualquier imagen al servidor de archivo, el sistema escribe metadatos estándares EXIF:
  - `EXIF:DateTimeOriginal`: Año histórico definido por el operador (ej. `1985:01:01 12:00:00`).
  - `EXIF:Software`: Nombre exacto del motor utilizado (ej. `Desktopia Lab - GFPGAN + Real-ESRGAN`).
  - `EXIF:Artist`: Nombre del operador responsable de la digitalización.
  - `EXIF:ImageDescription`: Nombre del lote y procedencia del álbum.

---

## 💻 Requisitos de Hardware y Sistema

### Hardware de la Estación de Trabajo:
- **Procesador (CPU)**: Intel Core i5 / i7 o AMD Ryzen (mínimo 4 núcleos físicos).
- **Memoria RAM**: 8 GB o superior (16 GB recomendado).
- **Placa de Video (GPU)**: AMD Radeon RX 580 (o equivalente compatible con Vulkan 1.2+).
- **Escáner Plano**: Xerox Phaser 3100 (u otro modelo USB compatible con el backend SANE).
- **Red Local (LAN)**: Conexión Ethernet hacia el switch local para transferencia de alta velocidad al NAS.

### Servidor de Almacenamiento NAS:
- **Dirección IP**: `192.168.1.80`
- **Ruta de Archivo**: `/srv/Disco_Nuevo/lab_fotos/`
- **Protocolo de Comunicación**: SSH / rsync sin contraseña mediante claves públicas SSH (`id_rsa`).

---

## 🔧 Instalación y Configuración

### 1. Dependencias del Sistema Operativo (Debian / Ubuntu Linux)
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv \
                    curl unzip \
                    sane sane-utils \
                    libimage-exiftool-perl \
                    rsync \
                    libvulkan1 mesa-vulkan-drivers
```

### 2. Clonado e Instalación Rápida (Todo en 1)
Tras clonar el repositorio, el script `instalar.sh` crea el entorno virtual, instala las dependencias Python, genera tu `.env` desde `.env.example` y descarga automáticamente los binarios y modelos pesados de IA (excluidos de Git):
```bash
git clone https://github.com/MapikGodoy/lab-fotos-vity.git
cd lab-fotos-vity
./instalar.sh
```

### 3. Descarga Automática de Modelos y Pesos de IA
Los archivos pesados (>100 MB) no se almacenan en GitHub. Al correr `./instalar.sh`, `./descargar_modelos.sh`, o la primera vez que ejecutás `./iniciar_desktopia.sh`, se descargan automáticamente:
- **Real-ESRGAN Vulkan ncnn (`ia_engine/`)**: Binario `realesrgan-ncnn-vulkan` y modelos `realesrgan-x4plus` / `animevideov3`.
- **GFPGAN v1.4 + Facexlib (`gfpgan/weights/`)**: `GFPGANv1.4.pth`, `detection_Resnet50_Final.pth` y `parsing_parsenet.pth`.

### 4. Parámetros de Configuración (`.env`)
Copiá `.env.example` a `.env` (o editá el que creó `instalar.sh`) con tus credenciales locales y contraseña del NAS:
```bash
cp .env.example .env
```

### 5. Compatibilidad con Otros Escáneres (Uso en Otra PC)
> **Observación importante**: El sistema viene preconfigurado para el escáner **Xerox Phaser 3100MFP**, pero puede funcionar con **cualquier otro escáner compatible con SANE en Linux** (o incluso sin driver de escaneo) teniendo en cuenta los siguientes puntos:

1. **Cambiar el patrón de dispositivo en `.env` (sin tocar código)**:
   En `app/config.py`, por defecto busca `XeroxPhaser3100:usb:...`. En otra PC, ejecutá `scanimage -L` para ver el identificador de tu nuevo escáner y definí `SCANNER_DEVICE_PATTERN` en tu `.env` local. Por ejemplo, para tomar automáticamente el primer escáner SANE detectado:
   ```ini
   SCANNER_DEVICE_PATTERN=device `([^']+)'
   ```
2. **Ruta del binario y permisos `sudo` sin contraseña**:
   El módulo de escaneo (`app/routers/scanning.py`) ejecuta `sudo /usr/sbin/scanimage` en segundo plano (sin terminal para pedir clave). En otra PC debés:
   - Verificar que exista `/usr/sbin/scanimage` (si tu distribución lo instala en `/usr/bin/scanimage`, crear un enlace simbólico: `sudo ln -s /usr/bin/scanimage /usr/sbin/scanimage`).
   - Permitir ejecutar `scanimage` sin contraseña en `/etc/sudoers` (con `sudo visudo`):
     ```text
     tu_usuario ALL=(ALL) NOPASSWD: /usr/sbin/scanimage
     ```
3. **Parámetro `--mode=Color` y DPI**:
   El comando invoca `--format=png --mode=Color --resolution=150|300`. La gran mayoría de escáneres planos SANE aceptan `Color`; si un modelo antiguo requiriera otro literal (ej. `24bit Color` o `color`), se debe ajustar en `app/routers/scanning.py`.
4. **Alternativas sin drivers propietarios complejos**:
   - **Escáneres modernos USB o Wi-Fi (eSCL / AirScan)**: En distribuciones Ubuntu/Debian modernas, instalando `sane-airscan` la mayoría de escáneres HP, Epson, Canon y Brother funcionan directo en `scanimage -L` sin instalar drivers propietarios.
   - **Usando el software nativo o celular (Botón "Importar")**: Si en la otra PC escaneás con la aplicación del fabricante (o en Windows/macOS), todo el resto del sistema (recorte, GFPGAN, Real-ESRGAN, lupa, EXIF y subida al NAS) funciona al 100% cargando las fotos con el botón **Importar**.

---

## 🚀 Puesta en Marcha

### Inicio en 1 Solo Clic (Para los Chicos / Operadores)
El sistema incluye un script automatizado que limpia instancias previas, inicia el servidor desacoplado en segundo plano y abre Google Chrome directamente en la aplicación:
```bash
./iniciar_desktopia.sh
```
*(También se encuentra disponible el acceso directo con icono en el Escritorio del sistema: **"Iniciar Desktopia Lab"**).*

### Verificación de Estado
- Acceso web local: [http://localhost:7777](http://localhost:7777)
- Acceso desde red local: `http://192.168.1.48:7777`
- Al abrir la interfaz, el indicador superior derecho debe mostrar `● Activo` en verde.

### Apagado Limpio y Seguro
Para finalizar la jornada o liberar la tarjeta gráfica:
1. Hacé clic en el botón rojo **"Apagar"** de la barra superior.
2. Si querés dejar la estación vacía para el siguiente operador, tildá *"Limpiar fotos de la sesión activa al salir"*.
3. Presioná **"Apagar y Salir"**. El sistema detendrá todos los subprocesos de Python, liberará el puerto 7777 y cerrará la sesión de forma limpia.

---

## 📖 Guía de Operación para Operadores

### Paso 1: Configurar el Lote
Al iniciar la aplicación, completá la tarjeta de apertura:
1. **Operador**: Tu nombre o apodo (ej. *Martín*). Permite registrar tu actividad en la tabla de estadísticas.
2. **Nombre del Álbum**: Tema o nombre de la carpeta destino (ej. *Cumple_Abuelo_1985*).
3. **Año Histórico**: Año aproximado de la fotografía (ej. *1985*). Se grabará de forma indeleble en la fecha EXIF de la foto digital.
4. Hacé clic en **"Iniciar Lote"**.

### Paso 2: Digitalizar o Ingresar Fotos
- **Escanear (Vidrio / Platina)**: Colocá entre 1 y 4 fotos sobre el vidrio del escáner separadas por al menos 1 cm. Seleccioná `300 DPI` y presioná **"Escanear"**. OpenCV detectará y recortará cada foto automáticamente.
- **Importar**: Permite cargar archivos ya escaneados o fotos sacadas con el celular (formatos JPG o PNG). Normaliza automáticamente la orientación EXIF y la escala para el motor de IA.
- **Simulador**: Carga fotos históricas de muestra para entrenamiento de nuevos operadores sin desgastar el escáner físico.

### Paso 3: Mesa de Control y Visor Comparador
Cada imagen procesada se muestra en una tarjeta interactiva:
- **Slider Divisorio**: Arrastrá la línea verde para contrastar la foto original (izquierda) contra la restauración con IA (derecha).
- **Selector de Capas (1, 2, 3)**:
  - `Total (Rostros + 4x)`: Fusión completa recomendada.
  - `Solo 4x`: Reescalado nítido sin alteración de rasgos.
  - `Solo Rostros`: Mejora facial a resolución original.
- **Lupa 2x (Zoom Dinámico)**: Presioná el botón de lupa. La imagen se agranda a 2.2x y podés arrastrarla con el dedo o mouse para examinar detalles en las cuatro esquinas sin salirte del marco.
- **Botón Rotar 90°**: Gira en sentido horario todas las versiones de la foto simultáneamente manteniendo la sincronía del visor.
- **Herramienta de Recorte**: Permite reencuadrar con guías de composición y cruz central.
  - *Aplicar Recorte*: Ajusta la foto actual y sincroniza todas las capas de IA. Incluye botón **"Deshacer"** si te equivocaste.
  - *Extraer como Foto Nueva*: Divide fotos que hayan quedado juntas en una sola toma sin perder la anterior.

### Paso 4: Criterios de Aprobación
| Botón | Tecla | ¿Cuándo elegirlo? |
|---|:---:|---|
| **Aprobar Total** | <kbd>A</kbd> | **Recomendado en el 90% de los casos**: La foto contiene personas y las caras mejoraron notablemente junto a la nitidez general. |
| **Solo 4x** | <kbd>I</kbd> | Para paisajes, vehículos, edificios o retratos donde los rostros lucen ya bien sin intervención facial. |
| **Solo Rostros** | <kbd>C</kbd> | Para retratos donde se desea conservar el tamaño y grano original sin superresolución. |
| **Original** | <kbd>0</kbd> | Cuando la fotografía original ya estaba en perfecto estado. |
| **Descartar** | <kbd>D</kbd> | Elimina y borra la toma si salió cortada, borrosa o duplicada. |

### Paso 5: Sincronización con el NAS
- **Enviar Lote (Parcial)**: Transfiere al servidor NAS las fotos aprobadas hasta ese momento, pero mantiene el lote abierto para seguir escaneando.
- **Cerrar Álbum**: Se presiona al terminar el sobre o álbum completo. Sincroniza todas las fotos restantes, suma el puntaje a las estadísticas del operador y deja la mesa lista para el próximo trabajo.

---

## ⌨️ Atajos de Teclado (Cheat Sheet)

Para trabajar a máxima velocidad sin usar el mouse:

| Tecla | Acción |
|:---:|---|
| <kbd>1</kbd> | Ver Capa **Total (Rostros + 4x)** en el comparador |
| <kbd>2</kbd> | Ver Capa **Solo 4x (Real-ESRGAN)** |
| <kbd>3</kbd> | Ver Capa **Solo Rostros (GFPGAN)** |
| <kbd>A</kbd> | **Aprobar Total** (Versión recomendada) |
| <kbd>I</kbd> | **Aprobar Solo 4x** |
| <kbd>C</kbd> | **Aprobar Rostros** |
| <kbd>0</kbd> | **Aprobar Original** |
| <kbd>D</kbd> | **Descartar / Borrar foto** |

---

## 📂 Estructura del Proyecto

```
lab-fotos-vity/
├── app/                            # Núcleo del servidor FastAPI
│   ├── config.py                   # Configuración y variables del sistema
│   ├── main.py                     # Punto de entrada de la aplicación y endpoints
│   ├── models.py                   # Esquemas Pydantic
│   ├── state.py                    # Estado de sesión activa y lotes
│   ├── routers/                    # Endpoints modulares (scanning, photos, processing, sessions)
│   ├── services/                   # Motores de negocio (ai_service, scanner_service, image_processor)
│   └── utils/                      # Utilidades EXIF, QR móvil y manejo de archivos
├── gfpgan/                         # Carpeta de pesos GFPGAN (descargados automáticamente)
├── ia_engine/                      # Motor y modelos Real-ESRGAN Vulkan (descargados automáticamente)
├── manual/                         # Manuales, esquemas e infografías del sistema
│   ├── Manual_Operador_Desktopia_Lab.pdf  # Manual PDF listo para imprimir (7 páginas)
│   ├── manual_documento.fodt       # Código fuente OpenDocument del manual
│   ├── compilar_manual.py          # Script de compilación automatizada a PDF
│   ├── generar_diagramas.py        # Generador de esquemas SVG y PNG de alta resolución
│   └── diagrama_*.svg / .png       # Diagramas vectoriales de flujo, IA, red y visor
├── simulador/                      # Fotografías de prueba históricas para capacitación
├── static/                         # Frontend Web responsivo (HTML, CSS y JS moderno)
│   ├── index.html                  # Interfaz de usuario SPA y estilos SAAS modo oscuro
│   └── js/                         # Módulos JS (app.js, crop.js, scan.js, qr.js)
├── .env.example                    # Plantilla de variables de entorno y credenciales NAS
├── .gitignore                      # Excluye venv, .env, logs y pesos pesados (>100 MB)
├── descargar_modelos.sh            # Descarga automática de pesos GFPGAN y Real-ESRGAN
├── iniciar_desktopia.sh            # Lanzador en 1 solo clic (auto-descarga modelos si faltan)
├── instalar.sh                     # Instalador integral tras clonar el repositorio
├── requirements.txt                # Dependencias de paquetes Python
├── run.py                          # Ejecutor Uvicorn
└── readme.md                       # Documentación técnica del sistema
```

---

## 📑 Manual en PDF y Diagramas

Dentro de la carpeta `manual/` se encuentra disponible el **Manual del Operador en formato PDF de alta calidad**, diseñado especialmente con diagramas vectoriales, infografías y lenguaje amigable para los operadores:

- 📄 **Ruta del archivo**: [`manual/Manual_Operador_Desktopia_Lab.pdf`](manual/Manual_Operador_Desktopia_Lab.pdf)
- 📐 **Diagramas incluidos**:
  - `diagrama_flujo.png`: Secuencia paso a paso del laboratorio.
  - `diagrama_ia.png`: Diagrama de la arquitectura Dual Engine (CPU + GPU + Fusión).
  - `diagrama_visor.png`: Anatomía del visor comparador y botones de control.
  - `diagrama_recorte.png`: Guía de recorte de precisión y división de fotos múltiples.
  - `diagrama_red.png`: Topología de red local y sincronización con el servidor NAS.

Para recompilar el manual tras cualquier modificación:
```bash
python3 manual/compilar_manual.py
```

---

## ❓ Solución de Problemas Frecuentes (FAQ / Troubleshooting)

### 1. ¿Qué hacer si una foto queda en estado "Incompleto" o error de GPU?
- Ocurre si la imagen ingresada tenía dimensiones extremas o si la memoria de la tarjeta de video estaba ocupada por otra tarea.
- **Solución**: En la misma tarjeta aparecerá un botón amarillo **"Reintentar"**. Al presionarlo, el sistema re-encola el procesamiento y lo completa sin perder los datos del lote.

### 2. El escáner Xerox no responde al presionar "Escanear"
- Verificá que el cable USB del escáner esté bien enchufado a la PC y que el equipo esté encendido.
- Verificá en la consola si SANE lo detecta ejecutando:
  ```bash
  scanimage -L
  ```
- Si quedó una sesión de escaneo trabada en Linux, desconectá y volvé a conectar el cable USB o reiniciá el servicio SANE:
  ```bash
  sudo systemctl restart saned
  ```

### 3. Las fotos no se transfieren al servidor NAS
- Verificá la conectividad de red con el NAS:
  ```bash
  ping -c 3 192.168.1.80
  ```
- Verificá que la clave SSH pública esté autorizada en el NAS:
  ```bash
  ssh mak@192.168.1.80 "ls /srv/Disco_Nuevo/lab_fotos"
  ```
- Si la conexión falla, revisá que la IP del NAS no haya cambiado por DHCP en el router.

### 4. El puerto 7777 dice estar ocupado al iniciar
- Si cerraste el navegador pero el servidor quedó ejecutándose de fondo, corré:
  ```bash
  ./iniciar_desktopia.sh
  ```
  *(El script mata automáticamente las instancias viejas antes de iniciar la nueva).*
- O matá los procesos manualmente:
  ```bash
  pkill -f "run.py"
  pkill -f "uvicorn.*app.main:app"
  ```

---

<p align="center">
  <b>Desktopia Lab 2.0</b> • Diseñado para preservar la memoria histórica y familiar con la máxima calidad tecnológica.
</p>
