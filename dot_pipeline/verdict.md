# Verdict — Lightswitch-Cover-Single

## PASS

Both test targets — `Lightswitch Cover Single V2 (corrected jumbo)` and
`Lightswitch Cover Single V2 (tapered edge)` — are approved for printing.
Full measurements and methodology are in `tests.md`.

## Reasoning

Every check that could gate a print was independently re-measured from the
live Fusion geometry (not re-read from prior reports) and passed:

- **Topology**: both bodies are single, watertight solids (`lumps==1`,
  `isSolid==True`). The tapered-edge body was diffed feature-by-feature
  against the corrected-jumbo body and differs *only* by the intended
  1.5mm outer-edge fillet (8 cylindrical + 8 toroidal faces, matching
  exactly) — no stray geometry changes.
- **Screw hole**: shank diameter 4.7625mm, countersink top diameter
  7.9375mm, 45° half-angle (genuine cone, not a counterbore), total guide
  channel 1.9000mm — all match the retail-verified values exactly. Critically,
  by enumerating every face on the body I confirmed there is no material
  anywhere between the boss floor (Y=3.10mm) and the back opening (Y=0mm) at
  either screw location — **a screw can physically pass all the way
  through**, which was the main open question carried over from the prior
  fix round.
- **Wall thickness**: thinnest wall found is 1.65mm (general skin/side wall),
  comfortably clearing the 0.8mm nozzle minimum with 0.85mm to spare (106%
  over). The boss/collar wall (2.12mm) has even more margin.
- **Fit/clearance**: the relief pocket clears the real switch yoke
  (44.45×74.625mm) by 20.6mm on the tight axis and 30.9mm on the other —
  large margin, no interference risk.

## Non-blocking items flagged (do not gate this pass)

1. **Spec text inaccuracy**: `specs.md` §5 describes a ~4mm rim inset /
   80.9×131.7mm pocket footprint; the actual geometry uses a 1.65mm inset /
   85.6×136.4mm pocket. The deviation is favorable (bigger pocket, more
   clearance), so it's not a functional problem — but the spec document
   should be corrected so it stops describing geometry that doesn't match
   the model.
2. **Print-process advisory, not a defect**: the boss/collar floor (a small
   9mm-diameter ring at each screw location) is structurally connected only
   from above and hangs over open cavity below it, in the documented print
   orientation. This is very likely printable as a short bridge given its
   small size, but is worth a slicer bridging-setting check and a look at
   the first layer of that feature on the first real test print.
3. **ESTIMATED values, confirmed intentional, not gaps**: 9mm boss/collar
   diameter and 1.5mm tapered-edge fillet radius are explicit design choices
   without a real-world reference spec behind them (as called out in the
   task background) — listed for traceability, no action required.

## What would have blocked this pass (none found)

- A boss/collar diameter, shank diameter, or countersink geometry that
  didn't match the retail-verified hardware numbers — not found; all exact.
- A wall under 0.8mm anywhere — not found; thinnest is 1.65mm.
- A blocked/obstructed screw channel — not found; verified open by complete
  face enumeration, not sampling.
- A split body, non-manifold geometry, or unintended difference between the
  two test bodies — not found; both are single solids, and the tapered body
  differs only by its intended fillet.
- A pocket too small to clear the real switch yoke — not found; margin is
  >20mm on every axis.
