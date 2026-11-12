# apps.json から index.html を作る。アイコンが icons/ に無いアプリは App Store から1回だけ取ってくる。
# 使い方: python3 build.py
import json, os, subprocess, urllib.request
from html import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
SUPPORT = "https://jjayck.github.io/app-support"


def fetch_icon(app):
    path = os.path.join(ROOT, "icons", app["slug"] + ".png")
    if os.path.exists(path):
        return
    with urllib.request.urlopen(f"https://itunes.apple.com/jp/lookup?id={app['id']}") as r:
        res = json.load(r)["results"]
    if not res:
        raise SystemExit(f"App Store に見つからない: {app['name']} ({app['id']})")
    url = res[0]["artworkUrl512"].rsplit("/", 1)[0] + "/192x192bb.png"
    urllib.request.urlretrieve(url, path)
    subprocess.run(["sips", "-s", "format", "png", path, "--out", path], check=False, capture_output=True)
    print("icon:", app["slug"])


def card(a):
    en = f' <span class="en" lang="en">{escape(a["en"])}</span>' if a.get("en") else ""
    note = f'<p class="note">{escape(a["note"])}</p>' if a.get("note") else ""
    links = [f'<a href="https://apps.apple.com/jp/app/id{a["id"]}">App Store</a>']
    if a.get("support", True):
        links.append(f'<a href="{SUPPORT}/{a["slug"]}/support.html">サポート</a>')
    if a.get("privacy", True):
        links.append(f'<a href="{SUPPORT}/{a["slug"]}/privacy.html">プライバシーポリシー</a>')
    return f"""<li class="app">
<img src="icons/{a['slug']}.png" width="64" height="64" alt="">
<div>
<h3>{escape(a['name'])}{en}</h3>
<p>{escape(a['desc'])}</p>{note}
<p class="links">{' '.join(links)}</p>
</div>
</li>"""


def main():
    data = json.load(open(os.path.join(ROOT, "apps.json"), encoding="utf-8"))
    os.makedirs(os.path.join(ROOT, "icons"), exist_ok=True)
    sections = []
    for g in data["groups"]:
        for a in g["apps"]:
            fetch_icon(a)
        items = "\n".join(card(a) for a in g["apps"])
        sections.append(f'<section>\n<h2>{escape(g["title"])}</h2>\n<ul class="apps">\n{items}\n</ul>\n</section>')
    count = sum(len(g["apps"]) for g in data["groups"])
    html = TEMPLATE.replace("{{COUNT}}", str(count)).replace("{{SECTIONS}}", "\n\n".join(sections)) \
        .replace("{{CONTACT}}", escape(data["contact"]))
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(html)
    print(f"index.html: {count} apps")


TEMPLATE = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>jjayck のiPhoneアプリ</title>
<meta name="description" content="個人開発者 jjayck が App Store で配信している iPhone アプリの一覧と、各アプリのサポート・プライバシーポリシー。">
<style>
:root{--bg:#fafaf8;--card:#fff;--text:#1d1d1f;--sub:#5c5c62;--line:#e3e3e0;--link:#0a5fc2}
@media (prefers-color-scheme:dark){:root{--bg:#141416;--card:#1e1e21;--text:#ececef;--sub:#a4a4ab;--line:#33333a;--link:#7ab4ff}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP",Meiryo,sans-serif;line-height:1.7;-webkit-text-size-adjust:100%}
main{max-width:760px;margin:0 auto;padding:40px 16px 24px}
header h1{font-size:1.6rem;margin:0 0 6px;line-height:1.3}
header p{margin:0;color:var(--sub)}
h2{font-size:1rem;color:var(--sub);font-weight:600;margin:36px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--line)}
ul.apps{list-style:none;margin:0;padding:0;display:grid;gap:12px}
.app{display:flex;gap:14px;align-items:flex-start;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px}
.app img{flex:none;width:64px;height:64px;border-radius:14px;border:1px solid var(--line)}
.app div{min-width:0}
.app h3{margin:0;font-size:1.05rem;line-height:1.4}
.app .en{font-size:.8rem;font-weight:400;color:var(--sub);margin-left:4px}
.app p{margin:4px 0 0;font-size:.93rem}
.app .note{color:var(--sub);font-size:.82rem}
.links{display:flex;flex-wrap:wrap;gap:4px 16px;margin-top:8px !important}
a{color:var(--link);text-underline-offset:2px}
footer{max-width:760px;margin:0 auto;padding:16px 16px 48px;color:var(--sub);font-size:.85rem;border-top:1px solid var(--line)}
footer p{margin:4px 0}
@media (max-width:480px){.app{gap:12px;padding:12px}.app img{width:52px;height:52px;border-radius:12px}}
</style>
</head>
<body>
<main>
<header>
<h1>jjayck のiPhoneアプリ</h1>
<p>App Store で配信中の {{COUNT}} 本の一覧です。各アプリのサポートとプライバシーポリシーもこちらから開けます。</p>
</header>

{{SECTIONS}}
</main>
<footer>
<p>お問い合わせ: <a href="mailto:{{CONTACT}}">{{CONTACT}}</a></p>
<p><a href="tools.html">個人用自動化ツールについて</a></p>
</footer>
</body>
</html>
"""

if __name__ == "__main__":
    main()
