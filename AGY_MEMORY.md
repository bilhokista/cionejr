# Project status

## Scope

cionejr is an experimental open-source illustration skill with reproducible Python examples. The skill uses basic shapes, contextual craft checks, and scene staging. It is not an editor plugin or image model.

## Initial distribution

- Portable skill name/directory: cionejr, version 0.1.0, MIT.
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

## Next

Continue the craft work in docs/roadmap.md. Keep publication/technical checks separate from visual approval. Run behavioral evaluations with actual image inputs in separate agent sessions before claiming effectiveness.
