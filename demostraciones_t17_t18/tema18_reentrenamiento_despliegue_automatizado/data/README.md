# Datos de la demostración T18

`generate_data.py` crea dos datasets sintéticos:

- `train.csv`: datos históricos usados para crear el champion inicial.
- `production_batch.csv`: lote posterior con un cambio deliberado en la distribución y en la relación entrada-salida.

El cambio es intencional: permite que el modelo inicial se degrade y que el trigger de reentrenamiento pueda observarse durante la clase.

Los CSV generados son locales y están excluidos de Git.
