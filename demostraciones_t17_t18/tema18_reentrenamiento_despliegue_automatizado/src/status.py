from common import MODEL_NAME, client


def main():
    c = client()
    aliases = ["champion", "challenger", "previous_champion"]

    print("\n=== ESTADO DEL MODEL REGISTRY ===")
    for alias in aliases:
        try:
            version = c.get_model_version_by_alias(MODEL_NAME, alias)
            print(f"{alias:18s} -> versión {version.version}")
        except Exception:
            print(f"{alias:18s} -> no asignado")


if __name__ == "__main__":
    main()
