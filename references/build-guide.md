# Build guide

Conceptual reference for the build phase. The source of truth for all CSS and JS is `templates/base-scaffold.html` — this guide covers only what Claude needs to know to customize and run the build.

## Technical constraints

- **HTML/CSS/JS only.** No frameworks, no build tools, no dependencies
- **Google Fonts** for typography (loaded via `<link>` in `<head>`)
- **Single file.** The entire scrollytelling piece lives in one `.html` file
- **Images** referenced at relative paths (e.g., `slides/slide-NNN.jpg`)

## Customization points

The scaffold has two areas to customize per project, both clearly marked with `REPLACE` comments:

1. **Google Fonts `<link>`** — swap to the project's font families
2. **`:root` CSS variables** — set the project's palette and typography tokens:
   - `--bg`, `--text`, `--text-dim`, `--text-faint` — background and text hierarchy
   - `--gold`, `--gold-light`, `--gold-dim` — accent color at full, light, and low-opacity
   - `--serif`, `--body` — display and body font stacks

Everything else in the scaffold (beat type CSS, animations, scroll handlers, responsive rules) is stable infrastructure that works without modification.

## Responsive approach

Single breakpoint at `max-width: 900px`. Split layouts stack vertically, triptych becomes single column, section indicator is hidden. No per-project responsive work needed — it's handled by the scaffold.

## Build script

`scripts/build.py` reads the BEATS JSON from the storyboard and assembles final HTML:

```
python3 ~/.claude/skills/scrollytelling-generator/scripts/build.py storyboard.html --output scrollytelling.html --scaffold base-scaffold-custom.html
```

The script handles all structural HTML generation — it is deterministic and produces correct output for all beat types. **Do NOT read `build.py`** — just run it. Reading the script wastes context budget on implementation details Claude doesn't need. Claude's role in build is: customize the scaffold's design tokens, run the script, review the output.
