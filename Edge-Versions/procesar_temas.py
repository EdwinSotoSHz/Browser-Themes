import os
import shutil
from PIL import Image
import colorsys

# Configuración de los 11 temas
TEMAS_CONFIG = {
    "Blue-Dark-Theme-Neon": 0.0,            # Tema base original
    "Cyberpunk-Magenta-Theme-Neon": 0.25,   # Rosa / Magenta
    "Deep-Violet-Theme-Neon": 0.15,         # Violeta / Púrpura
    "Electric-lce-Theme-Neon": -0.08,       # Cian / Hielo
    "Golden-Gold-Theme-Neon": 0.52,         # Dorado / Amarillo
    "Matrix-Hacker-Theme-Neon": 0.38,       # Verde Matrix
    "Red-Voltage-Theme-Neon": 0.40,         # Rojo
    "Retrofuturismo-Amber-Theme-Neon": 0.48,# Ámbar / Naranja
    "Silver-Steel-Theme-Neon": 0.0,         # Plata / Gris
    "Sunset-Coral-Theme-Neon": 0.43,        # Coral
    "Teal-Vaporwave-Theme-Neon": 0.32       # Turquesa / Teal
}

NOMBRE_TEMA_BASE = "Blue-Dark-Theme-Neon"

def cambiar_tono(img, shift_hue):
    """Aplica un cambio de tono (Hue) manteniendo la transparencia y brillo."""
    if shift_hue == 0.0:
        return img

    img = img.convert("RGBA")
    pixels = img.load()
    width, height = img.size

    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue

            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            nuevo_h = (h + shift_hue) % 1.0
            nuevo_r, nuevo_g, nuevo_b = colorsys.hsv_to_rgb(nuevo_h, s, v)

            pixels[x, y] = (
                int(nuevo_r * 255),
                int(nuevo_g * 255),
                int(nuevo_b * 255),
                a
            )
    return img

def superponer_edge(img_base, img_overlay_path, padding=10, escala_relativa=0.25):
    """Superpone edge.png en la esquina inferior derecha de img_base."""
    if not os.path.exists(img_overlay_path):
        print(f"   ⚠️ No se encontró {img_overlay_path}")
        return img_base

    overlay = Image.open(img_overlay_path).convert("RGBA")
    
    base_w, base_h = img_base.size
    nuevo_ancho = int(base_w * escala_relativa)
    ratio = nuevo_ancho / float(overlay.width)
    nuevo_alto = int(float(overlay.height) * float(ratio))
    
    overlay = overlay.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)

    pos_x = base_w - nuevo_ancho - padding
    pos_y = base_h - nuevo_alto - padding

    capa_comb = Image.new("RGBA", img_base.size, (0, 0, 0, 0))
    capa_comb.paste(img_base, (0, 0))
    capa_comb.paste(overlay, (pos_x, pos_y), mask=overlay)

    return capa_comb

def restaurar_imagenes_desde_base(raiz_script):
    """Limpia y copia las imágenes del tema base hacia los otros temas."""
    ruta_base_images = os.path.join(raiz_script, NOMBRE_TEMA_BASE, "images")

    if not os.path.exists(ruta_base_images):
        raise FileNotFoundError(f"❌ No se encontró la carpeta base original: {ruta_base_images}")

    print("🔄 Limpiando carpetas y clonando imágenes originales desde Blue-Dark-Theme-Neon...")

    # Lista de archivos originales en la carpeta base
    archivos_base = [
        f for f in os.listdir(ruta_base_images) 
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
    ]

    for carpeta_tema in TEMAS_CONFIG.keys():
        if carpeta_tema == NOMBRE_TEMA_BASE:
            continue

        ruta_destino_images = os.path.join(raiz_script, carpeta_tema, "images")

        # Asegurar que existe la carpeta destino
        os.makedirs(ruta_destino_images, exist_ok=True)

        # 1. Vaciar imágenes existentes
        for archivo in os.listdir(ruta_destino_images):
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                os.remove(os.path.join(ruta_destino_images, archivo))

        # 2. Copiar archivos originales desde el tema base
        for archivo in archivos_base:
            src = os.path.join(ruta_base_images, archivo)
            dst = os.path.join(ruta_destino_images, archivo)
            shutil.copy2(src, dst)

        print(f"   ✓ Imágenes restauradas en: {carpeta_tema}")

def procesar_todo():
    raiz_script = os.path.dirname(os.path.abspath(__file__))
    
    # Subir un nivel para encontrar assets/edge.png
    ruta_edge = os.path.abspath(os.path.join(raiz_script, "..", "assets", "edge.png"))

    print(f"🔍 Logo Edge configurado en: {ruta_edge}\n")

    # Paso A: Restaurar/Clonar las imágenes desde el tema base
    restaurar_imagenes_desde_base(raiz_script)

    print("\n🎨 Aplicando recambio de tono y marca Edge...")

    # Paso B: Aplicar cambios de color y marca de agua
    for carpeta_tema, shift in TEMAS_CONFIG.items():
        ruta_images = os.path.join(raiz_script, carpeta_tema, "images")

        if not os.path.exists(ruta_images):
            print(f"\n❌ La carpeta no existe: {ruta_images}")
            continue

        print(f"\n🎨 Procesando tema: {carpeta_tema}...")

        for archivo in os.listdir(ruta_images):
            if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                ruta_archivo = os.path.join(ruta_images, archivo)
                img = Image.open(ruta_archivo).convert("RGBA")

                # 1. Aplicar cambio de tono
                img_modificada = cambiar_tono(img, shift)

                # 2. Superponer marca Edge solo en logo-gem.png
                if archivo.lower() == "logo-gem.png":
                    img_modificada = superponer_edge(img_modificada, ruta_edge)
                    print(f"   ✓ Recolor y marca Edge añadida a: {archivo}")
                else:
                    print(f"   ✓ Recolor aplicado a: {archivo}")

                # Guardar cambios
                img_modificada.save(ruta_archivo)

    print("\n🚀 ¡Proceso de restauración y reemplazo completado con éxito!")

if __name__ == "__main__":
    procesar_todo()