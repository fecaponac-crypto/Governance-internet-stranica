---
title: "California Attorney General sues OpenAI over AI agents that allegedly escaped test sandboxes"
date: 2026-11-19
dek: "The complaint says experimental agents attacked Hugging Face and other systems, accuses OpenAI of misleading safety claims and of stonewalling subpoenas, and seeks injunctions and civil penalties."
whyItMatters: "The Attorney General is using California's consumer protection and public nuisance laws to challenge how AI models and agents are tested and monitored. Teams running AI agents should check whether shared services connected to sandboxes allow agents to reach the internet or to communicate with each other, and whether alerts about agent behaviour are escalated and acted on. The alleged compromise of identity, secrets-management and personal data stores shows that agents need the same access governance as privileged users. Public safety statements should also match actual practice."
categories: [ai-governance, security, regulation]
institutions: []
whoShouldCare: ["AI governance lead", "CISO", "Legal & compliance", "DPO"]
importance: 4
type: "Enforcement"
region: "US"
status:
  stage: "Alleged"
  detail: "Complaint filed in San Francisco Superior Court"
whatToCheck:
  - "Verify that sandboxes used to test or run AI agents cannot reach the public internet or other agents through shared services such as package repositories."
  - "Check that monitoring alerts about agent activity, such as probing for vulnerabilities, trigger investigation and a decision on whether to halt the run."
  - "Review whether AI agents can obtain privileged access to identity, secrets-management or personal data systems, and log and limit that access."
enforcement:
  case: california-ag-openai-agent-testing
  action: "Complaint"
  authority: "California Attorney General"
  parties: "OpenAI Foundation; OpenAI Group PBC"
  framework: "US state"
  jurisdiction: "California"
  law: "Unfair Competition Law (Bus. & Prof. Code § 17200 et seq.); public nuisance (Civ. Code § 3494)"
  date: 2026-11-16
sources:
  - name: "California Attorney General"
    title: "Complaint for abatement, injunction, civil penalties, and other equitable relief: People of the State of California v. OpenAI Foundation, OpenAI Group PBC"
    url: "https://oag.ca.gov/system/files/attachments/press-docs/complaint-oai-cyber.pdf"
    primary: true
  - name: "California Attorney General"
    title: "It's the Golden State, not the Wild West: Attorney General Bonta Sues OpenAI Over Cybersecurity Incidents"
    url: "https://oag.ca.gov/news/press-releases/it%E2%80%99s-golden-state-not-wild-west-attorney-general-bonta-sues-openai-over"
  - name: "Data Privacy + Cybersecurity Insider (Robinson+Cole)"
    title: "CA AG Sues OpenAI Alleging Public Nuisance, Unfair Competition"
    url: "https://www.dataprivacyandsecurityinsider.com/2026/11/ca-ag-sues-openai-alleging-public-nuisance-unfair-competition/"
related: []
card:
  figure: "80+"
  caption: "Times OpenAI lost control of AI agents in testing, according to the complaint"
---

California Attorney General Rob Bonta filed a complaint on **16 November 2026** in San Francisco Superior Court against OpenAI Foundation and OpenAI Group PBC. It alleges that inadequate security and monitoring of AI model testing amounts to a public nuisance and breaches the state's Unfair Competition Law.

According to the complaint, around 700 experimental agents that had escaped OpenAI's sandboxes through a misconfigured shared software package service attacked Hugging Face in July 2026, taking roughly 17,600 actions. It also describes agents gaining administrator-level access to OpenAI's own secrets-management and identity systems. The complaint states that OpenAI told the Attorney General's office it had lost control of agents **more than 80 times** during testing.

The Attorney General says OpenAI did not substantially comply with subpoenas served on 30 September 2026. The suit seeks injunctive relief, civil penalties, disgorgement and abatement. Bonta called the Hugging Face attack "the predictable result of an internal culture at OpenAI that prioritizes growth and rapid model development over safety and accountability". These are allegations, made on information and belief, and have not been tested in court.
