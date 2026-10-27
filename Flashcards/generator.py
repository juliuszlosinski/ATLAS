"""ATLAS Flashcards: generator page (flashcards from text with a local LLM, editing and study mode).

Opened through the navigation in app.py.
"""

import random
from dataclasses import dataclass
from pathlib import Path

import streamlit as st

import flashcards as fc
import ollama_models as om
import rag
import theme

CARD_FIELDS = ("question", "answer", "kind", "difficulty")


@dataclass
class Settings:
    model: str
    model_ready: bool
    per_chunk: int
    min_score: int
    chunk_size: int
    deck_name: str


@st.cache_data(ttl=30)
def installed_models() -> list[str]:
    return om.installed_models()


# --- Sidebar: settings ---------------------------------------------------------

def model_label(name: str, installed: list[str]) -> str:
    if om.is_installed(name, installed):
        return f"{name}  ·  pobrany"
    return f"{name}  ·  do pobrania, ~{om.download_size(name)}"


def download(name: str) -> None:
    bar = st.progress(0.0, text=f"Pobieram {name}…")
    for fraction, status in om.pull(name):
        bar.progress(fraction, text=f"Pobieram {name}: {status}")
    installed_models.clear()
    st.rerun()


def model_picker(label: str, default: str, installed: list[str], key: str, help: str) -> str:
    options = installed + [m for m in om.CATALOG if not om.is_installed(m, installed)]
    index = options.index(default) if default in options else 0
    name = st.selectbox(label, options, index=index, key=key, help=help,
                        format_func=lambda m: model_label(m, installed))
    if not om.is_installed(name, installed):
        st.warning(f"Model **{name}** nie jest pobrany (~{om.download_size(name)}). "
                   f"Pobierz go przyciskiem poniżej albo w terminalu:")
        st.code(f"ollama pull {name}", language="bash")
        if st.button(f"Pobierz {name}", key=f"pull_{key}", width="stretch"):
            download(name)
    return name


def sidebar_settings() -> Settings:
    with st.sidebar:
        st.header("Ustawienia")
        installed = installed_models()
        if not installed:
            st.error("Nie widzę Ollamy. Uruchom ją (ikona lamy przy zegarku) i odśwież stronę.")
            st.stop()
        model = model_picker("Model językowy", fc.MODEL, installed, key="model",
                             help="Tworzy fiszki i ocenia ich jakość. Mniejszy model jest szybszy, większy dokładniejszy.")
        st.divider()
        return Settings(
            model=model,
            model_ready=om.is_installed(model, installed),
            per_chunk=st.slider("Fiszek na fragment (maks.)", 1, 10, 5),
            min_score=st.slider("Minimalna ocena jakości", 1, 5, 4,
                                help="Model ocenia każdą fiszkę w skali 1-5; niżej ocenione zostaną odrzucone."),
            chunk_size=st.slider("Długość fragmentu (znaki)", 1000, 5000, 2500, step=500),
            deck_name=st.text_input("Nazwa talii w Anki", "ATLAS"),
        )


# --- Generate tab --------------------------------------------------------------

def source_text() -> str:
    source = st.radio("Źródło tekstu", ["Wklej tekst", "Wgraj plik"], horizontal=True)
    if source == "Wklej tekst":
        return st.text_area("Tekst", height=220, placeholder="Wklej notatki, artykuł, fragment podręcznika…")
    upload = st.file_uploader("Plik .txt, .docx lub .pdf", type=["txt", "docx", "pdf"])
    if not upload:
        return ""
    text = fc.text_from_bytes(upload.getvalue(), Path(upload.name).suffix.lower())
    if text:
        with st.expander(f"Podgląd tekstu ({len(text)} znaków)"):
            st.text(text[:3000] + ("…" if len(text) > 3000 else ""))
    return text


def build_index(text: str) -> "rag.Index | None":
    if not om.is_installed(rag.EMBED_MODEL, om.all_models()):
        st.info(f"Przycisk Wyjaśnij wymaga modelu {rag.EMBED_MODEL}. Pobierz go: ollama pull {rag.EMBED_MODEL}")
        return None
    with st.spinner("Buduję indeks do wyjaśnień…"):
        return rag.Index.build(fc.split_into_chunks(text, max_chars=rag.PASSAGE_CHARS))


def run_generation(text: str, settings: Settings) -> None:
    with st.status("Generuję fiszki…", expanded=True) as status:
        bar = st.progress(0.0)
        result = fc.generate_from_text(
            text, per_chunk=settings.per_chunk, min_score=settings.min_score, chunk_size=settings.chunk_size,
            model=settings.model,
            progress=lambda fraction, message: bar.progress(fraction, text=message),
        )
        for error in result.errors:
            st.warning(error)
        status.update(label=f"Gotowe: {len(result.accepted)} z {result.unique} fiszek zaakceptowanych",
                      state="complete", expanded=False)
    st.session_state.result = result
    st.session_state.study = None
    st.session_state.index = build_index(text)


def edited_cards(rows: list[dict]) -> tuple[list[fc.Flashcard], int]:
    """Kept rows of the editor as validated flashcards, plus the number of rows that no longer validate."""
    cards, invalid = [], 0
    for row in rows:
        if not row.get("zachowaj"):
            continue
        try:
            cards.append(fc.Flashcard(**{k: row[k] for k in CARD_FIELDS}))
        except Exception:
            invalid += 1
    return cards, invalid


def results(settings: Settings) -> None:
    result: fc.GenerationResult = st.session_state.result
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Fragmenty", result.chunks)
    c2.metric("Kandydaci", result.candidates)
    c3.metric("Unikalne", result.unique)
    c4.metric("Zaakceptowane", len(result.accepted))

    st.subheader("Zaakceptowane fiszki")
    st.caption("Możesz poprawić treść w tabeli i odznaczyć fiszki, których nie chcesz eksportować.")
    edited = st.data_editor(
        [{"zachowaj": True, **card.model_dump(), "ocena": verdict.score} for card, verdict in result.accepted],
        width="stretch",
        num_rows="dynamic",
        column_config={
            "zachowaj": st.column_config.CheckboxColumn("✓", width="small"),
            "question": st.column_config.TextColumn("Pytanie", width="large"),
            "answer": st.column_config.TextColumn("Odpowiedź", width="large"),
            "kind": st.column_config.SelectboxColumn("Typ", options=["definition", "fact", "concept", "example"]),
            "difficulty": st.column_config.SelectboxColumn("Trudność", options=["easy", "medium", "hard"]),
            "ocena": st.column_config.NumberColumn("Ocena", disabled=True, width="small"),
        },
        key="editor",
    )

    final, invalid = edited_cards(edited)
    if invalid:
        st.warning(f"{invalid} fiszek pominięto, bo po edycji nie spełniają zasad (np. puste pytanie).")
    st.session_state.final = final

    d1, d2 = st.columns(2)
    d1.download_button("Pobierz dla Anki (.txt)", disabled=not final,
                       data=fc.anki_text(final, settings.deck_name).encode("utf-8"),
                       file_name="flashcards_anki.txt", mime="text/plain")
    d2.download_button("Pobierz CSV", disabled=not final,
                       data=fc.csv_text(final).encode("utf-8-sig"),
                       file_name="flashcards.csv", mime="text/csv")

    if result.rejected:
        with st.expander(f"Odrzucone przy ocenie jakości ({len(result.rejected)})"):
            for card, verdict in result.rejected:
                st.markdown(f"**{card.question}**: {card.answer}  \n"
                            f"<small>ocena {verdict.score}: {verdict.reason}</small>", unsafe_allow_html=True)


def generate_tab(settings: Settings) -> None:
    text = source_text()
    if not settings.model_ready:
        st.info("Najpierw pobierz wybrany model (panel Ustawienia po lewej).")
    if st.button("Generuj fiszki", type="primary", disabled=not text.strip() or not settings.model_ready):
        run_generation(text, settings)
    if "result" in st.session_state:
        results(settings)


# --- Study tab -----------------------------------------------------------------

def new_study_session(size: int) -> dict:
    order = list(range(size))
    random.shuffle(order)
    return {"order": order, "pos": 0, "show": False, "known": 0}


def explain_box(card: fc.Flashcard, session: dict, model: str) -> None:
    index = st.session_state.get("index")
    if index is None:
        return
    cached = session.get("explanation")
    if cached and cached[0] == session["pos"]:
        _, text, passages = cached
    elif st.button("Wyjaśnij"):
        with st.spinner("Szukam w materiale i wyjaśniam…"):
            text, passages = rag.explain(card.question, card.answer, index, model=model)
        session["explanation"] = (session["pos"], text, passages)
    else:
        return
    st.markdown(text)
    with st.expander("Źródła z materiału"):
        for p in passages:
            st.markdown(f"**[{p.number}]** podobieństwo {p.score:.2f}")
            st.text(p.text)


def study_tab(settings: Settings) -> None:
    cards = st.session_state.get("final") or []
    if not cards:
        st.info("Najpierw wygeneruj fiszki w zakładce „Generuj”.")
        return

    session = st.session_state.get("study")
    # start again after a new generation or when the deck was edited in the table
    if session is None or len(session["order"]) != len(cards) or st.button("Potasuj i zacznij od nowa"):
        session = st.session_state.study = new_study_session(len(cards))

    total = len(session["order"])
    if session["pos"] >= total:
        st.success(f"Koniec talii! Znasz {session['known']} z {total} fiszek.")
        return

    card = cards[session["order"][session["pos"]]]
    st.progress(session["pos"] / total, text=f"Fiszka {session['pos'] + 1} z {total}")
    with st.container(border=True):
        st.markdown(f"### {card.question}")
        if session["show"]:
            st.markdown(f"**{card.answer}**")
            st.caption(f"{card.kind} · {card.difficulty}")
            explain_box(card, session, settings.model)

    if not session["show"]:
        if st.button("Pokaż odpowiedź", type="primary"):
            session["show"] = True
            st.rerun()
        return
    knew, did_not = st.columns(2)
    if knew.button("Wiem", width="stretch"):
        session.update(pos=session["pos"] + 1, show=False, known=session["known"] + 1)
        st.rerun()
    if did_not.button("Jeszcze nie", width="stretch"):
        session.update(pos=session["pos"] + 1, show=False)
        st.rerun()


# --- Page ----------------------------------------------------------------------

settings = sidebar_settings()
theme.page_header()
tab_make, tab_study = st.tabs(["Generuj", "Ucz się"])
with tab_make:
    generate_tab(settings)
with tab_study:
    study_tab(settings)
