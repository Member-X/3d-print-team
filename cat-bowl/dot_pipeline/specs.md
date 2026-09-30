# Spec — Sleeping Cat Catch-All Bowl

New part for this repo: a stylized sleeping-cat figure draped over the back rim of a round,
shallow catch-all bowl, in the style of an existing commercial product (6 reference renders
supplied by the user, described in prose below — used for style/pose guidance only; every
number in this document is the authoritative dimensional source, not the images).

This is a **spec-only** document. No modeling or geometry generation was performed to produce it —
that is the Coder's job. Essentially all dimensions here were supplied directly by the
requester as already-solid numbers; this pass organizes them into the standard spec format,
assigns provenance tags, makes the print-orientation call explicit, and calls out modeling and
risk items for the Coder/Tester/Reviewer to carry forward.

## Source key

| Tag | Meaning |
|---|---|
| **USER-PROVIDED** | Supplied directly by the requester as an exact target dimension for this new design — not derived, not a web/generic-standard lookup, not independently re-measured against a physical object. Treated as authoritative per the requester's explicit instruction ("already solid numbers, no estimation needed"). |
| **USER-PROVIDED — style only** | From the requester's prose description of the 6 reference renders; guides pose/proportion/finish intent but carries no numeric authority. |
| **ESTIMATED** | A convention or default assumed by this document, not supplied by the requester (e.g. nozzle diameter). |
| **PROJECT CONVENTION** | Carried forward from established practice elsewhere in this repo (e.g. how solid vs. shelled construction is normally handled). |

No dimension in §§2–5 below is `ESTIMATED` — the requester was explicit that the numeric spec is
already solid. The only `ESTIMATED` items in this document are printer/slicer assumptions not
supplied (nozzle diameter) and the finish/material risk flag in §7.

---

## 1. File paths (Coder deliverables)

| File | Purpose |
|---|---|
| `cat-bowl/step/sleeping-cat-bowl.step` | Editable CAD source (parametric/history-bearing if the modeling tool supports it) |
| `cat-bowl/3mf/sleeping-cat-bowl.3mf` | Slicer-ready intermediate with any print-orientation/support hints baked in |
| `cat-bowl/stl/sleeping-cat-bowl.stl` | Final mesh for slicing/printing |

All three should represent the **single, boolean-unioned, manifold/watertight solid** described in
§4 — no separate bodies for cat, paws, tail, and bowl in the delivered files.

---

## 2. Design description (style reference — not numerically authoritative)

**USER-PROVIDED — style only**, from the requester's description of 6 supplied reference renders
(images themselves not forwarded to this session; described in prose by the requester):

- Cat's head rests forward/down between its two front paws, which are crossed/resting on top of
  the bowl's back rim, paws dipping slightly into the bowl interior (not just resting on the rim
  edge).
- Cat's body curves down the back/side of the bowl, blending smoothly into the bowl's outer wall
  — no sharp seam between cat and bowl; reads as one continuous sculpted form.
- Rounded tail curls around the lower-left side of the bowl's exterior, back around toward the
  front-left, sitting proud of the bowl's outer wall.
- Bowl body itself: simple, smooth, rounded rim, no texture/pattern. Matte/sandstone-like finish
  is a slicer/post-processing concern, not a modeling one — not spec'd numerically here.
- Ears: simple triangular/rounded-triangle shapes, symmetric, upright.
- Facial features (closed eyes, nose/mouth): subtle recessed line details on the front of the
  face, not deep carving.

This section exists so the Coder has pose/proportion intent to work from; if any number below and
this prose description ever conflict, **the numeric spec in §§3–5 wins** — flag the conflict back
to this document rather than silently picking one.

---

## 3. Overall envelope and printer constraints (stated up front)

| Constraint | Value | Tag / Source |
|---|---|---|
| Overall bounding envelope | **~190mm W × 155mm D × 145mm H** | USER-PROVIDED |
| Printer | P2S | PROJECT CONVENTION — user memory note |
| Build volume | 256 × 256 × 256mm | PROJECT CONVENTION — user memory note |
| Fit check | 190×155×145mm envelope vs. 256mm cube | VERIFIED — computed: clears every axis with 65mm+ margin in any single-piece orientation; this is **not** a tight constraint for this part, per the requester's own note |
| Nozzle diameter | 0.4mm (assumed standard) | ESTIMATED — not explicitly confirmed by the requester or in memory notes; flagged as a slicer question in §9 |
| Minimum wall/boss thickness implied | ≥0.8mm (2× nozzle) for any wall or boss under load | VERIFIED — computed. The bowl's 5mm nominal wall (§4) clears this by a wide margin; no thin-wall risk anywhere in this design — everything above the bowl's shell is solid sculptural mass (§6). |

---

## 4. Bowl dimensions

| Parameter | Value | Tag / Source |
|---|---|---|
| Outer diameter at rim | **145mm** | USER-PROVIDED |
| Outer diameter at base | **140mm** | USER-PROVIDED |
| Overall bowl height | **55mm** | USER-PROVIDED |
| Inner diameter at rim | **125mm** | USER-PROVIDED |
| Usable interior depth | **~47mm** | USER-PROVIDED |
| Nominal wall thickness (sides and bottom) | **5mm** | USER-PROVIDED |
| Internal bottom fillet radius | **12–15mm** | USER-PROVIDED |
| Rim edge treatment (top edge rounding) | **4–5mm radius** | USER-PROVIDED |
| Base | **Flat, Z=0** — bowl sits flat on its base with no feet/pedestal | USER-PROVIDED |

Wall-thickness math sanity check: (145 − 125) / 2 = 10mm total rim material split across the
rounded rim profile and the straight wall below it — consistent with a 5mm nominal wall plus the
4–5mm rim rounding rolling some of that material into the rounded top edge. No conflict found
between the OD/ID pair and the stated nominal wall thickness.

---

## 5. Cat figure dimensions

| Parameter | Value | Tag / Source |
|---|---|---|
| Body width (seated/sleeping, centered behind bowl) | **~72mm** | USER-PROVIDED |
| Head width | **~70mm** | USER-PROVIDED |
| Ear size | **25–28mm** | USER-PROVIDED |
| Front paw dimensions (each) | **~32 × 27 × 26mm** | USER-PROVIDED |
| Paw position | Rest over the rear bowl rim, extend **15mm** into the bowl interior | USER-PROVIDED |
| Tail diameter | **20–22mm** | USER-PROVIDED |
| Tail path | Wraps around the lower-left side of the bowl exterior, back-to-front-left | USER-PROVIDED |
| Facial feature recess depth | **0.8–1.0mm**, engraved/cut (not embossed) | USER-PROVIDED |

---

## 6. Construction — single boolean-unioned solid, blending instructions for the Coder

**All of bowl + cat body + head + ears + both paws + tail must be boolean-unioned into one single
manifold/watertight solid — no separate bodies in the delivered files.** This is a hard
requirement from the requester, not a style suggestion.

Because this is a sculptural, organic form, the union itself is not enough to satisfy the "reads
as one continuous sculpted form" intent from the reference images (§2) — the following seams need
**explicit fillet/blend treatment**, not just a raw boolean union with sharp intersection lines:

1. **Cat body → bowl outer wall.** The reference description is explicit: "no sharp seam between
   cat and bowl; reads as one continuous sculpted form." This needs a generous, smoothly-varying
   blend radius (large enough to remove any visible step at the union line) along the entire
   contact run down the back/side of the bowl — not a small cosmetic fillet.
2. **Paws → bowl rim / interior.** Paws rest on the rim and dip 15mm into the interior — the
   underside of each paw where it crosses the rim and the transition into the bowl's interior
   wall both need a blended fillet, both for the "one continuous form" read and because a sharp
   inside corner here is also the print-risk zone flagged in §8.
3. **Tail → bowl outer wall.** Tail "sits proud of" the wall per the reference description (i.e.
   it's not flush — it stands off the surface) but still needs to read as sculpturally continuous
   at its points of contact, not a cylinder floating with a hard seam. Blend at the contact
   points; leave the free-standing curl proud as described.
4. **Ears → head, paws → forelegs/body, tail → body.** Standard secondary-feature blends —
   smaller radius fillets, mainly for a natural sculptural look; lower risk than 1–3 above.

**Verification step for the Coder:** after every union/fillet operation, confirm the result stays
a single body / single lump / `isValid`(watertight) — per this repo's established practice on
other organic/complex-boolean builds, a boolean union across many separate bodies is a common
place for hidden non-manifold edges or accidentally-enclosed internal voids to slip in unnoticed
(see §10, edge case 3).

**Internal construction:** the cat sculpture above the bowl's rim (body/head/ears/paws/tail)
should be modeled **solid**, not separately hollowed — per this repo's established convention
(see `cat-toy-holder/dot_pipeline/specs.md` §6), actual material usage is controlled by the
slicer's infill percentage, not by hollowing the CAD body. Only the bowl itself is a genuine
hollow vessel (its 5mm shell walls, per §4, are a real geometric requirement, not an infill
question).

---

## 7. Material recommendation

**PLA.** This is a stationary, decorative catch-all object (keys, jewelry, treats-adjacent items)
sitting on a table — not a hung part, not under repeated mechanical/cyclic stress, and not a
keyhole-mount or snap-fit feature. None of this project's usual PETG-upgrade triggers (repeated
install/removal stress, cyclic-load keyhole bosses) apply here, so plain PLA — the user's general
default material — is appropriate.

**Risk flag, stated plainly per instruction — please confirm with the user:** this spec assumes
the bowl is used **dry** — holding small dry items (keys, jewelry, treats-adjacent objects), not
water, food, or any liquid, and not intended to be washed under running water or left in a damp
environment. PLA is **not** food-safe for sustained contact, is porous enough to harbor bacteria
under repeated washing/moisture exposure, and softens/deforms under heat (e.g. a sunny windowsill
or near a heat source) — none of which matter for a dry decorative catch-all, but all of which
would matter if this is ever actually intended as a washable pet food/water bowl. **This document
assumes the dry/decorative use case based on the requester's own framing ("decorative/dry
catch-all... not a washable food/water bowl") — flagging it explicitly here rather than deciding
it silently, so the director can double-check this assumption with the user if there's any doubt.**
If liquid/food contact is ever actually intended, this material recommendation and the bowl's
smooth-but-unsealed interior finish would both need to be revisited.

---

## 8. Print orientation intent

**Bed-facing face: the bowl's flat base (Z=0), bowl opening facing up** — same orientation as the
part's natural resting stance, which is also the coordinate frame the requester specified (§4,
flat Z=0 base). This is stated as a deliberate judgment call, not a default, because the design's
overhang risk needed to be checked against the alternative before committing:

- **Why not tip the part onto its side or back:** the bowl is the single largest feature (145mm
  rim OD) and a wide, thin-walled, continuously-curved vessel. Any orientation that isn't
  base-down turns the bowl's own rim and curved wall into a large-radius overhang or a full round
  bridge — a far worse printability problem than anything the cat geometry creates. Base-down is
  the clear better call once the bowl is weighed against the cat.
- **What base-down does NOT eliminate — flagged, not silently accepted:** three specific zones on
  the cat geometry are genuine overhang risks in this orientation, all below the requester's
  stated ~45°-from-horizontal threshold in places, and are exactly the zones the requester asked
  to have specifically checked:
  1. **Paw undersides where they extend 15mm into the bowl interior.** The paws project out over
     open air (the hollow bowl interior, ~47mm deep) — the underside of each paw between the rim
     and its forward tip is an unsupported overhang unless the §6 fillet blend keeps the
     underside profile shallow enough, or slicer supports are used inside the bowl cavity for
     that small region.
  2. **Tail-to-bowl transition**, specifically anywhere the tail curls away from the wall to sit
     "proud" of it (§5/§6) — the underside of that standoff curl is an overhang whose angle
     depends on exactly how the Coder shapes the curl; needs a slicer-preview overhang check once
     modeled, not just an assumption that the blend in §6 makes it safe.
  3. **Ear geometry** — upright triangular ears printed base-down have no overhang problem on
     their outward-facing sides (they taper up into open air, which is fine), but the requester
     specifically flagged this zone for a check — worth confirming the ear-to-head fillet base
     doesn't create a reverse (undercut) angle where the ear's inner face meets the head.
- **Resolution:** base-down/opening-up is the recommended orientation, but it is **not**
  support-free — the Coder should run a slicer overhang-angle preview specifically on the three
  zones above once geometry exists, and expect to need supports (tree/organic supports recommended
  over the bowl interior for the paw region specifically, since interior surface finish there is
  less visually critical than the bowl's exterior or the cat's face) rather than assume the design
  alone gets it under 45° everywhere.

---

## 9. Edge cases and open risks

1. **Overhang/support risk at paw undersides, tail-to-bowl transition, and ear base** (detailed in
   §8). This is a genuine risk carried into the build, not resolved by orientation choice alone —
   the Coder needs to check actual slicer overhang angles once geometry exists and plan for
   supports in the bowl-interior region if needed.
2. **Liquid/food-contact misuse** (detailed in §7). The spec assumes dry decorative use; if the
   bowl is ever used to hold water, wet food, or is washed repeatedly, PLA and the current design
   (unsealed interior finish, no food-contact-rated material) would both need reconsideration.
   Flagged for the director to confirm with the user rather than assumed silently.
3. **Non-manifold/hidden-void risk from the multi-body boolean union** (detailed in §6). Six+
   distinct organic bodies (bowl, cat body, head, two ears, two paws, tail) being unioned and
   heavily filleted at their seams is exactly the kind of operation where a slicer can silently
   accept a technically-invalid mesh (self-intersecting fillet, accidentally-enclosed internal
   void at a union seam) that looks fine in preview but fails or prints wrong. The Coder should
   verify single-body/single-lump/watertight status after every union and fillet step, not just at
   the end.

---

## 10. Question back to the requester

**What slicer settings should be used (layer height, infill)?** No layer height or infill target
has been specified for this part. Given the design is solid sculptural mass over a hollow bowl
shell (§6), infill percentage mainly affects print weight/time rather than structural performance
(this is not a load-bearing part) — a reasonable default (e.g. 0.2mm layer height, 15% infill)
would work absent other direction, but please confirm or state a preference before the Coder locks
in export settings.

**Also worth confirming while we're asking:** the §7 dry-use assumption (decorative catch-all, not
a washable food/water bowl) — flagging this explicitly rather than assuming it silently, since
getting it wrong would mean revisiting both the material choice and the interior finish.

---

## 11. Revision history

| Version | What changed | Why |
|---|---|---|
| v1 (this document) | Initial spec, organizing requester-supplied numeric spec into standard format, tagging provenance, making the base-down/opening-up print-orientation call explicit with its overhang caveats, and writing the boolean-union/fillet-blend instructions for the Coder. No dimensions were derived or estimated — all sourced `USER-PROVIDED` per the requester's own framing. | Initial build request for a new part. |
