# Example status

## Bird treatments

All eight birds share one stylized right-facing perching pose, built once in `examples/bird-styles/render.py` and restyled. Their crown, cheek patch, and dark throat were informed by Laitche's public-domain Osaka photograph of a Eurasian tree sparrow. The perched pose and rendering are adaptations, not an anatomical identification plate.

Seven styles are written as SVG in `vector_styles.py` and saved in `svg/`: geometric colour planes, a linocut-style one-ink print with carved paper-white cuts, pixel art, ink line, cut paper, stained glass and a blueprint-style construction sheet. The shapes are the same cubic curves the construction uses, so they stay curves in the SVG, and the main parts carry ids (`body`, `wing`, `crown`, `bib` and so on). Each PNG is rendered from its SVG with resvg. The eighth, gouache, is raster only: it is opaque brush-stroke fields with dry-brush edges and form-following strokes, and it does not survive as clean vector shapes.

What changed when the styles became vector, compared with the earlier raster versions:

- Pixel art is exact: one `rect` per run of same-coloured pixels on a 150 x 126 grid, with a checker dither on the belly shade.
- Ink line draws each contour as a filled variable-width outline, and hatching is clipped to its shape.
- Cut paper gets its shadows and paper grain from SVG filters (blur, offset, turbulence). Renderers that ignore filters will show flat paper; the fibres of the raster version are gone.
- Stained glass uses computed Voronoi panes for the background and per-piece gradients, without the mottling of the raster version.
- Linocut lost the random print speckles; the carved cuts are unchanged.
- The blueprint labels are live SVG text, so the PNG uses whichever sans-serif font the machine has.

The gouache study is inspired by gouache; it does not simulate pigment, water or paper physics. An earlier version used blurred masks and noise and read as airbrush.

During development, an unintended panel-background rectangle was removed, toe separators were added to the linocut, and the geometric beak join was cleaned up. The first pixel version filled only the left half of the frame and its beak merged with the face mask; the first stained-glass version drew lead lines for hidden parts of the wing. Not fixed: the ink wing outline is faint, the paper-cut belly shade is subtle, and the blueprint labels are small at sheet size. The blueprint carries no measurements, because none were taken. The first raster render preceded separate layout inspection, so this example does not establish perfect adherence to the skill workflow.

All eight are authored digital studies, not physical prints, glass, paper or paint. The sheet labels use DejaVu Serif or Pillow's fallback; no font files are bundled.

## Forest meeting

The page shows an owl chairing a meeting from a stump while a fox, deer, rabbit, squirrel, hedgehog and mouse sit in a ring and listen. It is full bleed and has no text. It replaces two earlier woodland pages, which stay in the git history.

Everything is drawn as vector shapes in `characters.py` and `render.py` and saved as `forest-meeting.svg`; the PNGs are rendered from it. Each character is a named group with a `translate` and `scale` transform, mirrored where needed so it faces the owl, so any of them can be moved or deleted in a vector editor. The characters were redrawn for this scene rather than reused: the fox is seated with its head tipped up and a white-tipped tail, the deer stands with its neck raised, the rabbit sits up with one paw raised to ask a question, the squirrel holds an acorn on the log, the hedgehog lifts its snout, the mouse takes notes on a leaf, and the owl holds up a leaf page.

The earlier `composition.png` was the finished SVG rendered in greys. That was a value study, not a coarse construction layout. The prior development record reported inspection before colour decisions and placement corrections; this does not establish that a separate mass layout was inspected before detail.

In v0.1.2, `composition.png` and `layout.svg` come from a separate mass builder without faces or material marks. `render.py --layout` writes only those files, preserving finished art. The finished scene in greys is now `value-study.png`. The mass layout was opened before this contact-repair pass, not before the original artwork was made.

Two contacts were repaired: a tapered neck connects the squirrel's head to its body, and the owl's grip now overlaps both the leaf and its raised wing. Tests check these narrow relationships in rasterized SVG masks. Existing placement tests check character separation, page bounds, owl height/horizontal alignment, and horizontal facing. They do not prove convincing support or attention toward the speaker. See the [repair review](../examples/forest-meeting/review.md).

Not fixed: the hedgehog's quills are a generated zigzag and read mechanical up close, the deer's hind legs are stiff, the mouse's body and belly read as a ring, the squirrel's tail is tall and nearly a spiral, and the grass keeps off the cast through simple boxes. Character proportions are cartoon conventions, not checked against species references. The two repaired contacts do not settle those remaining defects. All judgments are agent inspection, not a viewer study. See the [roadmap](roadmap.md).

## Evidence

The examples were developed with AI assistance as explicit Python/Pillow/NumPy drawings, not as text-to-image model benchmarks. They were visually inspected and revised. Output tests check basic file contracts and selected placement rules, not artistic excellence or audience comprehension.

The skill's behavioral case list has not been executed as an independent agent benchmark. Neither example demonstrates mastery of all poses, subjects, or styles.

No third-party photographs or fonts are embedded in this repository. Attribution links identify influences and reference provenance, not endorsement by their authors.
