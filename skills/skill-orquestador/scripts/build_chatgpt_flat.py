#!/usr/bin/env python3
from __future__ import annotations
import argparse,shutil
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

def bundle(path,routes=None,profiles=None,files=None):
 items=[]
 for r in routes or []:
  secs,fs=resolve_route(r); items += [("section",x) for x in secs]+[("file",x) for x in fs]
 for p in profiles or []: items += [("section",x) for x in resolve_profile(p)]
 items += [("file",x) for x in (files or [])]
 seen=set(); items=[x for x in items if not (x in seen or seen.add(x))]
 with path.open("wb") as fh:
  for i,(kind,val) in enumerate(items):
   if i: fh.write(b"\n\n")
   fh.write((ROOT/val).read_bytes() if kind=="file" else section_bytes(val))
p=argparse.ArgumentParser(); p.add_argument("--output",default=str(ROOT/"dist/chatgpt-project-flat")); a=p.parse_args(); out=Path(a.output)
if out.exists(): shutil.rmtree(out)
out.mkdir(parents=True); shutil.copy2(ROOT/"SKILL.md",out/"00-SKILL.md")
bundle(out/"01-CORE-AND-POLICIES.md",files=MAN["alwaysFiles"])
for name,rs in {"02-PLANNING.md":["plan","audit","documentation","roadmap"],"03-ARCHITECTURE.md":["architecture","runtime","security"],"04-IMPLEMENTATION.md":["implement","validate"],"05-QUALITY-RELEASE.md":["release"],"06-GITHUB-READ.md":["github-read","issue-read"],"07-GITHUB-WRITE.md":["github-write","issue-write","branch-management"],"08-CI.md":["ci-inspect","ci-rerun"],"09-PR-REVIEW-MERGE.md":["pr-create","review-read","review-write","merge"],"10-RECOVERY.md":["recovery"],"11-MANAGEMENT.md":["delegation","management"],"12-PUBLISH.md":["publish"]}.items(): bundle(out/name,routes=rs)
for i,pf in enumerate(["typescript","node","electron","rust"],13): bundle(out/f"{i:02d}-PROFILE-{pf.upper()}.md",profiles=[pf])
shutil.copy2(ROOT/"catalogs/github-read-verbatim.md",out/"17-GITHUB-READ-VERBATIM.md"); shutil.copy2(ROOT/"catalogs/github-write-verbatim.md",out/"18-GITHUB-WRITE-VERBATIM.md")
bundle(out/"19-CONTRACTS.md",files=["contracts/authorization-envelope.schema.json","contracts/connector-contracts.md"]); shutil.copy2(ROOT/"templates/prompts.md",out/"20-TEMPLATES.md")
(out/"21-PROJECT-INSTRUCTIONS.txt").write_text("Use SKILL.md as the entrypoint. Load core and policies first. Select the smallest route and only the detected stack profile. GitHub remote operations use the connector; local git is local-only.\n")
if len(list(out.iterdir()))>25: raise SystemExit("flat package exceeds 25 files")
print(out); print("files:",len(list(out.iterdir())))
