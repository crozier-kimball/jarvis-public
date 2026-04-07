---

name: today

description: Morning planning ritual. Reads today's daily note dump,

yesterday's wrap, calendar, tasks, and relevant project context.

Produces a time-blocked daily brief for approval.

when_to_use: Called by the user at the start of their day after they

have created a daily note via voice dump. Produces the day's plan.

daily_pair: "/today opens the day; /endday closes it. /endday writes

artifacts/daily/YYYY-MM-DD-endday.md, which /today reads the following morning."

---

  

# /brief â€” Morning Daily Brief

  

## Purpose

Transform the user's morning voice dump into a structured,

time-blocked daily plan. Minimize back-and-forth. Load only what

is necessary to build the plan. Write nothing until the user approves.

  

---

  

## Day Boundary Rule

The owner works past midnight. Before reading or writing any dated file, determine the correct working date:

```bash
hour=$(date '+%H')
if [ “$hour” -lt 4 ]; then
  working_date=$(date -d 'yesterday' '+%Y-%m-%d')
else
  working_date=$(date '+%Y-%m-%d')
fi
```

If the current time is before 4:00 AM, treat “today” as yesterday's calendar date. Use `$working_date` everywhere `YYYY-MM-DD` appears in this skill.

---

## Step 1 — Load Context (silent, no output yet)

  

Read the following in order. Do not summarize to the user yet.

  

1. **Today's daily note** â€” find the file matching today's date in

`artifacts/daily/`. This is the user's dump. It is the primary input.

  

2. **Yesterday's daily note** â€” find the most recent `YYYY-MM-DD.md`

in `artifacts/daily/` and read its `## End of Day` section. If none

exists within 5 days, skip to Step 1b. If the most recent file is

older than 5 days, skip to Step 1c.

  

3. **Google Calendar** â€” pull today's events only. For each event

with attendees:

Â  Â - Check `people/` for an existing file for each attendee

Â  Â - If file exists, load it (name, current context, last

Â  Â interaction only â€” not full history)

Â  Â - If file does not exist, flag for creation after approval

  

4. **Ongoing task list** â€” read `artifacts/Tasklist.md`. Load task

names and status only. Do not load full project files unless a

task is marked active or in-progress today.

  

5. **Networking log** â€” read `artifacts/networking-log.md`. Count

outreaches in the last 7 days. Flag if fewer than 2.

  

6. **Workout log** â€” read `artifacts/workout-log.md`. Check if

today has a workout logged. Binary: yes or no.

  

7. **Spiritual study log** â€” read `artifacts/spiritual-log.md`.

Check if today has an entry. Binary: yes or no.

  

---

  

## Step 1b â€” No Wrap File Found (within 5 days)

  

Proceed without wrap context. Note in the brief that no recent

wrap was found. Carry forward any incomplete tasks visible in

the task list.

  

---

  

## Step 1c â€” Wrap File Older Than 5 Days

  

Before building the brief, ask the user the following questions

one at a time:

  

1. What did you finish since your last check-in?

2. What's still in progress?

3. Anything that was blocked or dropped?

4. Any new commitments or priorities that came up?

  

Capture responses and treat them as a catch-up wrap. Save to

`artifacts/daily/YYYY-MM-DD-catchup-wrap.md` after approval.

Then continue to Step 2.

  

---

  

## Step 2 â€” Present Summary (first output to user)

  

Present a single short summary block. Keep it tight. Example format:

Here's what I see for today:

ðŸ“… Meetings: [list meeting names, times, and attendees]

ðŸ“‹ Active tasks: [list today-relevant tasks from task list]

â³ Carried forward: [any incomplete items from yesterday's wrap]

âš ï¸ Flags: [networking behind / no workout logged / no spiritual

study yet â€” only include what applies]

What am I missing or what's changed?

Wait for the user to respond. This is the dump review exchange.

  

---

  

## Step 3 â€” Clarify if Needed (one exchange max)

  

If the user's dump or response makes priority order ambiguous,

ask one clarifying question only. Example:

  

"You mentioned both the dashboard and the visa â€” which one needs

to happen first?"

  

Do not ask multiple questions. If timing or duration is unclear

for a task, make a reasonable estimate based on what the user

has said and flag it in the plan.

  

---

  

## Step 4 â€” Build the Time-Blocked Brief

  

Using the user's dump, calendar events, and any clarification,

build a time-blocked schedule. Follow these rules:

  

**Scheduling rules:**

- Start from the current time, not a fixed hour

- Fixed calendar events are anchors â€” build around them

- Apply the user's prioritization framework:

Â  1. Urgent + Important (deadlines, meetings, deliverables)

Â  2. Important (projects, career, skill development)

Â  3. Maintenance (Python, SQL, technical practice)

- One task per block

- No multitasking

- Hard tasks earlier, light tasks later

- If energy is low or user flags fatigue, shift to maintenance

  

**Health and balance checks (add to plan if not already present):**

- Workout: if not logged and it's a weekday, add a block or flag

it as unscheduled

- Spiritual study: if not logged, add a 15-minute block or flag it

- Networking: if fewer than 2 outreaches this week, add a

15-minute block labeled "Networking outreach"

  

**Output format:**

ðŸ“‹ DAILY BRIEF â€” [Date]

[Time]â€“[Time] â€” [Task] ([duration])

â†’ [One line objective or goal for this block]

[Time]â€“[Time] â€” [Task] ([duration])

â†’ [One line objective]

...

â­ï¸ Intentionally deferred:

  

[Task] â€” [brief reason]

  

ðŸ” Carried forward to tomorrow if needed:

  

[Task]

Present the brief to the user. Ask:

"Does this work, or do you want to adjust anything?"

  

---

  

## Step 5 â€” Approval and Write

  

Once the user approves (any affirmative response), execute

the following writes in order:

  

1. **Write the morning brief into today's daily note** —

Open `artifacts/daily/YYYY-MM-DD.md` (create from template if it does not exist).

Replace the `## Morning Brief` section with the approved time-blocked plan.

Do not create a separate brief file.

  


2. **Update task list** — mark any tasks started today as

in-progress in `artifacts/Tasklist.md`. Add any new tasks

mentioned in the dump or the full daily note (including Notes

section entries such as workout log, spiritual log, session notes).

  

3. **Route people mentions** — for anyone mentioned in the dump

or conversation (not just meeting attendees), append context

to their `people/` file with a backlink to today's daily note.

If no file exists, create a stub at `people/First Last.md`

with today's date and a blank notes section.

  

4. **Route workstream/project mentions** — any strategic thought,

decision, or project update mentioned in the dump, route to

the relevant artifact file with a backlink to today's daily note.

  

5. **Update networking log** — if a networking outreach was

mentioned in the dump, add it to `artifacts/networking-log.md`.

  

6. **Flag new backlinks** — if any task or project mentioned

in the dump does not have a corresponding file in `artifacts/`,

note it at the bottom of the daily brief as:

`⚠️ No project file found for [project name] — create one?`

  

Do not create project files automatically. Flag only.

  

---

  


---

## Mid-Day Check-In Pattern

When the user asks to "check in on the daily note" (or similar),
execute the following:

1. Read the current state of `artifacts/daily/YYYY-MM-DD.md`
2. Identify new content added since the last routing pass
   (new Notes entries, log updates, decisions, people mentions)
3. Route that content to appropriate files with backlinks
   to today's daily note — same rules as Step 5 above
4. Report back: what was routed and where

Do not re-route content already processed in a previous pass.

## Principles

  

- Load minimum necessary context. Do not read full project

files unless directly needed to resolve ambiguity.

- Never write before approval.

- Keep exchanges to 3 maximum before presenting the plan.

- The spec evolves. If something isn't working, the user can

ask Claude Code to suggest an edit to this file.
