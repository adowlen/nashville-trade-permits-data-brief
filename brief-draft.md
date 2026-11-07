# Nashville's trade permits are the same-day counter

**One-line summary:** Of the 111,321 trade permits entered in Metro Nashville between October 12, 2023 and October 16, 2026, 107,213 carry an issuance date, and 87.1 percent of those were issued the same day they were entered, while the median building permit in the companion register waited 29 days.

Start with one day at the counter. In 2024, Metro Nashville's trade permit counter took in 37,164 permits, about 102 a day: the wiring, plumbing, and heating and cooling work that follows building projects and keeps existing buildings running. Almost none of them waited. This brief measures the trade side of Nashville's permit system, the third register in this series alongside the building permits issued (November 3, 2026) and the building permit applications still pending (November 4, 2026). Its permits clear faster than the building register's, and no district holds even 6 percent of them.

Machine Readable pulled the full Nashville Trade Permits view on November 6, 2026: 111,321 records whose entry dates run from October 12, 2023 to October 16, 2026 (1,101 days). The view is Metro's trade permitting record as served on the snapshot date; entry dates in the snapshot end on October 16, 2026, so no figure below describes permits entered after that date. One record is one trade permit. A single construction project normally generates several of them.

## The same-day counter

- 107,213 of the 111,321 records carry both an entered date and an issued date. Of the 107,210 with a non-negative gap, 93,345 (87.1 percent) were issued the same day they were entered, 6,373 (5.9 percent) the next day, and 5,245 (4.9 percent) within two to seven days. Only 588 dated permits (0.5 percent) took more than 30 days. The longest gap is 443 days. Three records carry an issued date before their entered date and are excluded from the gap figures.
- The median gap among permits that took at least a day is 2 days. The same-day share is stable across the window: 87.0 percent for permits entered in 2024, 87.1 percent in 2025, and 86.9 percent in 2026.
- By trade, plumbing issues the same day most often (92.6 percent of dated permits), then electrical (89.1 percent), then gas and mechanical (78.7 percent).
- The comparison figure from the companion register: among the 29,651 building permits issued in the three years to November 2, 2026, the median entry-to-issuance wait was 29 days. The two registers define their populations differently (the trade figures here cover every dated record in the trade view; the building figure covers permits that issued).

One permit kind is the exception at scale. Gas and mechanical unit change-outs, the permits that replace an existing furnace or air conditioner, were issued the same day only 46.0 percent of the time (7,523 dated permits), with a median gap of 1 day and a maximum of 178 days. The other slow lanes are the reconnection classes: electrical service reconnects cleared the same day 62.9 percent of the time (669 dated permits) and outage and reconnect permits 71.6 percent (4,728 dated permits). Every other kind with at least 1,000 dated permits clears between 86.6 and 99.5 percent the same day. The slowest kinds of all are tiny: the 143 dated photovoltaic permits carry a median gap of 13 to 15 days.

## Three trades, and two in five electrical permits are service-connection events

- Electrical is the largest trade: 52,534 permits (47.2 percent). Gas and mechanical follows with 31,318 (28.1 percent), then plumbing with 27,469 (24.7 percent). For every building permit issued in the companion register's window, about 3.8 trade permits were entered in this one (derived; the two windows are stated above and differ by a few weeks at each end).
- Inside electrical, the single largest kind is the full electrical permit (26,385). But 22,701 electrical permits (43.2 percent) are service-connection events rather than wiring permits: 14,064 service releases, 4,904 outage and reconnect permits, 2,863 emergency reconnects, and 870 service reconnects. The two halves of that family point in different directions, measured by the parcel join in this brief: 76.1 percent of service releases sit on a parcel that also holds an issued building permit in the companion window, level with the full electrical permits themselves (78.9 percent), and 45.6 percent of their purpose statements (a crude text count, in the package's data folder) contain the word "new". The reconnect classes sit on a building-permit parcel only 9.4 to 35.5 percent of the time, and their purpose statements describe repairs such as replacing damaged service wiring and meter centers. Temporary electrical service, the construction-site power permit, adds 3,144 more, 85.5 percent of them on building-permit parcels.
- Gas and mechanical carries its own existing-stock lane: 8,065 unit change-out permits (25.7 percent of the trade). Plumbing is the most uniform trade: 27,422 of its 27,469 permits (99.8 percent) carry the single generic subtype "Plumbing Permit."

## Spread across every district

Trade permit volume spreads across the whole county.

- District 19 (downtown) holds the most trade permits, 6,565, which is 5.9 percent of the 110,672 permits with a district. District 2 holds 5,935 (5.4 percent) and District 5 holds 5,712 (5.2 percent). The median district holds 3,037 permits, so the largest district holds 2.2 times the median. All 35 council districts appear; the smallest, District 29, holds 801.
- The contrast inside the same permit system: in the beer register published November 6, 2026, one district held 22.2 percent of issued permits, 11.4 times its median district. That register counts issued permits only, while this one counts every record it served; on dated records only, District 19's trade share is the same 5.9 percent, so the difference in populations does not move the contrast.
- By ZIP code, the leaders sit away from downtown: 37207 holds 10,625 permits (9.5 percent), 37209 holds 9,406 (8.4 percent), and 37013 holds 8,396 (7.5 percent). Downtown's 37203 is fourth with 6,944 (6.2 percent).
- Council district is missing on 649 records (0.6 percent), counted in the totals and excluded from district shares. The register's district field mixes zero-padded and bare spellings (for example "05" and "5"); every district figure in this brief uses the normalized district number.

## Where the large projects are

Permit counts are flat; the largest projects are not. The register's Contract_Value field carries a positive stated dollar value on 104,497 records (93.9 percent). The layer's metadata does not say whether that value is the trade's own contract value or the parent project's, but in the records it behaves as the project's: 19,625 records with a positive value on a real parcel repeat a value already carried by another trade permit on the same parcel, and one project in District 25 carries the same $53,809,905 statement on at least six electrical permits. So this brief never adds Contract_Value up, and no dollar total or dollar share appears in it.

Deduplicated by parcel, the footprint is measurable: 141 distinct parcels carry at least one trade permit stating a project value of $10 million or more, and 117 of the 141 (83.0 percent) are in District 19. In total 1,113 trade permits on real parcels carry a stated value of $10 million or more. The typical single permit states far less: the median positive value is $6,841 overall, $5,000 for electrical and plumbing permits, and $10,605 for gas and mechanical permits. Values are applicant-stated, and round numbers are common: 8.2 percent of positive values are exactly $5,000. A further 6,822 records (6.1 percent) state a value of zero and 2 state none; both groups are excluded from every value figure.

## The link back to building permits

The two registers share the parcel number, so the trade layer can be joined to the building permits issued layer from the November 3, 2026 brief (29,651 permits). The join excludes 626 trade records whose parcel field reads "RIGHT-OF-WAY" rather than a parcel number.

- Of the 110,695 trade permits carrying a real parcel number, 75,463 (68.2 percent) sit on a parcel that also holds an issued building permit in the companion layer.
- Counting parcels instead of permits: the trade layer touches 34,728 distinct parcels, the building layer 20,851, and 15,341 parcels appear in both. That is 44.2 percent of trade parcels and 73.6 percent of building parcels.
- The two windows differ (trade entries run October 12, 2023 to October 16, 2026; building issues run October 30, 2023 to November 2, 2026), so a trade permit can predate or follow its parcel's building permit outside either window. The match rates describe the overlap of the two snapshots, not a completion rate for building projects.
- Most trade parcels are repeat customers: 20,281 of the 34,728 (58.4 percent) hold two or more trade permits in the window.

## The status column, reported as recorded

The view's Case_Status field reads DONE on 81,662 records (73.4 percent), ISSUED on 19,278 (17.3 percent), EXPIRED on 6,640, CANCELLED on 2,351, and REJECTED on 674, with the remaining 716 records spread across six smaller values. A total of 4,108 records (3.7 percent) carry no issued date, including all 674 REJECTED records and 2,693 of the EXPIRED ones. The layer's public metadata does not define its status values, so this brief reports them as recorded and draws no conclusion from the DONE and ISSUED split.

## What this might mean

One possible reading is that Nashville's trade permitting is, in the main, a high-throughput service counter for the whole city: the volume is spread across every district, the connection classes split between following permitted construction (the releases, three in four landing on a building-permit parcel) and servicing addresses with no building permit in the window (the reconnects), and the counter clears the same day nearly nine times in ten. On that reading, the slow lanes documented in this series sit upstream, in building permits and their pending queue, not at the trade counter. The strongest alternative explanation is that the two counters do different jobs by design: most trade permit classes may be issued on application and fee payment, with inspection happening afterward, while building permits carry plan review before issuance. In that case the 87.1 percent and the 29 days measure class design more than counter performance, and the data in these registers cannot separate the two readings.

## Who can act

- **Metro Codes Administration (field definitions in the public layer).** The lever is the metadata for this view: defining the Case_Status values and stating whether Contract_Value is the trade's own contract value or the parent project's value would make both fields usable by any reader. Cost class: low-cost operational change. Outcome measure: the definitions present in the layer's metadata on a future snapshot, checkable against this same service.
- **Metro Codes Administration (permit linkage).** The lever is a parent reference: publishing the building permit or case number each trade permit attaches to would let completion chains be measured directly instead of inferred from parcel overlap. Cost class: low-cost operational change if the link exists in the source system. Outcome measure: the share of trade permits carrying a parent reference in a future snapshot of this view, with the parcel-join match rates in this brief as the baseline it replaces.
- **Metro Codes Administration (class-level queue reporting).** The lever is the one measurable slow lane at scale: gas and mechanical unit change-outs clear the same day 46.0 percent of the time against 89 percent or better for each of the register's four largest permit kinds. Publishing median entry-to-issuance gaps by permit class, or confirming the class medians are recomputable from this view, would show whether the change-out lane moves. Cost class: low-cost operational change. Outcome measure: the unit change-out same-day share and median gap in this view on a future snapshot, computed the same way as the subtype panel in this brief's data folder.

## Methods in brief

Snapshot of the full served view on November 6, 2026 (111,321 records; the live count the same evening matched the pull exactly). Dates are true timestamps in the source; all date arithmetic uses America/Chicago local dates. Entry-to-issuance gaps exclude the 3 records with a negative gap. Contract_Value is never summed, for the repetition reason printed above. The parcel join, its exclusions, and the pre-flight audit are documented in verification.md. This brief measures permits as recorded, not work performed: an issued trade permit is not proof the work was done, and the layer carries no inspection outcome field. The source records carry a Contact field with applicant names; that column is withheld from the published snapshot in this repository, and names are never published by Machine Readable.

Data, code, charts, and the full audit: https://github.com/adowlen/nashville-trade-permits-data-brief

*Machine Readable is a public-good civic data project. Figures are drawn from the sources in the repository's sources.md; corrections are welcome and will be recorded in the repository.*
