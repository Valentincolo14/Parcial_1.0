import cv2
import numpy as np
import os
import sys

# ==============================================================================
# 1. CONFIGURACIÓN DEL PROYECTO Y ARCHIVOS ⚙️
# ==============================================================================

# **¡IMPORTANTE!** DEBES CAMBIAR esta ruta por la ruta REAL donde se encuentran tus archivos.
BASE_PATH = 'C:\\Users\\USER\\OneDrive\\Documentos\\2025-2\\VPC\\Parcial\\'

# Lista de tus 5 archivos de entrada (Sentinel-1, polarización VV)
INPUT_FILES = [
    's1a-iw-grd-vv-20250730t232837-20250730t232902-060320-077f23-001.tiff',
    's1a-iw-grd-vv-20250811t232837-20250811t232902-060495-078598-001.tiff',
    's1a-iw-grd-vv-20250823t232837-20250823t232902-060670-078c7b-001.tiff',
    's1a-iw-grd-vv-20250904t232837-20250904t232902-060845-07936b-001.tiff',
    's1a-iw-grd-vv-20250916t232837-20250916t232902-061020-079a6e-001.tiff'
]

# Parámetro para el filtro de reducción de Speckle.
# Un tamaño de kernel impar (5x5, 7x7) determina el grado de suavizado.
KERNEL_SIZE_FILTER = 5 

# ==============================================================================
# 2. FUNCIÓN DE PROCESAMIENTO (RE-ESCALADO + FILTRADO)
# ==============================================================================

def process_sar_image_sequence(img_name, base_path, kernel_size):
    """Carga, re-escala (contraste), filtra y guarda una imagen SAR."""
    print(f"\n--- Iniciando procesamiento: {img_name} ---")

    img_path = os.path.join(base_path, img_name)
    
    # 1. CARGA DE LA IMAGEN (Usando cv2.IMREAD_UNCHANGED para datos SAR brutos)
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    
    if img is None:
        sys.exit(f"ERROR: No se pudo cargar la imagen {img_name}. Revisa la ruta y el nombre.")

    # 2. RE-ESCALADO PARA VISUALIZACIÓN (TU CÓDIGO)
    # --------------------------------------------------------------------------
    print("Aplicando re-escalado de contraste...")
    img2 = img.astype(np.single) # Cambiar a tipo flotante (real)

    # Lógica de contraste basada en el promedio (Media * 3.0)
    escala_display = np.mean(img2) * 3.0
    min_val = np.min(img2) 
    
    # Recorte de valores altos y bajos para mejorar el contraste
    img2[img2 > escala_display] = escala_display 
    img2[img2 < min_val] = min_val # Se mantiene tu lógica original

    # Normalización a 0-255 (rango de 8-bit para visualización estándar)
    img3 = 255.0 * (img2 / escala_display) 
    img_scaled = img3.astype(np.uint8) # Imagen final re-escalada

    # 3. FILTRADO (ELIMINACIÓN DE SPECKLE) 🧽
    # --------------------------------------------------------------------------
    # Utilizamos el Filtro Mediano (Median Blur) como un filtro espacial efectivo.
    # NOTA: Para un filtro especializado como el Filtro Lee o Frost, se requeriría 
    # una implementación manual o librerías externas. Este filtro cumple con el 
    # requisito de reducir el speckle para el análisis visual.
    
    print(f"Aplicando Filtro Mediano ({kernel_size}x{kernel_size}) para reducir Speckle...")
    img_filtered = cv2.medianBlur(img_scaled, kernel_size)
    
    # 4. GUARDAR IMAGEN DE SALIDA
    # --------------------------------------------------------------------------
    # Crear el nombre del archivo de salida: '[nombre]_scaled_filtered.png'
    name_prefix = os.path.splitext(img_name)[0]
    output_name = f"{name_prefix}_scaled_filtered.png"
    output_path = os.path.join(base_path, output_name)
    
    # Guardar la imagen filtrada en formato PNG (sin pérdida de calidad)
    cv2.imwrite(output_path, img_filtered)
    
    print(f"✅ Proceso terminado. Archivo guardado en: {output_path}")

# ==============================================================================
# 3. EJECUCIÓN DEL BUCLE PRINCIPAL
# ==============================================================================

if __name__ == "__main__":
    print(f"Iniciando procesamiento de {len(INPUT_FILES)} imágenes SAR...")
    
    for file in INPUT_FILES:
        process_sar_image_sequence(file, BASE_PATH, KERNEL_SIZE_FILTER)

    print("\n--- ¡Procesamiento de la secuencia de imágenes completado! ---")
    print("Ahora puedes realizar tu análisis visual haciendo zoom para comparar el ruido.")