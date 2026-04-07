---
name: auditproject
description: Audits CLAUDE.md and AGENTS.md against the original MVJ baseline to detect drift, scope creep, and evolution patterns. Use when the owner wants to review how the agentic OS has changed from its original intent, or to surface proposed improvements to the routing rules and operating principles.
---

# Audit Project

Compares the current `CLAUDE.md` and `AGENTS.md` against the original baseline stored in artifacts, using git history as a secondary source, to detect drift and surface proposed improvements.

## When to Use

- Owner invokes `/auditproject`
- Owner asks "how has CLAUDE.md changed?", "has the system drifted?", or "let's review the project config"

## Context to Load

Before starting, load all of the following:

1. `artifacts/Original README and CLAUDE.md for MVJ.md` — the baseline (original intent)
2. `CLAUDE.md` (root) — current state
3. `AGENTS.md` (root) — current state
4. `artifacts/Logs/project-audit.md` — prior audit entries (may be empty on first run)

## Steps

### Step 1: Pull Git History for CLAUDE.md

Run the following shell commands to reconstruct version history:

```bash
git log --oneline -- CLAUDE.md
```

For each commit returned, use the hash to inspect that version:

```bash
git show <hash>:CLAUDE.md
```

Or to see the full diff from the earliest tracked commit to HEAD:

```bash
git log --all --oneline -- CLAUDE.md | tail -1  # get earliest commit hash
git diff <earliest_hash> HEAD -- CLAUDE.md
```

Note: Git history is only traced for `CLAUDE.md`. `AGENTS.md` is treated as a near-duplicate; compare its current state against `CLAUDE.md` directly to catch any divergence, but do not pull separate git history for it.

### Step 2: Identify the Reference Point

Check `artifacts/Logs/project-audit.md`:
- If **no prior audit entries exist**: the baseline document (`artifacts/Original README and CLAUDE.md for MVJ.md`) is the full reference. This is a first-run audit.
- If **prior audit entries exist**: note what commit range or date the last audit covered. Focus the new analysis on changes *since* that audit, but still compare against the original baseline for cumulative drift.

### Step 3: Analyze Drift Across Three Dimensions

For each dimension, cite specific examples with before/after comparisons where possible.

**a. Intent Drift**
What from the original vision or principles has been lost, weakened, or quietly contradicted?
- Look for original principles that no longer appear in the current documents
- Look for original behaviors that have been replaced by more complex alternatives
- Flag if the core "manage their truth" mission has been diluted by operational complexity

**b. Scope Additions**
What rules, structures, or behaviors have been added that weren't in the original?
- New routing rules, constraints, or folder policies
- New skills registered
- New sections or subsections that expand the operating surface
- Use your judgment to distinguish *healthy evolution* (the system growing as designed) from *creeping complexity* (rules added reactively without pruning old ones)

**c. Evolution Patterns**
What trends are visible across the version history?
- Are routing rules getting more specific or more general over time?
- Are principles being added faster than they're being retired?
- Is the document growing in length? Is that growth load-bearing?
- Note any patterns worth calling out to the owner as signals about how the system is evolving

### Step 4: Present Findings in Chat

Deliver a structured summary to the owner:

```
## Audit — [YYYY-MM-DD]

### Intent Drift
[Findings]

### Scope Additions
[Findings]

### Evolution Patterns
[Findings]

### Proposed Changes
1. [Specific proposed edit — what, where, why]
2. [...]
```

Ask the owner which proposed changes, if any, they want to apply.

### Step 5: Apply Approved Changes

If the owner approves any proposed changes:
- Apply them to `CLAUDE.md` and `AGENTS.md` together (per the sync rule: if one is updated, both must be updated in the same change)
- Keep proposed changes minimal and surgical — do not refactor surrounding text unless the owner asks

### Step 6: Append Entry to Drift Log

Append a dated entry to `artifacts/Logs/project-audit.md` using this format:

```markdown
---

## Audit — YYYY-MM-DD

**Git commits covered:** [list commit hashes and messages from CLAUDE.md history since last audit, or "Initial audit — full history reviewed" on first run]

**Intent Drift**
[Summary of findings]

**Scope Additions**
[Summary of findings]

**Evolution Patterns**
[Summary of findings]

**Proposed Changes**
- [ ] [Proposed change 1]
- [ ] [Proposed change 2]

**Accepted Changes**
- [Change applied, or "None accepted this run"]
```

Use `- [x]` for accepted changes and `- [ ]` for declined ones.

## Output

- Chat presentation of drift analysis with proposed changes (Step 4)
- Appended entry in `artifacts/Logs/project-audit.md` (Step 6)
- Updated `CLAUDE.md` and `AGENTS.md` if owner approves changes (Step 5)

## Edge Cases

- **No git history for a file**: Note the absence in the report and rely on current state vs. baseline only.
- **First run / empty log**: Treat the baseline document as the full reference. Label the log entry "Initial audit."
- **Git commands unavailable**: If shell access fails, skip Step 1 and perform static comparison only (baseline vs. current). Note the limitation in the report.
- **CLAUDE.md and AGENTS.md are out of sync**: If they contradict each other, flag this as a priority finding before anything else.

## Meta

**Version:** 1.0
**Last improved:** 2026-04-06
**Pending suggestions:**
- (none yet — awaiting first run)

**Stable runs:** 0
(Suggestions are frozen after 3 consecutive runs with no accepted changes.)
