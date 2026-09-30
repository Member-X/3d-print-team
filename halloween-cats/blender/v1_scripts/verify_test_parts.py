"""Numeric verification + STL export/read-back for the stage-1 test parts.
All probes run in each object's LOCAL (design) coordinates, i.e. the spec frame.

    import sys, importlib
    sys.path.insert(0, r"H:/ClaudeStuff/3d-print-team/halloween-cats/blender")
    import verify_test_parts as V; importlib.reload(V)
"""
import bpy
import bmesh
import math
import struct
import sys
import importlib
from collections import defaultdict
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HERE = r"H:\ClaudeStuff\3d-print-team\halloween-cats\blender"
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import params as P  # noqa: E402
import build_test_parts as B  # noqa: E402
importlib.reload(P)
importlib.reload(B)


def r3(v, n=3):
    return round(float(v), n)


# ------------------------------------------------------------------ mesh-level
def mesh_report(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    nonman = sum(1 for e in bm.edges if not e.is_manifold)
    bound = sum(1 for e in bm.edges if e.is_boundary)
    wire = sum(1 for e in bm.edges if e.is_wire)
    loose = sum(1 for v in bm.verts if not v.link_faces)
    degenerate = sum(1 for f in bm.faces if f.calc_area() < 1e-8)
    vol = bm.calc_volume(signed=True)
    seen, comps = set(), 0
    for f in bm.faces:
        if f.index in seen:
            continue
        comps += 1
        stack = [f]
        seen.add(f.index)
        while stack:
            ff = stack.pop()
            for e in ff.edges:
                for g in e.link_faces:
                    if g.index not in seen:
                        seen.add(g.index)
                        stack.append(g)
    co = [v.co for v in bm.verts]
    bbox = [min(c.x for c in co), max(c.x for c in co), min(c.y for c in co),
            max(c.y for c in co), min(c.z for c in co), max(c.z for c in co)]
    # self intersection, 3D-Print-Toolbox method (n-gon faces, epsilon 1e-5)
    tree = BVHTree.FromBMesh(bm, epsilon=0.00001)
    selfx = len(tree.overlap(tree))
    # near-duplicate vertices (distinct verts closer than 1e-3 mm)
    from mathutils.kdtree import KDTree
    kd = KDTree(len(bm.verts))
    for v in bm.verts:
        kd.insert(v.co, v.index)
    kd.balance()
    near = 0
    for v in bm.verts:
        for (_, i, d) in kd.find_range(v.co, 1e-3):
            if i > v.index:
                near += 1
    bmt = bm.copy()
    bmesh.ops.triangulate(bmt, faces=bmt.faces[:])
    ntri = len(bmt.faces)
    min_tri_area = min(f.calc_area() for f in bmt.faces)
    parity = ray_parity(BVHTree.FromBMesh(bmt), bbox)
    bmt.free()
    bm.free()
    return {"verts": len(co), "faces": len(ob.data.polygons), "tris": ntri,
            "nonmanifold_edges": nonman, "boundary_edges": bound, "wire_edges": wire,
            "loose_verts": loose, "degenerate_faces": degenerate,
            "self_intersect_pairs_toolbox": selfx, "near_duplicate_vert_pairs_1um": near,
            "min_triangle_area_mm2": min_tri_area, "ray_parity": parity,
            "bodies": comps, "volume_mm3": r3(vol, 2),
            "bbox_local": [r3(b, 4) for b in bbox]}


def ray_parity(tree, bbox, n=20000, seed=11):
    """Random rays through the bbox: on a closed, non-self-intersecting surface
    every ray's hits alternate enter/exit.  Returns failures (grazing an
    edge exactly can cause a rare false failure)."""
    import random
    random.seed(seed)
    cx, cy, cz = (bbox[0] + bbox[1]) / 2, (bbox[2] + bbox[3]) / 2, (bbox[4] + bbox[5]) / 2
    ex, ey, ez = (bbox[1] - bbox[0]) / 2 + 2, (bbox[3] - bbox[2]) / 2 + 2, (bbox[5] - bbox[4]) / 2 + 2
    bad, hitting, hits, fails = 0, 0, 0, []
    for _ in range(n):
        o = Vector((cx + random.uniform(-ex, ex), cy + random.uniform(-ey, ey), cz + random.uniform(-ez, ez)))
        d = Vector((random.gauss(0, 1), random.gauss(0, 1), random.gauss(0, 1))).normalized()
        o = o - d * 300
        seq, oo, left = [], o.copy(), 800.0
        for _k in range(100):
            loc, nrm, idx, dist = tree.ray_cast(oo, d, left)
            if loc is None:
                break
            seq.append((nrm.dot(d), loc.copy()))
            left -= dist + 1e-3
            oo = loc + d * 1e-3
        if seq:
            hitting += 1
            hits += len(seq)
        ok = len(seq) % 2 == 0 and all((s < 0) if j % 2 == 0 else (s > 0) for j, (s, _l) in enumerate(seq))
        if not ok:
            bad += 1
            if len(fails) < 3:
                fails.append([[r3(x, 3) for x in l] for s, l in seq])
    return {"rays": n, "rays_hitting": hitting, "hits": hits, "failures": bad, "fail_examples": fails}


def tree_of(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    t = BVHTree.FromBMesh(bm)
    bm.free()
    return t


def ray_all(tree, origin, direction, maxd=500.0):
    o = Vector(origin)
    d = Vector(direction).normalized()
    out = []
    travelled = 0.0
    for _ in range(50):
        loc, nrm, idx, dist = tree.ray_cast(o, d, maxd - travelled)
        if loc is None:
            break
        travelled += dist
        out.append((loc.copy(), nrm.copy()))
        o = loc + d * 1e-4
        travelled += 1e-4
    return out


def radial_dir(phi):
    a = math.radians(phi)
    return Vector((math.sin(a), math.cos(a), 0.0))


def first_radial_hit(tree, phi, z, r0=0.0):
    d = radial_dir(phi)
    hits = ray_all(tree, Vector((0, 0, z)) + d * r0, d)
    return [r3(Vector((h[0].x, h[0].y, 0)).length, 4) for h in hits]


# ------------------------------------------------------------------ coupon
def coupon_checks(ob, flex=True):
    engage = P.TAB_ENGAGE if flex else P.TAB_ENGAGE_FALLBACK
    t = tree_of(ob)
    res = {}
    arm_spans = []
    if flex:
        for phi in P.TAB_ANGLES:
            g = P.arm_angles(phi)
            arm_spans.append((g["root"], g["gap_end"]))

    def in_arm(phi):
        for lo, hi in arm_spans:
            if lo - 1 <= phi % 360 <= hi + 1 or lo - 1 <= phi % 360 + 360 <= hi + 1:
                return True
        return False
    # pocket radius at mid height, 72 directions avoiding tunnel and arm zones
    rs = []
    for k in range(72):
        phi = k * 5.0 + 2.5
        if abs(((phi + 180) % 360) - 180) < 10 or in_arm(phi):
            continue
        h = first_radial_hit(t, phi, 6.0)
        rs.append(h[0])
    res["pocket_D_at_z6_min_max"] = [r3(2 * min(rs)), r3(2 * max(rs))]
    res["pocket_D_probe_count"] = len(rs)
    # pocket just above the entry chamfer and just below the top chamfer
    res["pocket_R_at_z0.3_(entry chamfer)"] = first_radial_hit(t, 92.5, 0.3)[0]
    res["pocket_R_at_z10.6_(top chamfer)"] = first_radial_hit(t, 92.5, 10.6)[0]
    # shelf underside and deck, vertical ray at r = 28.5 (between aperture and wall)
    hz = ray_all(t, Vector((28.5 * math.sin(math.radians(92.5)), 28.5 * math.cos(math.radians(92.5)), 5.0)),
                 (0, 0, 1))
    res["shelf_underside_z_at_r28.5"] = r3(hz[0][0].z, 4) if hz else None
    res["top_surface_z_at_r28.5"] = r3(hz[1][0].z, 4) if len(hz) > 1 else None
    # aperture / plenum bore
    ap = [first_radial_hit(t, phi, 12.0)[0] for phi in (2.5, 92.5, 182.5, 272.5, 45, 135, 225, 315)]
    pl = [first_radial_hit(t, phi, 14.5)[0] for phi in (2.5, 92.5, 182.5, 272.5, 45, 135, 225, 315)]
    res["aperture_D_at_z12_min_max"] = [r3(2 * min(ap)), r3(2 * max(ap))]
    res["plenum_D_at_z14.5_min_max"] = [r3(2 * min(pl)), r3(2 * max(pl))]
    # through-bore open: vertical ray up the axis hits nothing
    res["axis_clear_bottom_to_top"] = len(ray_all(t, (0, 0, -5), (0, 0, 1))) == 0
    # outer
    res["outer_D_at_z8"] = r3(2 * first_radial_hit(t, 92.5, 8.0, r0=40)[0])
    # tabs
    tabs = []
    for phi in P.TAB_ANGLES:
        rec = {"phi_nominal": phi}
        rec["tip_r_at_z2.0"] = first_radial_hit(t, phi, 2.0)[0]
        rec["engage_over_puck"] = r3(P.PUCK_D / 2 - rec["tip_r_at_z2.0"])
        rec["ramp_r_at_z0.5"] = first_radial_hit(t, phi, 0.5)[0]
        rec["ramp_r_at_z1.0"] = first_radial_hit(t, phi, 1.0)[0]
        p = Vector((0, 0, 0)) + radial_dir(phi) * 29.6
        down = ray_all(t, Vector((p.x, p.y, 6.0)), (0, 0, -1))
        rec["tab_top_z"] = r3(down[0][0].z, 4) if down else None
        # chord: sweep angles at z = 2.0, find where the hit radius < 29.5
        inside = []
        for i in range(-200, 201):
            a = phi + i * 0.05
            h = first_radial_hit(t, a, 2.0)
            if h and h[0] < P.POCKET_R - 0.3:
                inside.append(a)
        if inside:
            lo, hi = min(inside), max(inside)
            rt = rec["tip_r_at_z2.0"]
            rec["tab_angle_span_deg"] = [r3(lo, 2), r3(hi, 2)]
            rec["tab_center_deg"] = r3((lo + hi) / 2, 2)
            rec["tab_chord_at_tip_mm"] = r3(2 * rt * math.sin(math.radians((hi - lo) / 2)), 2)
        tabs.append(rec)
    res["tabs"] = tabs
    if flex:
        arms = []
        for phi in P.TAB_ANGLES:
            g = P.arm_angles(phi)
            mid = (g["root"] + g["tab"][0]) / 2
            hr = first_radial_hit(t, mid, 2.0)
            rec = {"phi_probe": r3(mid, 2), "radial_hits_z2": hr[:4]}
            if len(hr) >= 3:
                rec["arm_T"] = r3(hr[1] - hr[0])
                rec["slot_W"] = r3(hr[2] - hr[1])
            rm = P.ARM_R_MID
            pv = radial_dir(mid) * rm
            up = ray_all(t, Vector((pv.x, pv.y, -2.0)), (0, 0, 1))
            rec["arm_z_bottom_top_ceiling"] = [r3(h[0].z) for h in up[:3]]
            ps = radial_dir(mid) * (P.SLOT_R_OUT - 0.1)
            up2 = ray_all(t, Vector((ps.x, ps.y, -2.0)), (0, 0, 1))
            rec["slot_open_to_bed_first_hit_z_at_r_slotout-0.1"] = r3(up2[0][0].z) if up2 else None
            # free-end gap: sweep past the free end at r = 31.4, z = 2
            gap = []
            for i in range(0, 120):
                a = g["free"] - 1.0 + i * 0.05
                pp = radial_dir(a) * rm
                hh = ray_all(t, Vector((pp.x, pp.y, -2.0)), (0, 0, 1))
                if hh and hh[0][0].z > 3.0:
                    gap.append(a)
            if gap:
                rec["end_gap_deg"] = [r3(min(gap), 2), r3(max(gap), 2)]
                rec["end_gap_mm_at_r31.4"] = r3(math.radians(max(gap) - min(gap) + 0.05) * rm, 2)
            arms.append(rec)
        res["arms"] = arms
    # tunnel: probes at y = 38 (inside the ring, between pocket wall and outer)
    y = 38.0
    wx = ray_all(t, (0, y, 5.0), (1, 0, 0))
    wxm = ray_all(t, (0, y, 5.0), (-1, 0, 0))
    res["tunnel_width_at_y38_z5"] = r3(wx[0][0].x - wxm[0][0].x) if wx and wxm else None
    hz = ray_all(t, (0, y, -2.0), (0, 0, 1))
    res["tunnel_roof_z_at_x0_y38"] = r3(hz[0][0].z) if hz else None
    res["tunnel_roof_thickness"] = r3(hz[1][0].z - hz[0][0].z) if len(hz) > 1 else None
    # side wall height (z at which the side becomes the chamfer): ray up at x = +-3.4
    hs = ray_all(t, (3.45, y, -2.0), (0, 0, 1))
    res["tunnel_z_at_x3.45"] = r3(hs[0][0].z) if hs else None
    # reaches the edge: rays along +Y from the pocket centre across the tunnel section
    blocked = []
    for x in (-3.3, -2.0, 0.0, 2.0, 3.3):
        for z in (0.2, 2.0, 5.0, 7.9):
            if ray_all(t, (x, 0.0, z), (0, 1, 0)):
                blocked.append((x, z))
    for z in (9.0, 9.9):
        for x in (-1.4, 0.0, 1.4):
            if ray_all(t, (x, 0.0, z), (0, 1, 0)):
                blocked.append((x, z))
    res["tunnel_clear_rays_pocket_to_edge_blocked"] = blocked
    # bottom flat
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    zmin = min(v.co.z for v in bm.verts)
    bottom = [f for f in bm.faces if all(abs(v.co.z) < 1e-6 for v in f.verts)]
    res["z_min"] = r3(zmin, 6)
    res["bottom_faces_all_normal_down"] = all(f.normal.z < -0.999 for f in bottom)
    res["bottom_contact_area_mm2"] = r3(sum(f.calc_area() for f in bottom), 1)
    res["verts_below_z0"] = sum(1 for v in bm.verts if v.co.z < -1e-6)
    bm.free()
    return res


def bottom_area_expected(flex=True):
    """Hand estimate of the flat Z0 contact area of the coupon."""
    R = P.COUPON_D / 2 - P.COUPON_BOTTOM_CHAMFER          # 44.4
    ri = P.POCKET_R + P.POCKET_ENTRY_CHAMFER              # 31.2 mouth
    area = math.pi * (R * R - ri * ri)
    # tunnel groove across the ring (w x radial length)
    w = P.TUNNEL_W
    L = math.sqrt(R * R - (w / 2) ** 2) - math.sqrt(ri * ri - (w / 2) ** 2)
    area -= w * L
    engage = P.TAB_ENGAGE if flex else P.TAB_ENGAGE_FALLBACK
    ht = math.radians(2 * B.tab_half_deg(engage))
    rp = P.POCKET_R
    # tabs remove the entry chamfer over their span -> ring r 30.6..31.2 is solid
    area += len(P.TAB_ANGLES) * 0.5 * ht * (ri * ri - rp * rp)
    if flex:
        for phi in P.TAB_ANGLES:
            g = P.arm_angles(phi)
            span_slot = math.radians(g["free"] - g["root"])
            area -= 0.5 * span_slot * (P.SLOT_R_OUT ** 2 - P.ARM_R_OUT ** 2)
            span_gap = math.radians(g["gap_end"] - g["free"])
            area -= 0.5 * span_gap * (P.SLOT_R_OUT ** 2 - ri * ri)
    return area


# ------------------------------------------------------------------ dummies
def _dup(ob, name):
    d = ob.copy()
    d.data = ob.data.copy()
    d.name = name
    B.coll(B.COLL_WORK).objects.link(d)
    return d


def intersect_stats(a, b, tag="_isect"):
    """EXACT intersection of copies of a and b (world space). Returns volume
    and number of separate pieces."""
    tmp = _dup(a, tag)
    tmp.parent = None
    tmp.matrix_world = a.matrix_world.copy()
    B.apply_boolean(tmp, b, 'INTERSECT')
    bm = bmesh.new()
    bm.from_mesh(tmp.data)
    vol = bm.calc_volume(signed=True) if bm.faces else 0.0
    seen, comps, cents = set(), 0, []
    for f in bm.faces:
        if f.index in seen:
            continue
        comps += 1
        stack = [f]
        seen.add(f.index)
        pts = []
        while stack:
            ff = stack.pop()
            pts.append(ff.calc_center_median())
            for e in ff.edges:
                for g in e.link_faces:
                    if g.index not in seen:
                        seen.add(g.index)
                        stack.append(g)
        c = sum(pts, Vector()) / len(pts)
        cents.append([r3(math.degrees(math.atan2(c.x, c.y)) % 360, 1), r3(c.z, 2)])
    nf = len(bm.faces)
    bm.free()
    B.remove_obj(tmp.name)
    return {"volume_mm3": r3(vol, 4), "pieces": comps, "faces": nf, "piece_phi_z": cents}


def moved_copy(ob, name, dz=0.0, dy=0.0, scale_r=None):
    d = _dup(ob, name)
    d.parent = None
    d.matrix_world = ob.matrix_world.copy()
    if scale_r:
        d.scale = (scale_r, scale_r, 1.0)
    d.location = (ob.location.x, ob.location.y + dy, ob.location.z + dz)
    return d


def cable_clearance_analytic(zc, d):
    r = d / 2
    w, h, c = P.TUNNEL_W, P.TUNNEL_H, P.TUNNEL_CHAMFER
    roof = h - (zc + r)
    side = w / 2 - r
    cham = abs((w / 2 + h - c) - zc) / math.sqrt(2) - r   # line x + z = w/2 + h - c
    floor = zc - r                                          # cable bottom above Z0
    return {"roof": r3(roof), "side": r3(side), "chamfer": r3(cham), "cable_bottom_z": r3(floor)}


def ref_checks(coupon):
    """Run with the coupon at its design position (location 0)."""
    puck = bpy.data.objects["REF_puck"]
    ring = bpy.data.objects["REF_puck_ring"]
    c4 = bpy.data.objects["REF_cable_4"]
    c5 = bpy.data.objects["REF_cable_5"]
    out = {}
    out["puck_nominal"] = intersect_stats(coupon, puck)
    low = moved_copy(puck, "_puck_low", dz=-0.05)
    out["puck_lowered_0.05_contact_test"] = intersect_stats(coupon, low)
    B.remove_obj(low.name)
    # lateral clearance: grow the puck radius until contact
    for rr in (30.3, 30.45, 30.55):
        g = moved_copy(puck, "_puck_grow", scale_r=rr / 30.0)
        g.location.z = puck.location.z
        # scale about the object origin (0,0,0) keeps it centred
        s = intersect_stats(coupon, g)
        # exclude the tab tops by lifting 0.01
        B.remove_obj(g.name)
        out[f"puck_radius_{rr}"] = s
    out["ring_nominal"] = intersect_stats(coupon, ring)
    for zc in (P.CABLE_EXIT_Z_MIN, 5.5, P.CABLE_EXIT_Z_NOM, 7.0, 7.4, P.CABLE_EXIT_Z_MAX):
        for ob, d in ((c4, P.CABLE_D), (c5, P.CABLE_D_CHECK)):
            m = moved_copy(ob, "_cable", dz=zc - P.CABLE_EXIT_Z_NOM)
            s = intersect_stats(coupon, m)
            B.remove_obj(m.name)
            out[f"{ob.name}_zc{zc}"] = {"isect_volume": s["volume_mm3"], "pieces": s["pieces"],
                                        "analytic_margin": cable_clearance_analytic(zc, d)}
    return out


# ------------------------------------------------------------------ tile
def tile_checks(ob, dots="raised"):
    t = tree_of(ob)
    res = {"skins": []}
    zc = P.TILE_POCKET_ZC
    for x, s in zip(P.TILE_POCKET_X, P.TILE_SKINS):
        pts = [(0, 0), (-4, 0), (4, 0), (0, -9), (0, 9), (-5.3, -10.8), (5.3, 10.8)]
        meas = []
        for dx, dz in pts:
            h = ray_all(t, (x + dx, -5.0, zc + dz), (0, 1, 0))
            if len(h) >= 2:
                meas.append(r3(h[1][0].y - h[0][0].y, 4))
            else:
                meas.append(None)
        # pocket floor extent: sweep x at the skin mid-depth plane
        yprobe = s / 2 + 0.0
        # rays along Z inside the skin-to-back region just behind the skin
        yb = s + 0.02
        up = ray_all(t, (x, yb, zc), (0, 0, 1))
        dn = ray_all(t, (x, yb, zc), (0, 0, -1))
        rt = ray_all(t, (x, yb, zc), (1, 0, 0))
        lf = ray_all(t, (x, yb, zc), (-1, 0, 0))
        fl = {}
        if up and dn and rt and lf:
            fl = {"floor_W": r3(rt[0][0].x - lf[0][0].x), "floor_H": r3(up[0][0].z - dn[0][0].z)}
        # opening at the back face
        yb2 = P.TILE_T - 0.02
        up2 = ray_all(t, (x, yb2, zc), (0, 0, 1))
        dn2 = ray_all(t, (x, yb2, zc), (0, 0, -1))
        if up2 and dn2:
            fl["back_opening_H"] = r3(up2[0][0].z - dn2[0][0].z)
            fl["flank_deg_from_axis"] = r3(math.degrees(math.atan(
                ((up2[0][0].z - dn2[0][0].z) - fl.get("floor_H", 0)) / 2 / (yb2 - yb))), 2)
        res["skins"].append({"x": x, "target": s, "measured_at_7_points": meas,
                             "min": min(m for m in meas if m is not None),
                             "max": max(m for m in meas if m is not None), **fl})
    # dots: count faces whose plane is the dot face
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    yface = -P.TILE_DOT_H if dots == "raised" else P.TILE_DOT_H
    dotf = [f for f in bm.faces if all(abs(v.co.y - yface) < 1e-5 for v in f.verts)
            and f.normal.y < -0.99]
    groups = defaultdict(list)
    for f in dotf:
        c = f.calc_center_median()
        k = min(P.TILE_POCKET_X, key=lambda px: abs(px - c.x))
        groups[k].append((r3(c.x, 2), r3(c.z, 2), r3(2 * math.sqrt(f.calc_area() / math.pi), 3)))
    res["dots_per_pocket"] = {str(k): len(v) for k, v in sorted(groups.items())}
    res["dot_diameters"] = sorted({d[2] for v in groups.values() for d in v})
    bm.free()
    return res


# ------------------------------------------------------------------ STL
def write_stl(ob, path, center_xy=False):
    """Binary STL in mm from the object's LOCAL mesh (no modifiers on it).
    center_xy: translate so the bbox is centred on X/Y; z-min moved to 0."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    zs = [v.co.z for v in bm.verts]
    off = Vector((0, 0, -min(zs)))
    if center_xy:
        off.x = -(min(xs) + max(xs)) / 2
        off.y = -(min(ys) + max(ys)) / 2
    with open(path, "wb") as f:
        hdr = ("%s | mm | halloween-cats stage1 | spec v%s" % (ob.name, P.SPEC_VERSION)).encode()
        f.write(hdr[:80].ljust(80, b" "))
        f.write(struct.pack("<I", len(bm.faces)))
        for fc in bm.faces:
            n = fc.normal
            f.write(struct.pack("<3f", n.x, n.y, n.z))
            for v in fc.verts:
                c = v.co + off
                f.write(struct.pack("<3f", c.x, c.y, c.z))
            f.write(b"\x00\x00")
    n = len(bm.faces)
    bm.free()
    return {"path": path, "tris": n, "offset": [r3(o, 4) for o in off]}


def read_stl_check(path):
    """Independent check of a binary STL file (no Blender mesh data used)."""
    data = open(path, "rb").read()
    n = struct.unpack("<I", data[80:84])[0]
    ok_size = len(data) == 84 + 50 * n
    vid = {}
    faces = []
    for i in range(n):
        o = 84 + 50 * i + 12
        v = struct.unpack("<9f", data[o:o + 36])
        tri = (v[0:3], v[3:6], v[6:9])
        faces.append(tuple(vid.setdefault(p, len(vid)) for p in tri))
    pts = list(vid.keys())
    und = defaultdict(int)
    dire = defaultdict(int)
    degenerate = 0
    for a, b, c in faces:
        if a == b or b == c or a == c:
            degenerate += 1
        for u, w in ((a, b), (b, c), (c, a)):
            und[(min(u, w), max(u, w))] += 1
            dire[(u, w)] += 1
    nonman = sum(1 for k, c in und.items() if c != 2)
    orient_bad = sum(1 for (u, w), c in dire.items() if c != 1 or dire.get((w, u), 0) != 1)
    parent = list(range(len(pts)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b, c in faces:
        for u, w in ((a, b), (b, c)):
            ru, rw = find(u), find(w)
            if ru != rw:
                parent[ru] = rw
    bodies = len({find(a) for f in faces for a in f})
    vol = 0.0
    for a, b, c in faces:
        p, q, r = Vector(pts[a]), Vector(pts[b]), Vector(pts[c])
        vol += p.dot(q.cross(r)) / 6.0
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    zs = [p[2] for p in pts]
    zmin = min(zs)
    bottom_tris = sum(1 for f in faces if all(abs(pts[i][2] - zmin) < 1e-6 for i in f))
    return {"file_ok": ok_size, "triangles": n, "unique_verts": len(pts),
            "nonmanifold_edges": nonman, "orientation_errors": orient_bad,
            "degenerate_tris": degenerate, "bodies": bodies, "volume_mm3": r3(vol, 2),
            "bbox": [r3(min(xs), 4), r3(max(xs), 4), r3(min(ys), 4), r3(max(ys), 4),
                     r3(zmin, 4), r3(max(zs), 4)],
            "size_xyz": [r3(max(xs) - min(xs), 3), r3(max(ys) - min(ys), 3), r3(max(zs) - zmin, 3)],
            "bottom_tris_at_zmin": bottom_tris}
