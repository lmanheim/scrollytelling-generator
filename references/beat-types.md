# Beat types reference

Proven layout patterns for presentation-to-scrollytelling conversion. These are a starting vocabulary — extend per project as needed.

CSS and JS implementations for all beat types are in `templates/base-scaffold.html`.

## Design principles

Before choosing layout patterns, establish design intent. These principles should be in context during explore mode, before any visual decisions are made.

### Design thinking framework

Every scrollytelling project should answer these questions before layout begins:

- **Purpose:** What is this piece trying to do? Inform, persuade, move, teach?
- **Audience:** Who is reading this, and what do they already know?
- **Tone:** What voice does the piece speak in? Academic, editorial, conversational, cinematic?
- **Differentiation:** What makes this piece feel like *this* piece, not a generic scrollytelling template?

These answers shape everything downstream — typography, color, pacing, layout choices.

### Aesthetic guidelines

**Typography.** Choose typeface pairings that serve the tone. Serif display + serif body for editorial warmth. Sans display + serif body for modern authority. Avoid generic AI defaults (Inter, Roboto, system fonts) unless the project explicitly calls for them.

**Color.** Build a palette from the content, not from trends. Dark backgrounds with warm accents feel cinematic. Light backgrounds with muted tones feel editorial. High-contrast palettes create energy. Monochromatic palettes create focus. Every color should earn its place.

**Motion.** Motion should serve narrative, not decoration. Reveals draw the eye to what matters. Crossfades show transformation. Ken Burns creates immersion. Staggered delays create rhythm. If an animation doesn't support the story, remove it.

**Spatial composition.** White space (or dark space) is a design element. Generous padding around text creates reading room. Full-bleed images create immersion. Constrained max-widths create intimacy. Every spacing decision communicates priority.

---

## Layout patterns

### 1. text-only

**Structural function:** Carries narrative weight between visual beats. These screens do the heaviest editorial lifting — the "aha" moments, the synthesis, the connective tissue.

**When to use:**
- Opening lede that establishes voice and theme
- Synthesis after a series of visual beats (pulling examples into a principle)
- Narrative reveals (retroactive reframing of what the reader just experienced)
- Closing statements

---

### 2. dramatic

**Structural function:** Maximum typographic impact for a single statement. The presentation's thesis, a key turn, a one-line reveal.

**When to use:**
- Core thesis statement
- One-word or one-phrase moments ("Stop.")
- Emotional pivot points
- Bookend statements (opening/closing echo)

---

### 3. brief

**Structural function:** Short transitional pause. Creates breathing room and pacing variety between bigger beats.

**When to use:**
- Pivot between sub-topics
- Setup before a visual payoff ("But first — consider what happens when you don't.")
- Bridging statements between sections
- Anywhere a full text-only beat would feel too heavy

---

### 4. slide (full-screen)

**Structural function:** The image is the entire experience. No editorial text competes for attention.

**When to use:**
- Chapter/section title slides (typographic slides from the presentation)
- Rhetorical question slides
- Visual reveals that need no explanation
- Any slide where the typography or imagery is the point

---

### 5. cinematic

**Structural function:** Full-bleed immersive moment. The image fills every pixel. Emotional, not informational.

**When to use:**
- Stunning photography or artwork
- Emotional beats in an otherwise analytical sequence
- Dramatic visual metaphors
- Any slide where you want the reader to *feel* before they think

---

### 6. crossfade

**Structural function:** Scroll-driven transition between two near-identical slides. The shared context stays static while meaning shifts.

**When to use:**
- Slides that share the same base image but differ in one element (label, data point, annotation)
- Progressive builds (before/after, question/answer)
- Two views of the same visualization with different encodings revealed

---

### 7. triptych

**Structural function:** Three parallel examples displayed as a set on a single screen. Staggered reveal creates rhythm.

**When to use:**
- Three examples that share a structural relationship
- Parallel concepts that benefit from side-by-side comparison
- "Here are three things" moments
- Any grouped content where a gallery/carousel would be overkill

---

### 8. split-side

**Structural function:** Image and editorial text side by side. The reader can reference the visual while reading the explanation.

**When to use:**
- Diagrams or visualizations that need editorial narration
- Analytical slides where the image supports but doesn't replace the text
- Anywhere the text and image need to be consumed simultaneously
- Framework or breakdown slides (e.g., a process diagram with editorial explanation)

---

### 9. stacked

**Structural function:** Full-width image on top, editorial text below. Gives the image maximum breathing room while keeping text nearby.

**When to use:**
- Diagrams or charts that need the full width to be legible
- Sequential builds where consistent layout creates rhythm (e.g., three stacked beats in a row)
- Images where horizontal cropping would lose meaning
- Anywhere split-side would make the image too small

---

## Anti-patterns

These are patterns that consistently produce weak scrollytelling. Avoid them.

**Slide viewer.** Wrapping original slides with next/prev navigation. This is a presentation viewer, not scrollytelling. The reader should never feel like they're clicking through a deck.

**Every slide full-screen.** Using `.beat-slide` for every slide in sequence. This creates a monotonous visual rhythm with no narrative texture. Mix slide beats with text beats, crossfades, and split layouts.

**No text interstitials.** Going from slide to slide to slide without editorial breathing room. Text-only beats do the heaviest narrative lifting — they're where meaning lands. A scrollytelling piece without them is just an image gallery.

**Cookie-cutter layouts.** Applying the same beat type to every piece of content regardless of what it is. Layout choices should serve the content. A triptych works for three parallel examples; it doesn't work for three unrelated points.

**Presenter notes as UI.** Displaying speaker notes in a labeled panel ("Notes:") or tooltip. Notes should be reimagined as editorial prose woven into the narrative.

**Every beat at 100vh.** Making every section full viewport height regardless of content density. Brief text needs less space (50vh). Triptychs need enough space for three cards. Let the content determine the height.

**Generic AI aesthetics.** Inter or Roboto fonts, purple-to-blue gradients, predictable card layouts, excessive rounded corners, generic dark themes with neon accents. Every project should have a distinct visual identity derived from its content, not from default AI output patterns.
