#!/usr/bin/env python3
"""
Build script for scrollytelling-generator.

Reads the BEATS JSON from a storyboard HTML file, then assembles
production scrollytelling HTML using the base scaffold.

Usage:
    python3 build.py storyboard.html [--output output.html] [--scaffold path] [--validate]

The script:
1. Extracts the BEATS JSON from the storyboard's <script type="application/json" id="beats-data"> tag
2. For each beat, generates the correct HTML structure based on beat type
3. Wraps everything in the base scaffold (CSS, JS, progress bar, etc.)
4. Outputs a single self-contained HTML file
"""

import argparse
import json
import os
import re
import sys
from html import escape


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
DEFAULT_SCAFFOLD = os.path.join(SKILL_DIR, "templates", "base-scaffold.html")


def slide_path(n):
    return f"slides/slide-{n:03d}.jpg"


def extract_beats(storyboard_path):
    """Extract BEATS JSON from storyboard HTML."""
    with open(storyboard_path, "r", encoding="utf-8") as f:
        html = f.read()

    match = re.search(
        r'<script\s+type="application/json"\s+id="beats-data">\s*(.*?)\s*</script>',
        html,
        re.DOTALL,
    )
    if not match:
        print("Error: Could not find <script type=\"application/json\" id=\"beats-data\"> in storyboard.", file=sys.stderr)
        sys.exit(1)

    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in beats-data: {e}", file=sys.stderr)
        sys.exit(1)


def extract_design_system(storyboard_path):
    """Extract design system JSON from storyboard if present.

    Looks for <script type="application/json" id="design-system"> in the
    storyboard HTML. Expected JSON format:
    {
        "fonts_link": "<link href='https://fonts.googleapis.com/...' rel='stylesheet'>",
        "css_vars": {
            "--bg": "#1a1a1a",
            "--text": "#f0e6d3",
            ...
        }
    }

    Returns the parsed dict, or None if not found.
    """
    with open(storyboard_path, "r", encoding="utf-8") as f:
        html = f.read()

    match = re.search(
        r'<script\s+type="application/json"\s+id="design-system">\s*(.*?)\s*</script>',
        html,
        re.DOTALL,
    )
    if not match:
        return None

    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        print("Warning: Found design-system block but JSON is invalid. Using scaffold defaults.", file=sys.stderr)
        return None


def apply_design_system(scaffold, design_system):
    """Inject design system tokens into the scaffold HTML.

    Replaces the Google Fonts <link> and :root CSS variables.
    """
    # Replace fonts link
    fonts_link = design_system.get("fonts_link", "")
    if fonts_link:
        scaffold = re.sub(
            r'<link[^>]*fonts\.googleapis\.com[^>]*>',
            fonts_link,
            scaffold,
        )

    # Replace CSS variables in :root
    css_vars = design_system.get("css_vars", {})
    if css_vars:
        for var_name, var_value in css_vars.items():
            # Match the variable declaration in :root, e.g. --bg: #111;
            pattern = re.escape(var_name) + r'\s*:\s*[^;]+;'
            replacement = f'{var_name}: {var_value};'
            scaffold = re.sub(pattern, replacement, scaffold)

    return scaffold


def parse_body_paragraphs(body):
    """Split body text on newlines into paragraph list."""
    if not body:
        return []
    return [p.strip() for p in body.split("\n") if p.strip()]


def parse_captions(body):
    """Parse 'Caption 1: ...' / 'Caption 2: ...' from body text."""
    paragraphs = parse_body_paragraphs(body)
    cap1, cap2 = "", ""
    for p in paragraphs:
        if p.startswith("Caption 1:"):
            cap1 = p[len("Caption 1:"):].strip()
        elif p.startswith("Caption 2:"):
            cap2 = p[len("Caption 2:"):].strip()
    return cap1, cap2


def parse_panels(body):
    """Parse 'Panel 1: ...' / 'Panel 2: ...' / 'Panel 3: ...' from body text."""
    paragraphs = parse_body_paragraphs(body)
    panels = []
    for p in paragraphs:
        for i in range(1, 4):
            prefix = f"Panel {i}:"
            if p.startswith(prefix):
                panels.append(p[len(prefix):].strip())
    return panels


# ── Beat builders ──
# Each function generates the HTML for one beat type.
# Output shapes shown in comments; conditional elements noted with (?).


# Output: .beat-text > .beat-text-inner > .reveal[.display-text] + .reveal.reveal-dN[.body-text](*)
def build_text_only(beat):
    headline = beat.get("headline", "")
    paragraphs = parse_body_paragraphs(beat.get("body", ""))
    section = beat.get("section", "")

    inner = ""
    if headline:
        inner += f'    <div class="reveal">\n      <p class="display-text">{headline}</p>\n    </div>\n'

    for i, p in enumerate(paragraphs):
        delay = f" reveal-d{i + 1}" if i < 3 else f" reveal-d3"
        inner += f'    <div class="reveal{delay}">\n      <p class="body-text">{p}</p>\n    </div>\n'

    # Add gold rule between headline and body if both exist
    if headline and paragraphs:
        # Insert gold rule after first body paragraph
        parts = inner.split('<div class="reveal reveal-d1">')
        if len(parts) == 2:
            inner = parts[0] + '<div class="reveal reveal-d1">' + parts[1]

    return (
        f'<div class="beat-text" data-section="{section}">\n'
        f'  <div class="beat-text-inner">\n'
        f'{inner}'
        f'  </div>\n'
        f'</div>\n'
    )


# Output: .beat-text.dramatic > .beat-text-inner > .reveal[.display-text]
def build_dramatic(beat):
    headline = beat.get("headline", "")
    section = beat.get("section", "")

    return (
        f'<div class="beat-text dramatic" data-section="{section}">\n'
        f'  <div class="beat-text-inner">\n'
        f'    <div class="reveal">\n'
        f'      <p class="display-text">{headline}</p>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</div>\n'
    )


# Output: .beat-text.brief > .beat-text-inner > .reveal[.display-text]
def build_brief(beat):
    headline = beat.get("headline", "")
    section = beat.get("section", "")

    return (
        f'<div class="beat-text brief" data-section="{section}">\n'
        f'  <div class="beat-text-inner">\n'
        f'    <div class="reveal">\n'
        f'      <p class="display-text">{headline}</p>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</div>\n'
    )


# Output: .beat-slide > img + .slide-caption(?) > p(*)
def build_slide(beat):
    slides = beat.get("slides", [])
    section = beat.get("section", "")
    alt_text = beat.get("alt", f"Slide {slides[0]}" if slides else "")
    body = beat.get("body", "")

    img = slide_path(slides[0]) if slides else ""

    html = f'<div class="beat-slide" data-section="{section}">\n'
    html += f'  <img src="{img}" alt="{alt_text}" loading="lazy">\n'

    if body:
        paragraphs = parse_body_paragraphs(body)
        if paragraphs:
            html += f'  <div class="slide-caption">\n'
            for p in paragraphs:
                html += f'    <p>{p}</p>\n'
            html += f'  </div>\n'

    html += f'</div>\n'
    return html


# Output: .beat-slide.cinematic > img + .slide-caption(?) > p(*)
def build_cinematic(beat):
    slides = beat.get("slides", [])
    section = beat.get("section", "")
    alt_text = beat.get("alt", f"Slide {slides[0]}" if slides else "")
    body = beat.get("body", "")

    img = slide_path(slides[0]) if slides else ""

    html = f'<div class="beat-slide cinematic" data-section="{section}">\n'
    html += f'  <img src="{img}" alt="{alt_text}" loading="lazy">\n'

    if body:
        paragraphs = parse_body_paragraphs(body)
        if paragraphs:
            html += f'  <div class="slide-caption">\n'
            for p in paragraphs:
                html += f'    <p>{p}</p>\n'
            html += f'  </div>\n'

    html += f'</div>\n'
    return html


# Output: .beat-crossfade > .crossfade-sticky > img.crossfade-from + img.crossfade-to
#         + .crossfade-caption-bg + .crossfade-caption.crossfade-caption-from(?) + ...to(?)
def build_crossfade(beat):
    slides = beat.get("slides", [])
    section = beat.get("section", "")
    alt_text = beat.get("alt", "")
    body = beat.get("body", "")

    img_from = slide_path(slides[0]) if len(slides) > 0 else ""
    img_to = slide_path(slides[1]) if len(slides) > 1 else ""

    cap1, cap2 = parse_captions(body)

    # Split alt text on ". " for from/to if possible
    alt_parts = alt_text.split(". ") if ". " in alt_text else [alt_text, alt_text]
    alt_from = alt_parts[0]
    alt_to = alt_parts[1] if len(alt_parts) > 1 else alt_parts[0]

    html = f'<div class="beat-crossfade" data-section="{section}">\n'
    html += f'  <div class="crossfade-sticky">\n'
    html += f'    <img class="crossfade-from" src="{img_from}" alt="{alt_from}" loading="lazy">\n'
    html += f'    <img class="crossfade-to" src="{img_to}" alt="{alt_to}" loading="lazy">\n'
    html += f'    <div class="crossfade-caption-bg"></div>\n'

    if cap1:
        html += f'    <div class="crossfade-caption crossfade-caption-from">\n'
        html += f'      <p>{cap1}</p>\n'
        html += f'    </div>\n'

    if cap2:
        html += f'    <div class="crossfade-caption crossfade-caption-to">\n'
        html += f'      <p>{cap2}</p>\n'
        html += f'    </div>\n'

    html += f'  </div>\n'
    html += f'</div>\n'
    return html


# Output: .beat-triptych > .triptych-inner > .triptych-label(?) + .triptych-grid
#         > .triptych-card.reveal.reveal-dN[img + .triptych-desc(?)] x3
def build_triptych(beat):
    slides = beat.get("slides", [])
    section = beat.get("section", "")
    alt_text = beat.get("alt", "")
    label = beat.get("label", "")
    body = beat.get("body", "")

    panels = parse_panels(body)

    html = f'<div class="beat-triptych" data-section="{section}">\n'
    html += f'  <div class="triptych-inner">\n'

    if label:
        html += f'    <div class="triptych-label reveal">{label}</div>\n'

    html += f'    <div class="triptych-grid">\n'

    for i in range(3):
        delay = f"reveal-d{i + 1}"
        img = slide_path(slides[i]) if i < len(slides) else ""
        panel_alt = f"Panel {i + 1}" if not alt_text else alt_text
        panel_text = panels[i] if i < len(panels) else ""

        html += f'      <div class="triptych-card reveal {delay}">\n'
        html += f'        <div class="triptych-image">\n'
        html += f'          <img src="{img}" alt="{panel_alt}" loading="lazy">\n'
        html += f'        </div>\n'
        if panel_text:
            html += f'        <p class="triptych-desc">{panel_text}</p>\n'
        html += f'      </div>\n'

    html += f'    </div>\n'
    html += f'  </div>\n'
    html += f'</div>\n'
    return html


# Output: .beat-split-side(.reversed?) > .split-image[img] + .split-text
#         > .split-label(?) + .split-headline(?) + .split-body(*)
def build_split_side(beat):
    slides = beat.get("slides", [])
    section = beat.get("section", "")
    alt_text = beat.get("alt", f"Slide {slides[0]}" if slides else "")
    headline = beat.get("headline", "")
    label = beat.get("label", "")
    body = beat.get("body", "")
    reversed_layout = beat.get("reversed", False)

    img = slide_path(slides[0]) if slides else ""
    cls = "beat-split-side reversed" if reversed_layout else "beat-split-side"

    html = f'<div class="{cls}" data-section="{section}">\n'
    html += f'  <div class="split-image">\n'
    html += f'    <img src="{img}" alt="{alt_text}" loading="lazy">\n'
    html += f'  </div>\n'
    html += f'  <div class="split-text">\n'

    if label:
        html += f'    <div class="split-label">{label}</div>\n'
    if headline:
        html += f'    <div class="split-headline">{headline}</div>\n'

    paragraphs = parse_body_paragraphs(body)
    for p in paragraphs:
        html += f'    <p class="split-body">{p}</p>\n'

    html += f'  </div>\n'
    html += f'</div>\n'
    return html


# Output: .beat-stacked > .split-image[img] + .split-text
#         > .split-label(?) + .split-headline(?) + .split-body(*)
def build_stacked(beat):
    slides = beat.get("slides", [])
    section = beat.get("section", "")
    alt_text = beat.get("alt", f"Slide {slides[0]}" if slides else "")
    headline = beat.get("headline", "")
    label = beat.get("label", "")
    body = beat.get("body", "")

    img = slide_path(slides[0]) if slides else ""

    html = f'<div class="beat-stacked" data-section="{section}">\n'
    html += f'  <div class="split-image">\n'
    html += f'    <img src="{img}" alt="{alt_text}" loading="lazy">\n'
    html += f'  </div>\n'
    html += f'  <div class="split-text">\n'

    if label:
        html += f'    <div class="split-label">{label}</div>\n'
    if headline:
        html += f'    <div class="split-headline">{headline}</div>\n'

    paragraphs = parse_body_paragraphs(body)
    for p in paragraphs:
        html += f'    <p class="split-body">{p}</p>\n'

    html += f'  </div>\n'
    html += f'</div>\n'
    return html


# Output: .section-break > .section-break-inner > .section-break-line + .section-break-num + .section-break-line
def build_section_break(beat):
    sn = beat.get("sn", "").upper()
    return (
        f'<div class="section-break">\n'
        f'  <div class="section-break-inner">\n'
        f'    <div class="section-break-line"></div>\n'
        f'    <div class="section-break-num">{sn}</div>\n'
        f'    <div class="section-break-line"></div>\n'
        f'  </div>\n'
        f'</div>\n'
    )


# ── Beat type dispatch ──

BUILDERS = {
    "text-only": build_text_only,
    "dramatic": build_dramatic,
    "brief": build_brief,
    "slide": build_slide,
    "cinematic": build_cinematic,
    "crossfade": build_crossfade,
    "triptych": build_triptych,
    "split-side": build_split_side,
    "stacked": build_stacked,
    "break": build_section_break,
}


VALID_BEAT_TYPES = set(BUILDERS.keys())


def validate_beats(beats, base_dir=None):
    """Validate BEATS array structure. Returns list of error/warning strings.

    If base_dir is provided, also checks that slide image files exist on disk.
    """
    issues = []

    for i, beat in enumerate(beats):
        beat_id = beat.get("headline", beat.get("type", f"beat {i}"))
        beat_type = beat.get("type", "")

        if not beat_type:
            issues.append(f"ERROR: Beat {i} ({beat_id}) has no 'type' field")
        elif beat_type not in VALID_BEAT_TYPES:
            issues.append(f"ERROR: Beat {i} ({beat_id}) has unknown type '{beat_type}'")

        if not beat.get("section"):
            issues.append(f"WARNING: Beat {i} ({beat_id}) has no 'section' field")

        image_types = {"slide", "cinematic", "crossfade", "triptych", "split-side", "stacked"}
        if beat_type in image_types:
            slides = beat.get("slides", [])
            if not slides:
                issues.append(f"ERROR: Beat {i} ({beat_id}) type '{beat_type}' requires slides but has none")
            elif beat_type == "crossfade" and len(slides) < 2:
                issues.append(f"ERROR: Beat {i} ({beat_id}) type 'crossfade' needs 2 slides, has {len(slides)}")
            elif beat_type == "triptych" and len(slides) < 3:
                issues.append(f"WARNING: Beat {i} ({beat_id}) type 'triptych' expects 3 slides, has {len(slides)}")

            if base_dir and slides:
                for s in slides:
                    img_path = os.path.join(base_dir, slide_path(s))
                    if not os.path.exists(img_path):
                        issues.append(f"ERROR: Beat {i} ({beat_id}) references slide {s} but {slide_path(s)} not found")

        if beat_type in image_types and not beat.get("alt"):
            issues.append(f"WARNING: Beat {i} ({beat_id}) has no alt text")

        status = beat.get("status", "")
        if status == "proposed" and beat_type != "break":
            issues.append(f"WARNING: Beat {i} ({beat_id}) is still 'proposed'")

    for i in range(2, len(beats)):
        t0 = beats[i-2].get("type", "")
        t1 = beats[i-1].get("type", "")
        t2 = beats[i].get("type", "")
        if t0 == t1 == t2 and t0 not in ("text-only", "break"):
            issues.append(f"WARNING: 3 consecutive '{t0}' beats at positions {i-2}-{i}")

    return issues


def build_beat(beat):
    beat_type = beat.get("type", "")
    builder = BUILDERS.get(beat_type)
    if not builder:
        print(f"Warning: Unknown beat type '{beat_type}', skipping.", file=sys.stderr)
        return f"<!-- Unknown beat type: {beat_type} -->\n"
    return builder(beat)


def assemble(beats, scaffold_path):
    """Assemble all beats into the scaffold."""
    with open(scaffold_path, "r", encoding="utf-8") as f:
        scaffold = f.read()

    # Build all beat HTML
    content_lines = []
    for beat in beats:
        if beat.get("status") == "proposed":
            print(f"Warning: Beat '{beat.get('headline', beat.get('type'))}' is still 'proposed', not 'confirmed'.", file=sys.stderr)
        content_lines.append(build_beat(beat))

    content_html = "\n".join(content_lines)

    # Find the content insertion point in the scaffold
    # The scaffold has a comment block: <!-- ═══ BEAT CONTENT GOES HERE ... ═══ -->
    pattern = r'<!-- ═+\s*\n\s*BEAT CONTENT GOES HERE.*?═+ -->'
    match = re.search(pattern, scaffold, re.DOTALL)

    if match:
        scaffold = scaffold[:match.start()] + content_html + scaffold[match.end():]
    else:
        # Fallback: insert before </body>
        scaffold = scaffold.replace("</body>", content_html + "\n</body>")

    return scaffold


def main():
    parser = argparse.ArgumentParser(description="Build scrollytelling HTML from a storyboard.")
    parser.add_argument("storyboard", help="Path to storyboard HTML file")
    parser.add_argument("--output", "-o", default=None, help="Output HTML file path (default: scrollytelling.html)")
    parser.add_argument("--scaffold", default=None, help="Path to custom scaffold HTML (default: built-in base scaffold)")
    parser.add_argument("--validate", action="store_true", help="Validate storyboard beats without building")
    args = parser.parse_args()

    # Extract beats
    beats = extract_beats(args.storyboard)
    print(f"Found {len(beats)} beats in storyboard.", file=sys.stderr)

    # Validate-only mode
    if args.validate:
        storyboard_dir = os.path.dirname(os.path.abspath(args.storyboard))
        issues = validate_beats(beats, base_dir=storyboard_dir)
        if issues:
            for issue in issues:
                print(issue, file=sys.stderr)
            errors = [i for i in issues if i.startswith("ERROR")]
            warnings = [i for i in issues if i.startswith("WARNING")]
            print(f"\nValidation: {len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
            sys.exit(1 if errors else 0)
        else:
            print("Validation passed: no issues found.", file=sys.stderr)
            sys.exit(0)

    if not args.output:
        storyboard_dir = os.path.dirname(os.path.abspath(args.storyboard))
        args.output = os.path.join(storyboard_dir, "scrollytelling.html")

    # Count stats
    confirmed = sum(1 for b in beats if b.get("status") == "confirmed")
    proposed = sum(1 for b in beats if b.get("status") == "proposed" and b.get("type") != "break")
    if proposed > 0:
        print(f"Warning: {proposed} beats are still 'proposed'. Consider confirming all beats before building.", file=sys.stderr)

    # Determine scaffold path
    scaffold_path = args.scaffold if args.scaffold else DEFAULT_SCAFFOLD

    # Extract design system from storyboard and apply to scaffold (only when using default scaffold)
    if not args.scaffold:
        design_system = extract_design_system(args.storyboard)
        if design_system:
            print("Found design system in storyboard, applying to scaffold.", file=sys.stderr)
            with open(scaffold_path, "r", encoding="utf-8") as f:
                scaffold_html = f.read()
            scaffold_html = apply_design_system(scaffold_html, design_system)
            # Write to a temp scaffold so assemble() can read it
            temp_scaffold = os.path.join(
                os.path.dirname(os.path.abspath(args.output)),
                ".build-scaffold-tmp.html",
            )
            with open(temp_scaffold, "w", encoding="utf-8") as f:
                f.write(scaffold_html)
            scaffold_path = temp_scaffold

    # Assemble
    result = assemble(beats, scaffold_path)

    # Clean up temp scaffold if created
    temp_scaffold_path = os.path.join(
        os.path.dirname(os.path.abspath(args.output)),
        ".build-scaffold-tmp.html",
    )
    if os.path.exists(temp_scaffold_path):
        os.remove(temp_scaffold_path)

    # Write output
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Built {args.output} ({len(beats)} beats, {confirmed} confirmed)", file=sys.stderr)


if __name__ == "__main__":
    main()
