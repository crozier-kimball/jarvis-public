---
name: safe-file-editing
category: workflow
description: "Always read files before modifying them. Prefer patch over write_file. Prevents accidental data loss when editing existing files."
---

# Safe File Editing

Always use this when modifying any file that may already contain content.

## Trigger

Before any file modification (create, update, append, delete).

## Rules

1. **ALWAYS read the file first.** Use `read_file` to see current content before touching it.
2. **Never trust search_files alone.** It confirms a file exists but reveals nothing about its content.
3. **Prefer `patch` over `write_file`** for targeted edits — preserves surrounding content.
4. **Only use `write_file` when:**
   - The file does not exist (confirmed via read_file returning "not found")
   - A complete rewrite is explicitly requested
   - The entire content is known and intentional
5. **Git-tracked files are safer but not immune.** Always read first regardless.
6. **Untracked files are DANGER ZONE.** No git recovery path exists — overwriting destroys content permanently.

## Workflow

1. `read_file(path)` — get current content
2. Decide: `patch` (add/change section) or `write_file` (complete rewrite only if file doesn't exist)
3. Verify the result makes sense with current content
4. Add to Tasklist if relevant

## Pitfalls

- Search tools can return misleading results. Always verify with `read_file`.
- `write_file` completely overwrites — it does NOT merge or append.
