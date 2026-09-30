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
| `pet-memorial-urn/step/neck-fit-test.step` | **Standalone neck/collar fit-test article — MUST be rebuilt this revision, do not skip.** See the v5 note immediately below. |
| `pet-memorial-urn/3mf/neck-fit-test.3mf` | Slicer-ready fit-test article, same v5 resize as above |
| `pet-memorial-urn/stl/neck-fit-test.stl` | Final fit-test-article mesh, same v5 resize as above |

Body and lid are **two separate printed parts**, each independently manifold/watertight. They are
not printed in place and not glued together permanently — the lid simply rests removably on the
body's collar rim (§5.2). No mechanical or magnetic closure feature is modeled into either part;
see §6 for what changed and why.

**v5 flag — the `neck-fit-test` article is easy to overlook and MUST NOT be forgotten this round.**
This is a small standalone part (currently ~35mm tall, ~122mm max OD — just the neck-taper + collar
section, flange-cut at the bottom for bed stability, open bore both ends) built specifically so the
requester can physically test whether a real crematorium remains bag fits through the neck opening.
It exists in `step/`, `3mf/`, and `stl/` alongside the body and lid files, but was **not** previously
listed in this table — an oversight in earlier revisions being corrected now, precisely because this
revision's whole trigger (§4.4) is a neck-fit concern. **It represents the OLD 58mm ID / 66mm OD
neck / 78mm OD collar geometry and does NOT reflect this revision's target numbers.** It must be
rebuilt at the new **80mm ID / 88mm OD neck / 100mm OD collar** dimensions (§4.2.2, §6.2) — the same
collar height (15mm) and general flange-test-article construction can otherwise be reused. If this
file is left at its old dimensions, the requester's physical fit test will validate the wrong
opening size and give a false sense of confidence about a geometry that no longer matches the body.

---

## 3. Printer constraints (stated up front)

| Constraint | Value | Tag |
|---|---|---|
| Printer | P2S-class FDM | Per task instruction / user memory |
| Build volume | 256 × 256 × 256mm | Per user memory (`user_printer_specs.md`) |
| Nozzle diameter | 0.4mm (assumed standard) | ESTIMATED — not explicitly confirmed this session, standard shop default per every prior spec in this repo |
| Minimum wall/boss thickness implied | ≥0.8mm (2× nozzle) for any wall or boss under load | Computed from the line above |
| Body fits build volume? | ~154mm max OD × **153.5mm H** (v5 — height trimmed from v4's 160mm to compensate for the neck-widening volume gain, §4.2.2; max OD unchanged, belly untouched) | **Yes**, by a large margin on every axis (§4) |
| Lid fits build volume? | **100mm max OD** × 49mm H (v7 — see §5.1). Brim shrunk to 100mm and now sits flush with the 100mm collar (zero overhang, §5.1/§5.2); handle removed entirely (§7); total bounding-box height dropped from v6's 85mm to **≈49mm** (39mm brim-to-plateau stack + 10mm plug hanging below the underside reference plane) — a **-42% reduction**, still trivially clears 256mm. | **Yes**, by a large margin on every axis (§5) |

Body and lid are separate parts, so — per the task framing — the combined assembled height does
**not** need to fit the bed in one shot. **As of v7, combined assembled height (body rim + lid
above its seating plane) is ≈192.5mm** (153.5mm body + 39mm lid, §5.1) — down from ≈228.5mm at v6
and the ≈235mm figure cited in earlier passes of this document, entirely because of the v7 handle
removal and lid resize (§5.1, §13 v7). Each part individually clears 256mm on every axis with well
over 90mm of margin regardless; bed fit is not, and has never been, a binding constraint on this
design.

Every wall/collar/plug/brim dimension chosen in §§4–6 is checked against the 0.8mm minimum at the
end of each section — none of them come close to that floor; the thinnest feature in the whole
design (4mm nominal body wall) is 5× the minimum. (The handle, previously the other dimension
checked here, no longer exists as of v7 — see §7.)

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

---

**Status as of v5 — the ≈1579 cm³ target itself does NOT change, but the geometry that has to hit
it does.** Market-benchmarking research found the 58mm neck ID to be a significant outlier versus
comparable pet urns (114–121mm top openings) and even a direct 3D-printed competitor (~70–100mm
estimated). The requester has set a new **80mm neck ID** target — a deliberate compromise short of
the full 100mm considered, chosen specifically so the collar OD does not end up wider than the
98mm base OD. Widening the neck/collar bore adds internal volume near the top of the body; per the
requester's explicit instruction, this is compensated by **trimming the body's overall height**
(160mm → 153.5mm) rather than letting capacity climb, so the ≈1579 cm³ target is held rather than
moved. **Full re-derivation in the new §4.2.2 below — do not build against the pre-v5 neck/collar
numbers (58mm ID / 78mm OD / 160mm height) anywhere in this document; they are superseded.**

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

This subsection is the **current source of truth for the v4 as-built body** (belly geometry, wall
thickness, cavity/material volumes) — superseding the frustum estimate in §4.2 above. **As of v5,
the collar (OD/ID) row and the "160mm total height" figures below are superseded by §4.2.2** — the
belly/wall/volume figures in this table remain the correct starting baseline that §4.2.2's v5
derivation builds from (see §4.2.2's explicit use of the 1579 cm³ figure below as its baseline).

> **v8 (2026-09-10) — body profile below P3 reshaped for a rounder silhouette (see the new
> §4.2.3).** The cavity / material / belly / wall figures in the table below are the **v7 as-built
> baseline** and are exactly the starting point §4.2.3's v8 volume delta-calc builds from — same
> method §4.2.2 used for the v5 neck-widening (verified baseline + hand-calc delta for only the
> region that moved). v8's hand-calc cavity estimate is **≈1608 cm³ (+1.8% vs the ≈1579 cm³
> target, inside the ±5% band)**. This table is **not** updated to v8 numbers until the Coder
> rebuilds the body and the Tester independently re-measures — `parameters.md` likewise stays at
> as-built v7.
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

### 4.2.2 v5 re-derivation — neck/collar widening (58mm→80mm ID) and compensating height trim

**This subsection is now the current source of truth for the neck/collar/height numbers**,
superseding the 58mm ID / 78mm OD collar / 160mm total height used everywhere above and in
§4.2.1. Nothing about the belly (76.97mm ext. radius / 72.97mm int. radius, ~4mm wall) or the base
(98mm OD) is touched — both are explicitly out of scope for this change and are carried forward
unchanged from §4.2.1/§4.3.

> **v8 (2026-09-10):** P3 and everything above it — **neck ID 80mm, neck OD 88mm, collar OD 100mm
> / ID 80mm / 10mm wall / 15mm band, the P3→P4 external blend, the whole constant-diameter bore —
> are byte-identical to v7 and are NOT touched by v8.** v8 reshapes only the base→belly→shoulder
> region below P3 for a rounder silhouette (§4.2.3). P3's position (Z_ext 138.5mm), radius
> (internal 40mm / external 44mm) and dr/dz→0 tangent condition are all held exactly as in this
> §4.2.2 table. The neck-widening derivation below is unaffected.

| Feature | Old (v4) | New (v5) | Tag |
|---|---|---|---|
| Neck ID (constant through collar) | 58mm (r=29mm) | **80mm (r=40mm)** | Requester's explicit target — a deliberate compromise short of the 100mm initially considered, chosen so the collar OD doesn't exceed the 98mm base OD |
| Neck OD, below collar (at P3) | 66mm (r=33mm) | **88mm (r=44mm)** | DERIVED — 80mm ID + 2×4mm nominal wall (holds the existing wall convention used everywhere else in the profile) |
| Collar ID | 58mm | **80mm** | Matches the new neck ID (constant bore through the collar, same convention as v1–v4) |
| Collar OD | 78mm (r=39mm) | **100mm (r=50mm)** | DERIVED — 80mm ID + 2×10mm reinforcement wall. The requester explicitly chose to **keep** the 10mm reinforcement wall (not revert to the nominal 4mm) even though it no longer houses magnets — it now serves purely as a lid-seating/reinforcement band, kept for structural margin and rim character (same reasoning as v3's §6.2 decision, just re-affirmed at the new size) |
| Collar wall thickness | 10mm | **10mm — unchanged** | Requester's explicit decision |
| Collar height | 15mm | **15mm — unchanged** | Not part of this change; only ID/OD are being resized |

#### Base-vs-collar proportion check

**Base OD (98mm, r=49mm) vs. new collar OD (100mm, r=50mm): a 2mm diameter difference (1mm radius
difference) — essentially at parity, not a meaningful top-heavy proportion.** The widest point of
the vessel remains the belly (153.9mm OD), which is far wider than either the base or the collar,
so the base-to-belly-to-collar silhouette keeps a low visual/physical center of gravity. **No
base-widening compensation is needed** — confirmed once working with the real target numbers above,
per the requester's own expectation.

#### Volume delta from the neck/collar widening (frustum-approximation method, same technique used throughout this project's hand-calcs)

The as-built v4 cavity (≈1579 cm³) was produced by manual belly sculpting, not a clean parametric
spline — §4.2.1 explicitly declined to re-derive it from a fresh hand-calc for that reason ("a
hand-calc against sculpted geometry would only be a rough approximation of an approximation").
That reasoning still applies here, so this derivation does **not** attempt to rebuild the whole
1579 cm³ figure from scratch. Instead, it computes the **volume added specifically by the neck/
collar ID change**, holding the shoulder (P2) and all segment heights fixed, and applies that delta
to the known-good, three-times-independently-verified 1579 cm³ baseline. This isolates the actual
geometry change from the sculpted region's un-recomputable shape, and is the more defensible
hand-calc method available at spec time.

**Correcting a stale figure found in the process:** §4.2.1/`parameters.md` carry a shoulder (P2)
internal radius of ~57mm alongside a Reviewer-corrected external radius of 46.42mm — but 57mm
internal is larger than 46.42mm external, which is geometrically impossible (that would require a
negative wall thickness). The 57mm figure is a stale leftover from the pre-v4 profile (57mm
internal + the original 4mm wall ≈ 61mm external, matching the *other* stale figure — 122mm OD/
61mm radius — that the Reviewer already flagged and corrected on the external side only). **For
this derivation, the shoulder internal radius is corrected/estimated at ~42.42mm** (46.42mm
verified external − the ~4.00mm wall thickness independently verified at this exact Z-height by
three parties, per §4.2.1's Z=10–140mm sampling range, which covers Z=119). This is `ESTIMATED`,
not independently re-measured on real CAD — **flagged explicitly for the Coder to re-verify the
true internal shoulder radius against the actual rebuilt geometry**, and to adjust the height trim
below by the same delta method if it differs meaningfully (the ±5% tolerance convention applies
here exactly as everywhere else in this project).

Using `V = (π·h/3)(r1²+r1·r2+r2²)` for the internal cavity, holding P2 (r1=42.42mm) and both
segment heights (26mm taper, 15mm collar) fixed, only changing P3/P4 (r2):

| Segment | r1 → r2 (old) | r1 → r2 (new) | h | V (old) | V (new) | ΔV |
|---|---|---|---|---|---|---|
| Shoulder→neck-taper-end (P2→P3) | 42.42→29mm | 42.42→**40mm** | 26mm | 105.37 cm³ | 138.76 cm³ | **+33.39 cm³** |
| Collar bore, straight cylinder (P3→P4) | 29mm (const.) | **40mm** (const.) | 15mm | 39.63 cm³ | 75.40 cm³ | **+35.77 cm³** |
| **Total added by neck/collar widening** | | | | | | **+69.16 cm³** |

```
New total (before height trim) = 1579 cm³ (verified v4 baseline) + 69.16 cm³ = 1648.16 cm³
Deviation from 1579 cm³ target: +4.38% — inside the ±5% routine band on its own, but the
requester explicitly directed a height trim rather than letting capacity climb, so one is applied
below regardless of whether it's strictly required by the tolerance band.
```

#### Compensating height trim

**Where the trim is taken from, and why:** the belly-apex-to-shoulder segment (P1→P2, currently
50mm tall, ~535 cm³) is the single largest-volume segment in the profile and the only one that can
absorb a "slight" trim without a large relative change — trimming the same ~69 cm³ out of the much
smaller shoulder-to-neck-taper segment (26mm tall) would require removing exactly half of it
(~13mm), a much bigger structural change than "slightly trimming height." Taking the trim from
segment 2 also keeps the base→belly flare (P0→P1, self-supporting, unchanged) and the belly apex
itself (radius, plateau shape) completely untouched — only the belly-to-shoulder descent gets
shorter, and the shoulder/neck/collar shift down with it.

Segment 2's frustum volume is linear in height (r1=72.97mm, r2=42.42mm fixed as endpoints):

```
dV/dh = (π/3)(r1² + r1·r2 + r2²) = (π/3)(5324.62 + 3095.39 + 1799.46) = (π/3)(10219.47)
      ≈ 10.702 cm³/mm

Required trim: ΔH = 69.16 cm³ ÷ 10.702 cm³/mm ≈ 6.46mm

Chosen (rounded, practical) trim: ΔH = 6.5mm → new total height = 160 − 6.5 = 153.5mm
Volume removed at 6.5mm: 6.5 × 10.702 ≈ 69.56 cm³
New estimated total: 1648.16 − 69.56 ≈ 1578.6 cm³  →  −0.03% vs. the 1579 cm³ target
```

**This 1578.6 cm³ figure is a hand-calculated ESTIMATE**, built from a real, verified baseline
(1579 cm³) plus two frustum-approximated deltas — not a fresh from-scratch volume derivation of the
whole body. It should track the eventual as-built CAD volume more closely than a full-rebuild
hand-calc would (because the un-recomputable sculpted belly/shoulder region is never touched by
this delta, only referenced by its already-verified radius), but it is **not** a substitute for the
Coder's own CAD mass-properties query once the new geometry actually exists. **Per this project's
own standing rule: verify against the real model, and flag back for a further micro-adjustment
(a slight tweak to the segment-2 height) if the built cavity falls outside the ±5% band around
1579 cm³** — exactly the same convention used in every prior round of this spec.

#### Re-derived profile — full control-point table (v5, supersedes §4.2/§4.2.1's P0–P4 table)

| Point | Z from base (v5) | Z from base (v4, old) | % of new 153.5mm height | Internal r | External r | Notes |
|---|---|---|---|---|---|---|
| P0 — floor/base | 5mm | 5mm | 3.3% | 45mm | 49mm (98mm OD) | **Unchanged** |
| P1 — belly apex (plateau) | ~69mm (plateau 66.9–71.4mm, absolute Z **unchanged**) | ~69mm (plateau 66.9–71.4mm) | **~45.0%** (plateau ~43.6–46.5%) | 72.97mm | 76.97mm | **Unchanged in mm** — only the % figure moves, because the denominator (total height) shrank while this segment's own position didn't |
| P2 — shoulder | **112.5mm** (moved down 6.5mm) | 119mm | 73.3% | ~42.42mm (corrected estimate, see above — **ESTIMATED**, needs Coder re-verification) | 46.42mm (Reviewer-verified, v4) | Height trim applied entirely to the P1→P2 segment (50mm → 43.5mm) |
| P3 — neck-taper-end / base of collar | **138.5mm** | 145mm | 90.2% | **40mm** (was 29mm) | **44mm** (was 33mm) | ID/OD widened per target above; P2→P3 segment height held at **26mm, unchanged** |
| P4 — rim / top of collar | **153.5mm** (= new total height) | 160mm | 100% | **40mm** (was 29mm) | **50mm** (was 39mm) | Collar height held at **15mm, unchanged**; internal bore constant-radius through the collar, same convention as before |

**Belly position, restated in both terms as requested:** the belly apex sits at an **unchanged
absolute height (~69mm from the base, plateau spanning 66.9–71.4mm)**, but now reads as
**~45.0% of the new 153.5mm total** (plateau ~43.6–46.5%) — up from ~43–44% of the old 160mm
total. The belly itself did not move or change shape; only the total height it's being measured
against got shorter.

#### Neck-to-collar external blend — re-checked, not assumed unchanged (feeds §9)

See §9 for the full overhang re-check. Short version: the external radius **delta** driving this
blend (collar OD minus neck OD) is **unchanged at 6mm on radius** in both the old (39−33mm) and new
(50−44mm) designs — a direct consequence of the requester's decision to keep the same 10mm collar
wall over the same 4mm nominal neck wall. Holding the blend's height span unchanged too (the same
7mm out of the 15mm collar height used in the v4 construction, §2.3 of `parameters.md`), the
resulting blend curve — built with the same tangent-constrained-cubic-Bezier method, zero slope at
both ends — is a function only of (Δr, Δz, method), none of which changed. **The peak overhang
angle at this transition is therefore expected to stay ~47.25°, at the same relative position
within the blend (now Z≈140.75mm instead of Z≈147.25mm, shifted down by the same 6.5mm as the rest
of the collar/neck)** — not worse, not better, just relocated. This is a reasoned estimate from
geometric invariance, not a fresh CAD measurement — flagged for Coder confirmation once built,
exactly like every other angle figure in this document.

### 4.2.3 v8 body-profile revision (2026-09-10) — rounder "thrown-ceramic" silhouette

**Scope / authority.** The requester approved a rounder body silhouette for Large from the mockup
`concept/v8-rounder-body.png` — explicit words: *"The large body is approved."* This is the
**third** size to get this treatment; Small (`small/dot_pipeline/specs.md` §7.7) and Medium
(`medium/dot_pipeline/specs.md` §4.7) got the identical three-move recipe first, and this
subsection mirrors it. It is a focused aesthetic revision, **not** a from-scratch re-derivation:
it reshapes the body profile **below P3 only**.

**Held fixed — do not move (per the revision brief's hard constraints):** overall body height
**153.5mm**; belly max OD **153.9mm** (external r 76.966mm, internal r 72.966mm) at its current
absolute height (Z_ext ≈ 69mm, plateau Z_ext 66.9–71.4mm); base OD **98mm** (external r 49mm);
nominal wall **4mm** (inner wall tracks the new rounder outer profile at the same constant
offset); floor **5mm**; and **everything at or above P3** — neck ID 80mm, neck OD 88mm, collar OD
100mm / ID 80mm / 10mm wall / 15mm collar band, the P3→P4 external blend, the bore — all
**byte-identical to v7**. Unlike Small, Large's base is **not** narrowed: Large's belly-to-base
delta (153.9 vs 98mm, belly is +57% wider) is already large enough that the rounder belly reads
fine without touching the base.

**The three moves (identical in kind to Small/Medium):**

1. **Belly (P1) — from "broad plateau" to a gentle broad swell.** Position and radius **unchanged**
   (Z_ext 69 / Z_int 64; internal r 72.966 / external r 76.966; still the single max-OD point).
   The P1 tangent-handle magnitudes are **lengthened** so curvature is spread smoothly through the
   apex instead of running flat across a ~4.5mm plateau and then breaking away. Target profile
   radius-of-curvature at the belly apex **≈38mm** — a full rounded swell on a 77mm-radius body
   (Medium used ≈30mm on its 60.2mm-radius body; 38mm ≈ that same ratio scaled to Large). **P1
   tangent stays horizontal (dr/dz = 0) and the handles must not overshoot** — the belly apex
   remains the single maximum-radius point at exactly 76.966mm external; the Coder must confirm the
   revolved body's max OD is 153.9mm ±0.1 and occurs at the belly, not above or below it.

2. **Shoulder (old P2) — demoted from a shape-driving inflection with a tangent break to a gentle
   curvature-continuous (G2) witness on one fair curve from base to neck.** This is the move that
   carries the volume risk for Large, so it is quantified precisely:

   **Which way does Large's v7 shoulder sit relative to its own P1–P3 chord?** The P1–P3 internal
   chord runs from (Z 69, r 72.966) to (Z 138.5, r 40.0), slope dr/dz = −0.4743. At the shoulder
   height Z_ext 112.5 the chord radius is **52.33mm**. The v7 as-built shoulder internal radius is
   **42.42mm** (VERIFIED, Tester R43). So Large's v7 shoulder sits **≈9.9mm INSIDE its own P1–P3
   chord** — a deep concave pinch, and the **deepest of the three sizes** (Medium pinched ~3.7mm
   inside; Small *bulged* ~2.3mm outside). This is the same geometry documented as the
   "ginger jar" / "belly-pinch" concept-fidelity drift at v4 (§10 v4 note; `parameters.md` §10) —
   v8 is, in effect, the correction of that drift. Because Large pinches inside (like Medium, only
   much more so), **smoothing the shoulder ADDS volume** (Medium gained ~+26 cm³ and went to +3%;
   Small *lost* ~5 cm³). See the volume math below for how much, and why Large cannot be
   de-pinched as fully as Medium/Small without leaving the band.

   **Revised P2 (v8) — a retained soft-shoulder witness, not a sub-mm one:**
   - **Internal radius 45.0mm** (external OD ≈ 98.0mm), at Z_ext **112.5mm** (Z_int 107.5mm) —
     **Z unchanged from v7** (deliberately not moved, to avoid adding a second volume lever;
     Medium moved its witness, Large does not because Large is band-constrained).
   - This sits **≈7.3mm inside the P1–P3 chord** (chord internal r 52.33 at this height − 45.0).
     Larger than Medium's 0.75mm and Small's 0.9mm retained offset — a real, deliberate difference,
     forced by the volume band (below), not an oversight.
   - Tangent **dr/dz = −0.474** (matched to the P1–P3 chord direction, ≈25.4° from vertical),
     **matched on both sides, G2 (curvature-continuous)**. The **tangent break is removed** — the
     single unavoidable belly-convex → neck-concave curvature reversal is now one gentle,
     distributed inflection near P2, **no kink**. The profile reads as one flowing curve from foot
     to collar; v8's shoulder is a gentle broad narrowing, not a corner and not a plateau-then-drop.

3. **Foot — sharp base edge eased into a rounded foot.** New **external foot fillet radius 7.0mm**,
   tangent to the flat underside and to the near-vertical foot wall (external r 49.0). New
   **internal floor-to-wall fillet radius 5.0mm** (= floor thickness, the same "fillet radius =
   floor thickness" rule Small used at R3 and Medium at R4; this pins the vague "equivalent to a
   ≈10mm fillet" language in §4.3 to an explicit value — cavity effect is within hand-calc noise,
   ±2 cm³). Radii follow the Small (R5 ext / R3 int) → Medium (R6 ext / R4 int) → **Large (R7 ext /
   R5 int)** progression. Base OD stays **98mm**, now first reached at the top of the fillet arc
   (Z_ext ≈ 7mm). **Disclosed consequence — ground-contact footprint:** the flat ground-contact
   ring shrinks from ≈98mm dia (v7 near-sharp base edge) to **≈84mm dia** (2 × [49 − 7]) — a ~14%
   diameter / ~26% area reduction. Contact-OD : height = 84 / 153.5 = **0.55** (was 0.64 at v7),
   essentially the same as Medium's v2 ratio (0.58) and still a stable footprint for a
   shelf-display vessel with a low centre of gravity (the belly, the widest point, sits low) under
   a static bagged-remains payload. Flagged, not hidden; not a blocker.

**v8 control-point table** (internal radii drive the cavity; external = internal + 4.0mm nominal
wall on the body sides, + foot fillet at the base, + the unchanged 10mm collar reinforcement above
P3 — exactly as v7):

| Point | Z_int | Z_ext | Internal r | External r | Tangent condition (profile plane) | Handle magnitudes |
|---|---|---|---|---|---|---|
| P0 — floor/base | 0 | 5 | 45.0 | 49.0 | dr/dz = 0 (wall vertical); foot fillets **R7 ext / R5 int** | up-handle ≈ 26mm |
| P1 — belly swell apex | 64 | 69 | 72.966 | 76.966 | dr/dz = 0 (wall vertical at max OD; **no overshoot** — single max-OD point at 153.9mm) | down-handle ≈ 26mm, up-handle ≈ 20mm — long, for a broad swell (target apex R-of-curvature ≈ 38mm) |
| P2 — soft shoulder (retained G2 witness) | 107.5 | 112.5 | **45.0** | **≈98.0 OD (r 49.0)** | dr/dz = −0.474 (≈25.4° from vertical, = P1–P3 chord direction), matched both sides, **G2** | ≈ 21mm toward P1, ≈ 12mm toward P3 |
| P3 — neck-taper-end | 133.5 | 138.5 | 40.0 | 44.0 | dr/dz → 0 — **UNCHANGED from v7** | ≈ 12mm toward P2; collar side straight |
| P4 — rim / top of collar | 148.5 | 153.5 | 40.0 | 50.0 | Constant r internally — **UNCHANGED from v7** | — |

**Coder construction:** build the outer profile as a single **G2-continuous chained-cubic spline
P0→P1→P2→P3**, revolved 360°, then verify the curvature comb shows (a) no cusp anywhere, (b)
exactly one gentle curvature-sign change (near P2), (c) no localized curvature spike at P1 or P2.
Offset inward 4.0mm for the inner profile, holding the 5mm floor, the R5 internal foot fillet, and
the 10mm collar reinforcement above P3 exactly as v7. The R7 external foot fillet is a separate
tangent fillet feature on the outer wall at the base.

**Volume hand-calc — delta-from-verified-baseline method (per §4.2.2's v5 precedent, not a
from-scratch rebuild).** A full frustum chord-sum through the v8 control points comes to
≈1420 cm³ — ~160 cm³ *below* the verified v7 CAD cavity (≈1580 cm³). That gap is the
un-recomputable sculpted-belly bias §4.2.1 already documented (the manual v4 belly edit bulges far
outside any straight chord). So, exactly as §4.2.2 did for the neck-widening, the estimate is
**verified v7 baseline + the frustum chord-sum delta for only the region that moved (P1→P3) +
small fairing/fillet corrections**:

| Segment (internal) | v7: r1→r2 (h) | v7 V | v8: r1→r2 (h) | v8 V | ΔV |
|---|---|---|---|---|---|
| P1→P2 | 72.966→42.42 (43.5mm) | 465.48 cm³ | 72.966→**45.0** (43.5mm) | 484.35 cm³ | **+18.87** |
| P2→P3 | 42.42→40.0 (26mm) | 138.76 cm³ | **45.0**→40.0 (26mm) | 147.71 cm³ | **+8.95** |
| **P1→P3 total** | | 604.24 cm³ | | 632.06 cm³ | **+27.82 cm³** |

```
Fairing/fillet corrections (all small, partially offsetting — same treatment as Small/Medium):
  + lower flank (long P0→P1 handles bulge slightly outside the chord)      ≈ +2 to +3 cm³
  − belly apex rounding (plateau → swell curves away from max radius)      ≈ −1 to −2 cm³
  − upper flank (P1→witness sits just inside its local chord)              ≈ −1 to −2 cm³
  ± internal foot fillet pinned to R5 (vs v7's vague "≈10mm" corner)       ≈ ±2 cm³ (noise)
  Net corrections ≈ 0 ± 4 cm³

v8 faired hand-calc ≈ 1580 + 27.8 + 0  ≈  1608 cm³   (uncertainty band ≈ 1600–1618)

vs the ≈1579 cm³ binding target (§4.1) → +1.8%.
±5% band = ±5% of 1579 cm³ = ≈1500–1658 cm³ (the spec states the band as a percentage — §4.1,
§4.2.2 — not as explicit cm³ endpoints; computed here). → INSIDE, ~50 cm³ under the ceiling.
Back-check: 1608 ÷ 16.3871 ≈ 98.1 in³ (target was a 90 in³ minimum; already exceeded since v4 by
deliberate decision — v8 does not change that posture).
```

**Why Large's witness is held ≈7.3mm inside the chord and not sub-mm like Small/Medium.** A full
Medium/Small-style de-pinch — witness ~1mm inside the chord (internal r ≈ 51.3 at Z 112.5) — was
hand-calc'd both ways: the P1→P3 frustum delta comes to **+99.8 cm³**, cross-checked by a
shell-integral of the pinch void (≈112 cm³). That lands the cavity at **≈1680 cm³ → +6.4% →
OUTSIDE the ±5% band** (~22 cm³ over the 1658 cm³ ceiling). Large's v7 pinch is ~2.7× deeper than
Medium's and the body is ~1.5× the linear scale, so the same move that nudged Medium to a
comfortable +3% overshoots on Large. The retained **r 45.0 witness** removes the *kink* (G2, one
fair curve) and fills in most of the pinch, while giving back only ~+28 cm³ — enough headroom to
absorb the hand-calc→CAD surprise the belly-swell fairing may add, which for Large runs in the
*adding* direction.

**Fallback lever — within the reshaped region only (same as Small/Medium's revisions):** the
witness internal radius is the single volume lever. Sensitivity ≈ **±11 cm³ per ±1mm** of witness
radius in the r 43–48 range.
- If the real CAD cavity comes back **> ~1650 cm³**: deepen the P2 witness toward v7's internal
  r 42.42mm (each −1mm ≈ −11 cm³; r 42.42 ≈ returns to the v7 cavity). Still G2, still one fair
  curve — just a slightly more retained soft shoulder.
- If the real CAD cavity comes back **< ~1560 cm³** (not expected — v8 adds volume): shallow the
  witness toward internal r 47.5mm (≈+28 cm³ vs r 45; still ≈4.8mm inside the chord, still in band
  with ~22 cm³ ceiling margin) and/or lengthen the P1 down-handle toward P0 to fatten the swell.
- **Do NOT** move any fixed constraint (153.5mm height, belly OD, base OD, P3, 4mm wall) to chase
  the band — those are hard-held this revision.

**Print orientation, overhang, foot-fillet watch item:** unchanged — see the v8 note added to §9.
Base-down remains correct; the faired lower body rises to an estimated ~32–35° from vertical (was
~24° as a single chord) — comfortably self-supporting; belly→witness→P3 stays shrinking-radius
(self-supporting regardless of local angle) and is marginally *gentler* than v7's pinched descent
(~32.7° vs ~35.1° average external angle over that span). **One new minor first-print watch
item:** the underside of the R7 external foot fillet — its bottom ~2.05mm (= R·(1−cos45°)) sits
below 45° right on the build plate. Routine for any rounded/chamfered foot; a few bridged layers
with at most minor cosmetic sag on a downward-facing edge. Scales consistently with Medium's
~1.8mm (R6) and Small's ~1.5mm (R5). The neck-to-collar external blend zone (the one flagged
~45.6–47.25° zone, Z 138.5–145.5mm) is above P3 and byte-identical to v7.

**Lid / plug / neck-fit-test — unaffected, no rebuild (reasoning confirmed).** The lid (v7: capped
alignment plug, flush 99.700mm brim, flattened 21.73mm dome plateau), the plug, and
`neck-fit-test` are defined **entirely** by geometry at or above P3: the 80mm neck ID (the bore
the 79.5mm-OD plug enters and the opening a remains bag passes through), the 100mm collar OD /
80mm ID / 10mm wall / 15mm band, the flat collar rim seating face at Z_ext 153.5, and the P3→P4
external blend. v8 changes **nothing** at or above P3 — P3's position, radius and tangent are
byte-identical to v7, and the whole bore + collar band + blend are untouched. Therefore
`urn-lid.{step,3mf,stl}`, the plug, and `neck-fit-test.{step,3mf,stl}` are **not** rebuilt or
re-exported. This holds for the same reason it held on Small (§7.7) and Medium (§4.7).

**Coder deliverables for v8:** rebuild **only** `pet-memorial-urn/step/urn-body.step`,
`pet-memorial-urn/3mf/urn-body.3mf`, `pet-memorial-urn/stl/urn-body.stl`. The hero render
(`pet-memorial-urn/render/pet-memorial-urn-hero.png`) should be re-shot once the v8 body exists
(the silhouette changes visibly), as a post-rebuild step, same as prior revisions. `parameters.md`
stays at as-built v7 figures until the Coder rebuilds and the Tester re-verifies.

**Provenance tags for the v8 numbers:** belly apex radius/height — VERIFIED (carried from v4/v5,
unchanged). P3/P4 radii and Z, collar band — VERIFIED (carried from v5, unchanged). Base OD, wall,
floor, height — carried unchanged (VERIFIED as-built / ESTIMATED design convention, as tagged in
§4.3). **Revised P2 witness internal r 45.0mm / tangent −0.474 / G2 — `DERIVED — sizing
decision`** (chosen to de-kink the shoulder while holding the cavity inside its band). **Foot
fillets R7 ext / R5 int — `ESTIMATED`** (proportioned from the Small/Medium progression, a
design-convention scale, not a hard derivation). **Target belly apex radius-of-curvature ≈38mm —
`ESTIMATED`**. **v8 cavity estimate ≈1608 cm³ — hand-calc ESTIMATE** (verified v7 baseline +
frustum delta + fairing corrections), to be replaced by the Coder's CAD mass-properties query on
the real rebuilt geometry.

**Open items flagged for the requester:**
1. **Large cannot be de-pinched as fully as Small/Medium within the current constraints.** v8
   removes the shoulder kink (G2, one fair curve) but retains a ≈7.3mm-inside-chord soft shoulder,
   because the near-pure fair curve Medium/Small got would put Large's cavity at ~+6.4% — outside
   the ±5% band. Matching Medium's fuller fairing on Large would require relaxing exactly one
   hard-held constraint: **(a)** accept a cavity ~+6% over target (there is a direct precedent —
   the requester accepted +6.85% at v4), **(b)** trim body height ~3mm (v5-style compensation), or
   **(c)** thin the wall locally below 4mm. The revision brief authorizes none of these, so v8
   ships the in-band partial de-pinch. **Does the requester want the fuller fairing at one of
   those three costs, or is the in-band soft shoulder acceptable?**
2. **Hand-calc → CAD confidence is lower for Large than for Small/Medium.** Large's frustum
   hand-calc under-reads the sculpted belly by ~13% on the absolute, so the v8 estimate leans on
   the delta method (which cancels most of that bias). The real CAD cavity could still land
   somewhat off ≈1608 cm³; the flag-back triggers above cover both directions. Not a blocker,
   standard for this project.
3. **Band anchoring.** The ±5% band is computed here as ±5% of the ≈1579 cm³ target (≈1500–1658
   cm³); the spec never wrote explicit cm³ endpoints. If the Reviewer prefers it anchored on the
   as-built ≈1580.25 cm³ instead, the numbers move by <2 cm³ and nothing in this analysis changes.

### 4.3 Body external dimensions (wall thickness applied) — REVISED, see §13 v5 (v4 figures superseded for the neck/collar/height rows)

> **v8 (2026-09-10) — rounder body profile below P3, see §4.2.3.** Rows changed by v8: the
> **shoulder row** (P2 at Z_ext 112.5 — internal r goes from 42.42mm to a retained-witness
> **45.0mm**; external OD ~92.8mm → **~98.0mm**; tangent break removed, now G2-continuous).
> **New features:** external foot fillet **R7** (flat ground-contact ring shrinks from ≈98mm to
> **≈84mm** OD) and internal floor-to-wall fillet **R5** (pins the vague "≈10mm equivalent"
> corner-round language below to an explicit value). **Unchanged by v8:** 153.5mm height, 98mm
> base OD, 153.9mm belly OD / ext r 76.966mm, 4mm wall, 5mm floor, and every neck / collar / P3 /
> P4 row. The belly row's Z/plateau/percentage figures are unchanged (only the plateau becomes a
> broad swell — same radius, same height).

| Parameter | Value | Tag |
|---|---|---|
| Nominal wall thickness (body sides) | **4mm** design target; **~4.00mm as-built (verified 3.98–4.03mm across ~60 sampled heights, v4)** | The 4mm figure itself remains ESTIMATED (a design convention, chosen for perceived heft/"doesn't feel like plastic," §8, not a print-minimum — 5× the 0.8mm floor). **As-built achievement of that target is now VERIFIED** (§4.2.1) as of v4; **not yet re-verified against v5's neck/collar rework**, which does not touch this wall region. |
| Floor thickness | **5mm** | ESTIMATED — slightly thicker than the side wall for base stability and to support the settled weight of the remains bag over years on a shelf. Unchanged from v1. |
| External base OD (at P0) | **98mm — unchanged in v5**, confirmed at parity with the new ~100mm collar OD (§4.2.2) | DERIVED (internal 90mm + 2×4mm wall). Unchanged from v1; confirmed unchanged again in v4 and v5. |
| External max belly OD (at P1, `Z ≈ 66.9–71.4mm`, **~45.0%** of the new 153.5mm height — v5) | **~153.9mm** (2 × 76.97mm) — **unchanged in v5**, only its % position moved (§4.2.2) | VERIFIED (v4) — supersedes the v2 estimate of 146mm; see §4.2 footnote for the measurement basis. |
| External OD at shoulder (at P2, `Z = 112.5mm` in v5, was `Z=119mm` in v4) | **~92.8mm** (46.42mm radius, external unchanged); **internal radius corrected/estimated at ~42.42mm in v5** (§4.2.2 — the previously-carried 57mm internal figure was geometrically impossible next to the 46.42mm external figure and is corrected here) | External: VERIFIED (Reviewer-measured, v4). Internal: `ESTIMATED` in v5 (derived from external minus verified wall) — **flagged for Coder re-verification against the rebuilt CAD.** Z-position moved down 6.5mm in v5 as part of the height-trim compensation (§4.2.2). |
| External OD, neck at base of collar (at P3, `Z=138.5mm` in v5, was `Z=145mm`, below the reinforced collar band, see §6) | **88mm** (r=44mm) — **v5, up from 66mm** | DERIVED — 80mm new neck ID + 2×4mm nominal wall (§4.2.2). |
| Internal opening ID (constant through the collar) | **80mm** (r=40mm) — **v5, up from 58mm** | Requester's explicit target (§4.2.2) — market-research-driven, a deliberate compromise short of 100mm. |
| Collar OD (at P4, top of collar/rim) | **100mm** (r=50mm) — **v5, up from 78mm** | DERIVED — 80mm ID + 2×10mm reinforcement wall, kept at the requester's explicit instruction (§4.2.2, §6.2). |
| **Overall external height, base to top of neck rim** | **153.5mm** (5 + 64 + 43.5 + 26 + 15) — **v5, down from 160mm** | DERIVED — height trim compensating for the neck-widening volume gain, holding cavity volume near the ≈1579 cm³ target (§4.2.2). All of the trim (6.5mm) came out of the belly-to-shoulder segment; base, belly, neck-taper height, and collar height are otherwise unchanged. |

Internal floor/wall corner: previously called out as a standalone **10mm fillet radius**. Superseded
by the P0 horizontal-tangent condition in the spline method above, which produces the equivalent
rounding as part of the profile itself rather than as a separate feature. If the fallback
straight-segment method is used instead, reinstate a ≥10mm fillet at this corner specifically.
**Unaffected by v5.**

### 4.4 Neck opening size — named risk (REVISED, v5 — significantly de-risked, not fully closed)

**Internal opening ID is now 80mm (~3.15in), up from 58mm (~2.3in) as of this revision.** This was
the direct trigger for this spec revision: competitor benchmarking found 58mm to be a significant
outlier against comparable pet urns (114–121mm top openings) and even a direct 3D-printed
competitor (~70–100mm estimated opening). 80mm is a deliberate compromise — short of the full
100mm initially considered, chosen specifically so the collar OD doesn't exceed the 98mm base OD
(§4.2.2) — but it lands within, not below, the ~70–100mm range the closest 3D-printed competitor
was estimated at, which meaningfully reduces (without eliminating) the risk that a real
crematorium remains bag won't pass through comfortably.

**This is still not independently verified against a real filled cremation bag, and is still
tagged `ESTIMATED`.** The risk is smaller than it was at 58mm, not closed — flagging plainly rather
than treating "we made it a lot bigger" as equivalent to "we tested it." **The `neck-fit-test`
standalone article (see the new note in §2 and §13 v5) exists specifically so the requester can
physically test this — it must be rebuilt at the new 80mm ID / 88mm OD neck / 100mm OD collar
dimensions before that test is meaningful; the old 58mm-ID test article does not represent the
current design.** If a real bag still turns out too bulky/stiff even at 80mm, the fix is the same
as before: widen the neck/collar ID further in a future spec revision — it does not require
resizing the whole body.

---

## 5. Lid dimensions and the lid/body seating interface

### 5.1 Lid geometry — REVISED, v7 (brim shrunk flush with the collar, thickened, dome base re-derived, handle removed, apex flattened; see §13 v7)

**Full lid rework, shown with the same rigor as the original derivation** — this is not a
Coder-level tweak. Five confirmed changes land in this one revision, several of which materially
affect each other (a thicker, narrower brim; a re-derived dome base; a flattened apex; a capped
plug tip; and the handle's outright removal). Each is worked through below with real numbers, not
just restated as if already dimensioned.

#### 5.1.1 Brim OD: 122mm → 100mm, flush with the collar, zero overhang

**Directed change, not a re-derivation:** the new brim OD **exactly matches the body's collar OD
(100mm, §4.2.2/§6.2)** — the lid becomes flush-edged with the collar rather than a cap that
overhangs it, replacing the v5/v6 122mm figure entirely. This removes the visible "overhang ring"
that has existed in every prior version of this lid (100mm in v1–v4, 122mm in v5–v6).

**Named risk, not previously applicable to an overhanging design: zero print-tolerance margin at
this exact-match edge.** Every prior brim/collar pairing had a comfortable overhang margin
(11mm/side minimum) that could absorb normal FDM dimensional variance without anyone noticing. A
brim printed to *exactly* nominal 100mm against a collar also printed to *exactly* nominal 100mm
has no such cushion. This project has already documented, in the context of the plug fit
(§5.2.1), that FDM's systematic tendency is for **external bosses/rims to print slightly
oversized**, not undersized — applied here, that means the more likely failure direction is a
lid brim that overshoots the collar's edge by a fraction of a millimeter, reading as a small
proud lip rather than a flush line, not the collar peeking out past an undersized lid. This is
disclosed as a named risk (see also §10, edge case 4) rather than silently assumed away; no
change to the specified 100mm target is made here, since the flush-fit instruction was explicit
and direct, but the Coder may want to consider a very small (0.2–0.3mm) negative allowance on the
brim OD if the first print reads as proud rather than flush — noted as an option, not specified
as required.

#### 5.1.2 Brim thickness: 5mm → 10mm

**Directed change:** the brim disc's own vertical thickness doubles from 5mm to 10mm — no change
to its radial reach (that's §5.1.1 above). Checked downstream effects:
- **Plug attachment is unaffected in position.** The plug (§5.2.1/§5.2.2) hangs from the brim's
  *underside* (the seating plane) down into the neck bore — its depth (10mm) and Z-position
  relative to the body are unchanged by how thick the brim is *above* that underside plane.
- **The plug's internal "ceiling" (§5.2.2) becomes a thicker solid cap** — the solid brim material
  directly above the plug's hollow interior grows from 5mm to 10mm thick. This does not change the
  bridge's *span* (still ~71.5mm, unaffected by ceiling thickness — see §5.2.2), but a thicker
  overlying disc is structurally more rigid once printed, a minor incidental positive, not a fix
  for the bridging event itself.
- **Wall/boss minimum check:** 10mm is 12.5× the 0.8mm print-floor (§3) — trivially clear, same as
  the 5mm figure was.

#### 5.1.3 Dome base OD — re-derived against the new 100mm brim

**Required check, not assumed fine.** The v6 dome base (~97.2mm, built against the old 122mm
brim) leaves only ~1.4mm margin per side against a 100mm brim — far too tight for a sensible flat
brim ring, exactly as flagged. Re-deriving using the same method v5 already established and this
project has now applied twice:

**Method — preserve the 0.80 dome-to-brim OD ratio.** v1–v4 held dome base (~80mm) ÷ brim (100mm)
= 0.80; v5 re-applied that same ratio to the new 122mm brim (122×0.80≈98mm) and found it
corroborated by a second, independent check (margin over the collar ID). Re-applying the identical
0.80 ratio to the new 100mm brim: **100 × 0.80 = 80mm dome base OD.**

**Corroborating checks, not just one number taken on faith:**
- **Flat brim ring width:** 50mm (brim r) − 40mm (dome-base r) = **10mm** per side — a clearly
  visible, proportionate flat rim, and notably the *same absolute width* as the collar's own 10mm
  reinforcement wall band (§6.2) that this brim sits directly on top of. A brim ring that visually
  echoes the collar band it caps is a pleasant, likely-unintentional-but-worth-naming corroboration,
  not a coincidence I'm leaning on as proof.
- **Absolute-precedent check:** 80mm dome base against a 100mm brim is *exactly* the v1–v4 lid's
  original absolute proportions (before v5 grew both dimensions in step with the wider collar).
  Since the v7 brim OD (100mm) also happens to return to the exact v1–v4 absolute figure (for an
  unrelated reason — flush-fit against a 100mm collar, not overhang-preservation), landing back on
  the original 80mm dome base via ratio-preservation is a reassuring convergence, not a forced
  result.
- **Margin over the collar ID, revisited:** the collar's internal bore is 80mm ID (r=40mm, §4.2.2)
  — identical to the new dome base OD (80mm, r=40mm also). Unlike v5's version of this check (which
  found a comfortable 9mm/side margin beyond the opening), this now shows **zero margin between the
  dome base edge and the bore edge in radius terms alone.** This sounds concerning at first glance
  but isn't, for a reason specific to this revision: with the brim now flush to the collar (§5.1.1),
  the **flat brim ring itself** (r=40–50mm) already fully covers the entire collar top face, bore
  edge to collar edge, independent of where the dome/brim split falls. The dome's job is no longer
  to be the primary "cap over the hole" the way it partially was when the brim only modestly
  overhung the collar in v1–v4 — that job is now fully handled by the brim alone. This makes the
  dome-base/bore-ID coincidence a non-issue rather than a red flag, but it's disclosed explicitly
  rather than silently noted as "still fine" without explaining why the old check's logic doesn't
  transfer directly.

**Dome base OD: 80mm, tagged `ESTIMATED`** (a judgment call via ratio-preservation, same tag/method
as v5's 98mm figure) — not a hard derivation, flagged for the Coder to build to and the Reviewer to
sanity-check visually against the concept-comparison renders.

#### 5.1.4 Dome apex — flattened plateau, replacing the fully-rounded apex

**Directed change, chosen by the requester over a fully-rounded alternative** (visual comparison
provided by the Concept Designer: `concept/v7-dome-apex-rounded.png` vs.
`concept/v7-dome-apex-flattened.png`). Stated reasoning: with no handle occupying the apex anymore,
a flat spot reads as more intentional than a bare rounded dome, and it was also expected to reduce
the previously-disclosed apex drooping/ribbing print risk (§9, prior revisions). Worked through
below rather than assumed.

**Dome curve baseline (hand-calc approximation, same honesty convention as the rest of this
project's frustum/spline tables).** Treating the existing built dome as a single-radius spherical
cap (base radius `a`, cap height `h`, sphere radius `R = (a²+h²)/(2h)`) — the same "curved arc
profile" construction method §4.2 describes as already used for this dome — with the new base
`a=40mm` (§5.1.3) and the previously-held `h=30mm` target: `R = (40²+30²)/(2×30) = 2500/60 ≈
41.667mm`.

**Plateau diameter: 22mm (r=11mm).** `ESTIMATED` — an aesthetic judgment call, sized against the
approved concept-comparison image (`v7-dome-apex-flattened.png`), where the flat top reads as
roughly a quarter of the dome's base width — 22mm ÷ 80mm ≈ 27%, matching that reference
proportion, not an arbitrary round number picked in isolation.

**Blend, using the same tangent-constrained-curve philosophy as the neck-to-collar blend
(§4.2.2/§9).** The natural spherical-cap curve reaches `r=11mm` at `z ≈ 28.52mm` (solving
`r²=R²−(z+11.667)²` for `z`), with a non-zero local slope there (~15.3° from horizontal) — left
unblended, this would be a visible ~15° kink where the curve meets a flat plateau, the same kind of
faceted transition this project's own history (§13 v2) has already established as worth fixing
properly rather than leaving as a sharp corner. A short tangent-matched blend (matching the natural
curve's slope at its start, easing to zero slope at the plateau edge — mechanically the same
technique as the neck-to-collar blend, just applied to a dome apex instead of a cylindrical collar)
absorbs this over the last ~1–1.5mm of height, landing the flat plateau at approximately **z ≈
29mm** — a ~1mm reduction from the previous 30mm point-apex height, an expected and immaterial
consequence of blending the last few degrees of slope out smoothly rather than assuming the same
nominal height applies unchanged to both a point apex and a flattened one.

**Does this genuinely reduce the apex-drooping risk, or just relocate it? Checked, not assumed.**
The previously-disclosed risk (§9, prior revisions: "a small amount of drooping/ribbing at the last
1–2mm of the apex... a normal, usually slicer-manageable artifact for small domes") is specifically
a near-horizontal-curved-surface phenomenon — as a rounded apex closes to a point, the printer
traces an ever-tightening, near-degenerate sequence of tiny-radius rings, which is the actual
mechanism behind the cosmetic ribbing/drooping artifact. **A flattened plateau removes this
mechanism entirely, not partially:** the smallest ring printed on the curved portion is now r=11mm
(an unremarkable, completely normal feature, no different from any other point on a shallow dome),
and the flat 22mm-diameter disc that follows is the print's terminal, fully self-supported cap (the
dome curve's radius shrinks monotonically the whole way up to the blend, so every layer of the
plateau disc is fully supported by the layer directly beneath it — same "shrinking-cone,
self-supporting regardless of local angle" class this project has relied on repeatedly, e.g. §9's
belly/shoulder analysis). This is a genuine mechanistic elimination of the *specific* risk named,
not a smaller version of the same issue. **What replaces it is a different, much more mundane
consideration:** a flat top surface printed as the terminal layers of a solid part is a completely
standard slicer scenario (governed by ordinary "top solid layers"/ironing settings, not a
geometry-level overhang concern) — worth a one-line slicer note, not a named structural risk.

#### 5.1.5 Summary table

| Parameter | Value (v7) | Value (v6, superseded) | Tag |
|---|---|---|---|
| Flat brim disc OD | **100mm** — flush with the 100mm collar OD, zero overhang | ~~122mm~~ | Directed change (§5.1.1) — collar-matching value, DERIVED |
| Flat brim disc thickness | **10mm** | ~~5mm~~ | Directed change (§5.1.2) — ESTIMATED |
| Dome base OD (where dome meets brim) | **80mm** | ~~~97–98mm~~~ | ESTIMATED — re-derived via the 0.80 dome-to-brim ratio (§5.1.3) |
| Dome height above brim top surface | **≈29mm** | 30mm | ESTIMATED — ~1mm reduction from blending the apex to a flat plateau rather than a point (§5.1.4) |
| Dome apex — flattened plateau diameter | **22mm** (r=11mm) — **NEW** | N/A (fully rounded to a point) | ESTIMATED — sized against the approved concept-comparison image (§5.1.4) |
| Handle | **REMOVED ENTIRELY — no replacement grip feature of any kind** | 40mm tall, 9mm bail, 24×22mm opening | Directed, explicit identity reversal — see §7 |
| Alignment plug (lid underside) | 79.5mm OD × 10mm deep, 4.0mm wall — **now capped at the tip** (6mm hollow + 4mm solid end cap) | Same OD/depth/wall, **open at the tip** | Directed change — see §5.2.2 |
| **Total lid height (flat underside/seating plane to top of plateau)** | **≈39mm** (10 brim + 29 dome) | 75mm (5 brim + 30 dome + 40 handle) | DERIVED — a **-48% reduction**, driven almost entirely by the handle's removal |
| **Total lid bounding-box height (plug tip to top of plateau)** | **≈49mm** (39 + 10 plug) | 85mm (75 + 10 plug) | DERIVED — a **-42% reduction** |

**Business-context note, relayed rather than independently re-derived here:** per the task framing
for this revision, this height reduction also positively addresses an earlier competitive-research
concern about the design's overall height versus competitors. I was not able to locate a written
record of that specific competitor-height research in this project's own `dot_pipeline/` history
(the competitor research on file, §4.4/§13 v5, is specifically about neck-opening diameter, not
overall height) — flagging this plainly rather than asserting a provenance I couldn't verify.
Independent of that specific research question, the combined assembled height (body rim + lid
above its seating plane) drops from ≈228.5mm (v6) to **≈192.5mm** (153.5mm body + 39mm lid) as a
direct, verifiable consequence of this revision — a real, substantial reduction on its own merits,
whatever its relationship to the specific research the task referenced.

### 5.2 Seating interface — decision and why it changed from a first draft

**Decision: the lid's underside is a single flat plane. It rests directly on the body's flat
neck-collar rim (§6, now a 100mm OD flat ring as of v5 — was 78mm through v2–v4, see §13 v2/v5) —
no plug, no skirt, no alignment lip reaching down into the opening.**

This was **not** the first design considered in this pass. A first draft added a small
downward-facing alignment lip (to center the lid over the opening) — that was dropped for a
concrete, checked reason, not aesthetics:

- A lip protruding below the main flat underside creates a sudden radial "shelf" overhang when the
  lid is printed underside-down (its natural, lowest-overhang orientation) — the print would need
  to jump from a small-diameter lip footprint to the full brim footprint (now ~122mm as of v5,
  §5.1) within one layer,
  which is a genuine unsupported overhang requiring support material directly on the part's primary
  seating surface (bad for the flatness/finish of the one surface that most needs to stay flat).
- Removing the lip makes the **entire lid underside a single continuous flat plane** — the best
  possible surface for both print quality (zero overhang on the primary surface, ideal bed
  adhesion) and a flush, wobble-free seat against the body's flat collar rim.
- Centering is handled by the collar's visible edge alone (user aligns by eye/feel — this is a
  decorative object handled deliberately and slowly, not a snap-fit consumer product needing blind
  alignment). No magnetic or mechanical assist contributes to centering — that feature has been
  removed from the CAD entirely, see §6.

**Fit check — SUPERSEDED, v7: zero overhang, the check itself is now moot.** At the seating height,
body OD (collar, 100mm) and lid brim OD are now **identical (100mm, §5.1.1)** — there is no
overhang at all, in either direction. This section is retained (not deleted) to explicitly record
why the check no longer applies, per this project's own convention of never silently dropping a
prior finding from the record:

**The v1/v2-era collision check between the brim's overhang and the sloped shoulder below it
(previously verified safe at an 11mm/side overhang, and re-affirmed at v5's 122mm/11mm-per-side
figure) is no longer applicable, and here's why:** that check existed specifically to confirm that
brim material extending *radially beyond* the collar's edge wouldn't intersect the tapered shoulder
surface below it. With the brim now flush to the collar (100mm = 100mm, zero radial excess), there
is no brim material positioned beyond the collar's own edge at all — nothing exists that could
possibly reach outward toward the shoulder in the first place. This isn't a re-run of the check
that happened to still pass; the geometric condition the check was designed to catch (overhanging
material) no longer exists, so there is nothing left to check. What *is* newly relevant at this
flush edge is a different concern — print-tolerance margin at an exact-match diameter — named as a
new risk in §5.1.1 and §10 (edge case 4), not a collision risk.

**No dedicated clearance/tolerance value is needed for this interface** (unlike a plug/skirt fit)
because it's a flat-on-flat resting seat, not a sliding fit. With the magnet pockets removed from
the design (§6), there is no other tolerance-sensitive feature anywhere in the lid/body fit — the
flat seating plane described above is the entire interface.

**This paragraph is superseded if either option in §5.2.1 below is adopted** — a plug/skirt fit
would reintroduce exactly the clearance-tolerance question this paragraph currently says doesn't
apply. Left as-is (not deleted) until the user picks an option, since it remains accurate for the
current, no-plug, as-shipped v5 geometry.

### 5.2.1 Lid-underside alignment/friction-fit plug — ADOPTED as v6 (Option A), see §5.2.2 for the v7 tip-cap addition

**Status update: ADOPTED.** This subsection was written mid-decision, presenting two options
without yet knowing which the requester would choose — that decision has since been made, built,
and independently re-verified three times over (Coder, Tester, and Reviewer, `review.md` Addendum
4). **Option A (the straight-walled lip, below) is what was built and approved as v6** — 79.5mm
OD × 10mm deep, hollow, 4.0mm wall, 0.5mm diametral clearance, open at the tip. Option B (the
tapered stopper) was evaluated, found to require *more* total support than Option A despite
initial appearances, and was **not** adopted; it remains below only as a record of the comparison
that was made, not as a live alternative. **This whole subsection is now historical/provenance —
left unedited below for that reason — except where a v7 change requires a correction, noted
inline.** The single geometric change made in v7 (capping the previously-open tip) is documented
fresh in the new §5.2.2 immediately following this subsection, rather than retrofitted into the
text below.

This subsection documents a requested addition
— a piece under the lid that protrudes ~10mm down into the body's neck opening, for a more secure
fit than the current flat-on-flat seat (§5.2 above). **This exact idea was already considered and
rejected once**, in the original pass on this seating interface: a first-draft downward alignment
lip was dropped because it creates a sudden radial "shelf" overhang when the lid prints
underside-down (its natural, lowest-overhang orientation) — the print has to jump from a small lip
footprint to the full brim footprint within one layer, an unsupported overhang landing directly on
the lid's primary seating surface. **That reasoning was sound and is not being silently overridden
here.** What's changed is the constraint it was evaluated against: the requester has since said
supports are an acceptable tradeoff for this feature (they can print the lid angled or just enable
slicer supports here), so a support-free geometry is no longer a hard requirement — it's now a
real, disclosed cost/quality tradeoff to weigh, not an automatic blocker. Two concrete options are
worked out below with real numbers, per that relaxed constraint, plus a third (milder) variant
noted for completeness. **Nothing here changes the neck width, collar, belly, height, handle, or
body cavity volume (§4)** — this is a lid-underside-only addition, purely additive, body-cavity-
neutral by construction (it exists entirely below the already-flat brim, on the lid, not the body).

#### Clearance — derived, not a vague "close fit," with precedent shown

The neck ID at the relevant depth is **80.00mm** (r=40.000mm), VERIFIED — this exact figure is
independently confirmed by Coder, Tester, and Reviewer (`review.md`'s v5 full re-review table:
"Neck-taper-end (P3) ext/int radius... 44.0000mm / 40.0000mm" and "Collar (P4 band)... 40.0000mm...
constant z=145.5–153.5mm"), not a spec-only assertion.

This project has one existing precedent for reasoning about a friction/press-fit clearance: the
now-removed magnet pockets used **6.2mm pocket for a 6.0mm magnet — 0.2mm diametral oversize
(0.1mm/side)** for a snug, non-rattling precision press-fit at small (6mm) scale (`tests.md` R1,
R25-R29). That ratio (≈3.3% of diameter) is **not** simply carried forward unchanged here, for two
reasons: (1) the design intent stated for this feature is explicitly **"secure but not
press-fit-tight"** — looser than the magnet's snug fit, not tighter or equal; (2) an 80mm printed
circular feature accumulates more absolute roundness/shrinkage variance than a 6mm one (more
circumference, more first-layer/perimeter-path length over which small errors compound), so holding
the *same percentage* would actually be tighter in a way the small-scale precedent was never
validated for at this size.

**Chosen clearance: 0.5mm diametral (0.25mm/side), tagged ESTIMATED.** Scaled up in absolute terms
from the 0.2mm precedent (not held at the same ratio), for the two reasons above. Still small
enough to read as "secure," per the requester's own framing, and comfortably within normal desktop
FDM dimensional capability — not to be confused with the 0.8mm wall/boss print-minimum (§3), which
is a different metric (structural wall thickness, not a fit clearance).

**Critical/max plug diameter (both options below, at the point nearest full engagement): 80.0mm −
0.5mm = 79.5mm.**

**Material-mismatch risk, named rather than assumed away:** the plug is on the **PETG** lid,
engaging a **PLA** body opening — different shrinkage/dimensional behavior between the two
materials means the *realized* clearance on a real print may differ from this nominal 0.5mm
estimate in either direction. Recommended mitigation: print a small stand-alone test coupon (a
short cylinder/frustum at the chosen dimensions) and fit-check it against the already-planned
`neck-fit-test` article (§2, being rebuilt at 80mm ID regardless) *before* committing this geometry
to the full lid — the same "fit test coupon before full print" practice already used for this
project's magnet pockets (`review.md` §7.2, now moot for magnets but a sound precedent for this
new friction-fit feature).

#### Collision check against the v5 internal profile — real Z-coordinates, not assumed

- Lid seating plane (flat underside, where it rests on the collar rim) = **Z=153.5mm** (P4, top of
  collar), per §4.2.2's re-derived profile table.
- A 10mm-deep plug (the user's requested depth) extends from **Z=153.5mm down to Z=143.5mm**.
- The internal bore is a **constant 80mm ID (r=40.000mm) straight cylinder from Z=138.5mm (P3,
  neck-taper-end) up to Z=153.5mm (P4, rim)** — a 15mm-tall constant-diameter zone, independently
  confirmed by Coder/Tester/Reviewer (identical 40.0000mm figures at both Z=138.5 and the
  Z=145.5–153.5 collar band in the Reviewer's v5 table). The external neck-to-collar blend
  (§4.2.2/§9) changes only the *external* radius across this same span — it does not touch the
  internal bore, which stays a plain constant-ID cylinder throughout.
- **Plug tip (Z=143.5mm) sits 5.0mm above P3 (Z=138.5mm) — a clean 5mm margin before the internal
  bore would start widening toward the shoulder's 42.42mm radius.** No collision with the internal
  taper transition. (For reference: the full constant-ID zone is 15mm tall; a 10mm plug uses
  two-thirds of it, leaving real margin rather than landing exactly on the boundary.)
- **Confirmed compatible for both options below** — this check doesn't depend on plug OD or taper
  shape, only depth, which is the same (10mm) for both.

#### Option A — straight-walled lip

| Parameter | Value | Tag |
|---|---|---|
| OD (constant) | **79.5mm** | DERIVED — 80mm ID − 0.5mm clearance |
| Depth | **10mm** | Per request; collision-checked above |
| Shape | Plain cylinder, flat or lightly chamfered tip edge | — |
| Added part material (if solid) | **≈49.6 cm³** (πr²h, r=39.75mm, h=10mm) | ESTIMATED — upper bound; less if hollow-shelled, see below |

**Overhang character:** the plug's own wall is a true vertical cylinder — 0° from vertical, the
best-case shape, genuinely zero-overhang along its full 10mm height. **But** at Z=153.5mm, where
the plug meets the flat underside, the design must step outward from 79.5mm OD to the full 122mm
brim OD. Because the plug is uniform-diameter right up to that point, this is a **discontinuous
jump (Δr=21.25mm within a single layer transition), not a taper at all** — the same category of
problem originally rejected in the first draft, just at a larger, closer-to-full-diameter lip than
before.

**Support implications:** an annulus from r=39.75mm to r=61mm (122mm brim OD), **area ≈67.3 cm²**,
needs support material filling the full 10mm gap beneath it from the bed up to the underside plane.
This support sits directly beneath **both** the collar-mating ring (r=39.75–50mm — needs to be flat
and clean for a proper seat, though hidden once assembled) **and** the decorative overhang ring
(r=50–61mm — visible once assembled, per §5.2's fit-check). Support-removal witness marks on this
combination of a functional mating surface and a cosmetically visible surface is a real,
non-trivial print-quality risk specific to this region, distinct from "it's all hidden inside the
neck."

#### Option B — tapered stopper/bung (the shape the requester floated: wide at top, narrowing to the tip)

| Parameter | Value | Tag |
|---|---|---|
| Top diameter (at flat underside) | **79.5mm** | DERIVED — same clearance target as Option A |
| Tip diameter | **40mm** | ESTIMATED — chosen as a genuinely stopper-reading taper (~half the top diameter), still structurally substantial, not a fragile point |
| Depth | **10mm** | Per request; collision-checked above |
| Resulting taper angle from vertical | **≈63.1°** (`atan(19.75mm ÷ 10mm)`, Δr=(79.5−40)/2=19.75mm) | Computed, not assumed |
| Added part material (if solid) | **≈29.1 cm³** (frustum, R=39.75mm, r=20mm, h=10mm) | ESTIMATED — ~41% *less* than Option A's solid volume (a cone always has less volume than a cylinder of the same base/height) |

**The angle math, worked backward first, per the requested method:** targeting a comfortably
self-supporting ~42° (the low end of the ~40–45° range this project has used elsewhere) over a
10mm depth permits `Δr = 10mm × tan(42°) ≈ 9.0mm` — i.e., a top-to-tip taper from 79.5mm down to
only **≈61.5mm**, a mild, barely-tapered shape that doesn't read as a stopper at all. **Getting to a
genuinely cork/bung-shaped 40mm tip (Δr=19.75mm) necessarily requires ≈63°, well past the ~45°
guideline — there is no taper profile that is both recognizably stopper-shaped and self-supporting
within a 10mm depth. This is shown explicitly, not glossed over.**

**Support implications — corrected finding, not assumed:** the pronounced 40mm-tip taper needs
support along its **entire** 10mm tapered face (constant 63° the whole way, since it's a
straight-sided frustum) **in addition to** the same 67.3 cm² outer-annulus issue Option A has
(Option B's top diameter is also 79.5mm, so the flat brim beyond that point is elevated by the same
10mm either way). **Net result: Option B needs more total support material than Option A, not
less** — a straight vertical wall is definitionally zero-overhang, while any taper steep enough to
actually look/function like a stopper is, by these numbers, well past self-supporting. This
directly checks (and revises) an initial assumption that tapering would reduce support needs — it
doesn't, for a taper this pronounced. What Option B *does* have going for it: all of its extra
support sits on the plug's own face, entirely inside the neck opening, never visible once
assembled — unlike Option A's annulus, part of which (the decorative overhang ring) *is* visible.

**Self-centering / progressive-friction benefit — real, and mechanically confirmed, not just
asserted:** because the plug narrows toward its tip, a slightly misaligned lid is guided into the
opening as it's lowered (the tapered tip contacts the collar's inner edge and self-centers before
the wider section engages). The diameter of the plug passing through the neck's opening plane
increases as insertion progresses — loosest on first contact (tip only engaged), tightest right at
full seating (the 79.5mm/0.5mm-clearance top of the taper is what's engaged once the lid is fully
down). This is the literal "cork in a bottleneck" mechanic the requester described, and it is a
genuine functional difference from Option A (which has constant 0.5mm clearance throughout its
whole depth, i.e., a uniform, non-progressive slip fit).

**Milder, no-extra-support variant (noted for completeness, not a third fully-worked option):** top
79.5mm / tip ≈61.5mm / 10mm depth / ~42° stays within the self-supporting guideline — no more
support than Option A — and still gives a real, if subtle, self-centering/mild-progressive-fit
benefit. It will read much more like a gently chamfered lip than an actual stopper, though.

#### Solid vs. hollow-shelled plug — Coder-level implementation choice, flagged not decided

The volumes above (49.6 / 29.1 cm³) assume a **solid** plug — an upper-bound material estimate.
Given the v5 lid's material volume already grew +45.2% this revision (`review.md`'s v5 full
re-review, §6 — "the lid alone grew by nearly half its material volume"), a **hollow-shelled plug**
(matching this project's own nominal 4mm wall convention used elsewhere, well above the 0.8mm
print-minimum, §3) would meaningfully reduce the added material/print time for either option. This
is left as a Coder-level implementation choice unless the requester has a preference — noting it
explicitly so it isn't silently defaulted to "solid" without anyone having decided that.

#### What this does NOT change

Confirmed, not assumed: this addition touches only the lid's underside geometry, entirely below the
already-existing flat brim plane. It does not move, resize, or otherwise touch the neck ID/OD,
collar ID/OD, belly, shoulder, overall body height, or handle (§4, §6.2, §7 all unchanged), and has
zero effect on the body's internal cavity volume target (§4.1's ≈1579 cm³ figure) since nothing
about it exists on or inside the body.

#### Recommendation and open question — back to the requester

**If forced to pick one: Option B's pronounced (40mm-tip, ~63°) taper**, because it delivers a real
functional improvement over the current flat seat and over Option A alike (self-centering,
progressive friction — literally the feature requested) at a cost (more support material than
Option A) that lands entirely on a hidden, never-visible interior surface, using an
already-established practice in this design (support removal from a hidden void — the same
category of task as clearing the handle's through-hole support, §7). If minimizing total support
material matters more than the stopper feel, Option A (or the milder ~42° B variant) is the better
call. This is a genuine feel/tradeoff decision, not a correctness question — presented as a choice,
not decided here.

**Question back to the requester (HISTORICAL — resolved):** the option question above was answered
by the requester choosing Option A, straight-walled, hollow, 4mm wall — see the status note at the
top of this subsection and `review.md` Addendum 4 for the built/verified result.

---

### 5.2.2 Plug tip — capped, v7 (directly confirmed change, not previously modeled)

**Directed change:** the v6 plug (adopted above) is open at its tip — a plain hollow tube, sealed
at the top (where it meets the solid underside of the brim) but open at the bottom (the end that
reaches deepest into the neck bore). Cap this open end with a solid flat disc, matching the
project's own ≥4mm wall convention.

**Geometry.** Total plug envelope is **unchanged**: 79.5mm OD, 10mm total depth, 5.0mm collision
margin above P3 (§5.2.1's collision check, unaffected — the envelope this check depends on has not
moved). Within that unchanged 10mm depth: the last **4mm nearest the tip becomes a solid disc**
(the new cap, full 79.5mm OD), and the remaining **6mm nearest the brim stays hollow** (same 4.0mm
wall, same 71.5mm-diameter interior void as before, just over a shorter run). This keeps every
previously-verified collision number (5.0mm margin, 0.5mm clearance, 79.5mm critical OD) intact
without requiring the Coder or Tester to redo that check — only the plug's internal makeup changes,
not its external envelope or position.

**Print orientation context, restated because it's load-bearing for this analysis:** the lid prints
flat-underside-down (§9) — meaning, in print sequence, the plug's tip is the *first* thing printed
(bed-touching), the hollow tube builds upward from there, and the brim/dome/plateau follow above
it. This is not a new fact, but it is the fact this whole analysis depends on, so it's restated
here rather than assumed silently.

**Does capping eliminate the previously-disclosed 71.5mm internal bridge? Checked directly, not
assumed — the honest answer is more nuanced than "yes."**

1. **The existing ceiling bridge is unchanged, not eliminated.** The 71.5mm-diameter horizontal
   span where the hollow tube transitions into the solid brim above it (`review.md` Addendum 4,
   §2) is a function of that transition existing at all — it exists regardless of what happens at
   the *other* end of the tube. Capping the tip does not touch this transition in any way: same
   span, same expected sag/stringing under default settings, same reason it doesn't matter (fully
   sealed, never visible, disconnected from every fit-critical surface). Any claim that capping
   removes this bridge is incorrect, and is corrected here rather than carried forward uncritically.
2. **The new cap itself introduces zero new overhang/bridging risk, but specifically because of the
   print orientation, not automatically.** A flat disc is, in general, exactly the kind of feature
   that can bridge badly — but this specific disc is the **literal first printed layer(s)** of the
   whole part, resting directly on the build plate. The build plate itself fully supports every
   point of a first layer, regardless of its shape (a solid disc supports at least as well as, and
   arguably better than, the thin open ring it replaces — more first-layer bed contact area, a
   modest adhesion improvement). This is confirmed by walking through the actual print sequence
   (above), not asserted by analogy to the top-of-tube case. **If the print orientation were ever
   changed** (e.g., the alternate orientation considered and rejected in §9 below), this conclusion
   would not hold — the cap would then be the *last* feature printed, over an enclosed void, and
   would be a genuine bridge. This is exactly why orientation is decided here rather than left to
   incidental Coder choice (per this document's own standing practice).
3. **What actually changes is the internal void's enclosure, not its bridging risk.** Before
   capping: sealed at the top (brim), open at the bottom (tip) — a void with one theoretical, if
   impractical, access point. After capping: sealed at both ends — no access point at all. Working
   through what this means for the already-named trapped-support risk (`review.md` Addendum 4, §3):
   reasoning through how a "touching build plate only" slicer support setting evaluates this
   geometry, an open tip gives the void a continuous, unobstructed line back to the actual build
   plate (through the open hole) — meaning that setting could plausibly still generate support
   inside the void today, before this change, since the void technically "touches" the bed through
   the open end. **Once capped, the void's floor is solid material, not open bed** — there is no
   longer any unobstructed path from inside the void down to the actual build plate, so a
   "touching build plate only" setting should now reliably generate *zero* support inside this
   cavity. **This is a reasoned conclusion from how that slicer setting is generally described to
   work, not an empirically confirmed one** — slicer heuristics vary by software, and this has not
   been checked against a real slice. **Recommendation: before committing to the full lid print,
   check the slicer's print preview to confirm no support is generated inside the now-fully-sealed
   cavity** — this is a cheap, concrete check that resolves the uncertainty directly rather than
   relying on my reasoning about it. If a more permissive "everywhere" support setting is ever used
   despite this recommendation, any support generated inside would be more completely
   unreachable than before (no access point at all, versus a previously marginal and likely
   impractical one through a 10mm-deep, 71.5mm-wide narrow opening) — though this was already a
   low-practical-value access point either way.
4. **Net honest summary:** capping the tip does not remove the already-disclosed ceiling bridge
   (same risk, same reasoning, unchanged); it adds no new bridging risk of its own (confirmed by
   the print-sequence walkthrough, contingent on keeping the specified orientation); and it likely
   makes the standing "supports touching build plate only" mitigation more reliable, not less —
   though that specific claim should be confirmed in slicer preview, not taken purely on this
   reasoning. This is a more qualified conclusion than "capping eliminates the bridge" would
   suggest, and is presented that way deliberately, per the instruction not to assume capping is
   risk-free.

**Material impact.** New cap volume ≈ π×39.75²×4mm ≈ 19.86 cm³ (solid disc, full 79.5mm OD, 4mm
thick); remaining hollow section (6mm × the existing 4.0mm-wall annulus) ≈ 5.69 cm³ — **new total
plug material ≈25.55 cm³**, up from the v6 figure of ~9.49 cm³ (fully hollow, 10mm). This is a
real, if small, material increase (+~16 cm³) against a lid that, per §5.1, is otherwise getting
*lighter* overall (brim OD shrinking from 122mm to 100mm outweighs the brim-thickness and
plug-cap increases) — see §5.1.5's height table and the material estimate below.

**What this does NOT change:** the plug's OD, depth, wall thickness, clearance, or collision margin
(all unchanged from §5.2.1); the neck, collar, belly, height, or body cavity volume (§4, unaffected
— this remains a lid-underside-only feature); the hollow-vs-solid choice for the *remaining* 6mm
tube section (still a Coder-level implementation option, per §5.2.1, now scoped to a shorter run).

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

### 6.2 Neck collar (reinforced rim / seating band — no longer a magnet housing) — REVISED, v5 (ID/OD widened, wall thickness held)

**Collar OD/ID grew in v5 (78mm→100mm OD, 58mm→80mm ID, §4.2.2) — driven by the market-research
neck-widening decision, not a re-opening of the v2/v3 "leave the collar as-is" decision.** The
**10mm reinforcement wall thickness is explicitly held unchanged** — the requester chose to keep it
rather than revert to the nominal 4mm wall, even though it has had no magnet-housing purpose since
v3's pocket removal. It now serves purely as a lid-seating/reinforcement band, kept for structural
margin and rim character (the same reasoning v3 already established, just re-affirmed at the new
size). The previously-flagged minor concept-fidelity drift (the collar reads more "banded/
cylindrical" than the concept's continuous neck curve) is unchanged in kind by this revision —
growing the collar's absolute size doesn't newly introduce this drift, which was already accepted
in v2/v3.

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

| Parameter | Value (v5) | Value (v2–v4, superseded) | Tag |
|---|---|---|---|
| Collar height | 15mm — **unchanged** (= P3→P4 in the §4.2.2 profile) | 15mm | Carried from §4.2.2 |
| Collar external OD | **100mm** | ~~78mm~~ | DERIVED — 80mm ID + 2×10mm reinforcement wall (§4.2.2). |
| Internal ID through the collar | **80mm** | ~~58mm~~ | Requester's explicit target, matches the new neck ID (§4.2.2, §4.4). |
| Collar wall thickness | **10mm — unchanged** ((100−80)/2) | 10mm | DERIVED from the 100mm OD above; the requester explicitly chose to keep this at 10mm rather than the nominal 4mm, purely as a seating-band reinforcement — well above the 0.8mm print-minimum (§3). |

This collar is rotationally symmetric (no isolated bump geometry), reads plausibly as a rim
reinforcement detail on a ceramic-style vessel, and gives the lid a flat, adequately thick, uniform
surface to seat against — the same physical shape as before, just larger, doing the same narrower
job.

---

## 7. Handle — REMOVED ENTIRELY, v7 (deliberate, explicit, user-confirmed identity reversal)

**This section previously specified an open-loop bail handle (40mm tall, 9mm round bail, 24×22mm
clear opening) as a hard constraint compliance item. As of v7, the handle is removed entirely, with
no replacement grip feature of any kind — no nub, no knob, no raised boss, nothing.** The lid
becomes a plain dome (with a flattened apex plateau, §5.1.4) sitting on a flat brim; the user grips
the brim/dome edge by hand to lift it, the same way one would lift any domed lid with no dedicated
handle.

**This directly and deliberately reverses a hard constraint stated since the original concept
approval, and that reversal is being named plainly here, not discovered later by a downstream
reviewer as unexplained drift.** `concept/brief.md` describes the open-loop bail handle as **"the
key differentiating feature"** of the entire design, states it should "read as an intentional,
load-bearing part of the lid, not a decorative nub," and calls the open-through-hole geometry
specifically "a hard constraint when the Planner moves to CAD." Every prior revision of this
document (v1 through v6) treated that constraint as binding, and every Reviewer pass independently
re-verified the handle's open-loop integrity as one of this project's three named hard constraints
(`review.md`, repeated across every addendum).

**The requester has explicitly and directly confirmed removing the handle entirely, with no
replacement grip feature.** This spec records that instruction as exactly what it is — a direct,
deliberate override of the concept brief's own "hard constraint" framing, made knowingly and
explicitly, not a silent contradiction of it. The concept brief's original language is not being
edited or walked back; it is being explicitly superseded by this later, direct instruction, and
both facts are recorded side by side so nothing about this project's history reads as
self-contradictory to a future reader.

**Ripple effects, worked through rather than left as "delete and move on":**
- **Total lid height drops substantially** — see §5.1.5's table (75mm brim-to-handle-top stack,
  down to ≈39mm brim-to-plateau; ≈85mm total bounding-box height down to ≈49mm). The handle alone
  accounted for 40mm of the old 75mm stack — more than half of it.
- **Print orientation:** flat-underside-down was originally chosen for the seating surface,
  independent of the handle. Re-checked, not assumed, in §9 below — it still holds, and the
  reasoning for why an alternate orientation (now geometrically tempting, given a symmetric,
  handle-free part) is *not* actually better is worked through there in full.
- **The three hard constraints this project has tracked since the original concept approval are
  now two, not three, by deliberate design, not because one silently failed.** "Handle is a genuine
  open through-hole loop" is retired as a checkable constraint — there is no handle to check. This
  is noted explicitly so a future Reviewer pass doesn't either (a) waste effort looking for a
  feature that was intentionally removed, or (b) mistakenly read its absence as a defect. The
  remaining two hard constraints (plain/smooth body, single-size build) are entirely unaffected by
  this change and remain fully in force.
- **Business-fit implication, flagged for the Reviewer, not resolved here:** the concept brief
  called this feature "load-bearing to the design's identity." Whether the design still solves the
  stated business problem without it is a business-fit judgment call belonging to the Reviewer, not
  something this spec resolves unilaterally — recorded here as a fact for that review, not as a
  pre-judged conclusion.

**Material/cost note:** removing the handle also removes its (previously unestimated in isolation,
but non-trivial, per the ~35 cm³ implied by back-calculating the v6 lid's total measured material
volume) share of the lid's material and print time — a contributing factor, alongside the brim OD
reduction, to the lid's overall material volume estimate holding roughly flat or decreasing despite
the thicker brim and now-partially-solid plug (§5.1.5, §5.2.2).

---

## 8. Material recommendation — REVISED, see §13 v2

**Body: matte or silk PLA** (not standard/glossy PLA), per direct instruction and the
market-research finding that comparable products get called out in reviews for "feeling like
plastic." Reason: matte/silk PLA variants diffuse surface reflection in a way that reads closer to
the stoneware finish the concept calls for than standard glossy PLA does. Unchanged from v1.

**Lid: PETG.** Changed from v1's matte/silk PLA — this decision was made after the original draft
and is reflected here for the first time. Reason: PETG is more heat/UV-resistant than PLA, which
meaningfully reduces warp risk specifically for the lid — the smaller/thinner of the two parts, and
still the part most likely to be repeatedly picked up and handled, more prone to warping from
ambient heat than the larger body. This also directly mitigates the long-term-display risk flagged
in v1's edge case 3 (§10) for the *lid*, though not for the body, which remains PLA.

**v7 note — reasoning updated, conclusion unchanged.** Earlier phrasing of this section (and
`parameters.md`) tied part of the PETG rationale specifically to "the handle root fillet... the
feature most exposed to a knock or repeated cyclic grip load." **The handle no longer exists
(§7)**, so that specific mechanism no longer applies — this is corrected here rather than left as a
stale reference to a removed feature. The core rationale still holds without it: the lid remains
the part users repeatedly pick up and set down (now by gripping the brim/dome edge directly rather
than a handle), and PETG's better heat/UV resistance and impact toughness are still the right
material properties for a frequently-handled, thinner-walled part regardless of exactly where on it
the hand makes contact. **No change to the material recommendation itself — PETG for the lid still
stands — only to the specific feature-level justification that has since become inapplicable.**

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

> **v8 (2026-09-10):** the rounder body profile (§4.2.3) does **not** change the print orientation
> or its reasoning — base-down, neck up, unchanged. Re-check of the reshaped below-P3 region:
> the faired lower body (base→belly) rises to an estimated **~32–35° from vertical** (was ~24° as a
> single chord) — comfortably self-supporting; **belly→witness→P3** stays shrinking-radius
> (self-supporting regardless of local angle) and is marginally *gentler* than v7's pinched descent
> (~32.7° vs ~35.1° average external angle). **One new minor first-print watch item:** the underside
> of the **R7 external foot fillet** (§4.2.3) — its bottom ~2.05mm sits below 45° right on the build
> plate, routine for any rounded base edge (a few bridged layers, at most minor cosmetic sag on a
> downward-facing edge). The **neck-to-collar external blend zone** (the one flagged ~45.6–47.25°
> zone, Z 138.5–145.5mm) is above P3 and **byte-identical to v7** — unchanged.

**Body: base (flat, 98mm OD) down on the bed, opening/neck facing up.**
- Matches the part's natural resting stance. Unchanged from v1.
- **Overhang angles re-checked against the v5 profile (§4.2.2)** — this supersedes both the v2
  hand-calc table above and the v4 Reviewer's live-geometry sweep (`review.md` Addendum 3), neither
  of which reflect the v5 neck/collar/height changes. Baseline for this check is the Reviewer's own
  independently-verified v4 findings (a genuine continuous full-span sweep of the live geometry, the
  most rigorous overhang data this project has), adjusted for what v5 actually changes:
  - **Base→belly apex (Z=0–69mm): unchanged segment, unaffected by v5.** The Reviewer's v4 sweep
    found this genuinely monotonically non-decreasing (zero locally-decreasing radius steps across
    1,382 sampled points) — self-supporting regardless of local angle, and nothing in v5 touches
    this region.
  - **Belly apex→shoulder (Z=69–112.5mm in v5, was Z=69–119mm in v4):** radius still shrinks
    monotonically (76.97mm→46.42mm, unchanged endpoints) over a now-**shorter** span (43.5mm vs.
    50mm, due to the 6.5mm height trim, §4.2.2) — the average slope steepens slightly, from
    `atan(30.55/50) ≈ 31.4°` to `atan(30.55/43.5) ≈ 35.1°`. **This does not introduce new risk**:
    this is still the shrinking-radius ("shrinking cone") class this project has established is
    inherently self-supporting regardless of local angle magnitude, because the radius never
    increases with height here — only the *rate* of shrinking increases, which is not the failure
    mode overhang angle guidelines are protecting against.
  - **Shoulder→neck-taper-end (Z=112.5–138.5mm in v5, was Z=119–145mm in v4):** the internal/
    external radius change across this span **shrank dramatically** — external Δr went from
    `46.42→33mm` (13.4mm) in v4 to `46.42→44mm` (2.4mm) in v5, because the new neck OD (44mm) is
    much closer to the shoulder radius than the old neck OD (33mm) was. Average external angle:
    `atan(2.42/26) ≈ 5.3°` — markedly **gentler** than v4's equivalent figure, still monotonically
    shrinking (self-supporting class), no concern.
  - **Neck-to-collar external blend (Z=138.5–145.5mm in v5, was Z=145–152mm in v4) — the one
    pre-existing flagged risk zone, re-checked rather than assumed unchanged:** the radius **delta**
    driving this blend is **unchanged at 6mm** in both v4 (39−33mm) and v5 (50−44mm), because the
    requester kept the same 10mm collar wall over the same 4mm neck wall (§4.2.2). Holding the
    blend's height span unchanged too (7mm, the same fraction of the 15mm collar height used in the
    v4 construction), the same tangent-constrained-cubic-Bezier construction method applied to the
    same (Δr, Δz) inputs produces the **same curve shape** — so the peak overhang angle is expected
    to stay **~47.25°**, just relocated to Z≈140.75mm (was Z≈147.25mm). **This is a reasoned estimate
    from geometric invariance (same Δr, same Δz, same method ⇒ same curve), not a fresh CAD
    measurement** — flag for Coder/Tester confirmation once the v5 geometry is actually built, same
    as every other angle figure in this document. If the Coder's construction ends up using a
    different blend span than 7mm, the peak angle will differ from this estimate and should be
    re-measured directly rather than assumed.
  - **Net conclusion: the one flagged risk zone (neck-to-collar blend) is not made meaningfully
    worse or better by this revision — same ~47° "watch it on the first print" band as before, just
    at a different Z-height.** No *new* overhang risk is introduced anywhere else in the profile;
    if anything, the shoulder-to-neck-taper segment gets meaningfully gentler.
- The 98mm flat base gives a large, stable bed-adhesion footprint — unaffected by v5.

**Lid: flat underside down on the bed, dome/plateau facing up — re-confirmed, not carried forward
incidentally, now that the handle (§7) is gone.**

- **The core reasoning is unchanged and still holds on its own merits, independent of the handle.**
  This is the single flat plane established in §5.2 specifically because it's the best possible
  print orientation for this part — full, continuous bed contact with zero overhang on the primary
  seating surface. Nothing about removing the handle weakens that reasoning; the seating surface is
  still the seating surface.
- **A genuinely viable alternate orientation now exists, worth naming rather than ignoring — but it
  is not actually better, and here's the worked reasoning why.** With the handle gone and the apex
  flattened to a symmetric plateau (§5.1.4), the lid is, for the first time in this project, a
  shape whose *top* face is flat enough to plausibly rest on a bed too — a genuinely new
  consideration the handle's presence had always foreclosed outright. Checked directly:
  - **This would require flipping the entire dome, not just resting the plateau down.** The dome
    currently flares *outward as it descends* from the plateau to the brim (radius growing with
    decreasing height, when read dome-up) — in the print orientation actually used, radius shrinks
    monotonically as height increases (plateau-up), which is the inherently self-supporting
    "shrinking cone" class this project relies on throughout (§9, body sections; §5.1.4's plateau
    argument). Flipping to plateau-down would print the dome in the *opposite* direction — radius
    growing as height increases from the small plateau up to the wide 80mm dome base — the
    classic *expanding*-cone overhang case, requiring substantial support under the entire dome
    surface, not just a small feature.
  - **This is a strictly worse trade, not a wash.** Today's orientation has exactly one disclosed
    overhang zone on the lid (the plug's internal ceiling bridge, §5.2.2, hidden and inconsequential
    once sealed). Flipping to plateau-down would trade that one small, harmless, hidden bridge for
    full-surface support under the entire visible, cosmetically-important dome exterior — a much
    larger support burden landing on a surface that actually matters for finish quality, unlike the
    plug's sealed interior.
  - **It would also break §5.2.2's "cap is a bed-supported first layer" finding.** In a flipped
    orientation, the plug's new tip cap (§5.2.2) would become the *last* feature printed, over an
    enclosed void, with no bed support underneath it — reintroducing exactly the bridging risk
    §5.2.2 confirmed does not currently exist.
  - **Conclusion: flat-underside-down remains the clear, correct recommendation.** The alternate
    orientation is real and worth recording as considered (per the instruction not to leave this
    decision to incidental Coder choice), but it is not a close call once the whole dome's behavior
    and the plug's cap are both accounted for, not just the plateau's own flatness in isolation.
- **The dome's previously-disclosed apex-drooping risk is addressed by the plateau, not just
  relocated — see §5.1.4 for the full mechanistic argument** (the ribbing/drooping mechanism was
  specific to a near-degenerate closing point, which no longer exists; the flat plateau's own top
  surface is a standard, well-understood slicer scenario, not a geometry-level overhang concern).
- **The plug's internal ceiling bridge (§5.2.2) is the one disclosed overhang risk remaining on the
  lid** — unchanged in span or expected behavior by the tip-capping, sealed and inconsequential once
  printed, per §5.2.2's full analysis.
- **The handle's open-through-hole support consideration (previously the other item named here) no
  longer applies — there is no handle, and therefore no internal loop support to remove.**

---

## 10. Edge cases

1. **Pet significantly below the 90 lb design target (e.g. a 50 lb dog).** This urn is intentionally
   sized for the top of the stated 50–90 lb range (§4.1) as a deliberate single-size decision, not a
   miscalibration — a 50 lb pet's remains will use noticeably less than the current ~1579 cm³ built
   capacity (§4.1/§4.2.1 — updated in v4 from the original ~1477.8 cm³ design target, which this
   edge case's logic held for through v3; the underlying point is unchanged and, if anything,
   stronger now that the capacity is larger). This is expected and accepted per the requester's own
   instruction; a smaller size is a separate, future project (§12), not a fix needed here.
2. **Remains bag too bulky/stiff to pass through the neck opening — now 80mm, up from 58mm as of
   v5** (§4.4). This edge case was the direct trigger for this revision (market research found the
   old 58mm ID a significant outlier), and is meaningfully de-risked by the widening, but is still
   `ESTIMATED`/untested against a real bag — flagged, not closed. The fix, if it still comes up in
   testing at 80mm, is widening the neck ID further in a future spec revision, not resizing the
   body. The `neck-fit-test` article (§2) must be rebuilt at the new 80mm ID before it can be used
   to actually test this.
3. **Sustained heat or direct sunlight exposure** (e.g. a sunny windowsill, near a heat vent) — per
   this shop's standing PLA guidance, PLA (including matte/silk variants) can soften/warp under
   prolonged heat/UV. Accepted here because the finish requirement specifically calls for a PLA
   variant (§8), but worth surfacing to the requester as a real long-term-display risk, not silently
   absorbed into the material recommendation.
4. **Flush brim-to-collar fit lands proud or recessed instead of flush, due to normal FDM
   dimensional variance — NEW, v7.** As of v7, the lid brim OD and body collar OD are specified as
   *identical* nominal values (100mm each, §5.1.1), with zero designed-in overhang margin to absorb
   print-to-print variance the way every prior revision's overhanging brim could. Per this
   project's own documented FDM tendency (external bosses/rims print slightly oversized more often
   than undersized, §5.1.1/§5.2.1), the more likely outcome on a first print is a lid brim that
   reads as very slightly proud of the collar's edge rather than perfectly flush, not a collar that
   peeks out past an undersized lid. This is cosmetic, not functional (the seating interface itself
   is unaffected, §5.2), and is not a print blocker — but it's a real, newly-introduced risk this
   design didn't carry before, named here rather than silently assumed away. If the first print
   reads as visibly proud rather than flush, a small (0.2–0.3mm) negative allowance on the brim OD
   is the straightforward fix for a future revision.

---

## 11. Question back to the requester

**What slicer settings should be used (layer height, infill)?** No layer height or infill target has
been specified. Given this is a decorative, low-mechanical-stress vessel (as of v7, there is no
handle or other dedicated load-bearing lift feature at all, §7 — the lid is lifted by gripping the
brim/dome edge directly, and the body only ever carries the modest static weight of a bagged-remains
payload), a reasonable default absent other direction would be **0.16–0.2mm layer height** (finer
layers matter more here than usual, given the "doesn't feel like plastic" finish bar in §8, and now
also relevant to the lid's new flat plateau top surface, §5.1.4) and **15–20% infill** (the floor
and walls carry the modest weight of a bagged-remains payload; this isn't a structural load case
that needs high infill) — please confirm or state a preference before the Coder locks in export
settings. **New for v7: also confirm the lid's support setting is "touching build plate only"
before slicing** (§5.2.2) — separate from the layer-height/infill question, but worth bundling into
the same settings confirmation since both need to be locked before the Coder's export.

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
| v6 (ADOPTED — corrected from a stale "pending, not yet adopted" status left in this row by an earlier pass) | New §5.2.1: re-evaluated a previously-rejected downward alignment lip/plug under the lid (~10mm into the 80mm neck opening) now that the requester has said print supports are an acceptable tradeoff for this feature. Derived a clearance value (0.5mm diametral) by scaling this project's own magnet-pocket-oversize precedent (0.2mm at 6mm scale) up in absolute terms for the much larger 80mm interface. Ran a real Z-coordinate collision check against the v5 profile (plug tip at Z=143.5mm sits 5mm clear of P3 at Z=138.5mm — no collision). Worked out **Option A** (straight 79.5mm OD lip, zero overhang on its own wall, but a discontinuous jump to the 122mm brim requiring support on a partly-visible surface) and **Option B** (79.5mm-top/40mm-tip tapered stopper, ~63° taper, self-centering/progressive-friction benefit, but — a corrected finding, not an assumption — *more* total support than Option A because the taper itself exceeds the ~45° self-supporting guideline, all of it on a hidden surface). Flagged solid-vs-hollow as an open Coder-level choice and named a PETG-plug/PLA-body material-mismatch risk with a test-coupon mitigation. **No change to neck/collar/belly/height/handle/cavity volume — purely additive to the lid underside.** **The requester chose Option A** (straight-walled, hollow, 4.0mm wall); it was built, independently re-verified by Coder, Tester, and Reviewer via a fourth independent method (`review.md` Addendum 4), and approved with named, non-blocking watch-items (the 71.5mm internal bridge, the outer support annulus, a trapped-support slicer callout, a test-coupon recommendation). **This row is corrected in the v7 pass** — it had been left describing the two options as "awaiting user decision" long after that decision was actually made, built, and shipped; that staleness is fixed here rather than perpetuated into a third round, consistent with this project's own repeatedly-named documentation-lag pattern. | User asked for a more secure lid fit than the current flat-on-flat seat. The identical idea was rejected once already for a sound, documented reason (overhang on the primary seating surface); this revisits it honestly rather than either silently rebuilding the rejected design or silently refusing the request, now that the constraint that killed it (support-free requirement) has been relaxed by the requester. Presented as two real options with numbers rather than a unilateral pick, per direct instruction. |
| v7 (this document) | **Five confirmed lid-only changes, worked through together since several materially affect each other.** (1) **Plug tip capped** (§5.2.2): the v6 plug's open tip is closed with a solid 4mm-thick end disc (6mm hollow + 4mm solid, same 10mm total depth/5mm collision margin/79.5mm OD, all unchanged). Checked, not assumed: the existing 71.5mm ceiling bridge is **unchanged**, not eliminated, by this addition; the new cap itself introduces **no new overhang risk**, confirmed by walking through the actual print sequence (it lands as a bed-supported first layer in the specified orientation); the internal void becomes fully sealed (both ends), which reasoning suggests makes the standing "supports touching build plate only" mitigation *more* reliable, not less — flagged as a reasoned-but-unconfirmed conclusion, with a concrete slicer-preview check recommended before the full print. (2) **Handle removed entirely, no replacement grip feature** (§7) — an explicit, direct, user-confirmed reversal of `concept/brief.md`'s framing of the open-loop handle as "the key differentiating feature" and "a hard constraint," documented plainly as an override rather than a silent contradiction. Ripple effects worked through: total lid height drops from 75mm to ≈39mm (brim-to-plateau stack) and total bounding-box height from 85mm to ≈49mm (a -42% reduction); the flat-underside-down print orientation is re-confirmed to still hold on its own merits (§9), and a newly-viable alternate orientation (plateau-down, now geometrically tempting on a symmetric, handle-free part) is explicitly considered and rejected, with the full worked reasoning shown (it would flip the entire dome into an expanding-cone overhang and reintroduce a bridging risk on the plug's new cap); the "open-loop handle" hard constraint is retired (not failed) since there's no handle left to check. (3) **Brim thickness 5mm→10mm** (§5.1.2): checked downstream — no change to the plug's position or the already-established collision numbers; the plug's internal ceiling becomes a thicker (10mm, was 5mm) solid cap, a minor structural positive, not a fix for the bridging event itself. (4) **Brim OD 122mm→100mm, flush with the collar, zero overhang** (§5.1.1): required the dome base OD to be re-derived (§5.1.3) — re-applied the same 0.80 dome-to-brim ratio method v5 established, landing on **80mm** (down from ~97–98mm), corroborated three ways (flat-ring-width match to the collar's own 10mm wall band, an exact return to the v1–v4 lid's original absolute proportions, and a margin-over-bore check whose old logic is explicitly shown to no longer transfer the same way now that the brim alone fully covers the collar top face). The v1/v2-era brim-vs-shoulder collision check is explicitly retired as **moot, not re-verified-and-passing** — with zero overhang, there's no brim material left that could ever reach the shoulder, so there's nothing left to check. A new named risk is added (§5.1.1, §10 edge case 4): an exact-match 100mm-to-100mm edge has zero print-tolerance margin, and this project's own documented FDM tendency (external features print oversized, not under) suggests the more likely failure mode is a slightly proud lid edge, not a recessed one. (5) **Dome apex flattened to a plateau** (§5.1.4), chosen by the requester over a fully-rounded alternative (concept-comparison images: `concept/v7-dome-apex-rounded.png` vs. `v7-dome-apex-flattened.png`). Worked out real numbers: 22mm plateau diameter (sized against the reference image's proportions), a tangent-constrained blend from the existing spherical-cap dome curve (same technique as the neck-to-collar blend) landing the plateau at ≈29mm height (down ~1mm from the old 30mm point-apex, an expected consequence of blending rather than an arbitrary change). Confirmed, not assumed, that this genuinely eliminates the previously-disclosed apex-drooping/ribbing mechanism (a near-degenerate-closing-point artifact that no longer exists with a flat termination), replacing it with a standard, well-understood flat-top-surface slicer consideration. **Also updated as direct consequences:** §3 (lid build-volume-fit row, combined assembled height ≈192.5mm, down from ≈228.5mm/≈235mm); §8 (removed a now-stale handle-specific justification from the PETG rationale, kept the material recommendation itself unchanged); §13's own v6 row (corrected from a stale "pending" status, per the pattern above). **Nothing about the body (neck/collar/belly/height/cavity volume) changed — this remains a lid-only revision, exactly like v6.** | All five changes were confirmed directly and explicitly by the requester in a single round, including a deliberate reversal of a constraint the concept brief itself called "load-bearing to the design's identity" (the handle) — recorded here as a direct instruction, not a corner cut discovered after the fact. Several of the five changes materially affect each other (the brim shrinking forces the dome base to shrink; the handle's removal changes the height stack and reopens an orientation question; the apex flattening and the handle removal are motivated by the same "flat spot reads as intentional now" reasoning), so this is handled as one coordinated revision rather than five independent patches, per the same rigor this document has applied to every prior multi-dimension rework (v5's neck/collar/lid rework being the closest precedent). |
| v8 (this document) | **Body profile below P3 reshaped for a rounder "thrown-ceramic" silhouette — full spec in the new §4.2.3.** Third size to get this treatment; mirrors Small's §7.7 and Medium's §4.7 (same three-move recipe, same numeric rigor). **Move 1 — belly (P1):** position and radius unchanged; P1 tangent-handle magnitudes lengthened so the apex is a broad swell (target apex radius-of-curvature ≈38mm), not a plateau; explicit no-overshoot constraint so the belly stays the single 153.9mm max-OD point. **Move 2 — shoulder (P2):** demoted from a shape-driving inflection with a tangent break to a **gentle G2 (curvature-continuous) witness** on one fair curve base-to-neck. Large's v7 shoulder was found to sit **≈9.9mm INSIDE its own P1–P3 chord** (internal r 42.42 vs chord r 52.33 at Z 112.5) — the deepest pinch of the three sizes (Medium ~3.7mm inside; Small ~2.3mm *outside*). Smoothing therefore **adds** volume. A full sub-mm witness (Small/Medium style) hand-calcs to **+99.8 cm³** (shell-integral cross-check ≈112 cm³) → ≈1680 cm³ → **+6.4%, outside the ±5% band**. So v8 retains a partial witness: **internal r 45.0mm** (external OD ≈98.0mm) at Z_ext 112.5 (Z unchanged from v7), **≈7.3mm inside the P1–P3 chord**, tangent dr/dz = −0.474 matched both sides — kink removed, gentle soft shoulder retained. **Move 3 — foot:** external foot fillet **R7** (tangent to the flat underside and the foot wall) + internal floor-to-wall fillet **R5** (= floor thickness), continuing the Small R5/R3 → Medium R6/R4 → Large R7/R5 progression. Base OD stays 98mm at the top of the fillet arc. **Volume:** delta-from-verified-baseline method (per §4.2.2's v5 precedent, since Large's frustum chord-sum under-reads the sculpted belly by ~13%): verified v7 cavity ≈1580 cm³ + P1→P3 chord-sum delta **+27.8 cm³** + fairing/fillet corrections (≈0 ±4 cm³) → **≈1608 cm³, +1.8% vs the ≈1579 cm³ target, inside the ±5% band (≈1500–1658 cm³)**, ~50 cm³ under the ceiling. Fallback lever (within the reshaped region only): witness internal radius, sensitivity ≈±11 cm³/mm — deepen toward v7's r 42.42 if CAD lands >~1650, shallow toward r 47.5 (or fatten the swell) if <~1560; do not move any fixed constraint. **Ground-contact footprint** shrinks from ≈98mm to **≈84mm** dia (contact-OD:height 0.64 → 0.55, still stable for a low-CG shelf-display vessel). **New first-print watch item:** the R7 foot-fillet underside dips ~2mm below 45° at the build plate — routine for a rounded foot. **Held fixed (hard constraints):** 153.5mm height, 153.9mm belly OD / ext r 76.966mm, 98mm base OD, 4mm wall (inner wall tracks the new outer at constant offset), 5mm floor, and everything at or above P3 — neck ID 80mm, neck OD 88mm, collar OD 100mm / ID 80mm / 10mm wall / 15mm band, the P3→P4 blend, the bore — all byte-identical to v7. **Lid, plug, and `neck-fit-test` are NOT rebuilt** — they depend only on P3-and-above geometry, which v8 does not touch (reasoning stated in §4.2.3, confirmed the same way it was on Small/Medium). Notes marking v8 changes added to §4.2.1, §4.2.2, §4.3, §9. The Coder rebuilds **only** `urn-body.{step,3mf,stl}` (+ the `.step` CAD source); the hero render is re-shot post-rebuild. `parameters.md` stays at as-built v7 until the Coder rebuilds and the Tester re-verifies. | Requester approved the rounder aesthetic from the visual mockup `concept/v8-rounder-body.png` — *"The large body is approved"* — and had already directed the same change onto Small and Medium (this is the third size). Focused aesthetic revision against an approved mockup, not a from-scratch re-derivation. Smoothing v1/v7's concave shoulder pinch inherently gives cavity volume back; unlike Small/Medium, Large's pinch is deep enough that a full de-kink would breach the ±5% band, so a retained G2 witness plus the flag-back lever keep the built cavity in band **without moving any hard-held constraint**, per the revision brief's explicit instruction. Open item flagged for the requester: Large's shoulder can only be *partially* de-pinched within the volume band — matching Medium's fuller fairing would need the requester to accept a ~+6% cavity, a ~3mm height trim, or a local wall reduction (none authorized by this brief). |
| v1 | Initial spec. Derived internal volume target (1475 cm³) from the requester's 90 lb / 1 in³-per-lb rule, built a frustum-based body profile hitting that target within 0.2%, and worked through the lid/body seating interface, magnet housing, and handle geometry from first principles rather than reusing the concept image's placeholder numbers. | First planning pass for this project, picking up from the approved concept. |
| v2 | **§4.2/§4.3 rewritten:** (1) moved the belly-max control point from 56% up the total height (90mm) to 45% up (72mm), re-deriving the full height/volume table from scratch (not a linear rescale) — new segment heights 67/47/26/15mm vs. v1's 85/35/20/15mm, same 45/69/57/29mm radii, re-verified at ≈1477.8 cm³ (+0.20% vs. the 1474.8 cm³ target, same tolerance as v1); (2) replaced the straight-line frustum-stack-with-small-fillets construction method with a tangent-constrained spline through the same 5 control points (explicit tangency conditions given at each point), to fix a visibly faceted body silhouette. **§6.1/§6.2 corrected:** collar external OD updated from a stale 74mm to the actual settled 78mm (delegated-authority decision made elsewhere but not yet reflected in this document), with the wall-thickness (8→10mm) and magnet bolt-circle (66→68mm) figures propagated to match. **§8 updated:** lid material changed from matte/silk PLA to PETG (decision made after v1, reflected here for the first time), with a new named risk (PETG/PLA finish mismatch) called out rather than silently absorbed. **§9 re-verified:** overhang angles recomputed against the revised §4.2 profile rather than carried over unchecked; found the shoulder-to-neck-taper transition now runs ~47° from vertical (slightly past the 45° guideline) and flagged it as a named, minor consideration for the Tester's first print, not a blocker. | Two real gaps were found by the Coder doing a **direct pixel-measured visual comparison of the built body against `concept-v2.png`**, at the user's request, rather than just re-checking the spec's own numbers against themselves: the belly sat too high (an artifact of v1's derivation being checked only against the volume target, never against the concept's actual silhouette), and the body read as faceted rather than smoothly curved (an artifact of the frustum-stack construction method, not fixable with small fillets alone). Both are fixed here per explicit downstream instruction, with full re-derivation shown rather than a cosmetic patch. |
| v3 | **Magnet-assisted closure removed entirely from the CAD's scope.** §6 rewritten: no magnet pockets, bosses, or any other mechanical/magnetic closure feature are modeled in either part; the lid closure is now defined solely by the flat lid-underside-on-flat-collar-rim seating already described in §5.2. §6.1 replaced — the old "Magnets" hardware table (magnet type/size, count, bolt-circle placement, pocket size, embedding method, polarity note) is deleted outright rather than reworded, since none of it describes anything that still exists in the model. §6.2 reworded, not deleted: the neck collar's OD/ID/wall/height (78mm/58mm/10mm/15mm) are **unchanged** — this was an explicit user decision, made to avoid re-touching a region of the model with a history of three separate manual-edit incidents, accepting the previously-flagged minor concept-fidelity drift (collar reads more "banded" than the concept's continuous neck curve) as a known tradeoff rather than a defect to fix. Only the collar's *stated purpose* changed, from "magnet housing" to "reinforced rim / lid-seating band." Cross-references corrected: §2 (removability no longer attributed to a magnet-assist rationale), §5.2 (removed "magnets' own pull" from the centering discussion and the "magnet pocket fit" tolerance callout, since no pocket exists to have a tolerance on). Checked §8 (material) and §10 (edge cases) for stale magnet-specific risk callouts — none were found; the existing PLA/PETG finish-mismatch risk and the standing PLA heat/UV risk are both about material and finish generally, not about the magnet mechanism, so both are left as-is. | User decided to handle magnet placement (if any) themselves at print time — via a slicer-level pause-and-embed workflow or a fully manual post-print drill-and-glue step — rather than have pockets pre-modeled into the parts. This is a scope reduction requested directly by the user, not a fix for a defect found downstream. The collar band itself was explicitly kept as-is per the user's own instruction, to avoid another manual-edit pass on a part of the model that has already needed three such passes this project. |
| v4 | **§4 substantially revised to consolidate a post-v2 capacity drift into one authoritative record**, rather than leaving it scattered across test logs. §4.1: added a "current binding target" statement — the original ≈1474.8/1477.8 cm³ target is superseded by the now-accepted **≈1579 cm³** built-and-verified capacity (+6.85% over the original), with the reasoning laid out and a business-fit note added for the Reviewer (this is the design becoming *more* generous on capacity, not less). §4.2: added a status callout marking the v2 spline-derivation, frustum table, and ≈1477.8 cm³ figure as **historical provenance only** — no longer the current volume; updated the **P1 (belly) control-point row** to the verified as-built values (external radius **76.97mm**, height **~43–44%** of 160mm as a broad plateau — not the pre-edit 45%, and not the ~50% figure that was briefly and incorrectly reported mid-revision); flagged **P2 (shoulder)** as not independently re-verified against current geometry; confirmed P0/P3/P4 unchanged. **§4.2.1 (new):** authoritative as-built table — cavity volume ≈1579 cm³ (Coder 1578.9824 cm³, Tester-independent 1578.11 cm³), material volume ≈276.0 cm³ (Coder 275.9651 cm³), wall thickness verified ~4.00mm (3.98–4.03mm across ~60 sampled heights, the prior 13.3mm inner/outer peak misalignment fully resolved), and confirmation that the neck-to-collar junction is smooth at print-relevant resolution after a narrowly-scoped repair. §4.3: updated the belly-OD row (146mm → ~153.9mm, tag `DERIVED` → `VERIFIED`) and the wall-thickness row (added as-built verification) to match; flagged the shoulder-OD row (122mm) as unverified against current geometry. §3: updated the body max-OD build-volume-fit figure (146mm → ~154mm) — still clears the 256mm bed by a large margin, not a binding constraint. §6.2: added an addendum confirming a separately-found neck-to-collar crease (in the outer wall, unrelated to the belly/wall rebalance) was fixed with a narrowly-scoped repair (final 5mm of the outer wall's tail near the rim) and independently confirmed. §9: flagged, but did not recompute, that the body's stated overhang angles were derived from the pre-v4 profile and haven't been re-checked against the current as-built geometry. §10 edge case 1: updated the stale ≈1477.8 cm³ capacity reference to the current ≈1579 cm³ figure. | Consolidates a capacity drift that happened in three steps without ever being cleanly restated in one place: (1) v2's spline/profile fix produced a hand-calculated ≈1477.8 cm³ estimate, but the real spline-revolved CAD, once built, measured out to **≈1512 cm³** — a +2.3% deviation from the original 1474.8 cm³ target, within the ±5% band that §4.2's own caveat allowed as routine (not requiring a spec revision), so it was accepted and absorbed without a formal entry at the time. (2) The user then made a direct, intentional **manual edit to the body's outer belly** in Fusion, making it visibly fuller, and explicitly chose to **keep** that change rather than revert it. (3) This left the inner wall not tracking the new outer wall, so the user directed a **rework of the inner wall** to track the outer wall at a constant ~4mm offset (matching the approach used across the rest of the profile) — the resulting cavity, **≈1579 cm³**, is structurally larger than the original target allows, and the user explicitly chose to **accept the larger capacity** rather than thin the wall below ~4mm to force the volume back down. That final step crossed the ±5% tolerance band (+6.85% over the original target) that the spec itself defines as the threshold for a real revision rather than routine sign-off — hence this entry. A separate, unrelated **crease at the neck-to-collar junction** was found and fixed in the same verification pass; it's a narrowly-scoped repair, not connected to the capacity/wall changes, documented here so it isn't lost among the same test logs this revision exists to consolidate. All final numbers were **independently verified by the Tester**, not just Coder-reported, before being written into this spec — per this project's own standing rule that a wrong "final" number should never be silently built around. |
| v5 (this document) | **Neck/collar substantially widened, body height trimmed to compensate, lid resized to match — a full rework, not a number swap.** §4.1: added a v5 status note — the ≈1579 cm³ target itself is unchanged, but the geometry hitting it is fully re-derived. **§4.2.2 (new):** full derivation of the neck ID/OD widening (58mm→80mm ID, 66mm→88mm neck OD, 78mm→100mm collar OD, 10mm collar wall held unchanged), the base-vs-collar proportion check (98mm vs. 100mm, confirmed near-parity, no base-widening needed), the frustum-delta volume method (+69.16 cm³ from the neck/collar widening, applied to the verified 1579 cm³ v4 baseline rather than a from-scratch rebuild of the sculpted belly/shoulder region), the compensating height trim (6.5mm taken entirely from the belly-to-shoulder segment, landing the estimated new total at ≈1578.6 cm³, −0.03% vs. target), the full re-derived P0–P4 control-point table (new total height 153.5mm, belly apex unchanged in absolute mm but now ~45.0% of the shorter total), and a documentation fix (the stale, geometrically-impossible P2 internal radius of 57mm — larger than its own already-corrected 46.42mm external radius — replaced with a corrected/estimated 42.42mm, flagged for Coder re-verification). §4.3: table rewritten with v5-current values for the neck/collar/height rows, old values struck through/retained for reference. §4.4: rewritten — the 80mm ID substantially de-risks (but does not close) the untested-remains-bag-fit concern that has been flagged since v1; explicitly ties resolution to the `neck-fit-test` article being rebuilt. §5.1: full lid rework — brim OD 100mm→122mm (preserving the original 11mm/side overhang margin over the now-wider collar, chosen over a ratio-preserving 128mm alternative, both shown), dome base OD ~80mm→98mm (preserving the original 0.80 dome-to-brim ratio, cross-checked against the new collar ID and found consistent); dome height/brim thickness/total lid height held unchanged. §5.2: fit-check numbers updated to the new 100mm collar / 122mm brim (same 11mm/side margin, no collision, same reasoning as before). §6.2: collar table rewritten to 100mm OD / 80mm ID, 10mm wall explicitly re-affirmed as a kept (not reverted) decision. §9: full overhang re-check against the v5 profile — the belly-to-shoulder segment steepens slightly (still self-supporting, shrinking-radius class) due to the height trim; the shoulder-to-neck-taper segment gets markedly gentler (13.4mm external Δr shrank to 2.4mm); the one previously-flagged risk zone (neck-to-collar external blend) is reasoned, via geometric invariance (same 6mm radius delta, same 7mm blend span, same construction method), to stay at essentially the same ~47.25° peak angle, just relocated — not made meaningfully better or worse by this revision. §2: added the `neck-fit-test` article to the file table for the first time (an oversight in v1–v4) and flagged explicitly that it must be rebuilt at the new dimensions — it is easy to forget since it's a satellite part outside the main body/lid pair. §10: edge case 2 (remains-bag fit) updated to reflect the new 80mm ID and the still-open (though smaller) risk. | Competitor benchmarking (real market research) found the 58mm neck ID a significant outlier against comparable pet urns (114–121mm) and even a direct 3D-printed competitor (~70–100mm estimated) — this also directly de-risks the previously-flagged, never-resolved §4.4 concern about an untested remains-bag fit. The requester chose an 80mm ID as a deliberate compromise short of the 100mm initially considered, specifically to avoid making the collar wider than the 98mm base OD — a proportion/identity concern the requester weighed and decided against crossing. Widening the neck/collar unavoidably adds internal volume near the top of the body; per the requester's explicit instruction, this is compensated by trimming height rather than letting capacity climb further, holding the design to the same ≈1579 cm³ target established in v4. The collar's 10mm reinforcement wall was explicitly kept (not reverted to nominal) even though it lost its magnet-housing purpose back in v3 — the requester values it for structural margin and rim character on its own merits now. The lid was resized because a static 100mm/~80mm lid on a 100mm collar would no longer meaningfully overhang or read as properly proportioned to the much wider opening it caps — this is a real geometry rework of the lid, shown with the same rigor as the original lid derivation, not a cosmetic pass. |
