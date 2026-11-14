---
title: "Italy's Garante fines Meta €805 million over Facebook app's access to Android photo galleries"
date: 2026-11-14
dek: "The regulator found the gallery suggestions feature accessed photos, videos and metadata without specific consent, and rejected Meta's argument that Ireland's DPC should lead under a one-stop-shop."
whyItMatters: "The Garante held that any access to information on a smartphone requires free and informed consent under Article 122, regardless of whether data is transmitted or harm results. It rejected Meta's objection that the Irish authority was competent, on the grounds that the ePrivacy rules do not provide for a one-stop-shop. App owners should check whether broad operating-system permissions are reused for secondary features, and whether those features are enabled by default."
categories: [privacy, regulation]
institutions: [garante]
whoShouldCare: ["DPO", "Legal & compliance", "Product and app development leads", "Data stewards"]
importance: 5
type: "Enforcement"
region: "Italy"
status:
  stage: "Decision"
  detail: "Meta has 60 days to make the feature opt-in with separate consent"
whatToCheck:
  - "Map mobile app features that read device storage, such as photos or files, and confirm each one has its own specific consent, not a single app-wide permission."
  - "Check whether features that access device content are switched on by default, including for users who granted permissions earlier."
  - "Review whether processing of EU device data relies on the GDPR one-stop-shop where ePrivacy-based national rules, such as Article 122 in Italy, may instead apply."
enforcement:
  case: garante-meta-facebook-gallery
  action: "Fine"
  authority: "Garante per la protezione dei dati personali"
  parties: "Meta Platforms Ireland Limited (fined €805 million and ordered to change the Facebook gallery suggestions feature)"
  framework: "ePrivacy and cookies"
  jurisdiction: "Italy"
  amount: 805000000
  currency: "EUR"
  law: "Article 122 of the Italian Privacy Code (transposing the ePrivacy Directive)"
  date: 2026-11-14
sources:
  - name: "Garante per la protezione dei dati personali"
    title: "Facebook: il Garante Privacy sanziona Meta per 805 milioni di euro"
    url: "https://www.garanteprivacy.it/web/guest/home/docweb/-/docweb-display/docweb/10321080"
    primary: true
related: [cnil-fines-fnac-entities-eur-7-million-over-app-tracker-that-ignored-u]
card:
  figure: "€805m"
  caption: "Garante fine on Meta over Facebook app's access to Android photo galleries"
---

Italy's Garante has fined Meta Platforms Ireland Limited **€805 million**. It found that the Facebook app for Android accessed photos, videos and related metadata on Italian users' phones without specific consent or adequate information. The case concerns the "suggestions from your gallery" feature, available since 2023. The inquiry began in July 2025 after a complaint from the Bolzano consumer protection centre.

The Garante said gallery access relied on a single app-wide permission behind a generic prompt and that the feature was switched on by default. It found a breach of **Article 122 of the Italian Privacy Code**, which transposes the ePrivacy directive. Because ePrivacy has no one-stop-shop, it rejected Meta's claim that the Irish authority was competent.

Within 60 days, Meta must obtain separate, specific consent and keep the feature off by default, including for users who already granted permission. Use of the content to train AI was outside the case; Meta denies such use.
