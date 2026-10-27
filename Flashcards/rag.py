"""Plain RAG over the study material: an in-memory embedding index and grounded explanations.

Retrieval always runs exactly once per question (no agent loop): search, then answer from the found passages.
"""

from dataclasses import dataclass

import numpy as np
from ollama import chat, embed

EMBED_MODEL = "bge-m3"  # multilingual embedding model, works well for Polish
PASSAGE_CHARS = 800     # retrieval works better on smaller pieces than generation chunks


@dataclass
class Passage:
    number: int
    text: str
    score: float


class Index:
    """Passages of the material with their normalized embedding vectors."""

    def __init__(self, passages: list[str], vectors: np.ndarray):
        self.passages = passages
        self.vectors = vectors

    @classmethod
    def build(cls, passages: list[str], model: str = EMBED_MODEL, batch: int = 16) -> "Index":
        vectors = []
        for i in range(0, len(passages), batch):
            vectors += embed(model=model, input=passages[i:i + batch]).embeddings
        return cls(passages, _normalize(np.array(vectors, dtype=np.float32)))

    def search(self, query: str, k: int = 3, model: str = EMBED_MODEL) -> list[Passage]:
        query_vector = _normalize(np.array(embed(model=model, input=query).embeddings, dtype=np.float32))[0]
        scores = self.vectors @ query_vector  # cosine similarity, vectors are normalized
        best = np.argsort(-scores)[:k]
        return [Passage(n, self.passages[i], float(scores[i])) for n, i in enumerate(best, 1)]


def _normalize(vectors: np.ndarray) -> np.ndarray:
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


# In Polish on purpose: small models answer in the language of the prompt
EXPLAIN_PROMPT = """Wyjaśniasz studentowi fiszkę do nauki. Odpowiadaj po polsku.
Korzystaj tylko z ponumerowanych fragmentów materiału poniżej i powołuj się na nie jako [1] lub [2].
Jeśli fragmenty naprawdę nie dotyczą tematu, napisz to zamiast zgadywać.
Odpowiedz w 3-5 zdaniach."""


def explain(question: str, answer: str, index: Index, model: str, k: int = 3) -> tuple[str, list[Passage]]:
    passages = index.search(f"{question} {answer}", k=k)
    context = "\n\n".join(f"[{p.number}] {p.text}" for p in passages)
    response = chat(
        model=model,
        messages=[
            {"role": "system", "content": EXPLAIN_PROMPT},
            {"role": "user", "content": f"Fragmenty:\n{context}\n\nPytanie z fiszki: {question}\nOdpowiedź: {answer}"},
        ],
        options={"temperature": 0.2},
    )
    return response.message.content, passages
