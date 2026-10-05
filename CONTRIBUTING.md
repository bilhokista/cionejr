# Contributing

cionejr is in its earliest alpha. We want help from as many people as possible, including people who draw and people trying an agent skill for the first time. You do not need to be a programmer or an expert to contribute.

Start with [an issue](https://github.com/bilhokista/cionejr/issues) or a small pull request. A drawing critique with the brief and a marked problem area is useful. So is a report showing where an agent misunderstood an instruction. Include evidence when you can, and say what you could not check.

Keep a change tied to an observable problem. For visual work, include the brief and identify the location of the defect. Explain why it matters for the intended style rather than describing it as insufficiently premium or modern.

## Before a pull request

Run the skill validator and Python tests. Run an example's output checks when changing its renderer; render and inspect the changed image as well. Preserve before/after evidence in the pull request or a linked issue without adding every intermediate binary to the repository.

```bash
python tools/validate_skill.py
python -m unittest discover -s tests -v
python examples/bird-styles/test_outputs.py
python examples/forest-meeting/test_outputs.py
git diff --check
```

File tests do not substitute for visual inspection. State any checks you could not perform. New validator behavior should have a failing test before implementation.

## Useful changes

Improve character construction or interaction, fix a specific overlap, add a reference with verified scope, or make a renderer more portable. Avoid large batches of decorative variations with no distinct purpose.

Behavioral evaluations need actual inputs, outputs, host/model context, and inspection evidence. Do not mark the written evaluation cases as passed just because matching rules exist in SKILL.md.

## Rights and privacy

Only contribute material you can license under MIT. Record the provenance of references and any third-party material. Do not add books, proprietary fonts, unlicensed images, credentials, or private conversations. Do not copy an artist's character and call it original.

Submitting a contribution means you agree to license that contribution under the repository's MIT license.
