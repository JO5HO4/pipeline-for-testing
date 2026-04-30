---
name: hep-meta-first
description: "Single-entry HEP meta skill for long-horizon analysis work. Use when you want one triggerable skill that routes dynamically to the right structured contract by stage, dependency, required artifact, or next handoff."
---

# HEP Meta-First

Use this as the only installed HEP skill in the meta-first experiment.

1. Read `references/00_INDEX.md` for the default execution spine and stage groups.
2. If starting cold or before the first repo command, read `references/SKILL_HEP_ANALYSIS_ENV_SETUP.md` and normalize the runtime before bootstrap, tests, smoke runs, or fit execution.
3. Read `references/manifest.yaml` to resolve which contract produces the needed output, what can run now, or what should follow next.
4. Read `references/ROUTING_GUIDE.md` before loading any contract files.
5. Load only the specific `references/SKILL_*.md` files needed for the current blocking step.
6. Keep the active contract set small. Prefer one current contract plus the next likely handoff, not a whole stage worth of files.
7. Use `references/skills_refactor_audit.md` when dependency inference feels weak or multiple contracts look plausible.
