---
description: "Automated quality gates for Git-backed NI documentation."
icon: list-check
---

# Automation checks

Automation should make review safer and faster.

| Check | Purpose |
| --- | --- |
| Required metadata | Ensures product, audience, locale, source format, and owner are present |
| Broken links | Catches moved pages and stale external references |
| Terminology | Flags off-brand terms and inconsistent product naming |
| Translation readiness | Finds non-translatable fragments, missing alt text, and unapproved variables |
| AI summary | Adds a PR summary for reviewers and localization teams |

{% hint style="info" icon="robot" %}
The strongest automation story for NI is practical: reduce manual coordination across 24 writers and many SMEs, without asking writers to become platform engineers.
{% endhint %}
