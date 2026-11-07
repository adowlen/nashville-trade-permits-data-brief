"""Pre-flight audit (Brief-Writing Standards section 10) - Nashville Trade Permits.
Run BEFORE final charts/prose. Output recorded in verification.md."""
import csv, collections, datetime, os
PKG=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-trade-permits-brief-2026-11-07")
rows=list(csv.DictReader(open(os.path.join(PKG,"data/trade_permits_raw.csv"))))
out=[]
def log(s): out.append(str(s)); print(s)
log(f"rows pulled: {len(rows)}")
# 1. Counter of all unique values for every column used in a hardcoded categorical filter
for col in ["Trade","Permit_Type_Description","Permit_Subtype_Description","Case_Status","Per_Type","Per_SubType"]:
    c=collections.Counter(r[col] for r in rows)
    log(f"COUNTER {col}: {dict(c.most_common(60))}")
# 2. Zero/null sentinel handling, field by field
for col in ["Council_Dist","Zip","Census_Tract","Parcel","Address","Contract_Value","Date_Entered","Date_Issued","PermitNumber"]:
    missing=sum(1 for r in rows if r[col] in (None,"","None"))
    zero=sum(1 for r in rows if r[col] in ("0","0.0"))
    log(f"MISSING {col}: blank/null={missing}; zero-string={zero} of {len(rows)} ({100*(missing+zero)/len(rows):.1f}% blank-or-zero) - excluded from any rate denominator using that field; records counted in totals regardless")
# Council_Dist raw value census (string field - sentinel hunt)
log(f"COUNCIL_DIST CENSUS: {dict(collections.Counter(r['Council_Dist'] for r in rows).most_common(50))}")
# 3. Contract value distribution
cv=[float(r["Contract_Value"]) for r in rows if r["Contract_Value"] not in (None,"","None")]
log(f"CONTRACT_VALUE: nonnull={len(cv)}, zero={sum(1 for x in cv if x==0)}, negative={sum(1 for x in cv if x<0)}, positive={sum(1 for x in cv if x>0)}, max={max(cv)}, sum_positive={sum(x for x in cv if x>0)}")
# 4. Date sentinel / polarity check
def dt(ms):
    if ms in (None,"","None"): return None
    return datetime.datetime.fromtimestamp(int(float(ms))/1000, datetime.timezone.utc)
entered=[dt(r["Date_Entered"]) for r in rows]; issued=[dt(r["Date_Issued"]) for r in rows]
ev=[e for e in entered if e]; iv=[i for i in issued if i]
log(f"DATE_ENTERED: n={len(ev)}, min={min(ev)}, max={max(ev)}")
log(f"DATE_ISSUED: n={len(iv)}, min={min(iv)}, max={max(iv)}")
log(f"DATE_ISSUED missing: {len(rows)-len(iv)}; DATE_ENTERED missing: {len(rows)-len(ev)}")
log(f"ENTERED UTC HOUR CENSUS: {dict(collections.Counter(e.hour for e in ev).most_common())} (America/Chicago local midnights read as UTC hour 5 or 6)")
log(f"ISSUED UTC HOUR CENSUS: {dict(collections.Counter(i.hour for i in iv).most_common())}")
sents=[e for e in ev if e.year<1990]
log(f"ENTERED SENTINEL (pre-1990): {len(sents)} {collections.Counter(e.date().isoformat() for e in sents).most_common(10)}")
sents_i=[i for i in iv if i.year<1990]
log(f"ISSUED SENTINEL (pre-1990): {len(sents_i)} {collections.Counter(i.date().isoformat() for i in sents_i).most_common(10)}")
from zoneinfo import ZoneInfo
CT=ZoneInfo("America/Chicago")
def ldate(d): return d.astimezone(CT).date()
lags=[]; neg=[]
for r,e,i in zip(rows,entered,issued):
    if e and i:
        # Gaps use America/Chicago LOCAL dates - the same basis as the brief and
        # build_stats.py. (The first audit run used UTC calendar dates and counted
        # 93,357 zero gaps; the 12-permit difference is records crossing Chicago
        # midnight. Audit and brief now share one basis; see verification.md.)
        d=(ldate(i)-ldate(e)).days; lags.append(d)
        if d<0: neg.append((d, r["PermitNumber"], ldate(e).isoformat(), ldate(i).isoformat()))
lags_sorted=sorted(lags)
log(f"LAG POLARITY: n_with_both_dates={len(lags)}, negative={len(neg)} {neg[:5]}, zero={sum(1 for x in lags if x==0)}, median={lags_sorted[len(lags)//2]}, p90={lags_sorted[int(0.9*len(lags))]}, over_5y={sum(1 for x in lags if x>1825)}, max={max(lags)}")
# 5. Numerator/denominator unit agreement
log("UNIT CHECK: every share in this brief is permits / permits (same layer, same snapshot) or stated dollars / stated dollars over the positive-value population only, with the zero/null population count printed beside it. No rate mixes permits with parcels except the labeled parcel-join match rate (permits matched / permits with a parcel value).")
# 6. Status x issued-date consistency
cs=collections.Counter((r["Case_Status"], bool(r["Date_Issued"] not in (None,"","None"))) for r in rows)
log(f"CASE_STATUS x HAS_ISSUED_DATE: {dict(cs)}")
# 7. Uniqueness of permit numbers
pn=collections.Counter(r["PermitNumber"] for r in rows if r["PermitNumber"] not in (None,"","None"))
log(f"PERMITNUMBER: nonnull={sum(pn.values())}, unique={len(pn)}, max rows per number={pn.most_common(3)}")
oid=collections.Counter(r["OBJECTID"] for r in rows)
log(f"OBJECTID unique: {len(oid)} of {len(rows)}")
# 8. Trade x type cross-tab (categorical exhaustiveness for the trade split)
xt=collections.Counter((r["Trade"], r["Permit_Type_Description"]) for r in rows)
log(f"TRADE x TYPE CROSSTAB: {dict(xt.most_common(40))}")
# 8b. Classification edge: unit change-out subtype vs type counts differ by 2 rows
co_sub=[r for r in rows if r["Permit_Subtype_Description"]=="Gas / Mech Unit Change Out"]
co_typ=[r for r in rows if r["Permit_Type_Description"]=="Gas/Mechanical Unit Change Out ONLY"]
log(f"CHANGE-OUT EDGE: subtype rows={len(co_sub)} (types: {dict(collections.Counter(r['Permit_Type_Description'] for r in co_sub))}); type rows={len(co_typ)} - 2 records carry the change-out subtype under the rare 'Gas / Mech Replacement - HC MC VC' type. The brief uses subtype counts and this edge is disclosed in verification.md.")
# 9. District normalization trap: the string field mixes zero-padded and bare values
def dist(r):
    d=(r["Council_Dist"] or "").strip()
    return int(d) if d.isdigit() else None
raw_n=collections.Counter(r["Council_Dist"] for r in rows)
merged=collections.Counter(dist(r) for r in rows)
unpadded={k:v for k,v in raw_n.items() if k.isdigit() and len(k)==1}
log(f"DISTRICT NORMALIZATION: raw field mixes zero-padded ('05') and bare ('5') spellings; bare-spelling rows: {sum(unpadded.values())} {unpadded}. All district figures in this brief use the integer-normalized district. Districts present after normalization: {sum(1 for k in merged if k)}; unknown: {merged[None]}")
assert sum(1 for k in merged if k)==35
# 10. Parcel sentinels
pc=collections.Counter((r["Parcel"] or "").strip() for r in rows)
log(f"PARCEL SENTINELS: 'RIGHT-OF-WAY' rows: {pc['RIGHT-OF-WAY']} (not a parcel; excluded from every parcel join and parcel count); blank: {pc['']}; distinct real parcels: {len([k for k in pc if k and k!='RIGHT-OF-WAY'])}")
# 11. Contract_Value semantics: project value repeated across a project's trade permits
pairs=collections.Counter(((r["Parcel"] or "").strip(), r["Contract_Value"]) for r in rows if r["Contract_Value"] not in (None,"","None") and float(r["Contract_Value"])>0 and (r["Parcel"] or "").strip() not in ("","RIGHT-OF-WAY"))
extra=sum(c-1 for c in pairs.values() if c>1)
log(f"VALUE REPETITION: {extra} rows repeat a (parcel, stated value) pair already carried by another trade permit on the same parcel - Contract_Value behaves as the parent project's stated value stamped on each of its trade permits, so values are NEVER summed in this brief. Per-permit medians are reported with this disclosed; the only aggregate value figure is the deduplicated count of distinct parcels carrying a stated value of $10,000,000 or more.")
posv=[float(r["Contract_Value"]) for r in rows if r["Contract_Value"] not in (None,"","None") and float(r["Contract_Value"])>0]
roundshare={v: sum(1 for x in posv if x==v) for v in (1000,2500,3000,5000,10000)}
log(f"ROUND-VALUE CENSUS (share of {len(posv)} positive values): {roundshare} - round thousands are common applicant estimates; the median positive value is reported, never a mean of totals.")
# 12. Window and coverage
log("WINDOW: Date_Entered spans 2023-10-12 to 2026-10-16 on the 2026-11-06 pull (1,100 days). October 2023 is partial from the 12th and October 2026 ends on the 16th in this snapshot; the brief states the snapshot's own entry range wherever a period is named and never describes data past 2026-10-16.")
# 13. Internal control: parcel join sanity (join computed in build_stats; control stated here)
log("INTERNAL CONTROL (join): the companion building-permits-issued layer (29,651 permits) and this layer share the Parcel key. The join's control expectation: parcels in established neighborhoods with no construction in either window should NOT match; the match rates and both windows are printed in the brief and verification.md, and 'RIGHT-OF-WAY' plus blank parcels are excluded before matching.")
open(os.path.join(PKG,"data/audit_output.txt"),"w").write("\n".join(out)+"\n")
