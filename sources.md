# Sources

## Primary source for every figure in this brief

1. **Nashville Trade Permits (Trade_Permits_View), Metro Nashville / Davidson County via hubNashville open data (Nashville Open Data Portal).** ArcGIS FeatureServer layer 0, services2.arcgis.com/HdTo6HJqh92wn4D8. Full-view snapshot pulled November 6, 2026. 111,321 records; service data last edited November 6, 2026 per the layer metadata (archived in this package at data/source-metadata-layer.json). Entry dates in the snapshot span October 12, 2023 to October 16, 2026.
   - Service: https://services2.arcgis.com/HdTo6HJqh92wn4D8/arcgis/rest/services/Trade_Permits_View/FeatureServer
   - Dataset landing page: hubNashville (data.nashville.gov), Trade Permits. Agency: Metropolitan Government of Nashville and Davidson County, Department of Codes Administration (permitting system of record).
   - Fields used (public names): Trade, Permit_Type_Description, Permit_Subtype_Description, Date_Entered, Date_Issued, Contract_Value, Case_Status, Parcel, Council_Dist, Census_Tract, Zip, PermitNumber. The layer also carries a Contact field with applicant names; Machine Readable never publishes personal names from permit records.
   - The layer's public metadata does not define its Case_Status values or the Contract_Value field's basis (trade contract value vs parent project value). Both gaps are stated in the brief where the fields are used.

## Comparison sources (companion Machine Readable briefs)

2. **Building Permits Issued (Machine Readable, published November 3, 2026)** - 29,651 permits, issue dates October 30, 2023 to November 2, 2026; median entry-to-issuance wait 29 days; District 19 stated construction value $3,148,570,433 of $13,227,134,850 (23.8 percent). Repository: https://github.com/adowlen/nashville-building-permits-data-brief. The parcel join in the trade brief matches against that package's cleaned layer in the Metro Nashville Warehouse (Nashville locality stack, layer building_permits_issued).
3. **Building Permit Applications (Machine Readable, published November 4, 2026)** - cited only for series context (the pending queue). Repository: https://github.com/adowlen/nashville-building-permit-applications-data-brief.
4. **Beer Permit Locations (Machine Readable, published November 6, 2026)** - District 19 holds 458 of 2,064 issued beer permits (22.2 percent), 11.4 times the median district (40); used only for the same-unit (permits per district) contrast. Repository: https://github.com/adowlen/nashville-beer-permits-data-brief.

## Repository and license

Full code, charts, panels, and verification notes: https://github.com/adowlen/nashville-trade-permits-data-brief (the raw snapshot is retained in the project warehouse stack and reproducible with the pull script in that repository)
Brief text and data products: CC BY 4.0 (LICENSE in the package). The underlying permit records are published by Metro Nashville as government open data.
