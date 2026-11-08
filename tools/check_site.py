"""Offline checks for the generated static site. No third-party packages required."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from xml.etree import ElementTree as ET
import importlib.util, json, re, subprocess, sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build_site',ROOT/'tools/build_site.py')
build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.tags=[];self.stack=[];self.issues=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a))
  if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append(tag)
 def handle_endtag(self,tag):
  if not self.stack or self.stack[-1]!=tag:self.issues.append('Unbalanced '+tag)
  else:self.stack.pop()
 def find(self,tag,**attrs):return [a for t,a in self.tags if t==tag and all(a.get(k)==v for k,v in attrs.items())]

count=links=0
for lang,routes in build.ROUTES.items():
 for i,route in enumerate(routes):
  f=ROOT/route;s=f.read_text(encoding='utf-8');p=Page(s)
  assert not p.issues and not p.stack,(route,p.issues,p.stack)
  assert p.find('html',lang=lang)
  assert len(p.find('h1'))==len(p.find('main'))==len(p.find('title'))==1,route
  assert len(p.find('meta',name='description'))==1
  assert p.find('link',rel='canonical',href=build.url(route))
  for code,alternates in build.ROUTES.items():
   assert p.find('link',rel='alternate',hreflang=code,href=build.url(alternates[i]))
  assert p.find('link',rel='alternate',hreflang='x-default',href=build.url(build.ROUTES['pt-BR'][i]))
  ids=[a['id'] for _,a in p.tags if 'id' in a];assert len(ids)==len(set(ids)),route
  assert 'formsubmit' not in s.lower(),route
  assert 'googletagmanager' not in s.lower() and 'google-analytics' not in s.lower()
  for tag,a in p.tags:
   if tag=='img':assert all(k in a for k in ['alt','width','height']),route
   if tag in ['input','select','textarea'] and a.get('type') not in ['hidden','checkbox']:
    assert p.find('label',**{'for':a['id']}),(route,a)
   if tag=='label':assert a.get('for') in ids,(route,a)
   if a.get('target')=='_blank':assert 'noopener' in a.get('rel','') and 'noreferrer' in a.get('rel','')
   for attr in ['href','src']:
    if attr not in a:continue
    ref=a[attr];u=urlsplit(ref)
    if u.scheme:
     assert u.scheme=='https',(route,ref)
     continue
    target=(f.parent/unquote(u.path)).resolve() if u.path else f
    assert target.is_relative_to(ROOT.resolve()),(route,ref)
    assert target.is_file(),(route,ref)
    if u.fragment:
     dest=Page(target.read_text(encoding='utf-8'))
     assert any(x.get('id')==u.fragment for _,x in dest.tags),(route,ref)
    links+=1
  for match in __import__('re').finditer(r'<script[^>]+type="application/(?:ld\+json|json)"[^>]*>(.*?)</script>',s,__import__('re').S):json.loads(match.group(1))
  assert p.find('a',href=build.WA)
  assert p.find('a',href=build.EMAIL)
  for _,href in build.SOCIAL:assert p.find('a',href=href)
  if i==4:
   assert p.find('fieldset')[0].get('disabled','missing')!='missing'
   assert not p.find('input',name='access_key')
  count+=1
urls=ET.parse(ROOT/'sitemap.xml').getroot()
assert len(urls)==15
assert {x[0].text for x in urls}=={build.url(r) for rr in build.ROUTES.values() for r in rr}
assert (ROOT/'robots.txt').read_text().endswith(build.BASE+'sitemap.xml\n')
for script in (ROOT/'js').glob('*.js'):
 subprocess.run(['node','--check',str(script)],check=True)
config = (ROOT/'js/contact-config.js').read_text(encoding='utf-8-sig')
assert re.search(r'\benabled:\s*(?:true|false)\b', config), 'Missing contact activation setting'
if re.search(r'\benabled:\s*true\b', config):
 assert re.search(r"\baccessKey:\s*'[\da-fA-F]{8}(?:-[\da-fA-F]{4}){3}-[\da-fA-F]{12}'", config), 'Enabled Web3Forms requires a UUID-formatted Access Key'
print(f'PASS: {count} pages; {links} local references; balanced markup; labels; image metadata; canonical and hreflang; sitemap; preserved contacts; JavaScript syntax; contact configuration; no trackers.')
