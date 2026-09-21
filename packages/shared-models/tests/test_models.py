import pytest
from pydantic import ValidationError

from shared_models import Item, ItemStatus


def test_item_serializes_shared_contract() -> None:
    item = Item(id=1, name="Demo")

    assert item.model_dump() == {
        "id": 1,
        "name": "Demo",
        "description": None,
        "status": ItemStatus.ACTIVE,
    }


def test_item_rejects_non_positive_id() -> None:
    with pytest.raises(ValidationError):
        Item(id=0, name="Invalid")
