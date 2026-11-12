# Ejemplos de adaptación por tipo de proyecto

Estos ejemplos son orientativos. No todos los proyectos deben usar las mismas métricas.

| Tipo de proyecto | Calidad | Operación | Drift / entrada |
|---|---|---|---|
| Clasificación | F1, recall, precision, AUC | latencia, error rate | features, distribución de clases, confianza |
| Regresión | RMSE, MAE, R² | latencia, error rate | features, residuales, distribución de predicciones |
| Visión | Dice, IoU, F1 | latencia, GPU, errores | brillo, contraste, resolución, embeddings |
| Texto / NLP | F1, ROUGE, score propio | latencia, errores, longitud/tokens | idioma, longitud, embeddings, confianza |
| Señales | F1, RMSE, score propio | latencia, missing rate | RMS, media, std, potencia por bandas, calidad de señal |
| Video | mAP, F1, IoU | FPS, latencia, GPU | resolución, brillo, movimiento, embeddings |

## Regla práctica

Para modalidades complejas no intentes aplicar el monitor genérico directamente al dato crudo.

```text
imagen / texto / señal / video
        ↓
extraer indicadores numéricos
        ↓
tabla por observación o por lote
        ↓
monitor.py
```

Ejemplos:

```text
imagen → brillo, resolución, embedding, Dice
texto → longitud, idioma, embedding, confianza
señal → RMS, media, std, frecuencia
video → FPS, resolución, motion score, embedding
```

Usa `src/project_adapter_template.py` como guía para implementar tus propios indicadores.
