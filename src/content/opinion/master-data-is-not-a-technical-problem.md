---
title: "Master data is not a technical problem. It is an organisational decision we keep avoiding."
date: 2026-11-10
dek: "Platforms can match, merge and validate records, but they cannot decide what a customer is, which record is authoritative or who answers for it when it is wrong."
---

Every organisation claims that data is important. Many now claim that data is one of their most valuable assets.

Yet ask a few simple questions about a customer, supplier, product or employee, and the confidence quickly disappears.

- Who is the customer?
- Which system contains the authoritative customer record?
- What makes two records duplicates?
- When is a customer considered active?
- Who is allowed to change the legal name, address, tax identifier or contact information?
- Who accepts the operational consequences when that information is wrong?

These questions rarely fail because databases cannot store the answers. They fail because the organisation has never fully agreed on them.

**That is why master data is not primarily a technical problem.** It is an organisational decision that has often been postponed, distributed across departments or hidden inside systems.

## The illusion of a single source of truth

“Single source of truth” is one of the most frequently repeated expressions in data management.

It is also one of the most misleading.

A company may have several systems containing customer information: a customer relationship management platform, billing, enterprise resource planning, customer service, marketing automation, identity management, data warehouses and numerous local applications.

Installing a master data management platform does not automatically make one of those systems the truth.

Technology can consolidate records. It can match and merge them. It can apply survivorship rules, validate attributes and distribute a golden record. But technology cannot independently decide what the organisation means by “customer”, which attributes are authoritative or which business event makes a record valid.

Those are governance decisions.

Before an organisation can create a single source of truth, it must create a shared understanding of truth. That requires decisions about definitions, ownership, authority and accountability.

**Without those decisions, a golden record is simply another record produced by another system.**

## Duplicate records are usually a symptom

When users complain about master data, they often point to visible defects:

- duplicate customers
- incomplete addresses
- invalid telephone numbers
- inconsistent legal names
- obsolete contacts
- missing identifiers
- products assigned to the wrong category
- suppliers created several times by different departments

These are real problems, but they are not necessarily the root problem.

A duplicate customer can be created because matching rules are weak. It can also be created because employees cannot find an existing record, because the search function is poor, because different channels collect different identifiers or because creating a new customer is easier than correcting an existing one.

An invalid telephone number may be a data-entry mistake. It may also indicate that the application accepts any sequence of characters, that international and national formats are mixed or that nobody has defined whether the number is intended for contact, authentication, notification or marketing consent.

A technical control can reject malformed data. It cannot repair an undefined business process.

Data quality defects often reveal where responsibilities, rules and incentives have not been aligned.

## Everyone uses master data, but nobody owns the whole outcome

Master data crosses organisational boundaries.

Sales creates a customer because it needs to complete a transaction. Finance needs the correct legal entity and billing information. Marketing needs valid contact data and appropriate permissions. Customer service needs a complete relationship history. Compliance needs traceability. Analytics needs consistent segmentation. Management expects reliable reporting.

Each function may perform its own task correctly and still contribute to an incorrect overall result.

This is where the traditional idea of data ownership becomes difficult.

Naming a data owner is useful, but putting a person’s name into a governance catalogue does not create ownership. Ownership becomes real only when that person has:

1. a clearly defined decision domain
2. authority to approve or reject rules
3. access to evidence about data quality and usage
4. a process for resolving conflicts
5. time and organisational support to perform the role
6. accountability for agreed outcomes

**Without these conditions, data ownership is ceremonial.**

The organisation may have a data owner on paper while operational decisions remain scattered across application teams, business departments, external vendors and project boards.

## The problem becomes more serious with artificial intelligence

Poor master data has always created operational costs. It produces returned invoices, failed deliveries, incorrect reports, duplicate communication and unnecessary manual work.

Artificial intelligence changes the scale of the problem.

AI systems can consume, combine and act on data much faster than traditional processes. If customer identities are fragmented, product classifications are inconsistent or supplier relationships are incorrectly represented, AI does not remove that ambiguity. It may reproduce it at greater speed and with greater confidence.

An AI assistant connected to customer service data may provide an answer based on the wrong customer record. A recommendation model may treat duplicate profiles as separate individuals. An automated agent may update a non-authoritative system. A risk model may interpret missing master data as an actual business signal.

The question is no longer only whether the model is accurate.

We must also ask:

- Was the entity correctly identified?
- Was the authoritative record used?
- Were the relevant attributes valid at the time of the decision?
- Can the organisation reconstruct which version of the data was used?
- Who approved the rules that determined the record?
- Can a human correct both the decision and the underlying master data?

**AI governance without master data governance is governance built on uncertain identities and unstable definitions.**

## More controls do not automatically create better governance

A common response to poor data quality is to add more controls.

Additional validation rules can be useful, but controls have costs. They create exceptions, maintenance requirements, false positives and manual review. If every discovered defect results in another control, the organisation may eventually build a large monitoring environment without improving the process that generates the data.

A useful control should have a clear purpose:

- Which business risk does it address?
- Which data attribute does it evaluate?
- What is the expected condition?
- Who investigates the exception?
- What is the resolution deadline?
- How is a false positive handled?
- Does the correction reach the source system?
- How will the organisation know that the control is no longer necessary?

**A control without an owner is only an observation.**

A report showing ten thousand data-quality exceptions may appear impressive, but it has little value if nobody can explain which exceptions matter, who should resolve them or whether the same defects will return next week.

The objective should not be to produce more exceptions. It should be to reduce the organisation’s ability to create the same defect repeatedly.

## Start with decisions, not with the platform

Organisations frequently begin master data initiatives by evaluating tools. They compare matching capabilities, workflow engines, integration patterns, data catalogues and cloud architectures.

Those choices matter, but they should not be the first step.

A more durable starting point is to define a limited set of business decisions.

For one master-data domain, the organisation should answer:

1. **What is the entity?** Define precisely what constitutes a customer, supplier, product, location or employee.
2. **Why does the entity matter?** Identify the business processes and risks that depend on it.
3. **Which attributes are critical?** Not every field deserves the same level of governance.
4. **Where is each attribute created?** Document the actual process, not only the intended architecture.
5. **Which system is authoritative for each critical attribute?** Authority may differ by attribute and lifecycle stage.
6. **Who can make and approve changes?** Separate operational entry from governance authority.
7. **Which quality rules are mandatory?** Define completeness, validity, uniqueness, consistency and timeliness in measurable terms.
8. **How are exceptions resolved?** Specify the workflow, owner, evidence and escalation path.
9. **How is the decision audited?** Preserve the record of what changed, when, why and by whom.
10. **How will success be measured?** Connect data quality with operational outcomes, not only percentages.

Only after these answers are sufficiently clear should the organisation decide which technology is needed.

**Otherwise, it risks automating unresolved disagreements.**

## Data quality needs an economic translation

Data-quality metrics often remain too abstract.

A dashboard may report that customer-address completeness is 94 percent or that supplier-tax identifiers are 98 percent valid. These numbers are useful for monitoring, but they do not automatically explain the business impact.

Six percent of incomplete addresses can represent very different levels of risk. The affected records may belong to inactive customers, or they may be associated with high-value contracts, regulatory notifications or critical service locations.

Data quality should therefore be connected to business consequences.

Instead of reporting only the percentage of invalid records, organisations should also measure outcomes such as:

- invoices that could not be delivered
- orders delayed because of incomplete data
- customer contacts sent to the wrong person
- manual work required to reconcile identities
- duplicated supplier payments
- regulatory reports requiring correction
- AI-generated actions based on disputed attributes
- time needed to resolve a master-data exception

This does not mean that every defect must be converted into an exact monetary amount. It means that quality should be prioritised according to the decisions and processes it affects.

A technically imperfect dataset may be acceptable for one purpose and unacceptable for another.

## Good master data is a continuing organisational capability

Master data is sometimes treated as a clean-up project.

A team analyses the records, removes duplicates, completes missing attributes and declares that data quality has improved. For a short period, the metrics may confirm that conclusion.

Then the same defects return.

They return because the organisation corrected the data but did not change the conditions under which the data was created.

Sustainable master data management requires an operating model, not a one-time cleansing exercise. That operating model connects:

- business ownership
- data stewardship
- application responsibilities
- process design
- quality controls
- issue management
- metadata
- change management
- security and access
- audit history
- measurement and reporting

Its purpose is not to make data perfect. Perfect data is neither realistic nor always economically justified.

Its purpose is to make data sufficiently reliable for an explicitly defined use, and to ensure that the organisation knows what to do when it is not.

## The decision we can no longer postpone

Organisations are entering a period in which more decisions will be made with data, through data and increasingly by automated systems.

In that environment, master data cannot remain an invisible responsibility delegated to individual applications or temporary projects.

The central question is not whether a company has an MDM platform, a data catalogue or a data-quality dashboard.

**The real question is whether the organisation has agreed on the identity, meaning, authority and accountability of the entities on which its operations depend.**

If it has not, then the master-data problem is not waiting to be solved by better technology.

It is waiting for the organisation to make decisions it has avoided.
