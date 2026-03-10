# Quality check protocol

Run this checklist after generating each section of HTML. Present findings as two categories: "I can fix" (will fix immediately) and "need your input" (requires a decision).

## Visual hierarchy

- [ ] Text-only beats have adequate breathing room (100vh for standard, 50vh for brief)
- [ ] Display text and body text have clear typographic distinction
- [ ] Emphasis (`<em>`) is used sparingly and meaningfully
- [ ] Gold rule separators appear between logical thought groups, not everywhere

## Pacing variety

- [ ] Text beats appear between visual sequences (editorial breathing room)
- [ ] Section breaks clearly delineate structural shifts
- [ ] Brief beats are genuinely brief (one thought, no body text)

## Technical correctness

The build script's `--validate` flag covers structural checks (beat types, slide counts, alt text presence, consecutive type runs, image path resolution). Spot-check:

- [ ] Alt text is descriptive, not generic (e.g., "Dashboard overview" not "Slide 12")

## Editorial review

The build script can't verify these — this is Claude's value.

- [ ] Does the opening beat hook the reader?
- [ ] Do text beats earn their space, or could any be cut/combined?
- [ ] Do dramatic beats land as emotional peaks, not just large text?
- [ ] Are crossfade captions meaningfully different (not just restating what's visible)?
- [ ] Does the piece end with resolution, not just the last slide?

## After review

Summarize results as a brief table: category, status (pass/issues found), and notes for any issues. Then document confirmed fixes as a numbered list and track progress.
