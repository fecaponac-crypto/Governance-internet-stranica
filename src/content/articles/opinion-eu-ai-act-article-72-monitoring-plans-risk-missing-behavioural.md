---
title: "Opinion: EU AI Act Article 72 monitoring plans risk missing behavioural drift in high-risk AI"
date: 2026-11-11
dek: "A consultant writing for the IAPP argues that post-market monitoring built around performance thresholds will not detect AI systems that behave differently from the version that was assessed."
whyItMatters: "Monitoring plans that only track accuracy and error rates may satisfy a documentation check while missing changes in how a high-risk system actually decides. Governance teams preparing Article 72 plans can test whether anyone owns behavioural change, whether a baseline from the last assessment is kept and compared, and whether recalibration on data shaped by manual overrides triggers review. This also links model governance to data lineage: override and feedback data feeding retraining should be tracked as a source of change."
categories: [ai-governance, regulation, data-quality]
institutions: []
whoShouldCare: ["AI governance lead", "Model risk managers", "Data stewards", "Legal & compliance"]
importance: 2
type: "Guidance"
region: "EU"
status:
  stage: "Published"
  detail: "Contributed opinion piece; not official guidance"
sources:
  - name: "IAPP"
    title: "Compliant and still blind: What Article 72 monitoring doesn't see"
    url: "https://iapp.org/news/a/compliant-and-still-blind-what-article-72-monitoring-doesn-t-see"
related: [supervisors-press-banks-on-ai-agent-controls, occ-gives-bank-examiners-a-16-component-framework-for-supervising-ai-a]
card:
  figure: "Article 72"
  caption: "AI Act post-market monitoring may miss behavioural drift, a consultant argues"
---

In a contributed opinion piece published by the IAPP, Nadège Barnes, founder of Praxeon Consulting, argues that many organisations are treating **Article 72 post-market monitoring** under the EU AI Act as a paperwork exercise. She notes that these requirements are not yet applicable to most high-risk AI systems, but that firms are already drafting plans, incident processes and Annex IV documentation.

Her central point is that monitoring designed around performance failure, such as falling accuracy or rising complaints, will not catch **behavioural drift**. Using a credit scoring example, she describes how manual overrides feed back into operational data, and how recalibration can shift approvals and escalations while metrics still look normal.

She proposes three changes: a named owner for behavioural change, a live comparison baseline against the last review, and an independent "second sensor" with authority to trigger review without waiting for a threshold breach.

*Editor's note: This article is based on a contributed opinion piece published by the IAPP, not on official guidance or a regulatory document.*
