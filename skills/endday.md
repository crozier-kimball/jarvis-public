---
name: endday
category: workflow
description: "End-of-day review. Collects the day's notes and brain dumps, reviews workstream and tasklist progress, repairs missing wikilinks, and writes a daily summary to artifacts/daily/. Run once at the end of each working day. /today reads this output the following morning."
---

# /endday — End of Day Review

Run this once at the end of each working day to consolidate notes, check progress, and write a summary that /today will read tomorrow morning.

## When to Use

- Owner says "/endday", "end of day", "day review", "close out today", or "wrap the day"
- Once per day — not per session (use /wrap for per-session git commits)

## Day Boundary Rule

The owner works past midnight. Before reading or writing any dated file, determine the correct working date:

```bash
hour=$(date '+%H')
if [ "$hour" -lt 4 ]; then
  working_date=$(date -d 'yesterday' '+%Y-%m-%d')
else
  working_date=$(date '+%Y-%m-%d')
fi
```

If the current time is before 4:00 AM, treat "today" as yesterday's calendar date. Use `$working_date` everywhere `YYYY-MM-DD` appears in this skill.

## Context to Load

Load silently before starting:

1. Today's daily brief, if it exists: `artifacts/daily/YYYY-MM-DD-brief.md`
2. Any meeting notes ingested today: run `git log --since="4am" --name-only --diff-filter=A` and filter results for `meeting-transcripts/meetings/` — this captures meetings regardless of their meeting date header
3. Task list: `artifacts/Tasklist.md`
4. Any brain dumps or daily notes in `artifacts/daily/` dated today
5. List of all files changed today: `git status --short` and `git log --since="4am" --oneline`

## Steps

### Step 1 — Inventory the day

- Run `git status --short` to see what's changed since last commit
- Run `git log --since="4am" --name-only --diff-filter=A` and filter for `meeting-transcripts/meetings/` to find meetings ingested today (by ingestion date, not meeting date)
- Read today's brief and any meeting notes found above
- Read `artifacts/Tasklist.md`
- Note: if there's nothing at all (no brief, no meetings, no changes), ask the owner: "Quiet day or did things happen outside the workspace? Anything to capture before I write the summary?"

### Step 2 — Review and repair notes

For each file modified or created today:

- Scan for plain-text mentions of people who have files in `people/` — convert bare name mentions to `[[First Last]]` wikilinks where missing
- Scan for plain-text mentions of projects or artifacts with files in `artifacts/` — add `[[filename]]` wikilinks where missing
- Use judgment: link substantive references, not passing mentions. "I met with Sarah Chen" → `[[Sarah Chen]]`. A name in a list header or incidental context is not worth linking.
- Flag people or projects mentioned without any file — list them under "Open flags" in the summary. Do not create stub files automatically.
- Fix formatting issues only if they break readability (broken headers, malformed frontmatter). Don't refactor style.

### Step 3 — Review workstream and task progress

- Read `artifacts/Tasklist.md` and compare against what actually happened today (from brief and meeting notes)
- Identify: what was completed, what's in progress, what got blocked or deferred
- If a workstream file is linked from the tasklist, scan it for open items relevant to today
- Ask the owner one question if progress is ambiguous: "Looks like [X task] was on today's plan — did that move forward?" One question max.

### Step 4 — Update task list

Based on today's work:
- Mark completed tasks as done
- Mark started-but-unfinished tasks as in-progress
- Add any new tasks surfaced in meetings or conversation
- Defer items that clearly didn't happen and weren't mentioned as blocked

### Step 5 — Compose the day summary

Write a summary covering:
- Accomplishments (specific, not vague — "finished visa doc outline" not "worked on visa")
- What's in progress or deferred and why
- Decisions made today
- New people or commitments that surfaced
- Any flags for tomorrow

Keep it under 10 bullets. Lead with completions.

### Step 6 — Write the end-of-day summary into today's daily note

Open `artifacts/daily/YYYY-MM-DD.md` (create from template if it does not exist).

Replace the `## End of Day` section with:

```
## End of Day

### Summary
- [accomplishment]
- [accomplishment]
- [in progress / deferred item + reason if known]
- [decision made]

### Task updates
[What changed in Tasklist.md — completions, new tasks, deferrals]

### Link repairs
[Wikilinks added — or "None needed"]

### Open flags
[People or projects mentioned without files — "Create one?" — or "None"]

### Tomorrow
[Any specific carry-forwards or context /today should know]
```

Do not create a separate endday file. The daily note at `artifacts/daily/YYYY-MM-DD.md` is the single record for the day.

### Step 7 — Commit

Run `/wrap` to stage and commit all changes. Use `endday: [brief description of day]` as the commit message instead of the default `wrap:` prefix.

### Step 8 — Report

Show commit hash and files changed. Close with: "Run /today tomorrow morning to continue."

## Output

- `artifacts/daily/YYYY-MM-DD.md` — single daily note with End of Day section populated
- Updated `artifacts/Tasklist.md`
- Git commit via `/wrap` (message prefix: `endday:`)

## Edge Cases

- **No brief found:** proceed; note in summary that /today was not run today
- **No changes to commit:** still write the endday summary if the owner wants a record; skip git commit if tree is clean
- **Many unlinked mentions:** surface only the top 5 most meaningful; don't flood the output
- **Sensitive files staged:** flag immediately, never commit secrets

## Meta

**Version:** 1.1
**Last improved:** 2026-04-07
**Pending suggestions:** none
**Stable runs:** 0
