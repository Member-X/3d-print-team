# Stage 2 build log: full "Pumpkin Hug" figure

Short milestone notes from the 3d-blender-modeler, newest at the bottom.

## 2026-09-24 start
- Read spec v1.1, concept-a.png plus the 5 turnaround views, visual-brief.md, the light-kit drawing, parameters.md, params.py and the stage-1 scripts.
- Blender state: `halloween-cat-test-parts.blend` open and saved (not dirty). Blender 5.2.2, numpy 2.3.4 and OpenVDB (Python module) available, so no scipy is needed.
- Measured the concept numerically, not by eye, using the image's pixels. The figure axis is at column 502.3. Arm span 643 px = 109.9 mm. Head 488 px = 83.4 mm, widest at the cheeks (level z about 105). Cat eye centres at +/-17.1 mm, eye OD about 17 mm. Pumpkin width 505 px = 86.3 mm. Pumpkin eye centres at +/-16.0 mm.
- Plan:
  - Outer envelope built from implicit fields on a 0.5 mm grid (numpy), meshed with OpenVDB.
  - Chamber derived from the exact distance to the outer mesh, so walls are a uniform 2.0 / 3.0 mm, with 45 deg cone roofs.
  - Stage-1 base void, window pockets and colour zones applied with EXACT booleans.

## Milestone 1: envelope, chamber, master shell (v1, v2 saved in blender/versions/)
- `face_outlines.py` traced the pumpkin eyes, nose and mouth from the concept with sub-pixel marching squares, then enforced the rules:
  - corner radius >= 2 on the eyes and nose; every yellow gap >= 3 (opening r 1.5 on the mouth);
  - webs measured at 5.7 to 16.2 mm (>= 4); teeth about 6.5 W x 4.3 H (top) and 8.0 W x 4.7 H (bottom).
  - Cat eyes per spec. Cat nose traced and scaled to 8.5 x 6.5. The mouth is two arcs, 22 W, sag 3, 1.6 wide. The stem clears the mouth by 4.0.
- Ear fitted to the concept outline: corner radius 8.5, rms 0.27 mm.
- Envelope: one manifold shell, bbox exactly +/-60 x +/-60 x 0..150.007. Level-view overlay IoU against the concept is 0.93.
- Outer distance D_out: the OpenVDB level set was off by up to 0.93 mm, so the 1.9 M voxels in the wall band were refined to exact point-to-mesh distance.
- Chamber: one connected void of 502 cm3.
  - Walls are 2.0 (cat) / 3.0 (pumpkin, and black within 3 mm of the pumpkin).
  - Roof bridges: head Ø20 at z 134.3, pumpkin Ø30 at z 79.0.
  - DEVIATION: the roof cones are 58 deg from vertical in the front sector and 45 deg elsewhere. With 45 deg all round, 98% of each pumpkin eye and half of each cat eye sat behind 5-15 mm of wall. Now the cat eyes have the plain wall; pumpkin eyes median 3.9 mm, max 9.4 mm at the apex tips (measured along Y).
- A13, chamber mesh: every ceiling face is <= 60 deg except the two bridges and their anchoring corners (~114 mm2 of 60-85 deg faces, all at the bridge edges).
- A6:
  - neck overlap 1179-1288 mm2 (z 89.5-96.5); minimum chamber section 1464 mm2 (53 x 36);
  - plenum -> torso 1587 mm2 (53.5 x 38);
  - plenum -> pumpkin: only 114-730 mm2 at the deck plane (narrow skirt), but 2038 mm2 (53.5 x 49) of direct vertical line of sight;
  - pumpkin <-> torso 3488 mm2.
- Next: EXACT boolean with the stage-1 base void, then the window pockets.

## Milestone 2: stage-1 base void applied (v4)
- `build_base_void()` repeats `build_test_parts.build_coupon('flex')` with the same helpers, order and angular phases. Only two lengths differ: the plenum bore runs to z 18 (inside the chamber) and the tunnel runs past the r 60 edge.
- EXACT difference took 7 s. M1 is 1 shell with 0 non-manifold and 0 boundary edges. It removed 40,370 mm3 (hand estimate about 39,500).
- Identity with the printed coupon, inside r <= 44, z 0..15.5:
  - volumes 49,302.5928 vs 49,302.5928 mm3;
  - 299,992 of 300,000 random points classify the same; the 8 mismatches all lie within 2.5 mm of the artificial r 44 cut (ray-parity edge grazing).
  - The symmetric-difference booleans returned garbage (the EXACT solver fails on fully coincident surfaces), so they were not used.
- Every stage-1 probe passes on the full figure:
  - pocket Ø61.200 (38 probes); shelf underside z 11.0; aperture 53.998-54.000;
  - tabs at 60/180/300, engagement 0.900, top z 2.4, chord 8.95; arms 1.6 thick, slots 2.2, end gap 1.18-1.21;
  - tunnel 7.0 x 10.0, roof 6.0, clear from pocket to edge; base Ø119.998; bottom flat at z 0, contact area 7,476 mm2.
- (Session was interrupted by an API rate limit after this. Resumed with Blender still holding the v4 state.)
- Next: window pocket cutters, yellow and pink zones.

## Milestone 3: window pockets and five colour parts (v5, v6, v7)
- Problem found while building the pocket cutters: above each eye the 45 deg flank never meets the receding roof cone. A pocket that carves "back to the chamber" per column tunnels through thick roof wall, and leaves flat ceilings where it stops.
- Fixed in the chamber instead (v5): the roof is now the upper envelope of 58 deg cones from a point apex behind EVERY window column (at the natural 3 mm / 2 mm cavity entry), plus the main roof cones.
  - Measured max wall along the ray behind the windows: cat eyes 2.00, pumpkin eyes 3.05, nose and mouth 3.00. The pumpkin-eye apex is still 5.8 mm along Y, only because the 3 mm wall is oblique on the 47 deg shoulder.
  - New ceiling faces over 60 deg are only narrow crests where cones meet: 83 strips, widest 2.43 mm, 86 mm2 total. As bridges they are far inside the limits.
- Pocket back-limit: never deeper than the chamber behind the NEAREST window point, so flanks outside an outline pinch off in a 45 deg wedge.
- Cutters and zones were meshed on 0.2 mm local grids.
  - Skin floor = exact 0.5 mm offset of the outer mesh along its normal (26-step bisection on point-to-mesh distance).
  - Pocket floor runs 0.08 mm past each outline, so no edge coincides with a zone wall.
  - Pink back face = exact 1.0 mm offset.
- M2 = M1 - pockets (EXACT). Cat pockets removed 887.8 mm3; pumpkin pockets removed 3501.0 mm3.
  - The EXACT solver left tiny defects: one 8-vertex speck, a zero-length edge and one sub-mm hole. Repaired by merging vertices within 0.1 um and filling one hole. Volume unchanged.
- Zones: orange and green from field bisectors (0.5 mm grid, one shell each).
  - Found and fixed a 0/0 at ellipsoid centres (thigh centre fell on a grid node) that made a one-voxel orange island. Envelope inside/outside classification unchanged (0 sign differences).
- Parts, all by EXACT booleans, each boundary coming from ONE zone surface:
  - black = M2 - Zo - Zg - Yall - P: 292,003.0 mm3, 3 shells (body + 2 pupils).
  - orange = M2 ∩ Zo - Zg - Yall: 29,286.1 mm3, 1 shell.
  - yellow = M2 ∩ Yall: 701.3 mm3, 6 shells.
  - green = M2 ∩ Zg: 1,727.8 mm3, 1 shell.
  - pink = M2 ∩ P: 87.5 mm3, 2 shells.
  - Sum 323,805.7 vs master 323,806.0 (0.0001%).
  - Solver defects repaired: orange had one coincident double face (deleted); black had one missing triangle at the tunnel exit (filled). All parts are now 0 non-manifold, 0 boundary edges.
- Next: full A1-A14 verification, STL/3MF export with read-back, renders.

## Milestone 4: plinth fix, fold-free meshes, final parts (v8-v12)
- The A7 wall probe found real thin spots: black 0.84 mm and orange 0.50-1.41 mm at r ~27 just above the deck. In small crease gaps between the pumpkin skirt, the feet and the torso, the figure left the deck bare or covered by only 0.5 mm, right over the Ø54 plenum bore.
  - Fix: a low plinth in the black envelope, r 31.5 with a 45 deg chamfer to a flat top at z 21, smooth-blended so it reads as a crease fill. It covers the bore with >= 3 mm and is hidden under the figure except in those gaps.
- Self-intersections: the parts had 14-78 crossing triangle pairs.
  - Cause: the EXACT solver cutting warped OpenVDB quads produces warped polygons, which fold when triangulated.
  - Fix: every OpenVDB mesh is triangulated with BEAUTY right after meshing (tested: 0 crossings; the fixed 0-2 diagonal gives 448), so the booleans only see planar faces. M2 then had 0 crossings.
  - The remaining 4-14 micro-folds per part on cut seams (triangles 0.0002-0.1 mm2, vertices 1-40 um apart) were relaxed locally: only the vertices of crossing triangles moved, largest move 0.13 mm, topology and volume unchanged. Edge-collapse was tried first and broke manifoldness, so it was rejected (reverted by reloading v11).
- Final parts (v12): black 292,471.4 mm3 (3 shells), orange 28,841.7 (1), yellow 701.5 (6), green 1,728.0 (1), pink 87.5 (2).
  - All 0 non-manifold, 0 boundary, 0 crossing triangle pairs. Sum = master 323,830.1 exactly.
- Viewport screenshots are black: the Blender window is not being drawn (minimized?). Renders will use a Workbench render through an explicit orthographic camera, and every image gets checked.
- Next: A1-A14 verification on the final parts, exports with read-back, renders.

## Milestone 5: A1-A14 verified on the final parts, exported (v13)
- A second API rate-limit pause happened during a slow check (a per-face Python loop that ran until 01:05). Blender stayed alive with the v12 state. One later experiment (merging vertices within 2 um) broke manifoldness and was reverted by reloading v12.
- Measured on the final parts:
  - A1: bbox ±60 x ±60 x 0..150.0073, bottom at z 0 (±4e-15).
  - A2: base Ø119.999, deck z 15.995-15.997.
  - A3/A5: all stage-1 probes identical on the black part.
  - A4: puck touches only the 3 tabs; ring clear; cables 4/5 clear for exit z 4.5-7.5.
  - A6: one void, 504.4 cm3. Neck minimum 1464.5 mm2 (53.5 x 36.5); link 1179 mm2 (43.5 x 31.5). Plenum line of sight 2134 (pumpkin) and 1984 (torso) mm2. Pumpkin-torso 3488 mm2.
  - A7: black min 1.985 (p1 1.999) outside the window flank zone. Orange >= 2.88 from 5 mm out; in the 45 deg flank halo within 5 mm it thins (4-5 mm: 2.52, 3.5-4: 2.14).
  - A8: 6 yellow shells; skin 0.4997-0.5078 mm at 4,341 points (5 spec points each: 0.500-0.5008); >= 8.1 mm clear void behind every skin point.
  - A9: pupils Ø7.992-7.997; 2.00 mm black behind the centre; no yellow inside.
  - A10: all parts manifold with 0 crossing triangle pairs. Shells 3/1/6/1/2. Sum of volumes = master (0.1 mm3). Boundary coincidence tested on 9,965 faces: max gap 0.011 mm, p99 0.00001.
  - A11: mouth line 1.600 (16 sections). Inlay depth median 1.000, 100% within 1.0±0.1 away from a 0.2 mm rim band. Ear tip radius 8.73. Min feature (combined solid, outside windows) 1.984. Stem clearance 3.36. Teeth 6.9x4.6 / 8.2x4.35.
  - A12: head 83.9, pumpkin 86.43, arm span 111.9, eyes x ±17.000, ear tips 1.47/2.15 mm from the concept. Level-view overlay IoU 0.929.
  - A13: all interior ceilings <= 60 deg except the Ø20 head bridge, the Ø30 pumpkin bridge (short span 23.1) and crests <= 7.3 mm wide.
  - A14: tile skins 0.40/0.60/0.80/1.00 from the STL files (both variants).
- Exported: 5 part STLs + combined + 3MF (5 named parts under one assembly). All read back from disk with an independent numpy reader: 0 non-manifold, 0 orientation errors, bodies 3/1/6/1/2/1, volumes match.
- Next: renders and cross-sections.

## Milestone 6: renders and cross-sections (v14)
- All images are Workbench renders through an orthographic camera (`blender/render_figure.py`), saved in `renders/`. I looked at each one.
  - Views: front, three-quarter, back, both sides, top, underside, a colour preview in the spec colours, and two pumpkin close-ups.
  - Cross-sections, each with a cap on the cut face:
    - x=0 (full side, neck + head roof + stem, and the puck pocket with the REF puck, ring and Ø5 cable in place);
    - y=15 (neck opening and the head-roof cone);
    - x=17 (cat eye with pupil plug, pumpkin eye, full);
    - z=115 (cat eyes in plan, plus a close-up of the 0.5 skin and the full-thickness pupil);
    - z=68 (pumpkin eyes);
    - z=44 (pumpkin mouth).
- Seen in the images and not changed:
  - The ribs pucker slightly where they meet the stem.
  - There are small dimples at the pumpkin's bottom band where the skirt meets the plinth fillet; the feet mostly hide them.
  - Window pocket edges show a 0.2 mm sawtooth from the fine grid, which is below print resolution.
- The section objects were deleted after rendering; `render_figure.section_set()` rebuilds them. I checked the parts in the saved file against the STLs: the triangle counts and volumes match exactly.
- Saved `blender/halloween-cat.blend` + `versions/halloween-cat_v14_renders-sections.blend`.
- Re-probed the orange wall with 12,000 samples; the result is a spec miss.
  - Min 2.08 at 3.5-4 mm from a window edge (74% of samples there are below 2.8) and 2.49 at 4-5 mm (18% below). From 5 mm out it is >= 2.88.
  - 3.0% of the orange surface outside the 3.5 mm flank band is below 2.8.
  - Cause: the 45 deg flanks are measured against Y, and the pumpkin surface leans away from Y around the face. Left as is and reported; a fix would tilt those flanks relative to the surface (up to the allowed 60 deg).
- Pumpkin windows rib-free: the rib factor is exactly 0 at all 58,973 pumpkin-window yellow vertices, and the ribs start 4 mm outside the window box.

## v2 build (2026-09-25): new file `blender/halloween-cat-v2.blend`, versions v15+
Scope: surface-relative window flanks (orange >= 2.8 outside the flank band), spec v1.2 flush pupils (no plug), smoother pumpkin, lighter meshes (tiling kept exact), head roof bridge, Bambu 3MF + OBJ exports. The v1 deliverables are untouched. The v1 scripts are preserved in `blender/v1_scripts/`. v2 outputs go under `stl/v2/`, `3mf/v2/`, `obj/v2/` and `renders/v2/`.

### Milestone 7: v2 envelope, chamber, base, windows, parts (v15-v17)
- Heavy steps run from a Blender app timer (`blender/bgrun.py`) and write their status to a file, so no MCP call stays open.
- Pumpkin:
  - Grooves are softer (power 4, was 6) and fade out smoothly (C1) toward the stem (horizontal radius 17 to 30) and below z 27 to 37.
  - Each 45 deg skirt now gets a light blur (sigma about 0.6 mm) in z 14..38. The skirt recursion picks whole grid layers and had left ripples on the pumpkin underside.
  - Preview renders show no puckering at the stem and no dimples along the low rim. The tiny 0.5 mm grid aliasing at the deck fillet line is unchanged and far below print resolution.
- Envelope, 783k -> 180k tris (quadric decimation):
  - volume change -0.003%;
  - two-sided max deviation 0.0098 mm;
  - 0 crossings;
  - 44 chamfer vertices that the decimation moved 1.6 um below z 0 were snapped to z 0.
- D_out was recomputed from the decimated mesh, so walls and skins refer to the final surface.
- Chamber, 437k -> 60k tris: volume change -0.008%, max deviation 0.024 mm. Head roof bridge is Ø18.8 at z 134.61 (HEAD_ROOF_R 9.4).
- M0 = envelope + reversed chamber (no boolean; 0 overlapping triangle pairs).
- M1 = M0 - stage-1 base void. Identity with the printed coupon:
  - volume inside r 44 is 49,302.5928 mm3 for both;
  - every stage-1 probe is identical to v1 (pocket 61.2, aperture 53.998-54.0, tabs 0.900 engagement at 60/180/300, slots 2.2, tunnel 7.0 x 10.0).
- Windows in surface-normal coordinates:
  - The flank angle phi is chosen per outline point: <= 40 deg, with pocket ceilings <= 55 deg preferred and <= 60 deg hard.
  - Result: cat eyes phi 2.7-40, ceilings <= 59.9. Pumpkin eyes phi 19.5-40, <= 60.0. Mouth phi 40, <= 54.6.
  - Pumpkin nose apex: only 1.5 mm of outline cannot get below 60 (67.9 deg). It is a short bridge.
- Spec v1.2 pupils: the pocket behind the whole Ø17.5 eye disc is cut as one; the pupil is black skin in the same skin plane. The optional backing boss is OFF (PUPIL_BOSS_T = 0).
- Chamber depth along the normal behind every window column: cat 1.995-2.014, pumpkin 2.961-3.003.
- Skin before and after decimating the cutters: 0.4995-0.5036 mm (4,926 points).
- A split between approximate and exact foot points left hairline cracks (0.01 mm) in the zone walls. Every evaluated voxel now uses the exact point-to-mesh foot point.
- Parts, all by EXACT booleans from M2 and the decimated zones:
  - black 250,442 tris / 3 shells; orange 121,028 / 1; yellow 56,408 / 6; green 4,792 / 1; pink 5,318 / 2.
  - Total 437,988 tris (v1: 1,636,152).
  - The sum of the part volumes equals M2 (324,589.6 mm3).
- Clean-up:
  - 3 micro-fold pairs in black (paw crease, both eye tops) were relaxed, max move 0.127 mm. The 15 vertices shared with a neighbouring part moved together, so the parts still tile.
  - Zero-area slivers were removed by merging vertices < 20 um apart.
  - All parts are 0 non-manifold / 0 boundary / 0 crossing.
- Tiling:
  - The union of the parts is closed (0 open edges) with volume equal to the sum.
  - 22 sub-0.2 mm spots where the two parts' seam meshes do not conform (4-way edges in the union only, no gap).
- Saved v17.

### Milestone 8: v2 verified, rendered, exported (v18)
- A1/A2:
  - bbox ±60.0004 x ±60.0004 x 0..150.0087; nothing below z 0;
  - base Ø 119.997-120.001 (72 probes); deck z 15.994-15.999.
- A3/A5/A4: all stage-1 probes identical on the black part. The volume inside r 44 equals the coupon (49,302.5928). The puck touches only the 3 tabs; the ring and cables are clear.
- A6:
  - one void, 504.4 cm3, all reached from the plenum;
  - neck 1464.5 mm2 (53.5 x 36.5); head-torso link 1179-1288 mm2;
  - plenum line of sight: pumpkin 2132 (53.5 x 49), torso 1984 (53.5 x 45).
- A7:
  - orange, 27,000 samples, min per band: 3.5-4 mm 2.883; 4-5 mm 2.962; 5-6 mm 2.965; > 6 mm 2.848. Nothing below 2.8 outside 3.5 mm.
  - Inside the flank band: 0-1 0.495, 1-2 1.02, 2-2.5 1.78, 2.5-3 2.15, 3-3.5 2.51.
  - black (pupils excluded) >= 1.974 outside 3.5 mm.
- A8: 6 yellow shells.
  - Skin: 0.5000-0.5012 at the 5 spec points of every window; 0.4993-0.5041 at 4,341 points.
  - Along the inward normal there is >= 56.9 mm of clear void behind every skin point. Along +Y, 92 points near the steep eye tops look into wall within 2 mm; this follows from the normal-based flank.
  - Pumpkin windows are rib-free (rib factor 0 at 17,683 vertices).
- A9 (spec v1.2):
  - pupils Ø 7.989-7.996; skin 0.5000-0.5016 at 9 points each;
  - flush (<= 9e-6 mm from the envelope); nothing behind;
  - 0 non-black hits inside r 3.85; the ring next to the pupil is 0.5001-0.5005.
- A10: all parts manifold with 0 crossing triangles; shells 3/1/6/1/2; sum of volumes = master; interface gap p99 1e-5 mm; union of the parts closed.
- A11: mouth line 1.600; inlay depth 0.955-1.004 inside the 0.2 mm rim (100% within 1.0 ± 0.1); ear tips R 8.73; combined minimum feature 1.986; stem clearance 3.36; teeth 6.9 x 4.6 and 8.2 x 4.35.
- A12: head 83.9, pumpkin 86.3, arm span 111.9, eyes ±17.000 / z 115 / OD 17.50; ear tips 1.07 and 1.75 mm from the concept; IoU 0.929 level and 0.874 at the 13 deg view.
- A13:
  - Pumpkin bridge 554 mm2, span 22.9 (limit 30); head bridge 19.0 x 19.0 (limit 20).
  - Crests behind the pumpkin-eye tops have a short span of 5.1; the nose-apex pocket ceiling is 3.8 x 3.2 (79 deg). Every other > 60 deg cluster is <= 2.6 mm2.
- A14: tile skins 0.40 / 0.60 / 0.80 / 1.00; bed fit 120 x 120 x 150.
- Renders in `renders/v2/` (views, close-ups, sections at x0, y15, x17, z115, z68, z44, and the A12 overlays). I looked at each. The x17 and z115 sections show the pupil as a thin skin with no plug behind it. Parts are smooth-shaded for renders only.
- Exports: STL x 6, core 3MF, Bambu 3MF, OBJ x 2 + MTL.
  - Read back independently: all part meshes 0 non-manifold, 0 degenerate, 0 orientation errors.
  - The triangles of every part are bit-identical in STL, core 3MF, Bambu 3MF and the 5-part OBJ.
  - The painted single-mesh OBJ is closed but has 22 non-manifold edges.
- The Bambu 3MF was NOT opened in Bambu Studio. The user's Bambu Studio was running, and a command-line test could have loaded the file into their session.
- Saved v18.
