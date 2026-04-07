---

name: readmeeting

description: Ingests a meeting transcript from meeting-transcripts/raw/, classifies
  the meeting type, extracts topics/decisions/action items, and produces a structured
  Obsidian note with backlinks to people, workstreams, artifacts, and the task list.
  Deletes the raw file after writing.

when_to_use: Called by the user after dropping a transcript file into
  meeting-transcripts/raw/. Produces an Obsidian meeting note and updates all
  downstream files. Also invokable from /today when unprocessed transcripts are
  detected.

---

# /readmeeting â€” Meeting Transcript Ingestion

## Purpose

Turn a raw transcript into a structured, backlinked Obsidian note. Update people
files, the task list, and relevant workstreams. Leave no orphan data. Delete the
raw file when done.

---

## Scope and Guardrails

- Do not manually process transcript content outside `/readmeeting`.
- Only ingest from `meeting-transcripts/raw/`.
- Always write processed meeting notes to `meeting-transcripts/meetings/`.
- Use graph-based context routing with wiki-link traversal and backlinks, limited to 1-hop from seed notes.

---

## Learned Patterns (Owner-Confirmed)

Apply these rules automatically during ingestion.

### Meeting Classifications

| Meeting Name | Type | Primary Presenter | Workstream |
|---|---|---|---|
| BIA Weekly Meeting | work | McKay Marshall | pcs |

### Format Preferences

- Prefer the Otter.ai summary format (has an Action Items section, no speaker timestamps) over raw verbatim transcript when both exist for the same meeting.

### Identity Mappings

- "Crozier" in PCS meeting transcripts = the owner.

### People -> Workstream Mappings

- Reference the .obsidian graph and existing notes to identify known people and their associated workstreams. For example, if "McKay Marshall" appears in a transcript and has a people file that links to the "pcs" workstream, infer that the meeting likely touches the "pcs" workstream.

## Step 1 â€” Scan for Transcripts (silent)

Look in `meeting-transcripts/raw/` for all files.

- If no files are present: tell the user "No transcripts found in
  meeting-transcripts/raw/. Drop a file there and run /readmeeting again."
  Stop.
- If one file: proceed with it.
- If multiple files: check whether any share the same meeting (similar name,
  same date). If so, prefer the structured summary format (no speaker
  timestamps, has an Action Items section) over the raw verbatim transcript.
  If they are different meetings, list them and ask the user which to process
  first, then process one at a time.

---

## Step 2 â€” Load Context (silent, no output yet)

Read the following. Do not summarize yet.

1. **Transcript file** â€” full content.
2. **Today's daily note** â€” find the file matching today's date in
   `artifacts/daily/`. Load it if it exists; skip if not.
3. **Learned patterns** â€” read the `## Learned Patterns (Owner-Confirmed)`
   section in this file and apply stored rules (e.g., recurring meeting names,
   known attendees, known workstream mappings).
4. **People files** â€” for each name appearing in the transcript, check
   `people/` for a matching file. Load name and most recent interaction only.
5. **Workstream files** â€” scan `artifacts/workstreams/` for any workstream
   whose name or key people appear in the transcript. Load frontmatter + first
   section only.
6. **Task list** â€” read `artifacts/Tasklist.md` to understand current format
   and existing tasks.
7. **Networking log** â€” read `artifacts/networking-log.md` (for networking
   meeting classification only).

---

## Step 3 â€” Parse the Transcript (silent)

Extract the following:

- **Meeting name** â€” from filename or first lines of the transcript.
- **Meeting date** â€” from filename or transcript header. If absent, use today's
  date and flag it.
- **Attendees** â€” full names where available. Note speaker labels if only
  first names or labels are present.
- **Meeting type** â€” classify as one of:
  - `work` â€” org meeting, business agenda, multiple colleagues from same
    company or project.
  - `networking` â€” 1:1 or small group, external contact, career or
    relationship focus.
  - `unclear` â€” flag for user to confirm in Step 4.
- **Topics discussed** â€” key subjects covered, with the primary speaker for
  each.
- **Decisions made** â€” any explicit conclusions or approvals reached.
- **Your action items** â€” tasks assigned to you or that you volunteered for.
- **Others' action items** â€” tasks assigned to attendees (record for
  context, not your task list).
- **Relevant workstreams** â€” which of your active workstreams does this
  meeting touch?

---

## Step 4 â€” Present Full Write Manifest (first output to user)

Present two things in one output: a summary of what was parsed, and a complete
manifest of every file that will be touched. This is the only approval gate â€”
make it complete.

Format:

```
ðŸ“‹ MEETING INGESTION PREVIEW

Meeting: [Name] â€” [Date]
Type: [work / networking / unclear]
Attendees: [Name 1] (people file: âœ“/âœ—), [Name 2] (âœ“/âœ—), ...
Workstreams touched: [workstream name(s) or "none detected"]

Topics:
- [Topic] (led by [Name])
- ...

Decisions:
- [Decision]
- ...

â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
ðŸ“‚ FILES TO BE WRITTEN
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

[AUTO] meeting-transcripts/meetings/YYYY-MM-DD-[name].md â€” new meeting note

[REVIEW] artifacts/Tasklist.md â€” add [N] task(s):
  - [ ] [Task description] | check-in: [proposed date â€” ask if not known]
  - ...

[AUTO] people/[name].md â€” add interaction entry: "[one-line summary]"
[AUTO] people/[name].md â€” create stub (role: [role if known])
  ... (one line per person)

[REVIEW] artifacts/workstreams/[name].md â€” add to ## Recent Meetings:
  "[meeting-note-link] - [one-line context]"
  Also propose any content updates if the meeting materially changes
  the workstream's status, trigger conditions, or active work section.
  Show the proposed addition(s) explicitly.

[AUTO] networking-log.md â€” add entry (networking meetings only)

[AUTO] meeting-transcripts/raw/[filename] â€” DELETE after writes complete

â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
Assumptions made:
- [Any inference the model is not sure about]
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
```

Then ask:
"Approve all, or call out anything to skip or change?"

**Labels explained:**
- `[AUTO]` â€” low-risk, always safe to execute. Will proceed unless user says
  otherwise.
- `[REVIEW]` â€” involves judgment: task additions, workstream narrative edits.
  Show proposed content explicitly so the user can approve or edit inline.

For any task without a known check-in date, propose a reasonable default
(3â€“5 business days) and note it as a suggestion. The user can override.

Wait for the user to respond before writing anything.

---

## Step 5 â€” Process Approval (one exchange max)

- If the user says "approve all" or any broad affirmative: proceed to Step 6
  for all items.
- If the user calls out specific items to skip, change, or edit: update those
  items only, confirm the change inline ("Got it â€” [what changed]"), then
  proceed to Step 6 for the approved set.
- Do not re-present the full manifest after corrections. Just confirm what
  changed and write.

---

## Step 6 â€” Write on Approval

Execute the following writes in order.

### 6a â€” Create the Meeting Note

Create `meeting-transcripts/meetings/YYYY-MM-DD-[kebab-case-meeting-name].md`.

**Work meeting format:**

```markdown
---
date: YYYY-MM-DD
type: work
attendees: [firstname-lastname, firstname-lastname]
workstreams: [workstream-name]
---

# [Meeting Name] â€” YYYY-MM-DD

**Attendees:** [person-note-link], [person-note-link], ...
**Workstreams:** [workstream-note-link], ...

---

## Topics

### [Topic Name]
[2â€“4 sentence summary. Attribute key points to speaker where relevant.]

---

## Decisions

- [Decision]

---

## My Action Items

- [ ] [Action item] â†’ [[artifacts/Tasklist]]
- [ ] ...

## Others' Action Items

- [Name]: [action item]
- ...
```

**Networking meeting format:**

```markdown
---
date: YYYY-MM-DD
type: networking
attendees: [firstname-lastname]
---

# [Meeting Name / Person Name] â€” YYYY-MM-DD

**With:** [person-note-link]

---

## What We Discussed

[2â€“4 sentence summary.]

---

## What I Learned About Them

[Notable context about the person â€” goals, role, situation.]

---

## Follow-Ups

- [ ] [Follow-up action] â†’ [[artifacts/Tasklist]]
- [ ] ...
```

### 6b â€” Update Task List

Append your action items from this meeting to `artifacts/Tasklist.md`.

- Match the existing format in that file exactly.
- Each task should include a backlink to the meeting note:
  `[[YYYY-MM-DD-meeting-name]]`
- Do not duplicate tasks already in the list.

### 6c â€” Update People Files

For each attendee:

- If a `people/` file exists: append a new interaction entry with the date,
  meeting name (backlinked), and a one-line note on what was discussed with or
  learned about them.
- If no file exists: create a stub at `people/firstname-lastname.md` with
  today's date, meeting name backlink, role (if known), and a blank notes
  section.

### 6d â€” Update Networking Log (networking meetings only)

If meeting type is `networking`, append an entry to
`artifacts/networking-log.md` with: date, person, one-line summary, and
next follow-up action.

### 6e â€” Backlink Workstreams

For each workstream file identified in Step 3:

- Do not modify the workstream file's content.
- Note the meeting reference at the bottom under a `## Recent Meetings`
  section (create the section if it does not exist):
  `- [[YYYY-MM-DD-meeting-name]] â€” [one-line context]`

### 6f — Update Today's Daily Note

Open `artifacts/daily/YYYY-MM-DD.md` for today's date (the date /readmeeting is run, not the meeting date).

- If the file exists: find the `## Meetings` section and append a link:
  `- [[YYYY-MM-DD-meeting-name]] — [one-line description of the meeting]`
  If the `## Meetings` section does not exist, create it between `## Morning Brief` and `## Notes`.
- If no daily note exists for today: skip silently. /endday will catch the meeting via git history.

### 6g — Delete Raw Transcript

Delete the original file from `meeting-transcripts/raw/`. This signals the
file has been processed. If multiple raw files existed for the same meeting,
delete all of them.

---

## Step 7 â€” Confirm and Flag Patterns

After writes complete, output a brief confirmation:

```
âœ… Meeting ingested: [Meeting Name]

Created: meeting-transcripts/meetings/[filename].md
Updated: Tasklist.md ([N] tasks added)
Updated: people/[name].md x[N]
Deleted: meeting-transcripts/raw/[filename]
```

Then, if you made any assumptions in Step 3 that are not already in this
file's `## Learned Patterns (Owner-Confirmed)` section, list them and ask:

"I made the following assumptions that aren't in my patterns file. Want me
to save any of these so I remember them next time?"

- [Assumption 1] â€” e.g., "BIA Weekly Meeting = work meeting, McKay Marshall
  is the presenter"
- ...

If the user confirms, append the approved patterns to the
`## Learned Patterns (Owner-Confirmed)` section in this file.

---

## Principles

- Never write before Step 5 approval.
- Match the existing format of every file you update â€” do not introduce new
  structure without checking what is already there.
- Prefer sparse, high-signal notes over verbose summaries. Capture what
  matters; skip small talk and tangents.
- If a person appears in a transcript but has no people file and no calendar
  entry to confirm their role, create the stub with what is known and flag it.
- If an action item is ambiguous about ownership, assign it to you only if
  it was clearly directed at you. Otherwise log it under others' action items.
- The spec evolves. If something isn't working, the user can ask Claude Code
  to suggest an edit to this file.

