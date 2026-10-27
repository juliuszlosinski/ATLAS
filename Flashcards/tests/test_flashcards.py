"""Tests of the flashcard logic with the LLM replaced by a fake, so they run without Ollama.

    python -m unittest discover tests
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import flashcards as fc  # noqa: E402
import ollama_models as om  # noqa: E402


def card(question: str, answer: str = "odpowiedź") -> fc.Flashcard:
    return fc.Flashcard(question=question, answer=answer, kind="fact", difficulty="easy")


def reply(payload: dict) -> SimpleNamespace:
    """Shape of an ollama.chat() response: response.message.content."""
    return SimpleNamespace(message=SimpleNamespace(content=json.dumps(payload)))


class FakeChat:
    """Answers generation calls with the given decks (one per chunk) and review calls with fixed scores."""

    def __init__(self, decks: list, scores: dict[str, int]):
        self.decks = list(decks)
        self.scores = scores
        self.models: list[str] = []

    def __call__(self, model, messages, format, options):
        self.models.append(model)
        if "flashcards" in format["properties"]:
            deck = self.decks.pop(0)
            if isinstance(deck, Exception):
                raise deck
            return reply({"flashcards": [c.model_dump() for c in deck]})
        question = messages[-1]["content"].split("Question: ")[1].split("\n")[0]
        score = self.scores[question]
        if score is None:
            raise RuntimeError("timeout")
        return reply({"score": score, "reason": "ok"})


class SplitIntoChunksTest(unittest.TestCase):
    def test_keeps_whole_paragraphs_within_limit(self):
        text = "\n".join(f"akapit {i} " + "x" * 30 for i in range(10))
        chunks = fc.split_into_chunks(text, max_chars=100)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(c) <= 100 for c in chunks))
        self.assertEqual(" ".join(chunks).split(), text.split())

    def test_empty_text_gives_no_chunks(self):
        self.assertEqual(fc.split_into_chunks("\n\n"), [])


class DeduplicateTest(unittest.TestCase):
    def test_removes_near_identical_questions(self):
        cards = [card("Gdzie zachodzi fotosynteza?"), card("Gdzie zachodzi fotosynteza ?"), card("Co to jest LLM?")]
        self.assertEqual([c.question for c in fc.deduplicate(cards)],
                         ["Gdzie zachodzi fotosynteza?", "Co to jest LLM?"])


class GenerateFromTextTest(unittest.TestCase):
    def test_accepts_and_rejects_by_score(self):
        fake = FakeChat(decks=[[card("Pytanie dobre?"), card("Pytanie słabe?")]],
                        scores={"Pytanie dobre?": 5, "Pytanie słabe?": 2})
        with patch.object(fc, "chat", fake):
            result = fc.generate_from_text("Jakiś tekst.", min_score=4)
        self.assertEqual([c.question for c, _ in result.accepted], ["Pytanie dobre?"])
        self.assertEqual([c.question for c, _ in result.rejected], ["Pytanie słabe?"])
        self.assertEqual((result.chunks, result.candidates, result.unique), (1, 2, 2))

    def test_one_model_writes_and_reviews(self):
        fake = FakeChat(decks=[[card("Pytanie A?")]], scores={"Pytanie A?": 5})
        with patch.object(fc, "chat", fake):
            fc.generate_from_text("Tekst.", model="wybrany")
        self.assertEqual(fake.models, ["wybrany", "wybrany"])

    def test_failing_chunk_and_review_do_not_stop_the_run(self):
        text = "A" * 30 + "\n" + "B" * 30
        fake = FakeChat(decks=[ValueError("zły JSON"), [card("Czym jest Ollama?"), card("Na jakim porcie działa API?")]],
                        scores={"Czym jest Ollama?": None, "Na jakim porcie działa API?": 5})
        with patch.object(fc, "chat", fake):
            result = fc.generate_from_text(text, chunk_size=40, min_score=1)
        self.assertEqual(len(result.errors), 1)
        self.assertIn("Fragment 1", result.errors[0])
        # a failed review is rejected even when the threshold would accept score 1
        self.assertEqual([c.question for c, _ in result.rejected], ["Czym jest Ollama?"])
        self.assertEqual([c.question for c, _ in result.accepted], ["Na jakim porcie działa API?"])

    def test_reports_progress_up_to_100_percent(self):
        fake = FakeChat(decks=[[card("Pytanie A?")]], scores={"Pytanie A?": 5})
        seen = []
        with patch.object(fc, "chat", fake):
            fc.generate_from_text("Tekst.", progress=lambda fraction, message: seen.append(fraction))
        self.assertEqual(seen, sorted(seen))
        self.assertEqual(seen[-1], 1.0)


class ExportTest(unittest.TestCase):
    cards = [card("Gdzie zachodzi fotosynteza?", "W chloroplastach"), card('Co to jest; "LLM"?', "Model")]

    def test_anki_text_has_header_and_one_line_per_card(self):
        lines = fc.anki_text(self.cards, deck="Biologia").splitlines()
        self.assertEqual(lines[:4], ["#separator:tab", "#html:false", "#deck:Biologia", "#tags column:3"])
        self.assertEqual(lines[4], "Gdzie zachodzi fotosynteza?\tW chloroplastach\tfact easy")
        self.assertEqual(len(lines), 6)

    def test_csv_file_has_bom_and_quotes_special_characters(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.csv"
            fc.export_csv(self.cards, str(path))
            data = path.read_bytes()
        self.assertTrue(data.startswith(b"\xef\xbb\xbf"))
        self.assertNotIn(b"\r\r\n", data)
        self.assertIn('"Co to jest; ""LLM""?"', data.decode("utf-8-sig"))


class TextFromBytesTest(unittest.TestCase):
    def test_txt_normalizes_windows_newlines(self):
        self.assertEqual(fc.text_from_bytes("a\r\nb\rc".encode(), ".txt"), "a\nb\nc")


class OllamaModelsTest(unittest.TestCase):
    def test_untagged_model_matches_latest(self):
        self.assertTrue(om.is_installed("phi4-mini", ["phi4-mini:latest"]))
        self.assertFalse(om.is_installed("qwen2.5:7b", ["qwen2.5:3b"]))


if __name__ == "__main__":
    unittest.main()
