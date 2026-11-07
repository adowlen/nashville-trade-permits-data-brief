"""Independent verifier: recomputes headline figures from the raw CSV with pandas
(a second implementation, no shared code with build_stats.py) and cross-checks the
live ArcGIS service with server-side aggregates. Compares against stats.json."""
import json, os, urllib.request, urllib.parse
import pandas as pd
PKG=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-trade-permits-brief-2026-11-07")
S=json.load(open(os.path.join(PKG,"stats.json")))
df=pd.read_csv(os.path.join(PKG,"data/trade_permits_raw.csv"), dtype={"Council_Dist":str,"Zip":str,"Parcel":str}, low_memory=False)
checks={}
def eq(name, mine, theirs): checks[name]={"mine":mine,"stats_json":theirs,"pass":bool(mine==theirs)}
# row + trade counts
eq("rows_111321", len(df), S["rows"])
tc=df["Trade"].value_counts().to_dict()
eq("electrical_52534", int(tc["Electrical"]), S["trade_counter"]["Electrical"])
eq("plumbing_27469", int(tc["Plumbing"]), S["trade_counter"]["Plumbing"])
eq("gas_mech_31318", int(tc["Gas/Mechanical"]), S["trade_counter"]["Gas/Mechanical"])
# local dates via pandas tz conversion (UTC epochs -> America/Chicago)
for c in ["Date_Entered","Date_Issued"]:
    df[c+"_local"]=pd.to_datetime(df[c], unit="ms", utc=True).dt.tz_convert("America/Chicago").dt.date
df["lag"]=(pd.to_datetime(df["Date_Issued_local"])-pd.to_datetime(df["Date_Entered_local"])).dt.days
dated=df.dropna(subset=["lag"])
nonneg=dated[dated["lag"]>=0]
eq("dated_107213", len(dated), S["lag"]["n_both_dates"])
eq("negative_3", int((dated["lag"]<0).sum()), S["lag"]["negative_n"])
sd=int((nonneg["lag"]==0).sum())
eq("same_day_93345", sd, S["lag"]["same_day_n"])
eq("same_day_pct_87_1", round(100*sd/len(nonneg),1), S["lag"]["same_day_pct"])
eq("median_lag_0", float(nonneg["lag"].median()), float(S["lag"]["median_days"]))
eq("median_positive_lag_2", float(nonneg[nonneg["lag"]>0]["lag"].median()), float(S["lag"]["median_days_if_positive"]))
for t in ["Electrical","Plumbing","Gas/Mechanical"]:
    sub=nonneg[df.loc[nonneg.index,"Trade"]==t]
    eq(f"sameday_{t}", round(100*(sub['lag']==0).mean(),1), S["lag_by_trade"][t]["same_day_pct"])
# districts: normalize the string field independently
dnum=pd.to_numeric(df["Council_Dist"].str.strip(), errors="coerce")
vc=dnum.value_counts()
eq("district19_6565", int(vc.get(19,0)), S["district_top10"][0]["permits"])
eq("district_top_share_5_9", round(100*vc.get(19,0)/dnum.notna().sum(),1), S["district_top10"][0]["share_pct"])
eq("districts_35", int(dnum.nunique()), S["districts_present"])
eq("median_district_3037", float(vc.median()), float(S["median_district_permits"]))
# electrical service family
FAM=["ELECT SERVICE RELEASE","ELECT OUTAGE AND RECONNECT","ELECT EMERGENCY RECONNECT","ELECT SERVICE RECONNECT"]
elec=df[df["Trade"]=="Electrical"]
eq("service_family_22701", int(elec["Permit_Subtype_Description"].isin(FAM).sum()), S["electrical_service_family"]["n"])
eq("service_family_pct_43_2", round(100*elec["Permit_Subtype_Description"].isin(FAM).mean(),1), S["electrical_service_family"]["pct_of_electrical"])
# value medians (never sums)
pos=df[df["Contract_Value"]>0]["Contract_Value"]
eq("value_positive_104497", len(pos), S["value"]["positive_n"])
eq("median_value_6841", float(pos.median()), float(S["value"]["median_positive"]))
# megaproject parcels, deduplicated
big=df[(df["Contract_Value"]>=10_000_000) & (df["Parcel"].str.strip()!="RIGHT-OF-WAY") & (df["Parcel"].notna())]
eq("megaproject_parcels_141", int(big["Parcel"].str.strip().nunique()), S["megaproject_parcels"]["distinct_parcels"])
bd=pd.to_numeric(big.drop_duplicates("Parcel")["Council_Dist"].str.strip(), errors="coerce")
eq("megaproject_d19_117", int((bd==19).sum()), S["megaproject_parcels"]["in_district19"])
# entered by full years
ey=pd.to_datetime(df["Date_Entered_local"]).dt.year.value_counts().to_dict()
eq("entered_2024_37164", int(ey.get(2024,0)), S["entered_by_year"]["2024"])
eq("entered_2025_35083", int(ey.get(2025,0)), S["entered_by_year"]["2025"])
# server-side live aggregates (drift check against the live service)
base="https://services2.arcgis.com/HdTo6HJqh92wn4D8/arcgis/rest/services/Trade_Permits_View/FeatureServer/0/query"
def q(params):
    with urllib.request.urlopen(base+"?"+urllib.parse.urlencode(params), timeout=60) as r: return json.load(r)
live=q({"where":"1=1","returnCountOnly":"true","f":"json"})["count"]
checks["live_count_matches_pull"]={"mine":live,"stats_json":S["rows"],"pass":bool(live==S["rows"])}
grp=q({"where":"1=1","groupByFieldsForStatistics":"Trade","outStatistics":json.dumps([{"statisticType":"count","onStatisticField":"OBJECTID","outStatisticFieldName":"n"}]),"f":"json"})
live_trades={f["attributes"]["Trade"]:f["attributes"]["n"] for f in grp["features"]}
checks["live_trade_counts_match"]={"mine":live_trades,"stats_json":S["trade_counter"],"pass":bool(live_trades==S["trade_counter"])}
ok=sum(1 for v in checks.values() if v["pass"])
print(json.dumps(checks,indent=1,default=str)); print("PASS" if ok==len(checks) else "FAIL", f"{ok}/{len(checks)}")
json.dump(checks, open(os.path.join(PKG,"data/verify_independent_output.json"),"w"), indent=1, default=str)
