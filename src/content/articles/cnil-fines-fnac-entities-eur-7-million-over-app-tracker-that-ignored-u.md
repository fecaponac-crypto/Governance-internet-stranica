---
title: "CNIL fines Fnac entities EUR 7 million over app tracker that ignored users' refusal of consent"
date: 2026-10-29
dek: "The tracker sent browsing data to a third-party domain to personalise product recommendations and train a recommendation algorithm. Fnac must prove its new consent tool works within a month or face daily penalties."
whyItMatters: "The decision confirms that recommendation engines and the training of recommendation models are not exempt from consent under French tracker rules, even when they run inside a retailer's own app via API calls rather than browser cookies. Privacy and data teams should trace which app events and identifiers flow to third-party domains and confirm that a recorded refusal actually stops them. Where behavioural data feeds model training, lineage should show the consent status attached to each record so non-consented data can be excluded."
categories: [privacy, regulation, ai-governance]
institutions: [cnil]
whoShouldCare: ["DPO", "Legal & compliance", "Data stewards", "AI governance lead"]
importance: 4
type: "Enforcement"
region: "France"
status:
  stage: "Decision"
  detail: "Injunction requires proof of compliant consent within one month of notification"
whatToCheck:
  - "Check whether your mobile apps send user identifiers and product-view events to third-party domains via APIs before or despite a consent refusal."
  - "Verify that data used to train recommendation or personalisation models is filtered by recorded consent status."
  - "Confirm your consent management tool covers app-to-server API calls, not only browser cookies."
sources:
  - name: "CNIL"
    title: "Cookies et application mobile : sanctions de 7 millions d’euros à l’encontre des sociétés FNAC DARTY PARTICIPATIONS ET SERVICES et FNAC DIRECT"
    url: "https://www.cnil.fr/fr/sanction-cookies-app-fnac"
    primary: true
related: []
card:
  figure: "EUR 7m"
  caption: "CNIL fine on two Fnac companies for app tracking without consent"
---

France's CNIL fined FNAC DARTY PARTICIPATIONS ET SERVICES and FNAC DIRECT a combined **EUR 7 million** on 22 October 2026 for breaching the cookie and tracker rules in Article 82 of the French Data Protection Act. The first company was fined EUR 6 million and the second EUR 1 million.

The case followed a complaint by noyb and a CNIL inspection of the Fnac mobile app in March 2024. Inspectors found the app sent API requests to a third-party domain containing a Fnac-assigned user identifier and activity data such as products viewed. This data was used to show personalised and related products and to train the recommendation algorithm, even where users had declined tracking.

The CNIL said such uses fall outside Article 82's consent exemptions. The companies must show within **one month of notification** that their new tool collects consent where required, or pay EUR 10,000 per day of delay.
