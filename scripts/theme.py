"""Theme presets for the profile README.

Set "theme" in profile.config.json to one of the keys in THEMES, push, and
the Action re-renders everything that carries colour:
  assets/header.svg, assets/footer.svg, the HEADER and STATS sections of
  README.md, and (via --snake) the contribution snake colours.

Usage:
  python scripts/theme.py                 apply the configured theme (no network needed)
  python scripts/theme.py --preview FILE  write an HTML gallery of every theme
  python scripts/theme.py --snake         print snake outputs for the snake workflow
"""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "profile.config.json").read_text(encoding="utf-8"))

# bg: three gradient stops (top-left -> bottom-right)
# accent: glow, cursor, waves, typing text   accent2: secondary highlights
# text: name colour   sub: subtitle colour   card: stats card background
THEMES: dict[str, dict] = {
    "cyber": {
        "label": "Cyber Ocean", "bg": ["#0d1117", "#0b1f4a", "#0b3d91"],
        "accent": "#00f7ff", "accent2": "#3b82f6", "text": "#ffffff", "sub": "#9fe9ff",
        "card": "#0d1117", "card_text": "#c9d1d9",
    },
    "matrix": {
        "label": "Matrix", "bg": ["#000000", "#001a07", "#00330f"],
        "accent": "#00ff41", "accent2": "#008f11", "text": "#e6ffe9", "sub": "#7dff9a",
        "card": "#000000", "card_text": "#b6f5c3",
    },
    "synthwave": {
        "label": "Synthwave", "bg": ["#1a1033", "#3b1061", "#7a1e6e"],
        "accent": "#ff2a6d", "accent2": "#f9c80e", "text": "#ffffff", "sub": "#ffb3d1",
        "card": "#1a1033", "card_text": "#e8d9ff",
    },
    "dracula": {
        "label": "Dracula", "bg": ["#21222c", "#282a36", "#44475a"],
        "accent": "#bd93f9", "accent2": "#ff79c6", "text": "#f8f8f2", "sub": "#d6c4ff",
        "card": "#282a36", "card_text": "#f8f8f2",
    },
    "ember": {
        "label": "Ember", "bg": ["#120807", "#3a120c", "#7a2410"],
        "accent": "#ff8c42", "accent2": "#ffd166", "text": "#fff4e6", "sub": "#ffc89e",
        "card": "#140a08", "card_text": "#ffe3cc",
    },
    "nord": {
        "label": "Nord Arctic", "bg": ["#2e3440", "#3b4252", "#4c566a"],
        "accent": "#88c0d0", "accent2": "#81a1c1", "text": "#eceff4", "sub": "#d8dee9",
        "card": "#2e3440", "card_text": "#e5e9f0",
    },
    "aurora": {
        "label": "Aurora", "bg": ["#0b1026", "#103a4a", "#1d6b5a"],
        "accent": "#7cffcb", "accent2": "#b388ff", "text": "#ffffff", "sub": "#c3fff0",
        "card": "#0b1026", "card_text": "#d7f7ff",
    },
    "paper": {
        "label": "Clean Light", "bg": ["#ffffff", "#eef4ff", "#dbe8ff"],
        "accent": "#0969da", "accent2": "#8250df", "text": "#1f2328", "sub": "#3d4b5c",
        "card": "#ffffff", "card_text": "#1f2328",
    },
    # Glass themes: a frosted panel over drifting colour blobs (see glass_header_svg)
    "glass": {
        "label": "Frosted Glass", "style": "glass", "bg": ["#0b0b1f", "#141433", "#1e1b4b"],
        "blobs": ["#7c3aed", "#ec4899", "#06b6d4"],
        "accent": "#a5f3fc", "accent2": "#f0abfc", "text": "#ffffff", "sub": "#e0e7ff",
        "card": "#141433", "card_text": "#e0e7ff",
    },
    "glass-aurora": {
        "label": "Aurora Glass", "style": "glass", "bg": ["#06131f", "#0b2530", "#0f3b3a"],
        "blobs": ["#10b981", "#8b5cf6", "#22d3ee"],
        "accent": "#7cffcb", "accent2": "#c4b5fd", "text": "#ffffff", "sub": "#d1fae5",
        "card": "#0b1a24", "card_text": "#d7f7ff",
    },
}

DEFAULT_LINES = [
    "> Full-stack developer 🚀",
    "> Turning repetitive work into workflows ⚙️",
    "> Python · FastAPI · React · TypeScript",
    "> LLMs + real integrations = automation 🤖",
    "> Always shipping something new...",
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def glass_header_svg(t: dict) -> str:
    name = esc(CONFIG.get("display_name", CONFIG["username"]))
    tag = esc(CONFIG.get("tagline", "</>  FULL-STACK  ·  AUTOMATION  ·  AI SYSTEMS"))
    sub = esc(CONFIG.get("subtitle", "$ building software that watches, learns & automates"))
    b1, b2, b3 = t["blobs"]
    a = t["accent"]
    # The blobs are drawn twice: sharp behind everything, then blurred and clipped
    # to the panel, which is what makes the panel read as frosted glass.
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="260" viewBox="0 0 1200 260">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg'][0]}"/><stop offset="0.6" stop-color="{t['bg'][1]}"/><stop offset="1" stop-color="{t['bg'][2]}"/>
    </linearGradient>
    <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.22"/><stop offset="0.45" stop-color="#ffffff" stop-opacity="0.06"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.7"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.12"/><stop offset="1" stop-color="#ffffff" stop-opacity="0.4"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.18"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="38"/></filter>
    <filter id="frost" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="45"/></filter>
    <filter id="glow" x="-10%" y="-30%" width="120%" height="160%"><feDropShadow dx="0" dy="2" stdDeviation="6" flood-color="#000000" flood-opacity="0.45"/></filter>
    <clipPath id="panel"><rect x="140" y="30" width="920" height="200" rx="30"/></clipPath>
    <g id="blobs">
      <circle cx="260" cy="70" r="120" fill="{b1}">
        <animateTransform attributeName="transform" type="translate" values="0 0;90 40;0 0" dur="14s" repeatCount="indefinite"/>
      </circle>
      <circle cx="640" cy="230" r="110" fill="{b2}">
        <animateTransform attributeName="transform" type="translate" values="0 0;-80 -60;0 0" dur="12s" repeatCount="indefinite"/>
      </circle>
      <circle cx="980" cy="60" r="125" fill="{b3}">
        <animateTransform attributeName="transform" type="translate" values="0 0;-70 50;0 0" dur="16s" repeatCount="indefinite"/>
      </circle>
    </g>
    <style>
      .name {{ font: 800 60px 'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif; fill: {t['text']}; letter-spacing: 2px; }}
      .sub  {{ font: 500 20px Consolas, 'Fira Code', 'Courier New', monospace; fill: {t['sub']}; }}
      .tag  {{ font: 600 14px Consolas, 'Fira Code', 'Courier New', monospace; fill: {a}; letter-spacing: 3px; }}
      .fade {{ animation: fade 1.4s ease-out both; }}
      .fade2 {{ animation: fade 1.4s ease-out 0.5s both; }}
      .cursor {{ animation: blink 1s steps(1) infinite; }}
      .sweep {{ animation: sweep 6s ease-in-out infinite; }}
      @keyframes fade {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      @keyframes sweep {{ 0% {{ transform: translateX(-500px); }} 60%,100% {{ transform: translateX(1300px); }} }}
    </style>
  </defs>

  <rect width="1200" height="260" fill="url(#bg)"/>
  <use xlink:href="#blobs" href="#blobs" filter="url(#soft)" opacity="0.75"/>

  <g clip-path="url(#panel)">
    <rect x="140" y="30" width="920" height="200" fill="{t['bg'][1]}" fill-opacity="0.55"/>
    <use xlink:href="#blobs" href="#blobs" filter="url(#frost)" opacity="0.55"/>
    <rect x="140" y="30" width="920" height="200" fill="#ffffff" fill-opacity="0.10"/>
    <rect x="140" y="30" width="920" height="200" fill="url(#sheen)"/>
    <rect class="sweep" x="0" y="30" width="160" height="200" fill="url(#shine)" transform="skewX(-20)"/>
  </g>
  <rect x="140.5" y="30.5" width="919" height="199" rx="30" fill="none" stroke="url(#edge)" stroke-width="1.5"/>

  <text class="tag" x="600" y="78" filter="url(#glow)" text-anchor="middle">{tag}</text>
  <text class="name" x="600" y="146" text-anchor="middle" filter="url(#glow)">{name}</text>
  <text class="sub" x="600" y="190" filter="url(#glow)" text-anchor="middle">{sub}<tspan class="cursor" fill="{a}"> ▌</tspan></text>
</svg>
"""


def header_svg(t: dict) -> str:
    if t.get("style") == "glass":
        return glass_header_svg(t)
    name = esc(CONFIG.get("display_name", CONFIG["username"]))
    tag = esc(CONFIG.get("tagline", "</>  FULL-STACK  ·  AUTOMATION  ·  AI SYSTEMS"))
    sub = esc(CONFIG.get("subtitle", "$ building software that watches, learns & automates"))
    a, a2 = t["accent"], t["accent2"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="260" viewBox="0 0 1200 260">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg'][0]}"/><stop offset="0.6" stop-color="{t['bg'][1]}"/><stop offset="1" stop-color="{t['bg'][2]}"/>
    </linearGradient>
    <linearGradient id="wave" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{a}" stop-opacity="0.15"/><stop offset="0.5" stop-color="{a}" stop-opacity="0.35"/><stop offset="1" stop-color="{a2}" stop-opacity="0.2"/>
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="{a}" stroke-opacity="0.08"/>
    </pattern>
    <filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <style>
      .name {{ font: 800 64px 'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif; fill: {t['text']}; letter-spacing: 2px; }}
      .sub  {{ font: 500 21px Consolas, 'Fira Code', 'Courier New', monospace; fill: {t['sub']}; }}
      .tag  {{ font: 600 14px Consolas, 'Fira Code', 'Courier New', monospace; fill: {a}; letter-spacing: 3px; }}
      .fade {{ animation: fade 1.4s ease-out both; }}
      .fade2 {{ animation: fade 1.4s ease-out 0.5s both; }}
      .cursor {{ animation: blink 1s steps(1) infinite; }}
      .node {{ animation: pulse 2.4s ease-in-out infinite; }}
      .n2 {{ animation-delay: .8s; }} .n3 {{ animation-delay: 1.6s; }}
      @keyframes fade {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: none; }} }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      @keyframes pulse {{ 0%,100% {{ opacity: .25; }} 50% {{ opacity: 1; }} }}
    </style>
  </defs>
  <rect width="1200" height="260" fill="url(#bg)"/>
  <rect width="1200" height="260" fill="url(#grid)"/>
  <g stroke="{a}" stroke-opacity="0.35" fill="none" stroke-width="1.5">
    <path d="M60 40H180L210 70H300"/><path d="M1140 50H1020L990 80H900"/><path d="M80 200H160L190 170H260"/>
  </g>
  <g fill="{a}" filter="url(#glow)">
    <circle class="node" cx="300" cy="70" r="4"/><circle class="node n2" cx="900" cy="80" r="4" fill="{a2}"/><circle class="node n3" cx="260" cy="170" r="4"/>
  </g>
  <path fill="url(#wave)">
    <animate attributeName="d" dur="8s" repeatCount="indefinite" values="M0 215 C200 185 400 245 600 215 C800 185 1000 245 1200 215 V260 H0Z;M0 215 C200 245 400 185 600 215 C800 245 1000 185 1200 215 V260 H0Z;M0 215 C200 185 400 245 600 215 C800 185 1000 245 1200 215 V260 H0Z"/>
  </path>
  <path fill="{a}" fill-opacity="0.12">
    <animate attributeName="d" dur="6s" repeatCount="indefinite" values="M0 230 C300 250 500 210 800 232 C1000 246 1100 224 1200 230 V260 H0Z;M0 230 C300 210 500 250 800 228 C1000 214 1100 236 1200 230 V260 H0Z;M0 230 C300 250 500 210 800 232 C1000 246 1100 224 1200 230 V260 H0Z"/>
  </path>
  <text class="tag" x="600" y="62" text-anchor="middle">{tag}</text>
  <text class="name" x="600" y="132" text-anchor="middle" filter="url(#glow)">{name}</text>
  <text class="sub" x="600" y="174" text-anchor="middle">{sub}<tspan class="cursor" fill="{a}"> ▌</tspan></text>
</svg>
"""


def footer_svg(t: dict) -> str:
    stops = t.get("blobs") or [t["accent"], t["bg"][2], t["bg"][0]]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="110" viewBox="0 0 1200 110">
  <defs>
    <linearGradient id="f" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{stops[0]}"/><stop offset="0.5" stop-color="{stops[1]}"/><stop offset="1" stop-color="{stops[2]}"/>
    </linearGradient>
  </defs>
  <path fill="url(#f)" fill-opacity="0.85">
    <animate attributeName="d" dur="8s" repeatCount="indefinite" values="M0 40 C200 10 400 70 600 40 C800 10 1000 70 1200 40 V110 H0Z;M0 40 C200 70 400 10 600 40 C800 70 1000 10 1200 40 V110 H0Z;M0 40 C200 10 400 70 600 40 C800 10 1000 70 1200 40 V110 H0Z"/>
  </path>
</svg>
"""


def hx(c: str) -> str:
    return c.lstrip("#")


def header_section(t: dict) -> str:
    user = CONFIG["username"]
    lines = ";".join(urllib.parse.quote_plus(l) for l in CONFIG.get("typing_lines", DEFAULT_LINES))
    typing = (f"https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=900"
              f"&color={hx(t['accent'])}&center=true&vCenter=true&width=680&lines={lines}")
    dark = hx(t["bg"][0])
    return f"""<p align="center">
  <img src="./assets/header.svg" width="100%" alt="{esc(CONFIG.get('display_name', user))}" />
</p>

<p align="center">
  <a href="https://github.com/{user}">
    <img src="{typing}" alt="typing intro" />
  </a>
</p>

<p align="center">
  <a href="https://github.com/{user}?tab=followers"><img src="https://img.shields.io/github/followers/{user}?style=for-the-badge&logo=github&color={hx(t['accent2'])}&labelColor={dark}" alt="followers" /></a>
  <img src="https://img.shields.io/badge/status-building%20in%20public-{hx(t['accent'])}?style=for-the-badge&labelColor={dark}" alt="status" />
</p>"""


def stats_section(t: dict) -> str:
    user = CONFIG["username"]
    a, a2, card, txt = hx(t["accent"]), hx(t["accent2"]), hx(t["card"]), hx(t["card_text"])
    stats = (f"https://github-readme-stats.vercel.app/api?username={user}&show_icons=true&hide_border=true"
             f"&count_private=true&include_all_commits=true&rank_icon=github"
             f"&bg_color={card}&title_color={a}&icon_color={a2}&text_color={txt}&ring_color={a}")
    streak = (f"https://streak-stats.demolab.com?user={user}&hide_border=true&background={card}"
              f"&ring={a}&fire={a2}&currStreakNum={a}&currStreakLabel={a}&sideNums={txt}"
              f"&sideLabels={txt}&dates={txt}&stroke={a2}")
    return f"""<p align="center">
  <img height="170" src="{stats}" alt="GitHub stats" />
  <img height="170" src="{streak}" alt="GitHub streak" />
</p>"""


def snake_outputs(t: dict) -> str:
    # Contribution levels go from empty -> busiest; tint them from the theme.
    dots = ",".join([t["card"] if t["bg"][0] != "#ffffff" else "#ebedf0",
                     t["bg"][2], t["accent2"], t["accent"], t["text"]])
    return (f"dist/github-snake.svg?color_snake={t['accent2']}\n"
            f"dist/github-snake-dark.svg?palette=github-dark&color_snake={t['accent']}&color_dots={dots}")


def current() -> dict:
    name = CONFIG.get("theme", "cyber")
    if name not in THEMES:
        sys.exit(f"Unknown theme '{name}'. Choose one of: {', '.join(THEMES)}")
    return THEMES[name]


def replace_section(text: str, name: str, content: str) -> str:
    return re.sub(rf"(<!--START:{name}-->).*?(<!--END:{name}-->)",
                  lambda m: f"{m.group(1)}\n{content}\n{m.group(2)}", text, flags=re.S)


def apply() -> None:
    t = current()
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets/header.svg").write_text(header_svg(t), encoding="utf-8")
    (ROOT / "assets/footer.svg").write_text(footer_svg(t), encoding="utf-8")
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = replace_section(text, "HEADER", header_section(t))
    text = replace_section(text, "STATS", stats_section(t))
    readme.write_text(text, encoding="utf-8")


def preview(path: str) -> None:
    cards = []
    for key, t in THEMES.items():
        cards.append(f"""<section><h2><code>"theme": "{key}"</code> &nbsp;·&nbsp; {t['label']}</h2>
<div class="frame" style="background:{t['card']}">{header_svg(t)}
<div class="row">{''.join(f'<span style="background:{c}" title="{c}"></span>' for c in [*t['bg'], t['accent'], t['accent2']])}</div>
{footer_svg(t)}</div></section>""")
    Path(path).write_text(f"""<!doctype html><html><head><meta charset="utf-8"><title>Profile themes</title>
<style>body{{background:#0d1117;color:#c9d1d9;font:15px 'Segoe UI',sans-serif;max-width:1000px;margin:24px auto;padding:0 16px}}
h1{{font-weight:700}} h2{{font-size:16px;margin:28px 0 8px}} code{{color:#7ee787}}
.frame{{border:1px solid #30363d;border-radius:10px;overflow:hidden}} .frame svg{{display:block;width:100%;height:auto}}
.row{{display:flex;gap:8px;padding:12px}} .row span{{width:36px;height:22px;border-radius:5px;border:1px solid #30363d}}</style>
</head><body><h1>Profile README themes</h1><p>Each card shows the header, the palette and the footer wave.</p>{''.join(cards)}</body></html>""",
                          encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        preview(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == "--snake":
        print(snake_outputs(current()))
    else:
        apply()
