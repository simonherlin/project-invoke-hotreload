"""Modèles Pydantic exposés par les API."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ItemStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class Item(BaseModel):
    """Contrat volontairement partagé : toute modification apparaît dans /docs."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., gt=0, description="Identifiant unique")
    name: str = Field(..., min_length=1, description="Nom lisible")
    description: str | None = Field(default=None, description="Description optionnelle")
    status: ItemStatus = Field(default=ItemStatus.ACTIVE)


class ServiceInfo(BaseModel):
    name: str
    version: str
    description: str
