import csv, json, collections, statistics, datetime, os
from zoneinfo import ZoneInfo
PKG=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-trade-permits-brief-2026-11-07")
rows=list(csv.DictReader(open(os.path.join(PKG,"data/trade_permits_raw.csv"))))
CT=ZoneInfo("America/Chicago")
def ld(ms):
    if ms in (None,"","None"): return None
    return datetime.datetime.fromtimestamp(int(float(ms))/1000, datetime.timezone.utc).astimezone(CT).date()
for r in rows:
    r["_e"]=ld(r["Date_Entered"]); r["_i"]=ld(r["Date_Issued"])
    r["_lag"]=(r["_i"]-r["_e"]).days if r["_e"] and r["_i"] else None
    d=(r["Council_Dist"] or "").strip()
    r["_d"]=int(d) if d.isdigit() else None
    r["_cv"]=float(r["Contract_Value"]) if r["Contract_Value"] not in (None,"","None") else None
def med(xs): return statistics.median(xs) if xs else None
def pct(a,b): return round(100*a/b,1) if b else None
S={}
S["dataset"]="Nashville Trade Permits (Trade_Permits_View, layer 0, hubNashville / Metro Nashville open data)"
S["snapshot_date"]="2026-11-06"
S["rows"]=len(rows)
S["unit"]="one row = one trade permit record as served by the view; the view's own entry dates span 2023-10-12 to 2026-10-16 (1,101 days inclusive) on the 2026-11-06 pull"
S["entered_range"]=["2023-10-12","2026-10-16"]
S["trade_counter"]=dict(collections.Counter(r["Trade"] for r in rows))
S["trade_share_pct"]={k:pct(v,len(rows)) for k,v in S["trade_counter"].items()}
S["type_counter"]=dict(collections.Counter(r["Permit_Type_Description"] for r in rows))
S["subtype_counter"]=dict(collections.Counter(r["Permit_Subtype_Description"] for r in rows))
S["status_counter"]=dict(collections.Counter(r["Case_Status"] for r in rows))
S["with_issued_date"]=sum(1 for r in rows if r["_i"])
S["without_issued_date_by_status"]=dict(collections.Counter(r["Case_Status"] for r in rows if not r["_i"]))
# lag (Chicago local dates; negative lags excluded from lag stats, counted)
dated=[r for r in rows if r["_lag"] is not None]
nonneg=[r["_lag"] for r in dated if r["_lag"]>=0]
S["lag"]={"n_both_dates":len(dated),"negative_n":sum(1 for r in dated if r["_lag"]<0),"n_nonneg":len(nonneg),
 "same_day_n":sum(1 for x in nonneg if x==0),"same_day_pct":pct(sum(1 for x in nonneg if x==0),len(nonneg)),
 "median_days":med(nonneg),"median_days_if_positive":med([x for x in nonneg if x>0]),"p90_days":sorted(nonneg)[int(0.9*len(nonneg))],"max_days":max(nonneg)}
buckets=collections.Counter()
for x in nonneg:
    buckets["0" if x==0 else "1" if x==1 else "2-7" if x<=7 else "8-30" if x<=30 else "31-90" if x<=90 else "91+"]+=1
S["lag_buckets"]={k:{"n":buckets.get(k,0),"pct":pct(buckets.get(k,0),len(nonneg))} for k in ["0","1","2-7","8-30","31-90","91+"]}
def lag_block(sub):
    xs=[r["_lag"] for r in sub if r["_lag"] is not None and r["_lag"]>=0]
    return {"n":len(xs),"same_day_pct":pct(sum(1 for x in xs if x==0),len(xs)),"median_days":med(xs),"max_days":max(xs) if xs else None}
S["lag_by_trade"]={t:lag_block([r for r in rows if r["Trade"]==t]) for t in S["trade_counter"]}
S["lag_by_subtype_top"]={st:lag_block([r for r in rows if r["Permit_Subtype_Description"]==st]) for st in S["subtype_counter"]}
S["lag_by_entered_year"]={str(y):lag_block([r for r in rows if r["_e"] and r["_e"].year==y]) for y in (2024,2025,2026)}
# entries by year/month
ey=collections.Counter(r["_e"].year for r in rows if r["_e"])
S["entered_by_year"]=dict(sorted(ey.items()))
S["entered_per_day_full_years"]={str(y):round(ey[y]/365.25) for y in (2024,2025)}
S["entered_per_day_window"]=round(len(rows)/1101)
# electrical service family
FAM=["ELECT SERVICE RELEASE","ELECT OUTAGE AND RECONNECT","ELECT EMERGENCY RECONNECT","ELECT SERVICE RECONNECT"]
elec=[r for r in rows if r["Trade"]=="Electrical"]
fam=[r for r in elec if r["Permit_Subtype_Description"] in FAM]
S["electrical_service_family"]={"n":len(fam),"of_electrical":len(elec),"pct_of_electrical":pct(len(fam),len(elec)),
  "by_subtype":dict(collections.Counter(r["Permit_Subtype_Description"] for r in fam)),
  "full_electrical_n":sum(1 for r in elec if r["Permit_Subtype_Description"]=="Full Electrical Permit"),
  "temp_service_n":sum(1 for r in elec if r["Permit_Subtype_Description"]=="Temporary Elec Service")}
# districts (integer-normalized)
dn=collections.Counter(r["_d"] for r in rows if r["_d"])
known=sum(dn.values())
S["district_known_rows"]=known; S["district_unknown_rows"]=len(rows)-known
S["district_top10"]=[{"district":k,"permits":v,"share_pct":pct(v,known)} for k,v in dn.most_common(10)]
S["district_bottom5"]=[{"district":k,"permits":v} for k,v in dn.most_common()[-5:]]
S["districts_present"]=len(dn)
S["median_district_permits"]=statistics.median(list(dn.values()))
S["top_district_share_pct"]=pct(dn.most_common(1)[0][1],known)
S["top_to_median_ratio"]=round(dn.most_common(1)[0][1]/statistics.median(list(dn.values())),1)
# value discipline: medians only, never sums (see audit section 11)
pos=[r["_cv"] for r in rows if r["_cv"] and r["_cv"]>0]
S["value"]={"positive_n":len(pos),"positive_pct":pct(len(pos),len(rows)),"zero_n":sum(1 for r in rows if r["_cv"]==0),"null_n":sum(1 for r in rows if r["_cv"] is None),
 "median_positive":med(pos),"exactly_5000_n":sum(1 for x in pos if x==5000),"note":"Contract_Value repeats the parent project's stated value across that project's trade permits (19,625 rows repeat a (parcel, value) pair); values are never summed in this brief"}
S["value_by_trade"]={}
for t in S["trade_counter"]:
    pv=[r["_cv"] for r in rows if r["Trade"]==t and r["_cv"] and r["_cv"]>0]
    S["value_by_trade"][t]={"rows":S["trade_counter"][t],"positive_n":len(pv),"positive_pct":pct(len(pv),S["trade_counter"][t]),"median_positive":med(pv)}
big={}
for r in rows:
    p=(r["Parcel"] or "").strip()
    if p and p!="RIGHT-OF-WAY" and r["_cv"] and r["_cv"]>=10_000_000: big.setdefault(p,r["_d"])
S["megaproject_parcels"]={"threshold":10_000_000,"distinct_parcels":len(big),"in_district19":sum(1 for v in big.values() if v==19),
 "pct_in_district19":pct(sum(1 for v in big.values() if v==19),len(big)),
 "permits_carrying_10m_plus":sum(1 for r in rows if r["_cv"] and r["_cv"]>=10_000_000),
 "permits_carrying_10m_plus_real_parcels":sum(1 for r in rows if r["_cv"] and r["_cv"]>=10_000_000 and (r["Parcel"] or "").strip() not in ("","RIGHT-OF-WAY")),
 "by_district_top":collections.Counter(big.values()).most_common(6)}
# parcels
pc=collections.Counter((r["Parcel"] or "").strip() for r in rows)
S["parcels"]={"rows_with_parcel_field":len(rows),"right_of_way_rows":pc["RIGHT-OF-WAY"],
 "distinct_real_parcels":len([k for k in pc if k and k!="RIGHT-OF-WAY"]),
 "parcels_with_2plus_permits":sum(1 for k,v in pc.items() if v>=2 and k not in ("","RIGHT-OF-WAY"))}
S["parcel_join"]=json.load(open(os.path.join(PKG,"data/parcel_join_summary.json")))
S["service_family_detail"]=json.load(open(os.path.join(PKG,"data/service_family_detail.json")))
# ZIP top
zc=collections.Counter(r["Zip"] for r in rows if r["Zip"])
S["zip_top10"]=[{"zip":k,"permits":v,"share_pct":pct(v,len(rows))} for k,v in zc.most_common(10)]
# comparison anchors (companion briefs, cited in sources.md)
S["comparison"]={"building_permits_issued_rows":29651,"building_median_wait_days":29,
 "building_window":"issue dates 2023-10-30 to 2026-11-02, layer from the Machine Readable brief of 2026-11-03",
 "trade_to_building_ratio":round(len(rows)/29651,2)}
json.dump(S, open(os.path.join(PKG,"stats.json"),"w"), indent=2, default=str)
# panels
with open(os.path.join(PKG,"data/district_panel.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["district","permits","share_of_district_known_pct","median_stated_value_positive","permits_with_positive_value"])
    for k in sorted(dn):
        sub=[r for r in rows if r["_d"]==k]; pv=[r["_cv"] for r in sub if r["_cv"] and r["_cv"]>0]
        w.writerow([k,dn[k],pct(dn[k],known),med(pv),len(pv)])
with open(os.path.join(PKG,"data/trade_panel.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["trade","permits","share_pct","same_day_pct","median_lag_days","median_stated_value_positive"])
    for t in S["trade_counter"]:
        w.writerow([t,S["trade_counter"][t],S["trade_share_pct"][t],S["lag_by_trade"][t]["same_day_pct"],S["lag_by_trade"][t]["median_days"],S["value_by_trade"][t]["median_positive"]])
with open(os.path.join(PKG,"data/lag_panel.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["bucket_days","n","pct_of_dated_nonneg"])
    for k,v in S["lag_buckets"].items(): w.writerow([k,v["n"],v["pct"]])
with open(os.path.join(PKG,"data/subtype_panel.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["subtype","permits","permits_dated_nonneg","same_day_pct","median_lag_days"])
    for st,v in S["lag_by_subtype_top"].items(): w.writerow([st,S["subtype_counter"][st],v["n"],v["same_day_pct"],v["median_days"]])
with open(os.path.join(PKG,"data/zip_panel.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["zip","permits","share_pct"])
    for z in S["zip_top10"]: w.writerow([z["zip"],z["permits"],z["share_pct"]])
print(json.dumps({k:S[k] for k in ["rows","trade_counter","lag","district_top10","megaproject_parcels","electrical_service_family"]},indent=1,default=str)[:2600])
