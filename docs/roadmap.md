# Roadmap

## Before calling the samples finished

Addressed (agent inspection at full resolution; no independent reviewer or viewer study):

- Seven of the eight bird styles and the whole woodland page are SVG masters, with named parts and PNGs rendered from them.
- The woodland page is a staged meeting with a shared event and a cast drawn for it; the layout was inspected in greys before colour, and tests reject overlapping characters and characters that do not face the owl.
- The gouache bird uses opaque brush-cut fields, form-following strokes and dry-brush edges instead of blurred masks and noise.

Still open:

- Character proportions are cartoon conventions, not checked against species references.
- The hedgehog quills are mechanical, the deer's hind legs are stiff, the mouse reads as a ring, and the squirrel tail is nearly a spiral.
- Foliage stems share one construction; broad leaves differ only in shape and spacing.
- The gouache study is raster only and is not a simulation of the material.
- Text in SVG (blueprint labels) depends on installed fonts; outlining it would make the PNG identical everywhere.
- Add a grain or paper layer to the woodland SVG only if it can stay a filter, so the shapes remain clean.

The lists above are a development record, not a claim that an independent reviewer has validated any item.

## Skill evaluation

All 13 cases were run once on 2026-10-05; see [the run record](../evaluations/runs/2026-10-05.md). Next: repeat each case several times, on more than one model and host, with human grading and real drawings instead of synthetic fixtures. Rerun the eleven cases that passed on v0.1.0 against v0.1.1.

Do not claim improved drawing across styles from one successful study.

## Packaging and integration

- Keep the English documentation consistent as the workflow evolves; retain evidence limits in any future translations.
- Document and test discovery on selected agent hosts.
- Choose an editor/plugin host only when there is a concrete editing workflow to integrate.
- SVG export now exists for seven bird styles and the woodland page; check a round trip through a vector editor before calling it editable in practice.

Current scope is a portable skill and Python examples. A plugin or model service is not included.
