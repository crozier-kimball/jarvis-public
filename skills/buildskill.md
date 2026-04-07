# buildskill

A skill for designing, writing, and iteratively improving skill files within this Personal Agentic OS.

Invoke with: `/buildskill`

---

## Purpose

This skill takes a skill idea — anywhere from a rough name to a mostly-formed workflow — and produces a well-structured `skills/[skillname].md` file ready to drop into the workspace. It also bakes a self-improvement loop into every skill it creates, so each skill gets sharper with use.

---

## Phase 1: Capture the Idea

Before writing anything, understand what the owner actually wants.

Start by reading `user/USER.md` to ground the interview in who the owner is and how they operate. Then ask the following — one at a time, conversationally. Do not present them as a numbered list.

1. **What is the name of the skill?** (This becomes the invoke command, e.g. `/weeklyreview`)
2. **What triggers this skill?** What does the owner say or do that should kick it off?
3. **What should the agent do when it runs?** Walk through the rough steps — even messy is fine.
4. **What files or context does this skill need?** (e.g. does it need to read `artifacts/`, `people/`, transcripts?)
5. **What does a good output look like?** Ask the owner to describe a successful run.
6. **What would a bad run look like?** This surfaces edge cases early.

If the owner already has answers to most of these (they said "roughly between a rough idea and a fairly formed one"), don't re-ask what they've already told you. Extract from context first, ask only for gaps.

---

## Phase 2: Map to the Workspace

Before writing the skill, identify the context routing:

- Which folders does this skill need to read? (`user/`, `people/`, `artifacts/`, `meeting-transcripts/`, `skills/`)
- Does this skill produce output? If so, where does it write? (Default: `artifacts/` for strategic docs, `people/` for relationship updates)
- Does this skill invoke any other skills? (Note any dependencies.)
- Does this skill require information from the owner at runtime, or can it run on existing context alone?

Confirm your routing assumptions with the owner before proceeding.

---

## Phase 3: Write the Skill File

Output the skill as `skills/[skillname].md`.

### Required Structure

```
---
name: [skillname]
description: [one or two sentences — what it does AND when to invoke it. Be specific enough that the agent will trigger it reliably. Err toward over-specifying the trigger rather than under.]
---

# [Skill Name]

[One sentence: what this skill does and why it exists.]

## When to Use
[Specific trigger phrases or conditions. Be concrete.]

## Context to Load
[List exactly which files or folders to read before starting. Use 1-hop from seed notes per CLAUDE.md routing rules.]

## Steps
[Numbered, imperative steps. Each step should be a clear action. Where the agent needs to make a judgment call, say so explicitly rather than leaving it implicit.]

## Output
[What gets written, where, and in what format.]

## Edge Cases
[Known failure modes and how to handle them. Start with at least one, even if speculative.]

## Meta
[See Phase 4 below for rules on this section.]
```

### Writing Principles

These come directly from how the best harnesses work — skills are specs, and spec quality determines output quality:

- **Be literal.** The agent follows skill files literally. Vague steps produce vague behavior. If a step requires judgment, say "use your judgment to..." rather than implying it.
- **Keep it coherent.** Prefer a single file when it improves maintainability and operator clarity. Split only when the owner explicitly asks or when separation is functionally necessary.
- **Front-load the context.** List what to read *before* the steps, not during them. The agent should enter the workflow already loaded.
- **Name the output explicitly.** Don't say "save the result." Say "save as `artifacts/YYYY-MM-DD-[descriptor].md`."
- **One skill, one job.** If the skill is doing two distinct things, consider whether they should be two skills.

---

## Phase 4: The Meta Section

Every skill built by this SOP includes a `## Meta` section at the bottom. This section tracks the skill's evolution without letting it balloon.

### What goes in Meta

```markdown
## Meta

**Version:** 1.0  
**Last improved:** [date of last accepted change]  
**Pending suggestions:**  
- [Suggestion 1 from last run]  
- [Suggestion 2 from last run]  

**Stable runs:** 0  
(Suggestions are frozen after 3 consecutive runs with no accepted changes.)
```

### Rules for updating Meta

After every skill run (when the owner uses the skill it governs), the agent should:

1. Append one to three concrete improvement suggestions to `Pending suggestions` based on what just happened.
2. If the owner accepts any suggestion, apply the change, increment the version, update `Last improved`, and reset `Stable runs` to 0.
3. If the owner accepts no suggestions, increment `Stable runs` by 1.
4. **Once `Stable runs` reaches 3, stop updating `Pending suggestions`.** The skill is considered stable. The Meta section is frozen unless the owner explicitly asks to reopen it.

This prevents the Meta section from becoming a changelog nobody reads. A stable skill stays stable until there's a reason to revisit it.

---

## Phase 5: Optional Validation Run

After writing the skill file, offer — do not require — a dry run:

> "Want me to do a quick test run of this skill using a hypothetical scenario? I'll walk through the steps as if I were executing it and flag anything that feels underspecified."

If the owner says yes, simulate one execution:
- State which files you're reading and what you'd find there
- Walk through each step and narrate the decision at each one
- Note any step where you had to guess what to do
- Summarize what the output would look like

Then ask: "Does that match what you had in mind? Anything to adjust before we save it?"

If the owner says no, save the file as-is.

---

## Phase 6: Save and Register

1. Save the skill file to `skills/[skillname].md`.
2. Add the skill to the skill registry in `CLAUDE.md` under the `## Skills` section. Use this format:
   ```
   - `/[skillname]` — [one-line description]
   ```
3. Confirm with the owner: "Skill saved. You can now invoke it with `/[skillname]`."

---

## Improvement Suggestions for This Skill

After running `/buildskill`, apply the Meta rules above to this file too. Treat `/buildskill` as a skill that improves itself. After 3 stable runs, freeze suggestions.

---

## Reference: Skill Anatomy Cheatsheet

For quick reference when writing steps:

| Element | Rule |
|---|---|
| Trigger | Specific phrases or conditions, not just "when needed" |
| Context loading | Read before steps begin, not mid-workflow |
| Steps | Numbered, imperative, one action each |
| Judgment calls | Made explicit ("use your judgment to prioritize by date") |
| Output | Named file, named folder, named format |
| Edge cases | At least one, even if speculative |
| Length | No hard line limit; optimize for clarity and maintainability |
| Meta | Tracks version and suggestions; freezes at 3 stable runs |
