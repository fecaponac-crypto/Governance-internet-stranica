---
title: "UK NCSC reports marked rise in AI-assisted attacks using repurposed red-teaming frameworks"
date: 2026-11-24
dek: "The agency says attackers are exploiting old weaknesses such as leaked credentials, misconfigured infrastructure and unprotected APIs faster and more cheaply, and it sets out eight defensive questions."
whyItMatters: "The NCSC's first question is whether organisations know which systems are exposed to the internet and who is responsible for each, and it notes that compromised services are sometimes ones organisations have forgotten about, such as old websites and legacy equipment. Data and platform teams should check that secrets are kept out of repositories, that credentials are not over-privileged, and that identity and access settings have not drifted from their original design. The NCSC also advises collecting and retaining the logs needed to detect, investigate and recover from an incident."
categories: [security, ai-governance]
institutions: []
whoShouldCare: ["CISO", "CDO", "Data platform owners", "AI governance lead"]
importance: 4
type: "Guidance"
region: "UK"
status:
  stage: "Published"
  detail: "Published as an NCSC blog"
whatToCheck:
  - "Confirm that every internet-facing system and service, including old websites and legacy equipment, has someone responsible for it in your asset inventory."
  - "If your organisation publishes public code repositories, check them for committed credentials and enable pre-commit automation to prevent secrets being pushed."
  - "Review whether credentials and identity and access settings are over-privileged or have drifted from their original design, and apply rate limits to accounts, API tokens and authenticated sessions."
sources:
  - name: "National Cyber Security Centre (NCSC)"
    title: "Familiar weaknesses, exploited faster: defending against agentic cyber attacks"
    url: "https://www.ncsc.gov.uk/blogs/familiar-weaknesses-exploited-faster-defending-against-agentic-cyber-attacks"
    primary: true
  - name: "The Record (Recorded Future News)"
    title: "UK cyber agency seeing 'marked rise' in AI-driven attacks"
    url: "https://therecord.media/cyberattacks-uk-artificial-intelligence"
related: []
card:
  figure: "Since Sept 2026"
  caption: "NCSC has seen a marked rise in AI-assisted attacks using agentic offensive frameworks"
---

The UK's National Cyber Security Centre (NCSC) said it has seen **a marked rise in AI-assisted cyber attacks since September 2026**, driven by 'agentic offensive frameworks': red-teaming software in which a large language model plans attack steps, runs off-the-shelf security tools and adapts to the results. It said this activity has become "synonymous" with the ARTEX framework, and also named Cairn, PentAGI, RedAmon, Xalgorix and Darkmoon.

According to the NCSC, none of the exploited weaknesses is new. Agents target credentials committed to code repositories, infrastructure-as-code misconfigurations, default or missing authentication and weak APIs, then move through over-privileged accounts and flat networks. The current tools are noisy and therefore detectable, although that may change.

The guidance poses **eight questions**, covering asset exposure and ownership, removing services from the public internet, detection, patching, bot challenges, API rate limits, account creation and deception measures. It says nearly everything the NCSC has seen can be prevented by implementing cyber security best practice.
