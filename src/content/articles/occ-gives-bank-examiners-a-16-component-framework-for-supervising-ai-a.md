---
title: "OCC gives bank examiners a 16-component framework for supervising AI and agentic systems"
date: 2026-11-04
dek: "The US bank regulator says examiners should not treat AI as a separate risk category and that scrutiny may be scaled to consequences, delegated authority and human oversight, not technical sophistication."
whyItMatters: "Under the data governance component, a bank may assess the origin, licensing, transformations and limitations of training, fine-tuning, source and production data, including data embedded in third-party foundation models, and consider new data created by prompts, outputs, embeddings and logs. The purpose component suggests an inventory that may capture each use case's owner, provider, permissions, deployment status, monitoring and fail-over arrangements, with authorised data sources and actions stated in testable terms. Agent identities and credentials may be governed like privileged users, and decision traces may allow material actions to be reconstructed."
categories: [ai-governance, regulation, data-quality]
institutions: []
whoShouldCare: ["AI governance lead", "CDO", "Chief risk officer", "CISO"]
importance: 4
type: "Supervision"
region: "US"
status:
  stage: "Published"
  detail: "Examiner framework; OCC says it will be updated regularly"
whatToCheck:
  - "Check whether your AI inventory captures, for each use case, its owner, provider, permissions, deployment status, monitoring and fail-over arrangements."
  - "Check whether prompts, outputs, embeddings and logs that may hold sensitive information are subject to access controls and risk-based retention periods."
  - "Check whether vendor contracts state if bank data may be used to train models offered to other customers and require notice when vendors add AI features or change models."
sources:
  - name: "Office of the Comptroller of the Currency"
    title: "Super Intelligence: Supervisory Framework"
    url: "https://www.occ.gov/news-issuances/news-releases/2026/nr-occ-2026-97a.pdf"
    primary: true
  - name: "CDO Magazine"
    title: "OCC issues supervisory framework for banks using AI systems"
    url: "https://www.cdomagazine.tech/us-federal-news-bureau/occ-issues-supervisory-framework-for-banks-using-ai-systems"
related: [supervisors-press-banks-on-ai-agent-controls, forrester-urges-banks-to-replace-blanket-ai-agent-blocks-with-graduate]
card:
  figure: "16 components"
  caption: "OCC framework for examiners assessing banks' AI and agentic AI use"
---

The US Office of the Comptroller of the Currency (OCC) has published *Super Intelligence: Supervisory Framework*, a document for examiners assessing how national banks, federal savings associations and federal branches and agencies of foreign banking organisations use AI and AI agents. The OCC uses "Super Intelligence" (SI) for what was previously called AI, citing Executive Order 14434.

The framework sets out **sixteen components grouped into six pillars**: purpose, risk, control, oversight, resilience and assurance. Examiners should not treat SI as a distinct risk category, and **banks need not set a separate SI risk appetite**. Risk classification may be based on potential consequences, transfer of agency and the degree of human oversight; a simple agent able to initiate transactions could be riskier than a sophisticated drafting tool.

The OCC calls it a living document to be updated as technology and use cases change.
