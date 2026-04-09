---
name: tailorcv
description: Tailors the master CV to a specific job application. Invoke when the owner has a job description and wants a CV optimised for that role. Reads cv-v1.md and career-history.md, maps the JD requirements to the owner's strongest stories, and produces a tailored CV ready for review.
---

# /tailorcv

Generates a tailored CV for a specific job application by matching the owner's experience and stories to the role's requirements.

## When to Use

- Owner says "tailor my CV for [company/role]"
- Owner is preparing to apply to a specific role and has a JD available
- Owner wants to know how well their profile maps to a JD before applying

## Context to Load

Load before starting — do not load mid-workflow:

1. `artifacts/job-search/cv-v1.md` — master CV (source of truth for structure and bullets)
2. `artifacts/job-search/career-history.md` — STAR story bank (richer context behind each bullet)
3. `artifacts/job-search/applications-tracker.md` — to check if this company/role already has an entry
4. The JD — provided by the owner at runtime (pasted in chat or file path given)

## Steps

1. **Receive the JD.** If the owner has not yet provided it, ask: "Paste the JD here or give me the file path."

2. **Analyse the JD.** Extract and note silently (do not output yet):
   - Role title, company, location
   - Top 5 required skills/experiences (ranked by prominence in JD)
   - Top 3 "nice to have" skills
   - Keywords that should appear in the CV (tools, methodologies, concepts)
   - Tone signals (data-driven, leadership-heavy, startup, enterprise, etc.)

3. **Map the JD to the owner's profile.** For each top requirement, identify:
   - Which CV bullet(s) from `cv-v1.md` address it most directly
   - Whether `career-history.md` contains a stronger version of that story
   - Any requirement that has no clear match — flag as a gap

4. **Draft the tailored CV.** Follow these rules:
   - **Preserve the master CV structure** — same sections, same format as `cv-v1.md`
   - **Add a Profile paragraph** (3–4 lines) at the top, below contact info. Tailor it to the specific role and company. Do not fabricate — draw from USER.md and cv-v1.md only.
   - **Reorder bullets within each role** so the most JD-relevant bullet appears first
   - **Swap in richer versions** of bullets where `career-history.md` has better numbers or context than the master CV — only if factually consistent
   - **Incorporate JD keywords naturally** — do not force them, do not fabricate experience
   - **Do not add skills or experience the owner does not have**
   - Keep the CV to one page if possible; flag if it runs over

5. **Present gap summary before showing the draft.** Before outputting the full CV, show:
   ```
   ✅ Strong matches: [list top 3]
   ⚠️ Partial matches: [list any]
   ❌ Gaps: [list requirements with no match — be honest]
   ```
   Ask: "Want to proceed with the draft, or address any gaps first?"

6. **Output the tailored CV** after owner confirms. Format identically to `cv-v1.md`.

7. **Propose the save.** State: "I'll save this as `artifacts/job-search/cv-[company-slug].md` — okay?" Use lowercase kebab-case for company slug (e.g. `cv-preply.md`, `cv-google-analytics.md`). If the same company has multiple roles, use `cv-[company]-[role-slug].md`.

8. **After approval, write the .md file** and update `artifacts/job-search/applications-tracker.md`:
   - If the company already has a row, add the tailored CV filename to the Notes column
   - If not, add a new row with status `applied` (or `screening` if contact already made)

9. **Generate the HTML export.** Read `artifacts/job-search/templates/cv-template.html` as the base structure. Produce `artifacts/job-search/cv-[company-slug].html` by:
   - Replacing all content sections with the approved tailored CV content
   - Using American English throughout
   - Removing all tailoring notes (anything in the `## Tailoring Notes` section)
   - Preserving the exact CSS and layout from the template

10. **Export PDF via Chrome headless.** Run the following command (replace slug as needed):
    ```bash
    "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" --headless --disable-gpu --print-to-pdf="C:\\Users\\feser\\Desktop\\Python\\jarvis\\artifacts\\job-search\\cv-[company-slug].pdf" --print-to-pdf-no-header "C:\\Users\\feser\\Desktop\\Python\\jarvis\\artifacts\\job-search\\cv-[company-slug].html"
    ```
    Confirm the file was written. Tell the owner: "PDF saved as `cv-[company-slug].pdf`."

## Output

- `artifacts/job-search/cv-[company-slug].md` — tailored CV, approved by owner
- `artifacts/job-search/cv-[company-slug].html` — HTML source for PDF generation
- `artifacts/job-search/cv-[company-slug].pdf` — final export, generated via Chrome headless
- Updated row in `artifacts/job-search/applications-tracker.md`

## Edge Cases

- **JD is vague or generic:** Flag to owner — "This JD is light on specifics. Tailoring will be limited. I'll optimise for the role title and company context instead." Proceed with what's available.
- **Role requires tools the owner doesn't have:** List as a gap in Step 5. Do not add them to the CV. If minor (e.g. Looker basics), suggest owner notes them as "familiar with" only if truthful.
- **Same company, multiple roles:** Use `cv-[company]-[role-slug].md` naming. Do not overwrite a previous tailored CV.
- **Master CV has a ⚠️ flag unresolved:** Surface it before tailoring. Example: if a number is marked as unconfirmed, do not use it in the tailored version until resolved.
- **Owner provides a URL instead of pasting the JD:** Attempt to fetch. If the page is JS-rendered and fetch fails, ask owner to paste the text directly.

## Meta

**Version:** 1.2
**Last improved:** 2026-04-09
**Pending suggestions:** none yet — run the skill to generate first suggestions
**Stable runs:** 0
