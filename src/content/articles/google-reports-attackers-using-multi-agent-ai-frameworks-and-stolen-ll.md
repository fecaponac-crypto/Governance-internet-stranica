---
title: "Google reports attackers using multi-agent AI frameworks and stolen LLM credentials at 'machine speed'"
date: 2026-11-17
dek: "Google's latest AI Threat Tracker describes fully automated exploitation pipelines, 'LLMJacking' bills of up to $1 million and backdoors planted through AI coding assistant settings."
whyItMatters: "LLM API keys, session tokens and AI quotas are now assets that attackers steal and resell, so they need named owners, an inventory and the same revocation discipline as other privileged credentials. Usage and billing alerts on AI services are a practical early-warning control, since Google reports abuse generating six-figure charges within a day. AI coding assistant configuration files stored in repositories are an execution path and should fall under change control and code review. Faster weaponisation of disclosed flaws also shortens the time available to patch systems that hold personal or sensitive data."
categories: [security, ai-industry, ai-governance]
institutions: []
whoShouldCare: ["CISO", "AI governance lead", "Data platform owners", "DPO"]
importance: 3
type: "Research"
region: "Global"
status:
  stage: "Published"
  detail: "Quarterly threat report from Google Threat Intelligence Group and Mandiant"
sources:
  - name: "Google Threat Intelligence Group"
    title: "GTIG AI Threat Tracker: Agentic Threat Activity Crosses a Significant Threshold"
    url: "https://cloud.google.com/blog/topics/threat-intelligence/agentic-threat-activity-crosses-a-significant-threshold"
    primary: true
  - name: "The Record (Recorded Future News)"
    title: "Chinese state group developing automated attack tool for cyber espionage, Google says"
    url: "https://therecord.media/chinese-state-group-developing-automated-attack-tool-espionage"
related: [litellm-traces-poisoned-release-to-a-leaked-master-key-that-was-never]
card:
  figure: "$1 million"
  caption: "Worst cumulative LLMJacking resource abuse seen by Mandiant before remediation"
---

Google Threat Intelligence Group (GTIG) and Mandiant have published their latest AI Threat Tracker. According to the report, attackers are moving beyond basic prompting to open source multi-agent frameworks such as ARTEX, CAIRN, CyberStrikeAI and PentAGI to run multi-stage intrusions. GTIG says it saw CAIRN used against targets including the US aerospace sector, and found evidence that a PRC-nexus group was building its own framework for likely espionage use.

The report says attackers fully automated vulnerability discovery and exploitation without human involvement for the first time last quarter. It also describes 'LLMJacking', in which LLM credentials and cloud resources are stolen and access is resold. In some Mandiant cases, **single-day fraudulent charges exceeded $100,000**, and **cumulative abuse reached $1 million** in the worst.

A suspected North Korean cluster altered Claude Code configuration files in victims' repositories so that the tool downloaded a backdoor when it started.

*Editor's note: The findings come from Google's own threat intelligence report, which also promotes Google security products, and have not been independently verified.*
