"""ATLAS Flashcards: study flashcards generated from documents with a local LLM (Ollama).

Pipeline: text, chunks, LLM flashcards (JSON), deduplication, LLM review, export.
The Streamlit pages and the command line both use generate_from_text().

Usage:
    python flashcards.py <file.txt|.docx|.pdf>
"""

import csv
import io
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Literal

import docx2txt
from ollama import chat
from pydantic import BaseModel, Field
from pypdf import PdfReader

MODEL = "qwen2.5:3b"  # one language model both writes and reviews the flashcards
SYSTEM_PROMPT = """
You create study flashcards from the given text. Rules:
- one flashcard = one piece of information,
- the question must make sense on its own (never write "in the text" or "according to the author"),
- the answer is short: a word, a number or one sentence,
- use only information present in the text, never add your own,
- write in the same language as the text.
"""


class Flashcard(BaseModel):
    question: str = Field(min_length=5, max_length=200)
    answer: str = Field(min_length=1, max_length=300)
    kind: Literal["definition", "fact", "concept", "example"]
    difficulty: Literal["easy", "medium", "hard"]


class Deck(BaseModel):
    flashcards: list[Flashcard]


class Review(BaseModel):
    score: int = Field(ge=1, le=5)
    reason: str


# --- Input -------------------------------------------------------------------

def text_from_bytes(data: bytes, suffix: str) -> str:
    """Extract text from file content; the suffix (".docx", ".pdf", other) picks the reader."""
    if suffix == ".docx":
        return docx2txt.process(io.BytesIO(data))
    if suffix == ".pdf":
        return "\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(data)).pages)
    # same newline handling as reading the file in text mode
    return data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")


def load_text(path: str) -> str:
    p = Path(path)
    return text_from_bytes(p.read_bytes(), p.suffix.lower())


def split_into_chunks(text: str, max_chars: int = 2500) -> list[str]:
    """Split on paragraph boundaries so that no idea is cut in half."""
    chunks, current = [], ""
    for paragraph in text.split("\n"):
        if len(current) + len(paragraph) > max_chars and current:
            chunks.append(current.strip())
            current = ""
        current += paragraph + "\n"
    if current.strip():
        chunks.append(current.strip())
    return chunks


# --- LLM calls -----------------------------------------------------------------

def flashcards_from_chunk(text: str, count: int = 5, model: str | None = None) -> list[Flashcard]:
    response = chat(
        model=model or MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Create up to {count} flashcards from this text:\n\n{text}"},
        ],
        format=Deck.model_json_schema(),
        options={"temperature": 0.2},
    )
    return Deck.model_validate_json(response.message.content).flashcards


def review(card: Flashcard, source: str, model: str | None = None) -> Review:
    response = chat(
        model=model or MODEL,
        messages=[{"role": "user", "content":
            "Rate this flashcard from 1 to 5: is it correct according to the source text, "
            "unambiguous, and about a single piece of information?\n\n"
            f"Source: {source}\n\nQuestion: {card.question}\nAnswer: {card.answer}"}],
        format=Review.model_json_schema(),
        options={"temperature": 0},
    )
    return Review.model_validate_json(response.message.content)


# --- Pipeline ------------------------------------------------------------------

def normalize(s: str) -> str:
    return re.sub(r"[^\w ]", "", s.lower()).strip()


def deduplicate(cards: list[Flashcard], threshold: float = 0.85) -> list[Flashcard]:
    unique: list[Flashcard] = []
    for card in cards:
        if all(SequenceMatcher(None, normalize(card.question), normalize(u.question)).ratio() < threshold
               for u in unique):
            unique.append(card)
    return unique


@dataclass
class GenerationResult:
    chunks: int = 0
    candidates: int = 0
    unique: int = 0
    accepted: list[tuple[Flashcard, Review]] = field(default_factory=list)
    rejected: list[tuple[Flashcard, Review]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


ProgressFn = Callable[[float, str], None]


def generate_from_text(text: str, per_chunk: int = 5, min_score: int = 4, chunk_size: int = 2500,
                       model: str | None = None, progress: ProgressFn | None = None) -> GenerationResult:
    """Run the whole pipeline. A failing chunk or review is recorded instead of stopping the run.

    progress(fraction, message) is called as the work advances: generation takes 0-50 %, review 50-100 %.
    """
    report = progress or (lambda fraction, message: None)
    result = GenerationResult()

    chunks = split_into_chunks(text, max_chars=chunk_size)
    result.chunks = len(chunks)
    candidates: list[tuple[Flashcard, str]] = []
    for i, chunk in enumerate(chunks, 1):
        report((i - 1) / len(chunks) * 0.5, f"Fragment {i}/{len(chunks)}: tworzę fiszki")
        try:
            candidates += [(card, chunk) for card in flashcards_from_chunk(chunk, count=per_chunk, model=model)]
        except Exception as e:  # invalid JSON from the model, Ollama not running, ...
            result.errors.append(f"Fragment {i}: pominięty ({e})")
    result.candidates = len(candidates)

    unique = deduplicate([card for card, _ in candidates])
    result.unique = len(unique)
    sources = {id(card): chunk for card, chunk in candidates}
    report(0.5, f"{len(candidates)} kandydatów, {len(unique)} po usunięciu duplikatów. Oceniam jakość…")

    for j, card in enumerate(unique, 1):
        try:
            verdict = review(card, sources[id(card)], model=model)
        except Exception as e:
            result.rejected.append((card, Review(score=1, reason=f"Błąd oceny: {e}")))
        else:
            (result.accepted if verdict.score >= min_score else result.rejected).append((card, verdict))
        report(0.5 + j / len(unique) * 0.5, f"Ocena {j}/{len(unique)}")

    report(1.0, f"Gotowe: {len(result.accepted)} z {len(unique)} fiszek zaakceptowanych")
    return result


# --- Export --------------------------------------------------------------------

def anki_text(cards: list[Flashcard], deck: str = "ATLAS") -> str:
    """Plain-text format for Anki (menu File, option Import)."""
    lines = [f"#separator:tab\n#html:false\n#deck:{deck}\n#tags column:3\n"]
    lines += [f"{c.question}\t{c.answer}\t{c.kind} {c.difficulty}\n" for c in cards]
    return "".join(lines)


def csv_text(cards: list[Flashcard]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=";")
    writer.writerow(["question", "answer", "kind", "difficulty"])
    writer.writerows([c.question, c.answer, c.kind, c.difficulty] for c in cards)
    return buffer.getvalue()


def export_anki(cards: list[Flashcard], path: str, deck: str = "ATLAS") -> None:
    Path(path).write_text(anki_text(cards, deck), encoding="utf-8")


def export_csv(cards: list[Flashcard], path: str) -> None:
    # utf-8-sig makes Excel display non-ASCII characters; newline="" keeps csv's own \r\n line endings
    Path(path).write_text(csv_text(cards), encoding="utf-8-sig", newline="")


# --- Command line --------------------------------------------------------------

def generate(path: str, min_score: int = 4) -> list[Flashcard]:
    result = generate_from_text(load_text(path), min_score=min_score,
                                progress=lambda fraction, message: print(f"  [{fraction:4.0%}] {message}"))
    for error in result.errors:
        print(error)
    for card, verdict in result.rejected:
        print(f"Rejected ({verdict.score}): {card.question} | {verdict.reason}")
    print(f"Result: {result.candidates} candidates: {result.unique} unique: {len(result.accepted)} accepted")
    return [card for card, _ in result.accepted]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python flashcards.py <file.txt|.docx|.pdf>")
    cards = generate(sys.argv[1])
    export_anki(cards, "flashcards_anki.txt")
    export_csv(cards, "flashcards.csv")
