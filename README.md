# Scrollytelling generator

A Claude Code skill that converts presentations into scrollytelling HTML — editorial narrative woven through visual beats with intentional layout, pacing, and motion design.

Give it a PPTX file. It reads every slide, analyzes the narrative structure, maps slides and presenter notes to scrollytelling layout patterns, and builds a self-contained HTML page where the presentation's story is transformed into a reading experience.

## What it does

The skill runs in four phases, each producing artifacts the next phase consumes:

1. **Discover** — Extracts slides and writes a structured narrative analysis
2. **Explore** — Establishes a visual design system and maps slides to beat types (cinematic, crossfade, triptych, split, etc.)
3. **Storyboard** — Plans every beat: layout type, editorial copy, sequence, and rationale. The storyboard is a collaborative planning tool you iterate on before building.
4. **Build** — Generates production HTML from the approved storyboard using a deterministic build script

## Quick start

```bash
# Clone into your Claude Code skills directory
git clone https://github.com/lmanheim/scrollytelling-generator.git \
  ~/.claude/skills/scrollytelling-generator

# Install dependencies
cd ~/.claude/skills/scrollytelling-generator
./setup.sh
```

Then in Claude Code:

```
/scrollytelling-generator
```

Point it at a PPTX file and follow the prompts.

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- Python 3.8+
- LibreOffice (for slide image export)

The setup script handles the Python venv and `python-pptx` installation. LibreOffice needs to be installed separately:

```bash
# macOS
brew install --cask libreoffice

# Linux
sudo apt install libreoffice
```

## Project structure

```
scrollytelling-generator/
├── references/              # Design and technical guidance
├── templates/               # HTML scaffolds (copied to project before editing)
├── scripts/                 # Build and extraction scripts
├── setup.sh                 # Dependency installer
├── SKILL.md                 # Skill instructions (read by Claude)
└── README.md
```

## License

MIT
