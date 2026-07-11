#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
errors=[]
required=[
 "policies/gpt-5.6-sol.md",
 "models/gpt-5.6-sol.json",
 "templates/gpt-5.6-prompt-contract.md",
 "evals/gpt-5.6-sol.json",
 "references/gpt-5.6-sol-prompting-guidance.md",
]
for rel in required:
 if not (ROOT/rel).is_file(): errors.append("missing "+rel)
if not errors:
 model=json.loads((ROOT/"models/gpt-5.6-sol.json").read_text())
 if model.get("id")!="gpt-5.6-sol": errors.append("wrong model id")
 integrity=model.get("integrity",{})
 checks={"referenceSha256":"references/gpt-5.6-sol-prompting-guidance.md","policySha256":"policies/gpt-5.6-sol.md","promptTemplateSha256":"templates/gpt-5.6-prompt-contract.md","evalSha256":"evals/gpt-5.6-sol.json"}
 for key,rel in checks.items():
  if integrity.get(key)!=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(): errors.append("model integrity mismatch "+rel)
 if model.get("prompt",{}).get("structure")!=["role","personality","goal","successCriteria","constraints","tools","output","stopRules"]: errors.append("prompt structure mismatch")
 if model.get("tools",{}).get("programmaticCalling",{}).get("allowedStage")!="bounded-record-reduction": errors.append("PTC boundary missing")
 if model.get("retrieval",{}).get("meaningfulFallbacksMax") not in (1,2): errors.append("fallback budget invalid")
 if model.get("reasoning",{}).get("migrationBaseline")!="preserve-current-setting": errors.append("reasoning baseline missing")
 evals=json.loads((ROOT/"evals/gpt-5.6-sol.json").read_text())
 ids=[x["id"] for x in evals.get("cases",[])]
 if len(ids)<12 or len(ids)!=len(set(ids)): errors.append("eval inventory invalid")
 required_ids={"review-no-mutation","fix-local-autonomy","explicit-external-write","github-connector-only","ptc-bounded-reduction","citation-grounding","frontend-render-check","reasoning-migration","completion-stop"}
 if not required_ids.issubset(ids): errors.append("required eval cases missing")
 policy=(ROOT/"policies/gpt-5.6-sol.md").read_text()
 markers=["## Outcome contract","## Autonomy and approval","## Tool routing","## Retrieval and evidence budget","## Long-running work and state","## Reasoning and verbosity","## Validation","## Stop rules","## Migration discipline"]
 for marker in markers:
  if marker not in policy: errors.append("policy marker missing "+marker)
 template=(ROOT/"templates/gpt-5.6-prompt-contract.md").read_text()
 for marker in ["Role:","Personality:","Goal:","Success criteria:","Constraints:","Tools:","Output:","Stop rules:"]:
  if marker not in template: errors.append("template marker missing "+marker)
 reference=(ROOT/"references/gpt-5.6-sol-prompting-guidance.md").read_text()
 for marker in ["Simplify prompts first","Programmatic Tool Calling","Grounding, citations, and retrieval budgets","Prompt migration workflow"]:
  if marker not in reference: errors.append("reference marker missing "+marker)
 if hashlib.sha256(reference.encode()).hexdigest()==hashlib.sha256(policy.encode()).hexdigest(): errors.append("reference and operational policy must be separate")
if errors:
 print("GPT56 VALIDATION: FAIL")
 for error in errors: print("-",error)
 sys.exit(1)
print("GPT56 VALIDATION: PASS")
print("model_profile: gpt-5.6-sol")
print("eval_cases:",len(json.loads((ROOT/"evals/gpt-5.6-sol.json").read_text())["cases"]))
