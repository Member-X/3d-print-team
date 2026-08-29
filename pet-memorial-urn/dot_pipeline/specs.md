# Spec — Pet Memorial Urn (Large / 50–90 lb pet size)

Picking up from the **approved concept** (`pet-memorial-urn/concept/brief.md`, `concept-v2.png`).
No new shape proposal happens in this document — it converts the approved concept into buildable
numbers, all newly derived or estimated in this pass (the concept's own placeholder dimensions in
`concept-v2-dimensions.png` are explicitly NOT used, per the brief's own caveat and the requester's
instruction — see §2).

This is a **single-size build**: sized for the top of the stated 50–90 lb target range (~90 lb).
No parametrization for a small/medium lineup is in scope here — see §12.

---

## 1. Source key (dimension provenance)

| Tag | Meaning |
|---|---|
| **VERIFIED** | Independently confirmed this session — a real, currently-sold commodity part (e.g. a magnet size found listed by multiple suppliers), a manufacturer spec sheet, or a physical measurement. |
| **DERIVED — sizing decision** | Computed from the requester's explicit rule-of-thumb math (1 in³ internal volume per lb of pet body weight), with the formula shown. Not a guess, but also not independently measured — it's a calculation built on a target the requester chose. |
| **ESTIMATED** | A design convention or best-guess default (wall thickness, clearance, ergonomic handle size) not sourced from a spec sheet, measurement, or the volume-derivation math. |

There is **no hardware-mating item in this project** in the usual sense (this doesn't clip onto or
mount against a real external object) — per the requester's own note, the escalate-and-verify-with-
a-ruler-photo path doesn't apply here. The closest thing to a "mating dimension" is the **lid-to-body
seating interface**, which is self-contained (both parts are being designed together, not fit to a
pre-existing object) — flagged and reasoned through explicitly in §5 anyway, since a wrong number
there is still the highest-risk item in this spec even though it isn't a hardware-mating case.

---

## 2. Files (Coder deliverables)

| File | Purpose |
|---|---|
| `pet-memorial-urn/step/urn-body.step` | Editable CAD source for the body, parametric if the tool supports it |
| `pet-memorial-urn/step/urn-lid.step` | Editable CAD source for the lid |
| `pet-memorial-urn/3mf/urn-body.3mf` | Slicer-ready body, orientation baked in per §7 |
| `pet-memorial-urn/3mf/urn-lid.3mf` | Slicer-ready lid, orientation baked in per §7 |
| `pet-memorial-urn/stl/urn-body.stl` | Final body mesh |
| `pet-memorial-urn/stl/urn-lid.stl` | Final lid mesh |

Body and lid are **two separate printed parts**, each independently manifold/watertight. They are
not printed in place and not glued together permanently — the lid simply rests removably on the
body's collar rim (§5.2). No mechanical or magnetic closure feature is modeled into either part;
see §6 for what changed and why.

---

## 3. Printer constraints (stated up front)

| Constraint | Value | Tag |
|---|---|---|
| Printer | P2S-class FDM | Per task instruction / user memory |
| Build volume | 256 × 256 × 256mm | Per user memory (`user_printer_specs.md`) |
| Nozzle diameter | 0.4mm (assumed standard) | ESTIMATED — not explicitly confirmed this session, standard shop default per every prior spec in this repo |
| Minimum wall/boss thickness implied | ≥0.8mm (2× nozzle) for any wall or boss under load | Computed from the line above |
| Body fits build volume? | ~154mm max OD × 160mm H (updated v4 — belly OD grew from v2's 146mm due to a user-directed manual belly edit, §4.1/§4.2.1) | **Yes**, by a large margin on every axis (§4) |
| Lid fits build volume? | 100mm max OD × 75mm H | **Yes**, by a large margin on every axis (§5) |

Body and lid are separate parts, so — per the task framing — the combined assembled height
(~235mm, §5) does **not** need to fit the bed in one shot. Each part individually clears 256mm on
every axis with well over 90mm of margin; bed fit is not a binding constraint on this design.

Every wall/collar/handle dimension chosen in §§4–6 is checked against the 0.8mm minimum at the end
of each section — none of them come close to that floor; the thinnest feature in the whole design
(4mm nominal body wall) is 5× the minimum.

---

## 4. Sizing derivation — internal volume target and body dimensions (REVISED — v4, see §13)

### 4.1 Volume target — original derivation, and the current binding target (REVISED — v4)

Per the requester's explicit instruction: industry rule of thumb is **~1 in³ of internal usable
volume per pound of pet body weight**. Target category is large pets, 50–90 lb. Per instruction,
sizing to the **top of the range (90 lb)** since oversizing capacity slightly is preferable to
undersizing it for cremated remains.

```
Target internal volume = 90 lb × 1 in³/lb = 90 in³
90 in³ × 16.3871 cm³/in³ = 1474.8 cm³  (≈ 1.47 liters)
```

**Target: ≈1475 cm³ internal cavity volume.** Tagged `DERIVED — sizing decision`, not a measured
or manufacturer-sourced number — it is a deliberate application of the requester's chosen rule of
thumb to the top of the stated weight range, exactly as instructed.

---

**Status as of v4 — this is no longer the number the design is being held to.** The ≈1475 cm³
figure above (and the closely related ≈1477.8 cm³ hand-calculated estimate from the v2 profile
fix, §4.2) was the **original starting target** and remained this design's binding number through
v2 of this spec. Since then, a sequence of user-directed decisions during CAD refinement (detailed
in §4.2/§4.2.1 and §13 v4) has grown the built, independently-verified internal cavity volume to:

**≈1579 cm³** (Coder-measured 1578.9824 cm³; Tester independently measured 1578.11 cm³ — both via
CAD mass-properties queries on the actual as-built model, cross-verified in agreement, not a
hand-calculated estimate).

That is **+6.85% over the original 1474.8 cm³ target** — a crossing of the ±5% routine-tolerance
band this spec itself defines (§4.2's original caveat: "flag back for a spec revision if it falls
outside the ... band by more than ~5%"). That crossing is exactly why this is a formal spec
revision (v4) rather than an informal carry-forward in chat/test logs.

**Why:** the user made a direct, intentional manual edit to the body's outer belly in Fusion,
making it visibly fuller than the originally-derived profile — a deliberate aesthetic decision,
not a defect, and the user explicitly chose to keep it rather than revert. That edit left the
inner wall not tracking the new, fuller outer wall (uneven thickness); the user then directed the
inner wall be reworked to track the new outer wall at a constant ~4mm offset — matching the
wall-thickness approach used everywhere else in this profile — rather than (a) leaving the
mismatched inner wall as-is, or (b) thinning the wall below ~4mm specifically to force the volume
back down to the original target. The larger cavity is the accepted, explicit consequence of that
decision, not a silently-absorbed side effect.

**New binding target, effective this revision: ≈1579 cm³ internal cavity volume, ≈276.0 cm³
material/wall volume.** Both cross-verified independently by Coder and Tester (§4.2.1). Future
spec revisions, Tester checks, and Reviewer sign-off should be checked against **this** number
going forward — the original 1474.8 / 1477.8 cm³ figures above remain in this document only as
historical context for how the sizing target was originally derived, not as the current spec.

**Business-fit note (for the Reviewer's separate assessment):** the original 1474.8 cm³ figure was
always a *minimum* target — 90 lb × 1 in³/lb, deliberately sized to the top of the stated 50–90 lb
range ("oversizing capacity slightly is preferable to undersizing it," above). ≈1579 cm³ exceeds
that minimum by +6.85%; the design is now **more** generous on capacity than originally planned,
not less. Flagging this explicitly because "exceeded the spec's own tolerance band" could otherwise
read as a shortfall on first glance — it is the opposite direction. The business-fit judgment call
(whether more-generous-than-planned is still the right fit for this product line) is the
Reviewer's to make, not asserted here.

### 4.2 Body profile and the volume math — v2 derivation (HISTORICAL basis; see §4.2.1 for the current, as-built figures — v4)

> **v4 status note:** everything below in this section describes the **v2 spline-based derivation**
> the Coder originally built from — the tangent-constrained control points, the hand-calculated
> frustum approximation, and the resulting ≈1477.8 cm³ estimate. As of v4, the belly/shoulder
> region of the **built part** has since been directly, manually edited in Fusion by user
> instruction (making the belly fuller) — that is **not** a re-run of this spline math, it's a
> sculpted change layered on top of it. The **P1 (belly) row in the control-points table below has
> been updated** to the current as-built, verified values; everything else in this section (the
> frustum volume table, the hand-calc, and the ≈1477.8 cm³ figure) is retained as **historical
> provenance only** — it describes how the pre-edit shape was originally derived, not the part's
> current geometry or volume. **Do not build or verify against the ≈1477.8 cm³ figure below — see
> §4.2.1 for the current authoritative numbers (≈1579 cm³).**

**This section replaces the v1 frustum table.** Two problems were found by the Coder doing a direct
pixel-measured visual comparison of the built body against `concept-v2.png` (not just a re-read of
the v1 numbers): (1) the v1 belly-max point sat at 56% up the total height, while the concept's
belly reads at roughly 45% up — noticeably lower; (2) the v1 straight-line frustum-stack approach,
even with small transition fillets, produced a visibly faceted body rather than the smooth,
continuously-curved "ceramic vase" silhouette the concept shows. Both are fixed below. Everything
not called out as changed — total external height (160mm), 4mm nominal side wall, 5mm floor, the
~1475–1478 cm³ volume band, and the neck ID/collar geometry — is held fixed per instruction.

**Fix #1 — belly position.** The belly max is moved from 90mm up (56%) to **72mm up from the
external base (45% of the 160mm total height)**, matching the concept's measured proportion. This
was re-derived from scratch (not a linear rescale of the old table) — see the worked math below.

**Fix #2 — faceted appearance.** The v1 approach (straight-line segments between control points,
small corner fillets) is replaced with a **single continuous tangent-constrained spline** through
the same control points, revolved 360° about the vertical axis. This is the same technique already
used for the lid dome (a curved arc profile, not a straight-sided approximation) — applied here to
the body for the same reason. A fallback for tools that can't do a constrained fit-point spline is
given at the end of this section, but the spline is the specified primary method, not an
either/or left to the Coder's judgment.

#### Control points and tangencies (internal profile; spline sketch + revolve)

`Z_int` = height measured from the internal floor's top surface (0mm) to the rim (155mm).
`Z_ext` = height measured from the external base (0mm) to the rim (160mm) = `Z_int + 5mm` (floor
thickness sits below the internal profile's zero point).

| Point | Z_int | Z_ext | Internal radius | Tangent condition |
|---|---|---|---|---|
| P0 — floor/base | 0mm | 5mm | 45mm | **Horizontal** (dr/dz = 0) — smooth rounded foot where the flat floor meets the rising wall, no sharp internal corner. Replaces v1's separate "10mm fillet" callout; the spline itself now produces this rounding. |
| P1 — belly max (true apex/plateau) †v4 | ~63–65mm | **~68–70mm (43–44% of 160mm)** | **~72.97mm int. / 76.97mm ext.** | Broad, nearly-flat plateau, not a sharp point — see †v4 footnote below. Superseded by a direct manual edit; the original horizontal-tangent spline condition no longer strictly describes this region. |
| P2 — shoulder (inflection) | 114mm | 119mm | 57mm | Tangent-continuous, spline-default (interior inflection between two curve senses, not an apex — exact slope not hand-specified; the Coder should confirm the sketch's curvature comb shows no reversal/cusp here before revolving). **Not independently re-verified against current as-built geometry — see †v4 footnote.** |
| P3 — neck taper end / base of collar | 140mm | 145mm | 29mm | **dr/dz → 0** — must flatten to match the constant-radius straight section immediately above it, or there will be a visible kink where the taper meets the collar. |
| P4 — rim / top of collar | 155mm | 160mm | 29mm | Constant radius, P3→P4 is a true vertical cylinder (dr/dz = 0 throughout). |

†v4 — **P1 updated this revision.** Radius **76.97mm is the external (outer wall) radius**,
VERIFIED — Coder-measured directly on the as-built CAD, independently cross-verified by Tester
(both a CAD geometry query against the actual model, not an external reference — treated as
equivalent to a physical measurement per §1's `VERIFIED` definition). Internal radius (~72.97mm)
is derived from that external value minus the verified ~4.00mm wall (§4.2.1), not independently
queried on its own. Height is a broad, nearly-flat plateau spanning roughly `Z_ext = 68–70mm`
(43–44% of the total 160mm height) — documented as a range rather than a single decimal because
it is not a sharp apex. **This is not ~50%, which was an incorrect intermediate figure reported
during this revision's resolution, and not 45% (72mm), which was the pre-edit v2 value** —
43–44% is the corrected, final figure. P0 (floor), P3 (neck-taper end), and P4 (rim) are confirmed
**unchanged** this revision. P2 (shoulder) has **not** been independently re-verified against the
current as-built geometry in this revision — its 57mm/119mm figures are carried forward from the
v2 derivation below; flag for re-check in a future pass if precision here matters downstream (the
belly/shoulder region was described as one general area of manual editing, but only the belly
apex has verified post-edit numbers).

Construction: one fit-point spline through P0–P4 with the four explicit tangent constraints above
applied in the sketch, revolved 360°. **Fallback**, only if the CAD tool cannot do a
tangent-constrained fit-point spline: keep the v1-style straight-segment stack (same 5 points) but
increase the transition fillets well beyond v1's unspecified "small" radii — **≥15mm at the belly
apex (P1), ≥12mm at the shoulder (P2) and neck-taper-end (P3)** — large enough relative to the
47mm/26mm segment heights involved to actually read as continuous curvature rather than a corner
treatment on an otherwise straight wall. This is explicitly a fallback, not a second acceptable
default — use the spline unless the tool genuinely can't do it. **(This construction description
is historical/v2 — see the v4 status note at the top of this section; the as-built belly region
was subsequently hand-edited rather than produced purely by this spline method.)**

#### Volume math (re-derived from scratch, not rescaled from v1)

With P0, P3, and P4 radii fixed by other constraints (P0 by the base convention carried from v1;
P3/P4 by the untouched 58mm neck ID, §6.2) and P1 fixed by Fix #1 at `Z_int = 67mm`, the only free
variables left to hit the volume target are the shoulder radius/position (P2) and the height split
between segment 2 (P1→P2) and segment 3a (P2→P3), which must together span `155 − 67 − 15 = 73mm`.
Kept the same base/belly/shoulder radii as v1 (45 / 69 / 57mm) since changing only the height split
was sufficient to hit the target — no radius changes were needed:

Straight-line-chord (frustum) approximation used for hand-calculation, `V = (π·h/3)·(r1² + r1·r2 + r2²)`:

| Segment | Internal r1 → r2 | Height | Volume |
|---|---|---|---|
| 1. Floor (P0) → belly max (P1) | 45mm → 69mm | 67mm | 693.98 cm³ |
| 2. Belly max (P1) → shoulder (P2) | 69mm → 57mm | 47mm | 587.81 cm³ |
| 3a. Shoulder (P2) → neck taper end (P3) | 57mm → 29mm | 26mm | 156.36 cm³ |
| 3b. Straight neck/collar (P3→P4) | 29mm (constant) | 15mm | 39.63 cm³ |
| **Total internal volume** | | **155mm internal height** | **≈1477.8 cm³** |

```
Solve for the h2/h3 split (h2 + h3 = 73mm) that hits the target, holding radii fixed:
  Need V2+V3a ≈ 742.95 cm³ (= 1476.5 target − V1(693.95) − V3b(39.6))
  V2+V3a = (π/3)·[h2·(69²+69·57+57²) + (73−h2)·(57²+57·29+29²)]
         = (π/3)·[h2·11943 + (73−h2)·5743]
  Solving: h2 ≈ 46.8mm → rounded to h2 = 47mm, h3 = 73−47 = 26mm

Check: 693.98 + 587.81 + 156.36 + 39.63 = 1477.78 cm³
1477.78 cm³ vs. 1474.8 cm³ target → +0.20% — same tolerance band as v1, target met.
Back-check: 1477.78 cm³ ÷ 16.3871 cm³/in³ ≈ 90.18 in³  ✓ matches the 90 in³ target.
Sanity check on heights: 67 + 47 + 26 + 15 = 155mm internal ✓; +5mm floor = 160mm external ✓.
```

**Named caveat on the spline vs. this frustum table (same honesty rule as v1, restated for the new
geometry):** the table above is a straight-chord approximation between control points, not the
literal volume of the tangent-constrained spline that will actually be built. Because P1 is a true
apex with zero tangent, the real spline bulges slightly outward past the straight P0–P1–P2 chords
near the belly (adds volume vs. this table). Because P2→P3 is a concave "waist" pulling toward the
neck, the real spline likely sits slightly inside the P2–P3 chord there (removes volume vs. this
table). These two effects partially offset but can't be hand-computed precisely for a spline — **the
Coder must verify the true modeled internal volume with the CAD tool's mass-properties function
once the real spline-revolved geometry exists, and flag back for a spec revision if it falls outside
the 1475–1478 cm³ band by more than ~5%.** Given the frustum estimate already sits only +0.2% over
target, there isn't much headroom before a real deviation would require a small radius/height
tweak — this is a plausible, not unlikely, follow-up, and is not a failure if it happens.

All radii/heights in this table are `DERIVED — sizing decision` (chosen specifically to hit the
volume target while keeping the concept's silhouette proportions), except P3/P4's 29mm radius,
which is `DERIVED` directly from the untouched 58mm neck ID (§6.2), not a free choice.
**(All of the above, including the tags, describes the pre-edit v2 state — see §4.2.1 for the
current as-built numbers.)**

### 4.2.1 Current as-built profile — authoritative volumes and verified geometry (v4)

This subsection is the **current source of truth** for body volume and wall geometry, superseding
the frustum estimate in §4.2 above.

| Metric | Value | Tag / verification |
|---|---|---|
| Internal cavity volume | **≈1579 cm³** (Coder: 1578.9824 cm³; Tester independently: 1578.11 cm³) | VERIFIED — CAD mass-properties query on the as-built model, cross-checked by two independent measurements in agreement within normal tolerance |
| Material (wall) volume | **≈276.0 cm³** (Coder: 275.9651 cm³) | VERIFIED — Coder-measured from the same as-built geometry as the cavity figure above; not separately re-run by Tester as an independent check |
| Belly apex, external radius | **76.97mm** | VERIFIED (see §4.2 footnote above) |
| Belly apex, height | **~43–44% of the 160mm total height** (broad plateau, `Z_ext ≈ 68–70mm`) | VERIFIED — documented as a range, not a single decimal, because it's a broad, nearly-flat plateau, not a sharp point |
| Wall thickness through the belly | **~4.00mm** (verified 3.98–4.03mm across ~60 sampled heights) | VERIFIED — both inner and outer wall now peak at the same height (the prior 13.3mm vertical misalignment between inner/outer peaks, from the mid-revision inner-wall rework, is fully resolved) |
| Neck-to-collar junction (top of neck / base of collar) | Smooth at print-relevant resolution | VERIFIED — a pre-existing crease at this junction (present in the outer wall as the user left it after the belly edit, unrelated to the wall-rebalance itself) was found and repaired with a narrowly-scoped fix (only the final 5mm of the outer wall's tail near the rim), independently confirmed fixed. A sub-print-resolution irregularity at the repair splice seam was also found but is ~100× finer than print layer height — explicitly not a defect, noted here only as "checked," not as a remaining issue. |
| Collar (OD / ID) | 78mm / 58mm | Unchanged throughout this entire revision — see §6.2 |
| Base | Clean, 0 pockets | Unchanged |
| Solid integrity | Single valid manifold solid | Unchanged |

**Sequence that produced this state (full narrative in §13 v4):** (1) the user manually edited the
outer belly to be fuller, and explicitly chose to keep it; (2) this left the inner wall not
tracking the new outer wall, so the user directed a rework of the inner wall to track the outer
wall at a constant ~4mm offset; (3) the resulting cavity volume is structurally larger than the
original target allows, and the user explicitly chose to accept that larger capacity rather than
thin the wall below ~4mm to force the volume back down — a deliberate, informed override of the
original volume-tolerance-driven sizing, not a defect being silently absorbed; (4) a separate,
pre-existing crease at the neck-to-collar junction was found and fixed with a narrowly-scoped
repair, unrelated to the belly/wall changes.

**Not recomputed in this revision:** a fresh frustum-style hand-calculation for the full as-built
profile (segments 2–3a in the §4.2 table above) was not attempted, since the belly/shoulder region
was shaped by direct manual sculpting rather than parametric control points — a hand-calc against
sculpted geometry would only be a rough approximation of an approximation. The verified CAD
mass-properties figures above (1579 / 276.0 cm³) are treated as authoritative instead.

### 4.3 Body external dimensions (wall thickness applied) — REVISED, see §13 v4

| Parameter | Value | Tag |
|---|---|---|
| Nominal wall thickness (body sides) | **4mm** design target; **~4.00mm as-built (verified 3.98–4.03mm across ~60 sampled heights, v4)** | The 4mm figure itself remains ESTIMATED (a design convention, chosen for perceived heft/"doesn't feel like plastic," §8, not a print-minimum — 5× the 0.8mm floor). **As-built achievement of that target is now VERIFIED** (§4.2.1), including through the fuller belly region introduced in v4, where the inner wall was specifically reworked to keep tracking this thickness. |
| Floor thickness | **5mm** | ESTIMATED — slightly thicker than the side wall for base stability and to support the settled weight of the remains bag over years on a shelf. Unchanged from v1. |
| External base OD (at P0) | **98mm** | DERIVED (internal 90mm + 2×4mm wall). Unchanged from v1; confirmed unchanged again in v4 (§4.2.1). |
| External max belly OD (at P1, `Z_ext ≈ 68–70mm`, ~43–44% up) | **~153.9mm** (2 × 76.97mm) | VERIFIED (v4) — supersedes the v2 estimate of 146mm; see §4.2 footnote for the measurement basis. Grew from v2's 146mm as a direct result of the v4 manual belly edit (§4.1, §4.2.1), not a re-derivation from the volume target. |
| External OD at shoulder (at P2, `Z_ext = 119mm`) | **~92.8mm** (46.42mm radius) | VERIFIED — Reviewer-measured directly on the as-built geometry (Addendum 3, `review.md`), superseding the stale 122mm/61mm figure carried in earlier revisions of this row. The stale value was never re-derived from the volume math; it was simply left over from before the v4 belly rework — the shoulder transition shifted along with that manual belly edit and this figure wasn't re-measured/updated at the time. |
| External OD, neck at base of collar (at P3, `Z_ext = 145mm`, below the reinforced collar band, see §6) | **66mm** | DERIVED. Unchanged from v1. |
| Internal opening ID (constant through the collar) | **58mm** | DERIVED. Unchanged — untouched per instruction. |
| **Overall external height, base to top of neck rim** | **160mm** (5 + 67 + 47 + 26 + 15) | DERIVED. Same total as v1; internal split changed. |

Internal floor/wall corner: previously called out as a standalone **10mm fillet radius**. Superseded
by the P0 horizontal-tangent condition in the spline method above, which produces the equivalent
rounding as part of the profile itself rather than as a separate feature. If the fallback
straight-segment method is used instead, reinstate a ≥10mm fillet at this corner specifically.

### 4.4 Neck opening size — named risk

Internal opening ID is 58mm (~2.3in). This needs to be wide enough to insert the crematorium's own
sealed bag of remains. Cremated remains are a loose, granular/powder material in a flexible bag, so
a bag with more "relaxed" volume than 58mm-diameter can typically still be worked through an
opening this size by scrunching the flexible bag — but **this has not been tested against a real
filled cremation bag and is `ESTIMATED`, not verified.** Flagging as a named risk rather than a
silent assumption: if a real bag turns out too bulky/stiff to pass through 58mm comfortably, the
fix is widening the straight neck/collar ID in a spec revision — it does not require resizing the
whole body.

---

## 5. Lid dimensions and the lid/body seating interface

### 5.1 Lid geometry

| Parameter | Value | Tag |
|---|---|---|
| Flat brim disc OD | **100mm** | ESTIMATED — sized to visually overhang the neck collar (78mm, §6 — updated from a stale 74mm, see §13 v2) the way the concept image shows, with margin |
| Flat brim disc thickness | **5mm** | ESTIMATED |
| Dome height above brim top surface | **30mm** | ESTIMATED |
| Dome base OD (where dome meets brim) | **~80mm** | ESTIMATED |
| **Total lid height (flat underside to top of handle)** | **75mm** (5 brim + 30 dome + 40 handle, §6.2) | DERIVED from the above |

### 5.2 Seating interface — decision and why it changed from a first draft

**Decision: the lid's underside is a single flat plane. It rests directly on the body's flat
neck-collar rim (§6, 78mm OD flat ring — updated from a stale 74mm, see §13 v2) — no plug, no
skirt, no alignment lip reaching down into the opening.**

This was **not** the first design considered in this pass. A first draft added a small
downward-facing alignment lip (to center the lid over the opening) — that was dropped for a
concrete, checked reason, not aesthetics:

- A lip protruding below the main flat underside creates a sudden radial "shelf" overhang when the
  lid is printed underside-down (its natural, lowest-overhang orientation) — the print would need
  to jump from a small-diameter lip footprint to the full ~100mm brim footprint within one layer,
  which is a genuine unsupported overhang requiring support material directly on the part's primary
  seating surface (bad for the flatness/finish of the one surface that most needs to stay flat).
- Removing the lip makes the **entire lid underside a single continuous flat plane** — the best
  possible surface for both print quality (zero overhang on the primary surface, ideal bed
  adhesion) and a flush, wobble-free seat against the body's flat collar rim.
- Centering is handled by the collar's visible edge alone (user aligns by eye/feel — this is a
  decorative object handled deliberately and slowly, not a snap-fit consumer product needing blind
  alignment). No magnetic or mechanical assist contributes to centering — that feature has been
  removed from the CAD entirely, see §6.

**Fit check:** at the seating height, body OD (78mm, the collar) is smaller than the lid brim OD
(100mm) — the brim overhangs the collar by 11mm on each side, hanging in open air above the sloped
shoulder below it. Since the flat lid occupies no space below the seating plane, there is **no
collision** between the brim overhang and the tapered shoulder underneath it — confirmed by
comparing Z-heights, not assumed. This overhang is a visible, expected part of the "cap resting on
top" look and matches the concept photo's proportions reasonably well.

**No dedicated clearance/tolerance value is needed for this interface** (unlike a plug/skirt fit)
because it's a flat-on-flat resting seat, not a sliding fit. With the magnet pockets removed from
the design (§6), there is no other tolerance-sensitive feature anywhere in the lid/body fit — the
flat seating plane described above is the entire interface.

---

## 6. Lid closure — flat seating only, no built-in magnet or latch feature (REVISED, see §13 v3)

**As of this revision, the CAD does not include a magnet-assisted closure, or any other mechanical
latch/catch feature.** The lid closure is entirely: the lid's flat underside (§5.1) resting on the
body's flat collar rim (§6.2 below, and §5.2's seating-interface writeup) — nothing else. This
supersedes the earlier "magnet-assisted catch" design in v1/v2 of this document, which specified
paired 6mm magnet pockets in both parts; those pockets have been removed from scope (see §13 for
what changed and why).

Per market research already done for this project: **no airtight seal is needed** (remains are
already in the crematorium's own sealed bag) — the lid is a resting cap by design, not a latch, and
that was true independent of whether a magnet assist existed.

### 6.1 Magnet-assist and other closure hardware — explicitly out of this CAD's scope

The user has decided to handle any magnet placement (or other closure enhancement) themselves at
print time or after printing, rather than have it pre-modeled into the parts. This is a deliberate
scope reduction, not an oversight or something left for the Coder to improvise:

- **No pockets, bosses, or recesses for magnets (or any other hardware) should be modeled in either
  part.** The lid underside and the collar's top-facing rim are both plain, uninterrupted flat
  surfaces.
- If the user wants a magnet assist in the finished, physical print, that is now entirely a
  print-time or post-print decision made **outside this CAD**, using one of two approaches the user
  raised: (a) a slicer-level pause-and-embed workflow, where the operator manually creates their own
  void/modifier geometry in the slicer at a chosen layer and drops magnets in during a print pause,
  or (b) a fully manual post-print step — drilling a recess and gluing magnets in after the part is
  printed. Neither approach requires (or benefits from) anything being pre-cut into the model here.
- Nothing in §§4–5 or §7 depended on the magnet pockets existing (the body profile, volume, and
  seating interface were all derived independently of them), so removing them has no ripple effect
  outside this section and the specific cross-references corrected elsewhere in this revision (see
  §13).

### 6.2 Neck collar (reinforced rim / seating band — no longer a magnet housing)

**Collar geometry and dimensions are unchanged from v2 — this was an explicit user decision, not an
oversight.** The collar was originally added (v2) to serve as a magnet housing; with the magnet
pockets removed, its *purpose* is corrected below, but its OD/ID/wall/height are left exactly as
they were, at the user's explicit instruction, rather than reverting to the nominal 4mm body wall.
The user accepted the known, previously-flagged minor concept-fidelity drift this causes (the collar
reads slightly more "banded/cylindrical" than the concept's continuous neck curve) in preference to
re-touching a region of the model that has already had three separate manual-edit incidents during
this project.

**v4 addendum — neck-to-collar junction crease, found and fixed:** independent of the collar's own
geometry (unchanged, above) and independent of the belly/wall changes described in §4.1/§4.2.1, a
pre-existing crease at the neck-to-collar junction — in the outer wall, at the top of the neck just
below where the collar begins — was found during this revision's verification pass and repaired
with a narrowly-scoped fix (only the final 5mm of the outer wall's tail near the rim). Independently
confirmed fixed; the junction is smooth at print-relevant resolution. See §4.2.1 for the full
verification note, including a sub-print-resolution irregularity at the repair splice that was
checked and found immaterial (~100× finer than print layer height, not a defect).

**Corrected purpose:** the top **15mm of the neck (the straight section, §4.2 segment 3b) is a
locally thickened, full 360° reinforced band** that now exists purely as a **rim-reinforcement and
lid-seating detail** — a robust, constant-radius, flat-topped surface for the lid to rest on,
noticeably more substantial than the nominal 4mm body wall would give at the exact point that takes
the lid's contact load and repeated lift-off/reseating over the object's lifetime. It has **no
functional pocket, cavity, or hardware feature of any kind inside it.**

| Parameter | Value | Tag |
|---|---|---|
| Collar height | 15mm (= P3→P4 in the revised §4.2 profile) | Carried from §4.2 |
| Collar external OD | **78mm** | ESTIMATED — carried unchanged from v2 per the user's explicit instruction to leave this geometry as-is. |
| Internal ID through the collar | 58mm (unchanged — no effect on internal volume, §4.2) | DERIVED |
| Collar wall thickness | **10mm** ((78−58)/2) | DERIVED from the 78mm OD above; carried unchanged from v2. Well above the 0.8mm print-minimum (§3) purely as a seating-band reinforcement — no magnet pocket depth/diameter constraint applies to it any more. |

This collar is rotationally symmetric (no isolated bump geometry), reads plausibly as a rim
reinforcement detail on a ceramic-style vessel, and gives the lid a flat, adequately thick, uniform
surface to seat against — the same physical shape as v2, doing a narrower job.

---

## 7. Handle (open-loop bail) — hard constraint compliance

**Hard constraint, restated: the handle must be an open through-hole loop, not an enclosed/blind
cavity, specifically so internal print support material can be removed after printing.** This
geometry, as specified, satisfies that constraint directly — see below.

| Parameter | Value | Tag |
|---|---|---|
| Handle height above dome apex | **40mm** | ESTIMATED |
| Bail cross-section | **9mm round** | ESTIMATED — "thick, rounded," well above the 0.8mm print-minimum; not sized for a heavier load case (see load case note below) |
| Clear opening (the through-hole itself) | **24mm wide × 22mm tall** | ESTIMATED — ergonomic convention, sized for a single adult fingertip (typical fingertip width ~15–20mm) with comfortable margin |
| Handle footprint at the dome (both legs) | **~46mm wide × 14mm deep** | ESTIMATED |
| Fillet at handle-to-lid junction | **4mm** | ESTIMATED — modest, matched to the actual load case below, not over-built |

**Load case, per instruction:** the handle only needs to support the lid's own weight when lifted
by hand — not the assembled urn with body + contents. A 9mm-diameter PLA loop with a 4mm root
fillet is far in excess of what's needed to lift a single PLA lid (rough estimate: well under
200g), so no heavier-duty wall thickening was applied. It should still read as "an intentional,
load-bearing part of the lid" per the brief — the 9mm bail and generous proportions (vs. a thin
wire loop) are what deliver that without over-engineering for a load case that doesn't apply here.

**Open-hole compliance:** the loop is a simple arch with nothing else planned to pass through or
block the opening — no wiring, no second feature threading through it. When printed dome-up (§7.1
below), the only support material generated will be inside this one small 24×22mm opening, which is
fully accessible from both ends of the loop after printing. No blocker identified here.

---

## 8. Material recommendation — REVISED, see §13 v2

**Body: matte or silk PLA** (not standard/glossy PLA), per direct instruction and the
market-research finding that comparable products get called out in reviews for "feeling like
plastic." Reason: matte/silk PLA variants diffuse surface reflection in a way that reads closer to
the stoneware finish the concept calls for than standard glossy PLA does. Unchanged from v1.

**Lid: PETG.** Changed from v1's matte/silk PLA — this decision was made after the original draft
and is reflected here for the first time. Reason: PETG is more heat/UV-resistant than PLA, which
meaningfully reduces warp risk specifically for the lid — the part most likely to be repeatedly
picked up and handled (§7), and the smaller/thinner of the two parts, so more prone to warping from
ambient heat than the larger body. This also directly mitigates the long-term-display risk flagged
in v1's edge case 3 (§10) for the *lid*, though not for the body, which remains PLA.

**Named risk introduced by this change, flagged rather than silently absorbed:** PETG's default
finish is glossier than matte/silk PLA's. A glossy PETG lid sitting on a matte PLA body risks a
visible finish mismatch that undercuts the "doesn't feel like plastic" goal this material choice was
meant to serve in the first place. The planned sanding pass (below) should be applied more
aggressively to the lid specifically, to knock down PETG's default sheen and bring it closer to the
body's matte finish — this is not guaranteed to fully close the gap, and the Coder/Tester should
flag back if the finished parts read as visibly mismatched in person.

**Planned post-processing: a light sanding pass** on both parts before/after assembly, specifically
targeting visible layer lines on the body's smooth curved surfaces (where they'd be most visible and
most damaging to the "not plastic-feeling" goal), with extra attention to the lid per the
finish-mismatch risk above — this is a deliberate step in the plan, not an optional nice-to-have.

**Named risk, flagged rather than silently overridden (body only, now that the lid is PETG):** per
this shop's own standing material guidance, PLA (matte/silk or otherwise) softens and can warp under
sustained heat/UV exposure (e.g. displayed on a sunny windowsill, near a heat vent). This spec still
specifies PLA for the **body** because that's an explicit instruction tied to a specific finish
requirement (PETG doesn't come in the same matte/silk finish family as commonly), but the risk is
real for a piece intended for long-term display — see edge case 3 in §10. This risk no longer
applies to the lid, which is now PETG specifically to avoid it.

---

## 9. Print orientation (decided here, not left to the Coder)

**Body: base (flat, 98mm OD) down on the bed, opening/neck facing up.**
- Matches the part's natural resting stance. Unchanged from v1.
- **Overhang angles re-checked against the revised §4.2 profile** (not just carried over from v1 —
  the segment heights changed enough that the old claim needed re-verification, using
  `θ = atan(Δr / Δz)` measured from vertical on the external radii at each control point):
  - P0→P1 (base outward flare to belly, `Δr=24mm` over `Δz=67mm`): **~20° from vertical** — gentle, no concern.
  - P1→P2 (belly inward taper to shoulder, `Δr=12mm` over `Δz=47mm`): **~14° from vertical** — gentle, no concern.
  - P2→P3 (shoulder to neck taper end, `Δr=28mm` over `Δz=26mm`): **~47° from vertical** — this is
    the steepest transition and sits **slightly past** the conventional 45° self-supporting
    guideline (v1's equivalent segment was steeper still by this same measure, ~54°, despite v1's
    text claiming ~35–39°; that older figure appears to have used a different angle convention and
    is superseded here rather than carried forward uncorrected).
  - **This 47° spot is a minor, named consideration, not a blocker:** 45° is a rule-of-thumb, not a
    hard cutoff, and this is a continuously curved surface (not a flat shelf) at this point, which
    typically tolerates a few degrees past 45° with adequate part cooling. Flagging it so the Tester
    checks this specific band (roughly the P2–P3 transition, `Z_ext ≈ 119–145mm`) on the first test
    print for drooping/ribbing, and increases cooling or locally reduces print speed there if needed
    — rather than assuming it's fine on paper alone.
- The 98mm flat base gives a large, stable bed-adhesion footprint.
- **v4 flag, not re-verified:** the overhang angles above were computed against the pre-v4 (v2)
  profile (§4.2's historical table). The v4 manual belly edit (§4.1, §4.2.1) changed the belly's
  radius (69mm → 76.97mm external) and height position (45% → ~43–44%), which will shift these
  local angles somewhat — plausibly easing the P0→P1 angle and tightening P1→P2 somewhat, though
  this has **not** been recomputed against the current as-built geometry in this revision. Flagging
  rather than leaving the 20°/14°/47° figures stated as current fact. If a future print run is
  planned, the Tester should re-check actual print behavior at the belly transitions against the
  as-built model, not just this table.

**Lid: flat underside down on the bed, dome and handle facing up.**
- This is the single flat plane established in §5.2 specifically because it's the best possible
  print orientation for this part — full, continuous bed contact with zero overhang on the primary
  seating surface.
- The dome (apex-up) is a self-supporting flare through most of its height, with a **known, minor,
  cosmetic-only risk right at the very apex** where the surface angle approaches horizontal — a
  small amount of drooping/ribbing at the last 1–2mm of the apex is possible and is a normal,
  usually slicer-manageable artifact for small domes this size, not a structural concern.
- The handle loop's open through-hole (§7) will generate support material inside the loop only —
  by design, since the loop is open and that support is meant to be removed afterward.

---

## 10. Edge cases

1. **Pet significantly below the 90 lb design target (e.g. a 50 lb dog).** This urn is intentionally
   sized for the top of the stated 50–90 lb range (§4.1) as a deliberate single-size decision, not a
   miscalibration — a 50 lb pet's remains will use noticeably less than the current ~1579 cm³ built
   capacity (§4.1/§4.2.1 — updated in v4 from the original ~1477.8 cm³ design target, which this
   edge case's logic held for through v3; the underlying point is unchanged and, if anything,
   stronger now that the capacity is larger). This is expected and accepted per the requester's own
   instruction; a smaller size is a separate, future project (§12), not a fix needed here.
2. **Remains bag too bulky/stiff to pass through the 58mm neck opening** (§4.4). Flagged as an
   `ESTIMATED`, untested assumption — the fix, if it comes up in testing, is widening the neck ID in
   a spec revision, not resizing the body.
3. **Sustained heat or direct sunlight exposure** (e.g. a sunny windowsill, near a heat vent) — per
   this shop's standing PLA guidance, PLA (including matte/silk variants) can soften/warp under
   prolonged heat/UV. Accepted here because the finish requirement specifically calls for a PLA
   variant (§8), but worth surfacing to the requester as a real long-term-display risk, not silently
   absorbed into the material recommendation.

---

## 11. Question back to the requester

**What slicer settings should be used (layer height, infill)?** No layer height or infill target has
been specified. Given this is a decorative, low-mechanical-stress vessel (the only load-bearing
feature is the lid handle, §7, sized for the lid's own weight only), a reasonable default absent
other direction would be **0.16–0.2mm layer height** (finer layers matter more here than usual,
given the "doesn't feel like plastic" finish bar in §8) and **15–20% infill** (the floor and walls
carry the modest weight of a bagged-remains payload; this isn't a structural load case that needs
high infill) — please confirm or state a preference before the Coder locks in export settings.

---

## 12. Scope note — future sizing

Per instruction, this is a deliberate **single-size build**. The user's longer-term plan is a
small/medium/large lineup, but only "large" is being built and fully validated
(planner → coder → tester → reviewer) right now. The Coder should feel free to keep the CAD
parametric/editable internally (makes future resizing easier), but should **not** spend effort
building a generalized size-variant system in this pass — that is explicitly out of scope until
this size is complete and validated.

---

## 13. Revision history

| Version | What changed | Why |
|---|---|---|
| v1 | Initial spec. Derived internal volume target (1475 cm³) from the requester's 90 lb / 1 in³-per-lb rule, built a frustum-based body profile hitting that target within 0.2%, and worked through the lid/body seating interface, magnet housing, and handle geometry from first principles rather than reusing the concept image's placeholder numbers. | First planning pass for this project, picking up from the approved concept. |
| v2 | **§4.2/§4.3 rewritten:** (1) moved the belly-max control point from 56% up the total height (90mm) to 45% up (72mm), re-deriving the full height/volume table from scratch (not a linear rescale) — new segment heights 67/47/26/15mm vs. v1's 85/35/20/15mm, same 45/69/57/29mm radii, re-verified at ≈1477.8 cm³ (+0.20% vs. the 1474.8 cm³ target, same tolerance as v1); (2) replaced the straight-line frustum-stack-with-small-fillets construction method with a tangent-constrained spline through the same 5 control points (explicit tangency conditions given at each point), to fix a visibly faceted body silhouette. **§6.1/§6.2 corrected:** collar external OD updated from a stale 74mm to the actual settled 78mm (delegated-authority decision made elsewhere but not yet reflected in this document), with the wall-thickness (8→10mm) and magnet bolt-circle (66→68mm) figures propagated to match. **§8 updated:** lid material changed from matte/silk PLA to PETG (decision made after v1, reflected here for the first time), with a new named risk (PETG/PLA finish mismatch) called out rather than silently absorbed. **§9 re-verified:** overhang angles recomputed against the revised §4.2 profile rather than carried over unchecked; found the shoulder-to-neck-taper transition now runs ~47° from vertical (slightly past the 45° guideline) and flagged it as a named, minor consideration for the Tester's first print, not a blocker. | Two real gaps were found by the Coder doing a **direct pixel-measured visual comparison of the built body against `concept-v2.png`**, at the user's request, rather than just re-checking the spec's own numbers against themselves: the belly sat too high (an artifact of v1's derivation being checked only against the volume target, never against the concept's actual silhouette), and the body read as faceted rather than smoothly curved (an artifact of the frustum-stack construction method, not fixable with small fillets alone). Both are fixed here per explicit downstream instruction, with full re-derivation shown rather than a cosmetic patch. |
| v3 | **Magnet-assisted closure removed entirely from the CAD's scope.** §6 rewritten: no magnet pockets, bosses, or any other mechanical/magnetic closure feature are modeled in either part; the lid closure is now defined solely by the flat lid-underside-on-flat-collar-rim seating already described in §5.2. §6.1 replaced — the old "Magnets" hardware table (magnet type/size, count, bolt-circle placement, pocket size, embedding method, polarity note) is deleted outright rather than reworded, since none of it describes anything that still exists in the model. §6.2 reworded, not deleted: the neck collar's OD/ID/wall/height (78mm/58mm/10mm/15mm) are **unchanged** — this was an explicit user decision, made to avoid re-touching a region of the model with a history of three separate manual-edit incidents, accepting the previously-flagged minor concept-fidelity drift (collar reads more "banded" than the concept's continuous neck curve) as a known tradeoff rather than a defect to fix. Only the collar's *stated purpose* changed, from "magnet housing" to "reinforced rim / lid-seating band." Cross-references corrected: §2 (removability no longer attributed to a magnet-assist rationale), §5.2 (removed "magnets' own pull" from the centering discussion and the "magnet pocket fit" tolerance callout, since no pocket exists to have a tolerance on). Checked §8 (material) and §10 (edge cases) for stale magnet-specific risk callouts — none were found; the existing PLA/PETG finish-mismatch risk and the standing PLA heat/UV risk are both about material and finish generally, not about the magnet mechanism, so both are left as-is. | User decided to handle magnet placement (if any) themselves at print time — via a slicer-level pause-and-embed workflow or a fully manual post-print drill-and-glue step — rather than have pockets pre-modeled into the parts. This is a scope reduction requested directly by the user, not a fix for a defect found downstream. The collar band itself was explicitly kept as-is per the user's own instruction, to avoid another manual-edit pass on a part of the model that has already needed three such passes this project. |
| v4 (this document) | **§4 substantially revised to consolidate a post-v2 capacity drift into one authoritative record**, rather than leaving it scattered across test logs. §4.1: added a "current binding target" statement — the original ≈1474.8/1477.8 cm³ target is superseded by the now-accepted **≈1579 cm³** built-and-verified capacity (+6.85% over the original), with the reasoning laid out and a business-fit note added for the Reviewer (this is the design becoming *more* generous on capacity, not less). §4.2: added a status callout marking the v2 spline-derivation, frustum table, and ≈1477.8 cm³ figure as **historical provenance only** — no longer the current volume; updated the **P1 (belly) control-point row** to the verified as-built values (external radius **76.97mm**, height **~43–44%** of 160mm as a broad plateau — not the pre-edit 45%, and not the ~50% figure that was briefly and incorrectly reported mid-revision); flagged **P2 (shoulder)** as not independently re-verified against current geometry; confirmed P0/P3/P4 unchanged. **§4.2.1 (new):** authoritative as-built table — cavity volume ≈1579 cm³ (Coder 1578.9824 cm³, Tester-independent 1578.11 cm³), material volume ≈276.0 cm³ (Coder 275.9651 cm³), wall thickness verified ~4.00mm (3.98–4.03mm across ~60 sampled heights, the prior 13.3mm inner/outer peak misalignment fully resolved), and confirmation that the neck-to-collar junction is smooth at print-relevant resolution after a narrowly-scoped repair. §4.3: updated the belly-OD row (146mm → ~153.9mm, tag `DERIVED` → `VERIFIED`) and the wall-thickness row (added as-built verification) to match; flagged the shoulder-OD row (122mm) as unverified against current geometry. §3: updated the body max-OD build-volume-fit figure (146mm → ~154mm) — still clears the 256mm bed by a large margin, not a binding constraint. §6.2: added an addendum confirming a separately-found neck-to-collar crease (in the outer wall, unrelated to the belly/wall rebalance) was fixed with a narrowly-scoped repair (final 5mm of the outer wall's tail near the rim) and independently confirmed. §9: flagged, but did not recompute, that the body's stated overhang angles were derived from the pre-v4 profile and haven't been re-checked against the current as-built geometry. §10 edge case 1: updated the stale ≈1477.8 cm³ capacity reference to the current ≈1579 cm³ figure. | Consolidates a capacity drift that happened in three steps without ever being cleanly restated in one place: (1) v2's spline/profile fix produced a hand-calculated ≈1477.8 cm³ estimate, but the real spline-revolved CAD, once built, measured out to **≈1512 cm³** — a +2.3% deviation from the original 1474.8 cm³ target, within the ±5% band that §4.2's own caveat allowed as routine (not requiring a spec revision), so it was accepted and absorbed without a formal entry at the time. (2) The user then made a direct, intentional **manual edit to the body's outer belly** in Fusion, making it visibly fuller, and explicitly chose to **keep** that change rather than revert it. (3) This left the inner wall not tracking the new outer wall, so the user directed a **rework of the inner wall** to track the outer wall at a constant ~4mm offset (matching the approach used across the rest of the profile) — the resulting cavity, **≈1579 cm³**, is structurally larger than the original target allows, and the user explicitly chose to **accept the larger capacity** rather than thin the wall below ~4mm to force the volume back down. That final step crossed the ±5% tolerance band (+6.85% over the original target) that the spec itself defines as the threshold for a real revision rather than routine sign-off — hence this entry. A separate, unrelated **crease at the neck-to-collar junction** was found and fixed in the same verification pass; it's a narrowly-scoped repair, not connected to the capacity/wall changes, documented here so it isn't lost among the same test logs this revision exists to consolidate. All final numbers were **independently verified by the Tester**, not just Coder-reported, before being written into this spec — per this project's own standing rule that a wrong "final" number should never be silently built around. |
