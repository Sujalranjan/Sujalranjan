"""Render an animated snake that hunts the cells of the contribution calendar.

Writes assets/snake-dark.svg and assets/snake-light.svg, coloured from the
active theme. Pure SVG + SMIL animation, so it plays inside a GitHub README.

How it moves:
  * the snake visits every active day (nearest-first, drifting left -> right),
  * waypoints are joined with a centripetal Catmull-Rom spline (smooth, no loops),
  * a sideways sine wave is added on top for a slithering, lateral-undulation look,
  * the body is a stack of round-capped strokes of decreasing width and growing
    length, all ending at the head, which gives a tapered tail.
"""

from __future__ import annotations

import math
import random
import re
import urllib.request
from pathlib import Path

import theme

ROOT = Path(__file__).resolve().parent.parent
USER = theme.CONFIG["username"]

CELL, GAP = 11, 4
PITCH = CELL + GAP
PAD_X, PAD_TOP, PAD_BOTTOM = 26, 22, 34
SPEED = 95            # px per second
PAUSE = 2.5           # seconds of empty board before the loop restarts
WAVE_AMP, WAVE_LEN = 3.2, 52


# ── data ────────────────────────────────────────────────────────────────────

def fetch_calendar() -> tuple[list[tuple[int, int, int]], int]:
    """Return ([(week, weekday, level)], total contributions) from the public calendar."""
    req = urllib.request.Request(f"https://github.com/users/{USER}/contributions",
                                 headers={"User-Agent": f"{USER}-profile-readme"})
    html = ""
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                html = r.read().decode("utf-8", errors="replace")
            break
        except Exception:
            if attempt == 2:
                raise
    cells = [(int(c), int(r), int(lv)) for r, c, lv in re.findall(
        r'id="contribution-day-component-(\d+)-(\d+)" data-level="(\d)"', html)]
    m = re.search(r"([\d,]+)\s+contributions?\s+in the last year", html)
    return cells, int(m.group(1).replace(",", "")) if m else 0


# ── geometry ────────────────────────────────────────────────────────────────

def centre(week: int, day: int) -> tuple[float, float]:
    return PAD_X + week * PITCH + CELL / 2, PAD_TOP + day * PITCH + CELL / 2


def plan_route(targets: list[tuple[float, float]], width: float, mid: float) -> list[tuple[float, float]]:
    """Greedy hunt: nearest uneaten cell, with a penalty for doubling back."""
    pos, left, route = (-60.0, mid), list(targets), [(-60.0, mid)]
    while left:
        def cost(p):
            dx, dy = p[0] - pos[0], p[1] - pos[1]
            return math.hypot(dx, dy) + (abs(dx) * 1.6 if dx < 0 else 0)
        nxt = min(left, key=cost)
        left.remove(nxt)
        route.append(nxt)
        pos = nxt
    route.append((width + 60.0, mid))
    return route


def catmull_rom(points: list[tuple[float, float]], step: float = 2.5) -> list[tuple[float, float]]:
    """Centripetal Catmull-Rom through points, sampled roughly every `step` px."""
    pts = [points[0], *points, points[-1]]
    out: list[tuple[float, float]] = []

    def tj(ti, a, b):
        return ti + max(math.hypot(b[0] - a[0], b[1] - a[1]), 1e-3) ** 0.5

    for i in range(len(pts) - 3):
        p0, p1, p2, p3 = pts[i:i + 4]
        t0 = 0.0
        t1 = tj(t0, p0, p1)
        t2 = tj(t1, p1, p2)
        t3 = tj(t2, p2, p3)
        n = max(2, int(math.hypot(p2[0] - p1[0], p2[1] - p1[1]) / step))
        for k in range(n):
            t = t1 + (t2 - t1) * k / n

            def lerp(a, b, ta, tb):
                if tb - ta < 1e-9:
                    return a
                return ((tb - t) / (tb - ta) * a[0] + (t - ta) / (tb - ta) * b[0],
                        (tb - t) / (tb - ta) * a[1] + (t - ta) / (tb - ta) * b[1])
            a1, a2, a3 = lerp(p0, p1, t0, t1), lerp(p1, p2, t1, t2), lerp(p2, p3, t2, t3)
            b1, b2 = lerp(a1, a2, t0, t2), lerp(a2, a3, t1, t3)
            out.append(lerp(b1, b2, t1, t2))
    out.append(points[-1])
    return out


def slither(path: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Add a sideways sine wave along the path (lateral undulation)."""
    out, s = [], 0.0
    for i, (x, y) in enumerate(path):
        if i:
            s += math.hypot(x - path[i - 1][0], y - path[i - 1][1])
        a, b = path[max(i - 1, 0)], path[min(i + 1, len(path) - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        n = math.hypot(tx, ty) or 1
        off = WAVE_AMP * math.sin(2 * math.pi * s / WAVE_LEN)
        out.append((x - ty / n * off, y + tx / n * off))
    return out


def lengths(path: list[tuple[float, float]]) -> list[float]:
    acc = [0.0]
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        acc.append(acc[-1] + math.hypot(x1 - x0, y1 - y0))
    return acc


# ── colour helpers ──────────────────────────────────────────────────────────

def mix(c1: str, c2: str, f: float) -> str:
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * f):02x}" for x, y in zip(a, b))


def palette(t: dict, dark: bool) -> dict:
    accent = t["accent"]
    if dark:
        empty = "#161b22"
        levels = [empty] + [mix(empty, accent, f) for f in (0.3, 0.5, 0.72, 0.95)]
        label = "#8b949e"
    else:
        empty = "#ebedf0"
        deep = mix(accent, "#000000", 0.45)
        levels = [empty] + [mix(empty, deep, f) for f in (0.3, 0.5, 0.75, 1.0)]
        label = "#57606a"
    return {
        "empty": empty, "levels": levels, "label": label,
        "body": accent if dark else mix(accent, "#000000", 0.25),
        "outline": mix(t["bg"][0], "#000000", 0.3),
        "bands": mix(t["bg"][2], "#000000", 0.35),
        "stripe": mix(accent, "#ffffff", 0.6),
        "pop": t["accent2"],
    }


# ── svg ─────────────────────────────────────────────────────────────────────

def f(x: float) -> str:
    return f"{x:.1f}".rstrip("0").rstrip(".")


def render(cells, total, t: dict, dark: bool) -> str:
    weeks = max((c[0] for c in cells), default=52) + 1
    width = PAD_X * 2 + weeks * PITCH - GAP
    height = PAD_TOP + 7 * PITCH - GAP + PAD_BOTTOM
    mid = PAD_TOP + 3 * PITCH + CELL / 2
    pal = palette(t, dark)

    active = [c for c in cells if c[2] > 0]
    targets = [centre(w, d) for w, d, _ in active]
    if len(targets) < 18:  # quiet year: give the snake some ground to explore
        rnd = random.Random(7)
        targets += [centre(rnd.randrange(weeks), rnd.randrange(7)) for _ in range(18 - len(targets))]
    route = plan_route(targets, width, mid)
    path = slither(catmull_rom(route))
    acc = lengths(path)
    total_len = acc[-1]
    move = total_len / SPEED
    dur = move + PAUSE
    mf = move / dur  # fraction of the loop spent moving

    # time at which the head reaches each target = path distance of its nearest sample
    eat_at: dict[tuple[float, float], float] = {}
    for tx, ty in targets:
        best = min(range(len(path)), key=lambda i: (path[i][0] - tx) ** 2 + (path[i][1] - ty) ** 2)
        eat_at[(tx, ty)] = acc[best] / total_len * mf

    d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in path)
    D = f"{dur:.2f}s"

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
           f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           "<defs>",
           f'<path id="route" d="{d}" fill="none"/>',
           '<filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">'
           '<feDropShadow dx="0" dy="2.5" stdDeviation="2" flood-color="#000" flood-opacity="0.45"/></filter>',
           "</defs>"]

    # board
    out.append("<g>")
    for w, day, lv in cells:
        x, y = PAD_X + w * PITCH, PAD_TOP + day * PITCH
        col = pal["levels"][lv]
        rect = f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{col}"'
        if lv == 0:
            out.append(rect + "/>")
            continue
        te = eat_at[centre(w, day)]
        k1, k2 = max(te, 0.0005), min(te + 0.004, 0.97)
        out.append(rect + f'><animate attributeName="fill" dur="{D}" repeatCount="indefinite" '
                   f'values="{col};{col};{pal["empty"]};{pal["empty"]};{col}" '
                   f'keyTimes="0;{k1:.4f};{k2:.4f};0.985;1"/></rect>')
        # pop ring
        cx, cy = centre(w, day)
        p2 = min(te + 0.02, 0.98)
        out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="0" fill="none" stroke="{pal["pop"]}" stroke-width="1.6" opacity="0">'
                   f'<animate attributeName="r" dur="{D}" repeatCount="indefinite" values="0;0;11;11" keyTimes="0;{k1:.4f};{p2:.4f};1"/>'
                   f'<animate attributeName="opacity" dur="{D}" repeatCount="indefinite" values="0;0;0.9;0;0" '
                   f'keyTimes="0;{k1:.4f};{min(k1 + 0.001, p2 - 0.001):.4f};{p2:.4f};1"/></circle>')
    out.append("</g>")

    # body: (width, length) from thick/short to thin/long gives the taper
    layers = [(12.5, 30), (11, 62), (9.5, 95), (8, 126), (6.5, 152), (5, 174), (3.4, 192), (2, 204)]

    def segment(stroke: str, width_: float, length: float, extra: str = "", dash: str | None = None) -> str:
        dash = dash or f"{f(length)} {f(total_len + 400)}"
        return (f'<use xlink:href="#route" href="#route" stroke="{stroke}" stroke-width="{width_}" '
                f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{dash}" '
                f'stroke-dashoffset="{f(length)}" {extra}>'
                f'<animate attributeName="stroke-dashoffset" dur="{D}" repeatCount="indefinite" '
                f'values="{f(length)};{f(length - total_len)};{f(length - total_len)}" keyTimes="0;{mf:.4f};1"/></use>')

    out.append('<g filter="url(#shadow)">')
    for w_, L in layers:
        out.append(segment(pal["outline"], w_ + 2.6, L))
    for w_, L in layers:
        out.append(segment(pal["body"], w_, L))
    # banded scales: short dashes across the back, only along the body length
    band_len = 180
    bands = " ".join(["3.2 4.3"] * int(band_len / 7.5)) + f" 0 {f(total_len + 400)}"
    out.append(segment(pal["bands"], 7, band_len, 'opacity="0.55"', dash=bands))
    out.append(segment(pal["stripe"], 1.6, 150, 'opacity="0.55"'))
    out.append("</g>")

    # head
    out.append(
        f'<g opacity="0"><animate attributeName="opacity" dur="{D}" repeatCount="indefinite" '
        f'values="1;1;0;0" keyTimes="0;{mf:.4f};{min(mf + 0.001, 0.999):.4f};1"/>'
        f'<g><animateMotion dur="{D}" repeatCount="indefinite" rotate="auto" calcMode="linear" '
        f'keyPoints="0;1;1" keyTimes="0;{mf:.4f};1"><mpath xlink:href="#route" href="#route"/></animateMotion>'
        f'<g transform="translate(9.5 0)"><path d="M0 0H7.5L10.5-2.6M7.5 0L10.5 2.6" stroke="#ff4d6d" stroke-width="1.3" '
        f'fill="none" stroke-linecap="round"><animateTransform attributeName="transform" type="scale" '
        f'values="0.01 1;1 1;1 1;0.01 1;0.01 1" keyTimes="0;0.12;0.22;0.34;1" dur="1.7s" repeatCount="indefinite"/></path></g>'
        f'<path d="M-6 -6.6 C2 -8.4 9 -5.2 11 0 C9 5.2 2 8.4 -6 6.6 Z" fill="{pal["body"]}" stroke="{pal["outline"]}" stroke-width="1.3"/>'
        f'<path d="M-3 -2.6 C2 -3.6 6 -2 8 0 C6 2 2 3.6 -3 2.6 Z" fill="{pal["bands"]}" opacity="0.45"/>'
        f'<circle cx="4.2" cy="-4.1" r="1.9" fill="#0b0f14"/><circle cx="4.2" cy="4.1" r="1.9" fill="#0b0f14"/>'
        f'<circle cx="4.8" cy="-4.6" r="0.65" fill="#fff"/><circle cx="4.8" cy="3.6" r="0.65" fill="#fff"/>'
        f'<circle cx="9.3" cy="-1.3" r="0.45" fill="#0b0f14"/><circle cx="9.3" cy="1.3" r="0.45" fill="#0b0f14"/>'
        f'</g></g>')

    # caption
    out.append(f'<text x="{PAD_X}" y="{height - 11}" font-family="Consolas, \'Fira Code\', monospace" font-size="11" '
               f'fill="{pal["label"]}">$ snake --hunt {USER}/contributions  ·  {total} contributions this year  ·  '
               f'{len(active)} active days</text>')
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    cells, total = fetch_calendar()
    if not cells:
        raise SystemExit("could not read the contribution calendar")
    t = theme.current()
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets/snake-dark.svg").write_text(render(cells, total, t, True), encoding="utf-8")
    (ROOT / "assets/snake-light.svg").write_text(render(cells, total, t, False), encoding="utf-8")


if __name__ == "__main__":
    main()
