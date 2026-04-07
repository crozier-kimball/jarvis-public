---
name: wrap
category: workflow
description: "End-of-session wrap. Summarizes the session, stages and commits all changes to git. Run at the end of any working session to prevent data loss and maintain git history."
---

# /wrap — End of Session Wrap

Run this at the end of each working session to capture work and create a git checkpoint.

## When to Use

- Owner says "/wrap", "wrap up", "commit", or "end session"
- Always at the end of a session — even short ones if files were changed

## Context to Load

None required beyond the current conversation context.

## Steps

### Step 1 — Review session changes

- Run `git status --short` to see all changed, new, and deleted files
- Run `git diff --stat` to see a summary of changes
- If no changes exist, report "Nothing to commit — working tree clean" and stop

### Step 2 — Stage all changes

- Run `git add -A` to stage all modified, deleted, and new files
- Before staging, verify nothing sensitive is included: check for `.env`, credentials, large binaries. If found, flag and ask the owner to exclude before continuing.

### Step 3 — Create a commit message

- Summarize what happened in this session from conversation context
- Use present tense, keep it concise
- Format: `wrap: [brief description of session work]`
- Run `git commit -m "wrap: [message]"`

### Step 4 — Report

Show commit hash and files changed. Remind the owner: "Sync in VS Code when ready."

## Output

- Git commit containing all session changes
- No file written to disk (session context lives in git history)

## Edge Cases

- **Working tree already clean:** skip steps 2–3 and report cleanly
- **Sensitive files staged:** flag immediately, do not commit until resolved

## Git Hygiene Rules

- Never force push or rewrite history on this repo
- Commit every session — no exceptions

## Meta

**Version:** 2.1
**Last improved:** 2026-04-07
**Pending suggestions:** none
**Stable runs:** 0
