---
title: "Google adds self-learning enrichment to Knowledge Catalog, putting stewards in the review loop"
date: 2026-10-22
dek: "The preview feature analyses agent and user interactions to find missing or outdated business context and proposes fixes for data stewards to approve."
whyItMatters: "Catalogs are being repositioned as the context layer for AI agents, and the steward's job shifts from writing metadata to reviewing machine-proposed changes. The useful governance controls here — confidence thresholds, change requests, provenance and rollback — are worth demanding from any catalog vendor. Performance figures are Google's own benchmarks."
categories: [metadata, market, platforms]
whoShouldCare: [Data stewards, Data catalog owners, Data architects, AI platform teams]
importance: 3
type: Product launch
region: Global
sources:
  - name: Google Cloud Blog
    title: "Introducing new self-learning context enrichment in Knowledge Catalog"
    url: https://cloud.google.com/blog/products/data-analytics/knowledge-catalog-self-learning-context-enrichment-for-ai-agents/
    primary: true
related: []
sample: true
---

Google Cloud has launched **self-learning context enrichment** and a redesigned **Knowledge Studio**, both in preview, in Knowledge Catalog — the product Google now positions as a context engine for AI agents.

Enrichment pulls business definitions from documents, code repositories and wikis (including Google Workspace, GitHub, Confluence and SharePoint) and links them to tables and schemas. It proposes definitions, column descriptions, join relationships and agent instructions, each with source citations and a confidence score. The new self-learning mode analyses agent and user interactions to spot where agents struggled and stages fixes.

Organisations can set a confidence threshold for automatic approval; anything below it, and sensitive changes such as deletions, becomes a **change request** for a data steward. Every change is logged with provenance and can be reverted. Google claims agents become nearly 4x more accurate based on internal benchmarks.
