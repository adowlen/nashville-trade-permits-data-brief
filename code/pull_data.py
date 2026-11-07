import urllib.request, urllib.parse, json, csv, os, collections, datetime
base="https://services2.arcgis.com/HdTo6HJqh92wn4D8/arcgis/rest/services/Trade_Permits_View/FeatureServer/0/query"
PKG=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-trade-permits-brief-2026-11-07")
outdir=os.path.join(PKG,"data")
rows=[]
offset=0
while True:
    params={"where":"1=1","outFields":"*","returnGeometry":"false","f":"json","resultOffset":offset,"resultRecordCount":1000,"orderByFields":"OBJECTID"}
    url=base+"?"+urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=120) as r: d=json.load(r)
    feats=d.get("features",[])
    for f in feats: rows.append(f["attributes"])
    print(offset, len(feats), d.get("exceededTransferLimit"))
    if not d.get("exceededTransferLimit"): break
    offset+=len(feats)
fields=list(rows[0].keys())
with open(os.path.join(outdir,"trade_permits_raw.csv"),"w",newline="") as fh:
    w=csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
with open(os.path.join(outdir,"pull_log.json"),"w") as fh: json.dump({"rows":len(rows),"source":base,"snapshot_date":"2026-11-06"},fh,indent=2)
print("total",len(rows))
for col in ["Trade","Permit_Type_Description","Permit_Subtype_Description","Case_Status","Per_Type","Per_SubType","City","State"]:
    c=collections.Counter(str(r.get(col)) for r in rows)
    print("\n==",col)
    for k,v in c.most_common(40): print(repr(k),v)
def ts(v):
    return datetime.datetime.utcfromtimestamp(v/1000).date().isoformat() if v else None
entered=[r["Date_Entered"] for r in rows if r.get("Date_Entered")]
issued=[r["Date_Issued"] for r in rows if r.get("Date_Issued")]
print("\nentered range", ts(min(entered)), ts(max(entered)), "n",len(entered))
print("issued range", ts(min(issued)), ts(max(issued)), "n",len(issued))
print("council values", collections.Counter(str(r.get("Council_Dist")) for r in rows).most_common(45))
cv=[r["Contract_Value"] for r in rows if r.get("Contract_Value") is not None]
print("contract_value: n_nonnull",len(cv),"zero",sum(1 for x in cv if x==0),"negative",sum(1 for x in cv if x<0),"max",max(cv) if cv else None)
