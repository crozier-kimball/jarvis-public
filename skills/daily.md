---
name: daily
description: Generates today's daily note template in artifacts/daily/YYYY-MM-DD.md by running tools/scripts/daily.py. Use at the start of each day before /today to pre-scaffold the note structure.
---

# /daily — Generate Daily Note Template

Runs the daily template generator script to create a blank scaffold for today's date. Run this once each morning. `/today` then populates it.

## When to Use

When the owner says `/daily`, "build today's note", "generate the daily template", or similar at the start of their day.

## Steps

1. Run the script:
   ```bash
   python tools/scripts/daily.py
   ```

2. Report the result to the owner:
   - If created: `Created: artifacts/daily/YYYY-MM-DD.md — ready for /today.`
   - If already exists: `Today's note already exists. Run /today to populate it.`

That's it. Do not load context, do not ask questions, do not route anything. This skill is mechanical.

## Edge Cases

- **Script not found:** If `tools/scripts/daily.py` is missing, tell the owner and stop. Do not recreate the file manually.
- **Permission error on write:** Surface the error message verbatim and stop.
- **Wrong date:** The script uses the machine's local timezone. If the date looks wrong, the machine clock is the source — flag it to the owner.

## Meta

**Version:** 1.0
**Last improved:** 2026-04-09
**Pending suggestions:** none
**Stable runs:** 0
