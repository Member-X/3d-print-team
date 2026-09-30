# Jason Voorhees Candle Holder Bust — Visual Concept Brief

Status: Round 3 — NOT approved. v3 failed to apply its two targeted fixes; another
regeneration pass is needed before this can go back to the user.
Current best-approved-elements reference: concept-v2.png (v3 attempted two fixes on top
of it but the fixes did not visibly land — see Iteration log).

## Source
v1 was based on two reference photos the user pasted directly into chat (not saved to
disk — no image files were available to hand to the generator, so v1 was produced from
a text description only, via a from-scratch generation rather than an image-to-image
variation).

v2/v3 corrections are grounded in a specific real-world reference the user pulled up:
NECA's officially licensed Friday the 13th Part 3 Jason Voorhees prop-replica mask
(the classic/original hockey mask design). Sources cited by the user:
- https://www.timebombtoys.com/product-page/neca-friday-the-13th-part-3-jason-voorhees-prop-replica-mask
- https://toywiz.com/neca-friday-the-13th-part-3-jason-mask-prop-replica-re-issue/

If further rounds need closer fidelity to the original two chat-pasted photos, the user
should save/export those to a file path so they can be used as direct references.

## Concept
A bust of Jason Voorhees (Friday the 13th), sculpted from roughly the waist up, no legs,
standing on a flat round base like a display statue. Both arms are raised overhead, bent
at the elbow, and his gloved hands hold up a wide flat black ring-shaped platform above
his head — the ring is the candle-holder surface. Styled after licensed collectible
"figure holding a tray" busts (e.g. NECA-style Jason candle/tray bust).

## Pose / Hand Placement (CORRECTED in v2, confirmed still correct in v3)
- v1 had both hands together underneath/behind the ring's center — rejected as reading
  like a one-sided two-handed grip rather than balanced support.
- v2 and v3: hands are on EITHER SIDE of the ring — left hand grips the left side, right
  hand grips the right side, independently — so the ring reads as a physically balanced
  two-point support rather than a single grip point. Keep this two-point side-grip
  arrangement going forward. This element is working correctly and should NOT be touched
  in the next regeneration.

## Head / Mask (target spec — must match real NECA Part 3 prop mask)
- Base color: solid flat aged bone/ivory (no gradient — see finish rules below) — WORKING
  correctly in v2/v3
- Eye holes: OVAL, not perfectly round — appears roughly correct in v2/v3, subtle, worth
  a final visual confirmation but not currently flagged as broken
- Breathing holes: small round holes scattered IRREGULARLY, clustered mainly on the
  cheeks and forehead — NOT a neat symmetric grid — WORKING correctly in v2/v3
- Strap mounting: FOUR round flat metal rivet/washer discs at the strap attachment
  points — two near the temples, two lower near the jaw/cheek hinge area. There is NO
  plain leather/cloth strap band across the forehead.
  **STATUS: NOT YET ACHIEVED.** Both v2 and v3 only show 2 rivets total (at temple/
  eye-level height on each side) — the lower jaw-hinge pair was never added, despite v3
  being specifically prompted to add them. This still needs a regeneration attempt with
  a more forceful/explicit prompt (e.g. explicitly describe four distinct disc positions
  by name/height, possibly reference "like four large flat metal shirt-snap buttons at
  temple-height-left, temple-height-right, jaw-height-left, jaw-height-right").
- Red mark: ONE solid flat red inverted-V / chevron / checkmark shape, centered below
  the eyes, pointing down toward the chin. WORKING correctly in v2/v3 — do not disturb.
  This is the single most recognizable feature of this mask; v1 incorrectly used multiple
  diagonal slash marks — do not let that reappear even if "weathering/damage" is
  requested later.

## Torso / Clothing (unchanged concept, finish style corrected — WORKING in v2/v3)
- Stocky, broad-shouldered build
- Worn, wrinkled dark olive/army-green flannel work shirt, buttoned up the front, two
  flap chest pockets, sleeves pushed up toward the raised arms
- Fold/crease texture shown as hard-edged flat shadow shapes, not soft photoreal gradient
  shading — correct in v2/v3, do not disturb
- Black gloves on both hands

## The Platform / Tray (functional part — SHAPE FIX NOT YET ACHIEVED)
- Wide, flat black ring: a thick disc with an open center, generous lip supporting the
  underside of a jar candle. Overall scale/width/sturdiness reads correctly and matches
  the candle-clearance requirement below — do not shrink it.
- Held at two independent side points (left hand / right hand) — correct, do not disturb.
- **STATUS: NOT YET ACHIEVED.** Since v2, the ring has rendered as a stepped two-tier
  drum shape — a visible horizontal step/gap between a narrower lower band and a wider
  upper band — rather than a single continuous smooth ring of even thickness (a plain
  thick torus, like a thick tire). v3 was specifically prompted to fix this and the
  result was visually near-identical to v2's stepped profile — the fix did not land.
  Needs a regeneration attempt with a more forceful/explicit prompt emphasizing complete
  removal of the step/ledge and a single uniform torus cross-section (e.g. "no ledge, no
  shelf, no second tier — one smooth rounded/rectangular cross-section swept in a full
  circle, like a thick rubber tire or a fat wedding band, viewed from the front as a
  single flattened oval band with one continuous top edge and one continuous bottom
  edge").

## Finish / Color Approach (CORRECTED in v2 — important for printability — WORKING)
v1 used photoreal gradient shading and smoothly blended dirt/weathering, which was
flagged as not translating to an actual FDM print (color transitions on a real print are
either hard edges from filament swaps/multi-material or hand-painted afterward — both
need distinct, flat color zones, not gradients). v2/v3 correct this and it is working
well:
- Every material is ONE solid flat color: mask = solid aged-ivory/bone, red accent =
  solid flat red, shirt = solid olive-green, skin = solid tan, gloves = solid black,
  platform + base = solid black
- Shading approach is "cel-shaded / clean paintable zones" — hard-edged shadow shapes
  for fabric folds and mask contours, not soft/photoreal gradients
- If any weathering/scuffing is wanted on the mask or shirt in future rounds, it must be
  shown as a few small isolated solid-color patches, NOT a blended/smudged dirt gradient
- Keep this flat-color/cel-shaded rendering approach for all future concept rounds —
  do not revert to photoreal gradient shading even if other details change

## Presentation
Neutral studio product-shot background — background styling is not part of the design
itself and can be ignored/changed freely in later passes.

## CRITICAL FUNCTIONAL DIMENSION — flag for the Planner
This is a real, physical print intended to hold an actual candle jar, not just a display
piece:

- Target candle: Bath & Body Works "3-Wick" jar candle
- **4 in (101.6 mm) diameter x 3.5 in (88.9 mm) tall, 14.5 oz**
- The ring's inner opening / supporting lip needs to visually and (eventually,
  dimensionally) actually clear that footprint with margin — aim for roughly
  **4.25–4.5 in (108–115 mm) inner clearance**, generous rather than tight, since a real
  glass jar has to physically drop into it.
- No exact wall thickness, load-bearing calculations, or precise mm geometry have been
  set yet — those are the Planner's job once the visual design is locked. This document
  only specifies the intended real-world dimension the design must accommodate and the
  visual impression of scale/sturdiness needed to sell that it can.
- The two-point side-grip hand placement is itself a structural cue worth passing to the
  Planner: the user cares about the design reading as physically balanced/stable support
  for the ring, not just about visual style — worth keeping in mind when the real
  geometry is engineered (e.g., whether the ring needs its own independent structural
  support back to the base/shirt, versus relying purely on the arms).
- Note: once the ring shape is corrected to a single continuous band (see above), confirm
  the single-band profile still reads as thick/sturdy enough for the candle-bearing
  requirement — don't let "remove the step" accidentally thin out the ring's cross-section
  in the next attempt.

## Iteration log
- v1 (2026-09-14): First pass, generated from text description only (no source images
  available). Photoreal/gradient-shaded rendering; both hands together behind/under the
  ring's center; generic mask with round eye holes, neat grid of breathing holes, plain
  strap band, and multiple red diagonal slash marks.
- v2 (2026-09-14): Applied user feedback grounded in real NECA Part 3 mask reference.
  Changed hand placement to independent left/right side grips on the ring. Converted
  entire rendering to flat/solid cel-shaded colors with hard-edged shadows (no
  gradients, no blended weathering) for FDM-printability. Corrected mask to oval eyes,
  irregular hole clustering on cheeks/forehead, and a single solid red inverted-V chevron
  below the eyes (removed the incorrect multi-slash marks from v1). Shirt, pose concept,
  ring sturdiness/scale, and waist-up bust format carried over unchanged from v1 (all
  previously approved). Correction: on closer review this entry previously
  (incorrectly) logged v2 as having all four rivets — it did not; v2 only rendered 2 of
  the 4 requested rivet discs (temple-height pair only), and the ring rendered as a
  stepped two-tier shape rather than a single band, though this wasn't caught until v3's
  targeted fix attempt made the gap obvious by comparison.
- v3 (2026-09-15): User approved everything else in v2 and requested exactly two fixes:
  (1) add the missing 2 lower jaw-hinge rivets so all 4 are present, (2) change the ring
  from a stepped two-tier drum to a single continuous smooth band. RESULT: neither fix
  visibly landed — v3 is nearly pixel-similar to v2 in both respects. Still only 2
  rivets total, still a stepped two-tier ring profile. Everything else that was already
  working in v2 (cel-shaded flat colors, side-grip pose, mask coloring/chevron, shirt,
  base, proportions) remained correct and untouched in v3. NOT sent back to the user for
  review — flagged internally as needing another regeneration attempt with more forceful/
  explicit prompt language on these two specific points before the next round goes out
  for feedback.
