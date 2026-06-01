import json
import os
import urllib.request
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo

USERNAME = os.getenv("GITHUB_USERNAME", "claudiogt1992-netizen")
TOKEN = os.getenv("GITHUB_TOKEN", "")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "cabo-verde-dev-pulse",
}

if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def github_get(url):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def safe_text(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    user = github_get(f"https://api.github.com/users/{USERNAME}")
    repos = github_get(
        f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated&type=owner"
    )

    public_repos = user.get("public_repos", 0)
    followers = user.get("followers", 0)
    following = user.get("following", 0)

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
    total_forks = sum(repo.get("forks_count", 0) for repo in repos)

    languages = Counter(
        repo.get("language") for repo in repos if repo.get("language")
    )

    top_languages = " • ".join([lang for lang, _ in languages.most_common(5)])
    if not top_languages:
        top_languages = "Java • Spring Boot • React • Angular"

    updated_at = datetime.now(ZoneInfo("Atlantic/Cape_Verde")).strftime(
        "%d/%m/%Y às %H:%M"
    )

    svg = f"""<svg width="1000" height="360" viewBox="0 0 1000 360" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{
      font: 700 34px 'Segoe UI', Ubuntu, sans-serif;
      fill: #ffffff;
    }}

    .subtitle {{
      font: 500 18px 'Segoe UI', Ubuntu, sans-serif;
      fill: #dbeafe;
    }}

    .small {{
      font: 500 14px 'Segoe UI', Ubuntu, sans-serif;
      fill: #cbd5e1;
    }}

    .number {{
      font: 800 28px 'Segoe UI', Ubuntu, sans-serif;
      fill: #ffffff;
    }}

    .label {{
      font: 600 13px 'Segoe UI', Ubuntu, sans-serif;
      fill: #93c5fd;
      letter-spacing: .4px;
    }}

    .card {{
      fill: rgba(15, 23, 42, 0.72);
      stroke: rgba(255,255,255,0.14);
      stroke-width: 1;
    }}

    .wave1 {{
      animation: waveMove 7s ease-in-out infinite alternate;
    }}

    .wave2 {{
      animation: waveMove 9s ease-in-out infinite alternate-reverse;
    }}

    .pulse {{
      animation: pulse 2.2s ease-in-out infinite;
      transform-origin: center;
    }}

    .float {{
      animation: float 4s ease-in-out infinite;
    }}

    @keyframes waveMove {{
      from {{ transform: translateX(-20px); }}
      to {{ transform: translateX(22px); }}
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: .55; r: 5; }}
      50% {{ opacity: 1; r: 8; }}
    }}

    @keyframes float {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(-8px); }}
    }}
  </style>

  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1000" y2="360">
      <stop offset="0%" stop-color="#001b44"/>
      <stop offset="45%" stop-color="#002756"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>

    <linearGradient id="ocean" x1="0" y1="210" x2="1000" y2="360">
      <stop offset="0%" stop-color="#003893" stop-opacity=".55"/>
      <stop offset="100%" stop-color="#00aeef" stop-opacity=".18"/>
    </linearGradient>

    <filter id="glow">
      <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="1000" height="360" rx="28" fill="url(#bg)"/>

  <circle cx="110" cy="86" r="34" fill="#ffffff" opacity=".08"/>
  <circle cx="110" cy="86" r="22" fill="#003893"/>
  <circle cx="110" cy="86" r="7" fill="#F7D116"/>
  <circle cx="88" cy="69" r="4" fill="#F7D116"/>
  <circle cx="132" cy="69" r="4" fill="#F7D116"/>
  <circle cx="88" cy="103" r="4" fill="#F7D116"/>
  <circle cx="132" cy="103" r="4" fill="#F7D116"/>
  <circle cx="110" cy="58" r="4" fill="#F7D116"/>
  <circle cx="110" cy="114" r="4" fill="#F7D116"/>

  <rect x="176" y="76" width="184" height="8" rx="4" fill="#ffffff"/>
  <rect x="176" y="90" width="184" height="8" rx="4" fill="#CF2027"/>
  <rect x="176" y="104" width="184" height="8" rx="4" fill="#ffffff"/>

  <text x="54" y="166" class="title">🇨🇻 Cabo Verde Dev Pulse</text>
  <text x="54" y="202" class="subtitle">Morabeza • Código • Segurança • Java Full Stack</text>
  <text x="54" y="232" class="small">Praia, Santiago, Cabo Verde · Atualizado em {safe_text(updated_at)}</text>

  <g class="float">
    <rect x="680" y="42" width="260" height="132" rx="20" class="card"/>
    <text x="708" y="82" class="label">STACK EM EVOLUÇÃO</text>
    <text x="708" y="118" class="subtitle">{safe_text(top_languages)}</text>
    <text x="708" y="150" class="small">Construindo soluções modernas, seguras e escaláveis.</text>
  </g>

  <rect x="54" y="258" width="148" height="72" rx="18" class="card"/>
  <text x="78" y="287" class="number">{public_repos}</text>
  <text x="78" y="313" class="label">REPOSITÓRIOS</text>

  <rect x="222" y="258" width="148" height="72" rx="18" class="card"/>
  <text x="246" y="287" class="number">{followers}</text>
  <text x="246" y="313" class="label">SEGUIDORES</text>

  <rect x="390" y="258" width="148" height="72" rx="18" class="card"/>
  <text x="414" y="287" class="number">{total_stars}</text>
  <text x="414" y="313" class="label">ESTRELAS</text>

  <rect x="558" y="258" width="148" height="72" rx="18" class="card"/>
  <text x="582" y="287" class="number">{total_forks}</text>
  <text x="582" y="313" class="label">FORKS</text>

  <rect x="726" y="258" width="214" height="72" rx="18" class="card"/>
  <text x="750" y="287" class="number">{following}</text>
  <text x="750" y="313" class="label">SEGUINDO</text>

  <path class="wave1" d="M0 250 C130 214, 260 286, 390 250 C520 214, 650 286, 780 250 C890 220, 960 236, 1000 248 L1000 360 L0 360 Z" fill="url(#ocean)"/>
  <path class="wave2" d="M0 286 C145 250, 280 318, 420 284 C560 250, 690 318, 835 282 C925 260, 970 270, 1000 284 L1000 360 L0 360 Z" fill="#00AEEF" opacity=".15"/>

  <g filter="url(#glow)">
    <circle class="pulse" cx="808" cy="224" r="5" fill="#F7D116"/>
    <circle class="pulse" cx="832" cy="212" r="5" fill="#ffffff"/>
    <circle class="pulse" cx="858" cy="232" r="5" fill="#F7D116"/>
    <circle class="pulse" cx="884" cy="218" r="5" fill="#ffffff"/>
    <circle class="pulse" cx="906" cy="244" r="5" fill="#F7D116"/>
    <circle class="pulse" cx="785" cy="248" r="5" fill="#ffffff"/>
    <circle class="pulse" cx="846" cy="258" r="5" fill="#F7D116"/>
    <circle class="pulse" cx="876" cy="272" r="5" fill="#ffffff"/>
    <circle class="pulse" cx="920" cy="280" r="5" fill="#F7D116"/>
    <circle class="pulse" cx="806" cy="286" r="5" fill="#ffffff"/>
  </g>

  <path d="M740 205 C800 176, 890 174, 952 202" stroke="#ffffff" stroke-opacity=".22" stroke-width="2" stroke-dasharray="8 10"/>
  <text x="760" y="196" class="small">10 ilhas • 1 visão • tecnologia com identidade</text>
</svg>
"""

    os.makedirs("assets", exist_ok=True)

    with open("assets/cabo-verde-dev-pulse.svg", "w", encoding="utf-8") as file:
        file.write(svg)


if __name__ == "__main__":
    main()
