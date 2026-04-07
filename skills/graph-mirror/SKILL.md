---
name: graph-mirror
description: Mirror Obsidian vault link graph from private to public vault. Exports a single structured JSON artifact that preserves the wiki-link topology without exposing any file content. Run as part of daily startup or on-demand.
---

# Graph Mirror Skill

Mirrors the link graph from a private vault to a public vault as a structured JSON artifact. Preserves topology (which files link to which) while stripping all content.

## Usage

**As a skill:** Run `/graph-mirror` and the agent will execute the script with the correct paths.

**Directly:** From any tool (Hermes, Claude Code, Codex):

```bash
python3 scripts/graph_mirror.py --source /path/to/private-vault --output /path/to/public-vault/obsidian-graph-mirror.json
```

The script lives at `scripts/graph_mirror.py` in this skill's directory so it's portable.

## What it does

- Reads every `.md` file in the source vault
- Extracts all `[[wikilinks]]` patterns
- Produces one JSON artifact with:
  - File paths and folder locations
  - Outgoing link targets for each file
  - Stats (total files, total links, unique targets)

**The orchestrator agent reads this JSON to understand the full graph topology without ever touching sensitive content.**

## Guardrails

- NEVER modify `scripts/graph_mirror.py`
- ONLY this skill writes the output artifact — never let the agent write the mirror manually
- Always verify the output artifact after running
- The public vault must remain clean — no content should ever leak
- Run only in the user's local environment, never on remote or shared systems

## Configuration

The skill expects two paths:
1. `--source` — path to the private Obsidian vault
2. `--output` — path where the JSON artifact should be written (in the public vault)

These should be configured based on the user's setup. On first run, ask the user for both paths and record them.
