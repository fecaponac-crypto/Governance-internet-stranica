---
title: "CrowdStrike says China-nexus group VAPOR PANDA used ARTEX AI agents to target more than 200 organisations"
date: 2026-11-05
dek: "The campaign, which CrowdStrike says began on 17 October, paired the DeepSeek model with agentic tooling and, in one case, used mail-server keys likely not rotated since a 2022 directory export."
whyItMatters: "In the Greek case, keys likely unrotated since a 2022 directory export were still usable, according to CrowdStrike, which shows that old exports and backups holding authentication keys can become attack material. Data owners and security teams should inventory where such exports and backups are kept, apply retention and deletion rules to them, and rotate any secrets they contain. Agent-driven attacks test many paths in parallel, including cloud roles with broad command rights, so access reviews should cover those cloud roles as well as human accounts."
categories: [security, ai-industry, ai-governance]
institutions: []
whoShouldCare: ["CISO", "Data owners", "AI governance lead", "IT operations"]
importance: 3
type: "Research"
region: "Global"
status:
  stage: "Published"
  detail: "Threat intelligence findings published by CrowdStrike"
sources:
  - name: "CrowdStrike"
    title: "VAPOR PANDA uses ARTEX to scale global campaign"
    url: "https://www.crowdstrike.com/en-us/blog/vapor-panda-uses-artex-to-scale-global-campaign/"
    primary: true
  - name: "Data Privacy + Cybersecurity Insider (Robinson+Cole)"
    title: "VAPOR PANDA Using AI Pen Testing Platform to Enhance Hacking Speed"
    url: "https://www.dataprivacyandsecurityinsider.com/2026/11/vapor-panda-using-ai-pen-testing-platform-to-enhance-hacking-speed/"
related: [litellm-traces-poisoned-release-to-a-leaked-master-key-that-was-never, independent-test-finds-deepseek-model-can-bypass-shutdown-and-leave-fi]
card:
  figure: "200+"
  caption: "Organisations targeted by VAPOR PANDA with ARTEX AI agents, according to CrowdStrike"
---

CrowdStrike says its OverWatch team observed a campaign by the China-nexus adversary VAPOR PANDA that began on 17 October 2026. The group used ARTEX, an agentic intrusion framework, with the DeepSeek LLM and a second, unconfirmed commercial LLM against **more than 200 organisations worldwide**. Targets included foreign ministries, US pharmaceutical, semiconductor and defence firms, think tanks and telecoms providers.

According to CrowdStrike, it confirmed post-exploitation activity at nine organisations, and it describes BLOODALCHEMY backdoor deployments at a Middle East interior ministry and a Latin American foreign ministry. A human operator steered agents that ran several engagements in parallel. One intrusion consumed roughly 1.4 billion input tokens. Against a Greek government entity, the operator supplied the agent with a **2022 mail-server directory export** containing authentication keys that had likely not been rotated since the export.

CrowdStrike recommends rotating keys held in historical backups and exports, enforcing SAML signature validation and IMDSv2, and hunting for ARTEX markers. It has also published indicators of compromise.

*Editor's note: This article relies on CrowdStrike's own threat research and a law-firm blog summarising it; the findings have not been independently verified.*
