---
name: consensus
description: "Read-only second opinions from external models. Tries CLIs first, falls back to direct API. Usage: /consensus [topic or question]"
arguments:
  - name: topic
    description: "What you want second opinions on (optional: if omitted, uses the most recent decision/question in the conversation)"
    required: false
---

Invoke the `consensus` skill: $ARGUMENTS
