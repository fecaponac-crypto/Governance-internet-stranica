---
title: "CNIL publishes final recommendation on session replay tools, confirming prior consent is required"
date: 2026-11-05
dek: "The French regulator's guidance covers tool providers and site or app publishers, and asks for masking of irrelevant data, limits on sessions recorded and masking of chatbot conversations."
whyItMatters: "Session replay scripts are often added by product or UX teams without passing through privacy review, yet the CNIL now treats them as consent-based trackers with no exemption. Privacy and analytics owners should inventory where these tools run, confirm they fire only after consent, and record the purposes defined before deployment. Masking settings are now a governance control: form fields, authentication areas and chatbot content need to be masked by configuration, not left to defaults."
categories: [privacy, regulation, analytics]
institutions: [cnil]
whoShouldCare: ["DPO", "Legal & compliance", "Analytics and product teams", "CISO"]
importance: 4
type: "Guidance"
region: "France"
status:
  stage: "Published"
  detail: "Final version after public consultation from February to May 2026"
whatToCheck:
  - "Identify every website and app where a session replay tool is deployed and confirm it loads only after the user has given prior consent."
  - "Check that the consent interface mentions session replay specifically at the first layer of information, as the final recommendation now advises."
  - "Review masking settings so that irrelevant data, form entries, authentication areas and chatbot questions and answers are not captured."
sources:
  - name: "CNIL"
    title: "Outils de rejeu de session : la CNIL publie sa recommandation pour guider les acteurs"
    url: "https://www.cnil.fr/fr/rejeu-de-session-recommandation"
    primary: true
related: [cnil-fines-fnac-entities-eur-7-million-over-app-tracker-that-ignored-u]
card:
  figure: "Article 82"
  caption: "Session replay tools fall under France's tracker rule, with no exemption from consent"
---

France's CNIL has published its final recommendation on session replay tools. These tools use trackers to record or reconstruct a user's full journey on a website or app, including mouse movements, taps, clicks, scrolling and sometimes form entries. The recommendation is aimed at both **tool providers and the publishers that deploy them**.

The CNIL states that these tools fall under article 82 of the French Data Protection Act and that **no consent exemption applies**, so prior consent is required under its existing cookie rules. Purposes must be set before deployment, not after data is collected. Recommended measures include masking irrelevant data, limiting the number of sessions collected and limiting the use of identifiers.

After a public consultation held between February and May 2026, the final text adds specific first-layer consent information, masking of mouse movements in some areas to avoid capturing authentication codes, and masking of chatbot conversations. The CNIL plans to support organisations, including through a webinar.
