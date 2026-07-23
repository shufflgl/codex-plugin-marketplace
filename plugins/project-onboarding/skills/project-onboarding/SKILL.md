---
name: project-onboarding
description: Inspect an unfamiliar repository and produce an evidence-based implementation plan before changing code.
---

Use this workflow when the user asks how a repository works, requests a change in an unfamiliar codebase, or needs an implementation plan.

1. Read the applicable repository instructions first (`AGENTS.md`, local instructions, and contributor documentation).
2. Inspect only the files required to identify the relevant entry points, data flow, tests, and validation commands.
3. State the current behavior with file references, distinguishing verified facts from assumptions.
4. Propose the smallest safe implementation plan, including affected files and validation.
5. Do not edit files, install dependencies, change configuration, or run destructive commands unless the user requests it.
