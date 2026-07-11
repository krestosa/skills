#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SHARED=ROOT/"shared"
INTEGRITY=SHARED/"manifests/integrity.json"
errors=[]

def load(path):
    try:return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:errors.append(f"invalid json {path.relative_to(ROOT)}: {exc}");return {}

def require(path):
    if not path.is_file():errors.append("missing "+path.relative_to(ROOT).as_posix())

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

required=[
ROOT/"README.md",ROOT/"SKILL.md",ROOT/"orchestrator/SKILL.md",ROOT/"orchestrator/registry.json",
ROOT/"orchestrator/delegation-envelope.schema.json",ROOT/"scripts/build_chatgpt_flat.py",
ROOT/"scripts/build_compiled.py",ROOT/"scripts/validate_gpt56.py",ROOT/"scripts/verify_lossless.py",
SHARED/"manifests/routes.json",SHARED/"manifests/source-index.json",
SHARED/"evals/parallel-execution.json",SHARED/"evals/local-git-workspace.json",
SHARED/"references/parallel-execution-policy-verbatim.md"]
for p in required:require(p)

if sorted(ROOT.rglob("README.md"))!=[ROOT/"README.md"]:errors.append("expected one root README.md")
for p in ["skills/main","skills/orchestrator","skills/individual","skills/skill-orquestador"]:
    if (ROOT/p).exists():errors.append("legacy layer exists: "+p)
if (ROOT/".github/workflows").exists():errors.append("GitHub workflows are prohibited")

main=(ROOT/"SKILL.md").read_text(encoding="utf-8")
orch=(ROOT/"orchestrator/SKILL.md").read_text(encoding="utf-8")
if "orchestrator/SKILL.md" not in main:errors.append("main does not load orchestrator")
if re.search(r"skills/[a-z0-9-]+/SKILL\.md",main):errors.append("main loads individual skill")
for marker in ["Select one primary skill","Do not load all skills preemptively","Attach `local-git-workspace`","Attach `parallel-execution`","Cross-cutting auto-attached skills do not count"]:
    if marker not in orch:errors.append("orchestrator missing "+marker)

routes=load(SHARED/"manifests/routes.json").get("routes",{})
registry=load(ROOT/"orchestrator/registry.json")
skills=registry.get("skills",[])
ids=[x.get("id") for x in skills]
if len(ids)!=16 or len(ids)!=len(set(ids)):errors.append("expected 16 unique skills")
for item in skills:
    sid=item.get("id"); path=ROOT/f"skills/{sid}/SKILL.md"
    if item.get("skillFile")!=f"skills/{sid}/SKILL.md":errors.append(sid+" path mismatch")
    require(path); text=path.read_text(encoding="utf-8",errors="ignore") if path.is_file() else ""
    for h in ["## Role","## Personality","## Collaboration style","## Goal","## Success criteria","## Select when","## Exclude when","## Shared routes","## Output","## Stop rules"]:
        if h not in text:errors.append(f"{sid} missing {h}")
    for route in item.get("requiredRoutes",[])+item.get("optionalRoutes",[]):
        if route not in routes:errors.append(f"{sid} unknown route {route}")
    for dep in item.get("dependencies",[]):
        if dep not in ids:errors.append(f"{sid} unknown dependency {dep}")
    if not item.get("loadPolicy",{}).get("onDemand"):errors.append(sid+" not on-demand")

selection=registry.get("selectionPolicy",{})
if selection.get("crossCuttingSkillIds")!=["parallel-execution","local-git-workspace"]:errors.append("cross-cutting registry mismatch")
if not selection.get("ordinaryActiveSkillTarget",{}).get("excludesCrossCutting"):errors.append("cross-cutting target mismatch")

parallel=next((x for x in skills if x.get("id")=="parallel-execution"),{})
pa=selection.get("autoAttach",{}).get("parallel-execution",{})
if parallel.get("role")!="cross-cutting" or any(parallel.get("capabilities",{}).values()):errors.append("parallel capability boundary")
if parallel.get("requiredRoutes") or parallel.get("optionalRoutes"):errors.append("parallel routes must be empty")
if not parallel.get("loadPolicy",{}).get("autoAttachWhenApplicable") or pa.get("default")!="attach-when-applicable":errors.append("parallel auto-attach mismatch")
parallel_ref=SHARED/"references/parallel-execution-policy-verbatim.md"
if digest(parallel_ref)!="804cc93be433bf159a7ac57d0778fbb72806c8306940343657079e8aa5db8126" or len(parallel_ref.read_bytes())!=12903:errors.append("parallel reference mismatch")

local=next((x for x in skills if x.get("id")=="local-git-workspace"),{})
la=selection.get("autoAttach",{}).get("local-git-workspace",{})
if local.get("role")!="cross-cutting":errors.append("local Git role mismatch")
if local.get("capabilities")!={"remoteReads":False,"remoteWrites":False,"localWrites":True}:errors.append("local Git capability boundary")
if local.get("requiredRoutes") or local.get("optionalRoutes"):errors.append("local Git routes must be empty")
for key in ["autoAttachWhenApplicable","runBeforeFirstLocalGitCommand","onePreflightPerWorkspace"]:
    if not local.get("loadPolicy",{}).get(key):errors.append("local Git load policy "+key)
for key in ["requiresRootRuntime","runBeforeFirstLocalGitCommand","onePreflightPerWorkspace","prohibitsSafeDirectoryFallback","authorizedLocalMetadataRepairOnly","doesNotAuthorizeRemoteWrites","doesNotCountTowardOrdinaryActiveSkillTarget"]:
    if not la.get(key):errors.append("local Git auto-attach "+key)
if la.get("default")!="attach-before-local-git":errors.append("local Git attach default")
if la.get("ownershipCommand")!='sudo -n chown -R "$(id -u):$(id -g)" -- "$repo_root"':errors.append("ownership command mismatch")
if la.get("rootFallbackWhenSudoUnavailable")!='chown -R "$(id -u):$(id -g)" -- "$repo_root"':errors.append("ownership fallback mismatch")

local_text=(ROOT/"skills/local-git-workspace/SKILL.md").read_text(encoding="utf-8")
for marker in ["realpath -e",'sudo -n chown -R "$(id -u):$(id -g)" -- "$repo_root"',"ROOT_RUNTIME_REQUIRED","LOCAL_GIT_OWNERSHIP_REPAIR_FAILED","git config --global --add safe.directory","exclusive metadata lock","Remote GitHub access remains connector-only"]:
    if marker not in local_text:errors.append("local Git skill missing "+marker)

parallel_cases=load(SHARED/"evals/parallel-execution.json").get("cases",[])
local_cases=load(SHARED/"evals/local-git-workspace.json").get("cases",[])
if len({x.get("id") for x in parallel_cases})<10:errors.append("parallel eval coverage")
if len({x.get("id") for x in local_cases})<10:errors.append("local Git eval coverage")

def catalog(path):
    data=path.read_bytes();b=b"<!-- VERBATIM_CATALOG_BEGIN -->\n";e=b"<!-- VERBATIM_CATALOG_END -->\n"
    return data[data.index(b)+len(b):data.index(e)].rstrip(b"\n")
for rel,count,sha in [("catalogs/github-read-verbatim.md",56,"610c387f5f7c9047c65fef08734d5199696230866ca79e270700209eaab1324e"),("catalogs/github-write-verbatim.md",41,"499373638143f48b0549701bf5036725a2c2bc9b332a95d9a053a1e1ce687a3d")]:
    p=SHARED/rel;require(p)
    if p.is_file():
        data=catalog(p)
        if hashlib.sha256(data).hexdigest()!=sha or len([x for x in data.decode().split("\n\n") if x.strip()])!=count:errors.append(rel+" mismatch")

for script,label in [(ROOT/"scripts/verify_lossless.py","lossless"),(ROOT/"scripts/validate_gpt56.py","GPT-5.6")]:
    r=subprocess.run([sys.executable,str(script)],cwd=ROOT,text=True,capture_output=True)
    if r.returncode:errors.append(label+" validation failed:\n"+r.stdout+r.stderr)

active="\n".join([main,orch]+[(ROOT/x["skillFile"]).read_text(encoding="utf-8") for x in skills])
if "Remote GitHub operations use the GitHub connector" not in active:errors.append("connector boundary missing")
if re.search(r"(?m)^\s*(git\s+(clone|fetch|pull|push|ls-remote)|gh\s+(api|repo|pr|issue|run|workflow|release|search))\b",active):errors.append("remote git/gh command in active hierarchy")

static={
"README.md","SKILL.md","orchestrator/SKILL.md","orchestrator/registry.json","orchestrator/delegation-envelope.schema.json",
"scripts/build_chatgpt_flat.py","scripts/build_compiled.py","scripts/validate.py","scripts/validate_gpt56.py","scripts/verify_lossless.py",
"shared/catalogs/github-read-verbatim.md","shared/catalogs/github-write-verbatim.md",
"shared/contracts/authorization-envelope.schema.json","shared/contracts/connector-contracts.md",
"shared/core/identity.md","shared/core/project-authority-and-roles.md","shared/core/states-and-approval.md",
"shared/evals/gpt-5.6-sol.json","shared/evals/parallel-execution.json","shared/evals/local-git-workspace.json",
"shared/manifests/routes.json","shared/manifests/source-index.json","shared/models/gpt-5.6-sol.json",
"shared/policies/connector-native-integrity.md","shared/policies/github-write-safety.md","shared/policies/gpt-5.6-sol.md",
"shared/policies/network-and-transport.md","shared/policies/repository-context-and-authorization.md",
"shared/profiles/electron.json","shared/profiles/generic.json","shared/profiles/node.json","shared/profiles/rust.json","shared/profiles/typescript.json",
"shared/references/gpt-5.6-sol-prompting-guidance.md","shared/references/parallel-execution-policy-verbatim.md",
"shared/templates/gpt-5.6-prompt-contract.md","shared/templates/prompts.md"}
expected=static|{x["skillFile"] for x in skills}
for item in load(SHARED/"manifests/source-index.json").get("sources",[]):
    mp="shared/"+item["path"];expected.add(mp);m=load(ROOT/mp)
    if m.get("path"):expected.add("shared/"+m["path"])
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and p!=INTEGRITY and "dist" not in p.parts and "__pycache__" not in p.parts and ".git" not in p.parts}
if actual!=expected:
    if expected-actual:errors.append("inventory missing: "+", ".join(sorted(expected-actual)))
    if actual-expected:errors.append("inventory extra: "+", ".join(sorted(actual-expected)))

integrity=load(INTEGRITY); inventory_text="\n".join(sorted(expected))+"\n"
if integrity.get("inventory",{}).get("count")!=len(expected) or integrity.get("inventory",{}).get("sha256")!=hashlib.sha256(inventory_text.encode()).hexdigest():errors.append("integrity inventory mismatch")
if integrity.get("individualSkillCount")!=16 or integrity.get("crossCuttingSkillCount")!=2:errors.append("integrity skill counts")
lg=integrity.get("localGitWorkspace",{})
for key in ["autoAttachBeforeLocalGit","requiresRootRuntime","prohibitsSafeDirectoryFallback"]:
    if not lg.get(key):errors.append("integrity local Git "+key)
for item in integrity.get("protectedFiles",[]):
    p=ROOT/item["path"];require(p)
    if p.is_file() and (digest(p)!=item["sha256"] or len(p.read_bytes())!=item["bytes"]):errors.append("protected file mismatch "+item["path"])

with tempfile.TemporaryDirectory() as td:
    a=Path(td)/"a.md";b=Path(td)/"b.md"
    for out in [a,b]:
        r=subprocess.run([sys.executable,str(ROOT/"scripts/build_compiled.py"),"--output",str(out)],cwd=ROOT,text=True,capture_output=True)
        if r.returncode:errors.append("compiled build failed: "+r.stdout+r.stderr)
    if a.exists() and b.exists() and a.read_bytes()!=b.read_bytes():errors.append("compiled build nondeterministic")
    flat=Path(td)/"flat";r=subprocess.run([sys.executable,str(ROOT/"scripts/build_chatgpt_flat.py"),"--output",str(flat)],cwd=ROOT,text=True,capture_output=True)
    if r.returncode:errors.append("flat build failed: "+r.stdout+r.stderr)
    elif len(list(flat.iterdir()))>25:errors.append("flat build exceeds 25 files")

if errors:
    print("VALIDATION: FAIL")
    for e in errors:print("-",e)
    raise SystemExit(1)
print("VALIDATION: PASS")
print("individual_skills:",len(ids))
print("cross_cutting_skills: 2")
print("local_git_workspace: preflight-before-local-git")
print("parallel_execution: auto-attach-when-applicable")
print("canonical_sources: 15 lossless")
print("github_read_entries: 56")
print("github_write_entries: 41")
print("github_remote: connector-only")
print("github_workflows: absent")
