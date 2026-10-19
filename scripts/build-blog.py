"""Render approved published blog content into static pages.
Posts have slug, title, category, date (ISO), excerpt, and blocks.
Blocks: {type: paragraph|heading|list, text: str} or {type: list, items: [str]}.
Only status=published is rendered. Content is escaped; no raw HTML allowed.
"""
from pathlib import Path
from html import escape as e
from datetime import date
import json,re,shutil
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
posts=json.loads((ROOT/'content/posts.json').read_text())
published=[p for p in posts if p.get('status')=='published']
slugs=set()
for p in posts:
 assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',p['slug']), 'Invalid slug'
 assert p['slug'] not in slugs,'Duplicate slug'
 slugs.add(p['slug']);date.fromisoformat(p['date'])
 assert all(k in p for k in ['title','category','excerpt','blocks'])
published.sort(key=lambda p:p['date'],reverse=True)
blog=DIST/'blog'
if blog.exists():shutil.rmtree(blog)
blog.mkdir()

def shell(title,description,body,prefix):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{e(description,quote=True)}"><meta name="theme-color" content="#6CB4EE"><title>{e(title)} | JP Galinato</title><link rel="icon" href="{prefix}assets/jp.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/style.css"><link rel="stylesheet" href="{prefix}assets/jp.css"></head><body id="top"><a class="skip" href="#main">Skip to content</a><header><div class="nav-wrap"><a class="brand" href="{prefix}index.html">JP GALINATO<span class="brand-dot"></span></a><button id="menu-button" aria-expanded="false" aria-controls="navigation">Menu ☰</button><nav id="navigation" aria-label="Main navigation"><a href="{prefix}index.html#expertise">Expertise</a><a href="{prefix}index.html#approach">Approach</a><a href="{prefix}index.html#experience">Experience</a><a href="{prefix}blog/index.html" aria-current="page">Blog</a><a class="nav-contact" href="{prefix}index.html#contact">Let's talk ↗</a></nav></div></header><main id="main" class="wrap">{body}</main><footer class="wrap"><span>© 2026 Juan Paulo Galinato</span><span>Marketing Leader & GTM Engineer</span><a href="#top">Back to top ↑</a></footer><script src="{prefix}assets/jp.js"></script></body></html>'''

def card(p,prefix):
 return f'''<article class="blog-card"><p class="eyebrow">{e(p['category'])}</p><h3><a href="{prefix}{p['slug']}/index.html">{e(p['title'])}</a></h3><p>{e(p['excerpt'])}</p><div class="blog-card-bottom"><time datetime="{e(p['date'])}">{date.fromisoformat(p['date']).strftime('%d %B %Y')}</time><a class="text-link" href="{prefix}{p['slug']}/index.html">Read article ↗</a></div></article>'''

empty='''<div class="blog-empty"><span class="blog-symbol" aria-hidden="true">jp.</span><div><h3>The next conversation starts here.</h3><p>No articles published yet. This space will feature perspectives on GTM Engineering, demand generation, people-led solutions, and technology.</p></div></div>'''
body='''<section class="blog-heading"><p class="eyebrow">THE BLOG / JP GALINATO</p><h1>People. Systems.<br><em>Perspectives on growth.</em></h1><p>Ideas and practical thinking at the intersection of marketing, people-led solutions, and technology.</p><div class="blog-topics"><span>GTM Engineering</span><span>Demand Generation</span><span>People-led Solutions</span><span>Technology & AI</span></div></section>'''
body+=('<div class="blog-cards">'+''.join(card(p,'') for p in published)+'</div>') if published else empty
body+='''<section class="blog-outro"><h2>Let's keep the conversation going.</h2><a class="text-link" href="../index.html#contact">Connect with me ↗</a></section>'''
(blog/'index.html').write_text(shell('Blog','Perspectives on GTM Engineering, demand generation, people-led solutions and technology by JP Galinato.',body,'../'))
for p in published:
 blocks=[]
 for b in p['blocks']:
  if b['type']=='heading':blocks.append('<h2>'+e(b['text'])+'</h2>')
  elif b['type']=='paragraph':blocks.append('<p>'+e(b['text'])+'</p>')
  elif b['type']=='list':blocks.append('<ul>'+''.join('<li>'+e(i)+'</li>' for i in b['items'])+'</ul>')
  else:raise ValueError('Unsupported content block')
 count=len(' '.join(b.get('text','')+' '.join(b.get('items',[])) for b in p['blocks']).split())
 article=f'''<article class="article-page"><a class="text-link" href="../index.html">← All articles</a><div class="article-heading"><p class="eyebrow">{e(p['category'])}</p><h1>{e(p['title'])}</h1><p class="article-deck">{e(p['excerpt'])}</p><div class="article-meta">By Juan Paulo Galinato · <time datetime="{e(p['date'])}">{date.fromisoformat(p['date']).strftime('%d %B %Y')}</time> · {max(1,round(count/200))} min read</div></div><div class="article-content">{''.join(blocks)}</div><div class="article-end"><a class="text-link" href="../index.html">← Back to the blog</a><a class="text-link" href="../../index.html#contact">Let's connect ↗</a></div></article>'''
 folder=blog/p['slug'];folder.mkdir();(folder/'index.html').write_text(shell(p['title'],p['excerpt'],article,'../../'))
start='<!-- BLOG PREVIEW START -->';end='<!-- BLOG PREVIEW END -->'
home=DIST/'index.html';html=home.read_text()
preview=f'''{start}<section id="blog" class="section"><div class="section-heading"><p class="eyebrow">05 / THE BLOG</p><h2>A little perspective.<br><em>A more useful conversation.</em></h2><p>Thoughts on GTM Engineering, demand generation, people-led solutions, and technology.</p></div>{('<div class="blog-cards">'+''.join(card(p,'blog/') for p in published[:3])+'</div>') if published else empty}<div class="blog-view-all"><a class="button" href="blog/index.html">Explore the blog ↗</a></div></section>{end}'''
assert start in html and end in html
html=html[:html.index(start)]+preview+html[html.index(end)+len(end):]
home.write_text(html)
print(f'Blog built: {len(published)} published articles.')
