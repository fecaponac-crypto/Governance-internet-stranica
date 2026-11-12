---
title: "CalPrivacy advances CCPA amendments requiring opt-out signals to be honoured before tracking cookies fire"
date: 2026-11-10
dek: "Draft text extends opt-outs to linked pseudonymous profiles, bans cookie syncing after a GPC signal and adds signal-specific request metrics for large data handlers. A 45-day comment period is next."
whyItMatters: "The draft turns opt-out handling into a data lineage and identity-resolution problem: if your organisation links browsers and devices into a pseudonymous or master profile, a single GPC signal must propagate to every linked record and downstream third party. Tag and consent management sequencing becomes a compliance control, since tracking that fires before signal detection is treated as non-compliance. Large data handlers will also need request logs that record the channel each opt-out arrived through, so that annual metrics can be produced."
categories: [privacy, regulation, mdm]
institutions: [cppa]
legislation: [california-ccpa-regulations]
whoShouldCare: ["DPO", "Legal & compliance", "Data stewards", "Marketing technology owners"]
importance: 4
type: "Regulation"
region: "US"
status:
  stage: "Proposal"
  detail: "formal 45-day public comment period yet to open"
whatToCheck:
  - "Test whether advertising and analytics cookies, pixels or cookie-syncing scripts on your websites fire before your CMP or tag manager has detected a GPC signal."
  - "Map where browsers and devices are linked into pseudonymous or customer profiles and confirm that an opt-out received on one is applied to all linked records and notified to third parties."
  - "If you fall under the CCPA metrics reporting rule, confirm that your request-handling system records whether each opt-out came from a preference signal."
sources:
  - name: "California Privacy Protection Agency"
    title: "Proposed Text of Regulations: Opt-Out Preference Signals (OOPS)"
    url: "https://cppa.ca.gov/meetings/materials/20261105_06_09_text.pdf"
    primary: true
  - name: "Hunton Privacy & Information Security Law Blog"
    title: "CalPrivacy Proposes Amendments to Strengthen Opt-Out Preference Signal Compliance"
    url: "https://www.hunton.com/privacy-and-cybersecurity-law-blog/calprivacy-proposes-amendments-to-strengthen-opt-out-preference-signal-compliance"
related: [cppa-staff-propose-naming-global-privacy-control-in-ccpa-opt-out-signa]
card:
  figure: "50,000"
  caption: "Businesses CalPrivacy estimates would be in scope of the opt-out signal amendments"
---

California's privacy regulator, CalPrivacy, voted unanimously on 6 November 2026 to advance proposed amendments to its CCPA regulations on opt-out preference signals such as Global Privacy Control (GPC). According to Hunton, the agency estimates that about **50,000 businesses** would be in scope and says the changes largely clarify existing duties rather than add new ones.

The draft text states that a business letting advertising cookies or pixels fire before its consent or tag management tools check for a GPC signal has not complied "as soon as feasibly possible". Opt-outs must extend to pseudonymous profiles, including devices linked through matching techniques such as fingerprinting, and third-party cookie syncing must be blocked. Businesses already subject to metrics reporting, including those handling data of **10 million or more consumers** a year, would have to count signal-based opt-outs separately.

A formal 45-day public comment period is due to open; the sources give no date.
