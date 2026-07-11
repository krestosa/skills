#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'shared'; errors=[]
required=['policies/gpt-5.6-sol.md','models/gpt-5.6-sol.json','templates/gpt-5.6-prompt-contract.md','evals/gpt-5.6-sol.json','references/gpt-5.6-sol-prompting-guidance.md']
for rel in required:
 if not (ROOT/rel).is_file(): errors.append('missing '+rel)
if not errors:
 model=json.loads((ROOT/'models/gpt-5.6-sol.json').read_text()); integrity=model.get('integrity',{})
 checks={'referenceSha256':'references/gpt-5.6-sol-prompting-guidance.md','policySha256':'policies/gpt-5.6-sol.md','promptTemplateSha256':'templates/gpt-5.6-prompt-contract.md','evalSha256':'evals/gpt-5.6-sol.json'}
 if model.get('id')!='gpt-5.6-sol': errors.append('wrong model id')
 for key,rel in checks.items():
  if integrity.get(key)!=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(): errors.append('model integrity mismatch '+rel)
 if model.get('prompt',{}).get('structure')!=['role','personality','goal','successCriteria','constraints','tools','output','stopRules']: errors.append('prompt structure mismatch')
 evals=json.loads((ROOT/'evals/gpt-5.6-sol.json').read_text()); ids=[x['id'] for x in evals.get('cases',[])]
 if len(ids)<12 or len(ids)!=len(set(ids)): errors.append('eval inventory invalid')
if errors:
 print('GPT56 VALIDATION: FAIL'); [print('-',x) for x in errors]; sys.exit(1)
print('GPT56 VALIDATION: PASS')
print('model_profile: gpt-5.6-sol')
