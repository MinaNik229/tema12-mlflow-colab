# Runbook - [Nombre del incidente]

## 1. Señal que activa el runbook
- Métrica / log / traza:
- Umbral o condición:
- Severidad: P1 / P2 / P3

## 2. Impacto esperado
Describe qué componente, usuario o resultado del proyecto puede verse afectado.

## 3. Diagnóstico inicial
1. Revisar...
2. Comparar...
3. Confirmar...

## 4. Acción principal
Describe la acción que se ejecutará primero.

Ejemplos:
- rollback a versión anterior;
- reentrenamiento;
- limpieza/rechazo de lote;
- escalamiento a responsable;
- degradación controlada del servicio.

## 5. Validación de recuperación
Define qué métrica debe volver a rango normal y durante cuánto tiempo.

## 6. Evidencia a conservar
- captura del dashboard;
- log del incidente;
- alerta generada;
- resultado antes/después;
- decisión tomada.

## 7. Mejora posterior
¿Qué cambio harías para reducir la probabilidad o impacto de que vuelva a ocurrir?
