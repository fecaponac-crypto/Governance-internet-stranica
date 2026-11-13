---
title: "Google adds AI agent observability across BigQuery and Looker, logging prompts to customer-owned tables"
date: 2026-11-13
dek: "Telemetry from Google's own data agents and custom ADK or LangGraph agents lands in BigQuery, with opt-in conversation logging that skips turns touching masked or row-secured data."
whyItMatters: "Opt-in conversation logging creates a new store of user prompts and agent responses, and these may contain personal or confidential data. Teams should assign an owner for `agent_events` tables, set a retention period and record them in the data inventory. The fail-closed skip is tied to existing row-level security, policy tags and masking. Data that is sensitive but not tagged would therefore still be logged, which makes the completeness of classification and tagging a privacy control in its own right."
categories: [ai-governance, platforms, security]
institutions: []
whoShouldCare: ["AI governance lead", "Data stewards", "DPO", "Data platform owners"]
importance: 3
type: "Product launch"
region: "Global"
status:
  stage: "Available"
  detail: "Token quotas, Looker feedback review and native evaluations are in preview"
sources:
  - name: "Google Cloud Blog"
    title: "New AI agent observability and governance across BigQuery and Looker"
    url: "https://cloud.google.com/blog/products/data-analytics/enterprise-ai-agent-observability-with-bigquery-and-looker/"
    primary: true
related: [google-makes-bigquery-measures-generally-available-putting-governed-me, google-makes-lookml-metric-definitions-and-lineage-generally-available]
card:
  figure: "agent_events"
  caption: "Customer-owned BigQuery table that stores opt-in agent prompts and responses"
---

Google has announced expanded observability and evaluation features for AI agents across BigQuery and Looker. They cover its own Conversational Analytics agents and custom agents built with ADK or LangGraph. Telemetry is written to **BigQuery tables the customer owns**. The Conversational Analytics API, now generally available, carries admin audit logs, CMEK, VPC Service Controls and data residency options.

Google says operational metrics and trace spans leave out prompts, responses and generated SQL. Agent owners can opt in, agent by agent, to conversation logging into an `agent_events` table, which inherits the dataset's IAM permissions. A fail-closed check **skips logging whenever a knowledge source uses row-level security, column policy tags or dynamic data masking**.

Cost controls include per-query byte-scan caps. Daily token quotas per project, user or agent are in preview. So are native BigQuery agent evaluations, alongside Google's open-source Prism benchmarking tool.

*Editor's note: This article relies solely on Google's own announcement of its products.*
