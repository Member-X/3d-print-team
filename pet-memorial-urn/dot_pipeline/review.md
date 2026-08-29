# Reviewer Verdict — Pet Memorial Urn (Large, single-size build)

## APPROVED — print-ready, with one required documentation follow-up (non-blocking for print) and several named non-blocking watch items

The geometry in `step/`, `3mf/`, and `stl/` for `urn-body` and `urn-lid` is sound, independently
re-verified by me from scratch (not just re-read from `tests.md`/`verdict.md`), and matches the
approved concept well. Nothing found here reopens any of the settled Coder/Tester round-trips.
The one real gap I found that isn't already on record anywhere in this project is a **missing
top-level `README.md` and `parameters.md`** — every other completed project in this repo has
both, this one has neither. That's cheap to fix and shouldn't be skipped just because the CAD
itself is done. Full detail below.

---

## 1. Business fit — PASS

The design solves the stated problem: a memorial urn sized to the requester's own 90 lb / 1 in³-
per-lb rule (§4.1 of `specs.md`), with a genuinely liftable, open-loop lid handle and a
magnet-assisted (not airtight-dependent) closure appropriate for remains that are already
bagged. The plain, undecorated body and the loop-handle lid are the two features the concept
brief explicitly calls out as load-bearing to the design's identity, and both are intact in the
shipped files (verified independently in §3 below, not just asserted).

## 2. Technical/concept parity — PASS, independently re-verified, one honest departure named

I did not treat the chain of Coder/Tester agreement as sufficient on its own. I opened the live
Fusion document (`pet-memorial-urn`, 3 components: `urn-body`, `urn-lid`, `neck-fit-test` — no
size-variant scope creep, confirming §12's single-size constraint) and independently re-measured
the shipped `stl/urn-body.stl`, `stl/urn-lid.stl`, `3mf/urn-body.3mf` via `trimesh`, using my own
script, not the Tester's. Results, cross-checked against `tests.md`'s claims:

| Check | My independent measurement | Tester's claim | Match |
|---|---|---|---|
| Belly position | peak radius **73.0000mm at exactly z=72.0mm** (45.00% of 160mm), single clean symmetric peak | 73.000mm @ z=72.0mm, 45.00% | Exact |
| Base cleanliness (the historically-defective feature) | 0.1–5mm z-sweep: single boundary loop, **zero interior holes**, at every sampled height, in both STL and re-confirmed via collar cross-section area math | Clean, 77/136 vertices at uniform 49mm radius | Confirmed independently, different method |
| Collar magnet pockets | cross-section area drops by ~90.1mm² exactly at z=157.8mm (3 × π×3.1² ≈ 90.6mm²) — 3 pockets, correct size/depth | 3× 6.2mm dia, 34mm bolt circle, 2.2mm deep | Confirmed independently, different method (area-based, not vertex-based) |
| Shoulder→neck taper self-support | radius **monotonically non-increasing** at every 0.5mm step from z=119–145mm, zero increasing steps; peak local angle **54.499° at z=137mm** | Monotonic, 54.5° at z≈137mm | Exact |
| Neck-to-collar external blend | slope changes gradually across z=145–152mm (max single-step slope-jump **0.2275**), no discontinuity; peak angle **45.564° from vertical** | Smooth S-curve, largest step ~0.23, peak ~45.6° | Exact — the fix is real, not re-asserted |
| Plain-body / no engraving | radial std-dev **0.001–0.007mm** at 7 heights (z=20–130) — essentially perfect circles | 0.23–0.30mm (STL-facet-noise-limited method) | Confirmed, more tightly than the original test |
| Handle open-loop | 2 boundary loops (a hole) present at y=−4mm to +4mm, 1 loop (solid) outside that range | Same window (y=−4 to +4) | Exact |
| Body/lid material volumes | 293.14 cm³ / 150.82 cm³ (mesh) | 293.14 cm³ / 150.82 cm³ | Exact |

I regard this as a genuine, from-scratch re-derivation (I hit and fixed my own methodology bug
along the way — an unconverted local-frame projection that initially gave a false 75mm belly
radius — which is exactly the kind of thing a fresh pass is supposed to catch), not a rubber
stamp of the pipeline's own numbers.

**Concept-fidelity spot-check, done independently rather than accepted on the Tester's
"looks consistent" read:** I pixel-measured `concept/concept-v2.png` directly (edge-traced the
jar's silhouette against its background) — the belly reads as sitting roughly mid-height to
slightly-below-mid-height in the photo, consistent with (not contradicting) the low, wide belly
the exact 45%/z=72mm geometry produces. Photo-edge-detection on a textured, softly-lit product
photo has real error bars (my own estimate lands in a 45–50%-up-from-base band, not a single
precise number), so I'm treating the Tester's exact 3D ray-cast (73.000mm/45.00%) as the
authoritative figure and the photo check as corroborating, not competing, evidence.

**One honest, fresh finding — a real but small concept departure, not previously named this way:**
comparing a live Fusion screenshot of `urn-body` side-by-side against `concept-v2.png`'s own
neck/rim close-up, the built model's neck-to-collar area reads as a distinctly **banded,
partially-cylindrical rim** (the 15mm-tall constant-radius collar, required to give the magnet
pockets a flat home, per spec §6.2) where the concept shows one **continuous, softly rolling
curve** with no comparable straight/cylindrical segment. The recent blend-smoothing work
(R9/R21 in `tests.md`) fixed the *sharp-kink* version of this problem, and it's genuinely fixed —
but even the smoothed version is still a visibly more "banded" rim than the concept's fully
organic silhouette. This is a disclosed, functionally-necessary tradeoff (the magnet pockets
need a flat, constant-thickness wall under the lid's flat seating plane), not an oversight, and
it still plausibly reads as "a rim reinforcement detail on a ceramic vessel" — I'm not blocking
on it, but I want it named explicitly as a real, if minor, visual drift from the signed-off
reference, per the instruction not to silently wave through drift. **The lid, by contrast, is an
excellent match** — dome proportions, brim overhang, and open-loop handle shape all track
`concept-v2.png`'s lid close-up closely.

## 3. Hard constraints — all three independently reconfirmed, not re-read from prior passes

1. **Plain/smooth body, no engraving/plaque/text anywhere.** Reconfirmed via my own radial
   cross-section analysis at 7 heights spanning base to neck (table above) — deviation is
   essentially zero (mesh-tessellation-level noise only), no trace of a plaque or recessed panel
   anywhere I sampled. **Confirmed.**
2. **Handle is a genuine open through-hole loop, not a blind cavity.** Reconfirmed via my own
   y-axis cross-section sweep of `stl/urn-lid.stl` — a real hole (2 boundary loops) exists from
   y=−4mm to +4mm and vanishes (1 loop, solid) immediately outside that band. **Confirmed.**
3. **Single-size build, no variant scope creep.** The live Fusion document contains exactly 3
   components (`urn-body`, `urn-lid`, `neck-fit-test`) — no hidden/alternate-size bodies or
   duplicate scaled components anywhere in the document. **Confirmed.**

## 4. Overhang angles — independent assessment, not a rubber-stamp of the chain of agreement

Per the specific request for my own fresh take:

- **Shoulder-to-neck internal taper (locally up to ~54.5°):** I agree with the self-supporting
  assessment, and I checked the actual mechanism myself rather than accepting the "shrinking
  cone" argument by description — I directly confirmed **zero locally-increasing radius steps**
  across the entire z=119–145mm span at 0.5mm resolution. Since the argument's validity depends
  strictly on the sign of `dr/dz`, not its magnitude, and the sign is confirmed negative
  everywhere in this span, I concur this transition is inherently self-supporting regardless of
  local angle. No print-support risk.
- **Neck-to-collar external blend (~45.6° peak, now a genuine smooth curve):** I independently
  confirmed this is now a real, continuous S-curve (no discontinuous jump anywhere in a 0.1mm
  resolution scan) — the earlier hard-chamfer defect is genuinely gone. My own take on the
  ~45.6° peak, arrived at independently rather than inherited: this is a few degrees over the
  conventional guideline, on a fully closed 360° revolve (not a one-sided cantilever), for a span
  of only a few millimeters at the peak — I agree this is low risk, but I'd stop short of calling
  it zero risk the way the shrinking-taper case is; it's a genuine (if narrow and shallow)
  widening-with-height transition. **Practical recommendation, stated plainly for whoever
  slices this: treat the z≈147–151mm band as a "watch it on the first print" zone — a touch more
  cooling / a modest local speed reduction there is cheap insurance, not a redesign.**
- **Neck opening (58mm) vs. a real cremation bag:** unchanged status — still an `ESTIMATED`,
  physically-untested dimension per spec §4.4, exactly as the spec itself flags it. This is a
  genuine open item, correctly not silently treated as resolved anywhere in this pipeline. It
  does not block this review (it requires a physical bag, which no CAD reviewer can supply), but
  it is carried forward below as a named, must-not-be-forgotten item, per the task's own framing
  that an `ESTIMATED` mating dimension is a review blocker if silently dropped rather than a
  non-issue if explicitly carried forward with a real plan to close it out (the `neck-fit-test`
  article exists for exactly this).

## 5. Documentation — the one real gap found in this pass

`dot_pipeline/specs.md` is excellent as a planning document (VERIFIED/DERIVED/ESTIMATED tagging
throughout, a real §13 revision history). But **this project has no `README.md` and no
`parameters.md` at the project root** — every other completed project in this repo
(`cat-toy-holder/`, `noise-maker/`, `switch-plate-covers/`, `lightswitch-cover-single/`) has both.
`dot_pipeline/*` is pipeline working history; `README.md`/`parameters.md` at the project root is
this shop's own established convention for the lightweight, durable reference a future editor or
the requester would actually reach for — known limitations, print orientation, material
reasoning, and a short parameter sheet distinct from the much longer planning narrative in
`specs.md`. Nothing here blocks the physical print (the exported files are correct and complete),
but per this shop's own completion-workflow convention this should be produced before the project
is called finished. **Required follow-up, not a print blocker.**

Two smaller, related observations from independently inspecting the files themselves:

- **Material intent is only partially captured in exported file metadata, not "not captured" as
  broadly stated in `tests.md`/`verdict.md`.** I opened `3mf/urn-body.3mf`'s raw XML directly: it
  actually does carry a `<metadata name="Description">` field with the full "Material: matte/silk
  PLA..." text (Fusion exported the component description verbatim). `3mf/urn-lid.3mf`, by
  contrast, has no such field at all — it was exported before the PETG description was written
  onto the component. Practically this changes nothing (no slicer auto-selects material from a
  free-text 3MF Description field, so "must be set manually" remains correct either way), but the
  blanket claim that material "is also not captured in any file metadata" isn't quite accurate for
  the body file specifically — worth a precise footnote rather than a repeated broad claim.
- **Minor repo hygiene:** `pet-memorial-urn/nul` is a stray leftover file (a Python traceback —
  `AttributeError: 'NoneType' object has no attribute 'to_2D'` — apparently redirected to a
  literal file named `nul` from a Windows/POSIX shell mismatch during a Tester script run). Not a
  design issue, just noise; safe to delete.

## 6. Cost — PASS, trivially cost-effective

Material-shell volumes (mesh-measured, independently): body 293.14 cm³, lid 150.82 cm³. At PLA
density (~1.24 g/cm³) the body is on the order of 300–360g of filament depending on how much of
the nominal solid volume the slicer's stated 15–20% infill actually reduces (the walls are only
4mm nominal, leaving little room for an internal infill lattice in the curved wall itself — most
of the infill percentage will only matter in the thicker floor/collar sections); the PETG lid
(~1.27 g/cm³) is on the order of 150–190g. At typical consumer PLA/PETG pricing this is roughly
**$8–12 in filament for the pair** — trivially cost-effective for a decorative memorial piece.
Print *time* for a ~160mm tall part at 0.16–0.2mm layers will be substantial (many hours), but
that's a scheduling consideration, not a material-cost one, and nothing in the geometry (no
unnecessary solid mass, no oversized infill requirement) works against it.

## 7. What's carried forward, not re-litigated, not a blocker on this review

1. **Neck-opening-vs-real-bag physical test** — the `neck-fit-test` article is sound (I did not
   re-verify it from scratch since its represented dimensions were untouched by the last several
   rounds of change and were already independently confirmed in `tests.md` R5/R16/R24). This is
   the requester's physical test to run; no CAD reviewer can close it out.
2. **Magnet fit test coupons** (PLA body pockets, PETG lid pockets) — recommended before a full
   production print, per `tests.md`. Not re-litigated here.
3. **Slicer settings must be set manually** — 0.16–0.2mm layer height, 15–20% infill, plus
   PETG-specific temperature/cooling tuning for the lid (and, per §4 above, a specific watch-item
   band at the lid's — no, at the **body's** neck-to-collar z≈147–151mm region). None of this is
   embedded in the 3MF files.
4. **PETG-for-lid tradeoffs** (magnet pocket oversize possibly tight for PETG; dome-apex cooling)
   — already well-reasoned in `tests.md` R4, not reopened here.

## 8. Final render

Produced from the actual, current Fusion geometry (not a generated image) via
`mcp__fusion__fusion_mcp_execute`: applied a custom matte tan "stoneware" appearance (copied from
the Fusion Appearance Library's `Plastic - Matte (White)` base, recolored to a warm tan
consistent with `concept-v2.png` and the spec's matte/silk PLA / sanded-PETG material call) to
`urn-body` and `urn-lid` separately, assembled the lid onto the body at its true seated height
(160mm), set the Photo Booth lighting environment plus ground shadow/ambient occlusion, and
exported a hero-angle isometric shot at 1800×2000 directly from `Viewport.saveAsImageFile`.

Saved to: `H:\ClaudeStuff\3d-print-team\pet-memorial-urn\render\pet-memorial-urn-hero.png`

Honest caveat on the render itself: a faint background reference-grid/axis overlay is visible in
the image (a Fusion viewport-chrome element I could not fully suppress via the available API —
`SketchGridOff` and disabling ground-plane/canvas effects did not remove it). It does not affect
the model, material, or lighting shown, but it is not a fully "clean" studio backdrop — flagging
this plainly rather than presenting the image as more polished than it is.

**Concept-match note on the render specifically:** the render's overall silhouette and lid/handle
proportions match `concept-v2.png`'s spirit well. The one visible difference a careful side-by-side
would show is the same one named in §2 above — the built model's neck-to-collar area is a bit more
"banded" than the concept's fully continuous curve. This is disclosed here rather than left for
someone to discover only by comparing images later.

---

## Bottom line

**Approved.** The exported STEP/3MF/STL files for `urn-body` and `urn-lid` are geometrically
sound, independently re-verified against the spec and against the concept image using my own
methods (not a re-read of prior passes), and all three hard constraints (plain body, open-loop
handle, single-size) are confirmed true in the shipped files. Two required actions before this
project is fully "done" (neither blocks printing today):

1. **Add `README.md` and `parameters.md` at the project root**, matching this shop's convention
   for every other completed project — known limitations, print orientation, material reasoning,
   and a short parameter sheet with VERIFIED/DERIVED/ESTIMATED tags and revision history.
2. Delete the stray `pet-memorial-urn/nul` debug artifact.

Everything else (neck-fit-test physical validation, magnet fit coupons, manual slicer settings,
the minor neck-to-collar "banded rim" concept drift, the ~45.6° watch-item band) is a named,
non-blocking, carried-forward item — not a reason to withhold approval.

---
---

# ADDENDUM — 2026-08-27: third manual-edit incident, post-approval — re-confirmation

## Context

This project's original APPROVED verdict above was written by a prior Reviewer instance whose
transcript is no longer accessible. Since that approval, **a third manual/direct edit occurred
in the live Fusion document** (two others — a cross-component `participantBodies` leak and a
manual sketch-drag collapsing the neck profile — happened mid-pipeline, before the original
approval, and are already covered in the review above). This third incident: a user-described
edit "near the lid magnet pocket" turned out, on investigation, to have left the **lid entirely
untouched** — the actual damage was a manual drag on the **body's** neck/collar region (collar
ID/OD ballooned from 58mm/78mm to ~70.7mm/~90.4mm), which indirectly clipped the magnet pockets
down to abnormal ~3×1.9mm cuts as the growing bore ate into the 34mm pocket bolt circle. This was
not a delegated design change — it was treated as an unintended regression and recovered by
reproducing the exact previously-verified control-point/tangent recipe (this time `Revolve1`
picked up the corrected profile cleanly — no cascade rebuild of `Extrude1` was needed, unlike the
second incident).

The Tester independently re-verified this recovery against its own prior independent numbers
(not just the Coder's math) — see `tests.md` Re-test Pass 4 (R25-R29) and the corresponding
verdict in `verdict.md`. Per every number checked there, the recovered geometry matches the
pre-incident, already-approved state exactly or to within normal mesh-resolution noise, including
several genuinely bit-for-bit-identical floating-point figures (shell volume, face/vertex counts).

## My own independent spot-check (not accepted from the Coder/Tester chain alone)

I re-measured the current `stl/urn-body.stl` (freshly re-exported, timestamp 21:35) and
`3mf/urn-body.3mf` from scratch using my own `trimesh` script, cross-checked against the
untouched `stl/urn-lid.stl` (timestamp 12:01) as a control. Full results in my message to the
orchestrating agent; summary:

- **Manifold**: watertight, single component, Euler=2, bounds identical to every prior recorded
  state (±73.0mm XY, 0-160mm Z).
- **Shell volume**: 293.1365 cm³ — bit-for-bit identical to the Tester's R25 figure.
- **Face/vertex counts**: 47,298 / 23,651 — bit-for-bit identical to R25.
- **Belly apex**: exactly 73.000mm at z=72.0mm (45.00% of height) — exact match, after I
  independently hit and fixed the same local-frame-projection artifact that both the Tester (R2)
  and the original Reviewer (above, §2) separately flagged catching in their own scripts on this
  same geometry. A third independent party hitting and correcting the identical measurement
  pitfall is reassuring, not concerning — it confirms this is a known quirk of one specific
  technique on this curved geometry, not evidence of an actual defect.
- **Collar OD**: exactly 78.000mm at three sampled heights within the collar band. **Collar ID**:
  ~57.9-57.95mm (normal mesh-tessellation variance from the 58mm nominal).
- **Base cleanliness**: 77 vertices, all at exactly r=49.00mm, zero interior vertices — bit-for-bit
  identical to R25/R27, confirming the base-pocket defect from earlier in the project has not
  resurfaced.
- **Magnet pockets**: 3 pockets, bolt-circle radius exactly 34.000mm, diameter exactly 6.200mm,
  at 0°/120°/-120°, depth consistent with 2.2mm — exact match to R27, not the abnormal
  ~3×1.9mm cuts the incident produced.
- **Neck-to-collar blend**: smooth, gradually-changing slope across z=145-152mm with no
  discontinuous jump, anchor points exact (r=33.0000mm at z=145, r=39.0000mm at z=152) — consistent
  with R29, confirming the earlier collar-blend smoothness fix survived this recovery too.
- **Lid (control)**: watertight, 17,664 faces, bounds 100×100×75mm, 150.82 cm³, genuine open-loop
  handle confirmed via y-sweep — identical to every prior measurement, confirming it was genuinely
  untouched by this incident.
- **File timestamps**: `urn-body.*` fresh at 21:35; `urn-lid.*`/`neck-fit-test.*` unchanged at
  12:01/13:00 — consistent with the claimed incident scope.

I also confirmed the stray `pet-memorial-urn/nul` debug artifact (flagged as a minor hygiene item
in the original review, §5 above) has been deleted, and that `README.md`/`parameters.md` remain
in place and substantive.

## Determination: the original APPROVED verdict stands, unchanged

Every independently-checked figure matches the pre-incident, already-approved geometry exactly or
within normal mesh-resolution noise. This is not new geometry requiring a fresh review — it is a
faithful, independently-confirmed reproduction of the exact design this document already approved
above. None of the original approval's reasoning (business fit, technical parity, hard-constraint
compliance, documentation, cost) changes as a result of this incident or its recovery. The
**APPROVED** verdict at the top of this document stands as-is.

## Standing risk note, separate from the CAD verdict itself

This live Fusion file has now had **three manual/direct-edit incidents** across this project's
lifetime:

1. A scripted direct-BRep cut with an unset `participantBodies` property, leaking across
   components and producing stray base pockets (pre-approval).
2. A manual sketch-drag that collapsed the body's neck profile into a degenerate fragment,
   requiring a full profile/Revolve/Extrude rebuild (pre-approval).
3. A manual drag on the collar/neck region that ballooned the collar ID/OD and indirectly
   clipped the magnet pockets (post-approval, this addendum).

All three have been independently verified as fully recovered, with no residual damage found
anywhere checked, across three separate rounds of scrutiny. The recovery *process* on this
project is demonstrably working. But three incidents in one project's lifetime is a pattern, not
a coincidence, and it is worth flagging plainly for whoever edits this file next: **this document
and its predecessors' repeated recommendation stands** — prefer timeline-native, script-driven
parametric edits over direct manual dragging of sketch/BRep geometry in the Fusion UI for this
file, and if a manual edit is ever unavoidable, treat it as a higher-scrutiny change requiring an
explicit before/after geometry check (volume, face count, slope continuity), not a visual glance.
This is a file-handling/process risk, independent of and not a reason to revisit the CAD verdict
itself.

## Is the project's CAD work done?

**Yes**, modulo the same three non-CAD, requester-owned items already carried forward through
every prior pass and unaffected by this incident:

1. The physical neck-fit-test print-and-check (does a real remains bag pass through 58mm) —
   `neck-fit-test.*` files are confirmed untouched and still valid.
2. Magnet fit test coupons (PLA body, PETG lid) — never slicer-verified, unchanged status.
3. Manual slicer settings (layer height, infill, PETG-specific temps) — not embedded in any
   exported file, unchanged status.

None of these are CAD gates. The exported `step/`, `3mf/`, and `stl/` files for both `urn-body`
and `urn-lid` are geometrically sound, independently re-confirmed (again) to match the approved
design, and ready to print as-is.


---
---

# ADDENDUM 2 — 2026-08-28: magnet-assisted closure removed from CAD (targeted addendum, not a full re-review)

## Scope of this addendum

Per a direct request (relayed by `3d-director`, geometry side already settled through
Planner/Coder/Tester — see `specs.md` §6 v3 and `tests.md` Re-test Pass 5, R30-R34), the user
decided to remove the magnet-assisted lid closure entirely from the CAD. Both parts no longer
have any pre-modeled magnet pockets; the lid rests on the collar by flat-seating alone, and any
magnet assist the user wants is now their own print-time (slicer pause-and-embed) or post-print
(drill-and-glue) decision, outside this CAD. This addendum does not re-derive the geometry
conclusions from scratch — the Tester's Re-test Pass 5 is thorough and I did a quick corroborating
spot-check of my own (below) rather than a full independent re-analysis, per the scope requested.

**Quick corroboration (not a full re-derivation):** re-measured `stl/urn-body.stl` and
`stl/urn-lid.stl` directly — body remains watertight/single-component/Euler=2 with the same
bounds as every prior pass, and a sweep of the collar band (z=155-159.9mm) now shows exactly 2
boundary loops (outer wall + inner bore only) at every sampled height, versus the 5 loops
(outer + inner + 3 pockets) present in every pre-removal measurement — confirming the pockets are
genuinely gone, not capped over. Lid underside sweep (z=0-2.5mm) shows exactly 1 loop at every
height (plain flat plane, no pocket remnant), and the handle through-hole is unaffected
(2 loops from y=-4 to +4mm, 1 loop outside — same as every prior pass). This is consistent with
R30-R33 and gives me my own basis for the two points below, not just an inherited claim.

## 1. Business fit — re-confirmed PASS under flat-seating-only closure

My original "Business fit — PASS" finding (§1 above) cited "a magnet-assisted (not
airtight-dependent) closure appropriate for remains that are already bagged" as part of why the
design solves the stated problem. That specific mechanism is gone. Re-examining whether this
still holds:

- **The magnet assist was never load-bearing for the core business requirement.** The market
  research already on record in this project (cited in both `specs.md` §6 and my original
  review) established that no airtight seal is needed, because the crematorium's remains are
  already in their own sealed bag before they ever go in this urn. That finding is about the
  *seal*, not about the magnets specifically — a flat-seating lid was always functionally
  adequate for the actual containment requirement, independent of whether magnets existed. The
  magnets were an added "settled feel" nicety (per `specs.md` §6's original framing — "no airtight
  seal is needed... this is a 'settled feel' assist, not a latch"), not a functional requirement
  the business case depends on.
- **The approved concept brief itself never specifies a magnet closure at all.**
  `concept/brief.md` describes the lid as "domed, sized to seat on top of the neck opening" with
  the open-loop bail handle as "the key differentiating feature" — it says nothing about
  magnets, latches, or any closure hardware. The magnet-assist was a Planner-level spec addition
  (`specs.md` §6, made after the concept was approved), not something the signed-off concept
  itself promised. Removing it doesn't walk back anything the concept review approved.
- **The two features the concept brief does call load-bearing to the design's identity — the
  plain undecorated body and the open-loop lid handle — are both untouched by this change.**
  Independently reconfirmed above: handle through-hole still open, body still plain/smooth.
- **The removal is a legitimate, informed user decision, not a corner cut discovered after the
  fact.** The user explicitly chose to take on magnet placement themselves (pause-and-embed or
  drill-and-glue) rather than have it pre-modeled — this is a scope reduction the user asked for
  with a real alternative plan, not a silent regression the pipeline is asking me to wave through.

**Conclusion: business fit still holds.** The design continues to solve the stated problem (a
properly-sized, liftable-lid memorial urn for already-bagged remains) without the magnet
mechanism. Nothing the original approval actually depended on functionally has been undermined —
only a tactile nicety was removed, by the user's own informed choice, with a stated plan to
handle it outside the CAD if still wanted.

## 2. Correction to Addendum 1 (third manual-edit incident) — stale cross-reference fixed

Addendum 1 above (dated 2026-08-27, covering the third manual-edit incident) discusses the collar
magnet pockets as a present, currently-relevant feature (e.g. it describes the *legitimate*
collar/lid magnet pockets as intact and correctly restored after the incident, separately from
the unrelated *base-pocket defect* fixed earlier in the project). **That framing is now stale as
of this addendum's 2026-08-28 change**: the magnet pockets discussed there — both the body's
collar pockets and the lid's underside pockets — have since been intentionally and completely
removed from the current design, per `specs.md` §6 v3.

To be clear about what does and doesn't change as a result:
- **The third-incident history itself remains accurate and unchanged.** The incident happened,
  it was correctly diagnosed as a manual collar/neck drag that clipped the (then-still-existing)
  magnet pockets, and the recovery was correctly verified against the design as it existed at the
  time. None of that narrative is being rewritten.
- **What's stale is only the implication that the magnet pockets discussed in that addendum are
  still a current feature of the shipped design.** They are not — they were deliberately removed
  one day later, for unrelated reasons (a user preference to handle magnets outside the CAD), not
  because of any defect. Anyone reading Addendum 1 today should understand its magnet-pocket
  content as historical (accurate at the time it was written, describing a feature that has since
  been intentionally deleted), not as a description of the current print files.
- The **collar geometry itself** (78mm OD / 58mm ID, the neck-to-collar blend smoothness fix) that
  Addendum 1 also discusses is unaffected by the magnet-pocket removal and remains current and
  accurate — `specs.md` §6.2 v3 confirms the collar dimensions were explicitly held fixed even
  though its stated *purpose* changed from "magnet housing" to "reinforced seating band."

## Is `review.md` now internally consistent?

**Yes**, with this addendum in place. The original approval's business-fit and technical-parity
reasoning both still hold under the flat-seating-only closure (§1 above), and the one stale
cross-reference (Addendum 1's magnet-pocket discussion) is now explicitly flagged as describing a
since-removed feature rather than the current design (§2 above), without rewriting or discarding
that addendum's still-valid incident history.

## Final verdict

**Approval stands.** The removal of the magnet-assisted closure is a legitimate, user-driven
scope reduction that does not undermine any functional requirement the original approval actually
depended on, is consistent with the approved concept brief (which never specified magnets in the
first place), and has been independently verified (by the Tester in full, and by my own quick
corroborating spot-check above) as a clean, complete, regression-free removal on both parts.
`urn-body` and `urn-lid` remain approved and print-ready as currently exported. The same
non-CAD, requester-owned open items carried forward through every prior pass are unchanged: the
physical neck-fit-test bag check, and manual slicer settings. (Magnet fit test coupons are no
longer applicable, since there are no magnet pockets left in the CAD to test-fit against — this
item is now moot rather than open.)

---
---

# ADDENDUM 3 — 2026-08-28: capacity target change (~1477.8 cm³ → ~1579 cm³, +6.85%), fresh overhang re-check, render refresh

## Scope of this addendum

Per a direct follow-up request, this addendum covers three things prompted by `specs.md` v4 and
Tester `verdict.md` RE-TEST PASS 6 (the belly-fuller / wall-rebalance / neck-crease-fix round):
(1) a business-fit re-confirmation now that the built cavity volume has grown from the original
~1477.8 cm³ target to ~1579 cm³ — a change that explicitly crosses the spec's own ±5% tolerance
band (+6.85%), which the Tester correctly flagged as needing more than Coder-level sign-off;
(2) my own independent, from-scratch geometry spot-check of the current `urn-body` (not accepted
from the Coder/Tester chain alone); (3) a fresh overhang-angle check against the *current* belly
profile, since `specs.md` §9 explicitly disclosed that its overhang analysis was never recomputed
after the belly edit. This is a targeted addendum, not a full re-review — the geometry has already
been through multiple rigorous independent verification rounds (Tester RE-TEST PASSES 1–6, my own
Addenda 1–2 above), and nothing here reopens settled ground.

## 1. Independent geometry spot-check — my own measurement, live Fusion document, third independent method

I opened the live `pet-memorial-urn` Fusion document directly and wrote my own scripts against the
actual B-rep geometry (not the exported STL/3MF, and not a re-read of the Coder's or Tester's
numbers) — sampling the outer-wall and inner-wall NURBS faces directly via `Face.evaluator`, then
doing my own numerical revolution-integral for cavity volume. This is a **third independent
method**, distinct from both the Coder's Fusion mass-properties query and the Tester's mesh-based
integration:

| Check | My measurement (own method) | Coder | Tester | Agreement |
|---|---|---|---|---|
| Cavity volume | **1578.79 cm³** (direct integral of π·r(z)² over the sampled inner-wall profile, z=5–145mm, plus the exact bore cylinder z=145–160mm) | 1578.9824 cm³ | 1578.11 cm³ | Within 0.012% of Coder, 0.044% of Tester — solid |
| Belly apex (external radius) | **76.9659mm** at z=69.00mm | 76.97mm | 76.97mm | Exact match |
| Belly apex height | **43.12%** of 160mm (plateau spans z=66.9–71.4mm, i.e. 41.8%–44.6%) | ~43–44% (plateau) | ~43–44% (plateau) | Matches, confirms it's a genuine broad plateau, not a sharp point, at this same resolution |
| Wall thickness (belly/shoulder span) | **~4.000mm exactly** at every sampled height z=10–140mm | ~4.00mm (3.98–4.03mm) | ~4.00mm (3.98–4.03mm) | Matches, tighter than the claimed worst-case range at my sampling resolution |
| Material (shell) volume | **276.1556 cm³** (Fusion `physicalProperties.volume` on the live body) | 275.9651 cm³ | — | Within 0.07% |

I regard the cavity-volume match as the most meaningful confirmation here: three genuinely
different computational methods (Fusion's own mass-properties kernel, a mesh-integration on the
exported STL, and my own direct numerical integration of the sampled parametric surface) converge
on the same number to within four significant figures. **~1579 cm³ is not on shaky ground.**

## 2. Business fit — re-confirmed PASS, this is a *more generous* design, not a regression

Applying the same reasoning framework I used for the magnet-removal business-fit re-check
(Addendum 2, §1):

- The original ~1474.8/1477.8 cm³ figure was always framed as a **minimum**, not a fixed target —
  `specs.md` §4.1 derives it as `90 lb × 1 in³/lb`, explicitly choosing the top of the stated 50–90
  lb range because "oversizing capacity slightly is preferable to undersizing it for cremated
  remains." The new ~1579 cm³ figure, run back through the same rule the requester chose
  (`1579 cm³ ÷ 16.3871 cm³/in³ ≈ 96.3 in³ ≈ 96.3 lb` equivalent capacity), still describes a design
  comfortably serving the same "large, 50–90 lb" market segment — it does not push the product into
  a different weight bracket, misrepresent what it's for, or create a mismatch with a smaller/larger
  size in a lineup (this is explicitly the only size being built, §12).
- Nothing about the *shape* of the business case changed: this is still a single-size, large-pet
  urn, still with the same plain body and open-loop handle the concept brief calls
  load-bearing to its identity (both independently reconfirmed unaffected by this round — the belly
  edit and wall rebalance are internal-cavity/wall-thickness changes, not changes to the handle or
  the plain-body constraint).
- The mechanism by which this happened — a user-directed aesthetic choice (fuller belly, "kept
  intentionally") that had a volume side-effect the user then explicitly chose to accept rather
  than correct by thinning the wall — is a deliberate, informed tradeoff, not a defect discovered
  after the fact and rationalized. This is the same category of legitimate, disclosed scope
  decision as the magnet-removal round, just running in the opposite direction (adding capacity
  instead of removing a feature).
- **This does cross the spec's own ±5% routine-tolerance threshold**, which is exactly why
  `specs.md` was correctly bumped to a formal v4 revision rather than left as an informal
  Coder/Tester understanding — I agree with the Tester's judgment call that this warranted a
  written revision and a fresh business-fit look, and I'm making that look now rather than treating
  "the user already said it's fine informally" as sufficient on its own.

**Conclusion: Business fit — PASS, re-confirmed.** The original "Business fit — PASS" section at
the top of this document (§1) is updated by this addendum: the design's capacity is now ~1579 cm³
against the original ~1477.8 cm³ minimum target, a **deliberate, accepted, +6.85% increase in
generosity**, not a shortfall — the design continues to solve the stated problem for the same
50–90 lb target market, arguably with more safety margin against undersizing than the original
number carried.

## 3. Fresh overhang-angle check against the *current* (post-belly-edit) profile

`specs.md` §9 explicitly flagged that its overhang analysis was computed against the **pre-v4**
profile and never recomputed against the fuller/repositioned belly — the Planner and Tester both
named this as an open gap rather than silently carrying old numbers forward. I did the fresh check
directly on the live geometry rather than requiring another Tester round-trip, per the specific
request to fold this in:

**Method:** sampled the *entire* outer-wall surface continuously from z=0 (base) to z=160mm (rim)
— stitching together all four outer-wall face patches (`Body5` faces 7, 8, 9, 10, which together
span base→belly→shoulder→neck-taper→collar-blend→collar-cylinder) at sub-millimeter resolution,
computed local `dr/dz` at every step, and searched the **whole span** for any zone where the local
angle from vertical exceeds the 45° self-supporting guideline — not just re-checking the
previously-known trouble spot.

**Findings:**

- **The only zone anywhere on the entire outer wall exceeding 45° is the already-known, already-
  disclosed neck-to-collar external blend (z≈145–152mm).** Peak local angle there is now
  **47.25° at z=147.25mm** — about 1.6° higher than the ~45.6° figure reported for the pre-v4
  profile, but the same location, the same already-disclosed "watch it on the first print" zone
  (a few degrees over the guideline, on a short span of a fully closed 360° revolve), not a new
  concern and not a new site. `specs.md`/`parameters.md` should be updated with this refreshed
  number, but I don't think this needs a fresh Tester pass — it's the same disclosed risk,
  quantitatively confirmed, not a new one.
- **The belly region itself — both the base-to-belly flare (P0→apex) and the belly-to-neck-taper
  descent (apex→P3) — remains entirely in the self-supporting "shrinking/growing-monotonically"
  class.** I checked this directly rather than assuming it still holds on the new, bigger belly:
  - Base→apex (z=0–69mm): **zero locally-decreasing radius steps** across 1,382 sampled steps —
    genuinely monotonic non-decreasing, confirming the outward flare never reverses.
  - Apex→neck-taper-end (z=69–145mm): local angle stays negative (radius shrinking) at virtually
    every sampled point; the only positive-angle noise found (123 of 2,016 steps, max **0.409°**)
    sits at floating-point/sampling-noise level, concentrated right at the broad, nearly-flat belly
    plateau where the profile is *supposed* to be near-zero slope — this is not a real reversal,
    and it's two orders of magnitude below anything that would matter for print behavior.
  - This confirms the project's standing "shrinking-cone, self-supporting regardless of local
    angle magnitude" argument holds exactly as well on the current, fuller/lower belly as it did
    on the pre-edit profile — the belly getting bigger and moving slightly lower did **not**
    introduce a new overhang risk anywhere in this region.
- **Documentation discrepancy found in the process (not a geometry defect):** `specs.md` §4.3's
  shoulder OD row (122mm OD / 61mm radius at z=119mm) — which the spec itself already flagged as
  "not independently re-verified... may be stale" — **is confirmed stale by my direct
  measurement.** The actual current radius at z=119mm is **46.42mm (≈92.8mm OD)**, roughly 30mm of
  diameter off from the documented figure. This doesn't change any pass/fail conclusion (cavity and
  material volumes were verified directly via mass-properties, not derived from this figure), but
  it should be corrected in the next documentation pass so nobody designs against the stale number.

**Conclusion: no new problematic overhang was introduced by the v4 belly edit.** The body's
base-down print orientation remains sound; the one elevated-angle zone is the same one this
project has tracked since the collar-blend fix, marginally higher but not qualitatively different.
This is a manufacturability question I was able to close out directly from the live geometry —
I don't think it needs a dedicated Tester round-trip, but flagging that judgment call explicitly
per the request, in case the director wants a second, independent confirmation anyway given this
project's history of needing extra scrutiny in exactly this body region.

## 4. Incidental finding, fixed: body appearance had silently reverted to a default material

While setting up the render (below), I found `urn-body`'s `Body5` was displaying the default
**"Steel - Satin"** appearance rather than the custom **"Matte PLA - Stoneware Tan (urn-body)"**
appearance used in the original hero render — almost certainly a side effect of the `Revolve1`
recreation during this round's belly/neck work resetting the body's appearance override. The
correct custom appearance was still defined in the document (untouched), just not applied to the
current body. **I reapplied it and saved the document.** This is not a geometry defect and has no
bearing on the printed part, but it would have caused any future render or visual QA pass to show
the wrong (generic gray-steel) material look despite `specs.md`/`README.md`'s material recommendation
being unchanged — worth knowing about since this is the second time in this project that a
timeline-native rebuild has silently reset something adjacent to the geometry it touched (the
first being the `participantBodies` default itself, back in the original defect).

## 5. Documentation currency — real gap, required follow-up (same category as the original review's finding)

**`README.md` and `parameters.md` at the project root have not been updated to reflect `specs.md`
v4.** Both still describe the pre-v4 state throughout:

- `README.md` states "≈1512 cm³ (≈92 in³) internal capacity" — the actual current figure is
  ≈1579 cm³ (≈96.3 in³).
- `parameters.md` §1's body table still lists "External belly max OD: 146mm (r=73mm)" and
  "Internal cavity volume: 1511.8 cm³" — both superseded by the current 76.97mm-radius belly and
  ~1579 cm³ cavity. There's no mention anywhere in either document of the belly-fuller edit, the
  inner-wall rebalance to a constant ~4mm offset, or the neck-to-collar crease repair — all three
  of which are now fully documented in `specs.md` v4 but not propagated to the two documents this
  shop's own convention says a future editor or the requester would actually reach for.

This is the same category of finding as my original review's §5 (documentation lagging the
as-built design), just recurring: the pipeline is doing excellent work keeping `specs.md`/
`tests.md`/`verdict.md` current and rigorous, but the lightweight top-level docs are drifting out of
sync after a material design change, again. **Required follow-up before this project is called
fully "done" a second time** — not a print blocker (the exported STEP/3MF/STL files are correct
and reflect the current geometry; only the human-readable summaries are stale).

## 6. Cost — re-confirmed PASS, and this round is actually a mild cost *improvement*, not a tradeoff

Despite the +6.85% larger cavity, the body's actual material (shell) volume **decreased** slightly,
from ~293.4 cm³ (pre-v4, post-magnet-removal figure) to **~276.16 cm³** (my measurement, matching
the Coder's 275.9651 cm³) — the reshaped profile (fuller belly, but a shoulder-to-neck taper that
now converges noticeably faster) uses somewhat less total wall material overall despite enclosing
more internal volume. At the same PLA/PETG pricing basis used in the original review (§6), this
is, if anything, a fractionally cheaper body than before, not a more expensive one. **Cost verdict
unchanged: trivially cost-effective, ~$8–12 in filament for the pair**, and this round's design
change improves rather than worsens that number.

## 7. Render — refreshed to reflect the current, final geometry

The existing hero render (`render/pet-memorial-urn-hero.png`, produced 2026-08-27) predated this
round's belly/wall/neck-crease edits and no longer depicted the shipped design (it showed the
pre-v4, ~73mm-radius belly). Since a materially different silhouette is now the actual product,
I produced a fresh render from the live, current Fusion geometry rather than leave a stale image
as the project's "final" preview:

- Fixed the body's reverted appearance (§4 above) and confirmed the lid retains its correct
  **"Matte PETG - Stoneware Tan (urn-lid, sanded)"** appearance.
- Temporarily raised the lid occurrence to its true seated height (160mm) and made it visible for
  the render only, then **reverted both changes** afterward (transform back to identity, visibility
  back to hidden) so the live working document isn't left in a staged/assembled state — the only
  permanent change saved to the document is the appearance fix, which is a genuine correction.
- Confirmed the Photo Booth lighting environment (used in the original render) was already active,
  disabled the sketch grid, and captured an isometric hero angle via `Viewport.saveAsImageFile`
  directly from the API (the real geometry, not a generated image).
- Saved to `render/pet-memorial-urn-hero.png` (replacing the stale image); the pre-v4 render is
  preserved, not deleted, at `archive/pre-v4-belly-render/pet-memorial-urn-hero.png` for reference.
- **Same honest caveat as the original render:** a faint background reference-grid overlay is still
  visible and could not be fully suppressed via the available API — this is a rendering-tool
  limitation, not a model defect, consistent with what the original Reviewer found and disclosed.

## 8. Concept-fidelity check on the refreshed render — a real, incremental drift worth naming, not silently waved through

Comparing the new render directly against the approved `concept/concept-v2.png`, per the specific
instruction to flag (not silently approve) if the built design has drifted from what was actually
signed off on visually:

**The built design's belly-to-neck proportions are now noticeably more pronounced/pinched than the
concept image's considerably gentler taper.** `concept-v2.png` shows a wide-mouthed, gradually
tapering pot — the belly-to-opening width ratio is modest, and there's no sharp constriction
anywhere in the silhouette. The shipped design already had a narrower neck/collar than the concept
for a disclosed, functional reason (the reinforced lid-seating band, named as the "banded rim"
drift in my original review, §2), and the v4 belly enlargement (73mm→76.97mm external radius) has
widened that gap further by making the belly comparatively even bigger relative to the same-sized
neck/collar. The current render reads more like a rounded "ginger jar" silhouette with a distinct
shoulder pinch than the concept's smoother, more gradual vase shape.

**I'm naming this plainly rather than either blocking on it or silently letting it pass:**

- This is not a pipeline error or an undisclosed drift — the user directed this exact change with
  full awareness of its visual consequence (`specs.md` §4.1: "a deliberate aesthetic decision, not
  a defect... the user explicitly chose to keep it rather than revert").
- The concept brief's own words — "wider through the belly, tapering inward to a narrower neck" —
  are, if anything, *more* true of the current shape than of the original concept photo; this
  reads as an intensification of the same design language, not a departure into a different one.
- The two features the concept brief explicitly calls load-bearing to the design's identity (the
  plain undecorated body, the open-loop bail handle) are both fully intact and correctly
  proportioned in the current build, independently reconfirmed above and in prior passes.
- That said, "more pronounced than what was actually shown in the signed-off image" is a real,
  cumulative visual gap (on top of the already-disclosed banded-rim drift), not a null finding —
  **I'd recommend a quick, low-stakes visual check-in with the requester** (a side-by-side glance
  at the new render vs. `concept-v2.png`) before this is treated as fully final, purely as a
  courtesy confirmation that the more-bulbous look still reads as "right" to them now that it's
  built, not because I think the geometry needs to change.

## Final verdict for this addendum

**Approval stands.** Business fit is re-confirmed under the new ~1579 cm³ capacity (more generous,
not a regression) — the original "Business fit — PASS" conclusion at the top of this document is
hereby updated to reflect this. My own independent, from-scratch geometry spot-check (a third
method beyond the Coder's and Tester's) confirms the cavity volume, belly apex, and wall thickness
figures in `specs.md` v4 are solid. The fresh overhang-angle check requested against the current,
post-belly-edit profile found **no new problematic overhang anywhere** — the one elevated-angle
zone is the same previously-disclosed neck-to-collar blend, marginally higher (47.25° vs. ~45.6°)
but not a new site or a new category of risk; I don't believe this needs a dedicated Tester
round-trip, though the director may want one anyway given this body region's history. Two real,
non-blocking follow-ups are carried forward: **(1)** `README.md`/`parameters.md` need updating to
the v4 figures (capacity, belly OD, the three v4 edits) — required before the project is called
fully documented, not before it can be printed; **(2)** a quick requester visual check-in on the
now-more-pronounced belly-to-neck proportions vs. the originally approved concept image, as a
courtesy confirmation rather than a rework requirement. The refreshed hero render at
`render/pet-memorial-urn-hero.png` now depicts the actual, current, final geometry — the previous
render is preserved at `archive/pre-v4-belly-render/pet-memorial-urn-hero.png`. `urn-body` and
`urn-lid` remain approved and print-ready as currently exported.
