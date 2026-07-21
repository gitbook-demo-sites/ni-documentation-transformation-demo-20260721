---
description: "Compare full Markdown authoring with a DITA-to-Markdown publishing pipeline."
icon: file-code
---

# DITA to Markdown strategy

NI has already tested DITA's XML-to-Markdown export, and some content already exists in GitHub-flavored Markdown. That creates two viable paths.

| Decision | Full Markdown authoring | DITA-to-Markdown publishing pipeline |
| --- | --- | --- |
| Best for | New software docs, fast iteration, AI drafting | Legacy content, hardware governance, phased migration |
| Writer experience | Simple editing in GitBook or GitHub | Writers continue in DITA until migration timing is clear |
| AI access | Direct access to clean Markdown | AI works on exported Markdown after transformation |
| Translation impact | TMS integrates with GitBook/GitHub source | TMS can continue receiving structured export outputs |
| Risk | Requires authoring change management | Adds pipeline complexity and possible transform drift |

{% hint style="success" icon="lightbulb" %}
A practical demo path is hybrid: start software docs in Markdown where the team wants velocity, keep DITA-to-Markdown for legacy and hardware content until governance requirements are settled.
{% endhint %}
