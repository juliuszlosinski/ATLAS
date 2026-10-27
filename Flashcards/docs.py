"""ATLAS Flashcards: documentation page with system diagrams.

Opened through the navigation in app.py.
"""

from pathlib import Path

import streamlit as st

import diagrams
import flashcards as fc
import ollama_models as om
import rag
import theme

LOGO = Path(__file__).parent / "assets" / "atlas_logo.svg"


def diagram(svg: str, caption: str) -> None:
    st.html(f'<div class="atl-diagram">{theme.svg_img(svg, alt=caption)}<div class="atl-caption">{caption}</div></div>')


def hero() -> None:
    logo = theme.svg_img(LOGO.read_bytes(), alt="ATLAS") if LOGO.exists() else ""
    st.html(f"""
<div class="atl-hero">
  <div class="logo">{logo}</div>
  <div>
    <h1>Dokumentacja systemu</h1>
    <p>ATLAS Flashcards tworzy fiszki do nauki z Twoich materiałów i wyjaśnia je na podstawie źródeł (RAG).
       Działa w całości lokalnie: modele uruchamia Ollama na Twoim komputerze, więc dane nie trafiają do chmury.</p>
    <div class="atl-badges">
      <span class="atl-badge">Python 3.12</span><span class="atl-badge">Streamlit</span>
      <span class="atl-badge">Ollama</span><span class="atl-badge">Pydantic</span>
      <span class="atl-badge">model: {fc.MODEL}</span><span class="atl-badge">RAG: {rag.EMBED_MODEL}</span>
    </div>
  </div>
</div>
""")


def overview() -> None:
    st.html("""
<div class="atl-cards">
  <div class="atl-card"><h4>Dowolne materiały</h4>
    <p>Wklejony tekst albo pliki .txt, .docx i .pdf, np. moduły kursu.</p></div>
  <div class="atl-card"><h4>Lokalny model</h4>
    <p>Qwen 2.5 przez Ollamę. Bez kluczy API, bez opłat, działa offline.</p></div>
  <div class="atl-card"><h4>Kontrola jakości</h4>
    <p>Ten sam model ocenia każdą fiszkę (LLM-as-judge) i odrzuca słabe.</p></div>
  <div class="atl-card"><h4>Wyjaśnienia ze źródłami</h4>
    <p>Przycisk Wyjaśnij wyszukuje fragmenty materiału (RAG) i tłumaczy na ich podstawie.</p></div>
  <div class="atl-card"><h4>Nauka i eksport</h4>
    <p>Tryb nauki w aplikacji oraz eksport do Anki i CSV.</p></div>
</div>""")
    st.subheader("Szybki start")
    st.html(f"""<div class="atl-code"><span class="c"># 1. modele (raz): językowy i do embeddingów</span>
ollama pull {fc.MODEL}
ollama pull {rag.EMBED_MODEL}

<span class="c"># 2. biblioteki (raz)</span>
pip install ollama pydantic docx2txt pypdf streamlit numpy

<span class="c"># 3. uruchomienie aplikacji</span>
cd C:\\ATLAS\\Flashcards
python -m streamlit run app.py</div>""")


def models() -> None:
    st.markdown("""
Aplikacja korzysta z **dwóch rodzajów modeli**, które robią zupełnie różne rzeczy:

- **Model językowy (LLM)** czyta tekst i **pisze nowy tekst**: tworzy fiszki, ocenia ich jakość
  i wyjaśnia je w trybie nauki. To jedyny „agent” w systemie, wybierany w panelu bocznym.
- **Model do embeddingów** niczego nie pisze. Zamienia tekst na **listę liczb (wektor)**, która opisuje
  jego znaczenie. Teksty o podobnym sensie dostają podobne wektory, nawet gdy używają innych słów.
  Dzięki temu można wyszukiwać fragmenty materiału po znaczeniu, a nie tylko po słowach.
""")
    st.markdown(f"""
| Model | Rodzaj | Rola w aplikacji | Rozmiar | Uwagi |
|---|---|---|---|---|
| `qwen2.5:3b` | językowy | domyślny: tworzy, ocenia i wyjaśnia fiszki | ok. 1,9 GB | 3 mld parametrów, szybki na procesorze |
| `qwen2.5:7b` | językowy | wariant dokładniejszy, do wyboru w panelu | ok. 4,7 GB | 7 mld parametrów, wolniejszy, rzadziej się myli |
| `{rag.EMBED_MODEL}` | embeddingi | indeks i wyszukiwanie w RAG | ok. 1,2 GB | wektory o 1024 liczbach, dobrze zna polski |
""")
    st.markdown("""
**Qwen 2.5** to rodzina otwartych modeli zespołu Qwen (Alibaba Cloud). Rozumie wiele języków, w tym polski,
i dobrze trzyma się formatu JSON, co jest ważne przy fiszkach sprawdzanych przez Pydantic.
Ollama pobiera modele w wersji skwantyzowanej (wagi zapisane w ok. 4 bitach), dzięki czemu mieszczą się
w pamięci zwykłego laptopa. Domyślnie Ollama daje modelowi okno kontekstu 4096 tokenów.

**bge-m3** to model do embeddingów od BAAI (Beijing Academy of Artificial Intelligence),
wielojęzyczny i przystosowany do wyszukiwania. Jest mały i szybki, bo nie generuje tekstu,
tylko w jednym przebiegu liczy wektor.

**Jeden agent, jeden model językowy.** Ten sam wybrany model wykonuje wszystkie kroki wymagające
pisania: generowanie, ocenę i wyjaśnienia. Model do embeddingów nie jest drugim agentem,
tylko narzędziem do wyszukiwania, z którego korzysta system.
""")
    st.markdown("**Modele językowe polecane w panelu** (można je pobrać przyciskiem Pobierz):")
    st.markdown("| Model | Rozmiar do pobrania |\n|---|---|\n"
                + "\n".join(f"| `{name}` | {size} |" for name, size in om.CATALOG.items()))
    st.caption("Modele do embeddingów (np. bge-m3) są celowo ukryte na liście modeli językowych, "
               "bo nie potrafią pisać fiszek.")


def rag_section() -> None:
    st.markdown("""
### Czym jest RAG?
**RAG (Retrieval-Augmented Generation)**, czyli generowanie wspomagane wyszukiwaniem, to sposób,
w jaki model językowy korzysta z wiedzy, której sam nie ma. Zamiast odpowiadać „z pamięci”,
system najpierw **wyszukuje** pasujące fragmenty Twojego materiału, a potem **przekazuje je modelowi**
razem z pytaniem. Model odpowiada na ich podstawie i może je cytować.

**Dlaczego to ważne:**
- model nie zna Twoich notatek ani modułów kursu, a RAG mu je podaje,
- odpowiedź opiera się na źródle, więc model rzadziej zmyśla,
- widać, skąd pochodzi informacja, co ułatwia sprawdzenie odpowiedzi.
""")
    st.markdown("""
### Jak działa w ATLAS Flashcards
RAG ma dwie fazy. **Indeksowanie** odbywa się raz, zaraz po wygenerowaniu fiszek: materiał jest dzielony
na mniejsze fragmenty, a model do embeddingów zamienia każdy z nich na wektor. **Wyjaśnienie** odbywa się
po kliknięciu „Wyjaśnij” w trybie nauki: fiszka też jest zamieniana na wektor, system znajduje 3 najbliższe
fragmenty i przekazuje je modelowi językowemu, który tłumaczy temat po polsku.
""")
    diagram(diagrams.rag_svg(), "Rys. 5. RAG w aplikacji: indeksowanie materiału i wyjaśnianie fiszki na podstawie znalezionych fragmentów.")
    st.markdown(f"""
| Parametr (`rag.py`) | Wartość | Znaczenie |
|---|---|---|
| `EMBED_MODEL` | `{rag.EMBED_MODEL}` | model do embeddingów |
| `PASSAGE_CHARS` | {rag.PASSAGE_CHARS} znaków | długość fragmentu w indeksie; mniejsze fragmenty dają trafniejsze wyszukiwanie niż 2500 znaków przy generowaniu |
| `k` | 3 | ile najbliższych fragmentów trafia do modelu |
| miara podobieństwa | cosinus | wektory są znormalizowane, więc podobieństwo to iloczyn skalarny |
| `temperature` | 0,2 | wyjaśnienia trzymają się źródeł zamiast fantazjować |
""")
    st.markdown("""
### Zwykły RAG a agentowy RAG
W aplikacji działa **zwykły RAG**: kod zawsze wykonuje dokładnie jedno wyszukiwanie, a model tylko odpowiada.
To szybkie i przewidywalne rozwiązanie, dobre dla przycisku „Wyjaśnij”, gdzie pytanie jest zawsze podobne.

| | Zwykły RAG (w aplikacji) | Agentowy RAG |
|---|---|---|
| Kto decyduje o wyszukiwaniu | kod | model językowy |
| Liczba wyszukiwań | zawsze jedno | zero, jedno lub kilka |
| Zapytanie do wyszukiwarki | treść fiszki | układa je model |
| Szybkość | jedno wywołanie modelu | kilka wywołań |
| Dobre do | stałych, podobnych pytań | dowolnych, złożonych pytań, np. czatu z materiałem |

**Ograniczenia obecnej wersji:** indeks jest w pamięci i znika po restarcie aplikacji (powstaje na nowo przy
kolejnym generowaniu), a mały model czasem pomija odnośniki [1], [2] w treści. Źródła i tak są zawsze widoczne
w sekcji „Źródła z materiału”.
""")


def configuration() -> None:
    st.markdown("""
| Ustawienie (panel boczny) | Domyślnie | Znaczenie |
|---|---|---|
| **Model językowy** | `qwen2.5:3b` | jeden model tworzy fiszki, ocenia ich jakość i je wyjaśnia; lista zawiera modele pobrane i polecane „do pobrania” (z rozmiarem i przyciskiem Pobierz) |
| **Fiszek na fragment** | 5 | ile fiszek model może utworzyć z jednego fragmentu |
| **Minimalna ocena jakości** | 4 | model ocenia swoje fiszki w skali 1-5; niżej ocenione trafiają do odrzuconych |
| **Długość fragmentu** | 2500 znaków | dłuższy fragment = więcej kontekstu, ale wolniejsze odpowiedzi |
| **Nazwa talii w Anki** | ATLAS | nazwa talii zapisana w pliku eksportu |
""")
    st.markdown("""
| Funkcja | Rola |
|---|---|
| `flashcards.load_text(path)` / `text_from_bytes(data, suffix)` | wczytuje tekst z .txt, .docx lub .pdf (z pliku albo z wgranych danych) |
| `flashcards.split_into_chunks(text)` | dzieli tekst po akapitach na fragmenty |
| `flashcards.flashcards_from_chunk(text, count, model)` | generuje fiszki modelem (JSON zgodny z `Deck`) |
| `flashcards.deduplicate(cards)` | usuwa prawie identyczne pytania |
| `flashcards.review(card, source, model)` | ocenia fiszkę względem tekstu źródłowego |
| `flashcards.generate_from_text(text, …)` | cały potok; wspólny dla aplikacji i terminala, raportuje postęp |
| `flashcards.anki_text()` / `csv_text()` | treść eksportu do Anki lub arkusza (`export_anki()` / `export_csv()` zapisują ją do pliku) |
| `rag.Index.build(passages)` | zamienia fragmenty materiału na wektory i tworzy indeks |
| `rag.Index.search(query, k)` | zwraca k fragmentów najbliższych znaczeniowo |
| `rag.explain(question, answer, index, model)` | wyjaśnia fiszkę na podstawie znalezionych fragmentów |
| `ollama_models.is_embedding_model(name)` | rozpoznaje modele do embeddingów, żeby nie trafiły na listę modeli językowych |
""")
    st.markdown("""
| Plik | Rola |
|---|---|
| `app.py` | nawigacja, logo, motyw |
| `generator.py` / `docs.py` | strony aplikacji |
| `flashcards.py` | logika fiszek i wywołania modelu; działa też z terminala |
| `rag.py` | RAG: indeks embeddingów i wyjaśnienia ze źródłami |
| `ollama_models.py` | lista polecanych modeli, rozpoznawanie embeddingów, pobieranie |
| `theme.py` / `diagrams.py` | wygląd (style, nagłówek) i diagramy dokumentacji |
| `tests/` | 15 testów bez modelu: `python -m unittest discover tests` |
""")


def faq() -> None:
    with st.expander("Dlaczego generowanie trwa kilka minut?"):
        st.write("Model działa na procesorze. Każdy fragment to jedno wywołanie modelu, a każda fiszka "
                 "to kolejne wywołanie oceniające jej jakość. Mniejszy model (3b) lub krótszy tekst przyspieszają pracę.")
    with st.expander("Ocena przepuściła słabą fiszkę. Co zrobić?"):
        st.write("Odznacz ją w tabeli przed eksportem. Na stałe pomaga większy model (np. 7b) "
                 "albo wyższy próg minimalnej oceny.")
    with st.expander("Nie widzę przycisku Wyjaśnij. Dlaczego?"):
        st.write(f"Przycisk pojawia się w zakładce Ucz się dopiero po kliknięciu Pokaż odpowiedź. "
                 f"Wymaga pobranego modelu {rag.EMBED_MODEL} (ollama pull {rag.EMBED_MODEL}) oraz fiszek "
                 f"wygenerowanych od ostatniego uruchomienia aplikacji, bo indeks jest przechowywany w pamięci.")
    with st.expander(f"Czym różni się {rag.EMBED_MODEL} od qwen2.5?"):
        st.write("qwen2.5 to model językowy: czyta i pisze tekst. bge-m3 to model do embeddingów: zamienia tekst "
                 "na wektor liczb do wyszukiwania po znaczeniu i niczego nie pisze. Szczegóły w zakładce Modele.")
    with st.expander("Czy moje dane wychodzą poza komputer?"):
        st.write("Nie. Aplikacja łączy się tylko z Ollamą pod adresem localhost:11434 "
                 "i jest dostępna wyłącznie z Twojego komputera (server.address w .streamlit/config.toml).")
    with st.expander("Jak zaimportować fiszki do Anki?"):
        st.write("W Anki otwórz menu Plik, wybierz Importuj i wskaż pobrany plik flashcards_anki.txt. "
                 "Nagłówek pliku sam ustawi separator, talię i tagi.")


theme.docs_styles()
hero()

(tab_overview, tab_arch, tab_flow, tab_models, tab_rag,
 tab_data, tab_config, tab_faq) = st.tabs(
    ["Przegląd", "Architektura", "Przepływ danych", "Modele", "RAG", "Model danych", "Konfiguracja", "FAQ"]
)
with tab_overview:
    overview()
with tab_arch:
    st.markdown("System ma trzy warstwy: **interfejs** (Streamlit), **logikę** (`flashcards.py` i `rag.py`) "
                "oraz **modele** uruchamiane lokalnie przez Ollamę. Interfejs nie rozmawia z modelami "
                "bezpośrednio, tylko przez funkcje logiki, dzięki czemu ten sam kod działa też z terminala.")
    diagram(diagrams.ARCHITECTURE, "Rys. 1. Architektura: niebieskie bloki logiki wywołują model językowy, "
                                   "turkusowe korzystają z modelu do embeddingów.")
with tab_flow:
    st.markdown("Każdy tekst przechodzi przez 7 kroków. Ten sam model językowy jest użyty dwa razy: "
                "najpierw **tworzy** fiszki, potem **ocenia** ich jakość. Po wygenerowaniu powstaje też "
                "indeks RAG do wyjaśnień (zakładka RAG).")
    diagram(diagrams.pipeline_svg(), "Rys. 2. Przepływ danych od pliku do eksportu.")
    diagram(diagrams.sequence_svg(), "Rys. 3. Sekwencja wywołań: kto z kim rozmawia podczas generowania.")
with tab_models:
    models()
with tab_rag:
    rag_section()
with tab_data:
    st.markdown("Odpowiedzi modelu są sprawdzane modelami **Pydantic**. Ten sam schemat trafia do Ollamy "
                "w parametrze `format`, więc model od razu wie, jaki JSON ma zwrócić.")
    diagram(diagrams.DATA_MODEL, "Rys. 4. Model danych: talia zawiera fiszki, a ocena (Review) dotyczy pojedynczej fiszki.")
with tab_config:
    configuration()
with tab_faq:
    faq()
