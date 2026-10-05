# Example status

## Bird treatments

The three birds share a stylized right-facing perching pose. Their crown, cheek patch, and dark throat were informed by Laitche's public-domain Osaka photograph of a Eurasian tree sparrow. The perched pose and rendering are adaptations, not an anatomical identification plate.

The treatments use clean colour planes, one-ink negative cuts, and opaque brush-stroke fields. They are authored digital studies, not physical linocut prints or paintings. The painterly example is inspired by gouache: each field has a brush-cut edge with dry-brush gaps, overlapping strokes that follow the form (around round masses, along slender ones) and a matte surface. An earlier version used blurred masks and noise and read as airbrush. It still does not simulate pigment, water or paper physics.

During development, an unintended panel-background rectangle was removed, toe separators were added to the one-ink version, the painterly marks were revised, and the geometric beak join was cleaned up. The first material render preceded separate layout inspection, so this example does not establish perfect adherence to the skill workflow.

The portable renderer uses DejaVu Serif or Pillow's fallback for labels. Earlier development used Georgia; no font files are bundled. Regenerated label pixels can therefore differ from the initial development artifacts.

## More bird styles

`examples/more-styles/` reuses the bird's construction and changes only the visual language: pixel art on a 150 x 126 grid with a checker dither, an ink line drawing with pressure-varied contours and hatching, a cut-paper collage with scissor facets and soft shadows, a stained-glass panel with lead lines, and a blueprint-style construction sheet.

Issues found during inspection and fixed: the first pixel version filled only the left half of the frame and its beak merged with the face mask; the first stained-glass version drew lead lines for hidden parts of the wing. Not fixed: the ink wing outline is faint, the paper-cut belly shade is subtle, and the blueprint labels are small at sheet size. The blueprint carries no measurements, because none were taken. All five are agent-inspected digital studies, not physical media.

## Forest gathering

The page contains six fictional woodland characters around a basket on a stump. It is full bleed and has no text. The layout was opened before the full scene was implemented. The squirrel/perch was moved to avoid a rabbit-ear tangency.

Later inspections found grass marks on animals and on the stump, overlong sparrow legs, and a fox paw partly hidden by the tabletop. These were revised.

A second pass replaced the protected rectangles with a shape-aware mask (animal and prop silhouettes grown by a 12 px margin). The tests cover representative points inside the old rectangles, just outside contours, and on ears, paws and the stump rim; they do not cover every possible composition. The same pass moved the fox's apple onto the stump top, lowered the deer's gaze to the basket, and mixed broad leaves into the frond-only foliage. These changes were inspected by the agent at full resolution; no independent reviewer has assessed them.

The page remains a work in progress. It still needs refinement in character proportions and contours and in how foliage joins the branches. See the [roadmap](roadmap.md).

## Evidence

The examples were developed with AI assistance as explicit Python/Pillow/NumPy drawings, not as text-to-image model benchmarks. They were visually inspected and revised. Output tests check basic file contracts and selected placement rules, not artistic excellence or audience comprehension.

The skill's behavioral case list has not been executed as an independent agent benchmark. Neither example demonstrates mastery of all poses, subjects, or styles.

No third-party photographs or fonts are embedded in this repository. Attribution links identify influences and reference provenance, not endorsement by their authors.
