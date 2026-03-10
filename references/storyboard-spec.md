# Storyboard specification

The storyboard is a visual planning HTML file that serves as the source of truth for beat sequence, layout choices, and editorial copy.

## BEATS data structure

The storyboard is driven by a `BEATS` array embedded as valid JSON inside a `<script type="application/json" id="beats-data">` tag. Each beat is an object with these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `section` | string | yes | Section name (e.g., "The problem", "How it works") |
| `sn` | string | yes | Section number in roman numerals (e.g., "i", "ii", "iii") |
| `type` | string | yes | Beat type key (see below) |
| `slides` | number[] | yes | Array of slide numbers used in this beat. Empty `[]` for text-only beats |
| `status` | string | yes | `"confirmed"` or `"proposed"` |
| `headline` | string | yes | Display text (HTML allowed: `<em>` for emphasis). Empty string if none |
| `body` | string | yes | Body text (HTML allowed). Newlines (`\n`) separate paragraphs. For crossfade beats, use `Caption 1:` / `Caption 2:` prefix pattern. For triptych beats, use `Panel 1:` / `Panel 2:` / `Panel 3:` prefix pattern. Empty string if none |
| `alt` | string | yes | Image alt text for accessibility. Describe what the slide shows. Empty string for text-only/dramatic/brief beats |
| `label` | string | no | Small-caps label for split-side and stacked beats (e.g., "The gap", "Stage 1"). Omit or empty string if not applicable |
| `reversed` | boolean | no | For split-side beats only: `true` for text-left/image-right layout. Defaults to `false` (image-left/text-right) |
| `rationale` | string | yes | Short editorial note explaining why this beat type was chosen for this content. Empty string for break beats |

### Beat type keys

Valid values for the `type` field: `text-only`, `dramatic`, `brief`, `slide`, `cinematic`, `crossfade`, `triptych`, `split-side`, `stacked`, `break`

See `references/beat-types.md` for editorial guidance on when to use each type.

### JSON format

Use double quotes for all keys and string values (valid JSON). Use `\\n` for newlines within strings. HTML entities like `<em>` are allowed inside string values.

### Example beat objects

These examples come from a fictional product launch presentation for the scrollytelling generator itself — 24 slides about turning presentations into scrollytelling HTML.

```json
[
  {
    "section": "The problem", "sn": "i", "type": "text-only", "slides": [], "status": "confirmed",
    "headline": "Every presentation has a <em>narrative</em>. The slide deck buries it.",
    "body": "Speaker notes hold the connective tissue — the reasoning, the transitions, the moments where meaning lands. But in a deck, they're invisible. The audience sees slides. The story lives in the presenter's head.",
    "alt": "",
    "rationale": "Opening lede establishes the core tension (narrative exists but is trapped in slide format) before showing any visuals."
  },
  {
    "section": "The problem", "sn": "i", "type": "slide", "slides": [3], "status": "confirmed",
    "headline": "", "body": "",
    "alt": "Chapter title slide reading 'What gets lost?' in large serif type on dark background",
    "rationale": "Chapter title slide — full-screen, no caption. The typography on the slide does the work."
  },
  {
    "section": "The solution", "sn": "ii", "type": "crossfade", "slides": [8, 9], "status": "proposed",
    "headline": "",
    "body": "Caption 1: A slide deck. 24 slides, linear, static. The narrative lives in speaker notes no one reads.\nCaption 2: The same content as scrollytelling. The narrative <em>is</em> the experience — woven between full-screen visuals.",
    "alt": "Before: 24-slide grid. After: scrollytelling with narrative woven between visuals",
    "rationale": "Crossfade: both slides show the same content in different formats. The shared subject stays constant while the medium transforms."
  },
  {
    "section": "How it works", "sn": "iii", "type": "triptych", "slides": [12, 15, 18], "status": "proposed",
    "headline": "",
    "body": "Panel 1: <em>Discover</em> — read the source material, map the narrative arc, identify structural patterns.\nPanel 2: <em>Storyboard</em> — plan every beat: layout type, editorial copy, pacing rhythm. A visual source of truth.\nPanel 3: <em>Build</em> — generate production HTML with scroll-driven animations, responsive layout, and cinematic transitions.",
    "alt": "Three workflow stages: Discover, Storyboard, Build",
    "rationale": "Triptych: three workflow stages are parallel concepts that benefit from side-by-side display. Staggered reveal creates left-to-right reading rhythm."
  },
  {
    "section": "How it works", "sn": "iii", "type": "split-side", "slides": [16], "status": "proposed",
    "headline": "The storyboard is the <em>source of truth</em>.",
    "body": "Every beat is a card: layout type, slide reference, editorial copy, and a rationale explaining why this layout was chosen for this content. A rhythm strip across the top shows pacing at a glance — spot monotony before it reaches the reader.",
    "alt": "Storyboard interface showing beat cards with type badges, thumbnails, and editorial copy",
    "label": "Planning",
    "rationale": "Split-side: the storyboard screenshot needs editorial narration alongside it. Side-by-side lets the reader study the UI while reading what each element means."
  },
  {
    "section": "How it works", "sn": "iii", "type": "split-side", "slides": [18], "status": "proposed",
    "headline": "From storyboard to <em>production HTML</em>.",
    "body": "The build script reads the approved storyboard and assembles production-ready HTML — scroll-driven animations, responsive layout, cinematic transitions. One command, one file.",
    "alt": "Split view: HTML code on left, rendered scrollytelling preview on right",
    "label": "Build",
    "reversed": true,
    "rationale": "Split-side reversed: code-on-right, text-on-left varies the rhythm from the previous split-side beat."
  },
  {
    "section": "The result", "sn": "iv", "type": "dramatic", "slides": [], "status": "proposed",
    "headline": "The presentation had a story all along. Now the <em>reader</em> can experience it.",
    "body": "", "alt": "",
    "rationale": "Dramatic text: the thesis restated as resolution. Gold italic, large type — this is the emotional peak before the closing."
  },
  {
    "section": "How it works", "sn": "iii", "type": "break", "slides": [], "status": "proposed",
    "headline": "", "body": "", "alt": "", "rationale": ""
  }
]
```

## Section-by-section support

Storyboards can be generated incrementally:
- Each section storyboard includes its own rhythm strip for that section
- When all sections are complete, a combined full storyboard shows the entire piece
- The BEATS array can be extended section by section without rebuilding

## Reverse-engineering from existing HTML

When an HTML build already exists, the storyboard can be created from it:
1. Read the HTML, identify each beat element by CSS class
2. Extract: beat type, slide references, editorial copy, section grouping
3. Generate BEATS array entries with status `"confirmed"` for each extracted beat
4. Render the storyboard from the reconstructed array
