---
title: "Law firm says Delete Act deletions through DROP must reach AI-derived inferences, not just raw data"
date: 2026-11-24
dek: "Glancy Prongay Wolke & Rotter, writing for the IAPP, says brokers' profiling models make simple database deletion insufficient. It expects litigation over AI-derived data."
whyItMatters: "For brokers and firms that buy or enrich data from them, deletion has to propagate beyond source tables to derived scores, segments and model outputs linked to a consumer. That requires lineage from raw attributes to every inference and profile built on them, and matching logic that can find a person from the basic details DROP supplies. Teams should test whether their 45-day processing cycle actually deletes downstream derivatives and can evidence it."
categories: [privacy, regulation, metadata]
institutions: [cppa]
legislation: [california-delete-act]
whoShouldCare: ["DPO", "Legal & compliance", "Data stewards", "CDO"]
importance: 3
format: "Analysis"
byline:
  name: "Glancy Prongay Wolke & Rotter"
  role: "a law firm, writing for the IAPP"
type: "Regulation"
region: "US"
status:
  stage: "In force"
  detail: "Brokers must process DROP requests at least every 45 days since 1 August 2026"
sources:
  - name: "California Privacy Protection Agency (CalPrivacy)"
    title: "Delete Request and Opt-out Platform (DROP)"
    url: "https://privacy.ca.gov/drop/"
    primary: true
  - name: "IAPP"
    title: "Navigating DROP compliance after 1 Aug."
    url: "https://iapp.org/news/a/navigating-drop-compliance-after-1-aug"
related: []
card:
  figure: "45 days"
  caption: "Maximum interval between data brokers' DROP checks for deletion requests"
---

Attorneys at Glancy Prongay Wolke & Rotter, writing for the IAPP, argue that the end of the grace period for California's Delete Act exposes a clash between deletion duties and data brokers' business models. According to CalPrivacy, from 1 August 2026 registered brokers had to access its Delete Request and Opt-out Platform (DROP) **at least once every 45 days** to process deletion requests. One request reaches more than 600 brokers.

The authors note that brokers use AI and machine learning to score, rank and categorise consumers from scraped data. In their reading, the Act's definition of personal information covers **inferences used to build consumer profiles**, so deleting raw records is not enough.

The firm expects a wave of complex litigation over AI-derived data. Separately, CalPrivacy has [proposed rules](/news/calprivacy-proposes-delete-act-audit-rules-and-tighter-drop-deletion-p/) that would shorten the DROP cycle to 30 days and require matching across all of a broker's records.
