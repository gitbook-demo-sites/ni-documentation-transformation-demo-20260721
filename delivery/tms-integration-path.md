---
description: "How GitBook can coexist with NI's existing translation management system."
icon: language
---

# TMS integration path

Translation is non-negotiable for NI, and the current TMS already has rich APIs. The right demo should not suggest replacing it. It should show GitBook as the authoring and delivery layer around it.

{% stepper %}
{% step %}
### Detect changed source

A merge to the main branch identifies changed pages, metadata, and assets since the last translation batch.
{% endstep %}

{% step %}
### Generate a translation manifest

Automation creates a manifest with source file, product, locale targets, content type, owner, and priority.
{% endstep %}

{% step %}
### Send to the TMS API

The manifest and source files are submitted to NI's translation system. The TMS remains the system of record for translation memory and vendor workflow.
{% endstep %}

{% step %}
### Import localized output

Returned translations are committed back into Git, reviewed when needed, and published through GitBook.
{% endstep %}
{% endstepper %}

{% hint style="success" icon="plug" %}
The demo angle: GitBook does not need to own translation memory. It needs to make source changes, metadata, review, and publishing easy to integrate with the TMS NI already trusts.
{% endhint %}
