# jjayck.github.io

App Store の「デベロッパ Web サイト」から開かれるアプリ一覧ページ。`app-ads.txt` は広告の持ち主確認に使うので触らない。

1. アプリを足すときは `apps.json` に1件追加する(`slug` は app-support のフォルダ名、`id` は Apple ID)。
2. `python3 build.py` を実行すると、足りないアイコンを `icons/` に取ってきて `index.html` を作り直す。
3. `index.html`・`apps.json`・`icons/` をコミットして push する。
