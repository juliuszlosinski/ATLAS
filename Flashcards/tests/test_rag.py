"""Tests of rag.py with fake embedding and chat models, so they run without Ollama.

    python -m unittest discover tests
"""

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import ollama_models as om  # noqa: E402
import rag  # noqa: E402


def fake_embed(model, input):
    """Two "meanings": succulents/drought and trees; everything else lands far from both."""
    texts = [input] if isinstance(input, str) else input

    def vector(text):
        t = text.lower()
        return [float("aloes" in t or "susz" in t), float("dąb" in t or "drzew" in t), 0.1]
    return SimpleNamespace(embeddings=[vector(t) for t in texts])


PASSAGES = ["Dąb to drzewo liściaste.", "Aloes magazynuje wodę.", "Kurs złotego spadł."]


class IndexTest(unittest.TestCase):
    def test_finds_passage_by_meaning(self):
        with patch.object(rag, "embed", fake_embed):
            index = rag.Index.build(PASSAGES)
            hits = index.search("roślina, która przetrwa suszę", k=1)
        self.assertEqual(hits[0].text, "Aloes magazynuje wodę.")

    def test_builds_in_batches(self):
        calls = []

        def counting_embed(model, input):
            calls.append(len(input))
            return fake_embed(model, input)

        with patch.object(rag, "embed", counting_embed):
            index = rag.Index.build([f"fragment {i}" for i in range(5)], batch=2)
        self.assertEqual(calls, [2, 2, 1])
        self.assertEqual(index.vectors.shape, (5, 3))


class ExplainTest(unittest.TestCase):
    def test_sends_numbered_passages_in_polish_and_returns_answer(self):
        sent = {}

        def fake_chat(model, messages, options):
            sent["system"] = messages[0]["content"]
            sent["user"] = messages[-1]["content"]
            return SimpleNamespace(message=SimpleNamespace(content="Aloes gromadzi wodę [1]."))

        with patch.object(rag, "embed", fake_embed), patch.object(rag, "chat", fake_chat):
            index = rag.Index.build(PASSAGES)
            text, passages = rag.explain("Jak aloes znosi suszę?", "Magazynuje wodę", index, model="test", k=2)
        self.assertEqual(text, "Aloes gromadzi wodę [1].")
        self.assertIn("[1] Aloes magazynuje wodę.", sent["user"])
        self.assertIn("Odpowiadaj po polsku", sent["system"])
        self.assertEqual(len(passages), 2)


class EmbeddingModelsTest(unittest.TestCase):
    def test_embedding_models_are_not_offered_as_language_models(self):
        self.assertTrue(om.is_embedding_model("bge-m3:latest"))
        self.assertTrue(om.is_embedding_model("nomic-embed-text"))
        self.assertFalse(om.is_embedding_model("qwen2.5:3b"))


if __name__ == "__main__":
    unittest.main()
