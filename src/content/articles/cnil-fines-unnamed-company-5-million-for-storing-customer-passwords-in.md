---
title: "CNIL fines unnamed company €5 million for storing customer passwords in plain text"
date: 2026-11-18
dek: "The restricted committee also found shared staff logins to customer databases and contact-form data kept for more than ten years, and published its decision without naming the firm."
whyItMatters: "The CNIL chose to publish the decision for educational purposes, describing the securing of data accessible via passwords as one of the essential principles of data security, and stating that only individual accounts allow effective traceability of access. It also shows that having a retention policy is not enough: the regulator checked whether the firm actually applied its own one-year limit. Data owners and stewards should be able to show that retention rules are enforced in systems, not just documented, and that access to customer databases is traceable to individuals."
categories: [security, privacy, regulation]
institutions: [cnil]
whoShouldCare: ["DPO", "CISO", "Data stewards", "Legal & compliance"]
importance: 4
type: "Enforcement"
region: "France"
status:
  stage: "Decision"
  detail: "Company not named; decision published for educational purposes"
whatToCheck:
  - "Confirm that no customer-facing system stores passwords or security-question answers in plain text."
  - "Check whether any staff share logins to customer databases or the tools used to query them, and replace these with individual accounts."
  - "Compare actual data held, including contact-form and connection logs, against your documented retention periods and verify that deletion or purge jobs run."
legislation: [eu-gdpr]
enforcement:
  case: cnil-plain-text-passwords-san-2026-016
  action: "Fine"
  authority: "CNIL"
  parties: "Unnamed company (not named by the CNIL)"
  framework: "GDPR"
  jurisdiction: "France"
  amount: 5000000
  currency: "EUR"
  law: "GDPR Article 32 (security) and Article 5(1)(e) (storage limitation)"
  date: 2026-11-12
sources:
  - name: "CNIL"
    title: "Conservation des mots de passe clients en clair : la CNIL prononce une sanction de 5 millions d’euros"
    url: "https://www.cnil.fr/fr/conservation-des-mots-de-passe-sanction-5-millions-deuros"
    primary: true
related: [noyb-complaint-behind-cnil-s-eur-7-million-fine-on-fnac-app-tracker-th]
card:
  figure: "€5m"
  caption: "CNIL fine for plain-text passwords, shared logins and excessive data retention"
---

France's CNIL has imposed a **€5 million fine** on a company it did not name (deliberation SAN-2026-016 of 12 November 2026, announced on 18 November). An inspection, prompted by an alert about how the firm stored customer passwords and answers to security questions, found breaches of the GDPR. The restricted committee, the CNIL body that issues sanctions, said the amount reflected the seriousness of the failings, the number of people affected and the company's financial capacity.

Under Article 32, it found **customer account passwords were stored in plain text** and that staff shared logins to customer databases and the tool used to access them, which prevents effective traceability of access.

Under Article 5(1)(e), contact-form data had been kept for more than ten years, and connection data exceeded the company's own one-year retention policy. The company took corrective steps during the procedure, including deleting obsolete data and introducing a monthly purge.
