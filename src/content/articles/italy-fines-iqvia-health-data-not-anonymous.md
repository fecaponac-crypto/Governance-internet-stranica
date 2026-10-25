---
title: "Italy fines IQVIA EUR 7 million: “anonymous” patient database was not anonymous"
date: 2026-10-09
dek: "A persistent patient identifier combined with detailed clinical data made re-identification possible across a database of about one million patients."
whyItMatters: "Anonymisation is a data quality and governance claim, not a label. The decision shows how a persistent identifier plus rich attributes defeats anonymisation, pulling a dataset back under the GDPR with all its duties — legal basis, transparency, retention, DPIA and security. Teams that publish or sell “anonymised” datasets should test re-identification risk and document the result."
categories: [privacy, data-quality]
institutions: [garante]
whoShouldCare: [DPO, Data stewards, Data product owners, Healthcare & life sciences]
importance: 4
type: Enforcement
region: Italy
status:
  stage: Decision
sources:
  - name: EDPB
    title: "Italian DPA fines IQVIA EUR 7 000 000 for unlawful processing of patients’ health data"
    url: https://www.edpb.europa.eu/news/italian-dpa-fines-iqvia-eur-7-000-000-for-unlawful-processing-of-patients-health-data_en
    primary: true
related: [norway-fines-xandr-joint-controller-consent]
card:
  figure: "EUR 7M"
  caption: "Fine over an “anonymous” database of one million patients"
sample: true
---

The Italian Data Protection Authority has fined **IQVIA Solutions Italy EUR 7 million** over a database with health information on about one million patients of 800 general practitioners, used for studies including some commissioned by pharmaceutical companies.

IQVIA treated the data as anonymous. The regulator disagreed: a persistent identifier let each patient be followed over time and, combined with year of birth, sex, diagnoses, prescriptions, vaccinations and location data, allowed individuals to be singled out and potentially re-identified. The database also held directly identifying information on about 3,370 patients.

The authority found failures on legal basis, information to patients, retention periods, the data protection impact assessment and security. To continue, IQVIA has **120 days** to bring the processing into compliance — or the GPs must anonymise the data themselves under safeguards set by the authority.
