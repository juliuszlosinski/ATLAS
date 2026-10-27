"""System diagrams for the documentation page, as SVG markup (pure strings, work offline)."""


SVG_DEFS = """
<defs>
  <marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M1 1 L9 5 L1 9 Z" fill="#3B82F6"/>
  </marker>
</defs>"""

ARCHITECTURE = f"""
<svg viewBox="0 0 960 460" font-family="Segoe UI, Arial, sans-serif" role="img" aria-label="Architektura systemu">
  {SVG_DEFS}
  <!-- użytkownik -->
  <rect x="20" y="150" width="130" height="70" rx="14" fill="#F1F5F9" stroke="#94A3B8"/>
  <text x="85" y="180" text-anchor="middle" font-size="14" font-weight="700" fill="#0A2540">Użytkownik</text>
  <text x="85" y="199" text-anchor="middle" font-size="12" fill="#4a5b70">przeglądarka</text>

  <!-- interfejs -->
  <rect x="190" y="40" width="200" height="260" rx="18" fill="#EFF6FF" stroke="#3B82F6" stroke-dasharray="6 4"/>
  <text x="206" y="64" font-size="13" font-weight="700" fill="#1D4ED8">INTERFEJS · Streamlit</text>
  <g font-size="13">
    <rect x="205" y="80" width="170" height="50" rx="12" fill="#fff" stroke="#93C5FD"/>
    <text x="290" y="102" text-anchor="middle" font-weight="700" fill="#0A2540">app.py</text>
    <text x="290" y="119" text-anchor="middle" font-size="11.5" fill="#4a5b70">nawigacja, logo, motyw</text>
    <rect x="205" y="145" width="170" height="50" rx="12" fill="#fff" stroke="#93C5FD"/>
    <text x="290" y="167" text-anchor="middle" font-weight="700" fill="#0A2540">generator.py</text>
    <text x="290" y="184" text-anchor="middle" font-size="11.5" fill="#4a5b70">fiszki, nauka, Wyjaśnij</text>
    <rect x="205" y="210" width="170" height="50" rx="12" fill="#fff" stroke="#93C5FD"/>
    <text x="290" y="232" text-anchor="middle" font-weight="700" fill="#0A2540">docs.py</text>
    <text x="290" y="249" text-anchor="middle" font-size="11.5" fill="#4a5b70">dokumentacja i diagramy</text>
  </g>

  <!-- logika: fiszki -->
  <rect x="430" y="40" width="220" height="260" rx="18" fill="#0A2540"/>
  <text x="446" y="64" font-size="13" font-weight="700" fill="#93C5FD">LOGIKA · flashcards.py</text>
  <g font-family="Consolas, monospace" font-size="12.5" fill="#E0F2FE">
    <rect x="446" y="76" width="188" height="30" rx="8" fill="#123A66"/><text x="458" y="96">load_text()</text>
    <rect x="446" y="113" width="188" height="30" rx="8" fill="#123A66"/><text x="458" y="133">split_into_chunks()</text>
    <rect x="446" y="150" width="188" height="30" rx="8" fill="#1D4ED8"/><text x="458" y="170">flashcards_from_chunk()</text>
    <rect x="446" y="187" width="188" height="30" rx="8" fill="#123A66"/><text x="458" y="207">deduplicate()</text>
    <rect x="446" y="224" width="188" height="30" rx="8" fill="#1D4ED8"/><text x="458" y="244">review()</text>
    <rect x="446" y="261" width="188" height="30" rx="8" fill="#123A66"/><text x="458" y="281">export_anki/csv()</text>
  </g>

  <!-- logika: RAG -->
  <rect x="430" y="320" width="220" height="120" rx="18" fill="#0A2540"/>
  <text x="446" y="344" font-size="13" font-weight="700" fill="#67E8F9">RAG · rag.py</text>
  <g font-family="Consolas, monospace" font-size="12.5" fill="#E0F2FE">
    <rect x="446" y="356" width="188" height="30" rx="8" fill="#0E7490"/><text x="458" y="376">Index.build/search()</text>
    <rect x="446" y="393" width="188" height="30" rx="8" fill="#1D4ED8"/><text x="458" y="413">explain()</text>
  </g>

  <!-- ollama i modele -->
  <rect x="690" y="110" width="120" height="220" rx="16" fill="#1D4ED8"/>
  <text x="750" y="200" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">Ollama</text>
  <text x="750" y="221" text-anchor="middle" font-size="11.5" fill="#BFDBFE" font-family="Consolas, monospace">localhost:11434</text>
  <text x="750" y="241" text-anchor="middle" font-size="11" fill="#BFDBFE">lokalnie, offline</text>
  <rect x="840" y="95" width="105" height="56" rx="12" fill="#fff" stroke="#3B82F6"/>
  <text x="892" y="120" text-anchor="middle" font-size="13" font-weight="700" fill="#0A2540" font-family="Consolas, monospace">qwen2.5:3b</text>
  <text x="892" y="138" text-anchor="middle" font-size="11" fill="#4a5b70">model językowy</text>
  <rect x="840" y="165" width="105" height="56" rx="12" fill="#fff" stroke="#3B82F6"/>
  <text x="892" y="190" text-anchor="middle" font-size="13" font-weight="700" fill="#0A2540" font-family="Consolas, monospace">qwen2.5:7b</text>
  <text x="892" y="208" text-anchor="middle" font-size="11" fill="#4a5b70">lub dokładniejszy</text>
  <rect x="840" y="265" width="105" height="56" rx="12" fill="#ECFEFF" stroke="#22D3EE"/>
  <text x="892" y="290" text-anchor="middle" font-size="13" font-weight="700" fill="#0A2540" font-family="Consolas, monospace">bge-m3</text>
  <text x="892" y="308" text-anchor="middle" font-size="11" fill="#0E7490">embeddingi</text>

  <!-- pliki -->
  <rect x="190" y="345" width="95" height="50" rx="12" fill="#F1F5F9" stroke="#94A3B8"/>
  <text x="237" y="366" text-anchor="middle" font-size="12.5" font-weight="700" fill="#0A2540">Wejście</text>
  <text x="237" y="383" text-anchor="middle" font-size="11" fill="#4a5b70">.txt .docx .pdf</text>
  <rect x="295" y="345" width="95" height="50" rx="12" fill="#ECFEFF" stroke="#22D3EE"/>
  <text x="342" y="366" text-anchor="middle" font-size="12.5" font-weight="700" fill="#0A2540">Eksport</text>
  <text x="342" y="383" text-anchor="middle" font-size="11" fill="#4a5b70">Anki · CSV</text>

  <!-- połączenia -->
  <g stroke="#3B82F6" stroke-width="2.5" fill="none">
    <line x1="150" y1="185" x2="186" y2="185" marker-end="url(#ar)" marker-start="url(#ar)"/>
    <line x1="390" y1="170" x2="426" y2="170" marker-end="url(#ar)"/>
    <path d="M390 275 L410 275 L410 380 L426 380" marker-end="url(#ar)"/>
    <line x1="650" y1="165" x2="686" y2="165" marker-end="url(#ar)" marker-start="url(#ar)"/>
    <path d="M650 380 L670 380 L670 300 L686 300" marker-end="url(#ar)"/>
    <line x1="810" y1="135" x2="836" y2="123" marker-end="url(#ar)"/>
    <line x1="810" y1="193" x2="836" y2="193" marker-end="url(#ar)"/>
    <line x1="810" y1="285" x2="836" y2="293" marker-end="url(#ar)"/>
    <line x1="237" y1="345" x2="237" y2="304" marker-end="url(#ar)"/>
    <line x1="342" y1="300" x2="342" y2="341" marker-end="url(#ar)"/>
  </g>
  <text x="668" y="155" text-anchor="middle" font-size="11" fill="#1D4ED8">HTTP</text>
</svg>"""


def _rag_box(x: int, y: int, title: str, sub: str, kind: str = "step") -> str:
    fill, stroke, color, muted = {
        "step": ("#F1F5F9", "#94A3B8", "#0A2540", "#4a5b70"),
        "embed": ("#ECFEFF", "#22D3EE", "#0A2540", "#0E7490"),
        "llm": ("#1D4ED8", "#1D4ED8", "#FFFFFF", "#BFDBFE"),
        "store": ("#0A2540", "#0A2540", "#FFFFFF", "#93C5FD"),
    }[kind]
    return f"""
  <rect x="{x}" y="{y}" width="150" height="64" rx="14" fill="{fill}" stroke="{stroke}"/>
  <text x="{x + 75}" y="{y + 28}" text-anchor="middle" font-size="14" font-weight="700" fill="{color}">{title}</text>
  <text x="{x + 75}" y="{y + 47}" text-anchor="middle" font-size="11" fill="{muted}">{sub}</text>"""


def rag_svg() -> str:
    xs = [16, 196, 376, 556, 736]
    index_row = [("Materiał", "tekst lub plik", "step"), ("Fragmenty", "po 800 znaków", "step"),
                 ("bge-m3", "tekst na wektor", "embed"), ("Indeks", "1024 liczby na fragment", "store")]
    query_row = [("Fiszka", "pytanie i odpowiedź", "step"), ("bge-m3", "wektor pytania", "embed"),
                 ("Wyszukiwanie", "cosinus, 3 najlepsze", "step"), ("Prompt", "3 fragmenty i fiszka", "step"),
                 ("qwen2.5", "model językowy", "llm")]
    parts = [_rag_box(x, 45, *box) for x, box in zip(xs, index_row)]
    parts += [_rag_box(x, 180, *box) for x, box in zip(xs, query_row)]
    parts += [f'<line x1="{x + 152}" y1="77" x2="{x + 174}" y2="77" stroke="#3B82F6" stroke-width="2.5" marker-end="url(#ar)"/>'
              for x in xs[:3]]
    parts += [f'<line x1="{x + 152}" y1="212" x2="{x + 174}" y2="212" stroke="#3B82F6" stroke-width="2.5" marker-end="url(#ar)"/>'
              for x in xs[:4]]
    return f"""
<svg viewBox="0 0 960 340" font-family="Segoe UI, Arial, sans-serif" role="img" aria-label="Przepływ RAG">
  {SVG_DEFS}
  <text x="16" y="30" font-size="13" font-weight="700" fill="#0E7490">1. INDEKSOWANIE · raz, zaraz po wygenerowaniu fiszek</text>
  <text x="16" y="168" font-size="13" font-weight="700" fill="#1D4ED8">2. WYJAŚNIENIE · po kliknięciu „Wyjaśnij”</text>
  {''.join(parts)}
  <path d="M631 109 L631 140 L451 140 L451 176" stroke="#0E7490" stroke-width="2.5" stroke-dasharray="6 4" fill="none" marker-end="url(#ar)"/>
  <text x="541" y="134" text-anchor="middle" font-size="11.5" fill="#0E7490">przeszukiwany indeks</text>
  <line x1="811" y1="244" x2="811" y2="266" stroke="#3B82F6" stroke-width="2.5" marker-end="url(#ar)"/>
  <rect x="716" y="270" width="190" height="56" rx="14" fill="#E0F2FE" stroke="#3B82F6"/>
  <text x="811" y="294" text-anchor="middle" font-size="14" font-weight="700" fill="#0A2540">Wyjaśnienie</text>
  <text x="811" y="313" text-anchor="middle" font-size="11" fill="#4a5b70">po polsku, ze źródłami</text>
  <g font-size="11.5">
    <rect x="16" y="292" width="12" height="12" rx="3" fill="#ECFEFF" stroke="#22D3EE"/><text x="34" y="302" fill="#0E7490">model do embeddingów</text>
    <rect x="200" y="292" width="12" height="12" rx="3" fill="#1D4ED8"/><text x="218" y="302" fill="#1D4ED8">model językowy</text>
    <rect x="340" y="292" width="12" height="12" rx="3" fill="#F1F5F9" stroke="#94A3B8"/><text x="358" y="302" fill="#4a5b70">czysty Python</text>
  </g>
</svg>"""

STEPS = [
    ("1", "Wczytanie", ".txt · .docx · .pdf", "#F1F5F9", "#94A3B8", "#0A2540"),
    ("2", "Podział", "fragmenty ≤ 2500 zn.", "#F1F5F9", "#94A3B8", "#0A2540"),
    ("3", "Generowanie", "LLM, format JSON", "#1D4ED8", "#1D4ED8", "#FFFFFF"),
    ("4", "Walidacja", "Pydantic", "#EFF6FF", "#3B82F6", "#0A2540"),
    ("5", "Deduplikacja", "podobieństwo ≥ 0,85", "#F1F5F9", "#94A3B8", "#0A2540"),
    ("6", "Ocena", "ten sam model, 1-5", "#1D4ED8", "#1D4ED8", "#FFFFFF"),
    ("7", "Eksport", "Anki · CSV", "#ECFEFF", "#22D3EE", "#0A2540"),
]


def pipeline_svg() -> str:
    parts = []
    for i, (num, title, sub, fill, stroke, color) in enumerate(STEPS):
        x = 16 + i * 134
        muted = "#BFDBFE" if color == "#FFFFFF" else "#4a5b70"
        parts.append(f"""
  <rect x="{x}" y="40" width="118" height="78" rx="14" fill="{fill}" stroke="{stroke}"/>
  <circle cx="{x + 20}" cy="40" r="13" fill="#0A2540"/>
  <text x="{x + 20}" y="45" text-anchor="middle" font-size="12" font-weight="700" fill="#22D3EE">{num}</text>
  <text x="{x + 59}" y="78" text-anchor="middle" font-size="14" font-weight="700" fill="{color}">{title}</text>
  <text x="{x + 59}" y="98" text-anchor="middle" font-size="11" fill="{muted}">{sub}</text>""")
        if i < len(STEPS) - 1:
            parts.append(f'<line x1="{x + 120}" y1="79" x2="{x + 131}" y2="79" stroke="#3B82F6" stroke-width="2.5" marker-end="url(#ar)"/>')
    return f"""
<svg viewBox="0 0 960 250" font-family="Segoe UI, Arial, sans-serif" role="img" aria-label="Przepływ danych">
  {SVG_DEFS}
  {''.join(parts)}
  <path d="M761 118 L761 160" stroke="#EF4444" stroke-width="2.5" fill="none" marker-end="url(#ar)"/>
  <rect x="686" y="164" width="150" height="56" rx="12" fill="#FEF2F2" stroke="#FCA5A5"/>
  <text x="761" y="187" text-anchor="middle" font-size="13" font-weight="700" fill="#991B1B">Odrzucone</text>
  <text x="761" y="205" text-anchor="middle" font-size="11" fill="#7F1D1D">ocena poniżej progu</text>
  <rect x="852" y="164" width="96" height="56" rx="12" fill="#fff" stroke="#93C5FD" stroke-dasharray="4 3"/>
  <text x="900" y="187" text-anchor="middle" font-size="12" font-weight="700" fill="#0A2540">Edycja</text>
  <text x="900" y="205" text-anchor="middle" font-size="11" fill="#4a5b70">w tabeli</text>
  <line x1="900" y1="164" x2="900" y2="122" stroke="#93C5FD" stroke-width="2" stroke-dasharray="4 3" marker-end="url(#ar)"/>
  <g font-size="11.5" fill="#1D4ED8">
    <rect x="16" y="224" width="12" height="12" rx="3" fill="#1D4ED8"/><text x="34" y="234">wywołanie modelu językowego</text>
    <rect x="210" y="224" width="12" height="12" rx="3" fill="#F1F5F9" stroke="#94A3B8"/><text x="228" y="234" fill="#4a5b70">czysty Python</text>
  </g>
</svg>"""


DATA_MODEL = f"""
<svg viewBox="0 0 960 250" font-family="Segoe UI, Arial, sans-serif" role="img" aria-label="Model danych">
  {SVG_DEFS}
  <g font-family="Consolas, monospace" font-size="13">
    <!-- Deck -->
    <rect x="20" y="70" width="230" height="96" rx="14" fill="#fff" stroke="#3B82F6"/>
    <path d="M20 84 a14 14 0 0 1 14 -14 h202 a14 14 0 0 1 14 14 v20 h-230 Z" fill="#0A2540"/>
    <text x="36" y="96" font-weight="700" fill="#fff">Deck</text>
    <text x="36" y="134" fill="#0A2540">flashcards: list[Flashcard]</text>

    <!-- Flashcard -->
    <rect x="330" y="30" width="330" height="190" rx="14" fill="#fff" stroke="#3B82F6"/>
    <path d="M330 44 a14 14 0 0 1 14 -14 h302 a14 14 0 0 1 14 14 v20 h-330 Z" fill="#1D4ED8"/>
    <text x="346" y="56" font-weight="700" fill="#fff">Flashcard</text>
    <text x="346" y="92" fill="#0A2540">question:<tspan x="446">str</tspan><tspan x="500" fill="#64748B">5-200 znaków</tspan></text>
    <text x="346" y="120" fill="#0A2540">answer:<tspan x="446">str</tspan><tspan x="500" fill="#64748B">1-300 znaków</tspan></text>
    <text x="346" y="148" fill="#0A2540">kind:<tspan x="446">Literal</tspan></text>
    <text x="362" y="166" fill="#64748B" font-size="11.5">definition | fact | concept | example</text>
    <text x="346" y="194" fill="#0A2540">difficulty:<tspan x="446">Literal</tspan></text>
    <text x="362" y="212" fill="#64748B" font-size="11.5">easy | medium | hard</text>

    <!-- Review -->
    <rect x="740" y="70" width="200" height="96" rx="14" fill="#fff" stroke="#22D3EE"/>
    <path d="M740 84 a14 14 0 0 1 14 -14 h172 a14 14 0 0 1 14 14 v20 h-200 Z" fill="#0E7490"/>
    <text x="756" y="96" font-weight="700" fill="#fff">Review</text>
    <text x="756" y="130" fill="#0A2540">score:<tspan x="820">int</tspan><tspan x="854" fill="#64748B">1-5</tspan></text>
    <text x="756" y="152" fill="#0A2540">reason:<tspan x="820">str</tspan></text>
  </g>
  <line x1="250" y1="118" x2="326" y2="118" stroke="#3B82F6" stroke-width="2.5" marker-end="url(#ar)"/>
  <text x="288" y="110" text-anchor="middle" font-size="11.5" fill="#1D4ED8">1..*</text>
  <line x1="736" y1="118" x2="664" y2="118" stroke="#22D3EE" stroke-width="2.5" stroke-dasharray="5 4" marker-end="url(#ar)"/>
  <text x="700" y="110" text-anchor="middle" font-size="11.5" fill="#0E7490">ocenia</text>
</svg>"""

LIFELINES = [(120, "Użytkownik"), (360, "Interfejs"), (600, "flashcards.py"), (840, "Ollama")]
MESSAGES = [
    (0, 1, "tekst lub plik + „Generuj fiszki”", False),
    (1, 2, "split_into_chunks(text)", False),
    (1, 2, "flashcards_from_chunk() × fragment", False),
    (2, 3, "POST /api/chat (format = schemat Deck)", False),
    (3, 2, "JSON z fiszkami", True),
    (1, 2, "deduplicate(), review() × fiszka", False),
    (2, 3, "POST /api/chat (format = schemat Review)", False),
    (3, 2, "ocena + uzasadnienie", True),
    (1, 0, "tabela, metryki, odrzucone", True),
    (0, 1, "Pobierz dla Anki / CSV", False),
]


def sequence_svg() -> str:
    parts = []
    for x, name in LIFELINES:
        parts.append(f"""
  <rect x="{x - 70}" y="16" width="140" height="38" rx="12" fill="#0A2540"/>
  <text x="{x}" y="40" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">{name}</text>
  <line x1="{x}" y1="54" x2="{x}" y2="392" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="5 5"/>""")
    for i, (src, dst, label, reply) in enumerate(MESSAGES):
        y = 84 + i * 31
        x1, x2 = LIFELINES[src][0], LIFELINES[dst][0]
        x2 += -6 if x2 > x1 else 6
        color = "#22D3EE" if reply else "#2563EB"
        dash = ' stroke-dasharray="6 4"' if reply else ""
        parts.append(f"""
  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="2.2"{dash} marker-end="url(#ar)"/>
  <text x="{(x1 + x2) / 2}" y="{y - 7}" text-anchor="middle" font-size="11.5" fill="#0A2540">{label}</text>""")
    return f"""
<svg viewBox="0 0 960 400" font-family="Segoe UI, Arial, sans-serif" role="img" aria-label="Sekwencja wywołań">
  {SVG_DEFS}
  {''.join(parts)}
</svg>"""
