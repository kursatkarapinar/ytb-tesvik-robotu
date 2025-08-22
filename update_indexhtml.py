# python
import os
import shutil
import pathlib
from bs4 import BeautifulSoup
import streamlit as st

APP_TITLE = "YTB Teşvik Robotu & KOSGEB Hesaplama"
DESCRIPTION = "Yatırım Teşvik Belgesi Teşvik Robotu , KOSGEB Hızlı Büyüyen Firma Hesaplaması."
LOGO_FILE = "ytb-logo.png"
FAVICON_FILE = "favicon.ico"

HTML_ID = "google_analytics"
GA_ID = "GTM-NCNL62G6"

GA_SCRIPT = f"""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script id="{HTML_ID}">
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>
"""

def _index_path() -> pathlib.Path:
    return pathlib.Path(st.__file__).parent / "static" / "index.html"

def _backup(index_path: pathlib.Path):
    bck = index_path.with_suffix(".bck")
    if not bck.exists():
        shutil.copy(index_path, bck)

def inject_ga():
    index_path = _index_path()
    soup = BeautifulSoup(index_path.read_text(encoding="utf-8"), "html.parser")
    head = soup.find("head")
    if not head:
        head = soup.new_tag("head")
        if soup.html:
            soup.html.insert(0, head)
        else:
            # Beklenmeyen durum: doğrudan başa ekle
            soup.insert(0, head)

    # Zaten enjekte edilmemişse ekle
    if not soup.find(id=HTML_ID):
        _backup(index_path)
        ga_nodes = BeautifulSoup(GA_SCRIPT, "html.parser")
        head.insert(0, ga_nodes)
        index_path.write_text(str(soup), encoding="utf-8")

def update_title(new_title: str):
    index_path = _index_path()
    soup = BeautifulSoup(index_path.read_text(encoding="utf-8"), "html.parser")
    head = soup.find("head")
    if not head:
        head = soup.new_tag("head")
        if soup.html:
            soup.html.insert(0, head)
        else:
            soup.insert(0, head)

    title_tag = soup.find("title")
    if title_tag:
        title_tag.string = new_title
    else:
        t = soup.new_tag("title")
        t.string = new_title
        head.append(t)

    _backup(index_path)
    index_path.write_text(str(soup), encoding="utf-8")

def update_favicon(favicon_path: str):
    # favicon.ico'yu static klasörüne kopyala ve <link rel="icon"> etiketini güncelle
    index_path = _index_path()
    static_folder = index_path.parent
    static_favicon_path = static_folder / "favicon.ico"

    if not pathlib.Path(favicon_path).exists():
        raise FileNotFoundError(f"Bulunamadı: {favicon_path}")

    shutil.copy(favicon_path, static_favicon_path)

    soup = BeautifulSoup(index_path.read_text(encoding="utf-8"), "html.parser")
    head = soup.find("head")
    if not head:
        head = soup.new_tag("head")
        if soup.html:
            soup.html.insert(0, head)
        else:
            soup.insert(0, head)

    # Mevcut icon link etiketlerini temizle
    for link in head.find_all("link"):
        rel = link.get("rel")
        if rel and any("icon" in r for r in rel):
            link.decompose()

    # Yeni favicon.ico link etiketleri ekle
    link_icon = soup.new_tag("link", rel="icon", href="favicon.ico", type="image/x-icon")
    head.append(link_icon)
    link_shortcut = soup.new_tag("link", rel="shortcut icon", href="favicon.ico", type="image/x-icon")
    head.append(link_shortcut)

    _backup(index_path)
    index_path.write_text(str(soup), encoding="utf-8")

def update_social_preview_image(og_image: str, og_description: str, og_url: str):
    index_path = _index_path()
    soup = BeautifulSoup(index_path.read_text(encoding="utf-8"), "html.parser")

    head = soup.find("head")
    if not head:
        head = soup.new_tag("head")
        if soup.html:
            soup.html.insert(0, head)
        else:
            soup.insert(0, head)

    page_title = soup.title.string if soup.title and soup.title.string else APP_TITLE

    og_tags = {
        "og:title": page_title,
        "og:description": og_description,
        "og:type": "website",
        "og:url": og_url,
        "og:image": og_image,
        "og:image:width": "1200",
        "og:image:height": "630",
    }
    for prop, content in og_tags.items():
        tag = soup.find("meta", property=prop)
        if tag:
            tag["content"] = content
        else:
            head.append(soup.new_tag("meta", property=prop, content=content))

    twitter_tags = {
        "twitter:card": "summary_large_image",
        "twitter:title": page_title,
        "twitter:description": og_description,
        "twitter:image": og_image,
    }
    for name, content in twitter_tags.items():
        tag = soup.find("meta", attrs={"name": name})
        if tag:
            tag["content"] = content
        else:
            head.append(soup.new_tag("meta", attrs={"name": name, "content": content}))

    _backup(index_path)
    index_path.write_text(str(soup), encoding="utf-8")

if __name__ == "__main__":
    base_url = os.getenv("PUBLIC_BASE_URL", "https://tesvikrobotu.net/")
    inject_ga()
    update_title(APP_TITLE)
    update_favicon(FAVICON_FILE)
    update_social_preview_image(
        og_image=LOGO_FILE,
        og_description=DESCRIPTION,
        og_url=base_url,
    )