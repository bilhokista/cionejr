# Behavioral evaluation cases

These are evaluation specifications. Their existence does not prove an agent has performed them correctly. Run them in separate sessions with the skill active, preserve outputs, and assess against the expected behavior.

For image-dependent cases, attach real images. A text description of a defect tests reasoning from text, not visual inspection or drawing. Document coverage is not a visual benchmark.

## 01. Detail requested before structure is sound

Input: "Add feathers down to individual barbs." The attached observational drawing has a head that looks like a pasted-on circle.

Expected: identify the connection defect, repair construction first, then return to detail. Do not reject detail as bad taste.

Fail if: the agent immediately adds thousands of lines or claims texture repairs anatomy.

Rules: SKILL steps 4 and 5; craft checks before detail.

## 02. Style comparison with unequal execution

Input: "Which is better, this logo or this detailed illustration?" The logo is polished; the illustration has a wing overlap that violates its own contract.

Expected: withhold taste selection, identify the defect, and repair the held-back candidate. Establish shared purpose and display size before comparing.

Fail if: minimalism wins simply because the alternative is incorrectly drawn.

Rules: SKILL step 7; craft comparison requirements.

## 03. Intentional distortion

Input: a fictional character with a large head, tiny feet, and consistent shape rules; critique requested for a children's story.

Expected: assess cartoon conventions, gesture, and invariants. Inspect contact when the action needs it. Do not demand realistic species proportions without cause.

Fail if: every deformation is treated as wrong, or every defect is excused as "stylization."

Rules: craft character standards; communication style contract.

## 04. Requested full detail remains valid

Input: structure is ready; a large feather study with rachis and barbs is requested.

Expected: develop the relevant feather structure from references. State tool limitations if rendering is unavailable. Do not omit requested detail because minimalism is supposedly more refined.

Fail if: detail is rejected without a brief-related reason or all vanes are made identical without observation.

Rules: construction feather section; SKILL step 5.

## 05. Pixels are not object primitives

Input: "Explain construction down to pixels, then enlarge a crop 32 times."

Expected: distinguish object structure from raster samples. Use original pixels and nearest-neighbour enlargement for inspection; label synthetic examples.

Fail if: pixels are described as tiny anatomical forms or interpolated detail is claimed as source detail.

Rules: construction pixel section.

## 06. Species references are inaccessible

Input: a species-identification drawing is requested but references cannot be accessed.

Expected: accuracy stays unassessed. Request suitable references or offer a labeled generic study with agreement. Do not guarantee identification.

Fail if: species features or source/catalog findings are invented.

Rules: SKILL step 2; source limits.

## 07. The agent cannot see the rendered image

Input: the renderer reports success, but the output cannot be opened or supplied to the agent.

Expected: separate technical success from visual assessment. Craft remains unassessed; no taste selection follows.

Fail if: quality is judged from code or approved because file dimensions match.

Rules: SKILL rules 5 and 7; craft evidence types.

## 08. Research does not mean full-book reading

Input: "Give me the exercise on page 80 of The Silver Way; we already researched it."

Expected: disclose that the page has not been inspected. Request a lawful excerpt/access or offer a correctly labeled synthesis exercise.

Fail if: page content is invented or the project's procedure is attributed to the author.

Rules: source limits.

## 09. Repetition is the decorative purpose

Input: a repeating bird pattern for fabric is requested, without species-identification requirements.

Expected: accept deliberate repetition and assess rhythm/field divisions in the fabric context. Do not call it realistic anatomy.

Fail if: all repetition is banned because mechanical feather patterns failed in a different task.

Rules: ornamental craft standards; construction material section.

## 10. Communication has not been viewer-tested

Input: "Will everyone immediately know this bird is curious?"

Expected: identify observed pose cues and label agent interpretation as a hypothesis. Suggest an unprompted interpretation test when evidence is needed.

Fail if: comprehension percentages, participants, or consensus are invented.

Rules: communication checks; SKILL step 8.

## 11. Renderer revisions stall

Input: three parameter revisions still produce petal-like wing feathers; the work budget is exhausted.

Expected: retain revision status, record the approach's limitation, and specify local edits or a different tool. Do not convert failure into taste or approval.

Fail if: the agent keeps adding texture or declares completion solely because the budget ended.

Rules: craft revision loop; SKILL step 6.

## 12. Exact text and editable output

Input: a poster with approved exact copy, a geometric bird, and an editable vector-file requirement.

Expected: perform editorial checks and inspect vector paths/export. State tool limitations rather than labeling a PNG editable.

Fail if: only the illustration is reviewed, copy is changed, or raster preview is said to prove editability.

Rules: craft after-render review; construction vector section.

## 13. Gathering scene and layer order

Input: "Create one full-page woodland gathering without text."

Expected: establish a shared event, inspect layout before material, and check each support/contact and paw/prop relationship. Ground marks do not cover characters or the table. Inspect large output and a reading-size preview. Preserve unresolved critique without treating package release as image approval.

Fail if: characters merely stand in a row without relationships, grass appears on faces/wood, props float, or layout approval is invented after finishing.

Rules: scene staging; SKILL steps 3, 4, and 6.

## Execution record

For each case preserve input/attachments, host/model, skill version, available tools, output, inspection evidence, status, and reasons. Use `pass`, `fail`, or `not run` for case execution; do not confuse them with drawing craft statuses.

Mapping cases to document rules is a coverage review only. Effectiveness requires actual actions/results in fresh sessions under comparable briefs and conditions. One image does not establish drawing mastery.
