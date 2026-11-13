"""Download posted results (adverse events, participant flow) and stop reasons.

Same sample filter as 03_psyexcl_download.py.
Outputs (one row per ...):
  03_psyexcl_status_raw.xlsx           trial (all 112k): why_stopped, allocation, masking
  03_psyexcl_results_groups_raw.xlsx   adverse-event group: deaths / serious / other counts
  03_psyexcl_results_psych_ae_raw.xlsx psychiatric adverse-event term x group (MedDRA SOC "Psychiatric disorders")
  03_psyexcl_results_arms_raw.xlsx     registered arm: label, type
  03_psyexcl_results_flow_raw.xlsx     trial: participants started / completed (participant flow)
"""
import time

import pandas as pd
import requests

URL = "https://clinicaltrials.gov/api/v2/studies"
BASE = (
    "AREA[StudyType]INTERVENTIONAL"
    " AND AREA[Phase](PHASE2 OR PHASE3 OR PHASE4)"
    " AND AREA[StartDate]RANGE[2010-01-01,2025-12-31]"
)


def fetch(filter_advanced, fields, page_size):
    token = None
    while True:
        params = {"filter.advanced": filter_advanced, "fields": fields, "pageSize": page_size}
        if token:
            params["pageToken"] = token
        for attempt in range(6):
            try:
                r = requests.get(URL, params=params, timeout=180)
                r.raise_for_status()
                break
            except Exception as e:
                print("retry", attempt, e, flush=True)
                time.sleep(5 * (attempt + 1))
        else:
            raise SystemExit("download failed")
        page = r.json()
        yield from page["studies"]
        token = page.get("nextPageToken")
        if not token:
            return


def num(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


# 1. Status for all trials
status_rows = []
for s in fetch(BASE, "NCTId,WhyStopped,DesignInfo", 1000):
    p = s["protocolSection"]
    di = p.get("designModule", {}).get("designInfo", {})
    status_rows.append({
        "nct_id": p["identificationModule"]["nctId"],
        "why_stopped": p.get("statusModule", {}).get("whyStopped"),
        "allocation": di.get("allocation"),
        "masking": di.get("maskingInfo", {}).get("masking"),
    })
    if len(status_rows) % 20000 == 0:
        print("status", len(status_rows), flush=True)
pd.DataFrame(status_rows).to_excel("03_psyexcl_status_raw.xlsx", index=False)
print("status done", len(status_rows), flush=True)

# 2. Results for trials with posted results
group_rows, psych_rows, arm_rows, flow_rows = [], [], [], []
fields = "NCTId,ArmsInterventionsModule,AdverseEventsModule,ParticipantFlowModule"
n = 0
for s in fetch(BASE + " AND AREA[HasResults]true", fields, 200):
    n += 1
    p = s["protocolSection"]
    nct = p["identificationModule"]["nctId"]
    for a in p.get("armsInterventionsModule", {}).get("armGroups", []):
        arm_rows.append({"nct_id": nct, "arm_label": a.get("label"), "arm_type": a.get("type")})
    r = s.get("resultsSection", {})
    ae = r.get("adverseEventsModule", {})
    for g in ae.get("eventGroups", []):
        group_rows.append({
            "nct_id": nct,
            "group_id": g.get("id"),
            "group_title": g.get("title"),
            "group_description": (g.get("description") or "")[:2000],
            "deaths_affected": g.get("deathsNumAffected"),
            "deaths_at_risk": g.get("deathsNumAtRisk"),
            "serious_affected": g.get("seriousNumAffected"),
            "serious_at_risk": g.get("seriousNumAtRisk"),
            "other_affected": g.get("otherNumAffected"),
            "other_at_risk": g.get("otherNumAtRisk"),
            "frequency_threshold": ae.get("frequencyThreshold"),
        })
    for kind, key in (("serious", "seriousEvents"), ("other", "otherEvents")):
        for ev in ae.get(key, []):
            if ev.get("organSystem") != "Psychiatric disorders":
                continue
            for st in ev.get("stats", []):
                psych_rows.append({
                    "nct_id": nct,
                    "group_id": st.get("groupId"),
                    "event_kind": kind,
                    "term": ev.get("term"),
                    "num_affected": st.get("numAffected"),
                    "num_at_risk": st.get("numAtRisk"),
                })
    periods = r.get("participantFlowModule", {}).get("periods", [])
    if periods:
        def total(period, mtype):
            for m in period.get("milestones", []):
                if m.get("type") == mtype:
                    vals = [num(a.get("numSubjects")) for a in m.get("achievements", [])]
                    return sum(v for v in vals if v is not None)
            return None
        flow_rows.append({
            "nct_id": nct,
            "flow_started": total(periods[0], "STARTED"),
            "flow_completed": total(periods[-1], "COMPLETED"),
        })
    if n % 2000 == 0:
        print("results", n, flush=True)

pd.DataFrame(group_rows).to_excel("03_psyexcl_results_groups_raw.xlsx", index=False)
pd.DataFrame(psych_rows).to_excel("03_psyexcl_results_psych_ae_raw.xlsx", index=False)
pd.DataFrame(arm_rows).to_excel("03_psyexcl_results_arms_raw.xlsx", index=False)
pd.DataFrame(flow_rows).to_excel("03_psyexcl_results_flow_raw.xlsx", index=False)
print("done", n, len(group_rows), len(psych_rows), len(arm_rows), len(flow_rows), flush=True)
