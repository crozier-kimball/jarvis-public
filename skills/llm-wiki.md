---

name: llm-wiki

description: Build and maintain a persistent, interlinked markdown knowledge base
  following Karpathy's LLM Wiki pattern. Ingest sources, query compiled knowledge,
  and lint for consistency. Works as an Obsidian vault out of the box.

when_to_use: When the user wants to create, build, ingest into, query, or lint a
  personal wiki/knowledge base. Also when they reference notes, research topics, or
  domain learning. Default wiki path is ~/wiki, configurable via LLM_WIKI_PATH env var.

---

# llm-wiki — Personal Knowledge Base

Build a persistent, compounding knowledge base as interlinked markdown files.
Based on [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Unlike RAG (which rediscovers knowledge from scratch per query), the wiki compiles
knowledge once and keeps it current. Cross-references already exist. Contradictions
are flagged. Synthesis reflects everything ingested.

**Division of labor:** Human curates sources and directs analysis. Agent summarizes,
cross-references, files, and maintains consistency.

---

## Wiki Location

Default: `~/wiki`
Configurable via environment variable: `LLM_WIKI_PATH`

Check in order:
1. `$LLM_WIKI_PATH` if set
2. `~/wiki` as fallback

The wiki is a directory of markdown files — works as an Obsidian vault out of the box.

---

## Architecture: Three Layers

```
wiki/
├── SCHEMA.md           # Conventions, structure rules, domain config
├── index.md            # Sectioned content catalog with one-line summaries
├── log.md              # Chronological action log (append-only, rotated yearly)
├── raw/                # Layer 1: Immutable source material
│   ├── articles/       # Web articles, clippings
│   ├── papers/         # PDFs, arxiv papers
│   ├── transcripts/    # Meeting notes, interviews
│   └── assets/         # Images, diagrams referenced by sources
├── entities/           # Layer 2: Entity pages (people, orgs, products, models)
├── concepts/           # Layer 2: Concept/topic pages
├── comparisons/        # Layer 2: Side-by-side analyses
└── queries/            # Layer 2: Filed query results worth keeping
```

**Layer 1 — Raw Sources:** Immutable. Read but never modify.
**Layer 2 — The Wiki:** Agent-owned markdown files. Created, updated, cross-referenced.
**Layer 3 — The Schema:** `SCHEMA.md` defines structure, conventions, tag taxonomy.

## Resuming an Existing Wiki (CRITICAL — do FIRST every session)

1. Read `SCHEMA.md` — understand domain, conventions, tag taxonomy
2. Read `index.md` — learn what exists and the summaries
3. Scan recent `log.md` — last 20-30 entries for recent activity
4. THEN search for the topic at hand before creating anything

This prevents: duplicate pages, missed cross-references, contradicting conventions, repeating work.

## Initializing a New Wiki

1. Determine the wiki path (env var or ask; default `~/wiki`)
2. Create the directory structure above (mkdir -p)
3. Ask what domain the wiki covers — be specific
4. Write `SCHEMA.md` customized to the domain (template below)
5. Write initial `index.md` with sectioned headers
6. Write initial `log.md` with creation entry
7. Confirm ready and suggest first sources to ingest

---

### SCHEMA.md Template

Adapt to the user's domain:

```markdown
# Wiki Schema

## Domain
[What this wiki covers — e.g., "AI/ML research", "personal health", "startup intelligence"]

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., transformer-architecture.md)
- Every wiki page starts with YAML frontmatter (see below)
- Use [[wikilinks]] to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the updated date
- Every new page must be added to index.md under the correct section
- Every action must be appended to log.md

## Frontmatter
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
---

## Tag Taxonomy
[Define 10-20 top-level tags for the domain. Add new tags here BEFORE using them.]

Example for AI/ML:
- Models: model, architecture, benchmark, training
- People/Orgs: person, company, lab, open-source
- Techniques: optimization, fine-tuning, inference, alignment, data
- Meta: comparison, timeline, controversy, prediction

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it. This prevents tag sprawl.

## Page Thresholds
- Create a page when an entity/concept appears in 2+ sources OR is central to one source
- Add to existing page when a source mentions something already covered
- DON'T create a page for passing mentions, minor details, or things outside the domain
- Split a page when it exceeds ~200 lines — break into sub-topics with cross-links
- Archive a page when its content is fully superseded — move to _archive/, remove from index

## Entity Pages
One page per notable entity. Include:
- Overview / what it is
- Key facts and dates
- Relationships to other entities ([[wikilinks]])
- Source references

## Concept Pages
One page per concept or topic. Include:
- Definition / explanation
- Current state of knowledge
- Open questions or debates
- Related concepts ([[wikilinks]])

## Comparison Pages
Side-by-side analyses. Include:
- What is being compared and why
- Dimensions of comparison (table format preferred)
- Verdict or synthesis
- Sources

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: contradictions: [page-name]
4. Flag for user review
```

### index.md Template

```markdown
# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: YYYY-MM-DD | Total pages: N

## Entities
<!-- Alphabetical within section -->

## Concepts

## Comparisons

## Queries
```

When a section exceeds 50 entries, split into sub-sections by first letter or sub-domain.

### log.md Template

```markdown
# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: ## [YYYY-MM-DD] action | subject
> Actions: ingest, update, query, lint, create, archive, delete

## [YYYY-MM-DD] create | Wiki initialized
- Domain: [domain]
- Structure created with SCHEMA.md, index.md, log.md
```

Rotate when exceeding 500 entries: rename to `log-YYYY.md`, start fresh.

---

## Core Operations

### 1. Ingest

When user provides a source (URL, file, paste):

Step 1 — **Capture the raw source:**
   - URL → fetch content (curl, wget, web extraction), save to `raw/articles/`
   - PDF → extract text, save to `raw/papers/`
   - Pasted text → save to appropriate `raw/` subdirectory
   - Name descriptively: `raw/articles/author-topic-year.md`

Step 2 — **Check what already exists** — search index.md and existing pages for mentioned
   entities/concepts. This is the difference between a growing wiki and a duplicate pile.

Step 3 — **Write or update wiki pages:**
   - New entities/concepts: Only if they meet Page Thresholds (2+ source mentions
     or central to one source)
   - Existing pages: Add new info, update facts, bump `updated` date
   - Cross-reference: Every page must link to at least 2 other pages via [[wikilinks]]
   - Tags: Only from the taxonomy in SCHEMA.md

Step 4 — **Update navigation:**
   - Add new pages to `index.md` under correct section, alphabetically
   - Update "Total pages" count and "Last updated" date
   - Append to `log.md`: `## [YYYY-MM-DD] ingest | Source Title`
   - List every file created or updated

Step 5 — **Report what changed** — list every file created or updated.

### 2. Query

When user asks a question about the wiki's domain:

Step 1 — Read `index.md` to identify relevant pages
Step 2 — For wikis with 100+ pages, also grep across all .md files for key terms
Step 3 — Read the relevant pages
Step 4 — Synthesize an answer from compiled knowledge. Cite wiki pages: "Based on [[page-a]] and [[page-b]]..."
Step 5 — File valuable answers back — if the answer is a substantial comparison or novel
   synthesis, create a page in `queries/` or `comparisons/`. Don't file trivial lookups.
Step 6 — Update log.md with the query and whether it was filed.

### 3. Lint

When user asks to lint, health-check, or audit:

Step 1 — **Orphan pages:** Pages with no inbound [[wikilinks]] from other pages
Step 2 — **Broken wikilinks:** [[links]] pointing to pages that don't exist
Step 3 — **Index completeness:** Every wiki page should appear in index.md
Step 4 — **Frontmatter validation:** Every page must have all required fields
Step 5 — **Stale content:** Pages whose `updated` date is >90 days older than newest source
Step 6 — **Contradictions:** Pages on same topic with conflicting claims
Step 7 — **Page size:** Flag pages over 200 lines — candidates for splitting
Step 8 — **Tag audit:** Flag any tags not in the SCHEMA.md taxonomy
Step 9 — **Log rotation:** If log.md exceeds 500 entries, rotate it
Step 10 — **Report findings** grouped by severity (broken links > orphans > stale > style)
Step 11 — **Append to log.md:** `## [YYYY-MM-DD] lint | N issues found`

---

## Commands Reference

```bash
export WIKI="${LLM_WIKI_PATH:-$HOME/wiki}"

# List all wiki pages
find "$WIKI" -name "*.md" -not -path "*/raw/*" -not -path "*/_archive/*" -type f

# Search by content
grep -rli "keyword" "$WIKI" --include="*.md" | grep -v "/raw/"

# Search by filename
find "$WIKI" -name "*keyword*.md" -type f

# Search by tag
grep -rl "tags:.*alignment" "$WIKI" --include="*.md" | grep -v "/raw/"

# Count pages
find "$WIKI" -name "*.md" -not -path "*/raw/*" -not -path "*/_archive/*" -not -name "SCHEMA.md" -not -name "index.md" -not -name "log.md" | wc -l
```

## Obsidian Integration

The wiki directory works as an Obsidian vault:
- `[[wikilinks]]` render as clickable links
- Graph View visualizes the knowledge network
- YAML frontmatter powers Dataview queries
- `raw/assets/` folder holds images via `![[image.png]]`

For best results:
- Set Obsidian's attachment folder to `raw/assets/`
- Enable "Wikilinks" in Obsidian settings (on by default)
- Install Dataview plugin for queries like: `TABLE tags FROM "entities" WHERE contains(tags, "company")`

---

## Pitfalls

- **Never modify files in `raw/`** — sources are immutable
- **Always orient first** — read SCHEMA + index + recent log before any operation. Skipping causes duplicates.
- **Always update index.md and log.md** — skipping makes the wiki degrade
- **Don't create pages for passing mentions** — follow Page Thresholds
- **Don't create pages without cross-references** — every page links to 2+ others
- **Frontmatter is required** — enables search, filtering, staleness detection
- **Tags from taxonomy only** — freeform tags decay into noise
- **Keep pages scannable** — readable in 30 seconds; split over 200 lines
- **Handle contradictions explicitly** — don't silently overwrite. Note both claims with dates.
- **Rotate the log** — when exceeding 500 entries
- **Ask before mass-updating** — if ingest touches 10+ existing pages, confirm scope
