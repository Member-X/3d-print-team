# Pet Memorial Urn (Large)

A two-part memorial urn for pet cremated remains, sized for the top of a 50–90 lb pet weight
range (~90 lb), with a flat resting-cap lid closure (no built-in magnets/hardware, see below) and
an open-loop carry handle.

## What it is

- **Body** — a single smooth, rounded "ceramic vase" silhouette (wide low belly, tapering
  through a shoulder into a narrow neck), plain on all sides (no engraving/plaque — a hard
  design constraint), holding **≈1579 cm³ (≈96.3 in³) internal capacity** — sized against the
  requester's own rule of thumb (1 in³ of internal volume per lb of pet body weight, at the top
  of the stated 50–90 lb range) and now comfortably *exceeding* that ≈1475 cm³ minimum target
  by design (see "Design evolution" below and `parameters.md` for the full story of how and why).
- **Lid** — a domed cap with a flat brim that rests on the body's flat collar rim (no plug/skirt
  — deliberately, for the best possible print orientation and a flush seat), topped by an
  open-loop bail handle sized for a single fingertip.
- **Closure — flat seating only, no built-in hardware.** The lid's flat underside simply rests
  on the body's flat 78mm-OD collar rim; there is no magnet, latch, or any other closure feature
  modeled into either part. Not airtight (not needed — the crematorium's remains are already in
  their own sealed bag). An earlier version of this design had 3+3 magnet pockets (6mm × 2mm N42
  discs on a 34mm bolt circle); the user decided to handle any magnet placement themselves at
  print time (slicer pause-and-embed) or after printing (drill-and-glue) instead, so those
  pockets were removed from the CAD (2026-08-28). The pre-removal files are preserved at
  `archive/v2-with-magnet-pockets/` — see `parameters.md` §3/§9 for the full story.
- **Handle** — an open-loop bail (not a blind cavity), sized so any support material printed
  inside the loop can be removed afterward.

Body and lid are separate printed parts — not printed in place, not glued together. The lid
lifts off by hand.

## Design evolution — why the capacity grew past the original target

The body was originally derived to hit ≈1475 cm³ (90 lb × 1 in³/lb) and, once built, first
measured out to ≈1512 cm³ (+2.3%, still within the spec's own ±5% routine-tolerance band). Since
then, the user made a direct, deliberate manual edit to the body's outer belly in Fusion to make
it visibly fuller — an aesthetic choice, explicitly kept rather than reverted. That left the
inner wall not tracking the new outer wall (uneven thickness); the user then had the inner wall
reworked to track the fuller outer wall at a constant ~4mm offset, matching the wall-thickness
approach used everywhere else in the body, rather than thinning the wall further just to force
the volume back down. The result — **≈1579 cm³, +6.85% over the original minimum target** — is
the accepted, explicit consequence of that sequence of choices, not a defect. It's also a
*more*, not less, generous capacity for the same 50–90 lb market segment the urn was always sized
for. Full numbers and verification: `parameters.md` §1–§2, §10.

**Honest visual note:** the bigger belly, on the same neck/collar as before, now reads more
pinched/"ginger jar"-like against the original concept photo (`concept/concept-v2.png`) than the
earlier build did — an incremental change layered on top of an already-disclosed "banded collar"
drift from the concept's fully continuous neck curve (the collar's flat, constant-radius band is
needed as a robust lid-seating surface). Both features the concept calls load-bearing to the
design's identity — the plain body and the open-loop handle — remain fully intact. This was a
deliberate, informed choice at each step, not something that crept in unnoticed; a quick visual
check-in with the requester (new render vs. concept image) is a reasonable courtesy before
calling this fully final, not because the geometry needs to change.

## Files

| Path | Contents |
|---|---|
| `step/urn-body.step`, `3mf/urn-body.3mf`, `stl/urn-body.stl` | Current body — fuller belly, rebalanced ~4mm wall, and neck-to-collar crease fix (2026-08-28, spec v4); magnet pockets removed (2026-08-28, spec v3) |
| `step/urn-lid.step`, `3mf/urn-lid.3mf`, `stl/urn-lid.stl` | Current lid — unaffected by the v4 belly edit; magnet pockets removed 2026-08-28, otherwise unchanged since its original build |
| `archive/v2-with-magnet-pockets/` | Superseded body + lid STEP/3MF/STL from before the 2026-08-28 magnet-pocket removal, preserved unmodified — not the current print files, kept for reference only |
| `archive/pre-v4-belly-render/pet-memorial-urn-hero.png` | Superseded hero render, from before the v4 belly-fullness edit — preserved for reference, not the current design's appearance |
| `step/neck-fit-test.step`, `3mf/neck-fit-test.3mf`, `stl/neck-fit-test.stl` | Small standalone test article (just the neck + collar, ~35mm tall) — print this first to physically check a real crematorium remains bag fits through the 58mm neck opening before committing to the full ~160mm body print. Unaffected by the belly/collar edits — its represented dimensions (58mm ID, 78mm/66mm collar/neck OD) never changed. See `parameters.md` for what it does/doesn't need to be re-printed for. |
| `concept/` | Approved concept brief and reference images |
| `render/pet-memorial-urn-hero.png` | Current hero render, refreshed from the current (v4) geometry — the pre-v4 version is archived, see above |
| `dot_pipeline/` | Full planning/build/test/review history (`specs.md`, `tests.md`, `verdict.md`, `review.md`) — the detailed narrative behind every decision below, if needed |
| `parameters.md` | Full dimensional/technical reference for rebuilding or editing this design |

## Print notes

- **Material: body = matte or silk PLA, lid = PETG.** Different materials for the two parts,
  on purpose — see `parameters.md` for the reasoning (short version: the lid's handle root is
  the part most exposed to a knock or repeated grip, and PETG is meaningfully tougher there; the
  body's smooth, undecorated surfaces are what most need the matte/silk finish look, which PLA
  offers a wider selection of).
- **Orientation:** body prints base-down, opening/neck facing up (matches its natural resting
  stance, self-supporting everywhere except one named watch-item band, below). Lid prints
  flat-underside-down, dome and handle facing up (the flat underside is the seating surface — it
  gets the best possible print quality and bed adhesion printed this way). `neck-fit-test`
  prints flange-down, same self-supporting logic as the body.
- **Overhang watch-item (unchanged risk category, slightly higher number):** the only zone on the
  entire body that exceeds the conventional 45° self-supporting guideline is the neck-to-collar
  external blend, just below the rim (roughly the top ~7mm of the neck, right before the collar).
  It now peaks at **~47.25°** from vertical (up slightly from ~45.6° before the v4 belly edit) —
  same disclosed, low-risk "watch it on the first print" band as before, not a new concern: it's a
  short span on a fully closed 360° revolve, not a one-sided cantilever. A touch more cooling or a
  modest local speed reduction there is cheap insurance. The belly itself (bigger and slightly
  lower than before) was re-checked and introduces no new overhang risk anywhere.
- **Bed fit:** body ~154×154×160mm (grew from ~146×146×160mm — the belly is now bigger, see
  "Design evolution" above), lid ~100×100×75mm, `neck-fit-test` ~122×122×35mm — all clear a
  256×256×256mm bed with large margin. Printed as separate jobs, so combined assembled height is
  not a constraint.
- **Slicer settings are not embedded in any exported file** — set manually: 0.16–0.2mm layer
  height, 15–20% infill (both a reasonable default, not yet explicitly confirmed by the
  requester — see `dot_pipeline/specs.md` §11), plus PETG-appropriate temperature/cooling for
  the lid (hotter nozzle/bed than PLA, and a bit more cooling attention right at the dome apex
  and the neck-to-collar band on the body — see `parameters.md`).
- No magnet pockets exist in the current CAD (removed 2026-08-28), so there is nothing left to
  hole-size-verify for that feature. If you add a magnet assist yourself later (slicer
  pause-and-embed or post-print drill-and-glue), that fit is entirely yours to check — it's
  outside this CAD by design now.
- **Hole/circular-feature shrinkage:** the 58mm neck/collar ID is the one circular dimension a
  mating object (the remains bag) actually needs to clear. FDM parts typically print circular
  holes slightly undersized versus the model. No compensation has been baked into this dimension
  because there is no hard target diameter to compensate toward (§4.4 of `specs.md` — it's an
  `ESTIMATED`, untested fit against a real bag, not a hardware spec). **Check actual as-printed
  ID on the first `neck-fit-test` print** before assuming 58mm nominal is what you'll actually get.

## Status

**Approved by Reviewer**, including a fresh, independent re-verification of the v4 belly/wall/
capacity changes (business fit, geometry, and overhang — see `dot_pipeline/review.md` Addendum
3). This is the only planned size ("large," ~90 lb). A small/medium lineup has been discussed as
a future direction but is **not started** — nothing in this repo currently supports a size other
than the one built here.

**One real-world test is still outstanding, not yet closed out:** whether a real crematorium
remains bag actually fits through the 58mm neck opening. This was flagged as an untested
assumption from the start of the spec and has not been resolved by CAD review — it needs an
actual physical test (print `neck-fit-test` and try a real or mocked bag through it) or an
explicit written risk acceptance from the requester. Don't treat this project as fully
closed-out until that happens.

Five real incidents (manual/direct edits or feature-rebuild side effects disturbing the model)
were found and fixed during this build — see `parameters.md`'s incident notes (§6) if you're
editing this file further and want to avoid repeating them. All five were independently
re-verified as fully recovered; none left residual damage in the shipped files.
