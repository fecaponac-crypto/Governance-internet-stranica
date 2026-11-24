---
title: "Databricks adds Iceberg catalog labels to share ownership and classification tags across engines"
date: 2026-11-24
dek: "A new optional labels field in the Apache Iceberg REST Catalog API carries table- and column-level tags between platforms. Databricks' Tag Exchange, which exposes Unity Catalog tags this way, is in Beta."
whyItMatters: "Classifications, ownership and certification status often have to be re-created or synchronised by custom pipelines when data is read by other engines or AI agents; a shared labels field could let stewards maintain them once at the catalog. Because the standard leaves vocabulary undefined, teams would still need an agreed tag taxonomy so that a sensitivity or ownership label means the same thing to every consuming tool. Access-control teams should also confirm how downstream platforms interpret labels before relying on them for policy enforcement, as each tool applies its own rules."
categories: [metadata, platforms, market]
institutions: []
whoShouldCare: ["Data stewards", "CDO", "Data platform architects", "AI governance lead"]
importance: 3
type: "Product launch"
region: "Global"
status:
  stage: "Preview"
  detail: "Tag Exchange in Beta; PyIceberg label support due in its next 0.13 release"
sources:
  - name: "Databricks Blog"
    title: "Sharing catalog metadata across data platforms, engines and agents"
    url: "https://www.databricks.com/blog/sharing-catalog-metadata-across-data-platforms-engines-and-agents"
    primary: true
related: []
card:
  figure: "Beta"
  caption: "Tag Exchange shares Unity Catalog tags through Iceberg REST catalog labels"
---

Databricks says it worked with the Apache Iceberg community to add an **optional labels field to the Iceberg REST LoadTable response**. Catalog labels are string key-value pairs that can describe business ownership, intended use, sensitivity or other catalog-maintained context. The standard sets a common format but does not prescribe vocabulary or interpretation, so each receiving tool decides how to use the labels.

Databricks names Google Cloud, Salesforce, ClickHouse, Atlan, Collibra, DataHub, Immuta, Trust3 AI, PhoenixAI and Datastrato as partners. PyIceberg has added support for reading labels, which the company says will be usable in the next 0.13 release.

Databricks' own implementation, **Tag Exchange, is available in Beta** and exposes Unity Catalog table- and column-level tags as labels. According to Trust3 AI, a sensitivity label set once in Unity Catalog can drive policy in its platform without a separate metadata project.

*Editor's note: This article relies solely on Databricks' own announcement, including partner quotes it published.*
