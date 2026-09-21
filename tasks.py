"""Commandes de développement du monorepo."""

from pathlib import Path

from invoke import Context, task

ROOT = Path(__file__).parent
SHARED = ROOT / "packages" / "shared-models"
API_A = ROOT / "services" / "api-a"
API_B = ROOT / "services" / "api-b"


def _run_project(c: Context, project: Path, command: str) -> None:
    c.run(f"cd {project} && uv run {command}", pty=True)


@task
def install(c: Context) -> None:
    """Installe les environnements de tous les composants."""
    c.run(f"cd {ROOT} && uv sync", pty=True)
    for project in (SHARED, API_A, API_B):
        c.run(f"cd {project} && uv sync", pty=True)


@task
def test_shared(c: Context) -> None:
    """Exécute uniquement les tests de la librairie partagée."""
    _run_project(c, SHARED, "pytest")


@task(name="test-api-a")
def test_api_a(c: Context) -> None:
    """Exécute uniquement les tests de l'API A."""
    _run_project(c, API_A, "pytest")


@task(name="test-api-b")
def test_api_b(c: Context) -> None:
    """Exécute uniquement les tests de l'API B."""
    _run_project(c, API_B, "pytest")


@task
def test(c: Context) -> None:
    """Exécute la suite complète, projet par projet."""
    test_shared(c)
    test_api_a(c)
    test_api_b(c)


@task
def lint(c: Context) -> None:
    """Vérifie tous les fichiers Python avec Ruff."""
    c.run("uv run ruff check .", pty=True)


@task
def format(c: Context) -> None:
    """Formate tous les fichiers Python avec Ruff."""
    c.run("uv run ruff format .", pty=True)


@task(name="dev-api-a")
def dev_api_a(c: Context) -> None:
    """Démarre l'API A avec rechargement du code local et partagé."""
    _run_project(
        c,
        API_A,
        "uvicorn api_a.main:app --host 0.0.0.0 --port 8001 --reload "
        "--reload-dir src --reload-dir ../../packages/shared-models/src",
    )


@task(name="dev-api-b")
def dev_api_b(c: Context) -> None:
    """Démarre l'API B avec rechargement du code local et partagé."""
    _run_project(
        c,
        API_B,
        "uvicorn api_b.main:app --host 0.0.0.0 --port 8002 --reload "
        "--reload-dir src --reload-dir ../../packages/shared-models/src",
    )


@task(name="docker-build")
def docker_build(c: Context) -> None:
    """Construit les deux images de développement."""
    c.run("docker compose build", pty=True)


@task(name="docker-up")
def docker_up(c: Context) -> None:
    """Démarre les deux API en arrière-plan."""
    c.run("docker compose up -d", pty=True)


@task(name="docker-down")
def docker_down(c: Context) -> None:
    """Arrête les services Docker."""
    c.run("docker compose down", pty=True)


@task(name="docker-logs")
def docker_logs(c: Context) -> None:
    """Suit les logs des API."""
    c.run("docker compose logs -f", pty=True)


@task(name="docker-test")
def docker_test(c: Context) -> None:
    """Lance les tests dans les conteneurs."""
    c.run("docker compose run --rm api-a uv run pytest", pty=True)
    c.run("docker compose run --rm api-b uv run pytest", pty=True)
