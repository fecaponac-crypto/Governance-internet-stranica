---
title: "Google makes LookML metric definitions and lineage generally available in Knowledge Catalog"
date: 2026-10-26
dek: "Looker Core on Google Cloud now indexes models, joins, metric formulas and dashboard lineage into Knowledge Catalog by default, so Gemini Enterprise and custom agents can ground SQL in certified business logic."
whyItMatters: "Metric definitions, filters and ownership become catalog metadata that AI agents treat as authoritative, so certification and stewardship of LookML models now directly affect the quality of agent answers. Teams should decide which models count as certified before agents start consuming them. They should also confirm that access filters and column-level tags are set correctly, because the integration is on by default. Note that an opted-out instance leaves stale metadata in the catalog, which may need cleaning up."
categories: [metadata, ai-governance, analytics]
institutions: []
whoShouldCare: ["CDO", "Data stewards", "AI governance lead", "BI and analytics leads"]
importance: 3
type: "Product launch"
region: "Global"
status:
  stage: "Available"
  detail: "enabled by default on Looker Core on Google Cloud instances"
sources:
  - name: "Google Cloud Blog"
    title: "Unifying enterprise context and semantics: LookML in Knowledge Catalog is now GA"
    url: "https://cloud.google.com/blog/products/business-intelligence/lookml-metadata-indexing-in-knowledge-catalog-is-now-ga/"
    primary: true
  - name: "Google Cloud documentation"
    title: "Manage Looker (Google Cloud core) metadata in Knowledge Catalog"
    url: "https://docs.cloud.google.com/knowledge-catalog/docs/manage-looker-core-metadata"
    primary: true
related: [google-knowledge-catalog-self-learning-enrichment]
card:
  figure: "GA"
  caption: "LookML semantics and lineage now indexed in Google's Knowledge Catalog by default"
---

Google Cloud has announced the **general availability of LookML indexing in Knowledge Catalog** for Looker Core on Google Cloud. LookML models, Explores, views, field definitions, join conditions, mandatory filters and dashboards are synchronised into the catalog. According to Google, this lets Gemini Enterprise and custom agents use exact metric formulas rather than inventing SQL.

The documentation says synchronisation is **on by default and needs no configuration**. Updates pushed to production LookML are reflected through a live sync. Lineage runs from BigQuery tables to individual dashboard tiles, supporting impact analysis and upstream audit. Storing Looker technical metadata carries no charge, although standard pricing applies to API calls and business metadata enrichment.

Administrators can opt out. If they do, metadata already in the catalog remains there but is no longer updated. Gemini Enterprise queries the catalog using end-user credentials, so users see only the assets their IAM roles permit.

*Editor's note: Both sources are Google's own announcement and product documentation; the claims have not been independently verified.*
