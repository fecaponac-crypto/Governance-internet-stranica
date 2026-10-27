---
title: "AWS architects show how a semantic layer stopped an AI agent overstating revenue by 30.8%"
date: 2026-10-27
dek: "At dbt Summit 2026, two AWS architects described routing agent queries through certified dbt metrics and read-only Redshift execution, rather than letting the model write its own SQL."
whyItMatters: "The example shows that business rules held only in people's heads or a semantic layer are invisible to an agent reading the schema, so metric definitions become a control, not a convenience. Data owners should check whether key metrics such as revenue are formally certified, with exclusions like refunds and test accounts documented in metadata. AI governance leads can use the 'receipt' pattern — metric, compiled SQL, test results, query ID — as a benchmark for auditability of agent answers."
categories: [data-quality, metadata, ai-governance]
institutions: []
whoShouldCare: ["CDO", "Data stewards", "AI governance lead", "Analytics engineering leads"]
importance: 2
type: "Case study"
region: "Global"
status:
  stage: "Published"
  detail: "Conference presentation reported by dbt Labs"
sources:
  - name: "dbt Labs Blog"
    title: "Why an AI agent's revenue query was $3.5 million wrong, and how AWS fixed it with dbt Semantic Layer"
    url: "https://www.getdbt.com/blog/aws-dbt-semantic-layer-ai-agent-revenue-accuracy"
    primary: true
related: [google-makes-lookml-metric-definitions-and-lineage-generally-available, supervisors-press-banks-on-ai-agent-controls]
card:
  figure: "30.8%"
  caption: "How far an ungoverned agent-style SQL query overstated revenue in the AWS example"
---

Two AWS solutions architects, Neela Kulkarni and Venkatesh Aravamudan, presented a governed design for AI agents querying production data on Amazon Redshift, according to a dbt Labs blog post on their dbt Summit 2026 session. Their example: an agent-style query summing gross order amounts returned $14.86 million, while actual revenue was $11.36 million, **an overstatement of 30.8%**. Four business rules on discounts, refunds, order status and test accounts existed only in the semantic layer, not the schema.

In their design, the dbt MCP Server limits agents to an enumerated list of certified metrics and MetricFlow compiles the SQL; the Amazon Redshift MCP Server enforces **read-only, single-statement execution** at the server, IAM and database-grant levels. Each answer carries a receipt with metric name, compiled SQL, source model, dbt test results and a Redshift query ID.

*Editor's note: This article relies solely on a blog post by dbt Labs, a vendor whose product features in the architecture described.*
