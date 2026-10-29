---
title: "Dutch AP warns debt collectors that AI scoring and file enrichment may breach GDPR automated decision rules"
date: 2026-10-29
dek: "A survey of 29 registered Dutch collection agencies found algorithmic tools in core processes, weak transparency and a narrow view of personal data. The AP says profiling such as file enrichment should stop."
whyItMatters: "The report treats debt amounts and system outputs that say something about a person as personal data, which many agencies had excluded from their inventories. Organisations that score, prioritise or enrich customer records should check whether their records of processing cover these outputs. They should also check whether automated first-contact or approval steps fall under Article 22, and whether human review genuinely changes outcomes. The supplier findings matter beyond collections: AI features added to bought-in software can process personal data that the buyer never chose to process."
categories: [privacy, ai-governance, data-quality]
institutions: [dutch-ap]
whoShouldCare: ["DPO", "AI governance lead", "Data stewards", "Legal & compliance"]
importance: 4
type: "Supervision"
region: "Netherlands"
status:
  stage: "Published"
  detail: "Recommendations, not a binding decision; sector roundtable to follow"
whatToCheck:
  - "Confirm that your inventory of personal data includes debt or balance data and the scores or outputs your algorithms generate about individuals."
  - "Review fully automated steps, including approvals that favour the customer, to decide whether Article 22 applies and whether an exception covers them."
  - "Check supplier contracts for AI features and processing terms, especially where a vendor has added AI functions to existing software."
deadlines:
  - date: 2026-11-11
    what: "Deadline for collection-sector organisations to register for the AP roundtable"
  - date: 2026-12-02
    what: "AP roundtable with the debt collection sector on the report's findings"
sources:
  - name: "Autoriteit Persoonsgegevens"
    title: "AP informeert incassobureaus over verantwoorde inzet AI"
    url: "https://autoriteitpersoonsgegevens.nl/actueel/ap-informeert-incassobureaus-over-verantwoorde-inzet-ai"
    primary: true
  - name: "Autoriteit Persoonsgegevens"
    title: "Onderzoeksrapport Automatische incasso: Algoritmes en AI bij incassobureaus"
    url: "https://autoriteitpersoonsgegevens.nl/system/files?file=2026-10/Rapport%20automatische%20incasso%20algoritmes%20en%20AI%20bij%20incassobureaus.pdf"
    primary: true
related: []
card:
  figure: "Art. 22 GDPR"
  caption: "AP finds automated decisions likely at Dutch debt collectors without their knowledge"
---

The Dutch data protection authority (AP) has published a report on algorithms and AI at private debt collection agencies. It sent a questionnaire to **29 registered agencies**, and 22 gave usable answers. Ten said they use at least one algorithmic system, three of them AI.

Uses include choosing contact channels, automated payment arrangements, collection-probability scoring, enriching debtor files from registers and social media, vulnerability detection and call analysis. The AP considers it **plausible that Article 22 GDPR automated decision-making occurs** without agencies realising it. It notes that intermediate steps such as a risk score can count as a decision, citing the CJEU SCHUFA ruling.

The AP makes recommendations in five areas: data awareness, transparency, meaningful human intervention, supplier management and risk mitigation. It will hold a sector roundtable on 2 December 2026.
