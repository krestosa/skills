#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SHARED=ROOT/'shared'
p=argparse.ArgumentParser(); p.add_argument('--output',default=str(ROOT/'dist/chatgpt-project-flat')); a=p.parse_args(); out=Path(a.output)
if out.exists(): shutil.rmtree(out)
out.mkdir(parents=True)
shutil.copy2(ROOT/'SKILL.md',out/'00-MAIN.md'); shutil.copy2(ROOT/'orchestrator/SKILL.md',out/'01-ORCHESTRATOR.md')
for i,path in enumerate(sorted((ROOT/'skills').glob('*/SKILL.md')),2): shutil.copy2(path,out/f'{i:02d}-SKILL-{path.parent.name.upper()}.md')
# Shared bundles stay unique and below the 25-file project limit.
def bundle(target,paths):
 with target.open('wb') as fh:
  for p in paths: fh.write(p.read_bytes()+b'\n\n')
bundle(out/'16-SHARED-POLICIES.md',[SHARED/'policies/gpt-5.6-sol.md',SHARED/'policies/repository-context-and-authorization.md',SHARED/'policies/network-and-transport.md',SHARED/'policies/github-write-safety.md',SHARED/'policies/connector-native-integrity.md'])
shutil.copy2(SHARED/'catalogs/github-read-verbatim.md',out/'17-GITHUB-READ-VERBATIM.md'); shutil.copy2(SHARED/'catalogs/github-write-verbatim.md',out/'18-GITHUB-WRITE-VERBATIM.md')
bundle(out/'19-SHARED-CONTRACTS.md',[SHARED/'contracts/authorization-envelope.schema.json',SHARED/'contracts/connector-contracts.md'])
bundle(out/'20-GPT56.md',[SHARED/'models/gpt-5.6-sol.json',SHARED/'templates/gpt-5.6-prompt-contract.md'])
(out/'21-PROJECT-INSTRUCTIONS.txt').write_text('Load 00-MAIN.md, then 01-ORCHESTRATOR.md. The orchestrator selects only the required individual skill files. Remote GitHub operations use the connector; local git is local-only.\n',encoding='utf-8')
if len(list(out.iterdir()))>25: raise SystemExit('flat package exceeds 25 files')
print(out); print('files:',len(list(out.iterdir())))
