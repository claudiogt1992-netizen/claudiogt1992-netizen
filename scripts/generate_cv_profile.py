import os
import json
import html
import urllib.request
from collections import Counter
from datetime import datetime, timedelta

USERNAME = os.getenv("GITHUB_USERNAME", "claudiogt1992-netizen")
TOKEN = os.getenv("GITHUB_TOKEN", "")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "cabo-verde-dev-pulse"
}

if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def github_get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def esc(value):
    return html.escape(str(value))


def main():
    user = github_get(f"https://api.github.com/users/{USERNAME}")
    repos = github_get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner&sort=updated")

    public_repos = user.get("public_repos", 0)
    followers = user.get("followers", 0)
    following = user.get("following", 0)

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
    total_forks = sum(repo.get("forks_count", 0) for repo in repos)

    lang_counter = Counter(repo.get("language") for repo in repos if repo.get("language"))
    top_languages = " • ".join(lang for lang, _ in lang_counter.most_common(5))
    if not top_languages:
        top_languages = "Java • Spring Boot • React • Angular • Python"

    updated = (datetime.utcnow() - timedelta(hours=1)).strftime("%d/%m/%Y %H:%M")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="320" viewBox="0 0 1000 320">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#001b44"/>
      <stop offset="50%" stop-color="#002756"/>
      <stop offset="100%" stop-color="#030712"/>
    </linearGradient>

    <linearGradient id="wave1" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00AEEF" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#003893" stop-opacity="0.15"/>
    </linearGradient>

    <linearGradient id="wave2" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F7D116" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.08"/>
    </linearGradient>
  </defs>

  <rect width="1000" height="320" rx="24" fill="url(#bg)"/>

  <text x="50" y="55" fill="#FFFFFF" font-size="30" font-family="Segoe UI, Arial, sans-serif" font-weight="700">
    Cabo Verde Dev Pulse
  </text>

  <text x="50" y="85" fill="#B9D9FF" font-size="16" font-family="Segoe UI, Arial, sans-serif">
    Morabeza • Código • Segurança • Java Full Stack
  </text>

  <text x="50" y="110" fill="#DCEBFF" font-size="13" font-family="Segoe UI, Arial, sans-serif">
    Perfil: {esc(USERNAME)}  •  Praia, Santiago, Cabo Verde  •  Atualizado: {esc(updated)}
  </text>

  <g>
    <circle cx="88" cy="145" r="4" fill="#F7D116"/>
    <circle cx="110" cy="132" r="4" fill="#FFFFFF"/>
    <circle cx="134" cy="150" r="4" fill="#F7D116"/>
    <circle cx="158" cy="136" r="4" fill="#FFFFFF"/>
    <circle cx="182" cy="161" r="4" fill="#F7D116"/>
    <circle cx="70" cy="170" r="4" fill="#FFFFFF"/>
    <circle cx="128" cy="176" r="4" fill="#F7D116"/>
    <circle cx="160" cy="186" r="4" fill="#FFFFFF"/>
    <circle cx="196" cy="196" r="4" fill="#F7D116"/>
    <circle cx="92" cy="198" r="4" fill="#FFFFFF"/>
  </g>

  <rect x="620" y="35" width="330" height="88" rx="16" fill="#0B1220" fill-opacity="0.82" stroke="#1E3A5F"/>
  <text x="640" y="62" fill="#7CC7FF" font-size="13" font-family="Segoe UI, Arial, sans-serif" font-weight="700">
    STACK EM EVOLUÇÃO
  </text>
  <text x="640" y="88" fill="#FFFFFF" font-size="16" font-family="Segoe UI, Arial, sans-serif">
    {esc(top_languages)}
  </text>
  <text x="640" y="110" fill="#C9E3FF" font-size="12" font-family="Segoe UI, Arial, sans-serif">
    Construindo soluções modernas, seguras e escaláveis.
  </text>

  <rect x="50" y="225" width="160" height="62" rx="14" fill="#0B1220" fill-opacity="0.84" stroke="#1E3A5F"/>
  <text x="70" y="252" fill="#FFFFFF" font-size="26" font-family="Segoe UI, Arial, sans-serif" font-weight="700">{public_repos}</text>
  <text x="70" y="273" fill="#7CC7FF" font-size="12" font-family="Segoe UI, Arial, sans-serif" font-weight="700">REPOSITÓRIOS</text>

  <rect x="225" y="225" width="160" height="62" rx="14" fill="#0B1220" fill-opacity="0.84" stroke="#1E3A5F"/>
  <text x="245" y="252" fill="#FFFFFF" font-size="26" font-family="Segoe UI, Arial, sans-serif" font-weight="700">{followers}</text>
  <text x="245" y="273" fill="#7CC7FF" font-size="12" font-family="Segoe UI, Arial, sans-serif" font-weight="700">SEGUIDORES</text>

  <rect x="400" y="225" width="160" height="62" rx="14" fill="#0B1220" fill-opacity="0.84" stroke="#1E3A5F"/>
  <text x="420" y="252" fill="#FFFFFF" font-size="26" font-family="Segoe UI, Arial, sans-serif" font-weight="700">{total_stars}</text>
  <text x="420" y="273" fill="#7CC7FF" font-size="12" font-family="Segoe UI, Arial, sans-serif" font-weight="700">ESTRELAS</text>

  <rect x="575" y="225" width="160" height="62" rx="14" fill="#0B1220" fill-opacity="0.84" stroke="#1E3A5F"/>
  <text x="595" y="252" fill="#FFFFFF" font-size="26" font-family="Segoe UI, Arial, sans-serif" font-weight="700">{total_forks}</text>
  <text x="595" y="273" fill="#7CC7FF" font-size="12" font-family="Segoe UI, Arial, sans-serif" font-weight="700">FORKS</text>

  <rect x="750" y="225" width="200" height="62" rx="14" fill="#0B1220" fill-opacity="0.84" stroke="#1E3A5F"/>
  <text x="770" y="252" fill="#FFFFFF" font-size="26" font-family="Segoe UI, Arial, sans-serif" font-weight="700">{following}</text>
  <text x="770" y="273" fill="#7CC7FF" font-size="12" font-family="Segoe UI, Arial, sans-serif" font-weight="700">SEGUINDO</text>

  <g>
    <path d="M0 205 C120 185, 240 225, 360 205 C480 185, 600 225, 720 205 C820 190, 920 195, 1000 210 L1000 320 L0 320 Z"
          fill="url(#wave1)">
      <animateTransform attributeName="transform" attributeType="XML" type="translate"
                        values="-8 0;8 0;-8 0" dur="8s" repeatCount="indefinite"/>
    </path>

    <path d="M0 228 C130 208, 260 245, 390 226 C520 206, 650 245, 780 226 C880 212, 940 218, 1000 230 L1000 320 L0 320 Z"
          fill="url(#wave2)">
      <animateTransform attributeName="transform" attributeType="XML" type="translate"
                        values="10 0;-10 0;10 0" dur="10s" repeatCount="indefinite"/>
    </path>
  </g>
</svg>
"""

    os.makedirs("assets", exist_ok=True)
    with open("assets/cabo-verde-dev-pulse.svg", "w", encoding="utf-8") as f:
        f.write(svg)

    print("SVG generated successfully: assets/cabo-verde-dev-pulse.svg")


if __name__ == "__main__":
    main()
