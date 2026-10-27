"""Local Ollama models: which are installed, which we recommend, and downloading them."""

from collections.abc import Iterator

import ollama

# Recommended text models from the Ollama library, with their approximate download size
CATALOG = {
    "qwen2.5:1.5b": "1,0 GB",
    "qwen2.5:3b": "1,9 GB",
    "qwen2.5:7b": "4,7 GB",
    "qwen3:4b": "2,6 GB",
    "llama3.2:3b": "2,0 GB",
    "llama3.1:8b": "4,9 GB",
    "gemma3:4b": "3,3 GB",
    "mistral:7b": "4,1 GB",
    "phi4-mini": "2,5 GB",
}


EMBEDDING_MODELS = ("bge-m3", "nomic-embed-text", "mxbai-embed-large")


def is_embedding_model(name: str) -> bool:
    return "embed" in name or name.split(":")[0] in EMBEDDING_MODELS


def all_models() -> list[str]:
    """Every model in the local Ollama; [] when Ollama is not running."""
    try:
        return [m.model for m in ollama.list().models]
    except Exception:
        return []


def installed_models() -> list[str]:
    """Chat models only: embedding models cannot write flashcards."""
    return [n for n in all_models() if not is_embedding_model(n)]


def is_installed(name: str, installed: list[str]) -> bool:
    # Ollama lists untagged models as "<name>:latest"
    return name in installed or f"{name}:latest" in installed


def download_size(name: str) -> str:
    return CATALOG.get(name, "?")


def pull(name: str) -> Iterator[tuple[float, str]]:
    """Download a model, yielding (fraction done, status) as layers arrive."""
    for part in ollama.pull(name, stream=True):
        if part.total:
            yield min(part.completed / part.total, 1.0), part.status
