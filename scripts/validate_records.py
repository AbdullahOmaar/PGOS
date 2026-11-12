#!/usr/bin/env python3
"""Validate PGOS JSON governance records without third-party dependencies.

This is a structural/preflight validator, not an identity provider, signature
verifier, authorization gateway, or proof that an approval is genuine.
"""
from __future__ import annotations
import argparse, json, re, sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

VALID_RISK_TIERS = {"LOW", "MODERATE", "HIGH", "CRITICAL"}
VALID_DATA_CLASSES = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"}
AUTONOMY_LEVELS = {"A0": 0, "A1": 1, "A2": 2, "A3": 3, "A4": 4}
HIGH_IMPACT_ACTIONS = {"merge_to_default", "production_deploy", "production_write", "destructive_migration", "sensitive_data_export", "financial_side_effect", "legal_side_effect", "paid_provisioning", "external_communication"}
REQUIRED = {
 "Project": ("id","name","revision","status","owner","problem","outcomes","scope","non_goals","risk_tier","data_classes","canonical_sources"),
 "WorkOrder": ("id","project_id","revision","title","status","objective","scope","non_goals","owner_id","assignee","permission","acceptance_criteria","verification_plan","risk_tier"),
 "Decision": ("id","project_id","revision","title","status","context","options","decision","rationale","owner_id","approver_ids"),
 "Risk": ("id","project_id","title","description","likelihood","impact","inherent_score","mitigations","owner_id","status"),
 "Evidence": ("id","project_id","work_order_id","criterion_ids","exact_revision","environment","scope","procedure","result","producer_id","timestamp"),
 "Release": ("id","project_id","work_order_ids","status","exact_revision","environment","checks","rollback_plan","release_authority_id"),
}
def _dt(v):
 try: datetime.fromisoformat(v.replace("Z","+00:00")); return isinstance(v,str) and bool(v.strip())
 except (ValueError,AttributeError): return False
def _date(v):
 try: date.fromisoformat(v); return isinstance(v,str) and bool(v.strip())
 except (ValueError,TypeError): return False
def validate_record(record: Any, path="<memory>") -> list[str]:
 e=[]
 if not isinstance(record,dict): return [f"{path}: record must be a JSON object"]
 t=record.get("record_type")
 if t not in REQUIRED: return [f"{path}: unsupported or missing record_type: {t!r}"]
 for f in REQUIRED[t]:
  if f not in record or record[f] is None or record[f]=="": e.append(f"{path}: missing or empty required field '{f}'")
 if e: return e
 if not isinstance(record.get("revision",1),int) or record.get("revision",1)<1: e.append(f"{path}: revision must be a positive integer")
 if not isinstance(record.get("id"),str) or not re.match(r"^[A-Z][A-Z0-9-]{2,63}$",record["id"]): e.append(f"{path}: id must be an immutable uppercase identifier")
 if record.get("risk_tier") is not None and record.get("risk_tier") not in VALID_RISK_TIERS: e.append(f"{path}: invalid risk_tier")
 if t=="Project":
  o=record.get("owner")
  if not isinstance(o,dict) or not o.get("id") or not isinstance(o.get("verified"),bool): e.append(f"{path}: owner must include id and boolean verified")
  if not isinstance(record.get("outcomes"),list) or not record["outcomes"]: e.append(f"{path}: outcomes must be a non-empty array")
  if not isinstance(record.get("scope"),list) or not record["scope"]: e.append(f"{path}: scope must be a non-empty array")
  if not isinstance(record.get("non_goals"),list): e.append(f"{path}: non_goals must be an array")
  if not isinstance(record.get("data_classes"),list) or any(x not in VALID_DATA_CLASSES for x in record["data_classes"]): e.append(f"{path}: data_classes contains an unsupported class")
  s=record.get("canonical_sources")
  if not isinstance(s,dict) or not all(k in s and isinstance(s[k],str) and s[k].strip() for k in ("notion","linear","github","runtime")): e.append(f"{path}: canonical_sources must define notion, linear, github and runtime")
  if "created_at" in record and not _dt(record["created_at"]): e.append(f"{path}: created_at must be ISO-8601 datetime")
  if "review_date" in record and not _date(record["review_date"]): e.append(f"{path}: review_date must be YYYY-MM-DD")
 elif t=="WorkOrder":
  a=record.get("assignee")
  if not isinstance(a,dict) or not a.get("id") or not isinstance(a.get("verified"),bool): e.append(f"{path}: assignee must include id and boolean verified")
  p=record.get("permission")
  if not isinstance(p,dict): e.append(f"{path}: permission must be an object")
  else:
   level=p.get("level"); actions=p.get("actions",[])
   if level not in AUTONOMY_LEVELS: e.append(f"{path}: permission.level must be A0-A4")
   if not isinstance(actions,list) or any(not isinstance(x,str) for x in actions): e.append(f"{path}: permission.actions must be strings"); actions=[]
   if any(x in HIGH_IMPACT_ACTIONS for x in actions) and AUTONOMY_LEVELS.get(level,-1)<4: e.append(f"{path}: high-impact action requires A4 and action-specific approval")
   if level=="A4" and (not p.get("approval_ref") or p.get("approval_ref")=="NOT_REQUIRED_FOR_A1"): e.append(f"{path}: A4 requires approval_ref")
   if not p.get("environment"): e.append(f"{path}: permission.environment is required")
   if not actions: e.append(f"{path}: permission.actions must be non-empty")
   if not isinstance(p.get("resources"),list) or not p["resources"]: e.append(f"{path}: permission.resources must be non-empty")
   exp=p.get("expires_at")
   if not _dt(exp): e.append(f"{path}: permission.expires_at must be ISO-8601 datetime")
   else:
    x=datetime.fromisoformat(exp.replace("Z","+00:00"))
    if x.tzinfo is None: x=x.replace(tzinfo=timezone.utc)
    if x<=datetime.now(timezone.utc): e.append(f"{path}: permission has expired")
  c=record.get("acceptance_criteria")
  if not isinstance(c,list) or not c: e.append(f"{path}: acceptance_criteria must be non-empty")
  else:
   for i,x in enumerate(c):
    if not isinstance(x,dict) or not all(x.get(k) for k in ("id","given","when","then","evidence_required")): e.append(f"{path}: acceptance_criteria[{i}] is incomplete")
  if record.get("status")=="APPROVED" and (not record.get("approval_ref") or not isinstance(a,dict) or a.get("verified") is not True): e.append(f"{path}: APPROVED WorkOrder requires approval_ref and verified assignee")
 elif t=="Decision":
  if record.get("status")=="APPROVED" and (not record.get("decision") or not isinstance(record.get("approver_ids"),list) or not record["approver_ids"]): e.append(f"{path}: APPROVED Decision requires decision and approver")
  if record.get("effective_at") is not None and not _dt(record["effective_at"]): e.append(f"{path}: effective_at must be ISO-8601 datetime or null")
 elif t=="Risk":
  l,i=record.get("likelihood"),record.get("impact")
  if not isinstance(l,int) or not 1<=l<=5: e.append(f"{path}: likelihood must be 1..5")
  if not isinstance(i,int) or not 1<=i<=5: e.append(f"{path}: impact must be 1..5")
  if isinstance(l,int) and isinstance(i,int) and record.get("inherent_score")!=l*i: e.append(f"{path}: inherent_score must equal likelihood × impact")
  r=record.get("residual_score")
  if r is not None and (not isinstance(r,int) or not 1<=r<=25): e.append(f"{path}: residual_score must be 1..25")
 elif t=="Evidence":
  if record.get("result") not in {"PASS","FAIL","NOT_RUN","STALE","UNKNOWN"}: e.append(f"{path}: invalid evidence result")
  if not isinstance(record.get("criterion_ids"),list) or not record["criterion_ids"]: e.append(f"{path}: criterion_ids must be non-empty")
  if not _dt(record.get("timestamp")): e.append(f"{path}: timestamp must be ISO-8601")
  if not isinstance(record.get("exact_revision"),str) or not record["exact_revision"].strip(): e.append(f"{path}: exact_revision is required")
 elif t=="Release":
  if record.get("status") not in {"NOT_READY","READY_FOR_APPROVAL","APPROVED","DEPLOYING","DEPLOYED","LIVE_VERIFIED","ROLLED_BACK","FAILED"}: e.append(f"{path}: unsupported release status")
  if record.get("status") in {"APPROVED","DEPLOYING","DEPLOYED","LIVE_VERIFIED"} and not record.get("approval_ref"): e.append(f"{path}: release status requires approval_ref")
  if record.get("status")=="LIVE_VERIFIED" and (not record.get("deployment_receipt") or not record.get("live_verification")): e.append(f"{path}: LIVE_VERIFIED requires deployment receipt and verification")
  if not isinstance(record.get("checks"),list): e.append(f"{path}: checks must be an array")
 return e
def validate_directory(directory: Path):
 errors=[]; records=[]; files=sorted(directory.rglob("*.json"))
 if not files: return [f"{directory}: no JSON records found"],0
 for p in files:
  try: r=json.loads(p.read_text(encoding="utf-8"))
  except (OSError,json.JSONDecodeError) as ex: errors.append(f"{p}: invalid JSON: {ex}"); continue
  errors.extend(validate_record(r,str(p)))
  if isinstance(r,dict): records.append((p,r))
 seen={}
 for p,r in records:
  rid=r.get("id")
  if isinstance(rid,str):
   if rid in seen: errors.append(f"{p}: duplicate id '{rid}' also exists in {seen[rid]}")
   else: seen[rid]=p
 projects={r.get("id") for _,r in records if r.get("record_type")=="Project"}
 wos={r.get("id"):r for _,r in records if r.get("record_type")=="WorkOrder"}
 for p,r in records:
  t=r.get("record_type"); pid=r.get("project_id")
  if t in {"WorkOrder","Decision","Risk","Evidence","Release"} and pid not in projects: errors.append(f"{p}: project_id '{pid}' does not resolve to a Project")
  if t=="Evidence":
   wo=wos.get(r.get("work_order_id"))
   if wo is None: errors.append(f"{p}: work_order_id '{r.get('work_order_id')}' does not resolve")
   elif wo.get("project_id")!=pid: errors.append(f"{p}: Evidence and WorkOrder belong to different projects")
  if t=="Release":
   for wid in r.get("work_order_ids",[]):
    wo=wos.get(wid)
    if wo is None: errors.append(f"{p}: release WorkOrder '{wid}' does not resolve")
    elif wo.get("project_id")!=pid: errors.append(f"{p}: Release and WorkOrder belong to different projects")
 return errors,len(files)
def main():
 p=argparse.ArgumentParser(description="Validate PGOS JSON governance records"); p.add_argument("directory",type=Path); a=p.parse_args()
 if not a.directory.exists() or not a.directory.is_dir(): print(f"ERROR: directory does not exist: {a.directory}",file=sys.stderr); return 2
 errors,n=validate_directory(a.directory)
 if errors:
  print(f"PGOS validation FAILED: {len(errors)} finding(s) across {n} file(s)")
  for x in errors: print(f"- {x}")
  return 1
 print(f"PGOS validation PASSED: {n} JSON file(s); structural and cross-reference checks only")
 print("NOTE: this does not verify human identity, approval authenticity, provider settings or runtime behavior.")
 return 0
if __name__=="__main__": raise SystemExit(main())
