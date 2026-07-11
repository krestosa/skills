#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SHARED=ROOT/'shared'
errors=[]

def load_json(path):
 try: return json.loads(path.read_text(encoding='utf-8'))
 except Exception as exc: errors.append(f'invalid json {path.relative_to(ROOT)}: {exc}'); return {}

def require(path):
 if not path.is_file(): errors.append('missing '+path.relative_to(ROOT).as_posix())

# Single-layer structure.
for path in [ROOT/'README.md',ROOT/'SKILL.md',ROOT/'orchestrator/SKILL.md',ROOT/'orchestrator/registry.json',ROOT/'orchestrator/delegation-envelope.schema.json',SHARED/'manifests/routes.json']:
 require(path)
readmes=list(ROOT.rglob('README.md'))
if readmes != [ROOT/'README.md']: errors.append('repository must contain exactly one README.md at root')
legacy_name='skill'+'-orquestador'
legacy_label='skill'+' '+'orquestador'
for forbidden in ['skills/main','skills/orchestrator','skills/individual','skills/'+legacy_name]:
 if (ROOT/forbidden).exists(): errors.append('duplicate legacy layer exists: '+forbidden)
for candidate in ROOT.rglob('*'):
 if legacy_name in candidate.as_posix(): errors.append('legacy orchestrator path exists: '+candidate.relative_to(ROOT).as_posix())
 if candidate.is_file() and candidate != ROOT/'scripts/validate.py' and candidate.suffix in {'.md','.json','.py','.txt'}:
  text=candidate.read_text(encoding='utf-8',errors='ignore')
  if legacy_name in text.lower() or legacy_label in text.lower(): errors.append('legacy orchestrator name in '+candidate.relative_to(ROOT).as_posix())
if (ROOT/'.github/workflows').exists(): errors.append('GitHub workflows are prohibited')

main=(ROOT/'SKILL.md').read_text(encoding='utf-8') if (ROOT/'SKILL.md').is_file() else ''
orch=(ROOT/'orchestrator/SKILL.md').read_text(encoding='utf-8') if (ROOT/'orchestrator/SKILL.md').is_file() else ''
if 'orchestrator/SKILL.md' not in main: errors.append('main must load the orchestrator')
if re.search(r'skills/[a-z0-9-]+/SKILL\.md',main): errors.append('main must not load individual skills directly')
for marker in ['Select one primary skill','Do not load all skills preemptively','registry.json','shared/manifests/routes.json']:
 if marker not in orch: errors.append('orchestrator missing marker: '+marker)

routes=load_json(SHARED/'manifests/routes.json').get('routes',{})
reg=load_json(ROOT/'orchestrator/registry.json')
ids=[]
for item in reg.get('skills',[]):
 sid=item.get('id'); ids.append(sid)
 expected=f'skills/{sid}/SKILL.md'
 if item.get('skillFile')!=expected: errors.append(f'{sid} path must be {expected}')
 path=ROOT/expected; require(path)
 text=path.read_text(encoding='utf-8',errors='ignore') if path.is_file() else ''
 for h in ['## Role','## Personality','## Collaboration style','## Goal','## Success criteria','## Select when','## Exclude when','## Shared routes','## Output','## Stop rules']:
  if h not in text: errors.append(f'{sid} missing {h}')
 for route in item.get('requiredRoutes',[])+item.get('optionalRoutes',[]):
  if route not in routes: errors.append(f'{sid} references unknown route {route}')
 for dep in item.get('dependencies',[]):
  if dep not in [x.get('id') for x in reg.get('skills',[])]: errors.append(f'{sid} unknown dependency {dep}')
 if not item.get('loadPolicy',{}).get('onDemand'): errors.append(f'{sid} must be on-demand')
if len(ids)!=14 or len(ids)!=len(set(ids)): errors.append('expected 14 unique individual skills')

# Catalogs are exact.
def catalog_payload(path):
 data=path.read_bytes(); b=b'<!-- VERBATIM_CATALOG_BEGIN -->\n'; e=b'<!-- VERBATIM_CATALOG_END -->\n'
 return data[data.index(b)+len(b):data.index(e)].rstrip(b'\n')
for rel,count,digest in [('catalogs/github-read-verbatim.md',56,'610c387f5f7c9047c65fef08734d5199696230866ca79e270700209eaab1324e'),('catalogs/github-write-verbatim.md',41,'499373638143f48b0549701bf5036725a2c2bc9b332a95d9a053a1e1ce687a3d')]:
 path=SHARED/rel; require(path)
 if path.is_file():
  payload=catalog_payload(path)
  if hashlib.sha256(payload).hexdigest()!=digest: errors.append('catalog payload hash mismatch '+rel)
  if len([p for p in payload.decode().split('\n\n') if p.strip()])!=count: errors.append('catalog count mismatch '+rel)

# Canonical source losslessness.
r=subprocess.run([sys.executable,str(ROOT/'scripts/verify_lossless.py')],cwd=ROOT,text=True,capture_output=True)
if r.returncode: errors.append('lossless validation failed:\n'+r.stdout+r.stderr)
r=subprocess.run([sys.executable,str(ROOT/'scripts/validate_gpt56.py')],cwd=ROOT,text=True,capture_output=True)
if r.returncode: errors.append('GPT-5.6 validation failed:\n'+r.stdout+r.stderr)

# Active hierarchy transport boundary.
active='\n'.join([main,orch]+[(ROOT/item['skillFile']).read_text(encoding='utf-8') for item in reg.get('skills',[])])
if 'Remote GitHub operations use the GitHub connector' not in active: errors.append('connector-only GitHub boundary missing')
if re.search(r'(?m)^\s*(git\s+(clone|fetch|pull|push|ls-remote)|gh\s+(api|repo|pr|issue|run|workflow|release|search))\b',active): errors.append('remote git or gh command found in active hierarchy')

# Full repository integrity, excluding generated dist and self.
integrity_path=SHARED/'manifests/integrity.json'
integrity=load_json(integrity_path)
actual=[]
for p in ROOT.rglob('*'):
 if not p.is_file() or p==integrity_path or 'dist' in p.parts or '__pycache__' in p.parts: continue
 data=p.read_bytes(); actual.append({'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
actual.sort(key=lambda x:x['path'])
if actual!=integrity.get('files'): errors.append('repository integrity mismatch')

# Build determinism and flat limit.
with tempfile.TemporaryDirectory() as td:
 a=Path(td)/'a.md'; b=Path(td)/'b.md'
 for out in [a,b]:
  rr=subprocess.run([sys.executable,str(ROOT/'scripts/build_compiled.py'),'--output',str(out)],cwd=ROOT,text=True,capture_output=True)
  if rr.returncode: errors.append('compiled build failed: '+rr.stdout+rr.stderr)
 if a.exists() and b.exists() and a.read_bytes()!=b.read_bytes(): errors.append('compiled build is not deterministic')
 flat=Path(td)/'flat'
 rr=subprocess.run([sys.executable,str(ROOT/'scripts/build_chatgpt_flat.py'),'--output',str(flat)],cwd=ROOT,text=True,capture_output=True)
 if rr.returncode: errors.append('flat build failed: '+rr.stdout+rr.stderr)
 elif len(list(flat.iterdir()))>25: errors.append('flat build exceeds 25 files')

if errors:
 print('VALIDATION: FAIL')
 for e in errors: print('-',e)
 raise SystemExit(1)
print('VALIDATION: PASS')
print('main: root SKILL.md')
print('orchestrators: 1')
print('individual_skills:',len(ids))
print('readmes: 1')
print('canonical_sources: 15 lossless')
print('github_read_entries: 56')
print('github_write_entries: 41')
print('github_remote: connector-only')
print('github_workflows: absent')
