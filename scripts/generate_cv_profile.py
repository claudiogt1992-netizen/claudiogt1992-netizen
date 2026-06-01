import os
import json
import html
import math
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


def star_points(cx, cy, outer_r, inner_r, points=5):
    coords = []
    angle = -math.pi / 2
    step = math.pi / points

    for i in range(points * 2):
        r = outer_r if i % 2 == 0 else inner_r
        x = cx + math.cos(angle) * r
        y = cy + math.sin(angle) * r
        coords.append(f"{x:.2f},{y:.2f}")
        angle += step

    return " ".join(coords)


def star_ring(cx, cy, ring_r, star_outer, star_inner, count=10, start_deg=-90, animated=True):
    items = []
    for i in range(count):
        angle = math.radians(start_deg + i * (360 / count))
        sx = cx + math.cos(angle) * ring_r
        sy = cy + math.sin(angle) * ring_r
        pts = star_points(sx, sy, star_outer, star_inner)

        if animated:
            dur = 2.0 + (i % 5) * 0.25
            begin = -(i * 0.18)
            items.append(
                f'''
                <polygon points="{pts}" fill="#F7D116" opacity="0.92">
                  <animate attributeName="opacity" values="0.55;1;0.55" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
                </polygon>
                '''
            )
        else:
            items.append(f'<polygon points="{pts}" fill="#F7D116" opacity="0.95"/>')

    return "\n".join(items)


def main():
    user = github_get(f"https://api.github.com/users/{USERNAME}")
    repos = github_get(
        f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner&sort=updated"
    )

    public_repos = user.get("public_repos", 0)
    followers = user.get("followers", 0)
    following = user.get("following", 0)

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
    total_forks = sum(repo.get("forks_count", 0) for repo in repos)

    languages = Counter(repo.get("language") for repo in repos if repo.get("language"))
    real_languages = " • ".join(lang for lang, _ in languages.most_common(4))

    if not real_languages:
        real_languages = "Python"

    main_stack = "Java • Spring Boot • React • Angular • Python"
    updated = (datetime.utcnow() - timedelta(hours=1)).strftime("%d/%m/%Y %H:%M")

    decorative_star_ring = star_ring(
        cx=130, cy=242, ring_r=48, star_outer=6.6, star_inner=2.8, count=10, animated=True
    )

    flag_star_ring = star_ring(
        cx=44, cy=36, ring_r=18, star_outer=2.6, star_inner=1.1, count=10, animated=False
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="380" viewBox="0 0 1000 380">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#001B44"/>
      <stop offset="48%" stop-color="#002756"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>

    <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F2038" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#0A1527" stop-opacity="0.82"/>
    </linearGradient>

    <linearGradient id="ocean1" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00AEEF" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#003893" stop-opacity="0.12"/>
    </linearGradient>

    <linearGradient id="ocean2" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F7D116" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.05"/>
    </linearGradient>

    <radialGradient id="softGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="#00AEEF" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#00AEEF" stop-opacity="0"/>
    </radialGradient>

    <filter id="glow">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="shadow">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.35"/>
    </filter>
  </defs>

  <rect width="1000" height="380" rx="28" fill="url(#bg)"/>

  <!-- brilhos suaves -->
  <circle cx="920" cy="70" r="54" fill="url(#softGlow)">
    <animate attributeName="r" values="46;60;46" dur="5s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.6;1;0.6" dur="5s" repeatCount="indefinite"/>
  </circle>

  <circle cx="150" cy="270" r="95" fill="url(#softGlow)" opacity="0.55">
    <animate attributeName="r" values="86;102;86" dur="6s" repeatCount="indefinite"/>
  </circle>

  <!-- emblema superior esquerdo -->
  <g filter="url(#glow)">
    <circle cx="78" cy="72" r="28" fill="#003893" opacity="0.95"/>
    {star_ring(78, 72, 18, 3.2, 1.4, 10, -90, True)}
  </g>

  <!-- faixas inspiradas na bandeira -->
  <rect x="122" y="47" width="150" height="7" rx="3" fill="#FFFFFF"/>
  <rect x="122" y="60" width="150" height="7" rx="3" fill="#CF2027"/>
  <rect x="122" y="73" width="150" height="7" rx="3" fill="#FFFFFF"/>

  <!-- título -->
  <text x="42" y="140" fill="#FFFFFF" font-size="34" font-family="Segoe UI, Arial, sans-serif" font-weight="800">
    Cabo Verde Dev Pulse
  </text>

  <text x="42" y="170" fill="#D5E9FF" font-size="17" font-family="Segoe UI, Arial, sans-serif" font-weight="600">
    Morabeza • Código • Segurança • Java Full Stack
  </text>

  <text x="42" y="200" fill="#E3F0FF" font-size="13" font-family="Segoe UI, Arial, sans-serif">
    Perfil: {esc(USERNAME)} • Praia, Santiago, Cabo Verde • Atualizado: {esc(updated)}
  </text>

  <!-- card stack -->
  <g filter="url(#shadow)">
    <rect x="590" y="42" width="235" height="138" rx="22" fill="url(#glass)" stroke="#2B4F7C"/>
    <text x="615" y="77" fill="#6FC2FF" font-size="13" font-family="Segoe UI, Arial, sans-serif" font-weight="700">
      STACK EM EVOLUÇÃO
    </text>

    <text x="615" y="112" fill="#FFFFFF" font-size="18" font-family="Segoe UI, Arial, sans-serif" font-weight="700">
      <tspan x="615" dy="0">Java • Spring Boot • React</tspan>
      <tspan x="615" dy="22">Angular • Python</tspan>
    </text>

    <text x="615" y="148" fill="#D2E8FF" font-size="12" font-family="Segoe UI, Arial, sans-serif">
      Linguagens no GitHub: {esc(real_languages)}
    </text>
    <text x="615" y="166" fill="#93C5FD" font-size="12" font-family="Segoe UI, Arial, sans-serif">
      Construindo soluções modernas e escaláveis.
    </text>
  </g>

  <!-- bandeira oficial sem mastro -->
  <g transform="translate(852 36)" filter="url(#shadow)">
    <rect x="-10" y="-8" width="120" height="96" rx="20" fill="#08131f" fill-opacity="0.28" stroke="#24466C"/>

    <g>
      <animateTransform attributeName="transform" type="translate" values="0 0;0 -1.5;0 0" dur="4.6s" repeatCount="indefinite"/>

      <!-- campo azul -->
      <path fill="#003893">
        <animate attributeName="d" dur="5s" repeatCount="indefinite"
          values="
            M6 14 C26 8, 48 20, 84 14 L84 66 C48 72, 26 60, 6 66 Z;
            M6 14 C26 11, 48 17, 84 14 L84 66 C48 69, 26 63, 6 66 Z;
            M6 14 C26 8, 48 20, 84 14 L84 66 C48 72, 26 60, 6 66 Z"/>
      </path>

      <!-- faixas -->
      <path fill="#FFFFFF">
        <animate attributeName="d" dur="5s" repeatCount="indefinite"
          values="
            M6 33 C26 30, 48 36, 84 33 L84 38 C48 41, 26 35, 6 38 Z;
            M6 33 C26 31, 48 35, 84 33 L84 38 C48 40, 26 36, 6 38 Z;
            M6 33 C26 30, 48 36, 84 33 L84 38 C48 41, 26 35, 6 38 Z"/>
      </path>

      <path fill="#CF2027">
        <animate attributeName="d" dur="5s" repeatCount="indefinite"
          values="
            M6 38 C26 35, 48 41, 84 38 L84 46 C48 49, 26 43, 6 46 Z;
            M6 38 C26 36, 48 40, 84 38 L84 46 C48 48, 26 44, 6 46 Z;
            M6 38 C26 35, 48 41, 84 38 L84 46 C48 49, 26 43, 6 46 Z"/>
      </path>

      <path fill="#FFFFFF">
        <animate attributeName="d" dur="5s" repeatCount="indefinite"
          values="
            M6 46 C26 43, 48 49, 84 46 L84 51 C48 54, 26 48, 6 51 Z;
            M6 46 C26 44, 48 48, 84 46 L84 51 C48 53, 26 49, 6 51 Z;
            M6 46 C26 43, 48 49, 84 46 L84 51 C48 54, 26 48, 6 51 Z"/>
      </path>

      <!-- 10 estrelas -->
      <g>
        {flag_star_ring}
      </g>
    </g>
  </g>

  <!-- anel decorativo com 10 estrelas -->
  <g filter="url(#glow)">
    <circle cx="130" cy="242" r="58" fill="none" stroke="#2A5F8F" stroke-opacity="0.35" stroke-width="1.5"/>
    {decorative_star_ring}
  </g>

  <text x="655" y="235" fill="#E4F2FF" font-size="12" font-family="Segoe UI, Arial, sans-serif">
    10 ilhas • 1 visão • tecnologia com identidade
  </text>

  <!-- cards -->
  <g filter="url(#shadow)">
    <rect x="42" y="300" width="165" height="56" rx="16" fill="url(#glass)" stroke="#2B4F7C"/>
    <text x="68" y="325" fill="#FFFFFF" font-size="24" font-family="Segoe UI, Arial, sans-serif" font-weight="800">{public_repos}</text>
    <text x="68" y="344" fill="#72C8FF" font-size="11" font-family="Segoe UI, Arial, sans-serif" font-weight="700">REPOSITÓRIOS</text>

    <rect x="224" y="300" width="165" height="56" rx="16" fill="url(#glass)" stroke="#2B4F7C"/>
    <text x="250" y="325" fill="#FFFFFF" font-size="24" font-family="Segoe UI, Arial, sans-serif" font-weight="800">{followers}</text>
    <text x="250" y="344" fill="#72C8FF" font-size="11" font-family="Segoe UI, Arial, sans-serif" font-weight="700">SEGUIDORES</text>

    <rect x="406" y="300" width="165" height="56" rx="16" fill="url(#glass)" stroke="#2B4F7C"/>
    <text x="432" y="325" fill="#FFFFFF" font-size="24" font-family="Segoe UI, Arial, sans-serif" font-weight="800">{total_stars}</text>
    <text x="432" y="344" fill="#72C8FF" font-size="11" font-family="Segoe UI, Arial, sans-serif" font-weight="700">ESTRELAS</text>

    <rect x="588" y="300" width="165" height="56" rx="16" fill="url(#glass)" stroke="#2B4F7C"/>
    <text x="614" y="325" fill="#FFFFFF" font-size="24" font-family="Segoe UI, Arial, sans-serif" font-weight="800">{total_forks}</text>
    <text x="614" y="344" fill="#72C8FF" font-size="11" font-family="Segoe UI, Arial, sans-serif" font-weight="700">FORKS</text>

    <rect x="770" y="300" width="188" height="56" rx="16" fill="url(#glass)" stroke="#2B4F7C"/>
    <text x="796" y="325" fill="#FFFFFF" font-size="24" font-family="Segoe UI, Arial, sans-serif" font-weight="800">{following}</text>
    <text x="796" y="344" fill="#72C8FF" font-size="11" font-family="Segoe UI, Arial, sans-serif" font-weight="700">SEGUINDO</text>
  </g>

  <!-- ondas animadas -->
  <path d="M0 254 C130 230, 260 272, 392 254 C520 236, 650 274, 782 254 C894 238, 955 246, 1000 256 L1000 380 L0 380 Z"
        fill="url(#ocean1)">
    <animateTransform attributeName="transform" type="translate" values="-10 0;10 0;-10 0" dur="8s" repeatCount="indefinite"/>
  </path>

  <path d="M0 282 C142 258, 274 298, 414 280 C548 260, 680 298, 820 280 C918 264, 965 270, 1000 284 L1000 380 L0 380 Z"
        fill="url(#ocean2)">
    <animateTransform attributeName="transform" type="translate" values="12 0;-12 0;12 0" dur="10s" repeatCount="indefinite"/>
  </path>
</svg>
"""

    os.makedirs("assets", exist_ok=True)

    with open("assets/cabo-verde-dev-pulse.svg", "w", encoding="utf-8") as file:
        file.write(svg)

    print("Cabo Verde Dev Pulse generated successfully.")


if __name__ == "__main__":
    main()
