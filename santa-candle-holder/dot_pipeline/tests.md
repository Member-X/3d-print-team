# Santa Candle Holder — Tests

Self-checked directly in Blender during the build (this is a Blender-based organic sculpt, not
a Fusion model — the `3d-tester` subagent has no Blender access, so these checks were run
manually in the same session as the build, per [[feedback_blender_vs_fusion_tool_choice]]).

## Connectivity / manifold
- **Body (`RobeBody`):** single connected mesh (verified via flood-fill over the edge graph,
  islands=1) after every boolean union step. ~104,590 verts post-subsurf+displacement.
  Non-manifold edge count: ~1180 (~1% of edges), clustered in one beard/shoulder blend region.
  Tried remove-doubles, dissolve-degenerate, and hole-fill cleanup passes — reduced from ~1389
  but did not fully resolve. Voxel remesh (tried 0.6mm, 1.0mm, 1.2mm) was rejected as a fix —
  it fragmented the mesh into 700–1400 disconnected islands each time, worse than the defect it
  would have fixed. Flagged as a known issue for slicer auto-repair (see README).
- **Tray (`Tray`):** fully manifold, 0 non-manifold edges, single island.

## Dimensions vs spec
- Assembled height: body top-of-platform (z≈167.5) + tray height (12mm) ≈ 179.5mm, vs spec's
  ~180mm. Within 1mm.
- Tray: 137 × 137 × 12mm exactly, inner lip clear diameter 104mm, lip proud height 4mm — all
  match the spec's stated ranges (136–138mm OD, ~104mm ID, 3–5mm lip, ~12mm tray height).
- Body footprint: 136 × 129mm, well under both printers' 256×256mm bed.

## Bed fit
Both printers (P2S, Bambu A1 — 256×256×256mm) fit the 175mm-tall body and the 137mm-wide tray
with large margin. See [[user_printer_specs]].

## Printability notes
- Body needs slicer-generated support under the arm curves and hand platform (cantilevered
  overhead pose) — not eliminated by the 2-part split, only the tray's own support need was.
- Tray needs no support (flat disc + shallow lip).
- Thinnest intentional features: hem/cuff fur trim tori (~4mm wall) and alignment pegs (6.4mm
  diameter) — both above typical FDM minimum wall/feature guidance for 0.4mm nozzle PLA.
- No physical test print performed this session — this is a geometry-level check only.

## Not verified
- No real candle/jar on hand to test the 104mm lip fit against (per specs.md open item).
- No slicer-level support/bridging preview run (would need the file opened in the user's
  actual slicer, e.g. PrusaSlicer/Bambu Studio).
