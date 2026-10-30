---
title: "GSA watchdog finds 116 controlled unclassified files open to all staff in agency Google Drive"
date: 2026-10-30
dek: "Auditors traced the oversharing to weak data loss prevention management, including outdated search terms, OCR left switched off and an unnoticed 15 MB file-size limit."
whyItMatters: "The failure was internal oversharing rather than an external breach, which is a risk many organisations overlook in collaboration suites. Teams should check whether their DLP rules actually reflect their own classification guidance, whether OCR and file-size limits leave blind spots for scanned or large files, and whether 'share with whole organisation' permissions on sensitive files require approval. Consistent naming or labelling conventions for sensitive documents give DLP and stewards something reliable to detect."
categories: [security, privacy, metadata]
institutions: []
whoShouldCare: ["CISO", "DPO", "Data stewards", "CDO"]
importance: 3
type: "Supervision"
region: "US"
status:
  stage: "Published"
  detail: "GSA's CIO agreed with all recommendations"
sources:
  - name: "GSA Office of Inspector General"
    title: "Controlled Unclassified Information in GSA's Google Drive Was Improperly Exposed"
    url: "https://www.gsaig.gov/content/controlled-unclassified-information-gsas-google-drive-was-improperly-exposed"
    primary: true
  - name: "CDO Magazine"
    title: "GSA Inspector General Finds 116 CUI Files Improperly Exposed in Google Drive"
    url: "https://www.cdomagazine.tech/us-federal-news-bureau/gsa-inspector-general-finds-116-cui-files-improperly-exposed-in-google-drive"
related: []
card:
  figure: "116 files"
  caption: "CUI files found shared with all GSA users in the agency's Google Drive"
---

The Office of Inspector General of the US General Services Administration (GSA) found **116 files containing controlled unclassified information (CUI)** shared with all GSA users during a limited search of the agency's Google Drive. According to GSA management, the drive holds about 2.5 million documents. The exposed material included Social Security numbers, dates of birth, building blueprints, counterterrorism methods and vendor pricing proposals.

The auditors said GSA's data loss prevention (DLP) tool missed the files. Search terms had not been fully reviewed each year, many terms from GSA's own CUI guidance were missing, optical character recognition was not enabled, and staff were unaware of a **15-megabyte file-size limit**. GSA also had no approval process for sharing CUI and no standard naming convention.

GSA's Chief Information Officer agreed with all seven recommendations, which include restricting access and notifying affected individuals.
