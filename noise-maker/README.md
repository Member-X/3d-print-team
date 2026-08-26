# Noise Maker

A two-part **print-in-place** ratchet noisemaker (the classic "football rattle" / gragger mechanism) — prints as one job, fully assembled and working straight off the bed, no post-print assembly.

## What it is

- **Handle** — the part you hold. A hex tip and gear-tooth ring near the base mate through the Clacker's collar, topped by a long smooth, tapered grip shaft (surface texture is left to be added in the slicer rather than modeled into the part).
- **Clacker** — a forked loop that spins freely around the Handle's base once printed. A flex tang on the Clacker catches each tooth as it spins, producing the ratchet "clack."

The two parts are printed together with a small clearance gap between them so the Clacker can rotate freely but can't be pulled apart from the Handle.

## Current design

- Gear-tooth ring: 26mm long, sized and positioned so the tooth ring itself blocks the Clacker from sliding along the handle when the toy is inverted (no separate retention pins needed).
- Clacker's flex tang extended slightly (0.5mm) over the original design for reliable tooth engagement.
- Grip is a smooth taper — no molded knurl/texture (added at the slicer level instead).

## Files

- `stl/Noise_Maker_Handle_Clacker_v4_TestPrint.stl` — **current, printed, working design.**
- `step/`, `3mf/`, other files in `stl/` — earlier design iterations, kept for history (including an earlier mechanism concept based on a similar-looking but different commercial product, which was abandoned in favor of matching the original hand-made design).
- `dot_pipeline/` — design/verification notes (partially superseded by later revisions — the final printed design is described here, in this README).
- `reference/` — reference photos from earlier design exploration.

## Print notes

- Material: PLA.
- Orientation: stand upright, grip end down on the bed.
- Note the Handle+Clacker pairing currently exported/printed uses the original mesh-derived Clacker geometry. A from-scratch parametric rebuild of the Clacker (cleaner, far fewer faces, easier to edit) also exists in the Fusion project but hasn't been printed — worth switching to if the design needs further changes later.
