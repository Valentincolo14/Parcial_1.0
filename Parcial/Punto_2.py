import cv2
import numpy as np
import os
import sys
from sklearn.cluster import KMeans # Mantenemos el algoritmo K-Means estándar
import random # Necesario para el muestreo

# ==============================================================================
# 1. CONFIGURACIÓN DEL PROYECTO Y ARCHIVOS ⚙️
# ==============================================================================

# **¡IMPORTANTE!** DEBES CAMBIAR esta ruta por la ruta REAL de tu carpeta de trabajo.
BASE_PATH = 'C:\\Users\\USER\\OneDrive\\Documentos\\2025-2\\VPC\\Parcial\\'
''

# **Define los nombres de los archivos que vas a clasificar:**
# 1. Imagen FILTRADA (Debe existir: del reto anterior)
IMAGEN_FILTRADA = 's1a-iw-grd-vv-20250730t232837-20250730t232902-060320-077f23-001_scaled_filtered.png'

# 2. Imagen NO FILTRADA (Debe existir: la versión solo re-escalada a 8 bits)
IMAGEN_NO_FILTRADA_ESCALADA = 's1a-iw-grd-vv-20250730t232837-20250730t232902-060320-077f23-001.tiff'
# Si tu archivo se llama diferente (ej: .png o .tiff), cámbialo aquí.

# Parámetros de Clasificación
NUM_CLASES = 4 
PORCENTAJE_MUESTRA = 0.05 # Usaremos solo el 5% de los píxeles para entrenar K-Means

# ==============================================================================
# 2. FUNCIÓN DE CLASIFICACIÓN K-MEANS CON MUESTREO RÁPIDO
# ==============================================================================

def aplicar_kmeans_rapido(img_name, base_path, output_suffix, n_clusters, sample_perc):
    """
    Aplica K-Means entrenando solo sobre una muestra de píxeles para acelerar.
    Re-escala las clases a 0-255 en escala de grises y guarda el resultado.
    """
    img_path = os.path.join(base_path, img_name)
    print(f"\n--- Clasificando: {img_name} ({output_suffix}) ---")
    
    # 1. Cargar y preparar la imagen
    # Usamos IMREAD_GRAYSCALE, asumiendo que las imágenes ya son 8-bit (0-255)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) 
    
    if img is None:
        sys.exit(f"ERROR: No se pudo cargar la imagen {img_name}. Revisa la ruta y el nombre.")

    # Convertir a formato de lista de píxeles (N_píxeles x 1 característica)
    altura, ancho = img.shape
    datos_completos = img.reshape((-1, 1))
    datos_completos = np.float32(datos_completos) # K-Means necesita floats

    # ** ACELERACIÓN: Muestreo Aleatorio (Subsampling) **
    num_total_pixeles = datos_completos.shape[0]
    num_muestra = int(num_total_pixeles * sample_perc)
    
    # Garantizar que el número de muestra no sea 0 y que el muestreo se haga de forma aleatoria
    if num_muestra < n_clusters:
        num_muestra = n_clusters * 10 # Asegurar suficientes datos para las clases
        
    random.seed(42) # Fija la semilla para reproducibilidad
    indices_aleatorios = np.array(random.sample(range(num_total_pixeles), num_muestra))
    
    # Datos de entrenamiento = solo la muestra de píxeles
    datos_entrenamiento = datos_completos[indices_aleatorios]
    
    print(f"Iniciando K-Means con {n_clusters} clases. Entrenando con {num_muestra} píxeles ({sample_perc*100:.1f}%)...")
    
    # 2. Implementar K-Means Estándar (entrenado en la muestra)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10, max_iter=300)
    kmeans.fit(datos_entrenamiento) # Entrenamiento rápido con la muestra
    
    # 3. Aplicar la clasificación a TODOS los píxeles
    # Usar 'predict' en el dataset COMPLETO para clasificar toda la imagen
    labels = kmeans.predict(datos_completos) 
    centroids = kmeans.cluster_centers_

    # 4. Mapear Clases y Re-escalar a Escala de Grises (0-255)
    
    # Ordenar los centroides (intensidades) para que el mapeo sea de oscuro a claro
    sorted_indices = np.argsort(centroids.flatten())
    
    # Asignar valores de gris espaciados uniformemente (ej: 0, 85, 170, 255)
    new_values = np.linspace(0, 255, n_clusters, dtype=np.uint8)
    
    clasified_image_data = np.zeros_like(labels, dtype=np.uint8)
    for i in range(n_clusters):
        original_label = sorted_indices[i]
        new_gray_value = new_values[i]
        clasified_image_data[labels == original_label] = new_gray_value

    # 5. Reconstruir y Guardar la Imagen Clasificada
    img_clasificada = clasified_image_data.reshape(altura, ancho)

    name_prefix = os.path.splitext(img_name)[0].split('_scaled')[0] # Limpiar el nombre
    output_name = f"{name_prefix}_{output_suffix}_kmeans{n_clusters}_clasificado.png"
    output_path = os.path.join(base_path, output_name)
    
    cv2.imwrite(output_path, img_clasificada)
    
    print(f"✅ Clasificación K-Means terminada. Guardada en: {output_path}")
    print(f"Valores de Centroides (Intensidad Media): {centroids.flatten()}")
    print("-" * 60)
    
    return img_clasificada

# ==============================================================================
# 3. EJECUCIÓN DEL PROCESAMIENTO
# ==============================================================================

if __name__ == "__main__":
    print("Iniciando clasificación no supervisada K-Means (Acelerado por muestreo)...")
    
    # 1. Clasificar la imagen FILTRADA
    aplicar_kmeans_rapido(
        img_name=IMAGEN_FILTRADA,
        base_path=BASE_PATH,
        output_suffix="FILTRADA",
        n_clusters=NUM_CLASES,
        sample_perc=PORCENTAJE_MUESTRA
    )

    # 2. Clasificar la imagen NO FILTRADA (solo re-escalada)
    aplicar_kmeans_rapido(
        img_name=IMAGEN_NO_FILTRADA_ESCALADA,
        base_path=BASE_PATH,
        output_suffix="NO_FILTRADA",
        n_clusters=NUM_CLASES,
        sample_perc=PORCENTAJE_MUESTRA
    )
    
    print("\n¡Ambas clasificaciones han finalizado!")
    print("Ahora puedes realizar el análisis comparativo requerido.")