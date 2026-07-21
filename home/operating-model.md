---
description: "A practical operating model for a Git-backed documentation program at NI."
icon: diagram-project
---

# Future-state operating model

The operating model is designed around one principle: content should be easy for humans and agents to access, review, reuse, translate, and publish.

{% stepper %}
{% step %}
### Convert or export source content

Start with NI's existing DITA-to-Markdown export for software docs. Keep DITA as a source option while the team decides whether Markdown becomes the authoring format or the publish-time format.
{% endstep %}

{% step %}
### Review in GitHub

Writers, SMEs, external agencies, and approved customer contributors propose changes through branches and pull requests. CODEOWNERS can route reviews by product area.
{% endstep %}

{% step %}
### Publish through GitBook

GitBook turns the reviewed source into searchable HTML with metadata, page feedback, AI answers, and public or gated visibility.
{% endstep %}

{% step %}
### Localize through the TMS

Export changed content and metadata to the existing translation management system, then import localized content back into the Git/GitBook workflow.
{% endstep %}
{% endstepper %}
