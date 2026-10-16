import os
from git import Repo, GitCommandError

# ==========================
# CONFIGURACIÓN
# ==========================

# Ruta donde está tu dataset
RUTA_PROYECTO = r"C:/ruta/a/tu/proyecto"

# URL del repositorio remoto
REPO_URL = "https://github.com/usuario/repositorio.git"

# Mensaje del commit
MENSAJE_COMMIT = "Actualización de dataset limpio y deduplicado"

# Rama principal
RAMA = "main"


# ==========================
# FUNCIÓN PRINCIPAL
# ==========================

def subir_dataset():

    try:
        # Cambiar a la carpeta del proyecto
        os.chdir(RUTA_PROYECTO)

        # Verificar si ya es repo Git
        if not os.path.exists(".git"):
            print("Inicializando repositorio...")
            repo = Repo.init(RUTA_PROYECTO)
            repo.create_remote("origin", REPO_URL)
        else:
            print("Repositorio existente detectado...")
            repo = Repo(RUTA_PROYECTO)

        # Agregar archivos
        print("Agregando archivos...")
        repo.git.add(all=True)

        # Verificar si hay cambios
        if not repo.is_dirty(untracked_files=True):
            print("No hay cambios para subir.")
            return

        # Hacer commit
        print("Creando commit...")
        repo.index.commit(MENSAJE_COMMIT)

        # Subir cambios
        print("Subiendo al repositorio...")
        origin = repo.remote(name="origin")
        origin.push(RAMA)

        print("✅ Dataset subido correctamente.")

    except GitCommandError as e:
        print("❌ Error con Git:")
        print(e)

    except Exception as e:
        print("❌ Error general:")
        print(e)


# ==========================
# EJECUCIÓN
# ==========================

if __name__ == "__main__":
    subir_dataset()
