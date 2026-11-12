---
title: "Huntress links ScreenConnect attacks on 48 organisations to RMM+ extension that could accept a blank key"
date: 2026-11-12
dek: "Huntress says RMM+ bypasses ScreenConnect accounts, roles and MFA, and versions 1.0.31 and 1.0.32 accepted a blank key. ConnectWise disabled it in about 400 partner environments; on-premises users must do so themselves."
whyItMatters: "The incident shows how a forgotten add-on can sidestep MFA and role-based access on a privileged remote-management tool used by managed service providers. Security and third-party risk teams should ask their MSPs whether RMM+ or similar ScreenConnect extensions were installed, and whether access keys were ever set. Huntress advises reviewing Run Command and Toolbox history, revoking exposed sessions and not connecting to suspected hosts through ScreenConnect. Where personal data sat on affected endpoints, privacy teams should assess whether breach-notification duties apply."
categories: [security, platforms]
institutions: []
whoShouldCare: ["CISO", "Third-party risk managers", "IT operations leads", "DPO"]
importance: 3
type: "Research"
region: "Global"
status:
  stage: "Published"
  detail: "ConnectWise investigation ongoing; initial access route not fully confirmed"
sources:
  - name: "Huntress"
    title: "SCKit worm: rogue ScreenConnect clients (blog post with 11 November 2026 update)"
    url: "https://www.huntress.com/blog/sckit-worm-rogue-screenconnect"
    primary: true
  - name: "The Record (Recorded Future News)"
    title: "ConnectWise investigates ScreenConnect breaches after reports of incidents at nearly 50 organizations"
    url: "https://therecord.media/connectwise-screenconnect-breaches-third-party-tool"
related: [litellm-traces-poisoned-release-to-a-leaked-master-key-that-was-never]
card:
  figure: "288 hosts"
  caption: "Endpoints across 48 organisations affected within 90 minutes, according to Huntress"
---

Security firm Huntress said that on 11 November 2026 an operator used access to cloud-hosted ConnectWise ScreenConnect panels to push commands that installed rogue ScreenConnect clients and a toolkit called SCKit. It counted **288 hosts across 48 organisations** affected within 90 minutes.

In an update, Huntress linked the activity to RMM+, a third-party extension that authenticates with a shared access key rather than ScreenConnect's user accounts, roles and MFA. In **versions 1.0.31 and 1.0.32 the key defaulted to blank** and an empty value passed the check. According to The Record, ConnectWise said about 400 partner environments had the extension installed and that its presence alone did not establish compromise.

ConnectWise disabled RMM+ in hosted environments and urged on-premises customers to do the same. Blackpoint Cyber researchers told The Record the toolkit also exploits CVE-2026-84869, which the existing patch blocks. ConnectWise is still investigating.

*Editor's note: This article relies on a security vendor's own research publication and on news coverage of ConnectWise's statements.*
