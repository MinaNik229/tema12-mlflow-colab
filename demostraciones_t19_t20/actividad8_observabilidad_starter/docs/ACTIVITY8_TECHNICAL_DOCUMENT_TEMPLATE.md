# Plantilla sugerida - Documento técnico Actividad 8

## 1. Contexto del proyecto
- Problema de IA
- Tipo de datos/modalidad
- Modelo o servicio monitoreado

## 2. Indicadores de observabilidad
### Métricas
| Indicador | Qué mide | Baseline | SLO/umbral | Ventana | Acción |
|---|---|---:|---:|---|---|

### Logs
¿Qué eventos se registran y por qué?

### Trazas
¿Qué recorrido o etapa del pipeline se desea seguir?

## 3. Alertas inteligentes
- Regla
- Severidad
- SLO relacionado
- Error budget relacionado
- Acción asociada
- Cómo se evita ruido

## 4. Dashboard operativo
Explica cada panel y qué decisión habilita.

## 5. Estrategia de data drift
- Baseline
- Variables/indicadores comparados
- Método
- Umbral
- Acción

## 6. Runbooks
Incluye al menos los runbooks usados en los incidentes simulados.

## 7. Respuesta automatizada
Describe qué podría ejecutarse de forma automática: rollback, reentrenamiento, escalamiento, rechazo de datos, etc.

## 8. Evidencia
Enumera capturas, archivos JSON/logs, MLflow/W&B y resultados antes/después.
