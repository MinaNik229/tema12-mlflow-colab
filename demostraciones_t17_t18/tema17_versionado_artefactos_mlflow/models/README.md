# models/

Esta carpeta almacenará los artefactos generados por la práctica.

Después de ejecutar v1 y v2 se espera una estructura semejante a:

```text
models/
├── v1/
│   ├── model.pkl
│   ├── metrics.json
│   └── metadata.json
├── v2/
│   ├── model.pkl
│   ├── metrics.json
│   └── metadata.json
└── production.json
```

En proyectos reales, modelos grandes no deberían almacenarse directamente en Git. Para eso se utilizan registros de modelos y almacenes de artefactos, como MLflow Model Registry o almacenamiento de objetos. En este laboratorio los archivos son pequeños y se permiten con fines didácticos.
