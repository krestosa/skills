#!/usr/bin/env python3
from __future__ import annotations
import argparse
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

p=argparse.ArgumentParser(); p.add_argument("--routes",nargs="*",default=list(MAN["routes"])); p.add_argument("--profiles",nargs="*",default=[MAN["defaultProfile"]]); p.add_argument("--output",default=str(ROOT/"dist/skill-orquestador.compiled.md")); a=p.parse_args()
items=[("file","SKILL.md")]+[("file",x) for x in MAN["alwaysFiles"]]
for r in a.routes:
 secs,files=resolve_route(r); items += [("section",x) for x in secs]+[("file",x) for x in files]
for prof in a.profiles: items += [("section",x) for x in resolve_profile(prof)]
seen=set(); out=[]
for item in items:
 if item not in seen: seen.add(item); out.append(item)
t=Path(a.output); t.parent.mkdir(parents=True,exist_ok=True)
with t.open("wb") as fh:
 for i,(kind,val) in enumerate(out):
  if i: fh.write(b"\n\n")
  fh.write((ROOT/val).read_bytes() if kind=="file" else section_bytes(val))
print(t)
