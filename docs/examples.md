# Example status

## Bird treatments

All eight birds share one stylized right-facing perching pose, built once in `examples/bird-styles/render.py` and restyled. Their crown, cheek patch, and dark throat were informed by Laitche's public-domain Osaka photograph of a Eurasian tree sparrow. The perched pose and rendering are adaptations, not an anatomical identification plate.

The first three are clean colour planes (geometric), one-ink negative cuts (linocut) and opaque brush-stroke fields (gouache). The painterly example is inspired by gouache: each field has a brush-cut edge with dry-brush gaps, overlapping strokes that follow the form (around round masses, along slender ones) and a matte surface. An earlier version used blurred masks and noise and read as airbrush. It still does not simulate pigment, water or paper physics.

`extra_styles.py` adds five more: pixel art on a 150 x 126 grid with a checker dither, an ink line drawing with pressure-varied contours and hatching, a cut-paper collage with scissor facets and soft shadows, a stained-glass panel with lead lines, and a blueprint-style construction sheet. The blueprint carries no measurements, because none were taken.

During development, an unintended panel-background rectangle was removed, toe separators were added to the one-ink version, the painterly marks were revised, and the geometric beak join was cleaned up. The first pixel version filled only the left half of the frame and its beak merged with the face mask; the first stained-glass version drew lead lines for hidden parts of the wing. Not fixed: the ink wing outline is faint, the paper-cut belly shade is subtle, and the blueprint labels are small at sheet size. The first material render preceded separate layout inspection, so this example does not establish perfect adherence to the skill workflow.

All eight are authored digital studies, not physical prints, glass, paper or paint. The portable renderer uses DejaVu Serif or Pillow's fallback for labels. Earlier development used Georgia; no font files are bundled. Regenerated label pixels can therefore differ from the initial development artifacts.

## Forest meeting

The page shows an owl chairing a meeting from a stump while a fox, deer, rabbit, squirrel, hedgehog and mouse sit in a ring and listen. It is full bleed and has no text. It replaces an earlier page of six animals around a fruit basket, which is kept in the git history.

The owl, mouse, stump, log and glade are drawn in `render.py`. The fox, deer, rabbit, squirrel and hedgehog come from `cast.py`, are cut out and placed as sprites, and the deer and hedgehog are mirrored. Their construction was refined over earlier passes: a pear-shaped fox with shoulder and haunch, a deer with an S-curved neck and jointed legs, a rabbit shoulder fill, and foliage whose sprays and leaves all start on a branch point.

The grey layout was rendered and inspected before any material. It showed the fox's head overlapping the deer and the rabbit's ears covering the squirrel, so the cast was moved and scaled before the full render; a test now asserts that no two placed animals overlap. A first pass also let the frame trunks cut across the fox and squirrel, so the trunks are now drawn behind the cast. The mouse was first upscaled from a smaller drawing and looked soft; it is now drawn at final size. Ground marks avoid the placed silhouettes through a margin-grown mask.

Not fixed: the mouse's paw is a plain block on the leaf, the owl's leaf sits over its chest and not clearly in a wing, the hedgehog looks across the ring and not at the owl, the deer's gaze is downward, the fox's forepaw reaches toward nothing, and the squirrel's belly patch has a hard corner at the leg. Character proportions are cartoon conventions and were not checked against species references. All judgments are agent inspection, not a viewer study. See the [roadmap](roadmap.md).

## Evidence

The examples were developed with AI assistance as explicit Python/Pillow/NumPy drawings, not as text-to-image model benchmarks. They were visually inspected and revised. Output tests check basic file contracts and selected placement rules, not artistic excellence or audience comprehension.

The skill's behavioral case list has not been executed as an independent agent benchmark. Neither example demonstrates mastery of all poses, subjects, or styles.

No third-party photographs or fonts are embedded in this repository. Attribution links identify influences and reference provenance, not endorsement by their authors.
