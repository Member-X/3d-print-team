# Parameter Sheet — Cat Toy Holder (v5 rebuild, current as-built state)

Current-state-only reference: everything below is the **final, currently-exported geometry** of
`Cat Toy Holder v5 (rebuild) Final` (body name as of this revision — the user renamed it in Fusion;
component path is still `Cat Toy Holder v5 (rebuild):1`) in the Fusion document `Cat Toy Holder`.
This is enough on its own to rebuild the part from scratch. For the full iterative history
(correction rounds, dead ends, restored/degraded reference-body investigations, why earlier
approaches were rejected) see [`dot_pipeline/specs.md`](dot_pipeline/specs.md) — this document
intentionally does not repeat that narrative; cross-references to specific spec sections are given
below only where useful for provenance.

All dimensions in mm. Coordinate convention used throughout (matches the live Fusion body and the
print-ready export): **X = width (−1 to 233mm, 234mm total), Y = height (0–230mm), Z =
thickness/depth (0–41.308mm)**, origin at what was the bottom-left corner before the panel was
widened (the working body's own local X range is no longer 0-based — see "Overall panel" below).
The exported STEP/3MF/STL files are a translated copy of this same body, centered in X/Y at the
world origin (X −117 to 117mm, Y −115 to 115mm) with the bottom face at Z=0 — print-ready as
exported, no further repositioning needed.

## Overall panel

| Parameter | Value |
|---|---|
| Width (X) | **234.000mm** (grew from 232.000mm — see "End wall thickness" below) |
| Height (Y) | 230.000mm |
| Thickness (Z) | 41.308mm |
| Outer corner fillet radius (all 4 corners) | **5.0mm** (at the current, widened outer corners) |
| Body volume (current) | 747.4789 cm³ |
| Fill ratio (volume ÷ solid bounding-box volume) | 33.58% |

## Wand channels (×7)

| Parameter | Value |
|---|---|
| Count | 7 |
| Horizontal pitch (center-to-center) | 33.142857mm (= original 232mm interior arrangement ÷ 7 — **unchanged** by the panel-width increase; the extra 2mm went entirely into the two outer end walls, not the channel pitch — verified directly, rib X-positions identical to the mm before and after) |
| Channel width (open void, between ribs) | 29.000mm (unchanged) |
| Channel construction | Open-top vertical slot per wand — front wall, side walls (ribs), and (above Y≈213.1mm only) a back wall; open at the true top edge (Y=230mm) for the wand to drop in |
| Top opening | **Not a round bore.** The channel is a plain continuation of the same 29mm-wide rectangular void all the way to the top edge — no diameter, no radius, no separate "hole" feature. See "Vertical wall structure" below for exactly what changes above Y≈213.1mm. |
| Overhangs | None >45° — every wall is either vertical (parallel to print/thickness axis) or a straight top-down opening; no supports needed |

## Ribs / dividers (between channels)

| Parameter | Value |
|---|---|
| Interior rib count | 6 |
| Interior rib width | 4.142857mm |
| End divider / outer end wall (panel's own left/right perimeter wall, acting as the two outermost channel walls) | **~3.071mm each** (increased from 2.071429mm — 1mm added to each side, per explicit request; verified directly via geometry, left ≈3.06–3.08mm, right ≈3.06–3.08mm) |
| Rib height | Full panel height (Y 0–230mm) — solid, continuous, no step or notch anywhere along their length |
| Rib edge fillet | 2.0mm radius, on the vertical edges facing into each channel |
| Rib depth (through thickness) | Full thickness at every rib position (solid Z 0–41.308mm) — ribs are solid full-thickness columns even where the front/back walls around the open channel are thin/absent |

## Vertical wall structure (front / back walls, by Y-band)

| Y-band | Front wall (Z=0 side) | Back wall (Z=41.308 side) | Notes |
|---|---|---|---|
| Base band, Y 0–62mm | 7mm solid | 4mm solid | Hollow cavity between (see "Base / hollow cavity" below, now with 2 internal reinforcement webs); ribs continue solid through it |
| Main channel band, Y 62–213.1mm | 7mm solid (6 of 7 channels); **~7.0mm on the 2 keyhole-adjacent channels too**, as of a recent equalization edit — was ~6.6–6.7mm on those 2 only, now matches the other 5 | **Open — no back wall** | Channel is open front-to-back through most of its depth here; this is the original design's "channels open to the back" character. **Unreinforced for print-support purposes** — see "Print-quality reinforcement" below for why |
| Top band, Y 213.1–230mm | 7mm solid | **3.9mm solid** (Z≈37.4–41.3mm) | Back wall reappears in this band only, closing the channel's back; front wall unchanged. This band + the continuous full-height ribs (above) is what forms the open-top "slot" each wand drops into — no round hole, no fillet transition, just a plain rectangular slot open at the very top |

The Y≈213.1mm value is the measured transition where the back wall begins (fine 0.1mm-step
verification); there is **no other transition** — ribs and front wall run identically through this
Y value with no step, notch, or radius change.

## Base / hollow cavity (Y 0–62mm band only)

| Parameter | Value |
|---|---|
| Bottom solid lip | 5mm (Y 0–5mm, full width, solid) |
| Hollow cavity | Y≈5–52mm, between the 7mm front wall and 4mm back wall |
| Solid floor slab (separates cavity from the channel band above) | 10mm (Y 52–62mm, full width, solid) |
| Ribs through the cavity | Solid, full thickness, unchanged (6 interior + 2 end walls, same dimensions as elsewhere) |
| **Internal reinforcement webs (new)** | Two 2mm-thick horizontal webs, Z 16–18mm and Z 26–28mm, spanning the full width of all 7 channels, Y 5–52mm — see "Print-quality reinforcement" below |

## Print-quality reinforcement (base band only)

Added to reduce free-standing/floating-shell print instability in the interior ribs, which are
otherwise thin (4.14mm), tall, laterally-unbraced walls with open channel void on both sides for
most of their height. Confirmed via direct geometry, not a slicer re-check (no slicer access this
pass):

| Parameter | Value |
|---|---|
| Location | Base band only (Y 5–52mm) — this region has no wand-clearance function, confirmed safe to reinforce |
| Web 1 | Z 16.0–18.0mm, 2mm thick, full width of all 7 channels |
| Web 2 | Z 26.0–28.0mm, 2mm thick, full width of all 7 channels |
| Effect | Splits the base band's ~31mm continuous open hollow (Z≈7–38mm) into three shorter unsupported spans (~9mm, ~8mm, ~10mm), bracing each rib segment laterally at two intermediate heights instead of only at its very top and bottom |
| Channel clearance impact | **None, verified** — `pointContainment` probed at 5 Y-positions across the full main band (70–210mm) × all 7 channels × 6 Z-depths — void (fully clear) at every point, 210/210 checks |

**Known, explicitly unresolved limitation**: the main channel band (Y 62–213.1mm, ~151mm — most of
the panel's height, and where the print-quality symptoms were actually observed) received **no**
reinforcement. Every bracing approach evaluated for that region required either widening a rib
(narrows its channel) or bridging across a channel void (blocks it) — both violate the hard
wand-clearance constraint, so neither was implemented. If print-quality issues persist in that
region, the remaining options are a different print orientation or an explicit, signed-off decision
to accept some channel-clearance tradeoff — not something to be decided unilaterally in CAD.

## Keyhole wall-mount slots (×2, mounting/wall-facing face)

**Design (current, final — this is the fifth version of this feature, built directly from a
reference parametric keyhole generator's literal source code; see `dot_pipeline/specs.md` §§23–27
for why the first four were rejected/corrected):** a genuine **two-layer** mechanism, not a single
uniform cavity:

- **Shallow layer** (Z=0–1.5mm, at the Z=0 mounting face): the classic narrow keyhole silhouette —
  round head-entry (9.3mm) at the bottom, narrow shaft (3.75/3.90mm) above it, rounded cap at the
  top. This is what's visible from the mounting face and is what forms the **retaining shelf**: solid
  material sits directly on top of the wider deep layer beneath it everywhere except within the
  narrow shaft's own width.
- **Deep layer** (Z=1.5–3.5mm, hidden beneath the shallow layer): a capsule/stadium shape, **9.3mm
  (head-diameter) wide for its entire length** (Y=191.65–211.0mm) — this is the hidden channel where
  the screw head actually resides and travels as the panel slides, connected to the surface only at
  the single entry point where the shallow layer's own round head-entry shape opens all the way down
  through both layers.

A wall screw is driven into the wall (left protruding), the panel is brought up so the screw head
passes through the full-depth round entry into the hidden deep layer, then the panel slides so the
shank travels within the narrow visible shaft slot (shallow layer) while the head travels,
unobstructed, in the wide hidden layer directly beneath it. The shallow layer's own solid material
(everywhere outside the narrow shaft width) is the shelf trapping the head.

| Parameter | Left slot | Right slot |
|---|---|---|
| Head/entry diameter | 9.3mm | 9.3mm |
| Shank width (shallow layer only) | 3.75mm | 3.90mm |
| Shallow layer depth (visible, narrow) | **1.5mm**, from the Z=0 mounting face | Same |
| Deep layer depth (hidden, head-width) | **2.0mm**, Z=1.5–3.5mm | Same |
| Combined pocket depth | **3.5mm** total | Same |
| Deep-layer travel length (entry center to resting position) | Y=191.65–211.0mm (~19.35mm) | Same |
| Slot Y-span (head bottom = entry, to shaft-cap top) | Y 187.0–215.15mm | Same |
| X center | 46.706mm | 183.706mm |
| Solid backing before the hollow interior | ~3.0mm+, verified | Same |

The two slots are **not exactly mirror-symmetric about the panel's center** (X=116mm) — sum of the
two X-centers is 230.412mm vs. 232mm for a true mirror pair, a ~1.6mm asymmetry. This is the
original reference design's own as-measured asymmetry, preserved deliberately, not a build error.

### Functional verification (5 checks, simulating the real insertion+slide mechanism)

| Check | Result |
|---|---|
| Head-diameter probe enters at the entry point and reaches the deep layer | Void at every point: 5 radial offsets (full head radius) through the full combined depth (Z=0.3–3.4mm), both slots |
| Head-diameter probe travels the full deep-layer length unobstructed | Void at every point: 5 radial offsets × 10 Y-positions (192–210mm), Z=1.6–3.4mm, both slots — 100 checks, zero exceptions |
| Shank-width probe travels the full shallow-layer length near the surface | Void at every point: shaft centerline + half-width offset × 14 Y-positions (188–214mm), Z=0.3–1.2mm, both slots — 112 checks, zero exceptions |
| Solid shelf exists in the shallow layer outside the shank width, along the full length, directly overlaying the open deep layer beneath | Solid at every point: 4 radial offsets (2–4.5mm) × 7 Y-positions (198–210mm), Z=0.3–1.2mm, both slots — 56 checks, zero exceptions. Directly confirmed as a stacked pair at a representative point (shallow solid, deep void, same X/Y) |
| No breakthrough past the combined depth into the hollow interior | Solid at every point: 3 radial offsets × 14 Y-positions, Z=3.6–6.3mm, both slots — 84 checks, zero exceptions |

All 5 checks pass, both keyholes, with dense multi-point coverage along the entire travel path (not
just endpoints). This closes the bug in the prior (fourth) version, which widened the *entire*
cavity to head-width starting at the surface — removing the shelf material entirely rather than
hiding the wide travel channel beneath a narrow visible layer.

## Material and print orientation

| Parameter | Value |
|---|---|
| Material | PLA or PLA+ |
| Why | Single-hang use (not repeatedly mounted/unmounted, so no cyclic-load case for PETG); strictly indoor use (no UV/heat exposure concern) |
| Print orientation | Front face down (Z=0 face on the bed) — the panel's flat 234×230mm face is the largest flat face and gives the best bed adhesion; print height = 41.308mm |
| Overhangs | None >45° anywhere in the design |
| Supports | Not expected to be needed |
| Nozzle diameter (assumed) | 0.4mm |
| Recommended infill | 15–20%, 3+ wall loops (not separately confirmed by the user — reasonable default; PLA/PLA+ at this infill is adequate given the keyhole is now the primary load-bearing point and has its own local reinforcement) |
| Layer height | Not specified by the user — 0.2mm is a reasonable standard PLA default if none is set in the slicer |
| Bed fit | 234×230mm footprint vs. the user's P2S 256×256×256mm bed — clears with margin on every axis |

## FDM print-fit flags (unverified against real hardware/print)

- **Keyhole screw/anchor fit is not oversized for shrinkage compensation** — the head diameter
  (9.3mm) and shank widths (3.75/3.90mm) are used as-measured, with no FDM shrink allowance added.
  Check fit against the actual wall screw/anchor on the first print — if FDM shrinkage makes the
  hidden deep layer too tight for the real screw head to travel its full path, or the shallow layer
  too tight for the shank, this is the first thing to check.
- **Keyhole mechanical design has been verified geometrically** (all 5 checks in the keyhole section
  above pass, both slots, dense path coverage) but has **not been physically print-tested**. With
  the panel printed front-face-down (Z=0 on the bed), the shallow narrow layer prints first with no
  overhang concern; the solid material capping the hidden deep layer from above (starting at
  Z=3.5mm) has to bridge across the ~9.3mm-wide deep-layer void — a modest, typically-printable
  bridge span for PLA without supports, but worth a visual check on the first print given this is a
  small, somewhat intricate feature at this scale. Recommend a test print of just the keyhole region
  with a real screw before relying on this for a load-bearing hang.
- **Channel width (29mm) is not print-tested** against a real wand shaft at this exact size — check
  on the first print.
- Everything else (corner radius, rib/back-wall dimensions, base hollow) is structural/cosmetic, not
  a tight-tolerance mating dimension, so no shrink compensation was considered necessary.

## Export mesh quality (STL/3MF tessellation) — build-process correction, not a geometry change

A real bug was found and fixed (`dot_pipeline/specs.md` §31): every 3MF export this project has
produced omitted an explicit `meshRefinement` setting, silently defaulting to **Medium** quality
(0.1615mm surface tolerance, only 4 facets across each 90° corner-fillet arc) instead of matching
the STL export's explicit **High** quality (0.0404mm tolerance, 14 facets). At Medium quality, the
facet immediately adjacent to each corner's tangent point was measurably angled (~11.25°) away from
the flat wall it should blend into — not a real geometric defect (the underlying BRep was directly
verified perfectly tangent, 0.0000° normal deviation, at all 4 corners, including the trimmed top
two — see specs.md §31.2) but a real tessellation artifact, consistent with a reported visible
bulge/ridge line at the corners on physical prints (present on both this design and the unrelated,
structurally different `v4`, which shares nothing but this same export-script omission).

**Fixed**: `meshRefinement` is now explicitly set to High for the 3MF export too, matching STL. The
3MF's corner-fillet tessellation now exactly matches the STL's (0.0404mm tolerance, 14 facets per
90° arc — verified directly, not assumed). Geometry itself is completely unchanged — same 747.4789
cm³, same 186 faces, same body, confirmed identical before and after this fix.

| Export | `meshRefinement` | Surface tolerance | Facets per 90° corner arc |
|---|---|---|---|
| STEP | N/A (exact BRep, no tessellation) | N/A | N/A |
| STL | High (unchanged — always correct) | 0.0404mm | 14 |
| 3MF | **High (fixed — was defaulting to Medium)** | **0.0404mm** | **14** |

## Files

| File | Contents |
|---|---|
| `step/cat-toy-holder-v5.step` | Current state (this document), re-editable |
| `3mf/cat-toy-holder-v5.3mf` | Current state, with print metadata, **now exported at High mesh quality** (see above — previously silently at Medium) |
| `stl/cat-toy-holder-v5.stl` | Current state, universal fallback, High mesh quality (unchanged) |
| `step/cat-toy-holder-v4.step`, `3mf/cat-toy-holder-v4.3mf`, `stl/cat-toy-holder-v4.stl` | Superseded prior major revision (round through-holes on the wrong axis — known defect, kept only for reference) — see `dot_pipeline/specs.md` §13. The source Fusion body (`Cat Toy Holder v4 (rebuild)`) was deleted from the live document by the user during cleanup (§29.1); these exported files are now the only remaining record of it. |

All three v5 files were re-exported after the current state (final keyhole mechanism confirmed
working on a real print, §27; 5mm corner fillet, §28; panel widened 232→234mm with thicker end
walls, §29; base-band print-quality reinforcement webs, §30; 3MF mesh-quality build-process fix,
§31); they reflect the volume and dimensions in this document (747.4789 cm³, geometry unchanged by
§31), not any earlier state. The keyhole mechanism went
through four earlier same-day rejected/corrected attempts before landing on its current design (a
sealed backing pad, a full through-cut into the interior hollow, a shallow pocket with a
bottlenecked narrow shaft, and a shallow pocket widened to head-diameter with no retaining shelf) —
the current design is a genuine two-layer mechanism (narrow visible shelf layer + hidden
head-width travel layer beneath it), built directly from a reference parametric keyhole generator's
source code. See `dot_pipeline/specs.md` §§23–31 for the full story if useful.
