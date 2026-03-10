# Discover subagent prompt

The parent reads this file, replaces the `{{placeholders}}`, and passes the entire result as the `task` parameter to the Agent tool. Do not summarize, abbreviate, or rewrite any part of this prompt.

**Placeholders to replace:**
- `{{PROJECT_DIR}}` — absolute path to the project directory
- `{{PPTX_FILENAME}}` — name of the .pptx file (e.g., `my-presentation.pptx`)

---

## Task

You are running the discover phase of the scrollytelling-generator skill. Your job: extract slides from a presentation, read all slide images and metadata, then write a structured analysis file. All work happens in this subagent — when you finish, your context (including all slide images) is released.

**Project directory:** `{{PROJECT_DIR}}`

## Step 1: Extract slides (if needed)

If a `slides/` directory does not already exist in the project directory, run this command:

```
~/.claude/skills/scrollytelling-generator/scripts/.venv/bin/python3 ~/.claude/skills/scrollytelling-generator/scripts/extract.py "{{PROJECT_DIR}}/{{PPTX_FILENAME}}" --output-dir "{{PROJECT_DIR}}"
```

This creates `slides/` (JPG images) and `slides-data.json` (text metadata). If `slides/` already exists, skip this step.

Do NOT read the extract.py script — just run it.

## Step 2: Read source material

1. Read `{{PROJECT_DIR}}/slides-data.json` for text content and speaker notes
2. Read all slide images in `{{PROJECT_DIR}}/slides/` for visual analysis

Both are needed — the JSON has the narrative content, the images have the visual design.

## Step 3: Write discover-analysis.md

Save a file at `{{PROJECT_DIR}}/discover-analysis.md` covering all of the following sections:

### Analysis sections

1. **Topic and thesis** — what the presentation is about, its central argument
2. **Overall structure table** — sections, slides per section, narrative function, content density
3. **Narrative arc** — how the story builds, turns, and resolves
4. **Key moments and structural features** — bookends, before/after pairs, parallel patterns, dramatic moments
5. **Slide type observations** — common patterns (title slides, content slides, transition slides, etc.)
6. **Slide count and content density per section**
7. **Visual reference notes** — one row per slide, using the exact format below

### Visual reference notes format

This table is critical — it's the bridge that lets later phases work from the analysis rather than re-reading all slide images. Include every slide.

| Slide | Layout pattern | Visual elements | Color/type notes | Density | Beat type candidates |
|-------|---------------|-----------------|------------------|---------|---------------------|
| 1 | Full-bleed, centered text | Title in serif, gold accent word, subtitle in italic | Dark bg, cream/gold | Low | cinematic, dramatic |
| 2 | Single stat, centered | Large display number, supporting line below | Dark bg, gold numeral | Low | dramatic, slide |

**Column definitions:**

- **Layout pattern**: single panel, two-panel split, grid, full-bleed image, text-only, stat callout, etc.
- **Visual elements**: key imagery, diagrams, mockups, icons, typography treatments
- **Color/type notes**: dominant colors, font styles observed, accent usage
- **Density**: Low (cinematic/atmospheric), Medium (concept + supporting detail), High (dense content/reference)
- **Beat type candidates**: 1-2 suggested beat types with the strongest fit listed first. Valid types: `cinematic`, `dramatic`, `slide`, `split`, `crossfade`, `triptych`, `montage`, `text`, `brief`, `break`

## Done

After writing discover-analysis.md, stop. Do not read any other reference files. Do not proceed to explore or any other phase.
