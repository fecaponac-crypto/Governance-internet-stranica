---
title: "IBM launches Agent Identity and Vault controls to give AI agents owners, scoped credentials and audit trails"
date: 2026-10-29
dek: "Agent Identity, Vault 2.2 and agent evaluation in watsonx Orchestrate are generally available. Cross-platform agent discovery and a sandbox-plus-kill-switch feature remain in tech preview."
whyItMatters: "The launch treats AI agents as non-human identities that need a named owner, a lifecycle status and least-privilege, expiring credentials. That is the same discipline governance teams apply to data ownership and access reviews. Teams should check whether their agent inventory records an accountable owner and the data each agent can reach. They should also confirm that agents built on third-party platforms are not running on persistent, over-broad service credentials. For audit and incident investigation, the key question is whether agent actions can be traced back to an authorised scope."
categories: [ai-governance, security, market]
institutions: []
whoShouldCare: ["CDO", "CISO", "AI governance lead", "Data stewards"]
importance: 3
type: "Product launch"
region: "Global"
status:
  stage: "Available"
  detail: "Agent Identity, Vault 2.2 and evaluation GA; discovery and containment in tech preview"
sources:
  - name: "IBM (PR Newswire)"
    title: "IBM Introduces Identity and Control for AI Agents, Securing Frontier Intelligence for the Enterprise"
    url: "https://www.prnewswire.com/news-releases/ibm-introduces-identity-and-control-for-ai-agents-securing-frontier-intelligence-for-the-enterprise-302920156.html"
    primary: true
  - name: "CDO Magazine"
    title: "IBM adds identity and access controls to govern enterprise AI agents"
    url: "https://www.cdomagazine.tech/aiml/ibm-adds-identity-and-access-controls-to-govern-enterprise-ai-agents"
related: [norway-s-datatilsynet-warns-ai-agents-left-running-after-staff-move-on, supervisors-press-banks-on-ai-agent-controls]
card:
  figure: "Agent Identity"
  caption: "IBM's new record of each AI agent's owner, lifecycle status and granted authority"
---

IBM announced new identity, access and monitoring tools for enterprise AI agents at its TechXchange 2026 conference on 27 October. **Agent Identity**, used with HashiCorp Vault, is meant to keep an authoritative record of each agent, including its owner, lifecycle status and granted authority. Vault then issues short-lived credentials limited to the agent's task. IBM says access can be denied and the session revoked in real time if an agent attempts an unauthorised action.

watsonx Orchestrate adds three capabilities. Discover finds agents, models and MCP servers built on Amazon Bedrock, Microsoft Foundry and Google Gemini. Contain runs agents in isolated sandboxes and adds a kill switch. Evaluate tests agents for quality, accuracy and compliance before deployment and monitors them in production.

**Discover and Contain are in tech preview**. Agent Identity, Vault 2.2 and the evaluation capabilities are generally available. IBM cites Gartner as saying only 13% of organisations believe they have the right AI agent governance in place.

*Editor's note: This article relies on IBM's own press release and trade-press coverage of it; capability claims have not been independently verified.*
