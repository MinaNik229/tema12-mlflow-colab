# models/

Esta carpeta está vacía al clonar el repositorio, salvo por este README.

Los artefactos se generan **localmente** cuando cada alumno ejecuta la práctica. Después de crear v1 y v2 se espera una estructura semejante a:

```text
models/
├── README.md
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

Estos resultados están excluidos de Git mediante el `.gitignore` de la práctica. La razón es didáctica: **cada estudiante debe generar sus propias versiones**, comparar sus métricas y documentar su propia decisión de promoción.

En proyectos reales, los modelos y checkpoints tampoco suelen almacenarse directamente en Git. Para eso se utilizan sistemas como MLflow Model Registry, almacenamiento de objetos o repositorios especializados de artefactos.
