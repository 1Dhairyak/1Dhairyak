"""Builds README.md + assets/*.svg from live GitHub data. Run: python build.py
Token: $GH_TOKEN, else `gh auth token`. Needs Pillow for the ASCII portrait."""
import io, json, os, subprocess, urllib.request
from datetime import date, datetime, timedelta
from html import escape
from PIL import Image, ImageOps

# ---- edit me -------------------------------------------------------------
LOGIN = "1Dhairyak"
NAME = "Dhairya"
ROLE = "Cloud & Backend Engineer"
QUOTE = "I build full-stack cloud systems by day and play story-driven games by night."
FOCUS = [("Java / Spring Boot", "Current focus"),
         ("AWS / Azure", "In the build queue"),
         ("C++ / DSA", "Currently learning")]
FEATURED = [  # (repo, display name)
    ("Spotify-YouTube-music-visualizer-software", "music-visualizer"),
    ("Nova-stack-Full-stack-space-data-dashboard-with-real-time-WebSocket-streaming", "nova-stack"),
    ("SearchWars", "searchwars"),
    ("-N-Queens-Visualizer-description-", "n-queens"),
]
LINKS = [("GitHub", f"https://github.com/{LOGIN}", f"@{LOGIN.lower()}"),
         ("LinkedIn", "https://linkedin.com/in/dhairya153", "in/dhairya153"),
         ("Email", "mailto:dhairyakumar490@gmail.com", "dhairyakumar490@gmail.com"),
         ("Instagram", "https://instagram.com/dhairya_68", "@dhairya_68"),
         ("Bluesky", "https://bsky.app/profile/dhairya", "@dhairya")]
# --------------------------------------------------------------------------

BG, CARD, LINE, ACC, TXT, MUT = "#070b16", "#0b1124", "#1b2442", "#8b9bff", "#e8ebf7", "#6b7497"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
LANG = {"Java": ("#b07219", "JV"), "JavaScript": ("#f1e05a", "JS"), "TypeScript": ("#3178c6", "TS"),
        "HTML": ("#e34c26", "H5"), "CSS": ("#563d7c", "CS"), "Python": ("#3572A5", "PY"),
        "C#": ("#178600", "C#"), "C++": ("#f34b7d", "C+"), "C": ("#555555", "C")}
W = 1200


def token():
    return os.environ.get("GH_TOKEN") or subprocess.check_output(["gh", "auth", "token"], text=True).strip()


def fetch():
    q = """query($l:String!){user(login:$l){avatarUrl followers{totalCount}
      repositories(first:100,ownerAffiliations:OWNER,privacy:PUBLIC){totalCount nodes{name description url
        stargazerCount isFork pushedAt primaryLanguage{name} languages(first:10){edges{size node{name}}}}}
      contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
    req = urllib.request.Request("https://api.github.com/graphql",
                                 json.dumps({"query": q, "variables": {"l": LOGIN}}).encode(),
                                 {"Authorization": f"bearer {token()}"})
    return json.load(urllib.request.urlopen(req))["data"]["user"]


def svg(h, body, extra_css=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
<style>text{{font-family:{MONO}}} .e{{fill:{MUT};font-size:11px;letter-spacing:3px}} .t{{fill:{TXT};font-size:26px}}
.m{{fill:{MUT};font-size:12px}} .w{{fill:{TXT}}} .a{{fill:{ACC}}}
.in{{opacity:0;animation:in .9s ease forwards}} @keyframes in{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.pulse{{animation:pulse 2.4s ease-in-out infinite}} @keyframes pulse{{50%{{opacity:.25}}}}
{extra_css}</style>
<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="18" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>
{body}</svg>"""


def head(eyebrow, title):
    return (f'<text x="40" y="52" class="e">{eyebrow}</text><text x="40" y="94" class="t">{title}</text>'
            f'<line x1="40" y1="124" x2="{W-40}" y2="124" stroke="{LINE}" stroke-dasharray="6 6"/>')


def ascii_portrait(url, cols=78, rows=46):
    img = Image.open(io.BytesIO(urllib.request.urlopen(url + "&s=400").read())).convert("L")
    img = ImageOps.autocontrast(ImageOps.fit(img, (cols, rows * 2))).resize((cols, rows))
    ramp = " .:-=+*#%@"
    px = img.tobytes()
    return ["".join(ramp[p * (len(ramp) - 1) // 255] for p in px[r * cols:(r + 1) * cols]) for r in range(rows)]


def hero(u, stats):
    lines = ascii_portrait(u["avatarUrl"])
    art = "".join(f'<text x="770" y="{78 + i * 7.6:.1f}" xml:space="preserve" font-size="7.4" class="a">{escape(l)}</text>'
                  for i, l in enumerate(lines))
    cells = "".join(
        f'<g class="in" style="animation-delay:{1.2 + i * .15}s"><text x="{40 + i * 285}" y="478" class="e">{k.upper()}</text>'
        f'<text x="{40 + i * 285}" y="522" class="w" font-size="30">{v:,}</text>'
        f'<circle cx="{280 + i * 285}" cy="474" r="3" class="a pulse"/></g>' for i, (k, v) in enumerate(stats))
    css = (".nm{fill:transparent;stroke:#dfe4ff;stroke-width:1.6;stroke-dasharray:900;stroke-dashoffset:900;"
           "animation:draw 3s ease forwards,fillin 1s 2.6s forwards} @keyframes draw{to{stroke-dashoffset:0}}"
           "@keyframes fillin{to{fill:#dfe4ff1f}} .spin{transform-origin:955px 245px;animation:spin 40s linear infinite}"
           "@keyframes spin{to{transform:rotate(360deg)}} .scan{animation:scan 4s ease-in-out infinite}"
           "@keyframes scan{0%{transform:translateY(0);opacity:0}10%,90%{opacity:.8}100%{transform:translateY(340px);opacity:0}}"
           ".port{opacity:0;animation:in 2s .4s forwards}"
           ".cur{animation:blink 1s steps(1) infinite} @keyframes blink{50%{opacity:0}}")
    body = f"""<text x="40" y="52" class="e">{LOGIN.upper()} / LIVING IDENTITY</text>
<text x="{W-40}" y="52" class="e" text-anchor="end">@{LOGIN.lower()}</text>
<text x="40" y="150" class="e">HELLO, WORLD. I'M<tspan class="cur a"> _</tspan></text>
<text x="36" y="250" class="nm" font-size="96" font-weight="700">{escape(NAME)}</text>
<text x="40" y="318" class="w in" font-size="18" font-weight="700" style="animation-delay:1.8s">{' / '.join(escape(f[0].split(' /')[0]) for f in FOCUS)}</text>
<text x="40" y="344" class="m in" style="animation-delay:2s">{escape(ROLE)}</text>
<g class="spin"><circle cx="955" cy="245" r="200" fill="none" stroke="{LINE}" stroke-dasharray="2 10"/>
<circle cx="955" cy="245" r="218" fill="none" stroke="{ACC}" stroke-opacity=".25" stroke-dasharray="80 500"/></g>
<defs><radialGradient id="fade"><stop offset="55%" stop-color="#fff"/><stop offset="100%" stop-color="#000"/></radialGradient>
<mask id="pm"><rect x="770" y="66" width="350" height="356" fill="url(#fade)"/></mask></defs>
<g mask="url(#pm)"><g class="port">{art}</g><rect x="770" y="70" width="350" height="2" fill="{ACC}" class="scan"/></g>
<line x1="40" y1="430" x2="{W-40}" y2="430" stroke="{LINE}"/>{cells}"""
    return svg(560, body, css)


def focus():
    cols = "".join(
        f'<g class="in" style="animation-delay:{.2 + i * .25}s"><text x="{40 + i * 375}" y="190" class="a" font-size="34">{i + 1:02d}</text>'
        f'<line x1="{40 + i * 375}" y1="212" x2="{370 + i * 375}" y2="212" stroke="{LINE}"/>'
        f'<text x="{40 + i * 375}" y="250" class="w" font-size="20">{escape(n)}</text>'
        f'<text x="{40 + i * 375}" y="278" class="m">{escape(s)}</text></g>' for i, (n, s) in enumerate(FOCUS))
    return svg(330, head("WHAT MOVES THE WORK", "Three threads, one direction") + cols)


def tools(langs):
    out = []
    for i, (n, pct) in enumerate(langs[:8]):
        x, y = 40 + (i % 4) * 285, 170 + (i // 4) * 120
        c, ab = LANG.get(n, (ACC, n[:2].upper()))
        out.append(
            f'<g class="in" style="animation-delay:{i * .12}s"><rect x="{x}" y="{y}" width="30" height="30" rx="6" fill="{c}" fill-opacity=".9"/>'
            f'<text x="{x + 15}" y="{y + 20}" text-anchor="middle" font-size="11" font-weight="700" fill="#0b1124">{ab}</text>'
            f'<text x="{x}" y="{y + 54}" class="w" font-size="16">{escape(n)}</text>'
            f'<text x="{x}" y="{y + 74}" class="m" font-size="11">{pct:.0f}% of public code</text>'
            f'<rect x="{x}" y="{y + 86}" width="240" height="3" rx="2" fill="{LINE}"/>'
            f'<rect x="{x}" y="{y + 86}" width="{max(4, 240 * pct / 100):.0f}" height="3" rx="2" fill="{c}"/></g>')
    h = 170 + ((len(langs[:8]) + 3) // 4) * 120 + 20
    return svg(h, head("TECHNOLOGY SPECTRUM", "The tools behind the work") + "".join(out))


def node(x, y, r, lang, i):
    c, ab = LANG.get(lang, (ACC, "··"))
    return (f'<g class="in" style="animation-delay:{i * .2}s"><circle cx="{x}" cy="{y}" r="{r + 10}" fill="none" stroke="{ACC}" stroke-opacity=".3" stroke-dasharray="3 5" class="pulse"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#16204a"/><rect x="{x - 11}" y="{y - 11}" width="22" height="22" rx="4" fill="{c}"/>'
            f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="9" font-weight="700" fill="#0b1124">{ab}</text></g>')


def constellation(projs):
    pos = [(600, 260, 46), (260, 230, 26), (900, 200, 26), (860, 360, 24)]
    links = "".join(f'<line x1="600" y1="260" x2="{x}" y2="{y}" stroke="{ACC}" stroke-opacity=".35" stroke-dasharray="3 6"/>' for x, y, _ in pos[1:])
    nodes = "".join(node(x, y, r, p["lang"], i) +
                    f'<text x="{x}" y="{y + r + 30}" text-anchor="middle" class="w" font-size="15">{escape(p["alias"])}</text>'
                    f'<text x="{x}" y="{y + r + 48}" text-anchor="middle" class="m" font-size="11">{escape(p["lang"])} · updated {p["pushed"]:%b %Y}</text>'
                    for i, ((x, y, r), p) in enumerate(zip(pos, projs)))
    return svg(460, head("PROJECT CONSTELLATION", "A universe of work") + links + nodes)


def launch(projs):
    seq = sorted(projs, key=lambda p: p["pushed"])
    xs = [150 + i * 300 for i in range(len(seq))]
    css = ".flow{stroke-dasharray:6 8;animation:flow 1.5s linear infinite} @keyframes flow{to{stroke-dashoffset:-28}}"
    out = [f'<line x1="80" y1="290" x2="{W-80}" y2="290" stroke="{ACC}" stroke-opacity=".5" class="flow"/>']
    for i, (x, p) in enumerate(zip(xs, seq)):
        up = i % 2 == 0
        ty = 190 if up else 350
        out.append(node(x, 290, 20, p["lang"], i))
        out.append(f'<g class="in" style="animation-delay:{.3 + i * .25}s"><text x="{x}" y="{ty - 22}" text-anchor="middle" class="m" font-size="11">{p["pushed"]:%d / %b %Y}</text>'
                   f'<text x="{x}" y="{ty}" text-anchor="middle" class="w" font-size="16">{escape(p["alias"])}</text>'
                   f'<text x="{x}" y="{ty + 20}" text-anchor="middle" class="m" font-size="11">{escape(p["desc"][:40])}</text>'
                   f'<text x="{x}" y="{ty + 38}" text-anchor="middle" class="a" font-size="11" opacity=".7">{escape(p["lang"])}</text></g>')
    out.append(f'<text x="40" y="440" class="m" font-size="11">{len(seq)} featured repositories · follow the line from first signal to latest motion</text>')
    return svg(470, head("PROJECT LAUNCH SEQUENCE", "Where the work went next") + "".join(out), css)


def momentum(stats):
    css = ".run{animation:run 3s ease-in-out infinite alternate} @keyframes run{to{transform:translateX(200px)}}"
    out = "".join(
        f'<g class="in" style="animation-delay:{i * .2}s"><text x="{40 + i * 285}" y="200" class="w" font-size="34">{v:,}</text>'
        f'<text x="{40 + i * 285}" y="228" class="e" font-size="10">{k.upper()}</text>'
        f'<line x1="{48 + i * 285}" y1="290" x2="{250 + i * 285}" y2="290" stroke="{LINE}" stroke-dasharray="4 6"/>'
        f'<circle cx="{48 + i * 285}" cy="290" r="7" class="a run" opacity=".8" style="animation-delay:{i * .4}s"/></g>'
        for i, (k, v) in enumerate(stats))
    return svg(350, head("PROFILE SIGNAL", "Momentum, made visible") + out, css)


def trail(days, total):
    mx = max([d["contributionCount"] for d in days] + [1])
    out = []
    for i, d in enumerate(days):
        c = d["contributionCount"]
        x, y = 48 + (i // 7) * 21, 170 + (i % 7) * 26
        r = 1.6 + 5 * (c / mx) ** .6 if c else 1.4
        op = .18 + .82 * (c / mx) ** .5 if c else .12
        tw = ' class="pulse" style="animation-delay:%.1fs"' % ((i * 37) % 24 / 10) if c >= mx * .5 else ""
        out.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{ACC}" opacity="{op:.2f}"{tw}/>')
    out.append(f'<text x="40" y="380" class="m" font-size="11">{total:,} contributions · brighter stars mark busier days</text>')
    return svg(410, head("CONTRIBUTION ENERGY", "Every day leaves a trace") + "".join(out))


def channel():
    css = ".orb{transform-origin:1000px 260px;animation:orb 6s ease-in-out infinite} @keyframes orb{50%{transform:scale(1.12);opacity:.5}}"
    rows = "".join(f'<g class="in" style="animation-delay:{i * .15}s"><circle cx="50" cy="{170 + i * 36}" r="4" class="a"/>'
                   f'<text x="70" y="{175 + i * 36}" class="e" font-size="10">{k.upper()}</text>'
                   f'<text x="210" y="{175 + i * 36}" class="w" font-size="14">{escape(h)}</text></g>' for i, (k, _, h) in enumerate(LINKS))
    orb = (f'<g class="orb"><circle cx="1000" cy="260" r="70" fill="none" stroke="{ACC}" stroke-opacity=".6"/>'
           f'<circle cx="1000" cy="260" r="110" fill="none" stroke="{ACC}" stroke-opacity=".2" stroke-dasharray="2 8"/></g>')
    return svg(150 + len(LINKS) * 36 + 60, head("OPEN CHANNEL", "Build the next chapter") + rows + orb, css)


def main():
    u = fetch()
    repos = [r for r in u["repositories"]["nodes"] if not r["isFork"]]
    by = {r["name"]: r for r in repos}
    sizes = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            sizes[e["node"]["name"]] = sizes.get(e["node"]["name"], 0) + e["size"]
    tot = sum(sizes.values()) or 1
    langs = sorted(((n, 100 * s / tot) for n, s in sizes.items()), key=lambda t: -t[1])
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    projs = [{"name": n, "alias": a, "url": by[n]["url"], "desc": by[n]["description"] or "Work in progress.",
              "lang": (by[n]["primaryLanguage"] or {}).get("name", "Code"), "stars": by[n]["stargazerCount"],
              "pushed": datetime.fromisoformat(by[n]["pushedAt"].replace("Z", "+00:00"))} for n, a in FEATURED if n in by]
    # streak: walk back from today (today may still be empty)
    counts = {d["date"]: d["contributionCount"] for d in days}
    day, streak = date.today(), 0
    if not counts.get(day.isoformat()):
        day -= timedelta(days=1)
    while counts.get(day.isoformat()):
        streak, day = streak + 1, day - timedelta(days=1)
    active = sum(1 for c in counts.values() if c)
    stats = [("repositories", u["repositories"]["totalCount"]), ("contributions", cal["totalContributions"]),
             ("active days", active), ("languages", len(sizes))]

    files = {"hero": hero(u, stats), "focus": focus(), "tools": tools(langs), "constellation": constellation(projs),
             "launch": launch(projs), "momentum": momentum(stats), "trail": trail(days, cal["totalContributions"]),
             "channel": channel()}
    os.makedirs("assets", exist_ok=True)
    for k, v in files.items():
        open(f"assets/{k}.svg", "w", encoding="utf-8").write(v)

    div = '<p align="center">✦ ─────────────── ✦</p>'
    img = lambda k, alt: f'<img src="assets/{k}.svg" width="100%" alt="{alt}" />'
    links = " · ".join(f'<a href="{u_}">{k}</a>' for k, u_, _ in LINKS[:3])
    focus_md = " · ".join(f"`{f[0]}`" for f in FOCUS)
    proj_cells = "".join(
        f'<td valign="top" width="25%"><a href="{p["url"]}"><b>{escape(p["alias"])}</b></a><br/><br/>{escape(p["desc"][:110])}'
        f'<br/><br/><sub>{escape(p["lang"])} · updated {p["pushed"]:%b %Y}</sub></td>' for p in projs)
    sig = "<br/>".join(f"<b>{v:,}</b> {k}" for k, v in stats)
    readme = f"""<div align="center">

<p><sub>LIVING PROFILE · {LOGIN.upper()} · LIVE</sub></p>

{img("hero", f"{NAME} animated identity card with ASCII portrait")}

<p><strong>{escape(ROLE)}</strong></p>
<p>{escape(QUOTE)}</p>
<p>{links}</p>
</div>

{div}

## Identity, with signal

<table><tr>
<td valign="top" width="70%">{escape(QUOTE)}<br/><br/><b>Focus:</b> {focus_md}<br/><br/><sub>Cloud-native backends, serverless architectures, and distributed systems that hold up under load.</sub></td>
<td valign="top"><code>LIVE SIGNAL</code><br/><br/>{sig}</td>
</tr></table>

{div}

## What moves the work

{img("focus", "Current focus areas")}

<p align="center"><sub>Positioning is useful when the proof is close behind it.</sub></p>

{div}

## The tools behind the signal

{img("tools", "Language breakdown of public code")}

<p align="center"><sub>{" · ".join(n for n, _ in langs[:8])} · AWS · Azure · Spring Boot · React · Node.js — chosen for the work, not the trend</sub></p>

{div}

## Built, shipped, shared

{img("constellation", "Featured projects constellation")}

{img("launch", "Featured projects timeline")}

<table><tr>{proj_cells}</tr></table>

{div}

## Momentum, made visible

{img("momentum", "Profile stats")}

{div}

## The trail behind the work

{img("trail", "Contribution activity for the past year")}

<p align="center"><sub>{streak} day current streak · {active} active days</sub></p>

{div}

<div align="center">

<sub>KEEP THE SIGNAL MOVING</sub>

## Make something worth noticing

I like working with people who care about scale, clean architecture, and shipping the useful version.

{img("channel", "Contact links")}

<p>{" · ".join(f'<a href="{u_}">{k}</a>' for k, u_, _ in LINKS)}</p>

<sub>{escape(NAME)} · refreshed daily from live GitHub data</sub>

</div>
"""
    open("README.md", "w", encoding="utf-8").write(readme)
    print("built", ", ".join(files), "| streak", streak, "| active", active)


if __name__ == "__main__":
    main()
