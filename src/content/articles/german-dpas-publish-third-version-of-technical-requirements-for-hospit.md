---
title: "German DPAs publish third version of technical requirements for hospital information systems"
date: 2026-11-26
dek: "The DSK's updated guidance sets mandatory, recommended and optional controls for vendors and hospitals, covering role-based access, physical deletion, pseudonymisation, encryption and anonymised analytics."
whyItMatters: "Hospitals in Germany should map their patient record systems against the mandatory items, since the DSK states that unmet mandatory operator requirements mean compliant operation is not achieved. Data teams should check that warehouse and research feeds are anonymised, that deletion propagates physically across all subsystems and redundant copies, and that permission overviews can be reconstructed for any past date. Procurement should demand the listed vendor functions, and cloud contracts need a provider encryption concept showing who controls the keys."
categories: [privacy, security, metadata]
institutions: [german-dpas]
legislation: [eu-gdpr]
whoShouldCare: ["DPO", "CISO", "Data stewards", "Legal & compliance"]
importance: 3
type: "Guidance"
region: "Germany"
status:
  stage: "Published"
  detail: "Part 2, version 3; supersedes earlier editions of the 2014 guidance"
sources:
  - name: "Datenschutzkonferenz (DSK)"
    title: "Orientierungshilfen – 26. November 2026: Orientierungshilfe Krankenhausinformationssysteme (OH KIS)"
    url: "https://www.datenschutzkonferenz-online.de/orientierungshilfen.html#26-november-2026-orientierungshilfe-krankenhausinformationssysteme-oh-kis"
    primary: true
  - name: "Datenschutzkonferenz (DSK)"
    title: "Technische Anforderungen an die Gestaltung und den Betrieb von Krankenhausinformationssystemen (Teil 2, 3. Fassung)"
    url: "https://www.datenschutzkonferenz-online.de/media/oh/20261126_OH-KIS_Teil-2_Technische-Anforderungen-an-Krankenhausinformationssysteme.pdf"
    primary: true
related: []
card:
  figure: "1 year"
  caption: "Maximum period before hospitals must restrict access to closed patient case files"
---

Germany's data protection conference (DSK) has published version 3 of Part 2 of its guidance on hospital information systems, dated **26 November 2026**. It sets out technical measures for implementing data protection law and medical confidentiality, mainly in systems holding electronic patient records, and reflects the GDPR's Articles 24, 25, 32 and 35.

Each requirement is tagged as falling on manufacturers, hospital operators or both, and graded as "muss", "soll" or "sollte". Mandatory items include restricting access to closed case files after a hospital-defined period of **no longer than one year**, physical deletion once retention periods expire (soft deletes are insufficient), multi-factor authentication with limited exceptions, an integrated pseudonymisation service, and anonymisation before patient data enters analytics components such as a data warehouse.

The DSK says a data protection impact assessment is generally required for hospital processing via these systems.
