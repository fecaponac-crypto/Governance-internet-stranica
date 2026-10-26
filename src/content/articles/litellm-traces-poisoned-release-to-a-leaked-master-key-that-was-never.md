---
title: "LiteLLM traces poisoned release to a leaked master key that was never revoked"
date: 2026-10-26
dek: "A root-cause analysis says a key exposed in May led to an organisation owner's unscoped GitHub token, stolen CI secrets and a malicious v1.107.0 release on PyPI and container registries."
whyItMatters: "The chain began with a basic credential-hygiene failure: a leaked secret was removed from view but not rotated, and an AI agent tool held an owner-level personal token rather than a scoped service identity. Teams running AI agents or LLM gateways should treat their secrets, inference API keys and agent configurations as governed assets with owners, scopes and rotation records. The temporary relaxation of release approvals also shows how exceptions to controls need expiry dates and monitoring."
categories: [security, ai-industry, platforms]
institutions: []
whoShouldCare: ["CISO", "AI governance lead", "Platform engineering leads", "Data engineering leads"]
importance: 4
type: "Case study"
region: "Global"
status:
  stage: "Published"
  detail: "LiteLLM says it will share process changes the following week"
whatToCheck:
  - "Check whether litellm 1.107.0 was installed on any internet-connected machine and, if so, change every password and access key, as LiteLLM advises."
  - "Confirm that secrets known to have been exposed, even briefly, were actually revoked rather than just deleted from the repository."
  - "Review whether AI agent tools are authenticated with scoped service accounts instead of personal owner-level tokens."
sources:
  - name: "LiteLLM"
    title: "The attack chain behind the v1.107.0 LiteLLM release"
    url: "https://docs.litellm.ai/blog/security-incident-oct-21-2026-attack-chain"
    primary: true
  - name: "The Record (Recorded Future News)"
    title: "Popular AI tool LiteLLM says unrevoked key allowed hackers to target users"
    url: "https://therecord.media/litellm-hackers-ai-malware"
related: []
card:
  figure: "49,000"
  caption: "Approximate downloads of the compromised LiteLLM package, according to Wiz"
---

LiteLLM, an open-source tool used by AI developers, has published a root-cause analysis of the compromised **litellm 1.107.0** release of 21 October. A configuration file containing the master key to its internal Agent Platform was committed to a public repository on 27 May. The commit was overwritten, but **the key was never revoked**.

On 10 October an attacker used the key to retrieve the GitHub CLI token of an organisation owner, which was neither scoped down nor tied to a service account. Using CI workflows, the attacker exfiltrated two maintainers' tokens. Earlier that week, the release process had been relaxed to let any two engineers trigger and approve a release: the attacker used one stolen token to trigger the malicious release and the other to approve it. The malicious artefacts were live for about two hours.

According to Wiz, cited by The Record, the package was downloaded about 49,000 times. LiteLLM advises anyone who installed version 1.107.0 on an internet-connected computer to change every password and access key.

*Editor's note: This article relies on LiteLLM's own incident analysis and a secondary news report; download figures come from Wiz as reported by The Record.*
