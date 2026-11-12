---
title: "DataHub sets out six-step loop for managing shared context for AI agents after launch"
date: 2026-11-06
dek: "The metadata vendor argues that shared business definitions, not per-agent prompt engineering, decide agent accuracy, and proposes domain owners, daily evals and feedback loops to keep context current."
whyItMatters: "The guidance recasts familiar stewardship tasks as AI agent controls. These include named domain owners, certified tables, glossary definitions and deprecation of stale assets. Teams deploying agents can check whether each agent domain has an accountable owner and a fixed set of test questions with expert-approved answers. They can also check whether agent-reported missing, incorrect or conflicting context reaches stewards rather than staying with individual agent builders. The split between publish-then-verify and review-first modes offers a practical way to decide where human sign-off is needed for AI-generated metadata in sensitive domains."
categories: [metadata, ai-governance, data-quality]
institutions: []
whoShouldCare: ["Data stewards", "CDO", "AI governance lead", "Data platform teams"]
importance: 2
format: "How-to"
byline:
  name: "DataHub"
  role: "the vendor of the product described"
type: "Guidance"
region: "Global"
status:
  stage: "Published"
  detail: "Vendor guidance and commissioned survey"
sources:
  - name: "DataHub"
    title: "Agent Context Management: How to Manage Context for AI Agents After Launch"
    url: "https://datahub.com/blog/agent-context-management/"
    primary: true
  - name: "DataHub"
    title: "The State of Context Management in 2026"
    url: "https://datahub.com/guides/2026-context-management-report/"
    primary: true
related: [aws-architects-show-how-a-semantic-layer-stopped-an-ai-agent-overstati, google-makes-lookml-metric-definitions-and-lineage-generally-available]
card:
  figure: "83%"
  caption: "Share of 250 surveyed IT and data leaders who say agents need a context platform"
---

DataHub has published guidance on **agent context management**, which separates two levels of work. Agent builders manage what enters each agent's context window. Data and domain teams manage the shared definitions every agent draws on. The vendor proposes a repeatable loop for each domain: scope the domain and name an owner, write 20 to 50 expert-checked evaluation questions before adding context, ingest governed sources and generate the remaining documentation, choose expert review or eval-based checks, serve context through open interfaces such as MCP, then route agent-reported gaps back to owners.

According to DataHub, Miro's analytics agent rose from under 40% to over 90% accuracy as context was added. Pinterest reportedly cut 400,000 tables to 100,000 curated assets. DataHub also cites its commissioned survey of 250 IT and data leaders, in which **83%** agreed agentic AI cannot reach production value without a context platform.

*Editor's note: This article relies solely on a vendor's own blog post and its commissioned survey; customer figures are as reported by DataHub.*
