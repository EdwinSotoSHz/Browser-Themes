import os
import zipfile

# Lista de tus temas
TEMAS = [
    "Blue-Dark-Theme-Neon",
    "Cyberpunk-Magenta-Theme-Neon",
    "Deep-Violet-Theme-Neon",
    "Electric-lce-Theme-Neon",
    "Golden-Gold-Theme-Neon",
    "Matrix-Hacker-Theme-Neon",
    "Red-Voltage-Theme-Neon",
    "Retrofuturismo-Amber-Theme-Neon",
    "Silver-Steel-Theme-Neon",
    "Sunset-Coral-Theme-Neon",
    "Teal-Vaporwave-Theme-Neon"
]

def comprimir_tema(ruta_tema, ruta_zip_salida):
    """Comprime manifest.json y la carpeta images/ en la raíz del archivo .zip."""
    ruta_manifest = os.path.join(ruta_tema, "manifest.json")
    ruta_images = os.path.join(ruta_tema, "images")

    # Verificaciones previas
    if not os.path.exists(ruta_manifest):
        print(f"   ⚠️ No se encontró manifest.json en: {ruta_tema}")
        return False

    if not os.path.exists(ruta_images):
        print(f"   ⚠️ No se encontró la carpeta images/ en: {ruta_tema}")
        return False

    with zipfile.ZipFile(ruta_zip_salida, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 1. Agregar manifest.json en la raíz del zip
        zipf.write(ruta_manifest, arcname="manifest.json")

        # 2. Agregar el contenido de images/ dentro de la estructura 'images/...'
        for root, _, files in os.walk(ruta_images):
            for file in files:
                ruta_completa = os.path.join(root, file)
                # Calcula la ruta relativa para conservar la carpeta 'images/nombre_archivo'
                rel_path = os.path.relpath(ruta_completa, ruta_tema)
                zipf.write(ruta_completa, arcname=rel_path)

    return True

def procesar_compresion():
    raiz_script = os.path.dirname(os.path.abspath(__file__))

    print("📦 Iniciando compresión de temas para la Chrome Web Store...\n")

    for tema in TEMAS:
        ruta_tema = os.path.join(raiz_script, tema)

        if not os.path.exists(ruta_tema):
            print(f"❌ La carpeta del tema no existe: {ruta_tema}")
            continue

        # El archivo .zip se guardará en la raíz principal (donde corre el script)
        nombre_zip = f"{tema}.zip"
        ruta_zip_salida = os.path.join(raiz_script, nombre_zip)

        if comprimir_tema(ruta_tema, ruta_zip_salida):
            print(f"   ✓ Creado: {nombre_zip}")

    print("\n🚀 ¡Todos los temas han sido comprimidos en la raíz!")

if __name__ == "__main__":
    procesar_compresion()