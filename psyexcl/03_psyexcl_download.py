"""Download raw trial records from the ClinicalTrials.gov API v2.

Sample: interventional, phase 2/3/4, start date 2010-01-01 to 2025-12-31.
Output: 03_psyexcl_raw.xlsx (one row per trial), 03_psyexcl_raw.jsonl (full API records).
"""
import json
import time

import pandas as pd
import requests

URL = "https://clinicaltrials.gov/api/v2/studies"
FILTER = (
    "AREA[StudyType]INTERVENTIONAL"
    " AND AREA[Phase](PHASE2 OR PHASE3 OR PHASE4)"
    " AND AREA[StartDate]RANGE[2010-01-01,2025-12-31]"
)
FIELDS = ",".join([
    "NCTId", "BriefTitle", "Phase", "StartDate", "OverallStatus",
    "LeadSponsorClass", "EnrollmentCount", "HealthyVolunteers",
    "MinimumAge", "MaximumAge", "EligibilityCriteria",
    "LocationCountry", "ConditionBrowseModule", "Condition",
])

records = []
token = None
while True:
    params = {"filter.advanced": FILTER, "fields": FIELDS, "pageSize": 1000}
    if token:
        params["pageToken"] = token
    for attempt in range(5):
        try:
            r = requests.get(URL, params=params, timeout=120)
            r.raise_for_status()
            break
        except Exception as e:
            print("retry", attempt, e, flush=True)
            time.sleep(5 * (attempt + 1))
    else:
        raise SystemExit("download failed")
    page = r.json()
    records.extend(page["studies"])
    print(len(records), flush=True)
    token = page.get("nextPageToken")
    if not token:
        break

with open("03_psyexcl_raw.jsonl", "w") as f:
    for s in records:
        f.write(json.dumps(s) + "\n")

rows = []
for s in records:
    p = s.get("protocolSection", {})
    cb = s.get("derivedSection", {}).get("conditionBrowseModule", {})
    countries = sorted({loc.get("country") for loc in p.get("contactsLocationsModule", {}).get("locations", []) if loc.get("country")})
    rows.append({
        "nct_id": p.get("identificationModule", {}).get("nctId"),
        "brief_title": p.get("identificationModule", {}).get("briefTitle"),
        "phases": "|".join(p.get("designModule", {}).get("phases", [])),
        "start_date": p.get("statusModule", {}).get("startDateStruct", {}).get("date"),
        "overall_status": p.get("statusModule", {}).get("overallStatus"),
        "lead_sponsor_class": p.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("class"),
        "enrollment": p.get("designModule", {}).get("enrollmentInfo", {}).get("count"),
        "healthy_volunteers": p.get("eligibilityModule", {}).get("healthyVolunteers"),
        "minimum_age": p.get("eligibilityModule", {}).get("minimumAge"),
        "maximum_age": p.get("eligibilityModule", {}).get("maximumAge"),
        "conditions": "|".join(p.get("conditionsModule", {}).get("conditions", [])),
        "mesh_terms": "|".join(m["term"] for m in cb.get("meshes", [])),
        "mesh_ancestors": "|".join(m["term"] for m in cb.get("ancestors", [])),
        "countries": "|".join(countries),
        "eligibility_criteria": p.get("eligibilityModule", {}).get("eligibilityCriteria"),
    })

df = pd.DataFrame(rows)
# Excel cell limit is 32,767 characters; flag and truncate the rare longer texts
df["eligibility_truncated"] = df["eligibility_criteria"].fillna("").str.len() > 32000
df["eligibility_criteria"] = df["eligibility_criteria"].fillna("").str.slice(0, 32000)
df.to_excel("03_psyexcl_raw.xlsx", index=False)
print("done", len(df), "truncated:", int(df["eligibility_truncated"].sum()))
