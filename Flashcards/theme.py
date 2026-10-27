"""Shared look of the app: background, page header, documentation styles and SVG images."""

import base64

import streamlit as st

BACKGROUND_CSS = """
<style>
  /* deep-blue gradient + faint technical grid */
  .stApp {
    background:
      linear-gradient(rgba(59,130,246,.06) 1px, transparent 1px) 0 0 / 48px 48px,
      linear-gradient(90deg, rgba(59,130,246,.06) 1px, transparent 1px) 0 0 / 48px 48px,
      radial-gradient(1100px 600px at 12% -5%, #134a8c 0%, transparent 60%),
      radial-gradient(900px 520px at 105% 105%, #0f3d75 0%, transparent 55%),
      linear-gradient(160deg, #03102a 0%, #06244d 50%, #031634 100%);
    background-attachment: fixed;
  }
  /* two layers of glowing particles drifting at different speeds */
  .stApp::before, .stApp::after {
    content: ""; position: fixed; inset: -400px; pointer-events: none; z-index: 0;
  }
  .stApp::before {
    background-image:
      radial-gradient(circle, rgba(147,197,253,.55) 1px, transparent 1.7px),
      radial-gradient(circle, rgba(34,211,238,.40) 1px, transparent 1.9px);
    background-size: 120px 120px, 180px 180px;
    background-position: 0 0, 70px 95px;
    animation: atl-drift-a 70s linear infinite;
  }
  .stApp::after {
    background-image: radial-gradient(circle, rgba(96,165,250,.45) 1.6px, transparent 2.8px);
    background-size: 240px 240px;
    background-position: 130px 40px;
    filter: blur(.3px);
    animation: atl-drift-b 110s linear infinite;
  }
  /* each animation moves by a multiple of the tile size, so the loop is seamless */
  @keyframes atl-drift-a { to { transform: translate(0, -360px); } }
  @keyframes atl-drift-b { to { transform: translate(240px, -480px); } }
  @media (prefers-reduced-motion: reduce) { .stApp::before, .stApp::after { animation: none; } }

  /* keep Streamlit's own positioning (it pins the container to the viewport, so the sidebar can scroll) */
  [data-testid="stAppViewContainer"] { z-index: 1; background: transparent; }
  [data-testid="stHeader"] { background: transparent; }
  [data-testid="stSidebar"] {
    background: rgba(4, 18, 42, .72); backdrop-filter: blur(8px);
    border-right: 1px solid rgba(59,130,246,.25);
  }
  /* logo at the very top: the sidebar header only holds the collapse button, so float it in the corner */
  [data-testid="stSidebarHeader"] { position: absolute; top: 0; right: 0; z-index: 2;
                                    height: auto; min-height: 0; padding: .4rem; margin: 0; }
  [data-testid="stSidebarUserContent"] { padding-top: .6rem; }
  /* no developer toolbar in the top-right corner: hide the main menu and the Deploy button */
  [data-testid="stMainMenu"], [data-testid="stAppDeployButton"] { display: none; }
</style>
"""

HEADER_HTML = """
<style>
  .atl-head { display:flex; align-items:center; justify-content:space-between; gap:28px; flex-wrap:wrap;
              margin: 6px 0 18px; }
  .atl-head h1 { margin:0; font-size:44px; line-height:1.1; font-weight:800; color:#F8FAFF; letter-spacing:.5px; }
  .atl-head h1 span { background:linear-gradient(90deg,#60A5FA,#22D3EE); -webkit-background-clip:text;
                      background-clip:text; color:transparent; }
  .atl-head p { margin:8px 0 0; color:#9DB8E0; font-size:15.5px; max-width:520px; }

  /* flashcard that flips between question and answer */
  .flip-scene { position:relative; width:250px; height:150px; perspective:1000px; margin-right:12px; }
  .flip-scene::before { /* a second card underneath, like a deck */
    content:""; position:absolute; inset:0; border-radius:18px; transform:rotate(-7deg) translate(-10px,8px);
    background:rgba(37,99,235,.35); border:1px solid rgba(96,165,250,.45); }
  .flip-card { position:relative; width:100%; height:100%; transform-style:preserve-3d;
               animation: atl-flip 7s ease-in-out infinite; }
  .flip-face { position:absolute; inset:0; border-radius:18px; padding:16px 20px; display:flex; flex-direction:column;
               justify-content:center; gap:8px; backface-visibility:hidden; -webkit-backface-visibility:hidden;
               box-shadow:0 18px 40px rgba(2,8,23,.55); }
  .flip-front { background:#F8FAFF; color:#0A2540; border:1px solid #BFDBFE; }
  .flip-back  { background:linear-gradient(135deg,#1D4ED8,#0EA5E9); color:#fff; transform:rotateY(180deg); }
  .flip-tag { font:700 11px/1 Consolas, monospace; letter-spacing:2px; opacity:.75; }
  .flip-text { font-size:18px; font-weight:700; line-height:1.3; }
  @keyframes atl-flip {
    0%, 38%   { transform: rotateY(0deg); }
    50%, 88%  { transform: rotateY(180deg); }
    100%      { transform: rotateY(360deg); }
  }
  @media (prefers-reduced-motion: reduce) { .flip-card { animation: none; } }
</style>
<div class="atl-head">
  <div>
    <h1>ATLAS: <span>Flashcards</span></h1>
    <p>Fiszki do nauki z Twoich materiałów, generowane lokalnym modelem przez Ollamę.</p>
  </div>
  <div class="flip-scene" aria-hidden="true">
    <div class="flip-card">
      <div class="flip-face flip-front"><span class="flip-tag">PYTANIE</span>
        <span class="flip-text">Gdzie zachodzi fotosynteza?</span></div>
      <div class="flip-face flip-back"><span class="flip-tag">ODPOWIEDŹ</span>
        <span class="flip-text">W chloroplastach komórek roślinnych</span></div>
    </div>
  </div>
</div>
"""

DOCS_CSS = """
<style>
  .atl-hero { display:flex; gap:28px; align-items:center; flex-wrap:wrap; padding:26px 30px; border-radius:20px;
              background:#ffffff; border:1px solid #dbe6f5; box-shadow:0 10px 30px rgba(10,37,64,.08);
              position:relative; overflow:hidden; }
  .atl-hero::before { content:""; position:absolute; inset:0 0 auto 0; height:6px;
                      background:linear-gradient(90deg,#0A2540,#2563EB,#22D3EE); }
  .atl-hero .logo { width:300px; max-width:100%; }
  .atl-hero h1 { font-size:30px; line-height:1.15; margin:0 0 6px; color:#0A2540; }
  .atl-hero p { margin:0; color:#4a5b70; font-size:15.5px; max-width:560px; }
  .atl-badges { display:flex; gap:8px; flex-wrap:wrap; margin-top:14px; }
  .atl-badge { font:600 12px/1 Consolas, monospace; color:#1D4ED8; background:#EFF6FF; border:1px solid #BFDBFE;
               padding:6px 10px; border-radius:999px; }
  .atl-cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:14px; margin:18px 0 6px; }
  .atl-card { background:#fff; border:1px solid #dbe6f5; border-radius:16px; padding:16px 18px;
              box-shadow:0 4px 14px rgba(10,37,64,.05); }
  .atl-card h4 { margin:6px 0 4px; font-size:15px; color:#0A2540; }
  .atl-card p { margin:0; font-size:13.5px; color:#4a5b70; line-height:1.5; }
  .atl-diagram { background:#fff; border:1px solid #dbe6f5; border-radius:18px; padding:18px;
                 box-shadow:0 6px 20px rgba(10,37,64,.06); margin:8px 0 6px; }
  .atl-caption { font-size:13px; color:#4a5b70; margin:8px 4px 0; }
  .atl-code { background:#0A2540; color:#E0F2FE; border-radius:14px; padding:14px 18px;
              font:13.5px/1.7 Consolas, monospace; white-space:pre; overflow-x:auto; }
  .atl-code .c { color:#60A5FA; }
</style>
"""


def apply() -> None:
    st.html(BACKGROUND_CSS)


def page_header() -> None:
    st.html(HEADER_HTML)


def docs_styles() -> None:
    st.html(DOCS_CSS)


def svg_img(svg: str | bytes, alt: str = "") -> str:
    """<img> tag with the SVG as a data URI.

    st.html sanitizes markup: it drops inline <svg> and the <use> elements our logos are built from,
    while an image keeps the SVG intact.
    """
    if isinstance(svg, str):
        svg = svg.strip()
        if "xmlns=" not in svg.split(">", 1)[0]:
            svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
        svg = svg.encode("utf-8")
    return f'<img src="data:image/svg+xml;base64,{base64.b64encode(svg).decode()}" alt="{alt}" style="width:100%">'
