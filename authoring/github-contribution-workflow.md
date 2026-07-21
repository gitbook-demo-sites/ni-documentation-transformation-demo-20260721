---
description: "How SMEs, agencies, and external contributors can propose documentation updates safely."
icon: code-branch
---

# GitHub contribution workflow

Open contribution was one of the clearest objectives from discovery. GitBook can keep the contribution interface approachable while GitHub provides the governance layer underneath.

{% stepper %}
{% step %}
### Contributor proposes a change

A writer, SME, agency partner, or approved external contributor edits a Markdown page and opens a pull request.
{% endstep %}

{% step %}
### Automation checks the change

Checks validate frontmatter, broken links, required metadata, terminology, and TMS readiness.
{% endstep %}

{% step %}
### Review routes to the right owner

CODEOWNERS requests product SMEs, localization, or documentation services depending on file path and metadata.
{% endstep %}

{% step %}
### Merge publishes the update

GitBook syncs the merged change and updates the HTML site, AI index, llms files, and page metadata.
{% endstep %}
{% endstepper %}
