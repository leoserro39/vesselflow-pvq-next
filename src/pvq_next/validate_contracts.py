from __future__ import annotations

from .loader import (
    load_field_contract,
    load_madre_sample,
    load_menus,
    load_operational_state_rules,
    load_operational_window,
    load_source_392,
)


REQUIRED_FIELD_KEYS = {
    "field_id",
    "question",
    "answer",
    "field_type",
    "input_control",
    "menu_name",
    "required",
    "blocks_nomination",
    "review_route",
    "evidence_trace",
    "backend_field",
}


def validate() -> dict:
    fields = load_field_contract()
    menus = load_menus()
    window = load_operational_window()
    rules = load_operational_state_rules()
    sample = load_madre_sample()
    source_392 = load_source_392()

    errors: list[str] = []

    if len(fields) != 75:
        errors.append(f"Expected 75 field contract rows, got {len(fields)}")

    for idx, field in enumerate(fields, start=1):
        missing = REQUIRED_FIELD_KEYS - set(field)
        if missing:
            errors.append(f"Field row {idx} missing keys: {sorted(missing)}")
        if not field.get("field_id"):
            errors.append(f"Field row {idx} has empty field_id")
        if not field.get("backend_field"):
            errors.append(f"Field row {idx} has empty backend_field")

    if window.get("date_format") != "MM/DD/YYYY":
        errors.append("Operational window date_format must be MM/DD/YYYY")

    if len(source_392) != 392:
        errors.append(f"Expected 392 source archive rows, got {len(source_392)}")

    if sample.get("operational_state", {}).get("final_operational_state") != "PRE_APT_WITH_TECHNICAL_REVIEW":
        errors.append("MADRE sample final state must be PRE_APT_WITH_TECHNICAL_REVIEW")

    return {
        "ok": not errors,
        "errors": errors,
        "counts": {
            "fields": len(fields),
            "menus": len(menus),
            "source_392": len(source_392),
            "controlled_reviews": len(sample.get("operational_state", {}).get("controlled_review_items", [])),
            "statuses": len(rules.get("final_statuses", {})),
        },
    }


def main() -> None:
    result = validate()
    print(result)
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
