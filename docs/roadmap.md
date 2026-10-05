# Roadmap

## Before calling the samples finished

Addressed (agent inspection at full resolution; no independent reviewer or viewer study):

- Ground marks avoid animal and prop silhouettes through a margin-grown mask instead of coarse rectangles.
- The fox's apple rests on the stump top beside its paw, with a contact shadow on the wood.
- The fox has a pear-shaped body with a shoulder, haunch and neck ruff instead of a capsule; the rabbit has a shoulder fill under the head.
- The deer has an S-curved neck that flows into the chest and back, a lowered head and gaze toward the basket, and jointed legs with a hock bend.
- Every foliage spray and large leaf now starts on a branch point; fronds and alternating broad leaves vary in colour per leaf.
- The gouache bird uses opaque brush-cut fields, form-following strokes, dry-brush edges and flat tonal layers instead of blurred masks and noise.

Still open:

- Character proportions are cartoon conventions, not checked against species references.
- The squirrel's belly patch still has a hard corner at the leg.
- Foliage stems share one construction; broad leaves differ only in shape and spacing.
- The gouache study is not a simulation of the material; it is one opaque, brushy treatment of one pose.

The forest page received a provisional response that it was acceptable but still needed cleanup. The lists above are a development record, not a claim that an independent reviewer has validated any item.

## Skill evaluation

All 13 cases were run once on 2026-10-05; see [the run record](../evaluations/runs/2026-10-05.md). Next: repeat each case several times, on more than one model and host, with human grading and real drawings instead of synthetic fixtures. Rerun the eleven cases that passed on v0.1.0 against v0.1.1.

Do not claim improved drawing across styles from one successful study.

## Packaging and integration

- Keep the English documentation consistent as the workflow evolves; retain evidence limits in any future translations.
- Document and test discovery on selected agent hosts.
- Choose an editor/plugin host only when there is a concrete editing workflow to integrate.
- Consider vector export after path structure and editability can be verified.

Current scope is a portable skill and Python examples. A plugin or model service is not included.
