#!/usr/bin/env python3
"""Check the site after editing it by hand.

Everything here is something that has actually gone wrong at least once, or
that would break a page silently rather than visibly.  Run it before
committing; it prints what is wrong and exits non-zero, or says OK.
"""
import json, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
PAGES = sorted(HERE.glob("*.html"))
PAIRED = ("section", "div", "p", "span", "a", "li", "ol", "ul", "nav",
          "button", "table", "thead", "tbody", "tr", "td", "th", "figure",
          "sup", "b", "footer", "header", "h1", "h2", "h3", "time")
# The strings that must never reach a published page are themselves the ones
# worth hiding, so they live in a gitignored file rather than in this one.
# One per line; blank lines and #-comments ignored.  No file, no check.
def _leaks():
    f = HERE / ".identity-strings"
    if not f.exists():
        return []
    return [ln.strip() for ln in f.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")]

def check(p):
    s = p.read_text(encoding="utf-8")
    body = s.split("<script")[0]
    bad = []

    for t in PAIRED:
        o = len(re.findall(rf"<{t}[ >]", s))
        c = len(re.findall(rf"</{t}>", s))
        if o != c:
            bad.append(f"<{t}> が {o} 個、</{t}> が {c} 個")

    for i in set(re.findall(r'getElementById\("([a-z0-9_-]+)"\)', s)):
        if f'id="{i}"' not in body:
            bad.append(f'JS が id="{i}" を触るが本文にない（以降の描画が止まる）')

    for h in set(re.findall(r'href="([^":#]+\.html)"', s)):
        if not (HERE / h).exists():
            bad.append(f"リンク切れ {h}")

    for t in set(re.findall(r'src="(assets/tiles/[^"]+)"', s)):
        if "${" in t:            # built by JS; the ranks it can produce are fixed
            continue
        if not (HERE / t).exists():
            bad.append(f"牌画像がない {t}")
    for r in set(re.findall(r'src="assets/tiles/Sou\$\{t\}\.svg"', s)):
        missing = [n for n in range(1, 10)
                   if not (HERE / f"assets/tiles/Sou{n}.svg").exists()]
        if missing:
            bad.append(f"JS が組み立てる牌が欠けている: {missing}")

    m = re.search(r"^const D = (\{.*?\});$", s, re.S | re.M)
    if "const D" in s:
        if not m:
            bad.append("const D の行が壊れている（1行で `const D = {...};` の形が必要）")
        else:
            try:
                D = json.loads(m.group(1))
                for k in set(re.findall(r"\bD\.(\w+)", s)):
                    if k not in D:
                        bad.append(f"D.{k} を参照しているがデータにない")
            except json.JSONDecodeError as e:
                bad.append(f"const D が JSON として読めない: {e}")

    if p.name != "index.html":
        if not re.search(r"<time datetime=\"\d{4}-\d{2}-\d{2}\"", s):
            bad.append("日付 <time datetime=...> がない")
        if 'class="tag' not in s:
            bad.append("タグがない")
        if 'id="comments"' not in s:
            bad.append("コメント欄がない")

    for w in _leaks():
        if w.lower() in s.lower():
            bad.append("身元情報らしき文字列を検出（.identity-strings の項目）")
    return bad

def main():
    fail = 0
    for p in PAGES:
        bad = check(p)
        print(f"  {p.name:<26}{'OK' if not bad else '要修正'}")
        for b in bad:
            print(f"      - {b}")
        fail += len(bad)

    idx = (HERE / "index.html").read_text(encoding="utf-8")
    listed = set(re.findall(r'href: "([^"]+)"', idx))
    actual = {p.name for p in PAGES} - {"index.html"}
    for h in listed - actual:
        print(f"  index が存在しない記事を挙げている: {h}"); fail += 1
    for h in actual - listed:
        print(f"  index に載っていない記事: {h}"); fail += 1

    print("\n  " + ("すべて OK" if not fail else f"{fail} 件の要修正"))
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main())
