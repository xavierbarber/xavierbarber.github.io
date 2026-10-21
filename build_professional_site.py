"""Static trilingual website. Run with Python 3 and Pandoc; no client framework."""
from pathlib import Path
import argparse, json, html, re, shutil, subprocess
from urllib.parse import quote
R=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--pandoc',default=shutil.which('pandoc') or '/opt/homebrew/bin/pandoc');args=parser.parse_args()
DATA={l:json.loads((R/f'content/{l}.json').read_text()) for l in ('es','ca','en')}
PAPERS=json.loads((R/'content/papers.json').read_text())
BASE='https://xavierbarber.github.io/'
IDS=['consultoria','investigacion','proyectos','humanista','formacion','personal']
LINKS=['https://comunicacion.umh.es/2026/04/20/investigadores-de-la-umh-participan-en-el-desarrollo-del-nuevo-sistema-viogen-2-para-la-mejora-de-la-valoracion-del-riesgo-en-violencia-de-genero/','https://doi.org/10.1007/s00464-024-11237-4','https://doi.org/10.1016/j.aquaculture.2024.740917','https://doi.org/10.1016/j.talanta.2013.02.009','https://doi.org/10.3390/agronomy11091870','https://doi.org/10.1111/1750-3841.13501']
E=html.escape

def path(l):return '' if l=='es' else l+'/'
def root(l):return '' if l=='es' else '../'
def link(text,url,cls='text-link'):return f'<a class="{cls}" href="{E(url,quote=True)}">{E(text)} <span aria-hidden="true">↗</span></a>'
def label(d,key):return f'<p class="eyebrow">{E(d[key])}</p>'
def heading(d,key):return f'<h2>{E(d[key])}</h2>'
def paragraphs(ps):return ''.join(f'<p>{E(p)}</p>' for p in ps)

def shell(l,key,body,title=None):
 d=DATA[l];p=root(l);home='' if key=='index' else 'index.html';title=title or d['title'];url=BASE+path(l)+('' if key=='index' else key+'.html')
 nav=''.join(f'<a'+(' class="nav-consulting"' if i=='consultoria' else '')+f' href="'+('' if i=='consultoria' else home)+f'#{i}">{E(n)}</a>' for i,n in zip(IDS,d['nav']))
 langs=''.join(f'<a href="{p}{path(ll)}{key}.html" lang="{DATA[ll]["lang"]}" hreflang="{DATA[ll]["lang"]}"'+(' aria-current="true"' if ll==l else '')+f'>{name}</a>' for ll,name in [('es','ES'),('ca','VA'),('en','EN')])
 alts=''.join(f'<link rel="alternate" hreflang="{DATA[ll]["lang"]}" href="{BASE}{path(ll)}{key}.html">' for ll in DATA)
 return f'''<!doctype html>
<html lang="{d['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · Xavier Barber</title><meta name="description" content="{E(d['intro'],quote=True)}"><link rel="canonical" href="{url}">{alts}<link rel="alternate" hreflang="x-default" href="{BASE}{key}.html"><meta property="og:title" content="{E(title,quote=True)} · Xavier Barber"><meta property="og:description" content="{E(d['intro'],quote=True)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta name="theme-color" content="#0c1117"><link rel="icon" href="{p}assets/monogram.svg" type="image/svg+xml"><link rel="stylesheet" href="{p}assets/site.css?v=20261021-consulting-nav"><script defer src="{p}assets/site.js?v=20261021-consulting-nav"></script></head>
<body><a class="skip" href="#main">{E(d['skip'])}</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="index.html">XAVIER BARBER<span>{E(d['brandtag'])}</span></a><button class="menu-toggle" aria-expanded="false" aria-controls="main-nav">{d['menu']} <span aria-hidden="true">☰</span></button><nav id="main-nav" aria-label="{E(d['menu'])}">{nav}{link(d['talk'],'#contact','nav-contact')}</nav><nav class="languages" aria-label="{E(d['language'])}">{langs}</nav></div></header><main id="main">{body}</main>{contact(l)}<footer><div class="wrap footer-inner"><div class="brand">XAVIER BARBER<span>{E(d['footer'])}</span></div><div>{link('ORCID','https://orcid.org/0000-0003-3079-5855')}{link('Google Scholar','https://scholar.google.com/citations?user=KUzOpI4AAAAJ')}{link(d['umhprofile'],'https://portalinvestigacion.umh.es/investigadores/2181582/detalle')}</div><small>© 2026 Xavier Barber · {E(d['location'])}</small></div></footer></body></html>'''

def hero(l):
 d=DATA[l];p=root(l)
 return f'''<section class="hero" id="inicio" data-hud="off"><div class="hero-photo" aria-hidden="true"><img src="{p}photos/xavier-bayes.webp" width="1536" height="1024" fetchpriority="high" alt=""><div class="hero-hud"><div class="hud-stage"><img class="hud-panels" src="{p}assets/hero-hud.svg" width="800" height="710" alt=""><div class="hud-orbit"></div><div class="hud-scan"></div></div></div></div><div class="wrap hero-content">{label(d,'eyebrow')}<h1>{E(d['hero'][0])}<br><span>{E(d['hero'][1])}</span></h1><p class="hero-intro">{E(d['intro'])}</p><div class="actions">{link(d['cta'],'#contact','button')}{link(d['researchcta'],'#investigacion')}</div><p class="hero-role">{E(d['role'])}</p></div><div class="hero-bottom wrap"><span>{E(d['photocaption'])}</span><div class="hud-controls"><button class="hud-toggle" hidden data-pause="{E(d['hudlabels'][0])}" data-resume="{E(d['hudlabels'][1])}" data-enable="{E(d['hudlabels'][2])}"><span class="hud-toggle-icon" aria-hidden="true">Ⅱ</span> <span class="hud-toggle-label">{E(d['hudlabels'][0])}</span></button></div></div></section><div class="credentials"><div class="wrap">{''.join('<div><strong>'+E(a)+'</strong><span>'+E(b)+'</span></div>' for a,b in d['credentials'])}</div></div>'''

def profile(l,expanded=False):
 d=DATA[l];p=root(l)
 s=f'''<section class="section" id="perfil"><div class="wrap profile-grid"><div>{label(d,'aboutlabel')}{heading(d,'abouttitle')}<p class="lead">{E(d['aboutlead'])}</p>{paragraphs(d['aboutparagraphs'] if expanded else d['aboutparagraphs'][:2])}{link(d['profilecta'],'about.html#career')}</div><figure><img src="{p}photos/spatial-statistics-talk.svg" width="1200" height="900" loading="lazy" alt="{E(d['researchphotoalt'])}"><figcaption>Xavier Barber · i-MInD · UMH</figcaption></figure></div>'''
 if expanded:s+=f'<div class="wrap career" id="career"><h3>{E(d["career"])}</h3><ul>'+''.join('<li>'+E(t)+'</li>' for t in d['careeritems'])+'</ul></div>'
 return s+'</section>'

def research(l):
 d=DATA[l]
 s=f'<section class="section alt" id="investigacion"><div class="wrap">{label(d,"researchlabel")}<div class="section-head"><h2>{E(d["researchtitle"])}</h2><p>{E(d["researchintro"])}</p></div><div class="filters" role="group" aria-label="{E(d["filterlabel"])}">'+''.join(f'<button class="filter" data-filter="{i}" aria-pressed="{str(i==0).lower()}">{E(t)}</button>' for i,t in enumerate(d['filters']))+'</div><div class="papers">'
 for n,p in enumerate(PAPERS):
  names=p['authors'].split(';');short=names[0].split(',')[0]+(' et al.' if len(names)>1 else '')
  s+=f'''<article class="paper" data-category="{p['category']}"><div class="paper-meta"><span>{p['year']}</span><span>{E(d['filters'][p['category']])}</span></div><h3>{E(d['papertitles'][n])}</h3><p>{E(d['paperdescs'][n])}</p><details class="citation"><summary>{E(d['citationlabel'])}</summary><div><p class="original-title"><a href="{p['url']}">{E(p['title'])}</a></p><p class="journal">{E(p['journal'])} · {p['year']}</p><p class="authors">{E(short)}</p></div></details>{link(d['readpaper'],p['url'])}</article>'''
 return s+f'</div><div class="research-bottom"><span class="filter-count" aria-live="polite" data-count-label="{E(d["results"])}">6 {E(d["results"])}</span>{link(d["allpapers"],"cva.html")}</div></div></section>'

def projects(l):
 d=DATA[l];s=f'<section class="section" id="proyectos"><div class="wrap">{label(d,"projectslabel")}<div class="section-head">{heading(d,"projectstitle")}<p>{E(d["projectsintro"])}</p></div><div class="projects">'
 for i,(title,tag,body,url) in enumerate(zip(d['projectnames'],d['projecttags'],d['projecttexts'],LINKS)):
  anchor=['human-centred','health','environment','circular','golf','food'][i]
  s+=f'<article class="project" id="{anchor}"><div class="project-top"><p class="eyebrow">{E(tag)}</p><span>0{i+1}</span></div><h3>{E(title)}</h3><p>{E(body)}</p>{link(d["reference"],url)}</article>'
 return s+f'</div><aside class="collaboration"><div><h3>{E(d["partner"])}</h3><p>{E(d["partnertext"])}</p></div>{link(d["partnerlink"],"https://juan-aparicio-ia.chatgpt-umh.chatgpt.site/")}</aside></div></section>'

def human(l):
 d=DATA[l];s=f'<section class="section human" id="humanista"><div class="wrap">{label(d,"humanlabel")}<div class="human-grid"><div>{heading(d,"humantitle")}<p class="lead">{E(d["humanintro"])}</p><p>{E(d["humantext"])}</p></div><div class="principles">'
 for i,(a,b) in enumerate(d['principles']):s+=f'<article><span class="number">0{i+1}</span><h3>{E(a)}</h3><p>{E(b)}</p></article>'
 return s+f'</div></div><aside class="ethics" id="ethics"><span aria-hidden="true">◎</span><div><h3>{E(d["ethicstitle"])}</h3><p>{E(d["ethicstext"])}</p></div></aside></div></section>'

def training(l):
 d=DATA[l];s=f'<section class="section" id="formacion"><div class="wrap">{label(d,"traininglabel")}<div class="section-head">{heading(d,"trainingtitle")}<p>{E(d["trainingintro"])}</p></div><div class="course-list">'
 for i,(a,b) in enumerate(d['courses']):s+=f'<article><span class="number">0{i+1}</span><h3>{E(a)}</h3><p>{E(b)}</p></article>'
 return s+f'</div><div class="training-end"><p>{E(d["teachingnote"])}</p>{link(d["trainingcta"],"mailto:xbarber@umh.es?subject="+quote(d["contactoptions"][1]),"button")}</div></div></section>'

def personal(l):
 d=DATA[l];p=root(l)
 photos=[('photos/cycling-video.jpg',1920,1080),('photos/leisure/dansa.webp',935,1400),('photos/leisure/rowing.webp',1050,1400),('photos/leisure/moments-together.webp',1000,750),('photos/leisure/dolcaina.webp',1050,1400),('photos/leisure/sea.webp',1200,900)]
 gallery=''
 for i,(src,w,h) in enumerate(photos):
  caption=d['gallerytitles'][i];credit=d['photocredit'] if i==1 else ''
  gallery+=f'<figure class="leisure-photo"><a href="{p}{src}" class="photo-open" data-caption="{E(caption,quote=True)}" data-credit="{E(credit,quote=True)}" aria-label="{E(d["expandphoto"]+": "+caption,quote=True)}"><img src="{p}{src}" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{E(d["galleryalts"][i],quote=True)}"><span class="photo-zoom" aria-hidden="true">↗</span></a><figcaption>{E(caption)}'+(f'<small>{E(credit)}</small>' if credit else '')+'</figcaption></figure>'
 return f'''<section class="section personal" id="personal"><div class="wrap">{label(d,'personallabel')}<div class="section-head">{heading(d,'personaltitle')}<p>{E(d['personalintro'])}</p></div><div class="leisure-gallery" role="group" aria-label="{E(d['gallerylabel'])}">{gallery}</div><div class="personal-notes"><div><h3>{E(d['biketitle'])}</h3><p>{E(d['biketext'])}</p></div><div><h3>{E(d['musictitle'])}</h3><p>{E(d['musictext'])}</p></div></div><p class="rowing-note">{E(d['rowingnote'])}</p></div></section><dialog class="photo-dialog" aria-label="{E(d['gallerylabel'])}"><button class="photo-close" aria-label="{E(d['closephoto'])}" autofocus>×</button><figure><img alt=""><figcaption class="photo-caption"></figcaption></figure></dialog>'''

def download(l):
 d=DATA[l];return f'<aside class="download wrap" id="transfer-infographic"><div><h3>{E(d["downloadtitle"])}</h3><p>{E(d["downloadtext"])}</p></div><a class="button outline" href="{root(l)}downloads/xavier-barber-ia-ciencia-datos.pdf" download>{E(d["downloadcta"])} <span aria-hidden="true">↓</span></a></aside>'

def contact(l):
 d=DATA[l];address="<br>".join(E(line) for line in d["contactaddress"])
 consulting=f'<div class="contact-consulting" id="consultoria"><div><h3>{E(d["consultingtitle"])}</h3><p class="consulting-lead">{E(d["consultinglead"])}</p><p>{E(d["consultingtext"])}</p></div>{link(d["consultingcta"],"mailto:xbarber@umh.es?subject="+quote(d["consultingtitle"]),"button outline")}</div>'
 return f'<section class="section contact" id="contact"><div class="wrap"><div class="contact-grid"><div>{label(d,"contactlabel")}{heading(d,"contacttitle")}<p>{E(d["contacttext"])}</p></div><div><a class="email" href="mailto:xbarber@umh.es">xbarber@umh.es ↗</a><p>Universidad Miguel Hernández de Elche<br>{address}</p></div></div>{consulting}<div class="contact-options">'+''.join(link(t,'mailto:xbarber@umh.es?subject='+quote(t)) for t in d['contactoptions'][1:])+'</div></div></section>'

RAW=subprocess.check_output([args.pandoc,str(R/'cva.Rmd'),'--from=markdown','--to=html5','--wrap=none'],text=True)
SECTIONS=['artificial-intelligence','spatial-statistics','efficiency-productivity','highly-cited','further-artificial-intelligence-publications']
def bibliography(l):
 d=DATA[l]
 # Keep the original publication bodies (titles, authors, identifiers and counts).
 # Replace only editorial headings and category labels, outside all anchor text.
 body=RAW[RAW.index('<h2 id="artificial-intelligence"'):RAW.index('<h2 id="academic-profile"')]
 body=re.sub(r'<p>(?:Machine learning, Bayesian networks|Research with).*?</p>','',body,flags=re.S)
 # The AI list is navigation; the original detailed records follow it.
 for id,title in zip(SECTIONS,d['pubsections']):body=re.sub(r'(<h2 id="'+id+r'">).*?</h2>',lambda m:m.group(1)+E(title)+'</h2>',body)
 tags={'es':{'Artificial Intelligence':'Inteligencia artificial','Spatial &amp; environmental statistics':'Estadística espacial y ambiental','Efficiency &amp; productivity':'Eficiencia y productividad','Preprint · Dataset resource':'Preprint · Recurso de datos'},'ca':{'Artificial Intelligence':'Intel·ligència artificial','Spatial &amp; environmental statistics':'Estadística espacial i ambiental','Efficiency &amp; productivity':'Eficiència i productivitat','Preprint · Dataset resource':'Preprint · Recurs de dades'},'en':{}}[l]
 def tag(m):
  t=m.group(1)
  for a,b in tags.items():t=t.replace(a,b)
  return '<span class="tag">'+t.replace('citations',d['pubtag'])+'</span>'
 body=re.sub(r'<span class="tag">(.*?)</span>',tag,body)
 nav=''.join(link(t,'#'+i) for i,t in zip(SECTIONS,d['pubsections']))
 return f'<section class="section bibliography"><div class="wrap">{link(d["back"],"index.html")}<h1>{E(d["pubtitle"])}</h1><p class="lead">{E(d["pubintro"])}</p><div class="bibliography-grid"><aside>{nav}</aside><div class="records">{body}<h2 id="academic-profile">{E(d["career"])}</h2>{link(d["profilecta"],"about.html#career")}</div></div></div></section>'

for l,d in DATA.items():
 out=R/path(l);out.mkdir(exist_ok=True)
 pages={'index':hero(l)+profile(l)+research(l)+projects(l)+human(l)+training(l)+personal(l)+download(l),'about':profile(l,True)+human(l)+personal(l)+download(l),'xbarber':projects(l)+human(l)+download(l),'training':training(l),'cva':bibliography(l)}
 for key,body in pages.items():
  if key not in ('index','cva'):
   titles={'about':d['abouttitle'],'xbarber':d['projectstitle'],'training':d['trainingtitle']}
   # Each interior page gets one top-level heading; retain section hierarchy below it.
   body=re.sub(r'<h2>(.*?)</h2>',r'<h1>\1</h1>',body,count=1)
  (out/f'{key}.html').write_text(shell(l,key,body,d['pubtitle'] if key=='cva' else None))
urls=[BASE+path(l)+('' if key=='index' else key+'.html') for l in DATA for key in ('index','about','xbarber','training','cva')]
(R/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+u+'</loc></url>' for u in urls)+'</urlset>')
(R/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n')
print('Built 15 pages: Spanish, Valencian and British English.')
