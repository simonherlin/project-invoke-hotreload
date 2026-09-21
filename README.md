# Invoke + FastAPI + uv : démonstrateur de hot-reload

Ce dépôt est un exemple complet d'architecture Python composée de deux API
indépendantes et d'une librairie partagée. Chaque composant possède son
`pyproject.toml`, ses dépendances et ses tests. `uv` gère les environnements,
`ruff` la qualité du code et `Invoke` fournit une interface unique.

## Prérequis

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Docker et Docker Compose (pour le mode conteneurisé)

## Démarrage rapide sans Docker

```bash
uv sync
uv run invoke install
uv run invoke test
```

Lancer les deux serveurs dans deux terminaux :

```bash
uv run invoke dev-api-a   # http://localhost:8001/docs
uv run invoke dev-api-b   # http://localhost:8002/docs
```

Les processus Uvicorn surveillent à la fois le code de l'API et celui de
`packages/shared-models`. Modifiez par exemple `Item` dans
`packages/shared-models/src/shared_models/models.py`, sauvegardez, puis rechargez
Swagger : le schéma OpenAPI reflète le champ sans reconstruire l'image.

## Démarrage avec Docker

```bash
uv run invoke docker-build
uv run invoke docker-up
```

Les URLs sont les mêmes (`8001` et `8002`). Les volumes montent le dépôt dans
`/workspace` et les commandes de développement utilisent `--reload`.

```bash
uv run invoke docker-logs       # suivre les logs
uv run invoke docker-test       # tests dans des conteneurs éphémères
uv run invoke docker-down
```

## Tâches Invoke

| Commande | Rôle |
|---|---|
| `uv run invoke test` | tests de la librairie et des deux API |
| `uv run invoke test-shared` | tests de `shared-models` uniquement |
| `uv run invoke test-api-a` / `test-api-b` | tests d'une API uniquement |
| `uv run invoke lint` | `ruff check` sur tous les composants |
| `uv run invoke format` | formatage Ruff |
| `uv run invoke dev-api-a` / `dev-api-b` | serveur local avec hot-reload |
| `uv run invoke docker-build` | construit les deux images |
| `uv run invoke docker-up` / `docker-down` | démarre/arrête Compose |

Chaque test peut aussi être lancé directement depuis son projet :

```bash
cd services/api-a && uv run pytest
cd packages/shared-models && uv run pytest
```

## Organisation

```text
packages/shared-models/   # contrat Pydantic partagé + tests
services/api-a/           # API catalogue, port 8001 + tests
services/api-b/           # API commandes, port 8002 + tests
tasks.py                  # façade Invoke
docker-compose.yml        # deux services de développement
```

