"""Generate the 15 static pages. Runtime remains plain HTML, CSS and JavaScript.
Run from any directory: python tools/build_site.py
Edit translations in assets/i18n; generated HTML can be served without Python.
"""
from pathlib import Path
from html import escape as esc
import json, os
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://felipercode0698.com/'
ROUTES = {
    'pt-BR': ['index.html', 'sobre-mim.html', 'portfolio.html', 'servicos.html', 'contato.html'],
    'en': ['en/index.html', 'en/about.html', 'en/portfolio.html', 'en/services.html', 'en/contact.html'],
    'es': ['es/index.html', 'es/sobre-mi.html', 'es/portafolio.html', 'es/servicios.html', 'es/contacto.html'],
}
FLAG_FILES = {'pt-BR': 'br.svg', 'en': 'us.svg', 'es': 'es.svg'}
FLAGS = {'pt-BR': ('🇧🇷', 'Português'), 'en': ('🇺🇸', 'English'), 'es': ('🇪🇸', 'Español')}
WA = 'https://wa.me/5571996345224?text=Ol%C3%A1%20Felipe'
EMAIL = 'https://mail.google.com/mail/?view=cm&fs=1&to=felipercode0698@gmail.com'
SOCIAL = [('TikTok','https://www.tiktok.com/@felipercode0698'), ('Kwai','https://www.kwai.com/@felipercode0698'), ('YouTube','https://www.youtube.com/@felipercode0698'), ('X','https://x.com/@felipercode0698'), ('Instagram','https://www.instagram.com/felipercode0698/'), ('Facebook','https://www.facebook.com/felipercode0698'), ('GitHub','https://github.com/Feliperocha0698'), ('LinkedIn','https://www.linkedin.com/in/feliperocha0698/')]
PROJECTS = [
 ('FORMULARIO-1.png', 'https://github.com/Feliperocha0698/projetosfreelancer1/tree/main/FORMULARIO', 'other'),
 ('LISTA-DE-TAREFAS.png', 'https://github.com/Feliperocha0698/lista-de-tarefas', 'web'),
 ('RELOGIO-DIGITAL.png', 'https://github.com/Feliperocha0698/PROJETO-RELOGIO-DIGITAL', 'other'),
]
CATEGORIES = ['business','restaurants','burgers','gyms','web','apps','other']
ICON_PATHS = [
 '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01"/>',
 '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><path d="M14 6h4v4M6 14v4h4"/>',
 '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M10 18h4"/>',
 '<path d="m14 6 4-4a6 6 0 0 1-7 8L4 17a2 2 0 0 0 3 3l7-7a6 6 0 0 0 8-7l-4 4Z"/>',
 '<path d="M4 20h16M5 16l4-5 4 2 6-8M15 5h4v4"/>',
]

def e(text): return esc(str(text), quote=True)
def url(route): return BASE + ('' if route == 'index.html' else route)
def rel(path, current): return os.path.relpath(path, Path(current).parent).replace('\\','/')
def icon(index): return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+ICON_PATHS[index]+'</svg>'
def dump(data): return json.dumps(data,ensure_ascii=False).replace('<','\\u003c')

def render(d, index):
    lang=d['lang']; current=ROUTES[lang][index]; u=d['ui']; h=d['home']; ed=d['education']
    def path(p): return rel(p,current)
    def page(i): return path(ROUTES[lang][i])
    def flag(code): return f'<img class="language-flag" src="{path("assets/icons/"+FLAG_FILES[code])}" width="20" height="14" alt="" aria-hidden="true">'
    def external(href,text,cls=''):
        return f'<a class="{cls}" href="{e(href)}" target="_blank" rel="noopener noreferrer">{e(text)}<span class="sr-only">{e(u["newTab"])}</span></a>'
    def cta():
        return f'''<section class="section container"><div class="contact-banner"><div><p class="eyebrow">{e(u['ctaEyebrow'])}</p><h2>{e(u['ctaTitle'])}</h2><p>{e(u['ctaText'])}</p></div><div class="banner-actions"><a class="button light" href="{page(4)}">{e(u['quote'])} <span aria-hidden="true">↗</span></a>{external(WA,u['whatsapp'])}</div></div></section>'''
    def education():
        return f'''<div class="qualification-strip"><div class="container qualification-inner"><p><span aria-hidden="true">↗</span><strong>{e(ed['degree'])}</strong><span>{e(ed['degreeLabel'])}</span></p><span class="strip-divider" aria-hidden="true"></span><p><span aria-hidden="true">◇</span><strong>{e(ed['post'])}</strong><span>{e(ed['postLabel'])}</span></p></div></div>'''
    def service_cards(full=False):
        cards=[]
        for n,item in enumerate(d['services']['items']):
            title,desc,benefit,detail=item
            cards.append(f'''<article class="service-card"><span class="service-icon">{icon(n)}</span><h{'2' if full else '3'}>{e(title)}</h{'2' if full else '3'}><p>{e(desc)}</p>{f'<p class="service-benefit">{e(benefit)}</p>' if full else ''}<p class="service-detail">{e(detail)}</p><a class="text-link" href="{page(4)}?service={n}">{e(u['quote'])} <span aria-hidden="true">↗</span></a></article>''')
        return '<div class="services-grid">'+''.join(cards)+'</div>'
    def project_cards(filters=False):
        cards=[]
        for n,(image,href,cat) in enumerate(PROJECTS):
            title,desc,alt=d['portfolio']['projects'][n]
            category=d['portfolio']['categories'][CATEGORIES.index(cat)]
            cards.append(f'''<article class="project-card" data-category="{cat}"><div class="project-image"><img src="{path('img/'+image)}" alt="{e(alt)}" loading="lazy" width="640" height="400"></div><div class="project-body"><p class="eyebrow">{e(u['projectType'])}</p><h{'2' if filters else '3'}>{e(title)}</h{'2' if filters else '3'}><p>{e(desc)}</p>{f'<p class="category-label">{e(category)}</p><p class="tech-list"><span class="sr-only">{e(u["technologies"])}</span><span>HTML</span><span>CSS</span><span>JavaScript</span></p>' if filters else ''}{external(href,u['code'],'text-link')}</div></article>''')
        return '<div class="projects-grid" id="project-grid">'+''.join(cards)+'</div>'
    def page_hero(section):
        return f'<section class="page-hero"><div class="container"><p class="eyebrow">{e(section["eyebrow"])}</p><h1>{e(section["title"])}</h1><p class="page-intro">{e(section["intro"])}</p></div></section>'

    if index==0:
        benefits=''.join(f'<article><span aria-hidden="true">{n+1:02} /</span><div><h3>{e(t)}</h3><p>{e(v)}</p></div></article>' for n,(t,v) in enumerate(h['benefits']))
        body=f'''<section class="hero"><div class="container hero-grid"><div class="hero-copy"><p class="eyebrow"><span class="short-line" aria-hidden="true"></span>{e(h['eyebrow'])}</p><p class="professional-name">Felipe Rocha Maia</p><p class="professional-title">{e(d['titleRole'])}</p><h1>{e(h['headingBefore'])} <span>{e(h['headingAccent'])}</span> {e(h['headingAfter'])}</h1><p class="hero-description">{e(h['intro'])}</p><div class="hero-actions"><a class="button primary" href="{page(4)}">{e(u['quote'])} <span aria-hidden="true">↗</span></a><a class="button secondary" href="{page(2)}">{e(u['portfolio'])} <span aria-hidden="true">→</span></a></div>{external(WA,u['whatsapp'],'hero-whatsapp')}<p class="remote-note"><span aria-hidden="true">◎</span> {e(u['remote'])}</p></div><div class="portrait-wrap"><div class="portrait-frame"><span class="portrait-label">{e(h['portraitLabel'])}</span><img class="portrait" src="{path('img/minha-foto.png')}" alt="Felipe Rocha Maia — {e(d['titleRole'])}" width="480" height="480" fetchpriority="high"><div class="portrait-caption"><span class="caption-mark" aria-hidden="true">&lt;/&gt;</span><div><strong>{e(h['portraitCaption'])}</strong><span>{e(h['signature'])}</span></div></div></div><span class="portrait-corner" aria-hidden="true">+</span></div></div></section>
        {education()}
        <section class="section container"><div class="section-heading"><div><p class="eyebrow">{e(h['servicesEyebrow'])}</p><h2>{e(h['servicesTitle'])}</h2></div><p>{e(h['servicesIntro'])}</p></div>{service_cards()}<a class="text-link section-link" href="{page(3)}">{e(u['allServices'])} →</a></section>
        <section class="benefits-section"><div class="container benefits-grid"><div><p class="eyebrow">{e(h['benefitsEyebrow'])}</p><h2>{e(h['benefitsTitle'])}</h2><p>{e(h['benefitsIntro'])}</p><a class="text-link" href="{page(1)}">{e(u['moreAbout'])} →</a></div><div class="benefit-list">{benefits}</div></div></section>
        <section class="section container"><div class="section-heading"><div><p class="eyebrow">{e(h['projectsEyebrow'])}</p><h2>{e(h['projectsTitle'])}</h2></div><a class="text-link" href="{page(2)}">{e(u['allProjects'])} ↗</a></div><p class="projects-intro">{e(h['projectsIntro'])}</p>{project_cards()}</section>
        <section class="about-section"><div class="container about-grid"><div><p class="eyebrow">{e(h['aboutEyebrow'])}</p><h2>{e(h['aboutTitle'])}</h2></div><div><p>{e(h['aboutText'])}</p><p>{e(ed['sentence'])}</p><a class="text-link" href="{page(1)}">{e(u['learnAbout'])} →</a></div></div></section>{cta()}'''
    elif index==1:
        a=d['about']
        paragraphs=''.join(f'<p>{e(t)}</p>' for t in a['story'])
        commitments=''.join(f'<article class="service-card"><span class="service-icon" aria-hidden="true">{n+1:02}</span><h3>{e(t)}</h3><p>{e(v)}</p></article>' for n,(t,v) in enumerate(a['commitments']))
        body=f'''{page_hero(a)}<section class="section container story-grid"><figure class="about-portrait"><img src="{path('img/minha-foto.png')}" alt="Felipe Rocha Maia" width="480" height="480"><figcaption>Felipe Rocha Maia<span>{e(d['titleRole'])}</span></figcaption></figure><div class="story-copy"><h2>{e(a['storyTitle'])}</h2>{paragraphs}</div></section><section class="education-section"><div class="container"><h2>{e(a['educationTitle'])}</h2></div>{education()}</section><section class="section container"><div class="section-heading"><h2>{e(a['commitTitle'])}</h2></div><div class="three-grid">{commitments}</div></section>{cta()}'''
    elif index==2:
        p=d['portfolio']
        filters=''.join(f'<button type="button" data-filter="{cat}" aria-pressed="false">{e(label)}</button>' for cat,label in zip(CATEGORIES,p['categories']))
        body=f'''{page_hero(p)}<section class="section container portfolio-section"><div class="project-filters" role="group" aria-label="{e(u['filters'])}" hidden><button type="button" data-filter="all" aria-pressed="true">{e(u['all'])}</button>{filters}</div><p class="filter-status" role="status" id="filter-status"></p>{project_cards(True)}<p class="empty-projects" id="empty-projects" hidden>{e(u['noProjects'])}</p><p class="small-note">{e(p['techNote'])}</p></section><section class="benefits-section"><div class="container two-grid"><article class="future-slot"><span aria-hidden="true">+</span><h2>{e(p['futureTitle'])}</h2><p>{e(p['futureText'])}</p></article><article class="future-slot"><span aria-hidden="true">↗</span><h2>{e(p['clientsTitle'])}</h2><p>{e(p['clientsText'])}</p></article></div></section>{cta()}'''
    elif index==3:
        s=d['services']; steps=''.join(f'<article><span class="eyebrow">{n+1:02}</span><h3>{e(t)}</h3><p>{e(v)}</p></article>' for n,(t,v) in enumerate(s['process']))
        body=f'''{page_hero(s)}<section class="section container services-page">{service_cards(True)}<p class="pricing-note">{e(s['pricing'])}</p></section><section class="benefits-section"><div class="container"><h2>{e(s['processTitle'])}</h2><div class="three-grid process-grid">{steps}</div></div></section>{cta()}'''
    else:
        c=d['contact'];opts=''.join(f'<option value="{n}">{e(t)}</option>' for n,t in enumerate(c['options']))
        def field(id,label,control,helptext=''):
            return f'<div class="form-field"><label for="{id}">{e(label)}</label>{control}{f"<p class=\"field-help\" id=\"{id}-help\">{e(helptext)}</p>" if helptext else ""}<p class="field-error" id="{id}-error"></p></div>'
        fields=field('name',c['name'],'<input id="name" name="name" type="text" autocomplete="name" minlength="2" maxlength="120" required aria-describedby="name-error">')
        fields+=field('email',c['email'],'<input id="email" name="email" type="email" autocomplete="email" maxlength="254" required aria-describedby="email-error">')
        fields+=field('phone',c['phone'],'<input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="30" placeholder="+55 71 99999 9999" required aria-describedby="phone-help phone-error">',c['phoneHelp'])
        fields+=field('service',c['service'],f'<select id="service" name="service" required aria-describedby="service-error"><option value="">{e(c["choose"])}</option>{opts}</select>')
        fields+=field('description',c['description'],'<textarea id="description" name="message" rows="6" minlength="20" maxlength="5000" required aria-describedby="description-help description-error"></textarea>',c['descriptionHelp'])
        body=f'''{page_hero(c)}<section class="section container contact-grid"><aside class="contact-sidebar"><h2>{e(c['directTitle'])}</h2><p>{e(c['directText'])}</p>{external(WA,u['whatsapp'],'button primary')}{external(EMAIL,'felipercode0698@gmail.com','email-link')}<p class="remote-note">{e(u['remote'])}</p></aside><div class="contact-form-panel"><h2>{e(c['formTitle'])}</h2><p class="notice" id="integration-notice">{e(c['inactive'])}</p><p class="small-note">{e(c['required'])}</p><form id="contact-form" method="post" action="{page(4)}" novalidate><fieldset disabled><legend class="sr-only">{e(c['formTitle'])}</legend>{fields}<div class="spam-trap" aria-hidden="true"><label for="botcheck">{e(c['honeypot'])}</label><input id="botcheck" type="checkbox" name="botcheck" tabindex="-1" autocomplete="off"></div><p class="privacy-note" id="form-privacy">{e(c['privacy'])}</p><button class="button primary" id="contact-submit" type="submit" aria-describedby="integration-notice">{e(c['submit'])}</button></fieldset><p id="form-status" role="status" aria-live="polite" tabindex="-1"></p></form><noscript><p class="notice">{e(c['nojs'])}</p></noscript></div></section>'''

    nav=''.join(f'<a href="{page(i)}"'+(' aria-current="page"' if i==index else '')+f'>{e(name)}</a>' for i,name in enumerate(d['nav']))
    langlinks=''.join(f'<a href="{path(ROUTES[code][index])}?lang={code}" data-language="{code}" lang="{code}" hreflang="{code}"'+(' aria-current="true"' if code==lang else '')+f'>{flag(code)} {name}</a>' for code,(_,name) in FLAGS.items())
    alternates=''.join(f'<link rel="alternate" hreflang="{code}" href="{url(ROUTES[code][index])}">\n' for code in ROUTES)
    alternates+=f'<link rel="alternate" hreflang="x-default" href="{url(ROUTES["pt-BR"][index])}">'
    search=f'''<section class="container search-section" aria-labelledby="busca-titulo"><h2 id="busca-titulo">{e(u['searchHeading'])}</h2><form id="site-search" role="search"><label for="search-input">{e(u['searchLabel'])}</label><div class="search-row"><input id="search-input" name="q" type="search" placeholder="{e(u['searchPlaceholder'])}" maxlength="120" required><button class="button primary" type="submit">{e(u['searchButton'])}</button></div></form><p id="search-status" role="status"></p><ul id="search-results"></ul></section>'''
    config={'lang':lang,'page':index,'routes':{code:path(routes[index]) for code,routes in ROUTES.items()},'ui':u,'contact':d['contact'],'search':[{'title':name,'url':page(i),'terms':' '.join([name,d['meta'][i]]+([d['education']['degree'],d['education']['post']] if i==1 else [])+([' '.join(x[:2]) for x in d['portfolio']['projects']] if i==2 else [])+([x[0] for x in d['services']['items']] if i==3 else []))} for i,name in enumerate(d['nav'])]}
    schema={'@context':'https://schema.org','@graph':[{'@type':'Person','@id':BASE+'#felipe','name':'Felipe Rocha Maia','url':BASE,'image':BASE+'img/minha-foto.png','jobTitle':d['titleRole'],'sameAs':[s[1] for s in SOCIAL]},{'@type':'WebSite','@id':BASE+'#website','url':BASE,'name':'Felipe Rocha Maia — FelipeCode','inLanguage':['pt-BR','en','es'],'publisher':{'@id':BASE+'#felipe'}},{'@type':'WebPage','@id':url(current)+'#page','url':url(current),'name':d['nav'][index]+' | Felipe Rocha Maia','description':d['meta'][index],'inLanguage':lang,'isPartOf':{'@id':BASE+'#website'},'about':{'@id':BASE+'#felipe'}}]}
    title=f"{d['nav'][index]} | Felipe Rocha Maia — FelipeCode" if index else f"Felipe Rocha Maia | {d['digital']} — FelipeCode"
    html=f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(d['meta'][index])}">
<meta name="author" content="Felipe Rocha Maia">
<meta name="theme-color" content="#122a43">
<link rel="icon" type="image/svg+xml" href="{path('assets/icons/felipe-code.svg')}">
<link rel="canonical" href="{url(current)}">
{alternates}
<meta property="og:type" content="website">
<meta property="og:locale" content="{d['locale']}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(d['meta'][index])}">
<meta property="og:url" content="{url(current)}">
<meta property="og:image" content="{BASE}img/minha-foto.png">
<meta property="og:image:alt" content="Felipe Rocha Maia">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{path('assets/css/home.css')}?v=fc">
<link rel="stylesheet" href="{path('assets/css/site.css')}?v=fc">
<script type="application/ld+json">{dump(schema)}</script>
<script id="site-data" type="application/json">{dump(config)}</script>
<script src="{path('js/home.js')}" defer></script>
{f'<script src="{path("js/contact-config.js")}" defer></script><script src="{path("js/contact.js")}" defer></script>' if index==4 else ''}
</head>
<body>
<a class="skip-link" href="#conteudo">{e(u['skip'])}</a>
<header class="site-header"><div class="container header-inner"><a class="brand" href="{page(0)}" aria-label="Felipe Rocha Maia — {e(d['nav'][0])}"><img class="brand-mark" src="{path('assets/icons/felipe-code.svg')}" alt="" width="44" height="48"><span><strong>Felipe Rocha Maia</strong><span class="brand-sub">FelipeCode · {e(d['digital'])}</span></span></a><nav class="primary-nav" aria-label="{e(u['mainNav'])}">{nav}</nav><details class="language-picker"><summary aria-label="{e(u['language'])}">{flag(lang)} {FLAGS[lang][1]} <span aria-hidden="true">⌄</span></summary><nav class="language-panel" aria-label="{e(u['language'])}">{langlinks}</nav></details></div></header>
<main id="conteudo" tabindex="-1">{body}{search}</main>
<footer class="site-footer"><div class="container"><div class="footer-top"><div><a class="footer-brand" href="{page(0)}">Felipe Rocha Maia<span>FelipeCode</span></a><p>{e(d['titleRole'])}.<br>{e(u['footerText'])}</p>{external(EMAIL,'felipercode0698@gmail.com','email-link')}</div><nav aria-label="{e(u['footerNav'])}"><h2>{e(u['explore'])}</h2>{nav}</nav><nav class="social-links" aria-label="{e(u['connect'])}"><h2>{e(u['connect'])}</h2>{''.join(external(href,name) for name,href in SOCIAL)}</nav></div><div class="footer-bottom"><p>© <span id="current-year">2026</span> Felipe Rocha Maia. {e(u['rights'])}</p><p>{e(u['remote'])}</p></div></div></footer>
<a class="floating-whatsapp" href="{e(WA)}" target="_blank" rel="noopener noreferrer" aria-label="{e(u['whatsapp']+u['newTab'])}"><img src="{path('img/icons/whatsapp.png')}" width="25" height="25" alt=""><span>{e(u['floating'])}</span></a>
</body>
</html>
'''
    # Separate block elements for readable generated markup; text remains static for indexing.
    import re
    html=re.sub(r'(?=<\/?(?:article|section|header|footer|nav|main|form|details|summary|figure|fieldset|legend|h[1-3]|p|ul|li|div)\b)', '\n',html)
    html='\n'.join(line.rstrip() for line in html.splitlines())+'\n'
    (ROOT/current).write_text(html,encoding='utf-8')

if __name__=='__main__':
    datasets={code:json.loads((ROOT/'assets/i18n'/f'{code}.json').read_text(encoding='utf-8-sig')) for code in ROUTES}
    def shape(x):
        if isinstance(x,dict):return {k:shape(v) for k,v in x.items()}
        if isinstance(x,list):return [shape(v) for v in x]
        assert isinstance(x,str) and x.strip()
        return 'string'
    assert shape(datasets['pt-BR'])==shape(datasets['en'])==shape(datasets['es']), 'Incomplete translations'
    for data in datasets.values():
        for i in range(5):render(data,i)
    ns='http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('',ns)
    sitemap=ET.Element(f'{{{ns}}}urlset')
    for routes in ROUTES.values():
        for route in routes:
            entry=ET.SubElement(sitemap,f'{{{ns}}}url');ET.SubElement(entry,f'{{{ns}}}loc').text=url(route)
    ET.indent(sitemap)
    ET.ElementTree(sitemap).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /tools/\nSitemap: '+BASE+'sitemap.xml\n',encoding='utf-8')
    print('Generated 15 pages, sitemap and robots.txt. No publication performed.')
