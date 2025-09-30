CONCLUSIONES


PUNTO_1

Efecto del Re-escalado: El re-escalado realizado (con el factor de media×3.0) convierte los datos originales de alta profundidad (16 bits o más) a un formato 8 bits (uint8) para que sea visible en un monitor estándar (rango 0-255).
La imagen re-escalada (8-bit) permite que los valores útiles (la banda de energía promedio) se vean mejor, mientras que los picos de energía muy brillantes se recortan 
Si el factor 3.0 fue adecuado. Si la imagen se ve demasiado oscura o muy blanca, el contraste necesita ajuste
En conclusión, el procesamiento de las imágenes SAR de Sentinel-1 demostró la necesidad crítica de la eliminación del ruido speckle. El Filtro Mediano (5×5) aplicado tras el re-escalado de contraste fue altamente eficaz en suavizar las superficies homogéneas, haciendo la escena visualmente más interpretable. Sin embargo, como se espera con filtros espaciales, se apreció una ligera pérdida de definición en los objetos lineales finos. Las 5 imágenes filtradas representan ahora una secuencia temporal coherente y limpia, apta para tareas de análisis cuantitativo más avanzado, como la detección de cambios.

PUNTO_2


Speckle/Ruido

Imagen NO FILTRADA
Las clases están muy fragmentadas; hay "sal y pimienta" dentro de las grandes regiones homogéneas.

Imagen FILTRADA
Las clases son más suaves y cohesivas. Las áreas grandes (agua, campos) están representadas por bloques de píxeles del mismo color.


Fronteras/Bordes

Imagen NO FILTRADA
Los límites entre las clases pueden ser muy irregulares y ruidosos.	

Imagen FILTRADA
Los límites de las clases son más claros y definidos, lo que facilita la identificación de parcelas o cuerpos de agua.


Calidad de Agrupamiento

Imagen NO FILTRADA
El K-Means puede tener problemas para converger, ya que el ruido speckle introduce mucha variabilidad dentro de una misma cobertura.	

Imagen FILTRADA
El K-Means resulta en una mejor segmentación, ya que el filtro ayuda a que los píxeles de una misma cobertura tengan valores más cercanos entre sí (mayor coherencia).


Se usaron 4 clases:
Clase 1 (0/Oscura)	Agua y Sombras
Clase 2 (85/Gris Oscuro)	Vegetación Baja o Suelo Desnudo	
Clase 3 (170/Gris Claro)	Vegetación Media/Alta o Materiales Porosos	
Clase 4 (255/Blanca)	Estructuras Urbanas (Efecto de Doble Rebote)

Agua: Se ve claramente en la Clase 1 (Negra). El agua es la cobertura más limpia.

Vegetación Baja (Campos): Queda distribuida principalmente en la Clase 2 (Gris Oscuro), pero con mucha mezcla con la Clase 3.

Vegetación Media/Alta (Bosques): Se clasifica mayormente en la Clase 3 (Gris Claro), reflejando su mayor interacción volumétrica con el radar.

Edificios (Áreas Urbanas): Aparecen como puntos o manchas brillantes en la Clase 4 (Blanca). Esta es la clase más pequeña en área, pero la más intensa.


La clasificación K-Means es significativamente más limpia y representativa de la cobertura terrestre real cuando se aplica a la imagen filtrada, demostrando que el paso de reducción de speckle es esencial para el análisis cuantitativo de imágenes SAR.


PUNTO_3


Conclusión 1: El Ruido (Speckle) Destruye la Clasificación
Impacto Dominante: La imagen NO FILTRADA mostró un porcentaje de agua del 89.17%. Esto no significa que la escena esté cubierta de agua; significa que el algoritmo K-Means fue incapaz de diferenciar la señal de la tierra de la señal del agua.


Atracción del Centroide Oscuro: La alta variabilidad del speckle en los píxeles de tierra (vegetación y suelo) fue menor que la de los píxeles brillantes (edificios). Como resultado, la mayoría de los píxeles ruidosos fueron agrupados erróneamente en la Clase 1 (la clase más oscura, Agua), forzando a casi toda la escena a ser clasificada como agua o sombra.


Conclusión 2: Inviabilidad de la Medición sin Pre-Procesamiento
Fallo del Modelo: La clasificación K-Means es sensible a la intensidad del píxel. En la imagen no filtrada, el speckle introduce tanta variación que el algoritmo clasifica el ruido aleatorio en lugar de las características de la superficie terrestre.


Prueba de la Necesidad: La diferencia del 65.55% demuestra de forma inequívoca que la información cuantitativa extraída de una imagen SAR sin filtro de speckle no tiene validez científica ni práctica. Si se usara el resultado no filtrado para estimar la inundación o la disponibilidad de agua, las conclusiones serían catastróficas.


Conclusión 3: Éxito del Flujo de Trabajo SAR
Fiabilidad: La medición basada en la imagen FILTRADA (23.62%) es la medición confiable. El paso de reducción de speckle limpió las variaciones por ruido, permitiendo que K-Means agrupara correctamente los píxeles según las propiedades reales de retrodispersión (agua oscura, edificios brillantes, vegetación media).


El ejercicio prueba que, para la teledetección SAR, el filtro de speckle no es una mejora visual, sino una condición necesaria para que los algoritmos de clasificación y las mediciones de área funcionen correctamente.
