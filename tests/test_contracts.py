from pvq_next.validate_contracts import validate


def test_contracts_are_valid():
    result = validate()
    assert result["ok"], result["errors"]
    assert result["counts"]["fields"] == 75
    assert result["counts"]["source_392"] == 392
