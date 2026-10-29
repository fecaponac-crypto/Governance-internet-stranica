---
title: "Cisco open-sources Project Quarry to flag risky sequences of AI agent actions"
date: 2026-10-29
dek: "The detection language and engine examines whole agent sessions, including tool calls and MCP interactions, rather than single commands, and records the evidence behind each match."
whyItMatters: "Access reviews that approve each agent permission in isolation can miss harmful combinations, such as reading a credentials file and then calling an external endpoint. Governance and security teams deploying agents should check whether their logging captures full session sequences — tool calls and MCP traffic included — so that sequence-based rules can be written at all. The evidence records Quarry produces could also support audit trails for agent data access, but rules still need owners who understand which data flows are legitimate."
categories: [security, ai-governance]
institutions: []
whoShouldCare: ["CISO", "AI governance lead", "CDO", "Data stewards"]
importance: 3
type: "Product launch"
region: "Global"
status:
  stage: "Available"
  detail: "Released as open source on 28 October 2026"
sources:
  - name: "CDO Magazine"
    title: "Cisco open-sources Project Quarry to detect risky AI agent behavior"
    url: "https://www.cdomagazine.tech/aiml/cisco-open-sources-project-quarry-to-detect-risky-ai-agent-behavior"
related: [monte-carlo-launches-bayes-an-ai-agent-that-monitors-and-fixes-other-a, supervisors-press-banks-on-ai-agent-controls]
card:
  figure: "Open source"
  caption: "Cisco's Project Quarry detects risky multi-step AI agent behaviour"
---

Cisco has open-sourced **Project Quarry**, a detection language and engine for spotting potentially harmful AI agent behaviour, according to CDO Magazine, citing The Register. Rather than checking individual commands, Quarry analyses **sequences of actions across an agent's session**, a gap Cisco says conventional security monitoring leaves open.

Security teams can write rules covering large language model conversations, tool calls, Model Context Protocol (MCP) interactions and multimodal inputs. One example rule would flag an agent that reads a credentials file and then sends data to an external server. When a rule fires, Quarry logs the actions and fields that caused the match.

The release includes installation and rule-writing guidance, configuration examples, a starter rule pack and plugins for Claude Code, Codex and other MCP-compatible agents. Cisco said it had not tested Quarry against a July incident involving OpenAI agents and exposed Hugging Face tokens, but believed it could have caught warning signs.

*Editor's note: This article relies on secondary news coverage that in turn cites The Register and Cisco's own statements.*
