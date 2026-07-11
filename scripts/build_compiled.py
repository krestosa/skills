#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SHARED=ROOT/'shared'
REG=json.loads((ROOT/'orchestrator/registry.json').read_text()); ROUTES=json.loads((SHARED/'manifests/routes.json').read_text())
IDX=json.loads((SHARED/'manifests/source-index.json').read_text()); sections={}
for item in IDX['sources']:
 m=json.loads((SHARED/item['path']).read_text()); data=(SHARED/m['path']).read_bytes()
 for sec in m['sections']: sections[sec['id']]=data[sec['startByte']:sec['endByte']]
def expand(name,seen=None):
 seen=seen or set()
 if name in seen: return [],[]
 seen.add(name); r=ROUTES['routes'][name]; ss=[]; ff=[]
 for e in r.get('extends',[]): a,b=expand(e,seen); ss+=a; ff+=b
 ss+=r.get('sections',[]); ff+=r.get('files',[])
 return list(dict.fromkeys(ss)),list(dict.fromkeys(ff))
p=argparse.ArgumentParser(); p.add_argument('--skills',nargs='*',default=['repository-analysis','architecture','implementation','validation-quality','github-read','github-write','ci-diagnostics','pr-review-merge','recovery','frontend-visual','prompt-engineering','management-delegation','documentation-roadmap','release']); p.add_argument('--output',default=str(ROOT/'dist/skills.compiled.md')); a=p.parse_args()
out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
with out.open('wb') as fh:
 for path in [ROOT/'SKILL.md',ROOT/'orchestrator/SKILL.md',SHARED/'policies/gpt-5.6-sol.md',SHARED/'policies/repository-context-and-authorization.md',SHARED/'policies/network-and-transport.md']:
  fh.write(path.read_bytes()+b'\n\n')
 for sid in a.skills:
  item=next(x for x in REG['skills'] if x['id']==sid); fh.write((ROOT/item['skillFile']).read_bytes()+b'\n\n')
  for route in item['requiredRoutes']:
   ss,ff=expand(route)
   for f in ff: fh.write((SHARED/f).read_bytes()+b'\n\n')
   for s in ss: fh.write(sections[s]+b'\n\n')
print(out)
