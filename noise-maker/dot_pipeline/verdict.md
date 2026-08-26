# Verdict — Noise Maker: Handle + Clacker (2026-08-25)

## Overall: PASS, with open issues #1 and #2 below now resolved (main session, post-tester)

Nothing found here is a fundamental design failure. The Handle rebuild (twist → knurl, hex-tip
mechanism head, cone retention bumps) is a sound, well-reasoned approach, and the print-in-place
concept is geometrically workable. This session's changes (tooth growth, diameter growth,
sphere→cone retention bumps) were reasoned about geometrically and not re-verified end-to-end against
the *actual* current pairing (new Handle vs. original mesh Clacker) the way earlier iterations of this
project were (boolean intersection + trimesh) — the two concrete gaps below were closed with fresh,
direct point-containment/ray-cast verification against the live geometry (main session has
Fusion script-execute access; this tester pass did not).

## UPDATE (main session, same day): open issues #1 and #2 resolved

**Issue #1 (tooth/tang meshing) — was worse than suspected, now fixed.** A fresh full-circle,
multi-height scan (Y=1.0–3.4cm, every 3° near the fork's mouth, at both Handle-teeth and
Clacker-mesh actual surfaces) found the true closest approach was **1.62mm of clearance** (tooth
radius ~30.1mm vs. nearest Clacker material ~31.7mm) — i.e. the grown teeth were not making contact
with the Clacker at all, the opposite failure mode from the binding/jamming risk flagged below (no
engagement = silent, non-functional ratchet). This contradicted an earlier, less rigorous
same-session claim of "~0.58mm interference" that turned out not to hold up under a real full-sweep
check.

Fix applied: grew the same 75 tooth-tip faces (identified by radius >26mm within Y=0.9–3.6cm) via
three incremental `OffsetFacesFeatures` passes — +1.0mm, +0.5mm, +0.2mm (a single +2mm pass failed
Fusion's geometry heal step; smaller increments succeeded). Final verified result: **-0.09mm real
interference** at the same closest-approach point (31.79mm tooth vs. 31.7mm Clacker), consistent
across the full Y=1.4–3.4cm teeth band, body remains `isValid=True`. Net cumulative tooth growth
this project: +0.5mm (earlier) +1.7mm (this fix) = +2.2mm radial reach from the original.

Design note: the user asked whether extending the Clacker's tang instead would avoid this rather
than growing the teeth further. Confirmed via the same geometry that the teeth zone (Y=1.0–3.5cm)
and the collar/bore-wall zone (Y=0.1–0.5cm and Y=4.0–4.3cm) are disjoint — tooth growth cannot reach
the bore walls. Growing the Handle's teeth was chosen over modifying the Clacker because the Clacker
is explicitly out of scope for this rebuild (user requirement, stated repeatedly this project) and is
a dense mesh body, much more failure-prone to edit precisely than the Handle's clean BRep solid.

**Issue #2 (general shaft clearance, not just bump zone) — checked, fine, unaffected by the fix
above.** Direct radius scan at the mechanism-head shaft (the plain rotating cylinder, not the bump or
teeth): front collar wall (Y=0.1–0.5cm) shaft radius 22.76–23.24mm vs. Clacker bore 23.52–23.88mm →
~0.28–1.1mm clearance depending on angle (tightest point 0.28mm — snug but positive, matches the
~0.3–0.4mm centering correction made earlier this session). Back collar wall (Y=4.0–4.3cm) shows the
same ~22.75–23.24mm shaft radius. Re-confirmed unchanged after the tooth-growth fix above (tooth
offset was scoped to Y=0.9–3.6cm only, doesn't touch either collar wall). No binding risk identified
in the free-rotation zones.

## Blocking item: ESTIMATED dimension underlying multiple downstream features

**The Clacker's bore/collar radius (~23.5–23.9mm, hex-faceted) is not a caliper-verified ground-truth
number** — it comes from point-containment/ray-cast probing of a mesh body this session (better than
the ~573-vertex Tinkercad sampling used earlier in the project per `parameters.md`, but still a CAD
probe of an imported mesh, not a physical measurement). The new Handle's mechanism-head OD, tooth-ring
radius, and retention-bump peak radius (24.50mm) are all sized directly against this number. Per this
team's QA policy, an ESTIMATED dimension that mates with the part's own physical counterpart should be
verified or explicitly risk-accepted before being treated as resolved — this hasn't happened yet here.

**Recommended resolution (pick one, both cheap):**
1. If the physically-separated original Clacker part exists (it was separated in Tinkercad earlier in
   this project, implying a real or precisely-modeled reference may exist) — take a direct caliper
   measurement of the bore radius/hex facets and compare against the 23.5–23.9mm CAD-probed figure.
2. Otherwise, get explicit written acceptance from the user that the current point-containment-probed
   number is trusted as-is, given the first print itself will be the real-world confirmation either
   way (no off-the-shelf hardware is involved here, so "verify against real hardware" effectively means
   "verify against the first print").

This isn't a request to block indefinitely — either path is fast — but it shouldn't be silently
skipped, since it's the number three separate new/changed Handle features (mechanism OD, teeth,
bumps) all key off.

## Concrete open issue #1: tooth-growth/tang meshing not re-verified

This session grew the gear teeth +0.5mm radial reach and +4mm axial length. The only tooth/tang
collision check on record in this project (0.57mm³ residual overlap) was performed against a since-
abandoned parametric Clacker design and the *pre-growth* tooth size — it does not cover the grown
teeth against the Clacker's real, original flex tang. **This is the single most important functional
check to run before printing** — a mis-meshing tooth ring (too deep, too long) risks the ratchet
binding/jamming rather than clicking, which would be a functional failure of the whole point of the
toy, not just a cosmetic issue. Recommend a direct minimum-distance/boolean-intersection check between
the live `HandlePart:1` tooth ring and the live Clacker's actual tang geometry, swept through rotation,
not just checked at rest — this requires Fusion script-execute access I don't have this pass.

## Concrete open issue #2: mechanism-head OD vs. Clacker bore, general clearance (not just the bump zone)

The +0.5mm uniform diameter increase was checked at the retention-bump peak (24.50mm vs. 23.5–23.9mm
bore — confirmed as intentional interference). It was **not** separately confirmed at the plain
mechanism-head cylinder (the part of the shaft that rotates freely inside the collar during normal
use, not the bump). If that OD also crept close to or past the bore's ~23.5mm minimum facet radius,
every rotation — not just the retention stop — would bind. Cheap to check, and should be checked before
this is considered done, since it would be a much worse failure mode (constant friction/binding) than
anything else flagged here.

## Lower-priority, non-blocking flags

- **Drop test (inverted, impact):** the 0.6–1.0mm bump interference is ~2–3× typical FDM crack-risk
  thresholds for a forced interference event against a ~3mm PLA collar wall. Fine for the
  slow-slide/vibration case the geometry was designed for; untested for a hard knock. Recommend a
  physical drop test before calling the retention feature fully validated, not just a geometric review.
- **Material:** recommend PETG for the Clacker specifically (the flex tang is a cyclically-loaded thin
  feature — PLA's brittleness is a real fatigue/impact risk there), consistent with this project's own
  earlier material-flag reasoning. Handle can stay PLA — no flexing feature on that part.
- **Manifold/watertight check:** not independently re-verified numerically this pass (no
  script-execute access) — last known-good check on a similarly-built Handle was clean, but this is a
  "should re-check before printing," not a known problem.
- **`dot_pipeline/parameters.md` is now out of sync with the live document** (still describes an
  abandoned fully-parametric Clacker as "current") — flagging so it doesn't mislead the next person who
  reads it; not this pass's job to rewrite, but worth a follow-up pass.

## What would flip this to a clean PASS

Closing the ESTIMATED-dimension item (§ above) plus a fresh Fusion-side check of open issues #1 and #2
(both require script-execute access this Tester pass didn't have). Everything else here is either
already reasonably mitigated by design choices already made (cone bumps over spheres, hex tip left
non-keyed, print-in-place support-trapping avoided by construction) or a lower-stakes recommendation
(PETG for the Clacker, a physical drop test) rather than a hard blocker.
