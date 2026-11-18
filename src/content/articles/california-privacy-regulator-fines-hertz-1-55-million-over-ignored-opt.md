---
title: "California privacy regulator fines Hertz $1.55 million over ignored opt-out preference signals"
date: 2026-11-17
dek: "The CalPrivacy Board also ordered retailer CC Filson Co. to halt device-based sales and sharing of data to adtech firms and to pay a $217,987 fine."
whyItMatters: "The Hertz terms read as a template for what CalPrivacy expects: a maintained inventory of trackers, a gate before new tags go live, and opt-out testing in every environment and tag container. Privacy and marketing technology teams should confirm that opt-out preference signals are actually propagated to every downstream tag and vendor, since the regulator stressed that companies cannot shift responsibility to others. With the Opt Me Out Act requiring browsers to offer such signals from January 2027, signal volumes are likely to grow."
categories: [privacy, regulation, metadata]
institutions: [cppa]
whoShouldCare: ["DPO", "Legal & compliance", "Data stewards", "Marketing technology owners"]
importance: 4
type: "Enforcement"
region: "US"
status:
  stage: "Decision"
  detail: "CalPrivacy Board decision; Hertz agreed to the fine"
whatToCheck:
  - "Test whether your websites and apps detect and honour opt-out preference signals in both staging and production, across browsers, mobile platforms and every tag management container."
  - "Check that you keep an inventory of tracking technologies and require a review before any new tracker is added to sites or apps."
  - "Confirm your published CCPA request metrics can separate opt-outs received via preference signals from other opt-out requests."
enforcement:
  case: cppa-hertz-opt-out-signals
  action: "Fine"
  authority: "California Privacy Protection Agency (CalPrivacy) Board"
  parties: "The Hertz Corporation"
  framework: "US state"
  jurisdiction: "California"
  amount: 1550000
  currency: "USD"
  law: "California Consumer Privacy Act (CCPA)"
  date: 2026-11-17
sources:
  - name: "California Privacy Protection Agency (CalPrivacy)"
    title: "Vehicle Rental Services Company Hertz to Pay $1.55 Million CCPA Fine, Adjust Privacy Practices"
    url: "https://privacy.ca.gov/2026/11/vehicle-rental-services-company-hertz-to-pay-1-55-million-ccpa-fine-adjust-privacy-practices/"
    primary: true
  - name: "The Record (Recorded Future News)"
    title: "California fines Hertz $1.5 million for breaking state data privacy law"
    url: "https://therecord.media/california-fines-hertz-state-data-privacy-law"
related: []
card:
  figure: "$1.55m"
  caption: "CCPA fine on Hertz for failing to process opt-out preference signals"
---

The California Privacy Protection Agency (CalPrivacy) Board has issued a decision requiring The Hertz Corporation to pay **$1.55 million** and change its practices to resolve claims under the California Consumer Privacy Act (CCPA). The Enforcement Division alleged that Hertz failed to process opt-out preference signals, did not tell consumers how it handled them and added unnecessary friction to opting out. Hertz agreed to the fine, according to The Record.

The decision requires quarterly testing of CCPA request methods, an inventory of tracking technologies with review before new ones go live on Hertz, Thrifty and Dollar sites and apps, and opt-out testing across staging and production, browsers, devices and all tag management containers. Published request metrics must show how many opt-outs came from preference signals.

In a separate decision, outdoor clothing retailer CC Filson Co. must stop **device-based sales and sharing to adtech companies within 30 days** until it certifies compliance with obligations including audits, tests and training, and pay $217,987. CalPrivacy said the amount reflects confidential financial information showing Filson could not pay a multi-million dollar fine.
