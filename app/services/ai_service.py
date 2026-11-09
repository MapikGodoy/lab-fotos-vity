import asyncio
import subprocess
import os
import sys
import types
import shutil
from pathlib import Path
from PIL import Image, ImageFile
import cv2
import numpy as np

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Monkeypatch de compatibilidad para basicsr con torchvision moderno
try:
    import torchvision.transforms.functional as _F
    if "torchvision.transforms.functional_tensor" not in sys.modules:
        _functional_tensor = types.ModuleType("torchvision.transforms.functional_tensor")
        _functional_tensor.rgb_to_grayscale = _F.rgb_to_grayscale
        sys.modules["torchvision.transforms.functional_tensor"] = _functional_tensor
except Exception as e:
    print(f"Aviso compatibilidad torchvision: {e}")


class AIService:
    def __init__(self, dir_ia: Path, modelo: str, escala: int, 
                 tile: int, threads: str, timeout: int):
        self.dir_ia = dir_ia
        self.modelo = modelo
        self.escala = escala
        self.tile = tile
        self.threads = threads
        self.timeout = timeout
        self._gpu_lock = asyncio.Lock()
        self._gpu_id = "0"
        
        # GFPGAN
        self._gfpgan_restorer = None
        self._gfpgan_lock = asyncio.Lock()
        self._ruta_modelo_gfpgan = self.dir_ia.parent / "gfpgan" / "weights" / "GFPGANv1.4.pth"
        if not self._ruta_modelo_gfpgan.exists():
            self._ruta_modelo_gfpgan = self.dir_ia / "models" / "GFPGANv1.4.pth"

    def _obtener_gfpgan(self):
        """Inicialización Lazy de GFPGAN para no bloquear el arranque de FastAPI."""
        if self._gfpgan_restorer is None:
            from gfpgan import GFPGANer
            print(f"👤 Cargando modelo GFPGAN en CPU desde {self._ruta_modelo_gfpgan}...")
            self._gfpgan_restorer = GFPGANer(
                model_path=str(self._ruta_modelo_gfpgan),
                upscale=1,
                arch="clean",
                channel_multiplier=2,
                bg_upsampler=None,
                device="cpu"
            )
            print("✅ GFPGAN inicializado correctamente en CPU.")
        return self._gfpgan_restorer

    async def detectar_y_auto_orientar_rostros(self, ruta_original: Path) -> dict:
        """
        Analiza si la foto contiene personas y si su orientación es incorrecta.
        Si contiene personas y están de costado o invertidas, rota la imagen original para que quede vertical.
        Si es un paisaje o no tiene personas, NO realiza ninguna rotación.
        """
        def _analizar_orientacion():
            try:
                with Image.open(ruta_original) as pil_img:
                    from PIL import ImageOps
                    pil_img = ImageOps.exif_transpose(pil_img)
                    pil_rgb = pil_img.convert("RGB")
                    img_np = np.array(pil_rgb)
                    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

                alto, ancho = img_bgr.shape[:2]
                restorer = self._obtener_gfpgan()
                face_helper = restorer.face_helper

                def _evaluar_landmarks(landmarks):
                    if not landmarks:
                        return 0, 0
                    votos = {0: 0, 90: 0, 180: 0, 270: 0}
                    for lm in landmarks:
                        eye_center = (lm[0] + lm[1]) / 2.0
                        mouth_center = (lm[3] + lm[4]) / 2.0
                        dx = float(mouth_center[0] - eye_center[0])
                        dy = float(mouth_center[1] - eye_center[1])
                        
                        if dy > 0 and abs(dy) >= abs(dx):
                            votos[0] += 1
                        elif dy < 0 and abs(dy) >= abs(dx):
                            votos[180] += 1
                        elif dx < 0 and abs(dx) > abs(dy):
                            votos[90] += 1
                        elif dx > 0 and abs(dx) > abs(dy):
                            votos[270] += 1

                    angulo_ganador = max(votos, key=votos.get)
                    return angulo_ganador, len(landmarks)

                # 1. Probar en orientación actual (0°)
                face_helper.clean_all()
                face_helper.read_image(img_bgr)
                face_helper.get_face_landmarks_5(only_center_face=False, eye_dist_threshold=5)
                lms_0 = face_helper.all_landmarks_5

                if lms_0 and len(lms_0) > 0:
                    angulo, caras = _evaluar_landmarks(lms_0)
                    if angulo != 0:
                        return {"necesita_rotacion": True, "grados": angulo, "caras": caras}
                    return {"necesita_rotacion": False, "grados": 0, "caras": caras}

                # 2. Si tiene 0 rostros a 0° y la foto es horizontal (ancho > alto),
                # probamos si colocaron una foto vertical de costado en la platina
                if ancho > alto:
                    img_90 = cv2.rotate(img_bgr, cv2.ROTATE_90_CLOCKWISE)
                    face_helper.clean_all()
                    face_helper.read_image(img_90)
                    face_helper.get_face_landmarks_5(only_center_face=False, eye_dist_threshold=5)
                    lms_90 = face_helper.all_landmarks_5

                    if lms_90 and len(lms_90) > 0:
                        ang_90, caras_90 = _evaluar_landmarks(lms_90)
                        if ang_90 == 0:
                            return {"necesita_rotacion": True, "grados": 90, "caras": caras_90}

                    # Probar 270° CW
                    img_270 = cv2.rotate(img_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    face_helper.clean_all()
                    face_helper.read_image(img_270)
                    face_helper.get_face_landmarks_5(only_center_face=False, eye_dist_threshold=5)
                    lms_270 = face_helper.all_landmarks_5

                    if lms_270 and len(lms_270) > 0:
                        ang_270, caras_270 = _evaluar_landmarks(lms_270)
                        if ang_270 == 0:
                            return {"necesita_rotacion": True, "grados": 270, "caras": caras_270}

                # No se detectaron rostros en ninguna orientación: ES UN PAISAJE / OBJETO
                return {"necesita_rotacion": False, "grados": 0, "caras": 0}

            except Exception as e:
                print(f"Aviso en análisis de orientación de rostros: {e}")
                return {"necesita_rotacion": False, "grados": 0, "caras": 0}

        async with self._gfpgan_lock:
            info = await asyncio.to_thread(_analizar_orientacion)

        if info.get("necesita_rotacion") and info.get("grados", 0) != 0:
            grados = info["grados"]
            img = cv2.imread(str(ruta_original))
            if img is not None:
                if grados == 90:
                    rot = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                elif grados == 180:
                    rot = cv2.rotate(img, cv2.ROTATE_180)
                elif grados == 270:
                    rot = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                else:
                    rot = img
                cv2.imwrite(str(ruta_original), rot)
                try: os.chmod(str(ruta_original), 0o666)
                except Exception: pass
                print(f"🔄 Auto-orientación inteligente: {ruta_original.name} rotada {grados}° ({info.get('caras')} rostros detectados).")
                return {"rotada": True, "grados": grados, "caras": info.get("caras")}

        return {"rotada": False, "grados": 0, "caras": info.get("caras", 0)}

    async def procesar_foto_caras(self, ruta_original: Path, ruta_salida: Path) -> dict:
        """Restaura rostros con GFPGAN en CPU."""
        def _correr_gfpgan():
            try:
                with Image.open(ruta_original) as pil_img:
                    from PIL import ImageOps
                    pil_img = ImageOps.exif_transpose(pil_img)
                    pil_rgb = pil_img.convert("RGB")
                    img_np = np.array(pil_rgb)
                    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

                restorer = self._obtener_gfpgan()
                cropped_faces, restored_faces, restored_img = restorer.enhance(
                    img_bgr,
                    has_aligned=False,
                    only_center_face=False,
                    paste_back=True
                )
                
                num_caras = len(cropped_faces) if cropped_faces is not None else 0
                cv2.imwrite(str(ruta_salida), restored_img)
                try:
                    os.chmod(str(ruta_salida), 0o666)
                except Exception:
                    pass

                exito = ruta_salida.exists() and ruta_salida.stat().st_size > 0
                return {"exito": exito, "rostros_detectados": num_caras}
            except Exception as e:
                print(f"❌ Error en GFPGAN para {ruta_original.name}: {e}")
                import traceback
                traceback.print_exc()
                return {"exito": False, "rostros_detectados": 0}

        async with self._gfpgan_lock:
            resultado = await asyncio.to_thread(_correr_gfpgan)
            return resultado

    async def procesar_foto(self, ruta_original: Path, ruta_salida: Path) -> bool:
        """Upscale 4x con Real-ESRGAN Vulkan en GPU RX 580."""
        ruta_temp_jpg = ruta_original.with_suffix('.temp_input.jpg')
        try:
            with Image.open(ruta_original) as img:
                from PIL import ImageOps
                img = ImageOps.exif_transpose(img)
                img_rgb = img.convert('RGB')
                
                # Normalización inteligente para fotos de celular gigantes (evita agotar VRAM o timeouts de 5 min)
                MAX_DIM = 1800
                w, h = img_rgb.size
                if max(w, h) > MAX_DIM:
                    ratio = MAX_DIM / float(max(w, h))
                    nuevo_w = max(100, int(w * ratio))
                    nuevo_h = max(100, int(h * ratio))
                    img_rgb = img_rgb.resize((nuevo_w, nuevo_h), Image.Resampling.LANCZOS)
                    print(f"📐 Foto normalizada para IA: {w}x{h} -> {nuevo_w}x{nuevo_h} (Salida 4x será {nuevo_w*4}x{nuevo_h*4})")
                
                img_rgb.save(ruta_temp_jpg, format='JPEG', quality=95)
            
            comando = [
                str(self.dir_ia / "realesrgan-ncnn-vulkan"),
                "-i", str(ruta_temp_jpg),
                "-o", str(ruta_salida),
                "-n", self.modelo,
                "-s", str(self.escala),
                "-t", str(self.tile),
                "-j", self.threads,
                "-g", self._gpu_id
            ]
            
            print(f"🎮 Usando GPU ID: {self._gpu_id} (RX 580) | Procesando: {ruta_original.name}")
            
            async with self._gpu_lock:
                try:
                    def correr_vulkan():
                        return subprocess.run(
                            comando,
                            cwd=str(self.dir_ia),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            timeout=self.timeout
                        )
                    
                    resultado = await asyncio.to_thread(correr_vulkan)
                    
                    if resultado.returncode != 0:
                        stderr_text = resultado.stderr.decode('utf-8', errors='ignore')
                        print(f"❌ Vulkan stderr: {stderr_text[:500]}")
                    
                    exito = (
                        resultado.returncode == 0 and 
                        ruta_salida.exists() and 
                        ruta_salida.stat().st_size > 1000
                    )
                    
                    if exito:
                        try: os.chmod(str(ruta_salida), 0o666)
                        except Exception: pass
                    else:
                        print(f"⚠️ Fallo en Vulkan (Código: {resultado.returncode})")
                        if ruta_salida.exists():
                            try: ruta_salida.unlink()
                            except Exception: pass
                        
                except subprocess.TimeoutExpired:
                    print(f"⏰ Timeout en Vulkan para {ruta_original.name}")
                    exito = False
                    if ruta_salida.exists():
                        try: ruta_salida.unlink()
                        except Exception: pass
                except Exception as e:
                    print(f"Error crítico en IA: {e}")
                    exito = False
                    if ruta_salida.exists():
                        try: ruta_salida.unlink()
                        except Exception: pass
                
                if ruta_temp_jpg.exists():
                    ruta_temp_jpg.unlink()
                
                # Pausa breve para liberar el contexto de la GPU entre fotos
                await asyncio.sleep(1.0)
            
            return exito
            
        except Exception as e:
            print(f"Error preparando imagen para IA: {e}")
            if 'ruta_temp_jpg' in locals() and ruta_temp_jpg.exists():
                ruta_temp_jpg.unlink()
            return False

    async def procesar_foto_completo(self, ruta_original: Path, ruta_caras: Path, 
                                     ruta_ia: Path, ruta_completa: Path) -> dict:
        """
        Ejecuta en paralelo:
          1. Real-ESRGAN en GPU (RX 580) -> {base}_ia.png (4x)
          2. GFPGAN en CPU -> {base}_caras.png (1x con rostros restaurados)
        Luego genera la versión COMPLETA combinada (Rostros restaurados + Escalado 4x):
          - Si hay rostros: escala la imagen restaurada (_caras) con Real-ESRGAN en GPU.
          - Si no hay rostros o falla: copia segura de la versión 4x (_ia).
        Garantiza que {base}_completa.png SIEMPRE exista y nunca quede rota.
        """
        tarea_ia = self.procesar_foto(ruta_original, ruta_ia)
        tarea_caras = self.procesar_foto_caras(ruta_original, ruta_caras)
        
        exito_ia, resultado_caras = await asyncio.gather(tarea_ia, tarea_caras)
        rostros_detectados = resultado_caras.get("rostros_detectados", 0)
        exito_completa = False

        if exito_ia and ruta_ia.exists() and ruta_ia.stat().st_size > 1000:
            if rostros_detectados > 0 and ruta_caras.exists() and resultado_caras.get("exito", False) and ruta_caras.stat().st_size > 1000:
                print(f"🌟 Generando versión completa combinada (Escalando caras restauradas a 4x con GPU)...")
                try:
                    exito_comp = await self.procesar_foto(ruta_caras, ruta_completa)
                    if exito_comp and ruta_completa.exists() and ruta_completa.stat().st_size > 1000:
                        exito_completa = True
                    else:
                        print(f"⚠️ Fallo generando completa con GPU, aplicando fallback 4x...")
                        shutil.copy2(str(ruta_ia), str(ruta_completa))
                        exito_completa = True
                except Exception as e:
                    print(f"⚠️ Excepción en generación de completa: {e}, aplicando fallback 4x...")
                    shutil.copy2(str(ruta_ia), str(ruta_completa))
                    exito_completa = True
            else:
                # Si no hay rostros detectados, la versión completa es equivalente a la 4x
                try:
                    shutil.copy2(str(ruta_ia), str(ruta_completa))
                    exito_completa = True
                except Exception as e:
                    print(f"Aviso copiando 4x a completa: {e}")

        # Salvaguarda final: si por cualquier razón ruta_completa no existe o es vacía, creamos la copia desde ruta_ia
        if (not ruta_completa.exists() or ruta_completa.stat().st_size <= 1000) and ruta_ia.exists() and ruta_ia.stat().st_size > 1000:
            try:
                shutil.copy2(str(ruta_ia), str(ruta_completa))
                exito_completa = True
            except Exception:
                pass
            except Exception:
                pass

        return {
            "exito_ia": exito_ia,
            "exito_caras": resultado_caras.get("exito", False),
            "exito_completa": exito_completa,
            "rostros_detectados": rostros_detectados
        }
