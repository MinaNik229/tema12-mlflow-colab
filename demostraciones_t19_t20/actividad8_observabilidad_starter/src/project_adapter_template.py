"""Plantilla para adaptar la Actividad 8 a distintas modalidades.

La idea no es forzar todos los proyectos a usar las mismas métricas.
Convierte las salidas de tu proyecto en INDICADORES NUMÉRICOS que el sistema
pueda registrar, comparar y alertar.
"""

from __future__ import annotations

from typing import Any


def extract_project_metrics(raw_input: Any, prediction: Any, metadata: dict) -> dict[str, float]:
    """Devuelve indicadores numéricos de una observación o lote.

    Ejemplos de adaptación:

    - Clasificación: confidence, predicted_class, F1 cuando haya etiquetas.
    - Regresión: absolute_error, residual, RMSE por lote.
    - Imagen: brightness, contrast, resolution, Dice/IoU, embedding summaries.
    - Texto: text_length, language_id, confidence, embedding summaries.
    - Señales: RMS, media, desviación, energía por banda, calidad de señal.
    - Video: FPS, resolución, motion score, latencia, embeddings por clip.

    No es necesario usar todos los indicadores. Selecciona solo los que tengan
    sentido para la operación de tu proyecto.
    """

    raise NotImplementedError(
        "Adapta extract_project_metrics() a tu proyecto y devuelve un diccionario de métricas numéricas."
    )
