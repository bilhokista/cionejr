# Roadmap

## Before calling the samples finished

Addressed (agent inspection at full resolution; no independent reviewer or viewer study):

- The gouache bird uses opaque brush-cut fields, form-following strokes, dry-brush edges and flat tonal layers instead of blurred masks and noise.
- The bird set now covers eight visual languages from one construction.
- The woodland page is a staged meeting with a shared event; the layout was inspected before material, and a test rejects overlapping animals.
- The cast has pear-shaped fox, S-necked deer with jointed legs, rabbit shoulder fill, and foliage anchored to branch points.

Still open:

- Character proportions are cartoon conventions, not checked against species references.
- The fox's forepaw reaches toward nothing in the meeting, the hedgehog and deer do not look at the owl, and the mouse's paw is a plain block.
- The squirrel's belly patch still has a hard corner at the leg.
- Foliage stems share one construction; broad leaves differ only in shape and spacing.
- The gouache study is not a simulation of the material; it is one opaque, brushy treatment of one pose.
- Redraw the fox and hedgehog for the meeting instead of reusing poses made for a different scene.

The lists above are a development record, not a claim that an independent reviewer has validated any item.

## Skill evaluation

All 13 cases were run once on 2026-10-05; see [the run record](../evaluations/runs/2026-10-05.md). Next: repeat each case several times, on more than one model and host, with human grading and real drawings instead of synthetic fixtures. Rerun the eleven cases that passed on v0.1.0 against v0.1.1.

Do not claim improved drawing across styles from one successful study.

## Packaging and integration

- Keep the English documentation consistent as the workflow evolves; retain evidence limits in any future translations.
- Document and test discovery on selected agent hosts.
- Choose an editor/plugin host only when there is a concrete editing workflow to integrate.
- Consider vector export after path structure and editability can be verified.

Current scope is a portable skill and Python examples. A plugin or model service is not included.
