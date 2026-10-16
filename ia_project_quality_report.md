# Reporte de calidad — Antes vs Después

## Resumen de filas
- Filas originales: **6000**
- Filas después de deduplicación: **3290**

## Duplicados
- Duplicados por email (antes): **4199** | (después): **191**
- Duplicados por nombre+fecha (antes): **793** | (después): **36**

## Emails
- Emails vacíos (antes): **192** | (después): **191**
- Emails inválidos (antes): **3612** | (después): **1959**

## Categorización
- Valores únicos de `customer_status` (antes): **8** | (después): **3**
- Valores únicos de `plan` (antes): **6** | (después): **3**

## Consistencias
- Revisa en el cuaderno la celda de consistencias (`time_consistent`, `state_required_ok`) para la comparación exacta.

## Notas
- Conversión de moneda: se asumió **USD→MXN = 17.0** sólo para fines de práctica.
- La selección canónica prioriza email válido, `last_login` más reciente, plan de mayor jerarquía y mayor monto.
- Este dataset y pipeline son **sintéticos**.