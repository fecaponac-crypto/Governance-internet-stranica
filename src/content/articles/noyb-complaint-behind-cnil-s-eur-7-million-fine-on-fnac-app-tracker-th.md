---
title: "noyb complaint behind CNIL's EUR 7 million fine on Fnac app tracker that fed recommendation algorithm"
date: 2026-10-29
dek: "The fine traces back to a 2023 noyb complaint. The CNIL found the Fnac app sent browsing data to a third party without consent, both to show product recommendations and to train the recommendation algorithm."
whyItMatters: "The decision treats training a recommendation model on app browsing data as non-exempt tracking, so consent is needed before the data is collected, not only before ads are shown. Teams should check which SDKs and server-side API calls in their mobile apps send user identifiers and activity data to third parties. They should also confirm that a user's refusal of consent actually stops those calls. Data feeding personalisation or model training should be tagged in the data inventory with the consent state under which it was collected."
categories: [privacy, regulation, ai-governance]
institutions: [cnil]
whoShouldCare: ["DPO", "Legal & compliance", "Data stewards", "AI governance lead"]
importance: 3
type: "Enforcement"
region: "France"
status:
  stage: "Decision"
  detail: "Injunction with EUR 10,000 daily penalty if consent compliance is not shown within a month"
enforcement:
  case: cnil-fnac-app-trackers
  action: "Fine"
  authority: "CNIL"
  parties: "FNAC DARTY PARTICIPATIONS ET SERVICES; FNAC DIRECT"
  framework: "ePrivacy and cookies"
  jurisdiction: "France"
  amount: 7000000
  currency: "EUR"
  law: "Article 82 of the French Data Protection Act"
  date: 2026-10-22
sources:
  - name: "CNIL"
    title: "Cookies and mobile application: 7 million euros fine against FNAC DARTY PARTICIPATIONS ET SERVICES and FNAC DIRECT"
    url: "https://www.cnil.fr/en/sanction-app-cookies-fnac"
    primary: true
  - name: "noyb"
    title: "noyb win: French electronics retailer Fnac Darty fined €7 million"
    url: "https://noyb.eu/en/noyb-win-french-electronics-retailer-fnac-darty-fined-eu7-million"
related: [cnil-fines-fnac-entities-eur-7-million-over-app-tracker-that-ignored-u]
card:
  figure: "EUR 7 million"
  caption: "CNIL fine on Fnac entities over an app tracker that ran without users' consent"
---

France's CNIL has fined FNAC DARTY PARTICIPATIONS ET SERVICES and FNAC DIRECT **EUR 7 million** under Article 82 of the French Data Protection Act. The decision is dated 22 October 2026 and was published on 29 October. The case began with a complaint that noyb filed in September 2023, one of three it lodged in France that month.

A CNIL inspection in March 2024 found that the mobile app sent API requests to a third-party domain. Each request carried a Fnac-assigned user identifier and activity data such as the products viewed. The data was used to display personalised recommendations and to train the recommendation algorithm. The CNIL held that neither purpose falls within the Article 82 exemptions, so both required prior consent.

The companies must show **within one month of notification** that their new tool obtains consent where needed. Otherwise they face a daily penalty of EUR 10,000.
