import json

from common import MODEL_NAME, REPORTS_DIR, client, write_json


def main():
    report_path = REPORTS_DIR / "staging_report.json"
    if not report_path.exists():
        raise FileNotFoundError("Falta staging_report.json. Ejecuta primero staging_validate.py")

    report = json.loads(report_path.read_text(encoding="utf-8"))
    if not report.get("passed"):
        print("El challenger NO pasó staging. El champion actual se conserva.")
        return

    c = client()
    current_champion = c.get_model_version_by_alias(MODEL_NAME, "champion")
    challenger = c.get_model_version_by_alias(MODEL_NAME, "challenger")

    c.set_registered_model_alias(MODEL_NAME, "previous_champion", current_champion.version)
    c.set_registered_model_alias(MODEL_NAME, "champion", challenger.version)
    c.set_model_version_tag(MODEL_NAME, challenger.version, "role", "champion")
    c.set_model_version_tag(MODEL_NAME, challenger.version, "promotion_status", "promoted")
    c.set_model_version_tag(MODEL_NAME, current_champion.version, "role", "previous_champion")

    payload = {
        "previous_champion_version": str(current_champion.version),
        "new_champion_version": str(challenger.version),
        "source_alias": "challenger",
        "result": "PROMOTED",
    }
    write_json(REPORTS_DIR / "promotion.json", payload)

    print("\n=== PROMOCIÓN COMPLETADA ===")
    print(f"Champion anterior: versión {current_champion.version}")
    print(f"Nuevo champion:     versión {challenger.version}")
    print("Alias previous_champion asignado a la versión anterior.")


if __name__ == "__main__":
    main()
