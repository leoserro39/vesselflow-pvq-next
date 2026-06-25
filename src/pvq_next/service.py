from __future__ import annotations

import re
import unicodedata
from typing import Any

from .loader import (
    load_field_contract,
    load_madre_sample,
    load_menus,
    load_operational_state_rules,
    load_operational_window,
    load_source_392,
)


BLOCKING_OR_POTENTIAL_BLOCKING_VALUES = {"Sim", "Potencial"}
SYSTEM_REVIEW_ROUTE = "AUTO_SYSTEM_RULE"


def _area_id(area_name: str) -> str:
    normalized = unicodedata.normalize("NFKD", area_name)
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")


def _area_payload(area_name: str, fields: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "area_id": _area_id(area_name),
        "area_name": area_name,
        "fields": fields,
        "field_count": len(fields),
        "review_required_count": sum(
            field["review_route"] != SYSTEM_REVIEW_ROUTE for field in fields
        ),
        "blocking_or_potential_blocking_count": sum(
            field["blocks_nomination"] in BLOCKING_OR_POTENTIAL_BLOCKING_VALUES
            for field in fields
        ),
    }


def _area_payloads() -> list[dict[str, Any]]:
    grouped_fields: dict[str, list[dict[str, Any]]] = {}
    for field in load_field_contract():
        grouped_fields.setdefault(field["area"], []).append(field)
    return [_area_payload(area_name, fields) for area_name, fields in grouped_fields.items()]


def health() -> dict[str, Any]:
    fields = load_field_contract()
    return {
        "service": "pvq-next-operational-state",
        "status": "ok",
        "mode": "read_only",
        "field_count": len(fields),
    }


def summary(state_id: str) -> dict[str, Any]:
    sample = load_madre_sample()
    return {
        "state_id": state_id,
        "vessel": sample["vessel"],
        "operational_window": sample["operational_window"],
        "operational_state": sample["operational_state"],
        "counts": {
            "nomination_core_fields": len(sample["nomination_core"]),
            "source_archive_fields": len(load_source_392()),
        },
    }


def nomination_core(state_id: str) -> dict[str, Any]:
    sample = load_madre_sample()
    return {
        "state_id": state_id,
        "fields": sample["nomination_core"],
    }


def operational_state(state_id: str) -> dict[str, Any]:
    sample = load_madre_sample()
    return {
        "state_id": state_id,
        "operational_state": sample["operational_state"],
        "rules": load_operational_state_rules(),
    }


def evidence(state_id: str) -> dict[str, Any]:
    fields = load_field_contract()
    return {
        "state_id": state_id,
        "evidence": [
            {
                "field_id": item["field_id"],
                "answer": item["answer"],
                "evidence_trace": item["evidence_trace"],
                "evidence_type": item["evidence_type"],
                "confidence": item["confidence"],
                "review_route": item["review_route"],
            }
            for item in fields
        ],
    }


def full_archive(state_id: str) -> dict[str, Any]:
    return {
        "state_id": state_id,
        "source_392": load_source_392(),
    }


def areas(state_id: str) -> dict[str, Any]:
    area_payloads = _area_payloads()
    return {
        "state_id": state_id,
        "areas": area_payloads,
        "area_count": len(area_payloads),
    }


def area(state_id: str, area_id: str) -> dict[str, Any] | None:
    for area_payload in _area_payloads():
        if area_payload["area_id"] == area_id:
            return {
                "state_id": state_id,
                **area_payload,
            }
    return None


def menus() -> dict[str, Any]:
    return load_menus()


def operational_window() -> dict[str, Any]:
    return load_operational_window()
