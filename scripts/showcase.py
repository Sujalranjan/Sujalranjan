"""Hand-curated sections of the profile README, driven by profile.config.json.

  WHOAMI    the `whoami` code card; "building" follows the most recently pushed repo
  IMPACT    headline numbers ("auto:contributions" is filled from the calendar)
  FEATURED  project cards
  CONNECT   social links (only the ones filled in are shown)

Edit the config, not this file, to change what these sections say.
"""

from __future__ import annotations

import html
import json

# label, colour, simple-icons slug for the small stack badges on project cards
STACK = {
    "python": ("Python", "3776AB", "python"),
    "typescript": ("TypeScript", "3178C6", "typescript"),
    "fastapi": ("FastAPI", "009688", "fastapi"),
    "react": ("React", "20232A", "react"),
    "next": ("Next.js", "000000", "nextdotjs"),
    "postgresql": ("PostgreSQL", "4169E1", "postgresql"),
    "pgvector": ("pgvector", "336791", "postgresql"),
    "docker": ("Docker", "2496ED", "docker"),
    "streamlit": ("Streamlit", "FF4B4B", "streamlit"),
    "airflow": ("Airflow", "017CEE", "apacheairflow"),
    "mlflow": ("MLflow", "0194E2", "mlflow"),
    "scikit-learn": ("scikit--learn", "F7931E", "scikitlearn"),
    "tree-sitter": ("Tree--sitter", "5E7C3C", "treesitter"),
    "gmail": ("Gmail API", "EA4335", "gmail"),
    "slack": ("Slack API", "4A154B", "slack"),
    "llm": ("LLMs", "8A2BE2", "openai"),
}

SOCIALS = {
    "linkedin": ("LinkedIn", "0A66C2", "linkedin", "https://www.linkedin.com/in/{}"),
    "x": ("X", "000000", "x", "https://x.com/{}"),
    "leetcode": ("LeetCode", "FFA116", "leetcode", "https://leetcode.com/u/{}"),
    "kaggle": ("Kaggle", "20BEFF", "kaggle", "https://www.kaggle.com/{}"),
    "portfolio": ("Portfolio", "7CFFCB", "googlechrome", "{}"),
    "email": ("Email", "D14836", "gmail", "mailto:{}"),
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def stack_badge(key: str) -> str:
    label, color, logo = STACK.get(key, (key, "555555", ""))
    return (f'<img src="https://img.shields.io/badge/{label.replace(" ", "%20")}-{color}'
            f'?style=flat-square&logo={logo}&logoColor=white" alt="{label.replace("--", "-")}" />')


def describe(repo: dict, config: dict) -> str:
    return config.get("descriptions", {}).get(repo["name"]) or repo.get("description") or ""


def render_whoami(config: dict, repos: list[dict]) -> str:
    w = config.get("whoami", {})
    own = [r for r in repos if not r["fork"]]
    latest = own[0] if own else None
    building = ""
    if latest:
        d = describe(latest, config).split(".")[0]
        building = f"{latest['name']}: {d}" if d else latest["name"]
        if len(building) > 74:
            building = building[:71].rstrip() + "..."

    def py_list(items: list[str]) -> str:
        return "[" + ", ".join(json.dumps(i, ensure_ascii=False) for i in items) + "]"

    lines = ["```python", f"class {config.get('display_name', config['username']).replace(' ', '')}:"]
    rows = [("role", json.dumps(w.get("role", ""), ensure_ascii=False))]
    if building:
        rows.append(("building", json.dumps(building, ensure_ascii=False)))
    for key in ("focus", "learning", "open_to"):
        if w.get(key):
            rows.append((key, py_list(w[key])))
    if w.get("philosophy"):
        rows.append(("philosophy", json.dumps(w["philosophy"], ensure_ascii=False)))
    width = max(len(k) for k, _ in rows)
    lines += [f"    {k:<{width}} = {v}" for k, v in rows]
    lines += ["", "    def say_hi(self):",
              f"        print({json.dumps(w.get('hello', 'Thanks for dropping by!'), ensure_ascii=False)})",
              "```"]
    return "\n".join(lines)


def render_impact(config: dict, contributions: int) -> str:
    tiles = config.get("impact", [])
    if not tiles:
        return ""
    cells = []
    for t in tiles:
        value = t["value"]
        if value == "auto:contributions":
            if not contributions:
                continue
            value = f"{contributions:,}"
        src = t.get("source")
        src_html = (f'<br/><a href="https://github.com/{config["username"]}/{src}">{esc(t.get("source_label", src))}</a>'
                    if src else "")
        cells.append(f'<td align="center" width="{100 // len(tiles)}%"><h2>{esc(value)}</h2>'
                     f'<sub>{esc(t["label"])}{src_html}</sub></td>')
    return "<table>\n<tr>\n" + "\n".join(cells) + "\n</tr>\n</table>"


def render_featured(config: dict) -> str:
    user = config["username"]
    cards = []
    for p in config.get("featured", []):
        url = f"https://github.com/{user}/{p['repo']}"
        title = esc(p.get("title", p["repo"]))
        tags = []
        if p.get("team"):
            tags.append("👥 Team project")
        if p.get("demo"):
            tags.append("🟢 Live demo")
        tag_line = f"<sub>{' · '.join(tags)}</sub><br/>" if tags else ""
        points = "".join(f"<li>{esc(x)}</li>" for x in p.get("points", []))
        links = [f'<a href="{url}"><b>Code →</b></a>']
        if p.get("demo"):
            links.append(f'<a href="{esc(p["demo"])}"><b>Live demo ↗</b></a>')
        cards.append(
            f'<td width="50%" valign="top">\n'
            f'<h3>{p.get("emoji", "🚀")} <a href="{url}">{title}</a></h3>\n'
            f'{tag_line}<p>{esc(p["tagline"])}</p>\n'
            f'<ul>{points}</ul>\n'
            f'<p>{" ".join(stack_badge(s) for s in p.get("stack", []))}</p>\n'
            f'<p>{" &nbsp;·&nbsp; ".join(links)}</p>\n'
            f'</td>')
    rows = ["<tr>\n" + "\n".join(cards[i:i + 2]) + "\n</tr>" for i in range(0, len(cards), 2)]
    return "<table>\n" + "\n".join(rows) + "\n</table>" if rows else ""


def render_connect(config: dict) -> str:
    user = config["username"]
    links = [f'<a href="https://github.com/{user}"><img src="https://img.shields.io/badge/GitHub-{user}-181717'
             f'?style=for-the-badge&logo=github" alt="GitHub" /></a>']
    for key, value in config.get("socials", {}).items():
        if not value or key not in SOCIALS:
            continue
        label, color, logo, pattern = SOCIALS[key]
        links.append(f'<a href="{esc(pattern.format(value))}"><img src="https://img.shields.io/badge/{label}-{color}'
                     f'?style=for-the-badge&logo={logo}&logoColor=white" alt="{label}" /></a>')
    return '<p align="center">\n  ' + "\n  ".join(links) + "\n</p>"
