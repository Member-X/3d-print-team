# Santa Candle Holder

A Santa Claus figure holding a candle tray overhead, built to match a reference product photo
(see [concept/reference-spec-diagram.png](concept/reference-spec-diagram.png) and
[concept/reference-photo.webp](concept/reference-photo.webp)). Built entirely from scratch in
Blender — no purchased source model — for personal home decor.

## What's here

Two separate STL parts, designed to print independently and join with alignment pegs:

- **`stl/santa-body.stl`** — the Santa figure: robe, belt, beard, hat, and both arms raised
  overhead into a flat hand platform. ~136 × 129 × 175mm.
- **`stl/santa-tray.stl`** — the candle tray: 137mm outer diameter, 104mm inner lip diameter,
  12mm tall, with a ~4mm retaining lip so a standard 3-wick jar candle won't slide off. Sits on
  top of the body's hand platform.

Assembled height is ~180mm, matching the reference image's stated total height.

## Why two parts

The arms-overhead pose holding a wide tray is a big overhang for FDM printing. Printing the
tray separately avoids needing heavy support material directly under a 137mm-wide disc (which
would leave a rough, hard-to-clean underside). The body still needs some support under the
arm curves and hand platform — that's normal for this pose and any slicer's auto-support
handles it.

Three 6.4mm-diameter alignment pegs on the body's hand platform (top surface, ~z=169.5mm) mate
with matching blind sockets in the tray's underside, so the tray self-centers when you glue the
two parts together after printing.

## Print settings

- **Material:** PLA (user's default; see parameters.md).
- **Orientation:** print both parts exactly as exported — bed face already at Z=0.
- **Supports:** enable supports for the body (arm undersides, hand platform overhang). The
  tray needs no supports (flat, simple disc).
- **Known mesh issue:** the body STL has a small number of non-manifold edges (~1% of edges,
  clustered in one beard/shoulder blend area) left over from the boolean-heavy build process.
  Every mainstream slicer (PrusaSlicer, Cura, Bambu Studio, OrcaSlicer) auto-repairs this kind
  of minor defect during slicing — if yours flags it, run its "fix mesh" / "repair" option (or
  Windows 3D Builder's Repair tool) before slicing.

## Detail level

Built as a "high-detail attempt" per request: boolean-sculpted face/beard/hat/robe form, then
smoothed with Catmull-Clark subdivision, then a weighted procedural noise pass for beard curls,
fur trim (hem, cuffs, hat band), and subtle robe fabric folds — with the face kept smooth. This
is a stylized, hand-scripted sculpt, not a scan or a purchased model, so it won't match the
reference photo's photographic realism — FDM PLA at this scale wouldn't resolve that level of
detail anyway.

## Not yet done

- No independent print-in-hand verification (no physical test print yet).
- No 3MF export — this Blender install has no bundled 3MF exporter (STL/OBJ/FBX only, same
  limitation hit on the cat-bowl project). STL is provided for both parts.
- No STEP file — this is a mesh sculpt, not parametric CAD, so there's no STEP equivalent.
