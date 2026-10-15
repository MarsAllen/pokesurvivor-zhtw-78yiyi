"""產生繁中像素字型子集 assets/fonts/YiyiPixelTC.woff2。
    python tools/make_font_zh.py

- 來源：俐方體11號 Cubic 11（OFL 1.1，https://github.com/ACh-K/Cubic-11），
  只下載一次，快取在 tools/cache/fonts/（不進 repo）。
- 只保留繁中字典（lang-zh*.js、lang-fork.js）與少數程式碼裡實際用到的中日韓字元與全形標點。
- 「Cubic」「俐方體」是 OFL 的保留名稱：子集屬於修改版本，因此字型改名為 YiyiPixel TC，
  並保留原本的版權聲明；授權全文在 assets/fonts/OFL-Cubic11.txt。
- 改了翻譯之後要重新執行，否則新出現的字會用系統字型顯示。
"""
import hashlib
import os
import re
import urllib.request

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CACHE = os.path.join(ROOT, 'tools', 'cache', 'fonts')
SRC_URL = 'https://raw.githubusercontent.com/ACh-K/Cubic-11/4c566f7d6cc5c05ee360fe9cff56b5da1fcafd4d/fonts/ttf/Cubic_11.ttf'
SRC = os.path.join(CACHE, 'Cubic_11.ttf')
OUT = os.path.join(ROOT, 'assets', 'fonts', 'YiyiPixelTC.woff2')
FAMILY = 'YiyiPixel TC'

TEXT_FILES = [
    'js/data/lang-zh.js', 'js/data/lang-zh-names.js', 'js/data/lang-fork.js',
    'js/ui/ranking-ui.js', 'js/ui/settings-ui.js', 'dev.html',
]
# 與 css/style.css 的 unicode-range 一致：中日韓部首、標點、注音、漢字、相容字、直排與全形符號。
CJK = re.compile('[⺀-⿿　-〿㄀-ㄯ㐀-䶿一-鿿豈-﫿︰-﹏＀-￯]')


def main():
    os.makedirs(CACHE, exist_ok=True)
    if not os.path.exists(SRC):
        print('下載 Cubic_11.ttf')
        urllib.request.urlretrieve(SRC_URL, SRC)

    chars = set()
    for f in TEXT_FILES:
        with open(os.path.join(ROOT, f), encoding='utf-8') as fh:
            chars.update(CJK.findall(fh.read()))

    # 不更新 head 的時間戳記：同樣的字產生同樣的檔案（雜湊才不會每次都變）。
    font = TTFont(SRC, recalcTimestamp=False)
    cmap = font.getBestCmap()
    missing = sorted(c for c in chars if ord(c) not in cmap)
    keep = sorted(c for c in chars if ord(c) in cmap)

    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.hinting = False
    opts.layout_features = []
    opts.name_IDs = ['*']
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=[ord(c) for c in keep])
    sub.subset(font)

    # OFL 保留名稱：修改版不能叫 Cubic／俐方體。版權（nameID 0）保留。
    name = font['name']
    for rec in list(name.names):
        if rec.nameID in (1, 4, 16):
            rec.string = FAMILY
        elif rec.nameID == 6:
            rec.string = FAMILY.replace(' ', '')
        elif rec.nameID == 3:
            rec.string = FAMILY + ' (subset of Cubic 11)'
        elif rec.nameID == 17:
            rec.string = 'Regular'
    font.flavor = 'woff2'
    font.save(OUT)

    # sw.js 對 assets/fonts/ 是 cache-first：網址帶上內容雜湊，字型更新後玩家才會重新下載。
    with open(OUT, 'rb') as fh:
        digest = hashlib.sha1(fh.read()).hexdigest()[:8]
    css_path = os.path.join(ROOT, 'css', 'style.css')
    # newline='' 保留檔案原本的換行字元（上游的檔案是 CRLF）。
    with open(css_path, encoding='utf-8', newline='') as fh:
        css = fh.read()
    css = re.sub(r'YiyiPixelTC\.woff2(\?v=[0-9a-f]+)?', f'YiyiPixelTC.woff2?v={digest}', css)
    with open(css_path, 'w', encoding='utf-8', newline='') as fh:
        fh.write(css)

    print(f'ok: {len(keep)} 字 -> {os.path.relpath(OUT, ROOT)} ({os.path.getsize(OUT) // 1024} KB, v={digest})')
    if missing:
        print('字型裡沒有的字（會用系統字型顯示）：' + ''.join(missing))


if __name__ == '__main__':
    main()
