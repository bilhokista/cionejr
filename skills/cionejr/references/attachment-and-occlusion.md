# Attachments and occlusion

Read this when a part looks pasted on, a prop floats, or an action is unclear. Diagnose the relationship before adding surface marks. Apply it within the style contract, not as a universal anatomy rule.

## Keep working stages distinct

A mass layout contains body/head envelopes, action axes, major props, and support planes. Leave out eyes, plumage patterns, bark, and decorative foliage. It should be cheap to revise.

A value study checks light-dark relationships. Desaturating a finished picture creates a value study, not evidence that a construction layout was inspected before finishing. Both are useful; label them accurately. A simplified reconstruction made later is a new diagnostic aid, not historical proof of an earlier step.

Open the mass layout before developing materials. A renderer can write a layout file, but it cannot record human or agent inspection merely by producing that file.

## Record the intended relationships

For each important action, write a small relationship list:

| Parts | Intended relationship | Evidence to inspect |
|---|---|---|
| Head / torso | Attached through neck or shoulder | Continuous outer form, or a readable attachment under the style's conventions |
| Wing or arm / grip | Grip belongs to the limb | Traceable route from the body; no unexplained isolated oval |
| Grip / leaf | Leaf is held | Visible contact and deliberate overlap order |
| Foot / stump | Weight rests on a surface | Contact with the top plane, not only horizontal alignment |
| Character / speaker | Attention follows the event | Head direction and relevant gaze cues, not only a left/right mirror |

Include only relationships the brief needs. Parts intentionally separated in a symbol, cut-paper construction, or exploded diagram do not need anatomical joining. Record the exception.

## Inspect the actual rendered contact

1. Hide texture when practical. Inspect both parts alone, then together in the whole image.
2. Trace the attachment from one mass to the other. Distinguish a missing connector from a contour crease or intentional separation.
3. Enlarge the shared area. A prop can be near a paw without touching it. Check where the fingers/wing end actually land.
4. Inspect front-to-back order. A neck painted over a belly can introduce a triangular patch even when it closes the gap. Put connectors behind the masses when the pose requires that order.
5. Return to reading size. Contact that exists as one accidental pixel may still look broken. Conversely, exaggerated repairs may erase a necessary contour distinction.

Use negative space as evidence: is the gap supposed to be background, a separation line, or an opening between articulated parts? Avoid filling every gap indiscriminately.

## Choose the smallest structural repair

| Observed issue | Likely repair to investigate | Insufficient workaround |
|---|---|---|
| Head floats above body | Adjust the attachment or redraw a tapered neck/shoulder with appropriate overlap | Add fur across the empty background |
| Paw misses a held object | Repose the forearm/wing and grip together; check both attachment ends | Move only the object until it hides the gap |
| Connector cuts across a surface patch | Change layer order and inspect the outer contour again | Add a shadow over the resulting triangle |
| Limb disappears behind a rim | Specify its path and which portion crosses in front | Put a detached paw in front of the prop |
| Character only mirrors toward a speaker | Inspect head pitch, gaze, and pose for the actual event | Claim the entire group is listening from an x-coordinate test |

Do not copy a connector shape across every animal. Its width, curvature, and attachment depend on pose and the chosen abstraction.

## Useful checks for code-generated examples

Rasterized SVG part masks can check known overlap or silhouette connectivity while keeping actual transforms. Run them against the previous version so a passing test proves it catches the specific regression.

Calibrate sampling size and alpha threshold. Preserve clipping and transforms when isolating parts. Keep semantic parts named when using SVG. A foreground prop may be occluded in the final image, so inspect isolated masks and the composite together.

These checks have limits:

- Overlapping paint does not prove a convincing grip or plausible anatomy.
- Connected components can connect through an unintended shape elsewhere. Inspect the local route too.
- Non-overlap between characters is not a general quality rule. Interaction may require them to overlap.
- A mirror test checks horizontal facing, not gaze or viewer comprehension.
- Passing at one size does not establish readability at every size.

Use automated checks for narrow authored contracts. Do not turn them into artistic scores or apply this example's pixel thresholds to every drawing.

## Recheck record

Preserve the previous image and inspect the same crop in the revision. Record:

`Parts and relationship → observed gap/order defect → repair → local recheck → reading-size recheck → remaining limits`.

Keep unaffected strengths. If the repair introduces a new edge or hides an important cue, revise again. Do not call the whole illustration finished because two contacts improved.
