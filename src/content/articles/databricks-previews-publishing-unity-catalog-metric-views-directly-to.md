---
title: "Databricks previews publishing Unity Catalog metric views directly to Power BI semantic models"
date: 2026-11-10
dek: "The private preview translates governed metric definitions into DAX measures one way only, so edits made in Power BI are not written back and access control depends on the query mode."
whyItMatters: "Organisations with many Power BI workspaces often hold divergent copies of the same KPI; this approach makes the Unity Catalog metric view the single owned definition, so metric ownership and change control need to sit with whoever maintains it. Teams should note that governance guarantees differ by mode: Import copies data into Power BI under Power BI permissions, outside Unity Catalog masks and row filters. Because Power BI edits are not synced back, stewards should consider how to prevent or detect local measure changes that silently diverge from the governed definition."
categories: [metadata, analytics, market]
institutions: []
whoShouldCare: ["CDO", "Data stewards", "BI and analytics leads", "Data platform architects"]
importance: 2
type: "Product launch"
region: "Global"
status:
  stage: "Preview"
  detail: "Private preview; access via Databricks account teams"
sources:
  - name: "Databricks Blog"
    title: "Unity Catalog metric views now power Power BI: one unified, governed semantic layer for all your reporting"
    url: "https://www.databricks.com/blog/unity-catalog-metric-views-now-power-bi-one-unified-governed-semantic-layer-all-your-reporting"
    primary: true
related: [google-makes-lookml-metric-definitions-and-lineage-generally-available, aws-architects-show-how-a-semantic-layer-stopped-an-ai-agent-overstati]
card:
  figure: "Private preview"
  caption: "Unity Catalog metric views can be published as Power BI semantic models"
---

Databricks has announced **Publish to Power BI**, a capability that pushes Unity Catalog metric views into Power BI semantic models. It is in **private preview**, available through account teams.

According to Databricks, each metric view becomes one table in the Power BI model: dimensions become columns and measures are translated into DAX. Power BI queries the metric view itself, so joins and calculations run in Databricks and no Power BI relationships need rebuilding. Teams can publish on demand from Catalog Explorer or add a Power BI task to a Lakeflow Job to republish on a schedule or after upstream refreshes.

Publishing runs one way only; edits to a published measure in Power BI are not written back. Databricks says DirectQuery honours Unity Catalog access controls, row filters and column masks, while in Import mode the loaded copy follows Power BI permissions.

*Editor's note: This article is based solely on Databricks' own blog announcement.*
