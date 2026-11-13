---
title: "Microsoft to retire Purview Data Governance, ending support on 12 November 2027 in shift to Fabric"
date: 2026-11-13
dek: "The Unified Catalog, Data Map and Workflows are included, according to a report by catalog vendor DataGalaxy. Purview's data security and compliance tools continue, and the OneLake catalog in Fabric becomes Microsoft's governance experience."
whyItMatters: "Teams using Purview for glossaries, lineage and stewardship have a one-year window to move curated business metadata that cannot simply be rediscovered from source systems. According to DataGalaxy, manually written descriptions and classifications may require dedicated migration work, while custom attributes and approval processes may not have exact equivalents in a new platform. Lineage that supports impact analysis or regulatory evidence should be checked to confirm it survives the move. Because security labels and DLP stay in Purview while the catalog moves to Fabric, teams should also review how governance and protection controls will stay linked."
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
  - name: "DataGalaxy"
    title: "Microsoft Purview Data Governance is retiring: what happens next?"
    url: "https://www.datagalaxy.com/en/blog/microsoft-purview-data-governance-is-retiring-what-happens-next/"
related: []
card:
  figure: "12 Nov 2027"
  caption: "End of support for Microsoft Purview Data Governance"
---

Microsoft announced on 12 November 2026 that it is retiring its standalone Purview Data Governance offering, with **support ending on 12 November 2027**, according to a blog post by DataGalaxy, a competing catalog vendor. The report says the retirement covers the Purview Unified Catalog, Data Map, Workflows and classic Azure Purview governance solutions.

According to the report, Microsoft is moving governance into Microsoft Fabric, with the **OneLake catalog** positioned as its successor. The OneLake catalog offers discovery, ownership information, lineage and endorsements, and can cover external data through shortcuts, mirroring and connectors. Purview Data Security and Compliance, including sensitivity labels and data loss prevention, is not affected.

DataGalaxy says Microsoft acknowledges that some organisations have governance requirements beyond what Fabric currently offers. It cautions that the move should not be treated as a "guaranteed one-to-one replacement" of every existing governance capability.

*Editor's note: This story relies solely on a blog post by DataGalaxy, a competing data catalog vendor, not on Microsoft's own announcement.*
