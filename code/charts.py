import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
PKG=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-trade-permits-brief-2026-11-07")
s=json.load(open(os.path.join(PKG,"stats.json")))
CHAR="#232323"; AMBER="#E8A33D"; TEAL="#2A9D8F"; GREY="#8A8A8A"
plt.rcParams.update({"font.family":"DejaVu Sans","text.color":CHAR,"axes.edgecolor":GREY,"axes.labelcolor":CHAR,"xtick.color":CHAR,"ytick.color":CHAR})
def save(fig,name):
    fig.savefig(os.path.join(PKG,"charts",name), dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig); print(name)
# 1 trade split
order=["Electrical","Gas/Mechanical","Plumbing"]
labels={"Electrical":"Electrical","Gas/Mechanical":"Gas / Mechanical","Plumbing":"Plumbing"}
fig,ax=plt.subplots(figsize=(7.2,3.8))
vals=[s["trade_counter"][t] for t in order]; shares=[s["trade_share_pct"][t] for t in order]
ax.barh([labels[t] for t in order][::-1], vals[::-1], color=[TEAL,AMBER,TEAL])
for i,(v,sh) in enumerate(zip(vals[::-1],shares[::-1])): ax.text(v+1200,i,f"{v:,} ({sh}%)",va="center",fontsize=10)
ax.set_xlabel("Trade permits entered 2023-10-12 to 2026-10-16 (n=111,321)")
ax.set_title("Nearly half of Nashville's trade permits are electrical",fontsize=12,weight="bold",loc="left")
ax.spines[["top","right"]].set_visible(False); ax.set_xlim(0,61000); save(fig,"chart_trades.png")
# 2 lag buckets
bk=["0","1","2-7","8-30","31-90","91+"]
bl={"0":"Same day","1":"1 day","2-7":"2-7 days","8-30":"8-30 days","31-90":"31-90 days","91+":"91+ days"}
fig,ax=plt.subplots(figsize=(7.2,4.2))
pcts=[s["lag_buckets"][k]["pct"] for k in bk]
ax.bar([bl[k] for k in bk],pcts,color=[AMBER]+[TEAL]*5)
for i,p in enumerate(pcts): ax.text(i,p+2,f"{p}%",ha="center",fontsize=10,weight="bold")
ax.set_ylabel("Share of dated trade permits (%)")
ax.set_title("87.1% of trade permits were issued the day they were entered\n(107,210 dated, non-negative gaps; median building-permit wait: 29 days)",fontsize=11,weight="bold",loc="left")
ax.spines[["top","right"]].set_visible(False); ax.set_ylim(0,97); save(fig,"chart_lag_buckets.png")
# 3 districts top 10
top=s["district_top10"][::-1]
fig,ax=plt.subplots(figsize=(7.2,4.6))
ax.barh([f"District {d['district']}" for d in top],[d["permits"] for d in top], color=[AMBER if d["district"]==19 else TEAL for d in top])
for i,d in enumerate(top): ax.text(d["permits"]+130,i,f"{d['permits']:,} ({d['share_pct']}%)",va="center",fontsize=9)
ax.set_xlabel("Trade permits by council district, 2023-10-12 to 2026-10-16\n(n=110,672 with a district; median district 3,037)")
ax.set_title("No district holds even 6% of Nashville's trade permits",fontsize=12,weight="bold",loc="left")
ax.spines[["top","right"]].set_visible(False); ax.set_xlim(0,7900); save(fig,"chart_districts_top10.png")
# 4 same-day share by permit kind
kinds=[("Full Electrical Permit",s["lag_by_subtype_top"]["Full Electrical Permit"]["same_day_pct"]),
("ELECT SERVICE RELEASE",s["lag_by_subtype_top"]["ELECT SERVICE RELEASE"]["same_day_pct"]),
("Plumbing Permit",s["lag_by_subtype_top"]["Plumbing Permit"]["same_day_pct"]),
("Gas / Mech Permit",s["lag_by_subtype_top"]["Gas / Mech Permit"]["same_day_pct"]),
("Gas / Mech Unit Change Out",s["lag_by_subtype_top"]["Gas / Mech Unit Change Out"]["same_day_pct"])]
labels2={"Full Electrical Permit":"Full electrical","ELECT SERVICE RELEASE":"Electrical service release","Plumbing Permit":"Plumbing","Gas / Mech Permit":"Gas / mechanical","Gas / Mech Unit Change Out":"Gas / mech unit change-out"}
fig,ax=plt.subplots(figsize=(7.2,4.2))
ks=kinds[::-1]
ax.barh([labels2[k[0]] for k in ks],[k[1] for k in ks],color=[GREY if "Change" in k[0] else TEAL for k in ks])
for i,k in enumerate(ks): ax.text(k[1]+1.5,i,f"{k[1]}%",va="center",fontsize=10,weight="bold")
ax.set_xlabel("Share issued the same day as entered (%)")
ax.set_title("Unit change-outs are the slow lane: 46.0% same-day,\nagainst 89-95% for the register's biggest kinds",fontsize=11,weight="bold",loc="left")
ax.spines[["top","right"]].set_visible(False); ax.set_xlim(0,108); save(fig,"chart_sameday_by_kind.png")
