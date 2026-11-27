---
title: "Google requires AI agents to reach Workspace data through governed MCP servers and CLI from February 2027"
date: 2026-11-27
dek: "A new Workspace AI Tools Addendum steers external agents away from REST APIs, requires dedicated OAuth client IDs and bars model training on customer data, according to Google."
whyItMatters: "Organisations whose staff or vendors connect AI agents to Workspace through REST APIs should plan to move those integrations to the MCP servers or CLI, since Google says technical enforcement of the requirement begins on 1 February 2027. Because Google says MCP calls are checked against classification labels and DLP rules, the effectiveness of these controls depends on how consistently sensitive content is labelled. Governance teams should also register each agent as a distinct identity with an owner, scoped access and audit logging, and check that third-party agent providers can meet the addendum's storage, training and deletion terms."
categories: [ai-governance, security, platforms]
institutions: []
whoShouldCare: ["CISO", "AI governance lead", "CDO", "Data stewards"]
importance: 4
type: "Product launch"
region: "Global"
status:
  stage: "Available"
  detail: "REST API restriction enforced from 1 February 2027; some controls still coming soon"
whatToCheck:
  - "Inventory AI agents and integrations that access Workspace data via REST APIs and plan their move to the MCP servers or CLI before 1 February 2027."
  - "Verify that Drive and Gmail classification labels and DLP rules cover sensitive content, since Google says agent calls are checked against them."
  - "Review contracts with external AI agent providers against the addendum's bans on raw storage and model training and its deletion requirements."
deadlines:
  - date: 2027-02-01
    what: "Technical enforcement begins: AI agents must use Workspace MCP servers or CLI instead of REST APIs"
  - date: 2027-04-01
    what: "Billing begins for usage quotas on external AI agents accessing Workspace"
sources:
  - name: "Google Workspace Blog"
    title: "Built for trust and control: New AI agent protections and developer tools in Google Workspace"
    url: "https://workspace.google.com/blog/product-announcements/built-for-trust-and-control-new-ai-agent-protections-and-developer-tools-in-google-workspace"
    primary: true
  - name: "CDO Magazine"
    title: "Google requires AI agents to use governed access to Workspace data"
    url: "https://www.cdomagazine.tech/aiml/google-requires-ai-agents-to-use-governed-access-to-workspace-data"
related: [oracle-announces-ai-registry-and-ai-generated-business-ontologies-to-g, spain-s-aepd-publishes-ten-point-guide-on-delegating-tasks-to-ai-assis]
card:
  figure: "1 Feb 2027"
  caption: "AI agents must use Workspace MCP servers or CLI instead of REST APIs"
---

Google has made its Workspace **Model Context Protocol (MCP) servers and command-line interface (CLI)** generally available, describing them as Google-managed entry points for AI agents. The MCP servers work across Gmail, Drive, Docs, Sheets, Slides, Calendar, Chat and Tasks; the CLI is aimed at local and desktop agents and workflow automation.

Under a new Workspace AI Tools Addendum, AI agents must connect through these interfaces rather than traditional REST APIs, with **technical enforcement beginning on 1 February 2027**. Google says every call will be checked against an organisation's Workspace permissions, data loss prevention rules and classification labels. External agents must use dedicated OAuth client IDs with least-privilege scopes, and usage quotas will be billed from 1 April 2027.

The addendum also prohibits permanent raw storage of data and model training, and requires derived data to be removed within a defined window and data to be deleted on disconnection. Admins can view, audit and revoke agents in the admin console; user-level revocation and blocking of specific files are listed as coming soon.

*Editor's note: This article relies on Google's own announcement and trade press coverage of it.*
