---
name: today
description: Morning planning ritual. Loads context, creates today's daily
  note if it doesn't exist, collects the user's brain dump, and produces a
  time-blocked daily brief for approval.
when_to_use: Called by the user at the start of their day. No pre-existing
  daily note or voice dump required — the skill creates the note and collects
  the dump as part of the ritual.
daily_pair: "/today opens the day; /endday closes it. /endday writes
  artifacts/daily/YYYY-MM-DD.md End of Day section, which /today reads the
  following morning."
---

# /today — Morning Daily Brief

## Purpose

Open the day: load context, create today's daily note if it doesn't exist,
collect the user's brain dump, and produce a time-blocked plan. The user
does not need to prepare anything before running this skill — it starts
from scratch each morning and builds forward.

Write nothing until the user approves the brief.

---

## Day Boundary Rule

The owner works past midnight. Before reading or writing any dated file,
determine the correct working date:

```bash
hour=$(date '+%H')
if [ "$hour" -lt 4 ]; then
  working_date=$(date -d 'yesterday' '+%Y-%m-%d')
else
  working_date=$(date '+%Y-%m-%d')
fi
```

If the current time is before 4:00 AM, treat "today" as yesterday's calendar
date. Use `$working_date` everywhere `YYYY-MM-DD` appears in this skill.

---

## Step 1 — Load Context (silent, no output yet)

Read the following in order. Do not summarize to the user yet.

0. **Vault index** — read `index.md` for fast orientation. Use it to identify
   which people, workstreams, and artifacts are relevant before loading anything
   else.

1. **Today's daily note** — check for `artifacts/daily/YYYY-MM-DD.md`.
   - If it exists, read it. It may contain an early dump or carry-forward notes.
   - If it does not exist, that is normal. Create it from the template in Step
     1a and continue loading context. The dump will be collected in Step 2.

2. **Yesterday's daily note** — find the most recent `YYYY-MM-DD.md` in
   `artifacts/daily/` and read its `## End of Day` section. If none exists
   within 5 days, skip to Step 1b. If the most recent file is older than 5
   days, skip to Step 1c.

3. **Google Calendar** — pull today's events only. For each event with
   attendees:
   - Check `people/` for an existing file for each attendee
   - If file exists, load it (name, current context, last interaction only —
     not full history)
   - If file does not exist, flag for creation after approval

4. **Ongoing task list** — read `artifacts/Tasklist.md`. Load task names and
   status only. Do not load full project files unless a task is marked active
   or in-progress today.

5. **Networking log** — read `artifacts/networking-log.md`. Count outreaches
   in the last 7 days. Flag if fewer than 2.

6. **Workout log** — read `artifacts/workout-log.md`. Check if today has a
   workout logged. Binary: yes or no.

7. **Spiritual study log** — read `artifacts/spiritual-log.md`. Check if today
   has an entry. Binary: yes or no.

8. **Watched sites** — read `artifacts/watched-sites.md`. For each site marked
   **auto**:
   - Fetch the URL
   - Extract the marker described in the "What to extract" field
   - If `last_seen_marker` is empty or "(none yet)": flag as
     "Baseline set — [marker]" (first run)
   - If marker differs from `last_seen_marker`: flag as new content with the
     extracted marker and capture a direct link to the new article or post if
     available
   - If same: no output needed
   For each site marked **manual**: surface as a reminder if `last_verified` is
   "never" or more than 7 days ago.

---

## Step 1a — Create Today's Daily Note (if it doesn't exist)

Create `artifacts/daily/YYYY-MM-DD.md` with this template:

```markdown
---
date: YYYY-MM-DD
---

# [Month Day, Year]

## Morning Brief

<!-- Filled in after approval -->

## Suggestions

<!-- Jarvis-generated suggestions: drafts, priority flags, networking, scheduling -->

## Meetings

<!-- Add meetings here -->

## Notes

<!-- Add workout log, spiritual log, and session notes below -->
```

Do not announce this to the user. Continue to Step 2.

---

## Step 1b — No Wrap File Found (within 5 days)

Proceed without wrap context. Note in the brief that no recent wrap was found.
Carry forward any incomplete tasks visible in the task list.

---

## Step 1c — Wrap File Older Than 5 Days

Before building the brief, ask the user the following questions one at a time:

1. What did you finish since your last check-in?
2. What's still in progress?
3. Anything that was blocked or dropped?
4. Any new commitments or priorities that came up?

Capture responses and treat them as a catch-up wrap. Save to
`artifacts/daily/YYYY-MM-DD-catchup-wrap.md` after approval. Then continue
to Step 2.

---

## Step 2 — Present Summary and Collect Dump (first output to user)

Present a short summary of what was loaded, then ask for the brain dump.
Keep it tight. Example format:

---
Here's what I see for today:

📅 Meetings: [list meeting names, times, and attendees — or "None loaded (no calendar access)"]
📋 Carried forward: [incomplete items from yesterday's wrap]
⚠️ Flags: [networking behind / no workout logged / no spiritual study yet — only include what applies]
🌐 Site updates: Present as a three-column table — **Site | New Content | Link** — for any sites with new content. Include a direct link to the specific new article or post when available. Omit unchanged sites entirely.

What's on your mind for today? Give me your brain dump and I'll build the plan.

---

Wait for the user's response. This is the dump collection exchange.
Do not build the time-blocked plan until after the dump is received.

---

## Step 3 — Clarify if Needed (one exchange max)

If the user's dump makes priority order ambiguous, ask one clarifying question
only. Example:

"You mentioned both the dashboard and the visa — which one needs to happen
first?"

Do not ask multiple questions. If timing or duration is unclear for a task,
make a reasonable estimate based on what the user has said and flag it in the
plan.

---

## Step 4 — Build the Time-Blocked Brief

Using the user's dump, calendar events, and any clarification, build a
time-blocked schedule. Follow these rules:

**Scheduling rules:**
- Start from the current time, not a fixed hour
- Fixed calendar events are anchors — build around them
- Apply the user's prioritization framework:
  1. Urgent + Important (deadlines, meetings, deliverables)
  2. Important (projects, career, skill development)
  3. Maintenance (Python, SQL, technical practice)
- One task per block
- No multitasking
- Hard tasks earlier, light tasks later
- If energy is low or user flags fatigue, shift to maintenance

**Health and balance checks (add to plan if not already present):**
- Workout: if not logged and it's a weekday, add a block or flag it as
  unscheduled
- Spiritual study: if not logged, add a 15-minute block or flag it
- Networking: if fewer than 2 outreaches this week, add a 15-minute block
  labeled "Networking outreach"

**Output format:**

```
📋 DAILY BRIEF — [Date]

[Time]–[Time] — [Task] ([duration])
→ [One line objective or goal for this block]

[Time]–[Time] — [Task] ([duration])
→ [One line objective]

...

⭐ Intentionally deferred:
[Task] — [brief reason]

📝 Carried forward to tomorrow if needed:
[Task]

---

💡 Suggestions from Jarvis

**Drafts**
[Label]: [Draft content — only include if a draft was requested or clearly needed]

**Priority flags**
[Any priority or sequencing suggestions based on context — only include if non-obvious]

**Networking**
[Suggested outreach — only include if networking is behind or a timely opportunity is visible]

**Scheduling**
[Calendar or timing suggestions — only include if something is unscheduled that should be]
```

Omit any Suggestions subsection that has nothing to add. If no suggestions at
all, omit the section entirely.

Present the brief to the user. Ask: "Does this work, or do you want to adjust
anything?"

---

## Step 5 — Approval and Write

Once the user approves (any affirmative response), execute the following
writes in order:

1. **Write the morning brief into today's daily note** — open
   `artifacts/daily/YYYY-MM-DD.md`. Replace the `## Morning Brief` section
   with the approved time-blocked plan. Do not create a separate brief file.

2. **Write the Suggestions section into today's daily note** — append a
   `## Suggestions` section after `## Morning Brief`. Include only the
   subsections that had content (Drafts, Priority flags, Networking,
   Scheduling). If no suggestions were generated, omit the section entirely.

3. **Update task list** — mark any tasks started today as in-progress in
   `artifacts/Tasklist.md`. Add any new tasks mentioned in the dump or the
   full daily note (including Notes section entries such as workout log,
   spiritual log, session notes).

4. **Route people mentions** — for anyone mentioned in the dump or conversation
   (not just meeting attendees), append context to their `people/` file with a
   backlink to today's daily note. If no file exists, create a stub at
   `people/First Last.md` with today's date and a blank notes section.

5. **Route workstream/project mentions** — any strategic thought, decision, or
   project update mentioned in the dump, route to the relevant artifact file
   with a backlink to today's daily note.

6. **Update networking log** — if a networking outreach was mentioned in the
   dump, add it to `artifacts/networking-log.md`.

7. **Flag new backlinks** — if any task or project mentioned in the dump does
   not have a corresponding file in `artifacts/`, note it at the bottom of the
   daily brief as: `⚠️ No project file found for [project name] — create one?`
   Do not create project files automatically. Flag only.

---

## Mid-Day Check-In Pattern

When the user asks to "check in on the daily note" (or similar), execute the
following:

1. Read the current state of `artifacts/daily/YYYY-MM-DD.md`
2. Identify new content added since the last routing pass (new Notes entries,
   log updates, decisions, people mentions)
3. Route that content to appropriate files with backlinks to today's daily note
   — same rules as Step 5 above
4. Report back: what was routed and where

Do not re-route content already processed in a previous pass.

---

## Principles

- Load minimum necessary context. Do not read full project files unless
  directly needed to resolve ambiguity.
- Never write before approval.
- Keep exchanges to 3 maximum before presenting the plan.
- The spec evolves. If something isn't working, the user can ask Claude Code
  to suggest an edit to this file.
