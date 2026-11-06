from common import DB_PATH, MODEL_NAME, get_alias_version


def main():
    print("\n=== ESTADO DEL MODEL REGISTRY ===")
    print(f"Base MLflow local: {DB_PATH}")

    found_any = False

    for alias in ["champion", "challenger", "previous_champion"]:
        version = get_alias_version(alias)
        if version is None:
            print(f"{alias:18s} -> no asignado")
        else:
            found_any = True
            print(f"{alias:18s} -> versión {version.version}")

    if not found_any:
        print("\nNo existe todavía un modelo registrado con aliases para esta práctica.")
        print("Antes de ejecutar monitor.py debes crear el champion inicial:")
        print("")
        print("  python data/generate_data.py")
        print("  python src/bootstrap.py")
        print("  python src/status.py")
    else:
        champion = get_alias_version("champion")
        if champion is None:
            print("\nATENCIÓN: existen datos en el Registry, pero no hay alias champion.")
            print("Vuelve a crear o asignar el champion antes de monitorizar.")
        else:
            print("\nEstado correcto para monitoreo: existe un alias champion.")


if __name__ == "__main__":
    main()
