#!/usr/bin/env python3
"""Render reviewed policy translations as static HTML; no runtime dependencies."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("ko", "en", "de", "es", "fr", "it", "pt")
KINDS = ("terms", "privacy")
TERMS_IDS = ("provider", "service", "access", "premium", "refunds", "media", "conduct", "availability", "changes", "privacy")
PRIVACY_IDS = ("provider", "media", "faces", "permissions", "settings", "providers", "choices", "retention", "rights", "security", "updates")
LINKS = {
    "play": "https://play.google.com/store/apps/details?id=com.vora.camera",
    "refunds": "https://support.google.com/googleplay/answer/2479637",
    "google": "https://policies.google.com/privacy",
    "ads": "https://policies.google.com/technologies/ads",
    "mlkit": "https://developers.google.com/ml-kit/terms",
    "github": "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement",
}


def load():
    data = {}
    for lang in LANGUAGES:
        value = json.loads((ROOT / "content" / f"{lang}.json").read_text(encoding="utf-8"))
        for kind, ids in (("terms", TERMS_IDS), ("privacy", PRIVACY_IDS)):
            assert tuple(section["id"] for section in value[kind]) == ids, (lang, kind, "section parity")
            assert len(value[kind]) == len(ids)
            assert value["titles"][kind] and value["intro"][kind]
            for section in value[kind]:
                assert section["title"] and len(section["paragraphs"]) == 1, (lang, kind, section["id"])
                assert section["paragraphs"][0].strip()
        assert set(value["resources"]) == set(LINKS)
        data[lang] = value
    return data


def sections(data, lang, kind, bilingual):
    value = data[lang]
    prefix = f"{lang}-{kind}-"
    level = "h3" if bilingual else "h2"
    parts = [f'<p>{escape(value["intro"][kind])}</p>', '<ol>']
    for section in value[kind]:
        parts.append(f'<li><a href="#{prefix}{section["id"]}">{escape(section["title"])}</a></li>')
    parts.append('</ol>')
    for index, section in enumerate(value[kind], 1):
        parts.append(f'<{level} id="{prefix}{section["id"]}">{index}. {escape(section["title"])}</{level}>')
        parts.extend(f'<p>{escape(p)}</p>' for p in section["paragraphs"])
    return "\n".join(parts)


def render(data, kind, lang, bilingual=False):
    value = data[lang]
    prefix = "" if bilingual else "../"
    title = escape(value["titles"][kind])
    nav = [f'<a href="{prefix}index.html">{escape(value["home"])}</a>']
    for other in KINDS:
        current = ' aria-current="page"' if other == kind else ''
        nav.append(f'<a href="{other}.html"{current}>{escape(value["titles"][other])}</a>')
    languages = "\n".join(
        f'<a href="{prefix}{code}/{kind}.html" lang="{code}" hreflang="{code}">{escape(data[code]["languageName"])}</a>'
        for code in LANGUAGES
    )
    if bilingual:
        content = f'<section lang="ko" aria-labelledby="korean"><h2 id="korean">한국어</h2>{sections(data,"ko",kind,True)}</section>'
        content += f'<section class="language" lang="en" aria-labelledby="english"><h2 id="english">{escape(data["en"]["titles"][kind])}</h2><p class="updated">{escape(data["en"]["dateLabel"])}</p>{sections(data,"en",kind,True)}</section>'
    else:
        content = sections(data, lang, kind, False)
    resources = "\n".join(f'<li><a href="{escape(url, quote=True)}">{escape(value["resources"][key])}</a></li>' for key, url in LINKS.items())
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{title}">
  <link rel="stylesheet" href="{prefix}styles.css">
</head>
<body>
  <header><nav aria-label="{escape(value['home'])}">{' '.join(nav)}</nav></header>
  <main>
    <h1>{title}</h1>
    <p class="updated"><time datetime="2026-11-13">{escape(value['dateLabel'])}</time></p>
    <nav class="language-picker" aria-label="{escape(value['languageLabel'])}">{languages}</nav>
    {content}
  </main>
  <footer>
    <p>{escape(value['contactLabel'])}: <a href="mailto:mgfrind@gmail.com">mgfrind@gmail.com</a></p>
    <h2>{escape(value['resourcesLabel'])}</h2><ul>{resources}</ul>
  </footer>
</body>
</html>
'''


def main():
    data = load()
    for lang in LANGUAGES:
        folder = ROOT / lang
        folder.mkdir(exist_ok=True)
        for kind in KINDS:
            (folder / f"{kind}.html").write_text(render(data, kind, lang), encoding="utf-8")
    for kind in KINDS:
        (ROOT / f"{kind}.html").write_text(render(data, kind, "ko", bilingual=True), encoding="utf-8")
    print("Rendered 14 localized policies and 2 bilingual legacy URLs")
    from render_ios_privacy import render_all
    render_all()


if __name__ == "__main__":
    main()
