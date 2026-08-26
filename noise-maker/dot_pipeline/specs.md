# Spec — Noise Maker: Handle + Clacker (REWRITTEN 2026-08-25, replaces all prior wishbone/gear-wheel content)

> **This file replaces the entire prior revision history (v1 through v4.2).** The previous document
> tracked a design investigation that went through a misidentified-reference detour (wishbone blade +
> external gear wheel + living-hinge pawl, based on a *different* commercial product) before landing on
> the design described below. None of that history is reproduced here — see git history / the prior
> version of this file if that trail is needed. This is a **clean restatement of the actual current
> design**, sourced from the live Fusion document "Noise Maker Parts v2" plus this session's own
> screenshot/geometry verification.
>
> **`dot_pipeline/parameters.md` is ALSO now out of sync with the live document and should not be
> treated as current** — flagged explicitly, not silently worked around. Its "CURRENT — Handle +
> Clacker rebuild" section describes a *fully parametric* Clacker (plain circular bore, engineered
> flex tang) that has since been abandoned in favor of going back to the **original mesh-derived
> Clacker body** (hex-faceted bore, real flex tang) paired with a **newly-rebuilt parametric Handle**.
> The trimesh/boolean-intersection verification numbers in `parameters.md` (0.57mm³ residual overlap,
> 1.26mm minimum clearance, 3.0mm diametral bore clearance) apply to that **abandoned parametric-Clacker
> pairing**, not the live design — do not quote them as current-state verification. See §6.

## 0. What this object is

A two-part **print-in-place** ratchet noisemaker (classic "football rattle" / gragger mechanism),
printed together in one job, never separated and reassembled by hand.

- **Handle** — the shaft the user grips. Live Fusion: occurrence `HandlePart:1`, component
  `HandlePart`, single BRepBody `Handle`. This is the part actively being modified this session.
- **Clacker** — the forked loop body that spins freely around the Handle's mechanism end and produces
  the click. Live Fusion: root-level mesh body `Noise Maker Separated - Clacker (1)`. **Unchanged,
  original, already-functional geometry — explicitly out of scope for modification** ("there is no
  need to modify that... The handle is what I want modified... It should fit and operate the same").

Ignore in the live document: `Noise Maker Separated - Handle` (old original handle, hidden, kept only
as fallback reference), `ClackerPart:1` (rejected rebuild attempt, hidden), `PrintInPlaceAssembly:1`
(empty leftover). Also ignore `noise-maker/Noise Maker v2.stl` (project root) and everything currently
in `noise-maker/stl/` and `noise-maker/3mf/` and `noise-maker/step/` as **stale exports that predate
this session's Handle edits** (retention bumps, tooth growth, diameter increase — see §3) — none of
the files on disk reflect the current live geometry. `noise-maker/reference/ref_*.jpg` images are also
stale, from the abandoned wishbone-reference investigation — not authoritative for this design.

## 1. Geometry, by Y-station (Fusion internal cm units; long axis = world Y)

Shared rotation axis center: cx=7.6985cm, cz=9.8222cm (world X,Z). Handle spans Y=0 to Y=19.051cm.

| Y range (cm) | Feature |
|---|---|
| 0 – ~4.353 | **Mechanism head**: hex-profile tip at/near Y=0 (passes through the Clacker's hex collar bore — confirmed **decorative/non-keyed**, needs rotational clearance only, not a precision mating feature) + gear-tooth ring (this session: radial reach +0.5mm, axial length +4mm — see §3) |
| ~4.4 – 5.6 (peak 5.0) | **6 new cone-shaped retention bumps**, 60° apart, ~4mm base → ~0.3mm point, added this session (replacing an earlier sphere-shaped version, changed specifically for printability — see §4) |
| 4.353 – 19.051 | **Knurled/contoured grip shaft** (twist removed this session, replaced with knurl texture) |
| ~17.6 – 19.051 (approx, top of grip) | Rounded, hex-faceted decorative dome/pommel cap — confirmed by visual inspection (screenshots) to be a **separate, purely cosmetic** feature at the opposite end of the shaft from the Y=0 mating hex tip. Do not conflate the two — see §7 for a note on how easily this gets confused. |

Overall Handle diameter increased +0.5mm uniformly (all faces) this session, on top of the above.

**Clacker** (unchanged): fork/loop spanning world Y=0–4.353cm. Two thin collar walls (~3mm thick)
with a hex-shaped bore (radius ~23.5–23.9mm depending on facet angle) at Y≈0.1–0.5cm and Y≈4.0–4.3cm,
joined by an **open** forked middle (Y≈1.0–3.5cm, confirmed via screenshot — this is a genuine open
channel/trough, not a closed tube) where the flex tang lives and catches the gear teeth as the Clacker
rotates.

## 2. Print orientation

Whole assembly prints standing upright along Y (Handle's grip end down on the bed), per explicit user
direction. Envelope (from the most recent verified print-in-place export, pre-dating this session's
edits, so treat as approximate): roughly 180mm × 76mm × 190mm — comfortably inside the 256×256×256mm
P2S bed. This session's dimensional growth (+0.5mm diameter, +0.5mm tooth reach, +4mm tooth length) is
small relative to bed margin and does not change this conclusion.

## 3. This session's changes to the Handle (what actually needs testing)

1. Gear-tooth ring: radial reach +0.5mm, axial length +4mm.
2. 6 cone-shaped retention bumps added (sphere → cone, printability-motivated).
3. Overall diameter +0.5mm, uniform.
4. Twist removed from the grip, replaced with knurl/contour texture (carried over from earlier in the
   project, not new this session, but part of the same "replace the Handle" scope).

## 4. Material

Default is PLA (user's standing printer default, P2S/256mm bed). The Clacker's flex tang is a
repeatedly-cyclic-load flex feature (every ratchet click flexes it) — **this is exactly the class of
feature this team's own material-check policy calls out as a PLA brittleness risk.** See `tests.md` §5
for the concrete recommendation.

## 5. ESTIMATED / unresolved dimensions — do not treat as closed by default

Per this team's QA policy, anything tagged ESTIMATED that mates with the part's own physical
counterpart must be verified or explicitly risk-accepted before it's treated as resolved. Flagging
here, resolved further in `verdict.md`:

- **Clacker bore/collar radius (~23.5–23.9mm hex, varying by facet angle)** — sourced from
  point-containment/ray-cast probing of the original mesh body this session (an improvement over the
  even coarser 573-vertex Tinkercad-export sampling used earlier in the project, per `parameters.md`),
  but still not a caliper-verified, ground-truth number off the physical original part. The new
  Handle's mechanism-head, tooth-ring, and retention-bump dimensions are all sized against this number.
- **Retention-bump radial interference (0.6–1.0mm, varies by hex facet)** — explicitly called an
  approximate bound by whoever ran the check, not an exact figure ("I did not get an exact mm figure").
- **Free axial play before the retention stop engages (~4–7mm)** — same caveat, explicitly approximate.

None of these are being silently accepted here — see `verdict.md` for the recommended resolution path.

## 6. What has and hasn't been verified for the CURRENT pairing

**Verified this project (against the abandoned parametric-Clacker pairing, NOT the live design —
historical context only):** watertight/manifold on both bodies, 0.57mm³ residual tooth/tang overlap
(judged acceptable), 1.26mm global minimum clearance, print-in-place export fits the build volume.

**Verified against the ACTUAL current pairing (new Handle vs. original mesh Clacker), per the main
session's direct point-containment/ray-cast checks this session:** zero solid overlap at rest;
retention-bump-vs-collar-wall interference is geometrically real and rotation-independent (full closed
collar ring vs. 6 discrete bump lobes); the free-play distance to the retention stop is well short of
the distance to the teeth/tang zone, so no rubbing-against-teeth failure mode was found.

**NOT yet verified for the current pairing, flagged as a real gap, not an oversight to gloss over:**
whether the +0.5mm/+4mm tooth-ring growth still meshes cleanly with the Clacker's *actual* flex tang
without binding/jamming during ratchet operation. The only tooth/tang collision check on record
(0.57mm³ residual, from `parameters.md`) was against the old parametric tang design and the pre-growth
tooth size — it does not cover this session's enlarged teeth against the real original tang. See
`tests.md` §3 and `verdict.md`.
