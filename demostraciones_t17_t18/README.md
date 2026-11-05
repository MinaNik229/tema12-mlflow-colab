# Demostraciones T17-T18

Esta carpeta reúne las prácticas del Módulo 3 relacionadas con MLOps, versionado de artefactos, automatización y evolución del modelo.

## Tema 17 - Construcción y versionado

- [Laboratorio: construcción y versionado de artefactos con MLflow](tema17_versionado_artefactos_mlflow/README.md)

La práctica incluye instrucciones completas para Windows y macOS/Linux, dataset didáctico, versionado v1/v2, comparación de métricas y trazabilidad con Git y MLflow.

Flujo principal:

```text
entrenar
→ evaluar
→ crear artefacto
→ versionar
→ comparar
→ seleccionar
```

## Tema 18 - Reentrenamiento y despliegue automatizado

- [Demostración: monitoreo, trigger, retraining, staging y promoción](tema18_reentrenamiento_despliegue_automatizado/README.md)

La demostración continúa el concepto de versionado y simula localmente:

```text
champion
→ monitoreo
→ trigger
→ reentrenamiento
→ challenger
→ staging
→ pruebas
→ promote / reject
```

Incluye instrucciones desde `git clone`, rutas para Windows y macOS/Linux, MLflow Tracking, Model Registry, aliases, pruebas con pytest y un pipeline local automatizado.

## Continuidad pedagógica

```text
T17
¿qué versión del modelo tengo?
        ↓
T18
¿cuándo debo reemplazarla y cómo valido la nueva?
```
