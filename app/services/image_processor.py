import cv2
import numpy as np
from pathlib import Path
from PIL import Image, ImageFile
from typing import List
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

class ImageProcessor:
    def __init__(self):
        self.umbral_bypass = 1400
        self.area_minima = 100000
        self.pad = 10
        self.umbral_threshold = 220

    def cargar_imagen_tolerante(self, ruta: Path) -> np.ndarray:
        try:
            with Image.open(ruta) as pil_img:
                from PIL import ImageOps
                pil_img = ImageOps.exif_transpose(pil_img)
                pil_rgb = pil_img.convert("RGB")
                arr = np.array(pil_rgb)
                return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"Error Pillow: {e}")
            return cv2.imread(str(ruta))

    def order_points(self, pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect

    def procesar_platina(self, ruta_platina: Path, prefijo_base: str,
                         dir_salida: Path, forzar_recorte: bool = False) -> List[str]:
        try:
            image = self.cargar_imagen_tolerante(ruta_platina)
            if image is None:
                print("Error: No se pudo decodificar la imagen.")
                return []

            alto_img, ancho_img = image.shape[:2]
            print(f"📷 Imagen: {ancho_img}x{alto_img}")

            # Bypass para fotos chicas (una sola foto directa del simulador)
            if not forzar_recorte and alto_img < self.umbral_bypass and ancho_img < self.umbral_bypass:
                nombre_unico = f"{prefijo_base}_1"
                ruta_final = dir_salida / f"{nombre_unico}_original.png"
                cv2.imwrite(str(ruta_final), image)
                try: os.chmod(str(ruta_final), 0o666)
                except: pass
                return [nombre_unico]

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blurred, self.umbral_threshold, 255, cv2.THRESH_BINARY_INV)

            # Limpieza de bordes externos (sombras de la tapa del escaner)
            thresh[:10, :] = 0
            thresh[-10:, :] = 0
            thresh[:, :10] = 0
            thresh[:, -10:] = 0

            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            fotos_extraidas = []
            contador = 1
            contornos = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])

            for c in contornos:
                if cv2.contourArea(c) > self.area_minima:
                    rect = cv2.minAreaRect(c)
                    box = cv2.boxPoints(rect)
                    box = np.array(box, dtype="float32")
                    src = self.order_points(box)

                    widthA = np.linalg.norm(src[2] - src[3])
                    widthB = np.linalg.norm(src[1] - src[0])
                    maxWidth = max(int(widthA), int(widthB))

                    heightA = np.linalg.norm(src[1] - src[2])
                    heightB = np.linalg.norm(src[0] - src[3])
                    maxHeight = max(int(heightA), int(heightB))

                    pad = self.pad
                    maxWidth += pad * 2
                    maxHeight += pad * 2

                    dst = np.array([
                        [pad, pad],
                        [maxWidth - 1 - pad, pad],
                        [maxWidth - 1 - pad, maxHeight - 1 - pad],
                        [pad, maxHeight - 1 - pad]
                    ], dtype="float32")

                    M = cv2.getPerspectiveTransform(src, dst)
                    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

                    nombre_item = f"{prefijo_base}_{contador}"
                    ruta_item = dir_salida / f"{nombre_item}_original.png"
                    cv2.imwrite(str(ruta_item), warped)
                    try: os.chmod(str(ruta_item), 0o666)
                    except: pass

                    fotos_extraidas.append(nombre_item)
                    print(f"  ✅ Foto {contador}: {maxWidth}x{maxHeight}")
                    contador += 1

            # Fallback: si no detecto contornos, guardo la imagen completa
            if not fotos_extraidas:
                nombre_unico = f"{prefijo_base}_1"
                ruta_final = dir_salida / f"{nombre_unico}_original.png"
                cv2.imwrite(str(ruta_final), image)
                try: os.chmod(str(ruta_final), 0o666)
                except: pass
                fotos_extraidas.append(nombre_unico)
                print("  ⚠️ Sin contornos, guardando imagen completa")

            print(f"✅ Total: {len(fotos_extraidas)} foto(s)")
            return fotos_extraidas

        except Exception as e:
            print(f"❌ Error en procesar_platina: {e}")
            import traceback
            traceback.print_exc()
            return []
