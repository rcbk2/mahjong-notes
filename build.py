#!/usr/bin/env python3
"""Keep the published pages' data in step with the analysis.

The pages are written by hand -- the prose is the author's, and they carry
dates, tags and a comments section that no artifact knows about -- so nothing
here regenerates one.  All this does is lift the `const D = {...}` block out
of the artifact and drop it into each page, which keeps every table and chart
following the analysis without touching a word of the writing.

The one-time transformations that turned the artifacts into pages -- real
tiles, relative cross-links, the public footer -- are already applied in the
files themselves and are not repeated.
"""
import os, pathlib, re, sys

# Point MAHJONG_OUT at the analysis output directory.
SRC = pathlib.Path(os.environ.get("MAHJONG_OUT", "../analysis/out")).expanduser()
DST = pathlib.Path(__file__).parent

# Those URLs carry a whole M-League hand in the fragment.  The mirror they come
# from is published for free use with no terms attached, so they stay in.
MLEAGUE_REPLAY_LINKS = True

PAGES = {
    "v2_karagiri_slide.html":       ["faking-a-slide.ja.html", "faking-a-slide.html"],
    "v2_noten_karagiri_slide.html": ["who-fakes.ja.html"],
}

# span placeholders -> real tiles.  Souzu, matching the worked example.
def sync_data(src_name, out_name):
    """Refresh only the data block of a hand-written page."""
    src = (SRC / src_name).read_text(encoding="utf-8")
    m = re.search(r"^const D = \{.*?\};$", src, re.S | re.M)
    if m is None:
        raise SystemExit(f"{src_name}: データブロックが見つからない")
    data = m.group(0)
    # Tenhou account names.  Nothing on the page reads them, and naming the
    # players whose habits were counted is not something the site should do.
    data, n = re.subn(r',"reps":\[.*?\}\]', "", data)
    if n:
        print(f"  {'':24s} 天鳳アカウント名 (D.reps) を除去")

    if not MLEAGUE_REPLAY_LINKS:
        data = re.sub(r',"url":"https://tenhou\.net/5/#json=[^"]*"', "", data)
    page = DST / out_name
    cur = page.read_text(encoding="utf-8")
    if not re.search(r"^const D = \{.*?\};$", cur, re.S | re.M):
        raise SystemExit(f"{out_name}: 差し替え先のデータブロックがない")
    new = re.sub(r"^const D = \{.*?\};$", lambda _: data, cur, count=1,
                 flags=re.S | re.M)
    # every D.<key> the hand-written page reads must survive the refresh
    keys = set(re.findall(r"\bD\.(\w+)", new))
    missing = [k for k in keys if f'"{k}":' not in data]
    if missing:
        raise SystemExit(f"{out_name}: データに無いキーを参照 {missing}")
    page.write_text(new, encoding="utf-8")
    print(f"  {out_name:24s} データのみ更新 (参照キー {len(keys)} 個を確認)")


if __name__ == "__main__":
    print("sync:")
    for artifact, pages in PAGES.items():
        for page in pages:
            sync_data(artifact, page)
