#!/usr/bin/env python3
"""Generate brand-aligned pinned repo SVG cards for MGM Laboratory.

Reads repo metadata from the GitHub API and writes one SVG per featured
repo into profile/pins/. Cards follow the MGM Laboratory design system:
white surface, hairline border, calm typography, with a Bauhaus geometric
mark in the assigned brand color as a signature.

Run locally: GITHUB_TOKEN=ghp_xxx python profile/scripts/generate-pins.py
Run in CI:   handled by .github/workflows/update-pins.yml
"""

from __future__ import annotations

import json
import os
import textwrap
from pathlib import Path
from urllib.request import Request, urlopen

ORG = "MGM-Laboratory"
OUT_DIR = Path(__file__).resolve().parent.parent / "pins"

# Featured repos, each assigned a brand color + Bauhaus signature shape.
# Colors match the original github-readme-stats icon_color values.
REPOS = [
    {"name": "mgm-atlas-frontend",         "color": "#3A6DC5", "shape": "circle"},
    {"name": "mgm-asset-library-frontend", "color": "#F7BF33", "shape": "plus"},
    {"name": "mgm-domain-frontend",        "color": "#F94141", "shape": "triangle"},
    {"name": "mgm-keycloak-theme",         "color": "#0F8657", "shape": "halfdisc"},
]

# GitHub Linguist colors for the language dot
LANG = {
    "TypeScript": "#3178C6", "JavaScript": "#F1E05A", "Python": "#3572A5",
    "Go": "#00ADD8", "Rust": "#DEA584", "Java": "#B07219", "Kotlin": "#A97BFF",
    "Swift": "#F05138", "Dart": "#00B4AB", "C#": "#178600", "C++": "#F34B7D",
    "Vue": "#41B883", "Svelte": "#FF3E00", "HTML": "#E34C26", "CSS": "#563D7C",
    "SCSS": "#C6538C", "Shell": "#89E051", "FreeMarker": "#0050B2",
    "PHP": "#4F5D95", "Ruby": "#701516", "Lua": "#000080",
    "Dockerfile": "#384D54", "Jupyter Notebook": "#DA5B0B",
}


def gh(url: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "mgm-pinned-generator",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=20) as r:
        return json.loads(r.read())


def fmt_count(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M".replace(".0M", "M")
    if n >= 1000:
        return f"{n / 1000:.1f}k".replace(".0k", "k")
    return str(n)


def xml_escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def wrap_desc(desc: str, width: int = 52, max_lines: int = 2) -> list[str]:
    if not desc:
        return ["—", ""]
    lines = textwrap.wrap(desc, width=width, break_long_words=False)
    if len(lines) > max_lines:
        kept = lines[:max_lines]
        last = kept[-1]
        if len(last) + 1 > width:
            last = last[: width - 1]
        kept[-1] = last.rstrip(" ,.;:") + "…"
        lines = kept
    while len(lines) < max_lines:
        lines.append("")
    return lines


def bauhaus_mark(shape: str, color: str) -> str:
    """22×22 geometric signature in the assigned brand color."""
    if shape == "circle":
        return f'<circle cx="11" cy="11" r="10" fill="{color}"/>'
    if shape == "plus":
        return (f'<rect x="9" y="1" width="4" height="20" fill="{color}"/>'
                f'<rect x="1" y="9" width="20" height="4" fill="{color}"/>')
    if shape == "triangle":
        return f'<path d="M11 1 L21 19 L1 19 Z" fill="{color}"/>'
    if shape == "halfdisc":
        return f'<path d="M1 11 A10 10 0 0 1 21 11 Z" fill="{color}"/>'
    return f'<circle cx="11" cy="11" r="10" fill="{color}"/>'


def render(repo: dict, color: str, shape: str) -> str:
    name = repo["name"]
    desc = repo.get("description") or ""
    lang = repo.get("language") or ""
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)

    d1, d2 = wrap_desc(desc, width=52, max_lines=2)
    lang_color = LANG.get(lang, "#9AA1AD")
    sig = bauhaus_mark(shape, color)
    aria = f"{ORG}/{name} — {desc}" if desc else f"{ORG}/{name}"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="420" height="140" viewBox="0 0 420 140" role="img" aria-label="{xml_escape(aria)}">
  <title>{xml_escape(name)}</title>
  <style>
    .t  {{ font-family: "Geist", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }}
    .og {{ font-size: 14px; font-weight: 400; fill: #6B7280; letter-spacing: -0.005em; }}
    .nm {{ font-size: 16px; font-weight: 600; fill: #0E1116; letter-spacing: -0.01em; }}
    .ds {{ font-size: 13px; font-weight: 400; fill: #3B4150; }}
    .mt {{ font-size: 12px; font-weight: 500; fill: #3B4150; letter-spacing: 0.005em; }}
  </style>

  <!-- Card surface -->
  <rect x="0.5" y="0.5" width="419" height="139" rx="12" ry="12" fill="#FFFFFF" stroke="#ECECEA"/>

  <!-- Lucide book-marked icon -->
  <g transform="translate(22, 22)" fill="none" stroke="#6B7280" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M4 1.5 h10 a1.5 1.5 0 0 1 1.5 1.5 v13.5 a1.5 1.5 0 0 1 -1.5 1.5 H4 a1 1 0 0 1 -1 -1 v-14.5 a1 1 0 0 1 1 -1 z"/>
    <path d="M3 13.5 h12"/>
  </g>

  <!-- Title -->
  <text x="46" y="36" class="t">
    <tspan class="og">{xml_escape(ORG)} / </tspan><tspan class="nm">{xml_escape(name)}</tspan>
  </text>

  <!-- Bauhaus signature -->
  <g transform="translate(376, 22)">
    {sig}
  </g>

  <!-- Description (always two lines for vertical rhythm) -->
  <text x="22" y="68" class="t ds">{xml_escape(d1)}</text>
  <text x="22" y="87" class="t ds">{xml_escape(d2)}</text>

  <!-- Meta row -->
  <g transform="translate(22, 112)">
    <!-- Language -->
    <circle cx="6" cy="6" r="5" fill="{lang_color}"/>
    <text x="18" y="10" class="t mt">{xml_escape(lang) if lang else "—"}</text>

    <!-- Star -->
    <g transform="translate(132, 0)">
      <path d="M6 1 L7.4 4 L10.7 4.4 L8.2 6.6 L9 9.8 L6 8.1 L3 9.8 L3.8 6.6 L1.3 4.4 L4.6 4 Z"
            fill="none" stroke="#6B7280" stroke-width="1.3" stroke-linejoin="round" stroke-linecap="round"/>
      <text x="18" y="10" class="t mt">{fmt_count(stars)}</text>
    </g>

    <!-- Fork (git-fork) -->
    <g transform="translate(198, 0)">
      <circle cx="3" cy="3" r="1.6" fill="none" stroke="#6B7280" stroke-width="1.3"/>
      <circle cx="11" cy="3" r="1.6" fill="none" stroke="#6B7280" stroke-width="1.3"/>
      <circle cx="7" cy="11" r="1.6" fill="none" stroke="#6B7280" stroke-width="1.3"/>
      <path d="M3 4.6 V6.5 a2 2 0 0 0 2 2 h4 a2 2 0 0 0 2 -2 V4.6 M7 8.5 v0.9"
            fill="none" stroke="#6B7280" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="18" y="10" class="t mt">{fmt_count(forks)}</text>
    </g>
  </g>
</svg>
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for entry in REPOS:
        try:
            data = gh(f"https://api.github.com/repos/{ORG}/{entry['name']}")
        except Exception as exc:
            print(f"✗ {entry['name']}: {exc}")
            continue
        svg = render(data, entry["color"], entry["shape"])
        (OUT_DIR / f"{entry['name']}.svg").write_text(svg, encoding="utf-8")
        print(f"✓ {entry['name']}")


if __name__ == "__main__":
    main()
