import os

# Paletas de color neón (Stop 0%, 45%, 55%, 70%, 100%) ajustadas a cada tema
PALETAS_NEON = {
    "Blue-Dark-Theme-Neon": ["#0044FF", "#00C8FF", "#E0F8FF", "#00A3FF", "#0055FF"],
    "Cyberpunk-Magenta-Theme-Neon": ["#FF0055", "#FF007F", "#FFE0F5", "#FF00CC", "#9900CC"],
    "Deep-Violet-Theme-Neon": ["#5500FF", "#8A00FF", "#F0E0FF", "#AA00FF", "#4400AA"],
    "Electric-Ice-Theme-Neon": ["#0077FF", "#00E5FF", "#E0FFFF", "#00B2FF", "#0055CC"],
    "Golden-Gold-Theme-Neon": ["#FF8800", "#FFC800", "#FFFFE0", "#FFD700", "#CC6600"],
    "Matrix-Hacker-Theme-Neon": ["#00AA33", "#00FF66", "#E0FFE8", "#00CC44", "#007722"],
    "Red-Voltage-Theme-Neon": ["#CC0000", "#FF2A2A", "#FFE0E0", "#FF0033", "#880000"],
    "Retrofuturismo-Amber-Theme-Neon": ["#FF4500", "#FF7700", "#FFEEDD", "#FF9900", "#CC3300"],
    "Silver-Steel-Theme-Neon": ["#556677", "#AABBCC", "#FFFFFF", "#8899AA", "#334455"],
    "Sunset-Coral-Theme-Neon": ["#FF3366", "#FF6688", "#FFE6EC", "#FF5577", "#CC1144"],
    "Teal-Vaporwave-Theme-Neon": ["#008080", "#00E5CC", "#E0FFFF", "#00B3A1", "#005952"]
}

PLANTILLA_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">
  <defs>
    <!-- Filtro de resplandor neón -->
    <filter id="neon-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="blur1" />
      <feGaussianBlur stdDeviation="7" result="blur2" />
      <feMerge>
        <feMergeNode in="blur2" />
        <feMergeNode in="blur1" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Gradiente de color dinámico -->
    <linearGradient id="neon-gradient" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{c0}" />
      <stop offset="45%" stop-color="{c1}" />
      <stop offset="55%" stop-color="{c2}" />
      <stop offset="70%" stop-color="{c3}" />
      <stop offset="100%" stop-color="{c4}" />
    </linearGradient>
  </defs>

  <!-- Fondo oscuro minimalista -->
  <rect width="128" height="128" rx="28" fill="#050B14" />

  <!-- Trazo fluido en forma de 'S' estilo Edge -->
  <path d="M 86,34 C 76,26 52,24 42,38 C 30,54 40,68 64,64 C 88,60 98,74 86,90 C 76,104 52,102 42,94"
        fill="none" 
        stroke="url(#neon-gradient)" 
        stroke-width="10" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        filter="url(#neon-glow)" />
</svg>"""

def generar_svgs():
    raiz_script = os.path.dirname(os.path.abspath(__file__))
    carpeta_salida = os.path.join(raiz_script, "svgs_generados")
    os.makedirs(carpeta_salida, exist_ok=True)

    print("🎨 Generando los 11 iconos SVG neón...\n")

    for tema, colores in PALETAS_NEON.items():
        contenido_svg = PLANTILLA_SVG.format(
            c0=colores[0],
            c1=colores[1],
            c2=colores[2],
            c3=colores[3],
            c4=colores[4]
        )

        nombre_archivo = f"{tema.lower().replace('-theme-neon', '')}.svg"
        ruta_guardado = os.path.join(carpeta_salida, nombre_archivo)

        with open(ruta_guardado, "w", encoding="utf-8") as f:
            f.write(contenido_svg)

        print(f"   ✓ Creado: {nombre_archivo}")

    print(f"\n🚀 ¡Los 11 archivos SVG se guardaron en la carpeta: {carpeta_salida}!")

if __name__ == "__main__":
    generar_svgs()