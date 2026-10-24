from pathlib import Path
import json,re,zipfile
R=Path(__file__).resolve().parents[1]
cases=json.loads((R/'data/cases.json').read_text());sources=json.loads((R/'data/sources.json').read_text())
assert len(cases)==151
assert len({c['id'] for c in cases})==151 and len({c['title'] for c in cases})==151
assert len(set(c['group'] for c in cases))==18
assert len({s['id'] for s in sources})==19
assert sum(bool(c['sources']) for c in cases)==56
html=(R/'index.html').read_text()
assert '__DATA__' not in html and '__SOURCES__' not in html
assert '<b>151</b>个场景' in html
for c in cases:
 assert c['title'] in html and c['title'] in (R/'GUIDE.md').read_text()
for href in re.findall(r'href="([^"#]+)"',html.split('<script>')[0]):
 if not href.startswith(('http','${')): assert (R/href).is_file(),href
with zipfile.ZipFile(R/'downloads/social-conversation.zip') as z:
 assert z.testzip() is None
 assert len(z.namelist())==21
 assert 'social-conversation/SKILL.md' in z.namelist()
for f in R.rglob('*'):
 if f.is_file() and '.git' not in f.parts and f.suffix!='.zip':
  text=f.read_text()
  assert not re.search(r'(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{30,}|/Use[r]s/)',text),f
print('PASS: 151 unique scenarios, 18 topics, 56 sourced / 95 original, 19 sources, downloads and privacy scan')
