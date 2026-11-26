---
title: "German DPAs bar credit checks before customers pick a payment method and clarify scope of new § 37a BDSG"
date: 2026-11-26
dek: "At its 112th conference the DSK also said the new scoring rule is no standalone legal basis, and updated its hospital information systems guidance on access rights and cloud use."
whyItMatters: "Online retailers and payment providers operating in Germany should map where in the checkout flow credit queries are triggered and whether any occur before a risky payment method is selected. Teams running scoring models need a GDPR legal basis beyond § 37a BDSG, which the DSK says creates none: under legitimate interests the provision's statutory assessments should be weighed in the balancing, while under Article 6(1)(b) or (c) the § 37a(2) and (3) catalogues count in the necessity test where a listed criterion is used, so recording which criteria models use helps. Hospitals should review role-based access rights against the updated guidance, which supervisors will use as their benchmark in audits."
categories: [privacy, regulation, security]
institutions: [german-dpas]
legislation: [eu-gdpr]
whoShouldCare: ["DPO", "Legal & compliance", "Data stewards", "CISO"]
importance: 4
type: "Guidance"
region: "Germany"
status:
  stage: "Published"
  detail: "DSK resolutions adopted at its 112th conference, 24–26 November 2026"
whatToCheck:
  - "Check whether your checkout or ordering process triggers a credit check before the customer selects invoice, instalment or another payment method with default risk."
  - "Confirm that scoring processing relies on a GDPR legal basis rather than § 37a BDSG alone, and document which listed § 37a criteria the model uses."
  - "If you operate hospital information systems, compare current patient-data access rights and cloud arrangements with the updated DSK guidance."
sources:
  - name: "LfDI Baden-Württemberg / Datenschutzkonferenz (DSK)"
    title: "Pressemitteilung der DSK: 112. Datenschutzkonferenz vom 24.-26.11.2026"
    url: "https://www.baden-wuerttemberg.datenschutz.de/112dsk-bonitaet-scoring-krankenhaussysteme-pm/"
    primary: true
related: [german-dpas-publish-third-version-of-technical-requirements-for-hospit]
card:
  figure: "§ 37a BDSG"
  caption: "New German scoring rule, in force since 20 Nov 2026, is not a legal basis, says DSK"
---

Germany's federal and state data protection authorities (DSK) adopted several resolutions at their 112th conference, held from 24 to 26 November 2026.

The DSK said credit checks are in principle lawful only **after a customer has chosen a payment method carrying default risk**, such as invoice or instalments. Checking creditworthiness in advance to decide which payment options to show is in principle unlawful, including where shops, marketplaces or booking portals use external payment providers. Credit reference agencies must design their products so that unlawful queries are avoided as far as possible.

On **§ 37a BDSG, in force since 20 November 2026**, the DSK said it provides an exception for automated decisions under Article 22 GDPR but no independent legal basis for processing. Its criteria should feed into legitimate-interest balancing and necessity tests for other scoring. The DSK also updated its guidance on hospital information systems, tightening access-rights requirements and addressing cloud use.
