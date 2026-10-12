"""Regenerate the dynamic sections of the profile README.

Reads every public, non-fork repo of the configured user and rebuilds:
  SKILLS    badges for languages, frameworks and tools found in the repos
  LANGS     a terminal-style language breakdown
  PROJECTS  the most recently pushed repos
  ACTIVITY  the latest public events
  UPDATED   a timestamp

Only the text between <!--START:X--> and <!--END:X--> markers is replaced,
so everything else in README.md can be edited by hand. Standard library only.
"""

from __future__ import annotations

import base64
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CONFIG = json.loads((ROOT / "profile.config.json").read_text(encoding="utf-8"))
USER = CONFIG["username"]
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"

# key -> (label, hex colour, simple-icons logo slug, category)
SKILLS: dict[str, tuple[str, str, str, str]] = {
    # Languages (keys match GitHub's language names, lower-cased)
    "python": ("Python", "3776AB", "python", "lang"),
    "typescript": ("TypeScript", "3178C6", "typescript", "lang"),
    "javascript": ("JavaScript", "F7DF1E", "javascript", "lang"),
    "html": ("HTML5", "E34F26", "html5", "lang"),
    "css": ("CSS3", "1572B6", "css3", "lang"),
    "java": ("Java", "ED8B00", "openjdk", "lang"),
    "c++": ("C++", "00599C", "cplusplus", "lang"),
    "c": ("C", "A8B9CC", "c", "lang"),
    "c#": ("C%23", "512BD4", "dotnet", "lang"),
    "go": ("Go", "00ADD8", "go", "lang"),
    "rust": ("Rust", "000000", "rust", "lang"),
    "kotlin": ("Kotlin", "7F52FF", "kotlin", "lang"),
    "dart": ("Dart", "0175C2", "dart", "lang"),
    "shell": ("Bash", "4EAA25", "gnubash", "lang"),
    "powershell": ("PowerShell", "5391FE", "powershell", "lang"),
    "jupyter notebook": ("Jupyter", "F37626", "jupyter", "lang"),
    "sql": ("SQL", "4479A1", "mysql", "lang"),
    # Frameworks & libraries (keys match package names)
    "fastapi": ("FastAPI", "009688", "fastapi", "fw"),
    "flask": ("Flask", "000000", "flask", "fw"),
    "django": ("Django", "092E20", "django", "fw"),
    "pydantic": ("Pydantic", "E92063", "pydantic", "fw"),
    "uvicorn": ("Uvicorn", "499848", "gunicorn", "fw"),
    "sqlalchemy": ("SQLAlchemy", "D71F00", "sqlalchemy", "fw"),
    "pandas": ("Pandas", "150458", "pandas", "fw"),
    "numpy": ("NumPy", "013243", "numpy", "fw"),
    "scikit-learn": ("scikit--learn", "F7931E", "scikitlearn", "fw"),
    "tensorflow": ("TensorFlow", "FF6F00", "tensorflow", "fw"),
    "torch": ("PyTorch", "EE4C2C", "pytorch", "fw"),
    "streamlit": ("Streamlit", "FF4B4B", "streamlit", "fw"),
    "langchain": ("LangChain", "1C3C3C", "langchain", "fw"),
    "openai": ("OpenAI", "412991", "openai", "fw"),
    "anthropic": ("Claude API", "D97757", "anthropic", "fw"),
    "@anthropic-ai/sdk": ("Claude API", "D97757", "anthropic", "fw"),
    "selenium": ("Selenium", "43B02A", "selenium", "fw"),
    "playwright": ("Playwright", "2EAD33", "playwright", "fw"),
    "pytest": ("Pytest", "0A9EDC", "pytest", "fw"),
    "react": ("React", "61DAFB", "react", "fw"),
    "next": ("Next.js", "000000", "nextdotjs", "fw"),
    "vue": ("Vue.js", "4FC08D", "vuedotjs", "fw"),
    "svelte": ("Svelte", "FF3E00", "svelte", "fw"),
    "express": ("Express", "000000", "express", "fw"),
    "tailwindcss": ("Tailwind CSS", "06B6D4", "tailwindcss", "fw"),
    "electron": ("Electron", "47848F", "electron", "fw"),
    "three": ("Three.js", "000000", "threedotjs", "fw"),
    "socket.io": ("Socket.io", "010101", "socketdotio", "fw"),
    # Tools, platforms & integrations
    "vite": ("Vite", "646CFF", "vite", "tool"),
    "docker": ("Docker", "2496ED", "docker", "tool"),
    "github-actions": ("GitHub Actions", "2088FF", "githubactions", "tool"),
    "git": ("Git", "F05032", "git", "tool"),
    "sqlite": ("SQLite", "003B57", "sqlite", "tool"),
    "aiosqlite": ("SQLite", "003B57", "sqlite", "tool"),
    "postgresql": ("PostgreSQL", "4169E1", "postgresql", "tool"),
    "psycopg2": ("PostgreSQL", "4169E1", "postgresql", "tool"),
    "pymongo": ("MongoDB", "47A248", "mongodb", "tool"),
    "mongoose": ("MongoDB", "47A248", "mongodb", "tool"),
    "redis": ("Redis", "DC382D", "redis", "tool"),
    "firebase": ("Firebase", "FFCA28", "firebase", "tool"),
    "google-api-python-client": ("Google APIs", "4285F4", "google", "tool"),
    "googleapis": ("Google APIs", "4285F4", "google", "tool"),
    "slack_sdk": ("Slack API", "4A154B", "slack", "tool"),
    "@slack/web-api": ("Slack API", "4A154B", "slack", "tool"),
    "chrome-extension": ("Chrome Extensions", "4285F4", "googlechrome", "tool"),
    "rest-api": ("REST APIs", "FF6C37", "postman", "tool"),
    "llm": ("LLMs", "8A2BE2", "openai", "tool"),
}

CATEGORY_TITLES = {
    "lang": "💻 Languages",
    "fw": "⚙️ Frameworks & Libraries",
    "tool": "🛠️ Tools, Platforms & Integrations",
}

DEP_FILES = ("package.json", "requirements.txt", "pyproject.toml", "Pipfile")
SKIP_DIRS = ("node_modules/", "venv/", ".venv/", "dist/", "build/", "site-packages/")


def request(url: str, raw: bool = False):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": f"{USER}-profile-readme"}
    if TOKEN and url.startswith(API):
        headers["Authorization"] = f"Bearer {TOKEN}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
                body = r.read().decode("utf-8", errors="replace")
            return body if raw else json.loads(body)
        except urllib.error.HTTPError as e:
            if e.code in (404, 409):  # missing file / empty repo
                return None
            if e.code < 500 or attempt == 2:
                raise
        except (urllib.error.URLError, http.client.HTTPException, ConnectionError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(2 * (attempt + 1))


def fetch_repos() -> list[dict]:
    repos, page = [], 1
    while True:
        batch = request(f"{API}/users/{USER}/repos?per_page=100&page={page}&sort=pushed")
        if not batch:
            break
        repos += batch
        page += 1
    excluded = {n.lower() for n in CONFIG.get("exclude_repos", [])} | {USER.lower()}
    return [r for r in repos if not r["fork"] and not r["archived"] and r["name"].lower() not in excluded]


def packages_from(path: str, text: str) -> set[str]:
    if path.endswith("package.json"):
        try:
            data = json.loads(text)
        except ValueError:
            return set()
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        return {d.lower() for d in deps}
    # Python dependency files: first token on each line / quoted names in pyproject
    names = set()
    for line in text.splitlines():
        line = line.strip().strip("\"',")
        m = re.match(r"([A-Za-z0-9_.\-]+)", line)
        if m and not line.startswith("#"):
            names.add(m.group(1).lower())
    return names


def scan_repo(repo: dict) -> set[str]:
    """Return skill keys detected from a repo's files, dependencies and topics."""
    found = set(t.lower() for t in repo.get("topics", []))
    tree = request(f"{API}/repos/{repo['full_name']}/git/trees/{repo['default_branch']}?recursive=1")
    if not tree:
        return found
    paths = [t["path"] for t in tree.get("tree", []) if t["type"] == "blob"]
    paths = [p for p in paths if not any(s in p for s in SKIP_DIRS)]
    for p in paths:
        name = p.rsplit("/", 1)[-1]
        if name == "Dockerfile" or name.startswith("docker-compose"):
            found.add("docker")
        elif p.startswith(".github/workflows/"):
            found.add("github-actions")
        elif name == "manifest.json" and "extension" in p.lower():
            found.add("chrome-extension")
        elif name.endswith((".db", ".sqlite", ".sqlite3")):
            found.add("sqlite")
    for p in [p for p in paths if p.rsplit("/", 1)[-1] in DEP_FILES][:12]:
        url = f"https://raw.githubusercontent.com/{repo['full_name']}/{repo['default_branch']}/{urllib.parse.quote(p)}"
        text = request(url, raw=True)
        if text:
            found |= packages_from(p, text)
    return found


def badge(key: str) -> str:
    label, color, logo, _ = SKILLS[key]
    return (f'<img src="https://img.shields.io/badge/{label.replace(" ", "%20")}-{color}'
            f'?style=for-the-badge&logo={logo}&logoColor=white" alt="{label.replace("%23", "#").replace("--", "-")}" />')


def render_skills(detected: Counter) -> str:
    hidden = {h.lower() for h in CONFIG.get("hide_skills", [])}
    keys = set(detected) | {s.lower() for s in CONFIG.get("always_show_skills", [])}
    keys = [k for k in keys if k in SKILLS and k not in hidden]
    out, seen_labels = [], set()
    for cat, title in CATEGORY_TITLES.items():
        # most-used first; de-duplicate aliases that share a label (e.g. anthropic + @anthropic-ai/sdk)
        items = sorted((k for k in keys if SKILLS[k][3] == cat), key=lambda k: (-detected[k], SKILLS[k][0]))
        badges = []
        for k in items:
            if SKILLS[k][0] not in seen_labels:
                seen_labels.add(SKILLS[k][0])
                badges.append(badge(k))
        if badges:
            out.append(f"<h4>{title}</h4>\n<p>\n  " + "\n  ".join(badges) + "\n</p>")
    return "\n".join(out)


def render_langs(lang_bytes: Counter) -> str:
    total = sum(lang_bytes.values()) or 1
    lines = ["```text", f"$ git-stats --languages --user {USER}", ""]
    for lang, n in lang_bytes.most_common(8):
        pct = n / total * 100
        filled = round(pct / 4)
        lines.append(f"{lang:<18}{'█' * filled}{'░' * (25 - filled)}  {pct:5.1f} %")
    lines.append("```")
    return "\n".join(lines)


def ago(iso: str) -> str:
    delta = datetime.now(timezone.utc) - datetime.fromisoformat(iso.replace("Z", "+00:00"))
    if delta.days >= 30:
        return f"{delta.days // 30} mo ago"
    if delta.days >= 1:
        return f"{delta.days} d ago"
    hours = delta.seconds // 3600
    return f"{hours} h ago" if hours else "just now"


def render_projects(repos: list[dict]) -> str:
    rows = ["| 🚀 Project | 📝 What it does | 🧰 Stack | ⭐ | 🕒 Updated |", "|---|---|---|:-:|---|"]
    for r in repos[: CONFIG.get("max_projects", 6)]:
        desc = (r["description"] or "_Fresh build — description coming soon._").replace("|", "\\|")
        if len(desc) > 110:
            desc = desc[:107].rstrip() + "…"
        rows.append(f"| [**{r['name']}**]({r['html_url']}) | {desc} | `{r['language'] or '—'}` "
                    f"| {r['stargazers_count']} | {ago(r['pushed_at'])} |")
    return "\n".join(rows)


def render_activity() -> str:
    events = request(f"{API}/users/{USER}/events/public?per_page=50") or []
    lines = []
    for e in events:
        repo = e["repo"]["name"]
        link = f"[{repo}](https://github.com/{repo})"
        p = e.get("payload", {})
        t = e["type"]
        if t == "PushEvent":
            n = p.get("size") or len(p.get("commits", [])) or 1
            text = f"⬆️ Pushed {n} commit{'s' if n != 1 else ''} to {link}"
        elif t == "CreateEvent" and p.get("ref_type") == "repository":
            text = f"✨ Started a new project {link}"
        elif t == "PullRequestEvent":
            text = f"🔀 {p.get('action', '').capitalize()} PR #{p['pull_request']['number']} in {link}"
        elif t == "IssuesEvent":
            text = f"🐛 {p.get('action', '').capitalize()} issue #{p['issue']['number']} in {link}"
        elif t == "ReleaseEvent":
            text = f"📦 Released {p['release'].get('tag_name', '')} of {link}"
        elif t == "WatchEvent":
            text = f"⭐ Starred {link}"
        else:
            continue
        if lines and lines[-1].split(" · ")[0] == text:
            continue  # collapse consecutive duplicates
        lines.append(f"{text} · <sub>{ago(e['created_at'])}</sub>")
        if len(lines) >= CONFIG.get("max_activity", 6):
            break
    return "\n".join(f"{i}. {l}" for i, l in enumerate(lines, 1)) or "_Quiet for now — something is cooking._ 🧪"


def replace_section(text: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!--START:{name}-->).*?(<!--END:{name}-->)", re.S)
    if not pattern.search(text):
        print(f"warning: markers for {name} not found", file=sys.stderr)
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(2)}", text)


def main() -> None:
    repos = fetch_repos()
    lang_bytes: Counter = Counter()
    detected: Counter = Counter()
    for r in repos:
        try:
            langs = request(r["languages_url"]) or {}
            total = sum(langs.values()) or 1
            # Weight every repo equally so one big (or vendored) repo can't drown the rest,
            # and ignore languages under 5% of a repo (usually vendored or generated code).
            share = {l: n / total for l, n in langs.items() if n / total >= 0.05}
            lang_bytes.update(share)
            detected.update({l.lower() for l in share})
            detected.update(k for k in scan_repo(r) if k in SKILLS)
            print(f"scanned {r['name']}", file=sys.stderr)
        except Exception as e:  # one bad repo shouldn't block the whole update
            print(f"skipped {r['name']}: {e!r}", file=sys.stderr)

    text = README.read_text(encoding="utf-8")
    text = replace_section(text, "SKILLS", render_skills(detected))
    text = replace_section(text, "LANGS", render_langs(lang_bytes))
    text = replace_section(text, "PROJECTS", render_projects(repos))
    text = replace_section(text, "ACTIVITY", render_activity())
    stamp = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    text = replace_section(text, "UPDATED",
                           f"<sub>🤖 Auto-generated by GitHub Actions · last sync {stamp} · "
                           f"{len(repos)} public repos scanned</sub>")
    README.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
