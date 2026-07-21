---
description: "A repository structure that supports multiple product areas without forcing one giant docs tree."
icon: folder-tree
---

# Content repository model

A future repository can mirror NI's product taxonomy without forcing every manual into one navigation tree.

```
ni-docs/
  software/
    labview/
    teststand/
    flexlogger/
    instrumentstudio/
  shared/
    authoring-guides/
    style-guide/
    metadata/
  localization/
    handoff-manifests/
    returned-translations/
```

## Why this structure helps

* Product teams can own their folders.
* Shared guidance lives once and is referenced across products.
* GitHub CODEOWNERS can request the right SMEs automatically.
* Translation jobs can be generated from changed files instead of full manuals.
