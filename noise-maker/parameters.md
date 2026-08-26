# Parameter Sheet — Noise Maker (current, as-printed state, 2026-08-25)

**This document replaces all prior content of this file** (an earlier abandoned design direction —
three-part gear/pawl mechanism copied from a different commercial product, and a since-superseded
fully-parametric-Clacker pairing). That history is preserved in this repo's git log if ever needed;
it is not repeated here. Everything below describes the design that was actually printed
successfully.

## 0. What this is

A two-part **print-in-place ratchet noisemaker** ("football rattle" / gragger mechanism). Both
parts print together in a single job, in their final assembled position, with a small built-in
clearance gap — never separated and reassembled by hand.

- **Handle** — the part held in the hand. A mechanism head near one end (hex tip + a ring of gear
  teeth) passes through the Clacker's collar; the rest of the Handle is a long, smooth tapered grip.
- **Clacker** — a forked loop that spins freely around the Handle's mechanism head. A thin flexible
  tang on the Clacker catches each tooth as it rotates past, producing the "clack."

**Shared axis** (Fusion internal cm units, world coordinates): the Handle's long axis and the
Clacker's rotation axis are the same line, at world **X = 7.6985cm, Z = 9.8222cm**, running along
world **Y**. Every radius/position value below is measured from this axis unless stated otherwise.

## 1. Handle

Component `HandlePart`, single body `Handle`. Overall span: world Y = 0 to ~19.05cm (190.5mm), the
long axis running the full "handle" direction.

### 1.1 Mechanism head (Y = 0 to ~4.35cm)

This portion originates from the user's own Tinkercad-designed Handle piece (a mesh import,
`CutPasteBodies1` in the Fusion timeline) — its exact organic tooth-tip/hex-tip surface shape is
**not reproducible from a blank sketch**; the authoritative source for this shape is the exported
STEP file (see §4). What follows are the dimensions and modifications that WERE deliberately set
and can be reproduced/re-verified even without the original mesh:

| Feature | Value |
|---|---|
| Hex tip | Near Y=0, passes through the Clacker's collar bore. Decorative/clearance-only fit, not a keyed/precision mating feature. |
| Gear-tooth ring | Final axial length **26.0mm**, positioned at world **Y = 0.9cm to 3.5cm**. Tooth peak radius ~29.7–30.3mm (varies slightly per tooth); root radius ~22.9–23.2mm. Radial reach was grown a net **+2.2mm** over the life of the project from the original mesh's tooth size (via `OffsetFacesFeatures` on the tooth-tip faces — faces identified by radius >26mm within the tooth's Y-band). |
| Retention bumps | **None** — six cone-shaped bumps were added mid-project (as an explicit anti-slide feature for when the assembly is held inverted), then deliberately retracted back to baseline once the final tooth-ring length/position made them redundant: the tooth ring (~30mm radius) sitting only ~4mm from each collar wall already blocks the Clacker's collar bore (~23.5mm) from traveling far enough to matter. If the tooth geometry changes significantly in a future revision, re-verify this is still true. |
| Overall diameter | +0.5mm, uniform, applied early in the project (`OffsetFacesFeatures` on all outer faces). |
| Collar-mating shaft radius | ~22.76–23.24mm at the two points where the Handle passes through the Clacker's collar walls (world Y≈0.1–0.5cm and Y≈3.95–4.35cm) — gives ~0.28–1.1mm clearance against the Clacker's ~23.5–23.9mm hex bore, depending on facet angle. |

### 1.2 Grip shaft (Y ≈ 4.35cm to 19.05cm) — fully reproducible, smooth revolve

The original grip had a knurled/textured surface; this was **deliberately removed** (texture is
meant to be added at the slicer level instead) and replaced with a plain smooth revolve of the same
underlying taper. This is a genuine parametric feature and can be rebuilt exactly from the profile
below:

**Build recipe:** sketch the following (Y in cm, radius in mm) as a profile in a plane containing
the long axis, close it back to the axis at both ends, and revolve 360° around the axis.

| Y (cm) | Radius (mm) | | Y (cm) | Radius (mm) |
|---|---|---|---|---|
| 5.65 | 20.6 | | 14.0 | 20.907 |
| 5.7 | 20.451 | | 14.5 | 22.16 |
| 6.0 | 19.995 | | 15.0 | 23.892 |
| 6.5 | 19.243 | | 15.5 | 25.646 |
| 7.0 | 18.879 | | 16.0 | 26.626 (widest point) |
| 7.5 | 18.537 | | 16.5 | 26.603 |
| 8.0 | 18.377 | | 17.0 | 24.826 |
| 8.5 – 12.5 | 18.218 (flat waist) | | 17.5 | 21.043 |
| 13.0 | 18.924 | | 18.0 | 14.207 |
| 13.5 | 19.676 | | 18.3 | 13.569 |
| | | | 18.6 | 9.536 |
| | | | 18.8 | 6.733 |
| | | | 19.0 | 1.515 |
| | | | 19.051 | 0.0 (tip) |

Shape in plain terms: tapers in from the mechanism head to a narrow waist (~18.2mm) around
Y=8.5–12.5cm, flares out to its widest point (~26.6mm) around Y=16cm, then tapers to a rounded
point at the very tip.

**Verified**: this revolve was cross-checked point-by-point against the original knurled surface's
*averaged* radius (ignoring the ~0.5mm knurl texture itself) at multiple Y stations — matched
within 0.06mm everywhere checked.

## 2. Clacker

Two versions exist. **Read this section before picking which to build from.**

### 2.1 Clacker v2 (mesh-derived) — the one that was actually printed

Starts from the user's original Tinkercad Clacker mesh (also not separately exported into this
repo — only available inside the Fusion document's history, or as frozen geometry inside the
combined STEP/STL exports). **Cannot be rebuilt from a blank sketch** for this reason — its organic
fork/tail/tang shape is only preserved in the exported geometry files.

One deliberate modification was made and IS fully specified: the flex tang's reach was extended
**0.5mm** (from 29.35mm to 28.85mm radius, at world Y≈1.1–3.3cm, angle=180° from the shared axis)
by building a small solid wedge (radial span 28.85mm–33.0mm, angular half-width ~1.4mm, at that Y
range) and boolean-joining it to the existing tang. This closed the engagement gap against the
final tooth-ring size (see §3).

### 2.2 ClackerV3 — clean parametric rebuild, NOT printed, but fully reproducible from scratch

Built from measured reference points against Clacker v2, specifically so future edits don't require
fighting a 1000+ face mesh-derived body (v2 has 1157 faces; this rebuild has 59). **This is the
recommended starting point for any future Clacker changes.** Full build recipe, all dimensions
relative to the shared axis:

**Step 1 — arm/fork wall.** Sketch a thin (4mm wall thickness) ring-like profile through these
measured inner-boundary points (angle in degrees from the axis, radius in mm), spanning only 90°
to 270° (the fork's real angular extent — leave 270°→90° genuinely open, do not close it with a
straight chord across the middle, or the Handle's shaft will be blocked):

`90:34.13, 100:31.5, 110:31.64, 120:33.4, 130:36.55, 140:41.75, 150:50.48, 160:66.36, 170:101.3, 190:101.32, 200:66.37, 210:50.49, 220:41.76, 230:36.56, 240:33.41, 250:31.64, 260:31.51, 270:34.14`

Extrude this profile from world Y=0.4cm to Y=3.953cm.

**Step 2 — tail.** A solid block from radius 9.0cm to 15.05cm, angular half-width ~1.6cm (centered
on angle=180°), spanning Y=0.4cm to 3.953cm — joined to the arm wall (overlapping it, not just
touching).

**Step 3 — tang.** A solid wedge from radius 2.885cm to 9.2cm (the larger outer radius here — vs.
3.30cm used for the v2 patch — is needed because this tang has no pre-existing mesh material to
anchor into; it must reach all the way into the tail block itself), angular half-width ~0.12cm,
spanning Y=1.1cm to 3.3cm, at angle=180° — joined to the arm wall/tail.

**Step 4 — collar plates (×2).** Circular rings, 23.5mm inner bore, 35mm outer radius, 4.5mm thick
(with 0.5mm intentional overlap into the arm wall to guarantee the boolean join succeeds): one at
world Y = −0.05cm to 0.40cm, one at Y = 3.903cm to 4.353cm.

**Join everything into one body in a single combine operation** (joining all tool bodies at once,
rather than incrementally, avoids a coincident-face join failure that occurred during development —
see the Fusion gotchas memory file for why).

**Verified**: zero overlap against the Handle anywhere; tang engagement and collar-bore clearance
both match Clacker v2's verified numbers (tang transitions solid at ~28mm, matching the 28.85mm
target; collar bore transitions at ~23.5mm inner / 35mm outer, exactly as designed).

## 3. Verified clearances (final design, Clacker v2 + Handle)

| Interface | Clearance / engagement |
|---|---|
| Front collar wall vs. Handle shaft | ~0.28mm minimum (tight but positive) |
| Back collar wall vs. Handle shaft | similar, ~0.3–1mm depending on facet angle |
| Tooth ring vs. rigid Clacker arms | ~1.8mm minimum (comfortable print-safety margin) |
| Tooth peaks vs. flex tang | ~0.4–0.9mm real engagement (positive interference — this is what makes the click) |
| Tooth-ring buffer to each collar wall | ~4mm front, ~4.5mm back — this is what blocks axial slide when inverted, replacing the removed retention bumps |

All verified via direct point-containment/ray-cast probing against the live geometry, not assumed.

## 4. What requires the exported STEP file, not a blank canvas

Two organic, mesh-originated shapes are only fully preserved in the exported geometry (STEP is the
better starting point of the two, since it preserves real surfaces rather than a raw triangle mesh
like STL/3MF do):
- The Handle's mechanism-head surface detail (exact hex-tip and tooth-tip contours).
- Clacker v2's fork/tail/tang organic outer contour.

If a future edit needs to change these specific shapes significantly (not just resize/reposition,
which the offset/join recipes above already cover), start from `step/` and edit the imported
geometry directly, or use **ClackerV3 (§2.2)** for the Clacker, which sidesteps this limitation
entirely by being a true parametric rebuild.

## 5. Material and print settings

| Parameter | Value |
|---|---|
| Material | PLA (both parts, as printed) |
| Note | The Clacker's flex tang is a repeatedly-cyclic-load feature (flexes on every click) — PETG would be more durable here, but PLA and PETG don't bond, so mixing materials isn't viable in a single print-in-place job. If durability becomes an issue, printing the whole assembly in PETG (not just the tang) would be the way to address it. |
| Print orientation | Upright, grip end down on the bed |
| Bed | Fits comfortably within a 256×256×256mm build volume |

## 6. Files

| File | Contents |
|---|---|
| `stl/Noise_Maker_Handle_Clacker_v4_TestPrint.stl` | **Current, printed, working design** (Handle + Clacker v2, final state described above) |
| `step/`, other files in `stl/`/`3mf/` | Earlier design iterations — kept for history, not current |
| `dot_pipeline/specs.md`, `dot_pipeline/tests.md`, `dot_pipeline/verdict.md` | Snapshot from mid-project (after the tooth/retention-bump work, before the final tooth reposition/resize and bump removal) — useful for the verification methodology, but the specific numbers there are superseded by §3 above |
| `reference/` | Photos from an earlier, abandoned design investigation (a similar-looking but different commercial product) — not representative of the final design |
