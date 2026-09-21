from fastapi import FastAPI
from shared_models import Item, ServiceInfo

app = FastAPI(
    title="Catalog API",
    version="0.1.0",
    description="API A indépendante qui consomme le package shared-models.",
)


@app.get("/health", response_model=ServiceInfo, tags=["system"])
def health() -> ServiceInfo:
    return ServiceInfo(
        name="catalog-api",
        version="0.1.0",
        description="Service catalogue disponible",
    )


@app.get("/api/v1/items/{item_id}", response_model=Item, tags=["catalog"])
def get_item(item_id: int) -> Item:
    return Item(
        id=item_id,
        name=f"Item {item_id}",
        description="Objet fourni par l'API catalogue",
    )
