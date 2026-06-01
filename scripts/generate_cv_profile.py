import os
import json
import html
import math
import urllib.request
import urllib.error
from datetime import datetime, timedelta


USERNAME = os.getenv("GITHUB_USERNAME", "claudiogt1992-netizen")
TOKEN = os.getenv("GITHUB_TOKEN", "")


def esc(value):
    return html.escape(str(value), quote=True)


def github_get(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "cabo-verde-dev-pulse-generator",
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
        chunk = github_get(url)
        if not chunk:
            break
        repos.extend(chunk)
        if len(chunk) < 100:
            break
        page += 1
    return repos


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


def star_ring(cx, cy, ring_r, star_outer, star_inner, count=10, start_deg=-90, animate=True, id_prefix="ring"):
    parts = []
    for i in range(count):
        angle = math.radians(start_deg + i * (360 / count))
        sx = cx + math.cos(angle) * ring_r
        sy = cy + math.sin(angle) * ring_r
        pts = star_points(sx, sy, star_outer, star_inner)
        dur = 1.9 + (i % 4) * 0.22
        begin = -(i * 0.14)
        if animate:
            parts.append(
                f"""
                <polygon points="{pts}" fill="#F7D116" opacity="0.88">
                  <animate attributeName="opacity" values="0.45;1;0.45" dur="{dur:.2f}s" begin="{begin:.2f}s" repeatCount="indefinite"/>
                  <animate attributeName="transform" attributeType="XML"
                           type="scale" values="0.96 0.96;1.08 1.08;0.96 0.96"
                           dur="{dur:.2f}s" begin="{begin:.2f}s" repeatCount="indefinite"
                           additive="sum" />
                </polygon>
                """
            )
        else:
            parts.append(f'<polygon points="{pts}" fill="#F7D116" opacity="0.95"/>')
    return "\n".join(parts)


def technology_icons():
    return [
        ("java", "Java", "#23A4FF"),
        ("spring", "Spring Boot", "#75D13B"),
        ("react", "React", "#18E5FF"),
        ("angular", "Angular", "#FF2D55"),
        ("javascript", "JavaScript", "#FFD21F"),
        ("typescript", "TypeScript", "#2EA8FF"),
        ("python", "Python", "#F4C542"),
    ]


def icon_svg(kind, x, y, label, color, delay):
    common = f"""
    <g transform="translate({x} {y})">
      <animateTransform attributeName="transform" type="translate"
                        values="{x} {y};{x} {y-4};{x} {y}"
                        dur="3.8s" begin="-{delay:.2f}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.88;1;0.88" dur="2.8s" begin="-{delay:.2f}s" repeatCount="indefinite"/>
    """
    end = f"""
      <text x="64" y="12" fill="#F4F8FF" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="600">{esc(label)}</text>
    </g>
    """
    if kind == "java":
        body = f"""
      <g filter="url(#techGlow)">
        <path d="M31 4 C26 10, 38 12, 31 18 C27 21, 29 24, 34 26" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round"/>
        <path d="M38 0 C33 6, 43 8, 38 14 C34 17, 36 20, 41 22" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round" opacity="0.9"/>
        <path d="M16 27 C22 23, 42 22, 49 27" fill="none" stroke="{color}" stroke-width="3.5" stroke-linecap="round"/>
        <path d="M19 28 L21 45 C21.4 48 23 49 25 49 L39 49 C41 49 42.6 48 43 45 L45 28" fill="none" stroke="{color}" stroke-width="3.5" stroke-linejoin="round"/>
        <path d="M14 35 L18 36" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round"/>
        <path d="M46 36 L50 35" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round"/>
      </g>
        """
    elif kind == "spring":
        body = f"""
      <g filter="url(#techGlow)">
        <polygon points="33,2 53,14 53,38 33,50 13,38 13,14" fill="none" stroke="{color}" stroke-width="3.2" stroke-linejoin="round"/>
        <path d="M38 13 C31 14, 26 19, 25 26 C24 32, 27 38, 34 40 C42 42, 49 37, 49 28 C49 22, 45 17, 39 15 Z"
              fill="none" stroke="{color}" stroke-width="3.2" stroke-linejoin="round"/>
        <path d="M34 40 C33 29, 39 22, 46 18" fill="none" stroke="{color}" stroke-width="2.8" stroke-linecap="round"/>
      </g>
        """
    elif kind == "react":
        body = f"""
      <g filter="url(#techGlow)">
        <ellipse cx="33" cy="26" rx="24" ry="9" fill="none" stroke="{color}" stroke-width="3"/>
        <ellipse cx="33" cy="26" rx="24" ry="9" fill="none" stroke="{color}" stroke-width="3" transform="rotate(60 33 26)"/>
        <ellipse cx="33" cy="26" rx="24" ry="9" fill="none" stroke="{color}" stroke-width="3" transform="rotate(-60 33 26)"/>
        <circle cx="33" cy="26" r="4.6" fill="{color}"/>
      </g>
        """
    elif kind == "angular":
        body = f"""
      <g filter="url(#techGlow)">
        <polygon points="33,3 53,10 49,39 33,49 17,39 13,10" fill="none" stroke="{color}" stroke-width="3.2" stroke-linejoin="round"/>
        <path d="M33 14 L22 38" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round"/>
        <path d="M33 14 L44 38" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round"/>
        <path d="M26.5 29 L39.5 29" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round"/>
      </g>
        """
    elif kind == "javascript":
        body = f"""
      <g filter="url(#techGlow)">
        <rect x="10" y="4" width="46" height="46" rx="9" fill="none" stroke="{color}" stroke-width="3.2"/>
        <text x="18" y="37" fill="{color}" font-family="Segoe UI, Arial, sans-serif" font-size="22" font-weight="800">JS</text>
      </g>
        """
    elif kind == "typescript":
        body = f"""
      <g filter="url(#techGlow)">
        <rect x="10" y="4" width="46" height="46" rx="9" fill="none" stroke="{color}" stroke-width="3.2"/>
        <text x="16" y="37" fill="{color}" font-family="Segoe UI, Arial, sans-serif" font-size="22" font-weight="800">TS</text>
      </g>
        """
    else:  # python
        body = f"""
      <g filter="url(#techGlow)">
        <path d="M20 17 C20 10, 25 7, 32 7 L40 7 C46 7, 50 11, 50 17 L50 24 L29 24 C23 24, 19 28, 19 34 C19 41, 24 45, 30 45 L38 45 C44 45, 48 41, 48 35"
              fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="39" cy="15" r="1.8" fill="{color}"/>
        <path d="M46 36 C46 43, 41 46, 34 46 L26 46 C20 46, 16 42, 16 36 L16 29 L37 29 C43 29, 47 25, 47 19 C47 12, 42 8, 36 8 L28 8 C22 8, 18 12, 18 18"
              fill="none" stroke="#5AA9FF" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="27" cy="38" r="1.8" fill="#5AA9FF"/>
      </g>
        """
    return common + body + end


def stat_card(x, y, width, height, number, label, accent, delay, icon_kind):
    num_x = x + 85
    label_x = x + 85
    icon_x = x + 38
    icon_y = y + 42

    if icon_kind == "repo":
        icon = f"""
        <g transform="translate({icon_x} {icon_y})" stroke="{accent}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <rect x="-16" y="-18" width="32" height="36" rx="6"/>
          <path d="M-7 -8 H7"/>
          <path d="M-7 0 H10"/>
          <path d="M-7 8 H5"/>
        </g>
        """
    elif icon_kind == "followers":
        icon = f"""
        <g transform="translate({icon_x} {icon_y})" stroke="{accent}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="-6" cy="-8" r="7"/>
          <circle cx="10" cy="-2" r="6"/>
          <path d="M-18 18 C-16 7, 2 7, 6 18"/>
          <path d="M2 18 C4 10, 16 10, 20 18"/>
        </g>
        """
    elif icon_kind == "stars":
        icon = f"""
        <g transform="translate({icon_x} {icon_y})" stroke="{accent}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="{star_points(0, 0, 18, 8)}"/>
        </g>
        """
    elif icon_kind == "forks":
        icon = f"""
        <g transform="translate({icon_x} {icon_y})" stroke="{accent}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="0" cy="-16" r="5"/>
          <circle cx="-12" cy="16" r="5"/>
          <circle cx="12" cy="16" r="5"/>
          <path d="M0 -11 V4"/>
          <path d="M0 4 H-12 V11"/>
          <path d="M0 4 H12 V11"/>
        </g>
        """
    else:  # following
        icon = f"""
        <g transform="translate({icon_x} {icon_y})" stroke="{accent}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="0" cy="-8" r="10"/>
          <path d="M-18 18 C-15 5, 15 5, 18 18"/>
        </g>
        """

    return f"""
    <g transform="translate({x} {y})" filter="url(#shadowSoft)">
      <rect x="0" y="0" width="{width}" height="{height}" rx="24" fill="url(#cardGlass)" stroke="rgba(255,255,255,0.10)"/>
      <rect x="0.7" y="0.7" width="{width-1.4}" height="{height-1.4}" rx="23.3" fill="none" stroke="{accent}" stroke-opacity="0.30"/>
      <rect x="0" y="0" width="{width}" height="{height}" rx="24" fill="url(#cardInnerGlow)" opacity="0.55"/>
      <rect x="-70" y="-10" width="56" height="{height+20}" rx="18" fill="url(#shine)">
        <animateTransform attributeName="transform" type="translate"
                          values="0 0;{width+150} 0"
                          dur="4.8s" begin="-{delay:.2f}s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0;0.65;0" dur="4.8s" begin="-{delay:.2f}s" repeatCount="indefinite"/>
      </rect>
      <rect x="0" y="0" width="{width}" height="{height}" rx="24" fill="none" stroke="{accent}">
        <animate attributeName="stroke-opacity" values="0.22;0.58;0.22" dur="3.2s" begin="-{delay:.2f}s" repeatCount="indefinite"/>
      </rect>
      {icon}
      <text x="{num_x}" y="74" text-anchor="middle" fill="#FFFFFF" font-family="Segoe UI, Arial, sans-serif" font-size="30" font-weight="800">
        <animate attributeName="opacity" values="0.88;1;0.88" dur="2.6s" begin="-{delay:.2f}s" repeatCount="indefinite"/>
        {number}
      </text>
      <text x="{label_x}" y="112" text-anchor="middle" fill="#B8D9FF" font-family="Segoe UI, Arial, sans-serif" font-size="16" font-weight="600">{esc(label)}</text>
    </g>
    """


def main():
    os.makedirs("assets", exist_ok=True)

    try:
        user = github_get(f"https://api.github.com/users/{USERNAME}")
        repos = fetch_repos(USERNAME)
    except urllib.error.HTTPError as e:
        raise RuntimeError(
            f"GitHub API error {e.code}. Check GITHUB_USERNAME and GITHUB_TOKEN."
        ) from e
    except Exception as e:
        raise RuntimeError(f"Failed to fetch GitHub data: {e}") from e

    public_repos = int(user.get("public_repos", 0))
    followers = int(user.get("followers", 0))
    following = int(user.get("following", 0))
    total_stars = sum(int(repo.get("stargazers_count", 0)) for repo in repos)
    total_forks = sum(int(repo.get("forks_count", 0)) for repo in repos)

    updated = (datetime.utcnow() - timedelta(hours=1)).strftime("%d/%m/%Y %H:%M")

    tech_groups = []
    start_x = 150
    gap = 205
    tech_y = 402
    for idx, (kind, label, color) in enumerate(technology_icons()):
        tech_groups.append(icon_svg(kind, start_x + idx * gap, tech_y, label, color, idx * 0.22))
    tech_row_svg = "\n".join(tech_groups)

    cards = [
        stat_card(70, 530, 282, 132, public_repos, "Repositórios", "#38B6FF", 0.1, "repo"),
        stat_card(374, 530, 282, 132, followers, "Seguidores", "#53B8FF", 0.6, "followers"),
        stat_card(678, 530, 282, 132, total_stars, "Estrelas", "#43B4FF", 1.1, "stars"),
        stat_card(982, 530, 282, 132, total_forks, "Forks", "#8E6BFF", 1.6, "forks"),
        stat_card(1286, 530, 292, 132, following, "Seguindo", "#B26BFF", 2.1, "following"),
    ]
    cards_svg = "\n".join(cards)

    header_stars = star_ring(88, 93, 52, 8.5, 3.8, 10, -90, True, "header")
    flag_stars = star_ring(74, 50, 27, 4.3, 1.9, 10, -90, False, "flag")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1650" height="820" viewBox="0 0 1650 820" role="img" aria-label="Cabo Verde Dev Pulse">
  <defs>
    <linearGradient id="bgMain" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#050B18"/>
      <stop offset="42%" stop-color="#071733"/>
      <stop offset="72%" stop-color="#061128"/>
      <stop offset="100%" stop-color="#040913"/>
    </linearGradient>

    <linearGradient id="cyanBeam" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00D1FF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#00D1FF" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#00D1FF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="cardGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10264C" stop-opacity="0.68"/>
      <stop offset="100%" stop-color="#0A1630" stop-opacity="0.52"/>
    </linearGradient>

    <linearGradient id="cardInnerGlow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1A3F7A" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#0A1733" stop-opacity="0.03"/>
    </linearGradient>

    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#BFEFFF" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="ocean1" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00CFFF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#005CFF" stop-opacity="0.08"/>
    </linearGradient>

    <linearGradient id="ocean2" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F7D116" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.05"/>
    </linearGradient>

    <radialGradient id="blueGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00CFFF" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#00CFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="glowSoft" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="techGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3.2" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="shadowSoft" x="-25%" y="-25%" width="170%" height="170%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.28"/>
    </filter>
  </defs>

  <rect width="1650" height="820" rx="34" fill="url(#bgMain)"/>

  <!-- ambient glows -->
  <circle cx="250" cy="160" r="180" fill="url(#blueGlow)" opacity="0.55">
    <animate attributeName="r" values="165;195;165" dur="8s" repeatCount="indefinite"/>
  </circle>
  <circle cx="1430" cy="116" r="140" fill="url(#blueGlow)" opacity="0.42">
    <animate attributeName="r" values="126;154;126" dur="7s" repeatCount="indefinite"/>
  </circle>

  <!-- subtle digital lines -->
  <g opacity="0.18" stroke="#1ED6FF" stroke-width="2" fill="none">
    <path d="M40 70 H160 L210 120 H310"/>
    <path d="M1335 66 H1495 L1560 130 H1615"/>
    <path d="M70 725 H230 L290 682 H420"/>
    <path d="M1250 728 H1425 L1490 690 H1600"/>
  </g>

  <!-- animated particles -->
  <g fill="#46CCFF" opacity="0.65">
    <circle cx="310" cy="86" r="3">
      <animate attributeName="opacity" values="0.25;1;0.25" dur="2.6s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1280" cy="110" r="3">
      <animate attributeName="opacity" values="1;0.2;1" dur="2.9s" repeatCount="indefinite"/>
    </circle>
    <circle cx="525" cy="298" r="2.8">
      <animate attributeName="opacity" values="0.2;1;0.2" dur="3.1s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1038" cy="302" r="2.8">
      <animate attributeName="opacity" values="1;0.3;1" dur="3.0s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1460" cy="264" r="3">
      <animate attributeName="opacity" values="0.2;1;0.2" dur="2.7s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- header -->
  <g transform="translate(70 54)">
    <g filter="url(#glowSoft)">
      <circle cx="88" cy="93" r="70" fill="#0D3D99" stroke="#2D66C9" stroke-width="3"/>
      <rect x="26" y="78" width="124" height="16" rx="8" fill="#FFFFFF"/>
      <rect x="26" y="94" width="124" height="16" rx="8" fill="#CF2027"/>
      <rect x="26" y="110" width="124" height="16" rx="8" fill="#FFFFFF"/>
      {header_stars}
    </g>

    <line x1="182" y1="28" x2="182" y2="157" stroke="#3B76D8" stroke-opacity="0.55" stroke-width="3"/>

    <text x="216" y="70" fill="#FFFFFF" font-family="Segoe UI, Arial, sans-serif" font-size="40" font-weight="800">Cabo Verde Dev Pulse</text>
    <text x="216" y="121" fill="#D5E7FF" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="600">{esc(USERNAME)} • Cabo Verde • Systems Engineering &amp; Computer Science Student</text>
    <text x="216" y="150" fill="#8ABFFF" font-family="Segoe UI, Arial, sans-serif" font-size="15">Atualizado: {esc(updated)}</text>

    <!-- waving flag without pole -->
    <g transform="translate(1320 4)" filter="url(#shadowSoft)">
      <rect x="0" y="0" width="190" height="150" rx="28" fill="#09162D" fill-opacity="0.55" stroke="#255189" stroke-opacity="0.55"/>
      <g transform="translate(30 24)">
        <animateTransform attributeName="transform" type="translate" values="30 24;30 18;30 24" dur="4.2s" repeatCount="indefinite"/>
        <g>
          <animateTransform attributeName="transform" type="rotate" values="-4 10 10;4 10 10;-4 10 10" dur="4.4s" repeatCount="indefinite"/>
          <path fill="#003893">
            <animate attributeName="d" dur="4.4s" repeatCount="indefinite"
              values="
                M0 12 C26 1, 62 21, 126 12 L126 92 C62 103, 26 83, 0 92 Z;
                M0 12 C26 7, 62 17, 126 12 L126 92 C62 97, 26 87, 0 92 Z;
                M0 12 C26 1, 62 21, 126 12 L126 92 C62 103, 26 83, 0 92 Z"/>
          </path>
          <path fill="#FFFFFF">
            <animate attributeName="d" dur="4.4s" repeatCount="indefinite"
              values="
                M0 44 C26 39, 62 49, 126 44 L126 53 C62 58, 26 48, 0 53 Z;
                M0 44 C26 41, 62 47, 126 44 L126 53 C62 56, 26 50, 0 53 Z;
                M0 44 C26 39, 62 49, 126 44 L126 53 C62 58, 26 48, 0 53 Z"/>
          </path>
          <path fill="#CF2027">
            <animate attributeName="d" dur="4.4s" repeatCount="indefinite"
              values="
                M0 53 C26 48, 62 58, 126 53 L126 66 C62 71, 26 61, 0 66 Z;
                M0 53 C26 50, 62 56, 126 53 L126 66 C62 69, 26 63, 0 66 Z;
                M0 53 C26 48, 62 58, 126 53 L126 66 C62 71, 26 61, 0 66 Z"/>
          </path>
          <path fill="#FFFFFF">
            <animate attributeName="d" dur="4.4s" repeatCount="indefinite"
              values="
                M0 66 C26 61, 62 71, 126 66 L126 75 C62 80, 26 70, 0 75 Z;
                M0 66 C26 63, 62 69, 126 66 L126 75 C62 78, 26 72, 0 75 Z;
                M0 66 C26 61, 62 71, 126 66 L126 75 C62 80, 26 70, 0 75 Z"/>
          </path>
          <g>{flag_stars}</g>
        </g>
      </g>
    </g>
  </g>

  <!-- divider -->
  <line x1="70" y1="218" x2="1580" y2="218" stroke="#214B88" stroke-opacity="0.60" stroke-width="2"/>

  <!-- main title -->
  <text x="825" y="356" text-anchor="middle" fill="#F7FBFF" font-family="Segoe UI, Arial, sans-serif" font-size="84" font-weight="800">
    <tspan>Full Stack </tspan><tspan fill="#14C8FF">Java</tspan><tspan> Developer in Progress</tspan>
  </text>

  <!-- subtitle -->
  <g>
    <line x1="280" y1="420" x2="420" y2="420" stroke="#11C9FF" stroke-width="4" stroke-linecap="round"/>
    <line x1="1230" y1="420" x2="1370" y2="420" stroke="#11C9FF" stroke-width="4" stroke-linecap="round"/>
    <text x="825" y="432" text-anchor="middle" fill="#A9C8FF" font-family="Segoe UI, Arial, sans-serif" font-size="26" font-weight="500">Systems Engineering &amp; Computer Science Student</text>
  </g>

  <!-- technology row -->
  <g>
    {tech_row_svg}
  </g>

  <!-- stats cards -->
  <g>
    {cards_svg}
  </g>

  <!-- footer slogan -->
  <g transform="translate(825 758)">
    <g filter="url(#techGlow)" opacity="0.95">
      <path d="M-150 2 L-138 -6 L-126 0 L-116 -8 L-104 -2 L-92 -10 L-80 -4" fill="none" stroke="#0EC8FF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="-138" cy="-6" r="2.8" fill="#0EC8FF"/>
      <circle cx="-116" cy="-8" r="2.8" fill="#0EC8FF"/>
      <circle cx="-92" cy="-10" r="2.8" fill="#0EC8FF"/>
    </g>
    <text x="0" y="10" text-anchor="middle" fill="#CDE3FF" font-family="Segoe UI, Arial, sans-serif" font-size="20" font-weight="500">10 ilhas • 1 visão • tecnologia com identidade</text>
  </g>

  <!-- subtle ocean movement -->
  <path d="M0 620 C160 596, 330 654, 500 628 C680 600, 860 660, 1040 630 C1200 604, 1380 654, 1650 622 L1650 820 L0 820 Z"
        fill="url(#ocean1)">
    <animateTransform attributeName="transform" type="translate" values="-20 0;20 0;-20 0" dur="8s" repeatCount="indefinite"/>
  </path>

  <path d="M0 650 C190 626, 380 690, 560 662 C760 632, 950 696, 1130 665 C1310 638, 1480 686, 1650 658 L1650 820 L0 820 Z"
        fill="url(#ocean2)">
    <animateTransform attributeName="transform" type="translate" values="22 0;-22 0;22 0" dur="10.5s" repeatCount="indefinite"/>
  </path>

  <!-- soft foreground digital beam -->
  <rect x="-120" y="0" width="90" height="820" fill="url(#cyanBeam)" opacity="0.14">
    <animateTransform attributeName="transform" type="translate" values="0 0;1860 0" dur="16s" repeatCount="indefinite"/>
  </rect>
</svg>
"""

    with open("assets/cabo-verde-dev-pulse.svg", "w", encoding="utf-8") as f:
        f.write(svg)

    print("SVG generated successfully: assets/cabo-verde-dev-pulse.svg")


if __name__ == "__main__":
    main()
