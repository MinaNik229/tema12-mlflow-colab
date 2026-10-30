# Ejemplo de documentación técnica - Predicción de deserción estudiantil

## 1. Información general
| Componente | Descripción |
|---|---|
| Proyecto | Sistema de predicción de riesgo de deserción estudiantil |
| Versión del documento | 1.0 |
| Estado | Demostración académica / entorno local contenerizado |
| Responsables | Equipo de ciencia de datos y sistemas |

## 2. Propósito y alcance
Documentar la arquitectura, el proceso de despliegue, los componentes operativos y las consideraciones técnicas del sistema. El ejemplo cubre datos, modelo, API, Docker, pruebas y estrategia de despliegue. No pretende representar un entorno de producción real.

## 3. Arquitectura
`Cliente -> FastAPI -> RandomForest -> respuesta JSON`

| Componente | Implementación de la demo |
|---|---|
| Fuente de datos | Dataset sintético embebido en `modelo_desercion.py` |
| Procesamiento | Selección de edad, promedio y asistencia |
| Modelo ML | Random Forest |
| Motor de inferencia | FastAPI / Uvicorn |
| Interfaz | Swagger `/docs` y cliente `SimulaConsumo.py` |
| Infraestructura | Docker local; PaaS como estrategia simulada |

## 4. Datos
Entradas: edad, promedio y asistencia. Salida: predicción binaria, etiqueta de riesgo y probabilidad.

## 5. Modelo
- Algoritmo: RandomForestClassifier
- Entrenamiento: offline
- Artefacto: `modelo_desercion.pkl`
- Variables: edad, promedio, asistencia

## 6. Despliegue
1. Crear entorno e instalar dependencias.
2. Ejecutar `python modelo_desercion.py`.
3. Ejecutar API con Uvicorn y probar `/docs`.
4. Ejecutar `SimulaConsumo.py`.
5. Construir imagen Docker.
6. Ejecutar contenedor y repetir pruebas.
7. Documentar una estrategia PaaS; `Procfile` incluye el comando de inicio de referencia.

## 7. Pruebas
Caso de demostración: edad 22, promedio 5.5, asistencia 60. Se espera una clasificación de alto riesgo en la configuración reproducible incluida.

## 8. Operación y monitoreo
En una evolución a producción se deben observar latencia, número de inferencias, distribución de predicciones, errores y posibles cambios en la distribución de datos.

## 9. Riesgos y limitaciones
- Dataset extremadamente pequeño y sintético.
- No usar para decisiones reales.
- Requiere validación externa antes de cualquier aplicación real.
- Supervisión humana obligatoria.

## 10. Trazabilidad
| Elemento | Versión de demostración |
|---|---|
| Modelo | 1.0 |
| API | 1.0 |
| Documento | 1.0 |
