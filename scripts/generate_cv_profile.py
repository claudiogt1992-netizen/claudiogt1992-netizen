import os
import json
import html
import math
import urllib.request
from datetime import datetime, timedelta


USERNAME = os.getenv("GITHUB_USERNAME", "claudiogt1992-netizen")
TOKEN = os.getenv("GITHUB_TOKEN", "")


def esc(value):
    return html.escape(str(value), quote=True)


def github_get(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "cabo-verde-dev-pulse-clean-pro",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_repos(username):
    repos = []
    page = 1

    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}&type=owner&sort=updated"
        data = github_get(url)

        if not data:
            break

        repos.extend(data)

        if len(data) < 100:
            break

        page += 1

    return repos


def star_points(cx, cy, outer_r, inner_r):
    pts = []
    angle = -math.pi / 2
    for i in range(10):
        r = outer_r if i % 2 == 0 else inner_r
        x = cx + math.cos(angle) * r
        y = cy + math.sin(angle) * r
        pts.append(f"{x:.2f},{y:.2f}")
        angle += math.pi / 5
    return " ".join(pts)


def star_ring(cx, cy, ring_r, outer_r, inner_r, pulse=True):
    stars = []

    for i in range(10):
        angle = math.radians(-90 + i * 36)
        sx = cx + math.cos(angle) * ring_r
        sy = cy + math.sin(angle) * ring_r
        pts = star_points(sx, sy, outer_r, inner_r)

        if pulse:
            dur = 2.2 + (i % 4) * 0.25
            begin = -(i * 0.15)
            stars.append(f"""
            <polygon points="{pts}" fill="#F7D116" opacity="0.88">
              <animate attributeName="opacity" values="0.45;1;0.45" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
              <animateTransform attributeName="transform" type="scale" values="0.96;1.08;0.96" dur="{dur}s" begin="{begin}s" repeatCount="indefinite" additive="sum"/>
            </polygon>
            """)
        else:
            stars.append(f'<polygon points="{pts}" fill="#F7D116" opacity="0.95"/>')

    return "\n".join(stars)


def tech_chip(x, y, label, color, delay):
    return f"""
    <g transform="translate({x} {y})">
      <animateTransform attributeName="transform" type="translate"
        values="{x} {y};{x} {y-2};{x} {y}"
        dur="3.2s" begin="-{delay}s" repeatCount="indefinite"/>

      <rect width="120" height="38" rx="19" fill="#09192E" fill-opacity="0.92" stroke="{color}" stroke-opacity="0.28"/>
      <circle cx="19" cy="19" r="5.5" fill="{color}">
        <animate attributeName="opacity" values="0.45;1;0.45" dur="2.5s" begin="-{delay}s" repeatCount="indefinite"/>
      </circle>
      <text x="33" y="24" fill="#F2F7FF" font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="600">{esc(label)}</text>
    </g>
    """


def stat_card(x, y, width, height, number, label, accent, delay):
    return f"""
    <g transform="translate({x} {y})">
      <rect width="{width}" height="{height}" rx="22" fill="#08172B" fill-opacity="0.84" stroke="{accent}" stroke-opacity="0.32"/>
      <rect width="{width}" height="{height}" rx="22" fill="none" stroke="{accent}">
        <animate attributeName="stroke-opacity" values="0.22;0.62;0.22" dur="3.2s" begin="-{delay}s" repeatCount="indefinite"/>
      </rect>

      <rect x="-42" y="0" width="34" height="{height}" rx="17" fill="#FFFFFF" opacity="0">
        <animateTransform attributeName="transform" type="translate" values="0 0;{width+90} 0" dur="5.2s" begin="-{delay}s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0;0.13;0" dur="5.2s" begin="-{delay}s" repeatCount="indefinite"/>
      </rect>

      <text x="{width/2}" y="42" text-anchor="middle" fill="#FFFFFF" font-family="Segoe UI, Arial, sans-serif" font-size="28" font-weight="800">{number}</text>
      <text x="{width/2}" y="68" text-anchor="middle" fill="#BEDBFF" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="600">{esc(label)}</text>
    </g>
    """


def main():
    user = github_get(f"https://api.github.com/users/{USERNAME}")
    repos = fetch_repos(USERNAME)

    public_repos = int(user.get("public_repos", 0))
    followers = int(user.get("followers", 0))
    following = int(user.get("following", 0))
    total_stars = sum(int(repo.get("stargazers_count", 0)) for repo in repos)
    total_forks = sum(int(repo.get("forks_count", 0)) for repo in repos)

    updated = (datetime.utcnow() - timedelta(hours=1)).strftime("%d/%m/%Y %H:%M")

    technologies = [
        ("Java", "#00BFFF"),
        ("Spring", "#6DB33F"),
        ("React", "#19D8FF"),
        ("Angular", "#FF3B5C"),
        ("JavaScript", "#F7D116"),
        ("TypeScript", "#2F86FF"),
        ("Python", "#FFD43B"),
    ]

    tech_svg = "\n".join(
        tech_chip(150 + i * 138, 248, name, color, i * 0.22)
        for i, (name, color) in enumerate(technologies)
    )

    cards_svg = "\n".join([
        stat_card(70, 328, 190, 88, public_repos, "Repositórios", "#00AEEF", 0.1),
        stat_card(284, 328, 190, 88, followers, "Seguidores", "#2FB6FF", 0.5),
        stat_card(498, 328, 190, 88, total_stars, "Estrelas", "#F7D116", 0.9),
        stat_card(712, 328, 190, 88, total_forks, "Forks", "#8B5CF6", 1.3),
        stat_card(926, 328, 190, 88, following, "Seguindo", "#C084FC", 1.7),
    ])

    logo_ring = star_ring(68, 68, 40, 5.8, 2.5, True)
    flag_ring = star_ring(58, 40, 19, 3.2, 1.35, True)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="430" viewBox="0 0 1200 430" role="img" aria-label="Cabo Verde Dev Pulse">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#030A14"/>
      <stop offset="45%" stop-color="#061A35"/>
      <stop offset="100%" stop-color="#030711"/>
    </linearGradient>

    <linearGradient id="cyanLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00BFFF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#00BFFF" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#00BFFF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="ocean" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00AEEF" stop-opacity="0.17"/>
      <stop offset="100%" stop-color="#003893" stop-opacity="0.06"/>
    </linearGradient>

    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00BFFF" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#00BFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softGlow">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="shadow">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity="0.30"/>
    </filter>
  </defs>

  <rect width="1200" height="430" rx="28" fill="url(#bg)"/>

  <!-- ambient glow -->
  <circle cx="150" cy="90" r="95" fill="url(#glow)">
    <animate attributeName="r" values="88;104;88" dur="7s" repeatCount="indefinite"/>
  </circle>

  <circle cx="1030" cy="80" r="80" fill="url(#glow)" opacity="0.75">
    <animate attributeName="r" values="72;88;72" dur="6.2s" repeatCount="indefinite"/>
  </circle>

  <!-- subtle particles -->
  <g fill="#35C8FF" opacity="0.65">
    <circle cx="228" cy="44" r="2.5">
      <animate attributeName="opacity" values="0.25;1;0.25" dur="2.7s" repeatCount="indefinite"/>
    </circle>
    <circle cx="948" cy="32" r="2.5">
      <animate attributeName="opacity" values="1;0.25;1" dur="2.9s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1086" cy="150" r="2.5">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="3.1s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- top left logo -->
  <g transform="translate(42 30)" filter="url(#softGlow)">
    <circle cx="68" cy="68" r="54" fill="#003893" stroke="#2B6CF0" stroke-width="2.5"/>
    <rect x="23" y="59" width="90" height="8" rx="4" fill="#FFFFFF"/>
    <rect x="23" y="68" width="90" height="8" rx="4" fill="#CF2027"/>
    <rect x="23" y="77" width="90" height="8" rx="4" fill="#FFFFFF"/>
    {logo_ring}
  </g>

  <!-- header text -->
  <text x="160" y="82" fill="#FFFFFF" font-family="Segoe UI, Arial, sans-serif" font-size="34" font-weight="800">Cabo Verde Dev Pulse</text>
  <text x="160" y="114" fill="#D7E9FF" font-family="Segoe UI, Arial, sans-serif" font-size="16" font-weight="600">{esc(USERNAME)} • Cabo Verde • Systems Engineering &amp; Computer Science Student</text>
  <text x="160" y="137" fill="#7DC3FF" font-family="Segoe UI, Arial, sans-serif" font-size="13">Atualizado: {esc(updated)}</text>

  <!-- header divider -->
  <line x1="46" y1="160" x2="1148" y2="160" stroke="url(#cyanLine)" stroke-width="2"/>

  <!-- top right animated flag -->
  <g transform="translate(1010 36)" filter="url(#shadow)">
    <rect x="0" y="0" width="142" height="90" rx="20" fill="#09182E" fill-opacity="0.78" stroke="#1E4C7D" stroke-opacity="0.45"/>

    <g transform="translate(18 14)">
      <animateTransform attributeName="transform" type="translate"
        values="18 14;18 9;18 14"
        dur="3.8s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" additive="sum" type="rotate"
        values="-4 54 30;4 54 30;-4 54 30"
        dur="3.8s" repeatCount="indefinite"/>

      <path fill="#003893">
        <animate attributeName="d" dur="3.8s" repeatCount="indefinite"
          values="
          M0 8 C24 0, 52 14, 106 8 L106 58 C52 66, 24 52, 0 58 Z;
          M0 8 C24 4, 52 12, 106 8 L106 58 C52 62, 24 54, 0 58 Z;
          M0 8 C24 0, 52 14, 106 8 L106 58 C52 66, 24 52, 0 58 Z"/>
      </path>

      <path fill="#FFFFFF">
        <animate attributeName="d" dur="3.8s" repeatCount="indefinite"
          values="
          M0 27 C24 24, 52 31, 106 27 L106 33 C52 36, 24 29, 0 33 Z;
          M0 27 C24 25, 52 30, 106 27 L106 33 C52 35, 24 30, 0 33 Z;
          M0 27 C24 24, 52 31, 106 27 L106 33 C52 36, 24 29, 0 33 Z"/>
      </path>

      <path fill="#CF2027">
        <animate attributeName="d" dur="3.8s" repeatCount="indefinite"
          values="
          M0 33 C24 30, 52 37, 106 33 L106 42 C52 45, 24 38, 0 42 Z;
          M0 33 C24 31, 52 36, 106 33 L106 42 C52 44, 24 39, 0 42 Z;
          M0 33 C24 30, 52 37, 106 33 L106 42 C52 45, 24 38, 0 42 Z"/>
      </path>

      <path fill="#FFFFFF">
        <animate attributeName="d" dur="3.8s" repeatCount="indefinite"
          values="
          M0 42 C24 39, 52 46, 106 42 L106 48 C52 51, 24 44, 0 48 Z;
          M0 42 C24 40, 52 45, 106 42 L106 48 C52 50, 24 45, 0 48 Z;
          M0 42 C24 39, 52 46, 106 42 L106 48 C52 51, 24 44, 0 48 Z"/>
      </path>

      {flag_ring}
    </g>
  </g>

  <!-- main title -->
  <text x="600" y="220" text-anchor="middle" fill="#FFFFFF" font-family="Segoe UI, Arial, sans-serif" font-size="44" font-weight="800">
    <tspan>Full Stack </tspan><tspan fill="#12CBFF">Java</tspan><tspan> Developer in Progress</tspan>
  </text>

  <!-- subtitle moved away from icons -->
  <text x="600" y="250" text-anchor="middle" fill="#AFCFFF" font-family="Segoe UI, Arial, sans-serif" font-size="19" font-weight="500">
    Systems Engineering &amp; Computer Science Student
  </text>

  <!-- tech row -->
  {tech_svg}

  <!-- stat cards -->
  {cards_svg}

  <!-- ocean motion -->
  <path d="M0 345 C150 326, 300 362, 450 345 C600 328, 750 362, 900 345 C1030 330, 1115 350, 1200 340 L1200 430 L0 430 Z" fill="url(#ocean)">
    <animateTransform attributeName="transform" type="translate" values="-14 0;14 0;-14 0" dur="8s" repeatCount="indefinite"/>
  </path>

  <!-- footer -->
  <text x="600" y="396" text-anchor="middle" fill="#C0DDFF" font-family="Segoe UI, Arial, sans-serif" font-size="15" font-weight="500">
    10 ilhas • 1 visão • tecnologia com identidade
  </text>
</svg>
"""

    os.makedirs("assets", exist_ok=True)

    with open("assets/cabo-verde-dev-pulse.svg", "w", encoding="utf-8") as f:
        f.write(svg)

    print("Cabo Verde Dev Pulse SVG generated successfully.")


if __name__ == "__main__":
    main()
