import cv2
import numpy as np
import os
import sys

# ==============================================================================
# 1. CONFIGURACIÓN DEL PROYECTO Y ARCHIVOS ⚙️
# ==============================================================================

# **¡IMPORTANTE!** Reemplaza esta ruta por la ruta REAL de tu carpeta de trabajo.
BASE_PATH = 'C:\\Users\\USER\\OneDrive\\Documentos\\2025-2\\VPC\\Parcial\\'

# Nombres de los archivos clasificados generados en el paso anterior:
# Asegúrate de que estos archivos existen en tu BASE_PATH.
CLASIFICADA_FILTRADA = 's1a-iw-grd-vv-20250730t232837-20250730t232902-060320-077f23-001_FILTRADA_kmeans4_clasificado.png'
CLASIFICADA_NO_FILTRADA = 's1a-iw-grd-vv-20250730t232837-20250730t232902-060320-077f23-001_NO_FILTRADA_kmeans4_clasificado.png'

# Parámetros Clave:
# La Clase Agua fue la más oscura (valor más bajo) en la clasificación K-Means
VALOR_CLASE_AGUA = 0  # El valor de gris asignado a la Clase 1 (Agua)

# ==============================================================================
# 2. FUNCIÓN DE SEGMENTACIÓN BINARIA Y MEDICIÓN
# ==============================================================================

def segmentar_y_medir_agua(img_name, base_path, clase_agua_val, output_suffix):
    """
    Carga la imagen clasificada, segmenta solo la clase 'agua' (binario)
    y mide el porcentaje de área de esa clase.
    """
    img_path = os.path.join(base_path, img_name)
    print(f"\n--- Analizando: {img_name} ({output_suffix}) ---")
    
    # 1. Cargar la imagen clasificada (en escala de grises 8-bit)
    img_clasificada = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) 
    
    if img_clasificada is None:
        sys.exit(f"ERROR: No se pudo cargar la imagen clasificada {img_name}.")

    # 2. Segmentación Binaria (Clase Agua en blanco, el resto en negro)
    # Crear una máscara donde solo los píxeles iguales a VALOR_CLASE_AGUA son 255 (Blanco)
    
    # Thresholding: Si el valor del píxel es IGUAL a la Clase Agua (0), lo hace 255; de lo contrario, 0.
    # Usamos THRESH_BINARY para que la clase de interés (agua) sea el fondo y luego la invertimos,
    # o usamos THRESH_BINARY_INV. La forma más directa es crear la máscara:
    mask_agua = np.where(img_clasificada == clase_agua_val, 255, 0).astype(np.uint8)
    
    # 3. Medición del Porcentaje de Agua
    
    num_total_pixeles = img_clasificada.size
    # Contar los píxeles de la clase agua (valor 255 en la máscara)
    pixeles_agua = np.sum(mask_agua == 255)
    
    porcentaje_agua = (pixeles_agua / num_total_pixeles) * 100
    
    print(f"Número de Píxeles de Agua: {pixeles_agua:,}")
    print(f"Píxeles Totales de la Imagen: {num_total_pixeles:,}")
    print(f"🔵 Porcentaje de Agua Medido: {porcentaje_agua:.4f}%")
    
    # 4. Guardar la Imagen de Salida (Mapa Binario de Agua)
    
    name_prefix = os.path.splitext(img_name)[0]
    output_name = f"{name_prefix}_AGUA_BINARIA.png"
    output_path = os.path.join(base_path, output_name)
    
    cv2.imwrite(output_path, mask_agua)
    
    print(f"✅ Mapa Binario de Agua guardado en: {output_path}")
    print("-" * 60)
    
    return porcentaje_agua

# ==============================================================================
# 3. EJECUCIÓN Y COMPARACIÓN
# ==============================================================================

if __name__ == "__main__":
    print("Iniciando Segmentación Binaria de la Clase 'Agua'...")
    
    # Procesar la imagen FILTRADA
    porc_filtrada = segmentar_y_medir_agua(
        img_name=CLASIFICADA_FILTRADA,
        base_path=BASE_PATH,
        clase_agua_val=VALOR_CLASE_AGUA,
        output_suffix="FILTRADA"
    )

    # Procesar la imagen NO FILTRADA
    porc_no_filtrada = segmentar_y_medir_agua(
        img_name=CLASIFICADA_NO_FILTRADA,
        base_path=BASE_PATH,
        clase_agua_val=VALOR_CLASE_AGUA,
        output_suffix="NO_FILTRADA"
    )
    
    print("\n--- RESUMEN DE MEDICIONES ---")
    print(f"Porcentaje de Agua (Imagen Filtrada): {porc_filtrada:.4f}%")
    print(f"Porcentaje de Agua (Imagen No Filtrada): {porc_no_filtrada:.4f}%")
    
    diferencia = abs(porc_filtrada - porc_no_filtrada)
    print(f"Diferencia Absoluta entre Mediciones: {diferencia:.4f}%")
    print("\n¡Segmentación y medición completada! Continúa con el análisis.")