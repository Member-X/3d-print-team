# Tests — Noise Maker: Handle + Clacker (2026-08-25)

Testing method: live Fusion document inspection (`fusion_mcp_read` screenshots at multiple angles/
resolutions, iso-top-right/left, front, right, left, bottom), the main session's own reported
point-containment/ray-cast findings (incorporated and sanity-checked, not re-derived from scratch),
`parameters.md`'s historical trimesh/boolean-intersection data (used as corroborating context only,
flagged where it does not apply to the current pairing), and a websearch sanity-check on FDM
snap/retention interference norms. **No Fusion script-execute access this pass** — anything requiring
fresh numeric measurement of the live bodies is flagged as a follow-up for the main session, not
fabricated.

## 1. Manifold / watertight check

Visual inspection across 6+ screenshot angles shows no visible gaps, self-intersections, or open
shells on the Handle body. The last trimesh-verified export of a Handle built this same way (v2,
pre-dating this session's edits) was `is_watertight=True`, `euler_number=2`, single component
(`parameters.md`). **Not independently re-verified numerically this pass** (no script-execute access)
— recommend the main session re-run `trimesh` on a fresh export before print, since a hex-tip revolve
against a knurl-pattern boolean join (this Handle's actual construction method) is exactly the kind of
operation that has silently produced sliver/debris bodies elsewhere in this project (see this
project's own Fusion-mesh-gotchas memory). **Not a fail — a verification gap.**

## 2. Drop test (accidental knock)

Two features stand out as the drop-vulnerable points, in order of concern:

- **Clacker's flex tang** (original, unchanged, but now interacting with a physically larger tooth
  ring — see §3): any thin cantilevered flex feature is the single most drop/impact-vulnerable
  geometry on this assembly. PLA's low fatigue/impact tolerance on thin flexing sections is a real risk
  here — see §5.
- **Retention bumps + collar wall interaction under an inverted drop.** The task's own analysis
  frames retention as "a genuine mechanical stop, not just close clearance" for *rotation/vibration*
  loads. A **drop** while inverted is a different, higher-energy load case: sudden momentum drives the
  Clacker's far collar wall into the bump lobes all at once, rather than a slow slide. Per the
  websearch sanity check (§ below), typical FDM interference-fit guidance treats **>0.3mm per side as
  a real crack risk** for a wall that has to accept interference; this design's 0.6–1.0mm is roughly
  2–3× that threshold. A slow assembly slide tolerates this fine (that's the geometry's intended job),
  but a **sharp impact against a ~3mm PLA collar wall at this interference magnitude could crack the
  collar** rather than just being stopped by it. Recommend an explicit physical drop test (inverted
  orientation, from a normal handling height, e.g. ~1m onto a hard floor) before calling this closed —
  this is exactly the kind of load a real kid/user *will* apply, and it hasn't been tested, only
  reasoned about geometrically.

## 3. Load / functional test (does the ratchet mechanism work as intended)

No "max load" is stated in the spec for this toy (it's a hand-swung noisemaker, not a structural
bracket) — the relevant functional test is **repeated ratchet-cycle engagement**, not static load:

- **Tooth/tang meshing after this session's tooth growth — UNVERIFIED, flagged as the most concrete
  open functional risk in this design.** The teeth grew +0.5mm radial reach and +4mm axial length this
  session. The only tooth/tang collision check on record in this project (`parameters.md`: 0.57mm³
  residual overlap, judged acceptable) was performed against (a) the *abandoned* parametric-Clacker's
  engineered tang, and (b) the *pre-growth* tooth size. There is no check on record that the grown
  teeth still mesh cleanly with the Clacker's **actual, real, original** flex tang without binding —
  bigger teeth (radially and axially) narrow the clearance envelope the tang was implicitly shaped
  around. This should be checked directly (boolean intersection or measured minimum-distance between
  the live `HandlePart:1` tooth ring and the live Clacker's tang, swept through a full rotation, not
  just at rest) before this is called done.
- **Assembly-window / axial registration got tighter, not looser, from the axial tooth growth.**
  In the prior (now-superseded) parametric build, a 14mm-tall tooth zone inside a 20mm Clacker gap gave
  a 6mm print-in-place registration window. If the *live* Handle's tooth zone grew the same +4mm this
  session, and the Clacker's own gap is unchanged (it must be — Clacker is out of scope), the margin
  for the print-in-place export to land the tooth ring correctly inside the Clacker's open fork region
  is meaningfully smaller than it was. Not necessarily a failure, but a tighter tolerance the coder/
  main session should re-check explicitly rather than assume still fine by analogy to old numbers.
- **Retention-bump mechanical-stop behavior** — per the main session's geometry check, this is a real,
  rotation-independent physical stop (6 discrete bump lobes vs. a full closed collar ring — guaranteed
  overlap with at least one lobe as the wall slides through the bump zone). Geometrically sound
  reasoning; not yet load-tested (see §2's drop-test note — the concern is wall survival under impact,
  not whether the stop exists).

## 4. Fit test — real mating hardware, with clearance beyond the primary opening

Per this team's fit/clearance policy: check the full mating relationship, not just the obvious opening.

- **Hex tip through Clacker's hex collar bore (Y=0 end):** confirmed decorative/non-keyed, loose
  rotational clearance intended, not a precision fit. Low risk as designed.
- **Handle-shaft-through-collar-bore clearance, both collar walls, not just the near one:** the task's
  own numbers (Handle radius 24.50mm at the bump peak vs. Clacker bore 23.5–23.9mm) were checked
  specifically at the bump zone. The **plain shaft OD increase (+0.5mm uniform)** also reduces
  clearance at the *non-bump* Y stations that pass through both collar walls during normal free
  rotation (i.e., the mechanism-head cylinder itself, not just the bump lobes) — this wasn't called out
  as separately re-checked. If the +0.5mm diameter bump pushed the plain mechanism-head OD close to or
  past the Clacker's ~23.5mm minimum-facet bore radius, that would cause constant rubbing/binding
  during every rotation, not just at the bump stop — a materially worse problem than the bump
  interaction. **Recommend an explicit check of mechanism-head OD (post +0.5mm) vs. Clacker bore
  minimum radius, separate from the bump-specific number already checked.**
- **Retention bumps vs. collar wall, all 6 lobes, not just one:** covered — the "closed ring vs. 6
  lobes at any rotation" reasoning in the spec is sound and doesn't need a per-lobe re-check.
- **Support material trapped inside an enclosed mating cavity (the "mounting screw" analog for this
  design):** checked by geometry review. The two collar-wall regions (Y≈0.1–0.5 and Y≈4.0–4.3) are each
  thin thin closed rings around a smoothly tapered shaft with a pre-existing clearance gap — this is
  the standard self-supporting "captured ring" print-in-place geometry (each horizontal layer of the
  ring is a closed loop bridging its own gap, no internal support needed). The teeth and the new
  retention bumps both sit **outside** the two closed-ring regions (teeth are inside the Clacker's
  *open* fork middle; bumps sit just past the far collar wall, outside the Clacker entirely) — so any
  support these features need is externally accessible, not trapped inside an enclosed cavity. This is
  a genuine pass, not an assumption — confirmed by the Y-station layout in `specs.md` §1.

## 5. Material check

- **Handle (PLA):** rigid, non-flexing part (mechanism head, grip, teeth all rigid geometry) — PLA is
  fine here, no change recommended.
- **Clacker's flex tang (thin cantilever, cyclically loaded every ratchet click, original/unchanged
  geometry but now paired with a bigger tooth ring — see §3):** this is precisely the feature class
  this team's policy calls out — thin + mechanically stressed + repeatedly flexed. PLA's brittleness
  under repeated flex/impact is a real risk for exactly this feature. **Recommend PETG** for the
  Clacker specifically (this matches `parameters.md`'s own prior, still-valid reasoning for the
  now-abandoned parametric Clacker — the material argument carries over even though that specific
  geometry was abandoned, since the real Clacker has the same kind of tang). If PLA is kept for
  print-queue/on-hand-material reasons, flag it explicitly as an accepted risk, and consider that the
  now-larger teeth may increase the tang's per-click deflection, compounding the PLA fatigue risk
  rather than leaving it unchanged.
- **Retention bumps / collar wall:** rigid PLA is fine under normal rotational use; flagged only for
  the impact/drop scenario in §2, not general use.

## 6. Overhang / printability check (no slicer CLI available this session — confirmed via `which`/`where`, consistent with this project's own earlier-logged capability gap in `parameters.md`)

- **Gear teeth:** constant cross-section extruded along the Handle's long axis (= vertical print
  axis, per the standing-upright orientation). This means each tooth is a vertical rib running
  parallel to the print direction — self-supporting, no meaningful overhang risk from the teeth
  themselves.
- **6 cone retention bumps:** radial protrusions (axis roughly perpendicular to the vertical print
  axis) — the upper half of each cone, from its widest point up to its tip, is a genuine >45° overhang
  by geometry. The cone shape (vs. the earlier sphere) was the right printability call — cones root a
  wide base directly into existing material and taper to a point, which is the standard technique for
  making small radial bosses self-supporting at this size (a few mm), and is very likely fine without
  supports given the short span involved. Not slicer-verified this pass — recommend checking the
  slicer's support preview specifically over these 6 features before printing, per the spec's own
  flag.
- **Decorative hex-faceted dome cap (Y≈17.6–19.051, grip's far end):** rounded/domed, printed apex-up
  in this orientation (print-in-place / grip-down means the dome is actually the *top* of the whole
  print) — the very top point is a natural bridge/cooling stress point common to any domed top, not a
  new risk introduced by this design specifically.
- **Bed adhesion / orientation:** flat grip-end-down matches the spec's stated orientation; the grip's
  cross-section at the bottom of the print is a plain rounded/knurled cylinder — reasonable first-layer
  contact area, no obvious adhesion concern from geometry alone.

## 7. Websearch sanity check — retention bump interference magnitude

Standard FDM retention/snap-fit guidance (see sources in the final report) puts assemble-by-flexing
interference at ~0.1–0.3mm per side, with >0.3mm flagged as a real hole-wall cracking risk. This
design's 0.6–1.0mm is well above that range — **but** this is not an assemble-by-flexing snap (the
joint is printed already past the bump, never flexed into place), so the "cracks when you snap it
together" failure mode the guidance targets doesn't directly apply at print time. It does apply,
though, to any *later* forced event across that interference — see §2's drop-test framing. Separately:
the same guidance's undercut-engagement range (0.5–1.5mm) is a closer analogy for "how far a catch
should engage to reliably stop something," and 0.6–1.0mm sits inside that range — reasonable as a
static/vibration retention feature, consistent with the spec's own framing, just not necessarily
survivable under an impact.

Comparing to the project's own precedent: the original, proven-working handle's retention bumps were
measured earlier this project at ~3.5–3.8mm raw height / ~2.5mm+ effective radial protrusion over
local baseline — **noticeably larger** than this new design's 0.6–1.0mm. The new bumps are more
conservative (lower crack risk) but also mechanically weaker than the feature they're modeled after —
worth stating plainly rather than assuming "same category of feature" means "same strength."
