---
title: "AWS sets out pattern to score SageMaker catalogue assets against governance rules using metadata export"
date: 2026-11-11
dek: "A sample pipeline joins the SageMaker asset metadata export with form, glossary, data quality and subscription data to give each asset a weighted daily compliance score, and flags heavily used, poorly governed data."
whyItMatters: "The pattern makes metadata completeness measurable: owners can list assets missing required forms, stewards can find assets with no glossary terms, and CDOs can track whether compliance improves after new rules are published. Weighting findings by the number of consuming projects is a practical way to prioritise remediation backlogs. Teams on other catalogues can borrow the idea of combining platform-enforced and organisation-defined metadata requirements into one policy, but should set their own weights and thresholds rather than adopting the example scoring."
categories: [metadata, data-quality, platforms]
institutions: []
whoShouldCare: ["Data stewards", "Data owners", "CDO", "Data platform teams"]
importance: 2
format: "How-to"
byline:
  name: "AWS"
  role: "the vendor of the product described"
type: "Case study"
region: "Global"
status:
  stage: "Published"
  detail: "Sample code and walkthrough; scoring model described as a starting point"
sources:
  - name: "AWS Big Data Blog"
    title: "Governance compliance beyond the catalog in Amazon SageMaker Unified Studio"
    url: "https://aws.amazon.com/blogs/big-data/governance-compliance-beyond-the-catalog-in-amazon-sagemaker-unified-studio/"
    primary: true
  - name: "AWS Documentation"
    title: "Exporting asset metadata"
    url: "https://docs.aws.amazon.com/sagemaker-unified-studio/latest/userguide/export-asset-metadata.html"
    primary: true
related: [google-makes-lookml-metric-definitions-and-lineage-generally-available]
card:
  figure: "50%"
  caption: "Example weight given to required metadata form coverage in the compliance score"
---

AWS has published a reference pattern for Amazon SageMaker Unified Studio that turns catalogue metadata into a **daily, per-asset compliance score**. It builds on the asset metadata export, which writes catalogue inventory to an Apache Iceberg table in S3 Tables once a day.

A Lambda function joins the export with API data on attached metadata forms, glossary terms, data quality results and active subscriptions. Required forms combine SageMaker's own enforcement rules with organisation-defined rules held in an S3 policy file. The example weights are **form coverage 50%**, data quality score 20%, and 10% each for data quality rule coverage, glossary presence and a description; AWS stresses these are configurable.

Scores feed Athena queries, EventBridge alerts and a Quick Sight dashboard. A risk matrix marks assets scoring below 50 with two or more subscribing projects as needing action now. Code is in an aws-samples repository.

*Editor's note: This article relies solely on AWS's own blog post and product documentation.*
