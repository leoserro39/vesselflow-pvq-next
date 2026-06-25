from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_DIR = PACKAGE_ROOT / "contracts"
DATA_DIR = PACKAGE_ROOT / "data"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_field_contract() -> list[dict[str, Any]]:
    return load_json(CONTRACTS_DIR / "field_contract.json")


def load_menus() -> dict[str, Any]:
    return load_json(CONTRACTS_DIR / "menus.json")


def load_operational_window() -> dict[str, Any]:
    return load_json(CONTRACTS_DIR / "operational_window.json")


def load_operational_state_rules() -> dict[str, Any]:
    return load_json(CONTRACTS_DIR / "operational_state_rules.json")


def load_madre_sample() -> dict[str, Any]:
    return load_json(DATA_DIR / "madre_nomination_core.sample.json")


def load_source_392() -> list[dict[str, Any]]:
    return load_json(DATA_DIR / "source_392_madre.sample.json")
