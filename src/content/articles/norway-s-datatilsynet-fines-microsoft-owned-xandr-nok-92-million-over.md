---
title: "Norway's Datatilsynet fines Microsoft-owned Xandr NOK 92 million over sharing Grindr users' data"
date: 2026-11-03
dek: "The regulator's largest fine ever finds the ad-tech firm was a joint controller with Grindr and could not rely on the app to secure explicit consent for real-time bidding."
whyItMatters: "The decision confirms that a downstream recipient cannot rely on an upstream partner's consent claim: each controller must itself ensure, and be able to prove, a lawful basis for its own processing. Teams receiving personal data from partners, especially through ad-tech or data-sharing chains, should check whether they hold evidence of valid consent or another basis rather than contractual assurances alone. The finding that app usage alone can reveal special-category data also matters for data classification: metadata about which service a person uses may need the same protection as sensitive attributes."
categories: [privacy, regulation]
institutions: [datatilsynet-no]
whoShouldCare: ["DPO", "Legal & compliance", "Data stewards", "Marketing data owners"]
importance: 4
type: "Enforcement"
region: "Norway"
status:
  stage: "Decision"
  detail: "Regulator says Xandr did not appeal and the decision is final"
whatToCheck:
  - "Check whether, for personal data received from partners, you can independently evidence a valid lawful basis for your own processing rather than relying on the partner's assurance."
  - "Review whether any data-sharing or bidding arrangements could make you a joint controller with the data source, and whether responsibilities are documented accordingly."
  - "Check whether your data classification treats signals that indirectly reveal sensitive traits, such as use of a particular app, as special-category data requiring explicit consent."
enforcement:
  case: datatilsynet-xandr-grindr-rtb
  action: "Fine"
  authority: "Datatilsynet (Norway)"
  parties: "Xandr (formerly AppNexus, now part of Microsoft)"
  framework: "GDPR"
  jurisdiction: "Norway"
  amount: 92000000
  currency: "NOK"
  law: "Norwegian data protection rules (GDPR); explicit consent for special-category data"
  date: 2026-11-03
  final: true
sources:
  - name: "Datatilsynet"
    title: "Datatilsynet gir Microsoft-selskap 92 millioner i gebyr"
    url: "https://www.datatilsynet.no/aktuelt/aktuelle-nyheter-2026/datatilsynet-gir-microsoft-selskap-92-millioner-i-gebyr/"
    primary: true
related: []
card:
  figure: "NOK 92m"
  caption: "Datatilsynet's largest fine ever, imposed on Xandr over Grindr users' data in ad auctions"
---

Norway's data protection authority, Datatilsynet, has fined ad-tech company Xandr, formerly AppNexus and now part of Microsoft, **NOK 92 million**, the highest fine it has ever imposed. The case began with a 2020 complaint by the Norwegian Consumer Council (Forbrukerrådet).

Xandr acted as both seller and buyer in real-time bidding auctions, passing data about Grindr users in Norway to potentially thousands of other companies. The regulator held that being a Grindr user indicates sexual orientation, so **explicit consent was required**. Xandr argued it believed Grindr had collected consent, but Datatilsynet found the two were joint controllers and that Xandr never verified that consent was valid. The breaches ran from July 2018 to April 2020.

The fine was based on Xandr's own turnover, not Microsoft's. Datatilsynet says Xandr has not appealed and the decision is final.
