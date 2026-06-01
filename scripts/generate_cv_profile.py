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

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="360" viewBox="0 0 1000 360">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#001B44"/>
      <stop offset="45%" stop-color="#002756"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>

    <linearGradient id="ocean1" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00AEEF" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#003893" stop-opacity="0.12"/>
    </linearGradient>

    <linearGradient id="ocean2" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F7D116" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.06"/>
    </linearGradient>

    <filter id="glow">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="1000" height="360" rx="26" fill="url(#bg)"/>

  <circle cx="920" cy="60" r="52" fill="#00AEEF" opacity="0.06">
    <animate attributeName="r" values="45;58;45" dur="4s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.04;0.09;0.04" dur="4s" repeatCount="indefinite"/>
  </circle>

  <circle cx="140" cy="255" r="90" fill="#00AEEF" opacity="0.05">
    <animate attributeName="r" values="80;100;80" dur="6s" repeatCount="indefinite"/>
  </circle>

  <!-- Símbolo circular inspirado nas estrelas da bandeira -->
  <g filter="url(#glow)">
    <circle cx="82" cy="70" r="28" fill="#003893" opacity="0.95"/>
    <circle cx="82" cy="70" r="7" fill="#F7D116"/>
    <circle cx="61" cy="53" r="4" fill="#F7D116"/>
    <circle cx="103" cy="53" r="4" fill="#F7D116"/>
    <circle cx="61" cy="87" r="4" fill="#F7D116"/>
    <circle cx="103" cy="87" r="4" fill="#F7D116"/>
    <circle cx="82" cy="43" r="4" fill="#F7D116"/>
    <circle cx="82" cy="97" r="4" fill="#F7D116"/>
  </g>

  <!-- Faixas da bandeira -->
  <rect x="126" y="47" width="150" height="7" rx="3" fill="#FFFFFF"/>
  <rect x="126" y="60" width="150" height="7" rx="3" fill="#CF2027"/>
  <rect x="126" y="73" width="150" height="7" rx="3" fill="#FFFFFF"/>

  <!-- Bandeira de Cabo Verde animada -->
  <g transform="translate(835 35)">
    <rect x="-20" y="-12" width="130" height="108" rx="18" fill="#08131f" fill-opacity="0.35" stroke="#1E3A5F"/>
    <line x1="10" y1="10" x2="10" y2="82" stroke="#DCEBFF" stroke-width="3"/>

    <g>
      <animateTransform attributeName="transform" type="rotate" values="-1 10 14;2 10 14;-1 10 14" dur="5s" repeatCount="indefinite"/>

      <path fill="#003893">
        <animate attributeName="d" dur="5s" repeatCount="indefinite"
          values="
            M10 14 C30 7, 52 21, 80 14 L80 62 C52 69, 30 55, 10 62 Z;
            M10 14 C30 11, 52 17, 80 14 L80 62 C52 65, 30 59, 10 62 Z;
            M10 14 C30 7, 52 21, 80 14 L80 62 C52 69, 30 55, 10 62 Z"/>
      </path>

      <path fill="#FFFFFF">
        <animate attributeName="d" dur="5s" repeatCount="indefinite"
          values="
            M10 32 C30 29, 52 35, 80 32 L80 37 C52 40, 30 34, 10 37 Z;
            M10 32 C30 30, 52 34, 80 32 L80 37 C52 39, 30 35, 10 37 Z;
            M10 32 C30 29, 52 35, 80 32 L80 37 C52 40, 30 34, 10 37 Z"/>
      </path>

      <path fill="#CF2027">
        <animate attributeName="d" dur="5s" repeatCount="indefinite"
          values="
            M10 37 C30 34, 52 40, 80 37 L80 45 C52 48, 30 42, 10 45 Z;
            M10 37 C30 35, 52 39, 80 37 L80 45 C52 47, 30 43, 10 45 Z;
            M10 37 C30 34, 52 40, 80 37 L80 45 C52 48, 30 42, 10 45 Z"/>
      </path>

      <path fill="#FFFFFF">
        <animate attributeName="d" dur="5s" repeatCount="indefinite"
          values="
            M10 45 C30 42, 52 48, 80 45 L80 50 C52 53, 30 47, 10 50 Z;
            M10 45 C30 43, 52 47, 80 45 L80 50 C52 52, 30 48, 10 50 Z;
            M10 45 C30 42, 52 48, 80 45 L80 50 C52 53, 30 47, 10 50 Z"/>
      </path>

      <g fill="#F7D116">
        <polygon points="33,20 34.5,24 39,24 35.3,26.6 36.8,30.8 33,28.2 29.2,30.8 30.7,26.6 27,24 31.5,24"/>
        <polygon points="45,16 46.5,20 51,20 47.3,22.6 48.8,26.8 45,24.2 41.2,26.8 42.7,22.6 39,20 43.5,20"/>
        <polygon points="57,20 58.5,24 63,24 59.3,26.6 60.8,30.8 57,28.2 53.2,30.8 54.7,26.6 51,24 55.5,24"/>

        <polygon points="27,32 28.5,36 33,36 29.3,38.6 30.8,42.8 27,40.2 23.2,42.8 24.7,38.6 21,36 25.5,36"/>
        <polygon points="63,32 64.5,36 69,36 65.3,38.6 66.8,42.8 63,40.2 59.2,42.8 60.7,38.6 57,36 61.5,36"/>

        <polygon points="27,46 28.5,50 33,50 29.3,52.6 30.8,56.8 27,54.2 23.2,56.8 24.7,52.6 21,50 25.5,50"/>
        <polygon points="63,46 64.5,50 69,50 65.3,52.6 66.8,56.8 63,54.2 59.2,56.8 60.7,52.6 57,50 61.5,50"/>

        <polygon points="33,58 34.5,62 39,62 35.3,64.6 36.8,68.8 33,66.2 29.2,68.8 30.7,64.6 27,62 31.5,62"/>
        <polygon points="45,62 46.5,66 51,66 47.3,68.6 48.8,72.8 45,70.2 41.2,72.8 42.7,68.6 39,66 43.5,66"/>
        <polygon points="57,58 58.5,62 63,62 59.3,64.6 60.8,68.8 57,66.2 53.2,68.8 54.7,64.6 51,62 55.5,62"/>
      </g>
    </g>
  </g>

  <!-- Título -->
  <text x="50" y="132" fill="#FFFFFF" font-size="34" font-family="Segoe UI, Arial, sans-serif" font-weight="800">
    Cabo Verde Dev Pulse
  </text>

  <text x="50" y="162" fill="#B9D9FF" font-size="17" font-family="Segoe UI, Arial, sans-serif" font-weight="500">
    Morabeza • Código • Segurança • Java Full Stack
  </text>

  <text x="50" y="190" fill="#DCEBFF" font-size="13" font-family="Segoe UI, Arial, sans-serif">
    Perfil: {esc(USERNAME)} • Praia, Santiago, Cabo Verde • Atualizado: {esc(updated)}
  </text>

  <!-- Ilhas brilhando -->
  <g filter="url(#glow)">
    <circle cx="88" cy="222" r="3.6" fill="#F7D116">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="112" cy="210" r="3.6" fill="#FFFFFF">
      <animate attributeName="opacity" values="1;0.3;1" dur="2.4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="138" cy="228" r="3.6" fill="#F7D116">
      <animate attributeName="opacity" values="0.4;1;0.4" dur="2.6s" repeatCount="indefinite"/>
    </circle>
    <circle cx="162" cy="214" r="3.6" fill="#FFFFFF">
      <animate attributeName="opacity" values="1;0.3;1" dur="2.2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="184" cy="238" r="3.6" fill="#F7D116">
      <animate attributeName="opacity" values="0.4;1;0.4" dur="2.8s" repeatCount="indefinite"/>
    </circle>
    <circle cx="72" cy="244" r="3.6" fill="#FFFFFF">
      <animate attributeName="opacity" values="1;0.35;1" dur="2.1s" repeatCount="indefinite"/>
    </circle>
    <circle cx="132" cy="254" r="3.6" fill="#F7D116">
      <animate attributeName="opacity" values="0.4;1;0.4" dur="2.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="166" cy="268" r="3.6" fill="#FFFFFF">
      <animate attributeName="opacity" values="1;0.3;1" dur="2.7s" repeatCount="indefinite"/>
    </circle>
    <circle cx="206" cy="276" r="3.6" fill="#F7D116">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2.9s" repeatCount="indefinite"/>
    </circle>
    <circle cx="90" cy="280" r="3.6" fill="#FFFFFF">
      <animate attributeName="opacity" values="1;0.35;1" dur="2.3s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- Card stack flutuante -->
  <g>
    <animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="4.5s" repeatCount="indefinite"/>
    <rect x="610" y="48" width="330" height="112" rx="20" fill="#0B1220" fill-opacity="0.84" stroke="#1E3A5F"/>
    <text x="635" y="77" fill="#7CC7FF" font-size="13" font-family="Segoe UI, Arial, sans-serif" font-weight="700">
      STACK EM EVOLUÇÃO
    </text>
    <text x="635" y="105" fill="#FFFFFF" font-size="16" font-family="Segoe UI, Arial, sans-serif" font-weight="600">
      {esc(main_stack)}
    </text>
    <text x="635" y="132" fill="#C9E3FF" font-size="12" font-family="Segoe UI, Arial, sans-serif">
      Linguagens no GitHub: {esc(real_languages)}
    </text>
    <text x="635" y="150" fill="#93C5FD" font-size="12" font-family="Segoe UI, Arial, sans-serif">
      Construindo soluções modernas e escaláveis.
    </text>
  </g>

  <text x="690" y="228" fill="#C9E3FF" font-size="12" font-family="Segoe UI, Arial, sans-serif">
    10 ilhas • 1 visão • tecnologia com identidade
  </text>

  <!-- Cards de dados -->
  <rect x="50" y="285" width="165" height="54" rx="15" fill="#0B1220" fill-opacity="0.86" stroke="#1E3A5F"/>
  <text x="76" y="310" fill="#FFFFFF" font-size="24" font-family="Segoe UI, Arial, sans-serif" font-weight="800">{public_repos}</text>
  <text x="76" y="329" fill="#7CC7FF" font-size="11" font-family="Segoe UI, Arial, sans-serif" font-weight="700">REPOSITÓRIOS</text>

  <rect x="232" y="285" width="165" height="54" rx="15" fill="#0B1220" fill-opacity="0.86" stroke="#1E3A5F"/>
  <text x="258" y="310" fill="#FFFFFF" font-size="24" font-family="Segoe UI, Arial, sans-serif" font-weight="800">{followers}</text>
  <text x="258" y="329" fill="#7CC7FF" font-size="11" font-family="Segoe UI, Arial, sans-serif" font-weight="700">SEGUIDORES</text>

  <rect x="414" y="285" width="165" height="54" rx="15" fill="#0B1220" fill-opacity="0.86" stroke="#1E3A5F"/>
  <text x="440" y="310" fill="#FFFFFF" font-size="24" font-family="Segoe UI, Arial, sans-serif" font-weight="800">{total_stars}</text>
  <text x="440" y="329" fill="#7CC7FF" font-size="11" font-family="Segoe UI, Arial, sans-serif" font-weight="700">ESTRELAS</text>

  <rect x="596" y="285" width="165" height="54" rx="15" fill="#0B1220" fill-opacity="0.86" stroke="#1E3A5F"/>
  <text x="622" y="310" fill="#FFFFFF" font-size="24" font-family="Segoe UI, Arial, sans-serif" font-weight="800">{total_forks}</text>
  <text x="622" y="329" fill="#7CC7FF" font-size="11" font-family="Segoe UI, Arial, sans-serif" font-weight="700">FORKS</text>

  <rect x="778" y="285" width="172" height="54" rx="15" fill="#0B1220" fill-opacity="0.86" stroke="#1E3A5F"/>
  <text x="804" y="310" fill="#FFFFFF" font-size="24" font-family="Segoe UI, Arial, sans-serif" font-weight="800">{following}</text>
  <text x="804" y="329" fill="#7CC7FF" font-size="11" font-family="Segoe UI, Arial, sans-serif" font-weight="700">SEGUINDO</text>

  <!-- Ondas animadas -->
  <path d="M0 250 C130 225, 260 270, 390 250 C520 225, 650 270, 780 250 C900 230, 960 242, 1000 252 L1000 360 L0 360 Z"
        fill="url(#ocean1)">
    <animateTransform attributeName="transform" type="translate" values="-10 0;10 0;-10 0" dur="8s" repeatCount="indefinite"/>
  </path>

  <path d="M0 278 C140 255, 270 295, 410 276 C540 256, 670 295, 810 276 C910 260, 960 268, 1000 280 L1000 360 L0 360 Z"
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
