#!/usr/bin/env python3
"""Generate the static ITCS 3162 portfolio pages from data/projects.json."""
from __future__ import annotations
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = json.loads((ROOT / 'data/projects.json').read_text(encoding='utf-8'))


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def header(prefix: str, active: str = '') -> str:
    home = f'{prefix}index.html'
    projects_href = f'{prefix}index.html#projects'
    about_href = f'{prefix}index.html#about'
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="wordmark" href="{home}" aria-label="Matthew Ho, portfolio home"><span class="wordmark-mark" aria-hidden="true">MH</span><span>Matthew Ho <span aria-hidden="true">/</span> Data Notes</span></a>
    <button class="nav-toggle" type="button" data-nav-toggle aria-controls="primary-navigation" aria-expanded="false" aria-label="Open navigation">Menu</button>
    <nav class="site-nav" id="primary-navigation" data-site-nav aria-label="Main navigation">
      <a href="{projects_href}" {'aria-current="page"' if active == 'projects' else ''}>Projects</a>
      <a href="{about_href}" {'aria-current="page"' if active == 'about' else ''}>About</a>
    </nav>
  </div>
</header>'''


def footer(prefix: str) -> str:
    return f'''<footer class="site-footer"><div class="container footer-inner">
<p>Matthew Ho · UNC Charlotte · ITCS 3162</p>
<p>Coursework portfolio · <a href="{prefix}index.html#projects">Back to projects ↑</a></p>
</div></footer>'''


def document(title: str, description: str, content: str, prefix: str = '') -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(description)}">
  <meta name="theme-color" content="#f5f2e9">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="{prefix}assets/site.css">
  <script defer src="{prefix}assets/site.js"></script>
</head>
<body>
{content}
{lightbox_markup()}
</body>
</html>
'''


def expandable_image(src: str, alt: str, caption: str, prefix: str = '', eager: bool = False) -> str:
    image_src = f'{prefix}{esc(src)}'
    load_hint = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'''<button class="image-expand" type="button" data-expand-image data-image="{image_src}" data-alt="{esc(alt)}" data-caption="{esc(caption)}" aria-label="Expand image: {esc(alt)}" aria-haspopup="dialog">
<img {load_hint} src="{image_src}" alt="">
<span class="image-expand-hint" aria-hidden="true">Expand ↗</span>
</button>'''


def lightbox_markup() -> str:
    return '''<dialog class="image-viewer" data-image-viewer aria-label="Expanded project image">
  <button class="image-viewer-close" type="button" data-viewer-close aria-label="Close expanded image">Close <span aria-hidden="true">×</span></button>
  <figure class="image-viewer-figure"><img data-viewer-image alt=""><figcaption data-viewer-caption></figcaption></figure>
</dialog>'''


def home_page() -> str:
    first = PROJECTS[0]
    cards = []
    for p in PROJECTS:
        href = f'projects/{p["slug"]}/index.html'
        image = p['charts'][0]
        cards.append(f'''<article class="project-row">
  <div class="project-copy">
    <span class="project-number">PROJECT {esc(p['number'])} · {esc(p['category'])}</span>
    <h3 class="project-title"><a href="{href}">{esc(p['title'])}</a></h3>
    <p class="project-summary">{esc(p['deck'])}</p>
    <div class="project-meta"><span>{esc(p['year'])}</span><span>{esc(p['dataset'].split(' · ')[0])}</span></div>
    <a class="text-link" href="{href}">Read the case study <span aria-hidden="true">→</span></a>
  </div>
  <figure class="project-image">
    {expandable_image(image['src'], image['alt'], image['caption'])}
    <figcaption>{esc(image['caption'])}</figcaption>
  </figure>
</article>''')
    content = f'''{header('', 'projects')}
<main id="main">
  <section class="home-hero">
    <div class="container hero-grid">
      <div class="hero-copy">
        <p class="eyebrow">UNC CHARLOTTE · ITCS 3162 · 2024</p>
        <h1>Finding the story behind the numbers.</h1>
        <p class="lede">Four course projects exploring digital access, loan classification, food prices, and customer behavior—with a focus on what each dataset can and cannot tell us.</p>
        <div class="hero-actions"><a class="button-link" href="#projects">Explore the projects <span aria-hidden="true">↓</span></a><a class="text-link" href="#about">About this portfolio</a></div>
      </div>
      <figure class="hero-art">
        {expandable_image(first['charts'][0]['src'], first['charts'][0]['alt'], first['charts'][0]['caption'], eager=True)}
        <figcaption class="figure-caption"><strong>01 / Hong Kong internet adoption</strong><span>1980—2020</span></figcaption>
      </figure>
    </div>
  </section>
  <div class="intro-strip"><div class="container intro-strip-inner"><p class="course-tag">A small collection of data studies</p><p>Questions first. Methods made visible. Results kept in context.</p></div></div>
  <section class="section container" id="projects" aria-labelledby="projects-title">
    <div class="section-head"><div><p class="eyebrow">THE WORK</p><h2 id="projects-title">Four questions, four approaches.</h2></div><p>Browse each study for its question, data preparation, method, findings, and the limits I would address next.</p></div>
    <div class="project-list">{''.join(cards)}</div>
  </section>
  <section class="about-band" id="about" aria-labelledby="about-title"><div class="container about-grid">
    <div><p class="eyebrow">ABOUT THIS COLLECTION</p><h2 id="about-title">An honest record of the work.</h2></div>
    <p>This portfolio documents four projects completed for UNC Charlotte’s ITCS 3162 course. The case studies clarify the original notebooks, preserve their visual results, and call out small samples, modeling assumptions, and data gaps. The notebooks are included with saved outputs removed; the underlying CSV datasets are not redistributed here.</p>
  </div></section>
</main>
{footer('')}'''
    return document('Matthew Ho — ITCS 3162 Data Projects', 'Four data projects by Matthew Ho for UNC Charlotte ITCS 3162.', content)


def project_card_figure(chart: dict, prefix: str, hero: bool = False) -> str:
    cls = 'case-hero-figure' if hero else 'chart-figure'
    return f'''<figure class="{cls}">{expandable_image(chart['src'], chart['alt'], chart['caption'], prefix, eager=hero)}<figcaption>{esc(chart['caption'])}</figcaption></figure>'''


def project_page(p: dict, idx: int) -> str:
    prefix = '../../'
    hero_chart = p['charts'][0]
    chart_gallery = ''.join(project_card_figure(c, prefix) for c in p['charts'][1:])
    steps = ''.join(f'''<li><span class="step">0{n}</span><div><h3>{esc(step['title'])}</h3><p>{esc(step['text'])}</p></div></li>''' for n, step in enumerate(p['steps'], 1))
    prev_p = PROJECTS[idx - 1] if idx > 0 else None
    next_p = PROJECTS[idx + 1] if idx + 1 < len(PROJECTS) else None
    switch = ''
    if prev_p:
        switch += f'<a href="../../projects/{prev_p["slug"]}/index.html"><span>Previous project</span>← {esc(prev_p["title"])}</a>'
    if next_p:
        switch += f'<a href="../../projects/{next_p["slug"]}/index.html"><span>Next project</span>{esc(next_p["title"])} →</a>'
    facts = [('Data', p['dataset']), ('Period', p['year']), ('Tools', ', '.join(p['tools']))]
    facts_html = ''.join(f'<div class="case-fact"><span class="label">{esc(k)}</span><strong>{esc(v)}</strong></div>' for k,v in facts)
    content = f'''{header(prefix, 'projects')}
<main id="main">
  <section class="case-hero"><div class="container case-hero-grid">
    <div><p class="eyebrow">PROJECT {esc(p['number'])} · {esc(p['category'])}</p><h1>{esc(p['title'])}</h1><p class="lede">{esc(p['deck'])}</p>
      <div class="case-actions"><a class="button-link" href="{prefix}notebooks/{esc(p['notebook'])}" download="{esc(p['notebook'])}">Download notebook <span aria-hidden="true">↓</span></a><a class="text-link" href="{prefix}index.html#projects">All projects</a></div>
    </div>
    {project_card_figure(hero_chart, prefix, True)}
  </div></section>
  <div class="container"><div class="case-facts" aria-label="Project details">{facts_html}</div></div>
  <div class="container case-layout">
    <nav class="case-rail" aria-label="On this page"><p>On this page</p><a href="#question">Question</a><a href="#approach">Approach</a><a href="#findings">Findings & limits</a><a href="#visuals">Visuals</a><a href="#notebook">Notebook</a></nav>
    <div class="case-main">
      <section id="question"><p class="eyebrow">THE QUESTION</p><h2>What I wanted to understand</h2><p class="answer">{esc(p['question'])}</p></section>
      <section id="approach"><p class="eyebrow">THE WORKFLOW</p><h2>From raw data to a testable view</h2><p>{esc(p['method'])}</p><ol class="workflow-list">{steps}</ol></section>
      <section id="findings"><p class="eyebrow">WHAT THE RUN SHOWED</p><h2>Findings, with caveats.</h2><div class="result-panel"><div><h3>Observed finding</h3><p>{esc(p['finding'])}</p></div><div><h3>What to keep in mind</h3><p>{esc(p['limitation'])}</p></div></div>
        <p class="data-note" style="margin-top:18px"><strong>Next iteration:</strong> {esc(p['reflection'])}</p>
      </section>
      <section id="visuals"><p class="eyebrow">SELECTED FIGURES</p><h2>What the analysis looked like</h2><div class="chart-grid">{chart_gallery}</div></section>
      <section id="notebook"><p class="eyebrow">REPRODUCIBILITY</p><h2>Notebook and source data</h2><p>The downloadable notebook preserves the analysis code with saved outputs removed and data paths normalized to a local <code>data/</code> folder. Dataset files are not bundled; consult <code>notebooks/README.md</code> for the filenames referenced by the notebook and supply appropriately licensed source data before running it.</p><a class="text-link" href="{prefix}notebooks/{esc(p['notebook'])}" download>Download notebook <span aria-hidden="true">↓</span></a></section>
      <nav class="project-switcher" aria-label="Other case studies">{switch}</nav>
    </div>
  </div>
</main>
{footer(prefix)}'''
    return document(f"{p['title']} — Matthew Ho", p['deck'], content, prefix)


def main() -> None:
    (ROOT / 'index.html').write_text(home_page(), encoding='utf-8')
    for idx, p in enumerate(PROJECTS):
        dest = ROOT / 'projects' / p['slug'] / 'index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(project_page(p, idx), encoding='utf-8')
    (ROOT / '404.html').write_text(document('Page not found — Matthew Ho', 'This project page could not be found.', f'''{header('', '')}<main id="main" class="container section"><p class="eyebrow">404 · NOT FOUND</p><h1>This page is off the chart.</h1><p class="lede">The page may have moved. Return to the project index to keep browsing.</p><a class="button-link" href="index.html">Back to the portfolio</a></main>{footer('')}'''), encoding='utf-8')
    print('Generated home page and', len(PROJECTS), 'project case studies.')

if __name__ == '__main__':
    main()
