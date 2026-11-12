# Guía de alineación con la rúbrica - Actividad 8

La rúbrica distribuye la evaluación en cuatro criterios de 25% cada uno.

## 1. Diseño de monitorización y observabilidad - 25%

Busca integrar métricas, logs y trazas y relacionarlos con objetivos operativos.

Evidencia sugerida:
- tabla de indicadores;
- `monitoring_summary.json`;
- `monitoring_log.jsonl`;
- `traces.jsonl`;
- dashboard;
- explicación de qué decisión permite cada indicador.

## 2. Diseño y aplicación de alertas inteligentes - 25%

Busca alertas alineadas con SLO y error budget, con priorización de incidentes y reducción de ruido.

Evidencia sugerida:
- reglas en `config/monitoring_config.json`;
- `alerts.json`;
- severidad warning/critical;
- justificación del umbral;
- relación con SLO/error budget.

## 3. Simulación de incidentes y uso de runbooks - 25%

Busca incidentes relevantes y ejecución estructurada de runbooks.

Evidencia sugerida:
- al menos dos escenarios con `simulate_incidents.py` o incidentes equivalentes de tu proyecto;
- captura antes/después;
- runbook utilizado;
- decisión tomada;
- resultado de recuperación.

## 4. Documentación de la respuesta automatizada - 25%

Busca una respuesta clara y estructurada que incluya automatización efectiva o una implementación educativa coherente.

Evidencia sugerida:
- script o pseudocódigo de rollback/retraining/escalamiento;
- condición que activa la respuesta;
- validación posterior;
- límites de seguridad: cuándo NO automatizar.

## Principio de evaluación

No es necesario que todos los proyectos utilicen el mismo stack tecnológico. Lo importante es demostrar coherencia:

```text
señal
→ SLO/umbral
→ alerta
→ incidente
→ runbook
→ respuesta
→ validación
```
