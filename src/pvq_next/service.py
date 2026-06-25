from __future__ import annotations

from typing import Any

from .loader import (
    load_field_contract,
    load_madre_sample,
    load_menus,
    load_operational_state_rules,
    load_operational_window,
    load_source_392,
)


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


def menus() -> dict[str, Any]:
    return load_menus()


def operational_window() -> dict[str, Any]:
    return load_operational_window()
