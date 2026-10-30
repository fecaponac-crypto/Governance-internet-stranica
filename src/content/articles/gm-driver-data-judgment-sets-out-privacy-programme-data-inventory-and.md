---
title: "GM driver-data judgment sets out privacy programme, data inventory and consent terms running to 2046"
date: 2026-10-30
dek: "Oregon's stipulated judgment, one of the parallel multistate settlements, details what GM must build from 30 November 2026, including a disclosure inventory and a strict test for deidentified data."
whyItMatters: "The judgment turns familiar data governance controls into enforceable obligations: a maintained inventory of which data categories go to which third parties, data protection assessments before selling data or sharing location data, and due diligence and contract terms for service providers. Its definitions are also notable. 'Covered' data explicitly includes algorithmically derived data. Any identifier that can be linked back to a VIN makes data 'reasonably linkable'. Precise location is anything finer than roughly a 1,850-foot radius. Teams handling connected-device or telematics data can use these definitions as a benchmark for their own deidentification and classification rules."
categories: [privacy, regulation, metadata]
institutions: []
whoShouldCare: ["DPO", "Chief privacy officer", "Data stewards", "Legal & compliance"]
importance: 4
type: "Enforcement"
region: "US"
status:
  stage: "Decision"
  detail: "Stipulated judgment, appeal waived; terms effective 30 November 2026"
whatToCheck:
  - "Check whether your data inventory records, for each category of device or telemetry data, which third parties and affiliates receive it."
  - "Test whether data you label as deidentified is still linkable through persistent identifiers such as device or vehicle IDs, or through linkable alternative identifiers."
  - "Confirm that consent flows treat silence or inaction as a refusal and require separate consent for each unrelated feature that collects or shares data."
deadlines:
  - date: 2026-11-30
    what: "Effective date of GM judgment; 180-day privacy programme and 60-day enrolment procedure clocks start"
  - date: 2046-01-13
    what: "GM privacy programme obligations under the Oregon judgment end"
sources:
  - name: "Oregon Department of Justice"
    title: "Stipulated General Judgment and Money Award, State of Oregon v. General Motors LLC et al."
    url: "https://www.doj.state.or.us/wp-content/uploads/2026/10/2026-10-29-SGJ-Final-with-Exhibit-and-Cert.pdf"
    primary: true
  - name: "IAPP"
    title: "A view from DC: The one-two punch is a knockout for driver privacy"
    url: "https://iapp.org/news/a/a-view-from-dc-the-one-two-punch-is-a-knockout-for-driver-privacy"
related: [gm-agrees-to-pay-220-million-to-36-attorneys-general-over-sale-of-driv]
card:
  figure: "2046"
  caption: "GM's court-ordered privacy programme obligations run until 13 January 2046"
---

The Oregon Department of Justice has published its stipulated general judgment with General Motors and OnStar. It is one of the parallel judgments in the multistate driver-data settlement, which IAPP reports totals USD220 million across 36 attorneys general. GM agreed to the terms without admitting liability, and the parties waived their right to appeal.

The terms take effect on **30 November 2026**. Within 180 days, GM must run a documented privacy programme overseen by a chief privacy officer, with obligations lasting until 13 January 2046. The officer reports at least quarterly to the general counsel, annually to the CEO and annually to the board. GM must also keep an inventory of driver data that OnStar collects and discloses, assess new high-risk processing in advance and obtain separate consent for each feature.

**Data linked to a VIN or a garage address cannot count as deidentified.** Consumers who do not respond within 10 days of an enrolment notice must be treated as having declined.
