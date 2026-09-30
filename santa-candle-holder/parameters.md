# Santa Candle Holder — Parameters (recreate-from-scratch reference)

Everything below is baked into the Blender build script used this session
(`santa-candle-holder-wip.blend` holds the live scene). All coordinates in mm, Blender world
space, character facing -Y, up = +Z, base of figure at Z=0.

## Body (Part A) — `RobeBody` object

**Robe silhouette** — lathed (bmesh spin, 64 steps) from this radius/height profile:
```
(0,0) (58,0) (60,4) (57,9) (50,20) (44,35) (42,48) (46,60) (53,76)
(50,88) (44,97) (32,102) (20,107) (14,112) (0,116)
```

**Face + beard** — boolean union of UV spheres (EXACT solver):
- skull (0,-2,130) r24 · nose (0,-27,127) r7 · cheeks (±15,-18,126) r9 · jaw (0,-16,114) r15
- beard cascade (x,y,z,r): (0,-28,104,19) (0,-36,93,23) (0,-40,82,22) (0,-37,71,18) (0,-29,61,13)
  (0,-20,53,8) (±22,-26,97,17) (±30,-30,85,16) (±26,-28,72,13)
- mustache (±8,-31,117) r6.5, (±3,-32,115) r4.5
- eye sockets (subtract): (±10,-22,133) r5 · pupils (±10,-20,132) r3.2
- eyebrows: (±10,-24,138) r3.2, scale (1.9, 0.6, 0.45)

**Hat** — cone (r1=24, r2=0, depth=48) at (0,-2,150), Simple Deform Bend modifier
(axis X, angle 125°, limits 0.32–1.0) applied, then translated -10 in Z. Pompom = r8 sphere at
the bent tip's final position. Band = torus (major 25, minor 4.5) at (0,-2,126), scaled z×0.6.

**Belt/buckle/hem** — belt: cylinder r47 depth11 at (0,0,49). Buckle: cube scaled (9,4,6) at
(0,-48,49). Hem: torus (major 59, minor 6) at (0,0,6), scaled z×0.7.

**Arms** — bezier curves, bevel_depth 9mm, tapered via per-point radius (1.35→0.9):
- Right: (46,-18,96)→(58,-32,122)→(50,-20,148)→(28,4,163)→(13,8,167)
- Left: mirrored on X
Converted to mesh, open boundary loops capped via `bmesh.ops.holes_fill`.

**Hand platform** — cylinder r58 depth9 at (0,3,163) (top surface z≈167.5). Shoulder cuffs:
tori (major13/minor4) at (±46,-18,96). Finger bumps: spheres r6.5 at x∈{-20,-9,9,20},
(y,z)=(-56,160), scaled (1,1.3,0.85).

**Alignment pegs** — cylinders r3.2 depth5 at (28,23), (-28,23), (0,-27), top z=169.5.

## Finishing pipeline (applied in this order)
1. Catmull-Clark subsurf, 2 levels (topology-preserving smoothing of all boolean seams).
2. Per-vertex weighted noise displacement (Perlin turbulence, 3 octaves, freq 0.11) — amplitude
   capped per region: beard 1.0mm, hat band 0.75mm, hat cone body 0.3mm, hem/cuff trim 0.3mm
   (kept low — thin geometry), general robe 0.25mm, face zone suppressed ~92%.
3. Non-manifold cleanup pass (remove-doubles, dissolve-degenerate, hole-fill) — reduced but did
   not fully eliminate non-manifold edges (see README "Known mesh issue").

**Note:** voxel remesh was tried at multiple sizes (0.6–1.2mm) as a manifold-guarantee step and
rejected — it fragmented this mesh into hundreds of disconnected islands both before and after
displacement (same failure mode as [[feedback_blender_dense_mesh_viewport_artifacts]]'s cousin
issue from the cat-bowl project, but worse here — no single dominant island to keep). Catmull-
Clark subsurf was used instead specifically because it cannot break mesh connectivity.

## Tray (Part B) — `Tray` object
- Floor: cylinder r68.5 (Ø137mm) depth8, at (0,3,4) — center offset to Y=3 to match the hand
  platform's axis.
- Lip: ring (outer r56, inner r52 cut, i.e. ~4mm wall) depth4, sitting on top of the floor
  (proud height 4mm, within the 3–5mm spec range). Inner clear diameter = 104mm.
- Sockets: cylinders r3.6 depth6 at the same (x,y) as the body's pegs, cut into the underside.

## Printer / material
P2S or Bambu A1 (both 256×256×256mm bed) — comfortable fit. PLA default. See
[[user_printer_specs]].
