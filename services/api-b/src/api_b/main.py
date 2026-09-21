from fastapi import FastAPI
from shared_models import Item, ServiceInfo

app = FastAPI(
    title="Orders API",
    version="0.1.0",
    description="API B indépendante qui consomme le package shared-models.",
)


@app.get("/health", response_model=ServiceInfo, tags=["system"])
def health() -> ServiceInfo:
    return ServiceInfo(
        name="orders-api",
        version="0.1.0",
        description="Service commandes disponible",
    )


@app.get("/api/v1/orders/{order_id}", response_model=Item, tags=["orders"])
def get_order(order_id: int) -> Item:
    return Item(
        id=order_id,
        name=f"Order {order_id}",
        description="Objet fourni par l'API commandes",
    )
