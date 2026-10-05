# Project status

## Scope

cionejr is an experimental open-source illustration skill with reproducible Python examples. The skill uses basic shapes, contextual craft checks, and scene staging. It is not an editor plugin or image model.

## Initial distribution

- Portable skill name/directory: cionejr, version 0.1.1 (0.1.0 at first publish), MIT.
- Includes construction, craft, communication, scene staging, a worksheet, and behavioral evaluation specifications.
- Samples: three bird render treatments and one woodland storybook page. Their limitations are documented; the forest example needs refinement.
- Validation tooling checks frontmatter and local links. Renderer tests check output contracts and selected placement rules, not artistic quality.
- No source photos, third-party books/videos, proprietary fonts, or private session transcripts are bundled.
- Local checks passed: 18 validation/font-portability tests and eight example-output tests, plus the skill validator and 31 repository-local Markdown links. Renderer examples were regenerated before publishing preparation.
- Public repository: https://github.com/bilhokista/cionejr, main branch, MIT license verified through the GitHub API.
- Initial source commit 4bcc9a1 passed CI on Ubuntu and Windows, including regenerating and checking both examples: https://github.com/bilhokista/cionejr/actions/runs/37274519720. This does not establish artistic quality or agent behavioral effectiveness.
- Behavioral evaluation list contains 13 specifications; they have not been executed as an independent agent benchmark.

## English-first update

- All core skill instructions, supporting guides, worksheet, and 13 evaluation cases are now in English. The separate Indonesian README was removed to keep the initial distribution consistently English.
- Bird labels and the geometric sample filename are English. Regeneration and all 26 local tests passed after the rename; the missing English output was observed to fail before implementation.
- User-facing responses remain language-selectable; English documentation does not imply culturally universal taste judgments.
- Checked 22 current repository-local Markdown links and staged whitespace. English-first commit 9d691ad passed Ubuntu/Windows CI, including both example renderers: https://github.com/bilhokista/cionejr/actions/runs/37275514501.

## Earliest-alpha contribution invitation

- Marked v0.1.0 explicitly as the earliest alpha in the README and skill; metadata status is earliest-alpha.
- Added a visible invitation for as many people as possible to help improve the project. Drawing critiques and agent-use reports are welcome alongside focused code changes; programming experience is not required.
- CONTRIBUTING.md now points newcomers to issues or small pull requests. Existing evidence, privacy, and licensing requirements remain in place.

## Forest example second pass

- Replaced coarse protected rectangles with a shape-aware ground-mark mask (silhouettes plus 12 px margin). Wrote the failing test first, then the implementation; the test covers points inside the old boxes, just outside contours, and on ears, paws and the stump rim.
- Fox apple now sits on the stump top beside the paw with a contact shadow; deer gaze lowered to the basket; foliage mixes fronds and broad leaves with per-leaf colour jitter. Three floating contact shadows added first were judged detached in a full-resolution crop and removed.
- Checks run: skill validator, 18 repository tests, 5 forest output tests, `git diff --check`. These do not establish artistic quality; visual judgments are the agent's own.

## Refinement pass and first evaluation run (2026-10-05)

- Forest: pear-shaped fox with shoulder and haunch, deer with S-curved neck, lowered head and hock-bent legs, rabbit shoulder fill, foliage anchored to branch points. Gouache bird rebuilt with opaque brush-cut fields and form-following strokes.
- Ran all 13 evaluation cases once in fresh Sonnet 5.5 subagent sessions with the answer key withheld. 01 and 06 failed on v0.1.0 (detail over a known defect; species plate from memory). Added rules 9 and 10, bumped to v0.1.1, reruns passed. Record: evaluations/runs/2026-10-05.md. Fixtures: evaluations/fixtures/make_fixtures.py.
- Limits: one run per case, agent grader, same model family, reruns tuned to the failures, case 12 leaked a host skill.

## Next

Continue the craft work in docs/roadmap.md. Keep publication/technical checks separate from visual approval. Run behavioral evaluations with actual image inputs in separate agent sessions before claiming effectiveness.
