---
title: "SAP confirms cyber incident after reports hackers accessed its GitHub development environment"
date: 2026-11-27
dek: "SAP says it has found no evidence of access to customer business data, but Der Spiegel reports that attackers obtained employee authentication tokens allowing them to copy and modify source code."
whyItMatters: "SAP products are used to run critical operations such as accounting, procurement, supply chains and human resources, so any risk of tampered code reaching customers is a governance issue, not only a security one. Teams should track SAP's advisories on affected components, confirm that recent updates and packages are verified against current signing keys, and be ready to assess data integrity and notification duties if SAP later reports customer impact."
categories: [security, platforms]
institutions: []
whoShouldCare: ["CISO", "CDO", "Data stewards", "Legal & compliance"]
importance: 4
type: "Announcement"
region: "Global"
status:
  stage: "Unconfirmed"
  detail: "SAP confirms incident; reported source code access and tampering not confirmed by SAP"
whatToCheck:
  - "Check which SAP products, updates and SAP-developed open-source packages you have deployed recently and monitor SAP's communications on whether any are affected."
  - "Confirm that your processes verify SAP software signatures and would pick up the replacement of SAP's signing keys."
  - "Map which data sit in SAP systems used for accounting, procurement, supply chain and HR so the integrity impact can be assessed quickly if customer exposure is later confirmed."
sources:
  - name: "The Record (Recorded Future News)"
    title: "Software giant SAP confirms cyber incident amid reports of source code breach"
    url: "https://therecord.media/sap-germany-cyberattack-github"
related: []
card:
  figure: "GitHub"
  caption: "SAP's development environment reportedly targeted, per Der Spiegel"
---

SAP has confirmed a cybersecurity incident. It told Recorded Future News that it had identified suspicious activity and taken immediate steps, and that it had found **no evidence of unauthorised access to customer business data** so far. The company did not disclose the nature or extent of the intrusion.

According to Der Spiegel, attackers targeted SAP's software development environment on GitHub and **obtained employee authentication tokens that allowed them to copy and modify source code**. Reported containment measures included restricting GitHub access, halting automated development processes and replacing the keys used to verify software integrity.

It is unclear whether altered code reached customer software, who was responsible, how access was gained or whether the incident is contained. SAP also faced a separate supply chain attack in April on open-source packages it develops; any link is unknown.

*Editor's note: This article relies on a single secondary news report, which itself cites Der Spiegel, dpa and Handelsblatt; SAP's statement is quoted via that report.*
