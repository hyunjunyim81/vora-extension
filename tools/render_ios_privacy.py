#!/usr/bin/env python3
"""Render iOS privacy text independently of the existing Android policy URLs."""
from pathlib import Path
from html import escape
import json
ROOT=Path(__file__).resolve().parents[1]
LINKS=[('Apple privacy','https://www.apple.com/legal/privacy/'),('Apple purchases and billing','https://support.apple.com/billing'),('Google privacy','https://policies.google.com/privacy'),('Google ads privacy','https://policies.google.com/technologies/ads'),('Google Mobile Ads data disclosure','https://developers.google.com/admob/ios/privacy/data-disclosure'),('GitHub privacy','https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement')]
def render_all():
 data={lang:json.loads((ROOT/'content'/f'ios-{lang}.json').read_text()) for lang in ('ko','en')}
 assert [s['id'] for s in data['ko']['sections']]==[s['id'] for s in data['en']['sections']]
 assert len(data['ko']['sections'])==12
 def section(lang,bilingual):
  value=data[lang];level='h3' if bilingual else 'h2'
  contents='\n'.join(f'<{level} id="{lang}-{s["id"]}">{i}. {escape(s["title"])}</{level}><p>{escape(s["text"])}</p>' for i,s in enumerate(value['sections'],1))
  return f'<section lang="{lang}"><h2>{escape(value["title"])}</h2>{contents}</section>' if bilingual else contents
 for lang,bilingual,name in [('ko',True,'privacy-ios.html'),('ko',False,'ko/privacy-ios.html'),('en',False,'en/privacy-ios.html')]:
  prefix='../' if '/' in name else '';value=data[lang]
  nav=f'<a href="{prefix}index.html">VORA</a> · <a lang="ko" href="{prefix}ko/privacy-ios.html">한국어</a> · <a lang="en" href="{prefix}en/privacy-ios.html">English</a>'
  content=section('ko',True)+section('en',True) if bilingual else section(lang,False)
  html=f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(value['title'])}</title><link rel="stylesheet" href="{prefix}styles.css"><style>h1,h2,h3,p{{word-break:keep-all}}</style></head><body><header><nav>{nav}</nav></header><main><h1>{escape(value['title'])}</h1><p><time datetime="2026-11-25">2026-11-25</time></p>{content}<h2>관련 정책 / Resources</h2><ul>{''.join(f'<li><a href="{escape(url)}">{escape(label)}</a></li>' for label,url in LINKS)}</ul><p><a href="mailto:mgfrind@gmail.com">mgfrind@gmail.com</a></p></main></body></html>'''
  (ROOT/name).write_text(html+'\n')
 print('Rendered 3 iOS privacy pages, 2 languages, 12 matching sections')
if __name__=='__main__':render_all()
