---
title: "Microsoft to retire Purview Data Governance, ending support on 12 November 2027 in shift to Fabric"
date: 2026-11-13
dek: "Unified Catalog, Data Map, Workflows and the Azure Purview solutions are covered. Governance moves to the OneLake catalog in Microsoft Fabric, while Purview keeps data security and compliance."
whyItMatters: "Teams using Purview for glossaries, lineage and stewardship have a one-year window to move curated business metadata that cannot simply be rediscovered from source systems. Microsoft points customers to the OneLake catalog in Fabric, but itself acknowledges that some organisations need more than Fabric offers today and names third-party catalogs that integrate with it, so the real decision is where governance lives after November 2027. Because sensitivity labels and data loss prevention stay in Purview while the catalog moves to Fabric, teams should also check how protection and governance controls will stay linked."
categories: [metadata, platforms, market]
institutions: []
whoShouldCare: ["CDO", "Data stewards", "Data platform owners", "Legal & compliance"]
importance: 4
type: "Announcement"
region: "Global"
status:
  stage: "Announced"
  detail: "support for Purview Data Governance ends 12 November 2027"
whatToCheck:
  - "Inventory which glossaries, governance domains, data products, custom attributes and manually documented lineage currently live only in Purview's Unified Catalog or Data Map."
  - "Map which of your data platforms sit outside Fabric to decide whether the OneLake catalog alone can cover your governance scope."
  - "Confirm that ownership and stewardship assignments, and the approval workflows built in Purview Workflows, have a defined home and owner after migration."
deadlines:
  - date: 2027-11-12
    what: "Support for Microsoft Purview Data Governance, including Unified Catalog, Data Map and Workflows, ends"
sources:
  - name: "Microsoft Security Community Blog"
    title: "A next step in the evolution of the Microsoft Data Governance strategy"
    url: "https://techcommunity.microsoft.com/blog/microsoft-security-blog/a-next-step-in-the-evolution-of-the-microsoft-data-governance-strategy/4572227"
    primary: true
  - name: "Microsoft Partner Center"
    title: "Partner Center announcements, November 2026: Update on the Microsoft Data Governance strategy"
    url: "https://learn.microsoft.com/en-gb/partner-center/announcements/2026-november"
  - name: "DataGalaxy"
    title: "Microsoft Purview Data Governance is retiring: what happens next?"
    url: "https://www.datagalaxy.com/en/blog/microsoft-purview-data-governance-is-retiring-what-happens-next/"
related: []
card:
  figure: "12 Nov 2027"
  caption: "End of support for Microsoft Purview Data Governance"
---

Microsoft announced on 12 November 2026 that it is retiring **Microsoft Purview Data Governance**, with **support ending on 12 November 2027**. According to Microsoft's partner announcement, the retirement covers the Unified Catalog, Data Map, Workflows and the Microsoft Azure Purview solutions.

In a blog post, Microsoft said Microsoft Fabric is now its data governance solution and the **OneLake catalog** is "the single foundation for governing data across your entire estate". The company said the catalog can govern data outside OneLake through shortcuts, mirroring and supported connectors, and that governance is included in Fabric capacity rather than billed through separate meters.

**Purview stays focused on data security and compliance**, including classifying, labelling and protecting sensitive data and preventing data loss. Microsoft said customers with contractual obligations and those in highly regulated industries should engage their account team early, and that transition guidance is available.

Microsoft also acknowledged that "some organizations have needs that reach beyond what's in Fabric today", and said Fabric integrates with third-party providers such as Atlan, Alation, Collibra and Informatica. DataGalaxy, a competing catalog vendor, warns that manually curated descriptions, custom attributes and approval processes may need dedicated migration work.
