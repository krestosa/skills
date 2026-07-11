#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
MAN=json.loads((ROOT/"manifests/modules.json").read_text())
SOURCE_INDEX=json.loads((ROOT/MAN["sourceIndex"]).read_text())
SOURCES=[json.loads((ROOT/x["path"]).read_text()) for x in SOURCE_INDEX["sources"]]
SECTIONS={}
for _src in SOURCES:
 for _sec in _src["sections"]: SECTIONS[_sec["id"]]={"source":_src["path"],**_sec}
def resolve_route(name,stack=None):
 stack=[] if stack is None else stack
 if name in stack: raise ValueError("route cycle")
 r=MAN["routes"][name]; secs=[]; files=[]
 for parent in r.get("extends",[]):
  a,b=resolve_route(parent,stack+[name]); secs+=a; files+=b
 secs+=r.get("sections",[]); files+=r.get("files",[])
 return list(dict.fromkeys(secs)),list(dict.fromkeys(files))
def resolve_profile(name,stack=None):
 stack=[] if stack is None else stack
 if name in stack: raise ValueError("profile cycle")
 d=json.loads((ROOT/MAN["profiles"][name]).read_text()); secs=[]
 for parent in d.get("extends",[]): secs+=resolve_profile(parent,stack+[name])
 secs+=d.get("sections",[]); return list(dict.fromkeys(secs))
def section_bytes(sid):
 s=SECTIONS[sid]; data=(ROOT/s["source"]).read_bytes(); return data[s["startByte"]:s["endByte"]]

errors=[]
for f in MAN["alwaysFiles"]:
 if not (ROOT/f).is_file(): errors.append("missing always "+f)
for name in MAN["routes"]:
 try: secs,files=resolve_route(name)
 except Exception as e: errors.append(str(e)); continue
 for sid in secs:
  if sid not in SECTIONS: errors.append(f"route {name} missing section {sid}")
 for f in files:
  if not (ROOT/f).is_file(): errors.append(f"route {name} missing file {f}")
for name in MAN["profiles"]:
 try: secs=resolve_profile(name)
 except Exception as e: errors.append(str(e)); continue
 for sid in secs:
  if sid not in SECTIONS: errors.append(f"profile {name} missing section {sid}")
write_sections={x for x in SECTIONS if x.startswith("52.9")}; write_files={"catalogs/github-write-verbatim.md","policies/github-write-safety.md","policies/connector-native-integrity.md"}
for name in ["github-read","ci-inspect","review-read","issue-read"]:
 secs,files=resolve_route(name); bad=(set(secs)&write_sections)|(set(files)&write_files)
 if bad: errors.append(f"read route {name} has write content {sorted(bad)}")
stack=set(resolve_profile("typescript"))|set(resolve_profile("node"))|set(resolve_profile("electron"))
for name in ["plan","architecture","implement","validate","security","runtime","release","audit","documentation","roadmap"]:
 secs,_=resolve_route(name); bad=set(secs)&stack
 if bad: errors.append(f"generic route {name} has stack content {sorted(bad)}")
used=set(); [used.update(resolve_route(n)[0]) for n in MAN["routes"]]; [used.update(resolve_profile(n)) for n in MAN["profiles"]]
inactive={x["section"] for x in MAN["inactiveSections"]}
for sid in SECTIONS:
 if sid not in used and sid not in inactive: errors.append("unreachable section "+sid)
 if sid in used and sid in inactive: errors.append("inactive section routed "+sid)
r=subprocess.run([sys.executable,str(ROOT/"scripts/verify_lossless.py")],capture_output=True,text=True)
if r.returncode: errors.append(r.stdout+r.stderr)
BEGIN="<!-- VERBATIM_CATALOG_BEGIN -->\n"; END="\n<!-- VERBATIM_CATALOG_END -->"
for rel,count,digest in [("catalogs/github-read-verbatim.md",56,"610c387f5f7c9047c65fef08734d5199696230866ca79e270700209eaab1324e"),("catalogs/github-write-verbatim.md",41,"499373638143f48b0549701bf5036725a2c2bc9b332a95d9a053a1e1ce687a3d")]:
 text=(ROOT/rel).read_text(); payload=text.split(BEGIN,1)[1].split(END,1)[0].encode();
 if len([p for p in payload.decode().split("\n\n") if p.strip()])!=count or hashlib.sha256(payload).hexdigest()!=digest: errors.append("catalog mismatch "+rel)
if (ROOT.parents[1]/".github/workflows").exists(): errors.append("workflows prohibited")
needle="krestosa/"+"Crystal"
for p in ROOT.rglob("*"):
 if p.is_file() and p.suffix in {".md",".json",".py",".txt"} and p.name!="validate_skill.py" and needle in p.read_text(errors="ignore"): errors.append("hardcoded repo "+str(p.relative_to(ROOT)))
active=set(MAN["alwaysFiles"]); [active.update(resolve_route(n)[1]) for n in MAN["routes"]]
remote=re.compile(r"(?m)^\s*(git\s+(clone|fetch|pull|push|ls-remote)|gh\s+(auth|api|repo|pr|issue|run|workflow|release|search))\b")
for sid in used:
 text=section_bytes(sid).decode(errors="ignore")
 if remote.search(text) and sid not in {"9.3"}: errors.append("remote command in active section "+sid)
 if re.search(r"git\s+(switch|checkout)\s+main\b|working tree.*\bmain\b.*commits",text,re.I): errors.append("main branch hardcode in section "+sid)
integ=json.loads((ROOT/"manifests/integrity.json").read_text()); expected_files=[]
for shard in integ["shards"]:
 raw=(ROOT/shard["path"]).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=shard["sha256"]: errors.append("integrity shard hash "+shard["path"])
 expected_files += json.loads(raw)["files"]
actual=[]
for p in sorted(ROOT.rglob("*")):
 if p.is_file():
  rel=p.relative_to(ROOT).as_posix()
  if rel.startswith("dist/") or "__pycache__" in rel or rel=="manifests/integrity.json" or rel.startswith("manifests/integrity/"): continue
  d=p.read_bytes(); actual.append({"path":rel,"sha256":hashlib.sha256(d).hexdigest(),"bytes":len(d)})
if actual!=expected_files: errors.append("integrity mismatch")
with tempfile.TemporaryDirectory() as td:
 a=Path(td)/"a"; b=Path(td)/"b"; flat=Path(td)/"flat"
 for x in [a,b]:
  r=subprocess.run([sys.executable,str(ROOT/"scripts/build_compiled.py"),"--output",str(x)],capture_output=True,text=True)
  if r.returncode: errors.append("compiled build fail")
 if a.exists() and b.exists() and a.read_bytes()!=b.read_bytes(): errors.append("nondeterministic build")
 r=subprocess.run([sys.executable,str(ROOT/"scripts/build_chatgpt_flat.py"),"--output",str(flat)],capture_output=True,text=True)
 if r.returncode or len(list(flat.iterdir()))>25: errors.append("flat build fail/cap")
if errors:
 print("VALIDATION: FAIL"); [print("-",e) for e in errors]; sys.exit(1)
print("VALIDATION: PASS")
print("canonical_sources:",len(SOURCES))
print("text_mutations: 0")
print("github_read_entries: 56")
print("github_write_entries: 41")
print("read_routes_write_clean: yes")
print("generic_routes_stack_clean: yes")
print("github_workflows: absent")
print("flat_files_max: 25")
