---
name: cionejr
description: >-
  Construct and critique drawings, illustrations, characters, and graphic compositions from basic shapes across scales. Use for reference drawing, sketching, geometric illustration, feather and material detail, storybook scenes, visual storytelling, style translation, and contextual taste decisions. Require style-specific craft checks before comparing alternatives.
license: MIT
metadata:
  version: "0.1.2"
  status: "earliest-alpha"
  language: "en"
---

# cionejr

Build illustrations from basic shapes, then check their structure and meaning. Use circles, squares, and triangles to understand a subject, not as compulsory final contours. Execute every proposed style properly before comparing alternatives.

This is the earliest alpha of the skill. Its workflow has not yet been independently evaluated. It does not guarantee drawing competence, perfect results, or improved model output. A completed checklist alone cannot establish artistic quality.

The documentation is in English. Respond in the language requested by the user and preserve any approved copy exactly.

## Identify the requested task

- For research, critique, or skill development, do that work. Do not automatically make an image.
- For drawing or revision, follow the workflow below.
- For style comparison, check each candidate's craft first.
- For teaching, use the exercises in the construction guide. Address one weakness before increasing difficulty.
- For plugins, separate methodology from implementation. Establish the host and editing workflow before building an integration.

Resolve bundled paths from this skill directory. Do not assume internet access, a graphics editor, or an image model is available.

## Supporting documents

| Task | Read before working |
|---|---|
| Drawing or explaining construction | [construction.md](references/construction.md) |
| Reviewing or repairing a result | [craft-review.md](references/craft-review.md) |
| Style, character, composition, or taste | [communication-and-style.md](references/communication-and-style.md) |
| Full scenes, multiple characters, or storybook pages | [scene-staging.md](references/scene-staging.md) |
| Pasted-on parts, floating props, or uncertain contacts | [attachment-and-occlusion.md](references/attachment-and-occlusion.md) |
| Citing methods or extending research | [sources-and-limits.md](references/sources-and-limits.md) |
| Recording briefs and critique | [worksheet.md](templates/worksheet.md) |
| Evaluating skill behavior | [cases.md](evaluations/cases.md) |

For a complete illustration, read construction, craft review, and communication. Read scene staging for full scenes. For a narrow critique, read craft review and the relevant sections. Do not load every research source unnecessarily.

## Rules that cannot be skipped

1. Establish subject identity, action, and viewing context before detail. A generic bird is valid when requested; do not claim species accuracy without references.
2. Separate flat-shape construction from volumetric construction. Perspective and joins must suit the chosen approach.
3. Repair a defect at the scale where it occurs. Extra feathers cannot fix an incorrectly attached head.
4. Judge distortion against intent and style. Abstraction is not automatically an error, but "stylized" cannot excuse every defect.
5. Inspect the rendered result. Code, prompts, and descriptions cannot establish the image's quality.
6. Every candidate must pass its own relevant craft checks before a taste comparison. Mark an unfinished candidate for revision rather than declaring its style inferior.
7. Separate file checks, agent visual judgments, and real viewer responses. One kind of evidence cannot replace another.
8. Preserve previous versions and unresolved defects. Do not rewrite earlier critique as proof of success.
9. A known structural defect (a join, attachment, support or identity fault) blocks the detail the user asked for, even when the request says "only add X". Repair the smallest construction change that removes the defect first and say so, or stop and report that detail is blocked. Never layer detail over a defect you have named.
10. Without accessible references, do not draw identification plates, "X versus Y" callouts, or field-mark claims from memory. Ask whether a labeled generic study is acceptable before drawing, and keep any such study free of diagnostic marks.

## Workflow

### 1. Establish a sufficient brief

Record the subject and purpose. State what must be understood, by whom, at what size or in which medium. Choose an observational, fictional-character, geometric, or decorative approach. State whether the requested output is a rough study or a finished asset.

Use context already supplied. Ask at most two questions that would materially change the work. For missing details, state reversible assumptions. Do not invent species identity or market evidence. A personal learning goal does not require commercial validation.

### 2. Observe references and measure relationships

Choose references that support the pose and identifying features. Record provenance and reproduction rights. Separate the primary pose reference from detail references and style inspiration.

Record checkable relationships: mass ratios, feature placement relative to contours, joint directions, and support. Define invariants for fictional subjects. Do not mix incompatible species anatomy without a deliberate decision.

If references are inaccessible, state the limit and ask, in one short question, whether a labeled generic study is acceptable. Do not draw until that is settled unless the user already said so. A generic study may not carry diagnostic field marks, comparison callouts, or a test that tells species apart; those are unverifiable accuracy claims.

### 3. Construct masses and action

Start with the action direction or dominant arrangement. Place the main masses and their connecting parts. Use operations on basic shapes and simple volumes where needed.

Check silhouettes, negative space, relative size, and contact with the environment. For multiple characters, open the mass layout and inspect interactions and depth before material. Use coarse envelopes and support planes without finishing detail. Desaturating a finished image is a value study, not a construction-stage layout. Record the actual inspection. Construction lines may be rough; a neat outline must not conceal a faulty join.

### 4. Review structure before detail

Apply the structural checks in the craft guide. For attachment or prop faults, use the attachment and occlusion guide to trace each required relationship and its layer order. Verify both ends of a repair, then recheck at reading size; proximity alone does not establish contact. Record evidence and status: `ready for this stage`, `revise`, or `not yet assessed`.

If a relevant identity, action, perspective, or connection defect remains, return to construction. This applies when the user asked only for detail: a request for feathers, texture, or polish does not authorize leaving a pasted-on head or an unsupported limb in place (rule 9). For intentional deviations, state the deformation rule and inspect whether the result stays consistent and readable.

### 5. Develop parts and materials

Construct components according to their function and overlap. Add the required local detail. Coverts and flight feathers need different structures; texture should follow the surface rather than fill empty space.

Set the detail budget from purpose and final size. Full detail is valid after structure is sound. Raster pixels are colour samples, not tiny geometric objects; pixel art may deliberately use grid-based clusters as its visual language.

### 6. Render, inspect, and revise

Choose tools for the intended result. Do not force one renderer onto every approach. Open the whole image, enlarge risky areas, and inspect it at its intended display size.

Record the defect, suspected cause, change, and post-revision evidence. Address observed causes before adding decoration. If tools or budget prevent repair, stop with a revision status and a specific next step. Do not proceed to taste selection to avoid fixing a defect.

### 7. Compare only ready candidates

Use the communication and style guide. Hold purpose, action, and viewing conditions constant. Apply the appropriate craft standard to each style; equal detail is not required.

Once all candidates are ready, compare what they communicate and what they sacrifice. Explain the choice against the brief. User preference is legitimate, but it is not a universal law or objective taste score.

If a candidate is not ready, withhold the taste decision. Early concept critique may expose problems; it does not prove one style is better.

### 8. Deliver with an evidence status

Provide visual output when requested, reference credits, and a short account of changes and remaining limits. Save a worksheet for continuing work. Update project memory at milestones when the project has a memory file.

Name the checks actually performed. "The PNG opens" differs from "the structure matches the reference." Without a real viewer study, label communication claims as agent judgment or hypotheses.

## Required critique format

`Location → visible issue → why it matters for this brief → proposed change → recheck.`

Example: "At the nape, the head still ends as a separate arc. In this observational study, the connection looks pasted on. Adjust the transition against the photo, then inspect the silhouette without feathers."

Do not use "more premium," "more alive," or "better taste" without identifying the visual decision involved.
