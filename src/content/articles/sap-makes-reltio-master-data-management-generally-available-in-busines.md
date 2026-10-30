---
title: "SAP makes Reltio master data management generally available in Business Data Cloud for AI agents"
date: 2026-10-30
dek: "Announced at SAP TechEd Berlin alongside a completed Dremio deal, an Apache Polaris-based universal catalog and a new Ontology Manager for curated, agent-specific views of SAP Knowledge Graph."
whyItMatters: "SAP is positioning master data and shared business definitions as prerequisites for reliable AI agents. SAP customers should review whether matching rules, survivorship logic and data ownership are documented before reconciled profiles are fed to agents as governed data products. Agent-specific ontology views that inherit definitions from a central knowledge graph also need change control. Otherwise a single altered definition could silently affect every agent that uses it."
categories: [mdm, metadata, market]
institutions: []
whoShouldCare: ["CDO", "Data stewards", "AI governance lead", "Data architects"]
importance: 3
type: "Product launch"
region: "Global"
status:
  stage: "Available"
  detail: "SAP Reltio is generally available; Ontology Manager availability not stated"
sources:
  - name: "SAP News Center"
    title: "SAP lakehouse and new data fabric innovations in SAP Business Data Cloud for the autonomous enterprise"
    url: "https://news.sap.com/2026/10/sap-lakehouse-new-data-fabric-innovations-sap-bdc-autonomous-enterprise/"
    primary: true
  - name: "CDO Magazine"
    title: "SAP expands data fabric and master data tools for enterprise AI agents"
    url: "https://www.cdomagazine.tech/aiml/sap-expands-data-fabric-and-master-data-tools-for-enterprise-ai-agents"
related: [oracle-announces-ai-registry-and-ai-generated-business-ontologies-to-g, google-makes-lookml-metric-definitions-and-lineage-generally-available]
card:
  figure: "SAP Reltio"
  caption: "Multi-domain master data management now generally available in SAP Business Data Cloud"
---

SAP has announced at TechEd Berlin that, with its acquisition of Reltio now complete, **SAP Reltio is generally available in SAP Business Data Cloud (BDC)**. According to SAP, the tool uses AI-based entity resolution to match and reconcile customer, supplier and product records across SAP and third-party systems. The resulting profiles can be published as governed data products for its Joule agents.

SAP also said it has completed its acquisition of Dremio. BDC now supports native Apache Iceberg and a **universal catalog powered by Apache Polaris**, with zero-copy sharing to partners including Databricks, Snowflake, Google, AWS and Microsoft.

A new SAP Business Data Cloud Ontology Manager lets teams create domain-specific views of SAP Knowledge Graph, such as a collections view. SAP says these views inherit definitions and governance from the graph. SAP did not state when the Ontology Manager will be available.

*Editor's note: This article relies on SAP's own announcement and trade-press coverage of it; capability claims have not been independently verified.*
