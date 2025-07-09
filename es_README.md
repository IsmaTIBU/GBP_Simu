
# GBP_Simu - Detección en una simulación del buen o mal posicionamiento de placas en la línea principal de producción

### Uso
### Si quieres entrenar tu propio modelo con los datos
1. Clona el repositorio  
2. Descomprime data.zip y cárgalo en la raíz del proyecto (donde ya está). Esto divide las 4 situaciones/posiciones que el modelo puede detectar.  
3. Descarga todas las versiones de este Git ([Simu_Video](https://github.com/IsmaTIBU/GBP_Simu/releases/tag/Simu_Video)) y cárgalas en la raíz del proyecto, como hicimos con la carpeta 'data'  
4. Ejecuta 'video_mask.py' para generar un video de la línea de producción aplicándole una máscara para que el modelo pueda enfocarse en las 2 posiciones principales y se requieran menos datos para entrenarlo, tomará algo de tiempo. El resultado se cargará en Output/output_masked_video.mp4.  
5. Ejecuta 'Training.py'. Entrenará el modelo, idealmente deberías encontrar que val_loss y loss terminen en un valor bastante similar y accuracy y val_accuracy tendrían una nota bastante alta (de 0-1).

6. Ejecuta 'Model_test.py'. Aquí etiquetamos el video enmascarado con cuadrados que cambian de color dependiendo de la posición de la placa, en otras palabras, dependiendo de lo que el modelo detecte.

#### Si deseas usar este proyecto para una simulación personal, debes grabar un video, usarlo en 'videoToPhoto.py' como entrada, lo cual dividirá el video en todos sus fotogramas y los guardará en 'data', y luego poner las diferentes posiciones en su carpeta respectiva. También tendrás que cambiar las configuraciones de máscaras en 'video_mask.py' y el etiquetado en 'Model_test.py'.   

### Si solo deseas visualizar los resultados con el modelo entrenado actual  
1. Clona el repositorio
2. Descomprime data.zip y cárgalo en la raíz del proyecto (donde ya está). Esto divide las 4 situaciones/posiciones que el modelo puede detectar.
3. Descarga todas las versiones de este Git ([Simu_Video](https://github.com/IsmaTIBU/GBP_Simu/releases/tag/Simu_Video) & [PositionDetection_Model](https://github.com/IsmaTIBU/GBP_Simu/releases/tag/PosiotionDetection_Model)) y cárgalas en la raíz del proyecto, como hicimos con la carpeta 'data'  
4. Ejecuta 'video_mask.py' para generar un video de la línea de producción aplicándole una máscara para que el modelo pueda enfocarse en las 2 posiciones principales y se requieran menos datos para entrenarlo, tomará algo de tiempo. El resultado se cargará en Output/output_masked_video.mp4.  
5. Ejecuta 'Model_test.py'. Aquí etiquetamos el video enmascarado con cuadrados que cambian de color dependiendo de la posición de la placa, en otras palabras, dependiendo de lo que el modelo detecte.