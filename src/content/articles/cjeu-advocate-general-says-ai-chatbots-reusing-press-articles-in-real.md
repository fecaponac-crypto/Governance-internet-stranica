---
title: "CJEU Advocate General says AI chatbots reusing press articles in real time may infringe publishers' rights"
date: 2026-11-03
dek: "In the first generative AI case before the Court of Justice, Maciej Szpunar says LLM training is generally covered by the text and data mining exception, but chatbot answers built on retrieved articles may not be."
whyItMatters: "Organisations that build or deploy RAG-based assistants over web or licensed press content should be able to show how retrieved sources are accessed. They should also show that technical measures such as paywalls and scraping restrictions are respected, and how outputs are kept from reproducing source wording. The opinion points to provenance metadata for retrieval sources and output controls as the evidence of 'appropriate measures' that would decide liability. If the Court follows it, AI governance teams would treat training and real-time retrieval as separate risks."
categories: [ai-governance, regulation, ai-industry]
institutions: [cjeu]
whoShouldCare: ["AI governance lead", "Legal & compliance", "Data stewards", "CDO"]
importance: 4
type: "Regulation"
region: "EU"
status:
  stage: "Non-binding opinion"
  detail: "Court of Justice judgment to follow at a later date"
whatToCheck:
  - "Check whether your RAG or web-grounding pipelines record source provenance and respect paywalls and anti-scraping technical measures."
  - "Review whether chatbot outputs drawing on press content summarise facts or reproduce the articles' wording in a recognisable way."
  - "Document the controls you use to counter reuse of protected press publications, as the opinion links provider liability to the absence of such measures."
sources:
  - name: "Court of Justice of the European Union"
    title: "Press release No 155/26: Opinion of Advocate General Szpunar in Case C-250/25 Like Company"
    url: "https://curia.europa.eu/site/upload/docs/application/pdf/2026-11/cp260155en.pdf"
    primary: true
related: [anthropic-says-claude-bypassed-a-paywall-to-retrieve-georgia-vote-coun, meta-removes-ai-crawling-terms-language]
card:
  figure: "C-250/25"
  caption: "First generative AI case at the CJEU: Like Company v Google (Gemini)"
---

Advocate General Maciej Szpunar has delivered his opinion in **Case C-250/25 Like Company**, a reference from the Budapest Regional Court. Like Company, a Hungarian web portal operator, claims Google's Gemini chatbot used its articles for training and reproduced them between June 2023 and May 2024.

He advises the Court to declare the two training questions inadmissible as hypothetical. He adds that training an LLM on protected material is, as a rule, **freely permitted under the text and data mining exception**. On chatbot answers produced through retrieval-augmented generation, he says the press publisher's right may be infringed. This depends on whether access was unlawful, for example by circumventing a paywall or anti-scraping measures, and on whether the answer reuses the article's expression so recognisably that users need not read the original.

Providers would be liable where such use is inherent to their business model or where they have not taken credible, effective countermeasures. The opinion is not binding, and the judges have begun deliberating.
