# Reviewer Verdict — Lightswitch-Cover-Single (Jumbo Single-Gang Toggle Plate)

## APPROVE (with one required documentation fix, non-blocking for print)

Both test targets are cleared for export/printing:

- **`Lightswitch Cover Single V2 (corrected jumbo)`** — cleared
- **`Lightswitch Cover Single V2 (tapered edge)`** — cleared

`Body1` remains reference-only and is correctly **not** cleared for shipping (confirmed
unmodified — see §3 below).

This review independently re-measured the live Fusion geometry (own script pass, not a re-read
of `tests.md`) and cross-checked the hardware standards against external sources. One real
documentation defect was found in `specs.md` (a leftover incorrect number, not caught by the
correction pass) — detailed in §4. It does not affect the exported geometry and does not block
printing, but it should be fixed before this spec is called complete.

---

## 1. Business fit — PASS

The stated problem is a jumbo/oversized single-gang toggle wall plate that actually installs on
a real switch, printable on standard FDM. This is met:

- 3.5" × 5.5" (88.9mm × 139.7mm) is a real, commonly sold "jumbo/oversized single-gang toggle"
  wall plate size — confirmed via independent web search against multiple retailers (Amazon
  listings explicitly describe "Jumbo Light Switch Cover Oversize 1-Gang 5.5\" x 3.5\""),
  matching `specs.md` §2 exactly.
- The relief pocket clears a real toggle-switch yoke (44.45mm × 74.625mm) by 20.6mm / 30.9mm per
  side — huge margin, no interference risk.
- The critical fixed bug (screw channel too long/tight to seat a real screw) was independently
  re-verified: I confirmed by direct point-containment testing in Fusion that the space between
  the boss floor (Y=3.10mm) and the back face (Y=0) is empty on both screw holes — a screw
  inserted from the front can physically pass all the way through. This matches the Tester's
  face-enumeration finding via a different method.
- Material volume is trivial (see §5) — nothing about the geometry makes this impractical to
  print on a standard 0.4mm-nozzle FDM setup.

## 2. Technical parity — PASS, independently re-verified

I did not take the PASS verdict at face value. I opened the live document
(`urn:adsk.wipprod:dm.lineage:SszZxJywRyKQ40XwWnR3GQ`) myself and ran my own Fusion script pass,
independent of `tests.md`'s script:

| Check | My independent measurement | Spec value | Match |
|---|---|---|---|
| Overall envelope (both target bodies) | 88.9000 × 5.0000 × 139.7000 mm | 88.9 × 5 × 139.7mm | Exact |
| Body volumes | 22.4765 cm³ / 22.0409 cm³ | (matches `tests.md` exactly) | Exact |
| Screw hole spacing | Shank cylinders at Z=±30.1625mm → 60.3250mm | 60.325mm | Exact |
| Screw shank diameter | r=2.3813mm → ⌀4.7625mm | 4.7625mm (3/16") | Exact |
| Countersink half-angle | 45.00° (genuine Cone surface) | 90° included | Exact |
| Boss collar diameter | r=4.5mm → ⌀9.0mm | 9mm | Exact |
| Toggle opening | corner-radius cylinders (r=1.59mm) at ±5.16mm/±10.315mm offsets → 10.32×23.81mm opening | 10.32mm × 23.81mm | Exact |
| Rim inset / cavity footprint | ceiling face bbox 85.60 × 136.40mm; inset = (88.9−85.6)/2 = 1.65mm | 1.65mm inset / 85.6×136.4mm | Exact |
| Outer fillet radius | r=2.35mm cylinders at 4 corners | ~2.35mm | Exact |
| Open screw path | point-containment test: void from Y=0 to Y=3.10mm at both hole centers | "opens into fully open cavity" | Confirmed |

**Hardware standard cross-check (external, beyond what the Tester did):** I searched independently
for switch-plate screw-hole geometry and found (Kyle Switch Plates, a name already cited in
`specs.md`'s own sourcing): *"The screw holes themselves are 5/16\" across at the top and taper
to a 3/16\" opening at the bottom."* That is **exactly** this model's countersink construction —
7.9375mm (5/16") top diameter tapering via a genuine cone to 4.7625mm (3/16") — confirming the
screw-hole geometry is a real switch-plate hardware convention, not an invented number. (Real
switch-plate screws are 6-32 threaded, ~3.5mm major diameter, which passes with clearance through
the 3/16" taper — consistent, no interference.) NEMA toggle strap spacing of 2.375" is standard
industry knowledge and is also already in consistent use elsewhere in this project
(`switch-plate-covers/parameters.md`, double-gang plate).

I'm treating this as solid technical parity — the numbers aren't just internally self-consistent,
they match real hardware.

## 3. Body/topology sanity — PASS

- `Body1`: 80.0 × 5.0 × 125.0mm bounding box, unchanged — confirms it is genuinely kept as an
  unmodified original-draft reference (matches the "80mm × 125mm" original-draft number cited in
  `specs.md` §1), not shipped. Correct per the stated project intent.
- Both target bodies are single solids (`isSolid=True`), confirming no split geometry.
- Tapered-edge body's fillet-only diff (already verified by the Tester via face histogram) is
  plausible and not something I re-derived in full, but the shared bounding box, volume delta
  (22.48→22.04 cm³, consistent with removing material via edge fillets), and face-count delta are
  all consistent with a fillet-only change.

## 4. Documentation completeness — ONE ERROR FOUND, requires fix

`specs.md` was mostly corrected accurately — I independently confirmed the corrected rim
inset (1.65mm) and cavity footprint (85.6×136.4mm) in §5/§9 match the live geometry exactly, so
the main correction from the screw-hole revision round was applied correctly.

**However, one stale/incorrect value survived the correction pass:**

`specs.md` §5 and §9 both state:

> Boss collar depth (from front skin, i.e. how far the collar hangs into the cavity): **1.9mm**
> (matches guide-channel depth) — tagged **VERIFIED — geometry**

This is wrong, and it **contradicts `tests.md`'s own §5 finding on the same page**: *"the flat
annulus at Y=3.10mm... connects to the rest of the solid only from above, via the **0.25mm-tall**
collar wall up to the skin ceiling at Y=3.35mm."*

I independently measured the two relevant planar faces directly in Fusion:
- Cavity ceiling (general skin underside): **Y = 3.3500mm**
- Boss floor annulus (both holes): **Y = 3.1000mm**
- Collar wall height = 3.35 − 3.10 = **0.25mm**, not 1.9mm.

The 1.9mm figure is actually the **total guide-channel depth measured from the front face**
(Y=5.0 → Y=3.10), a real and correctly-stated number elsewhere in the same section — it's just
been copy-pasted into the wrong field and mislabeled as "how far the collar hangs into the
cavity," which is a different, smaller dimension (0.25mm). Because it's tagged "VERIFIED —
geometry," this is a false verification claim as currently written.

**Impact:** none on the physical part — the exported geometry is correct and this was just a
labeling/transcription error in the prose, not a modeling error. It does not block printing. It
should be corrected (change 1.9mm → 0.25mm in `specs.md` §5 and §9, and reword so "guide-channel
depth" and "collar wall height" are clearly distinguished) before this spec is considered fully
accurate documentation.

Revision history (§1) is otherwise clear and specific about what changed and why (jumbo size,
screw spacing, toggle opening, corner radius, and the mid-project screw-channel/boss-collar
rebuild) — no other stale numbers found in a full read-through.

## 5. Cost / practicality — PASS

Volume 22.48 cm³ for the primary body (22.04 cm³ for the tapered variant) — at PETG density
(~1.27 g/cm³) that's roughly **28–29 grams**, i.e. a few cents of filament. The design is already
a shelled/open-cavity part (not solid), so there's no excessive-infill concern, and nothing about
the size (139.7mm max dimension) is unusual for a standard FDM bed. The one process note already
flagged by the Tester — a small ~9mm-diameter unsupported bridge at each boss floor — is real
(confirmed independently: it's a 0.25mm-thick floor spanning open cavity below) but small enough
that it's a first-layer/bridging-setting check, not a redesign or reject condition.

## What would have blocked this pass (none found)

- A geometry mismatch between `specs.md`'s claimed values and the live Fusion model — not found,
  full independent re-measurement matched on every dimension checked except the collar-depth
  labeling error above (which is prose-only, not a geometry error).
- An unverifiable or fabricated hardware standard — not found; the screw-hole taper geometry
  matches an independently-sourced real switch-plate hardware description exactly.
- A blocked screw path, split body, or non-manifold geometry — not found (re-confirmed
  independently).
- Impractical print economics or geometry — not found.

## Action item before closing out this revision

Fix the "Boss collar depth" value in `specs.md` §5 and §9 (1.9mm → 0.25mm, with clearer wording
distinguishing it from the 1.9mm guide-channel depth). This does not block export/printing of the
two cleared bodies.
