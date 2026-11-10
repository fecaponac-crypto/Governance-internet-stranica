---
title: "Google makes BigQuery measures generally available, putting governed metrics on knowledge graph entities"
date: 2026-11-10
dek: "Metric definitions with descriptions and synonyms now sit on BigQuery Graph entities and are searchable in Knowledge Catalog, so dashboards, SQL and AI agents can work from the same governed logic."
whyItMatters: "Metric definitions that live in BI tools or prompts tend to diverge; placing them in the warehouse schema with descriptions and synonyms makes them catalogable assets that stewards can own and review. Teams using BigQuery should decide who approves measure definitions and their semantic metadata, and check whether ambiguous metric names such as 'volume' are resolved before agents query them. The vendor's accuracy claims have not been independently tested."
categories: [metadata, analytics, platforms]
institutions: []
whoShouldCare: ["Data stewards", "Analytics engineers", "CDO", "AI governance lead"]
importance: 2
type: "Product launch"
region: "Global"
status:
  stage: "Available"
  detail: "generally available; some integrations described without stated status"
sources:
  - name: "Google Cloud Blog"
    title: "BigQuery measures is now GA, unifying BI metrics and knowledge graphs for AI accuracy"
    url: "https://cloud.google.com/blog/products/data-analytics/bigquery-measures-ga-unifying-bi-metrics-and-knowledge-graphs/"
    primary: true
related: [google-makes-lookml-metric-definitions-and-lineage-generally-available, aws-architects-show-how-a-semantic-layer-stopped-an-ai-agent-overstati]
card:
  figure: "GA"
  caption: "BigQuery measures now generally available, unifying BI metrics with knowledge graphs"
---

Google has made **BigQuery measures generally available**. The feature lets teams define business metrics directly on BigQuery Graph entities, so BI dashboards, SQL and GQL queries and AI agents evaluate against the same definitions. Google says this addresses agents that "guess" relationships and give confidently wrong answers.

Measures are "grain-locked": according to Google, they keep each entity's native granularity so joins do not overcount, and a new start_node argument avoids inflated results when combining several fact tables. GA adds derived and composite measures, validated at schema compilation, and a Data Studio connector.

Measure definitions can now carry **descriptions, synonyms and custom key-value metadata**, which are automatically ingested into Knowledge Catalog. There, stewards and agents can search, inspect governance tags, view the SQL behind each metric and add glossary and stewardship context.

*Editor's note: This article relies solely on the vendor's own announcement.*
