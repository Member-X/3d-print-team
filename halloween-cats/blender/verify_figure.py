"""Stage-2 verification helpers (A1-A14).  Run inside Blender.

    import verify_figure as VF; importlib.reload(VF)
    VF.base_vs_coupon("M1_base")
"""
import math
import os
import sys
import importlib
import struct
from collections import defaultdict

import bpy
import bmesh
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HERE = r"H:\ClaudeStuff\3d-print-team\halloween-cats\blender"
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import params as P            # noqa: E402
import build_test_parts as B  # noqa: E402
import verify_test_parts as V  # noqa: E402
import figure_shapes as FS    # noqa: E402

STL_DIR = r"H:\ClaudeStuff\3d-print-team\halloween-cats\stl"


def r3(v, n=3):
    return round(float(v), n)


# ------------------------------------------------------------------ STL import (own reader)
def stl_to_obj(path, name, coll_name="WORK_temp"):
    data = open(path, "rb").read()
    n = struct.unpack("<I", data[80:84])[0]
    vid, verts, faces = {}, [], []
    for i in range(n):
        o = 84 + 50 * i + 12
        v = struct.unpack("<9f", data[o:o + 36])
        f = []
        for p in (v[0:3], v[3:6], v[6:9]):
            if p not in vid:
                vid[p] = len(verts)
                verts.append(p)
            f.append(vid[p])
        faces.append(f)
    B.remove_obj(name)
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    B.coll(coll_name).objects.link(ob)
    return ob


def cylinder_obj(name, r, z0, z1, seg=720, coll_name="WORK_temp"):
    bm = B.revolve_bm([(0.0, z0), (r, z0), (r, z1), (0.0, z1)], seg=seg, phase=0.3)
    return B.bm_to_obj(bm, name, B.coll(coll_name))


def volume(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    v = bm.calc_volume(signed=True)
    bm.free()
    return v


def isect_volume(a, b, tag="_iv"):
    s = V.intersect_stats(a, b, tag)
    return s


def base_vs_coupon(fig_name="M1_base"):
    """Exact comparison of the figure's base with the printed coupon inside
    r <= 44, z -1 .. 15.5 (where both are 'solid minus the same void')."""
    fig = bpy.data.objects[fig_name]
    cp = stl_to_obj(os.path.join(STL_DIR, "base-fit-coupon.stl"), "_coupon_stl")
    # the coupon STL was exported centred with z-min at 0 and design coords = file coords
    cyl = cylinder_obj("_cmp_cyl", 44.0, -1.0, 15.5)
    a = V.intersect_stats(fig, cyl, "_iv_fig")
    b = V.intersect_stats(cp, cyl, "_iv_cp")
    # symmetric difference: fig∩cyl minus coupon, and coupon∩cyl minus fig
    t1 = V._dup(fig, "_sd1"); t1.parent = None; t1.matrix_world = fig.matrix_world.copy()
    B.apply_boolean(t1, cyl, 'INTERSECT')
    B.apply_boolean(t1, cp, 'DIFFERENCE')
    d1 = volume(t1)
    t2 = V._dup(cp, "_sd2"); t2.parent = None
    B.apply_boolean(t2, cyl, 'INTERSECT')
    B.apply_boolean(t2, fig, 'DIFFERENCE')
    d2 = volume(t2)
    for n in ("_sd1", "_sd2", "_cmp_cyl", "_coupon_stl"):
        B.remove_obj(n)
    return {"figure_in_cyl_mm3": a["volume_mm3"], "coupon_in_cyl_mm3": b["volume_mm3"],
            "figure_minus_coupon_mm3": r3(d1, 4), "coupon_minus_figure_mm3": r3(d2, 4)}


def coupon_probes(fig_name="M1_base"):
    """The stage-1 coupon probe set, run on the figure (design coords)."""
    ob = bpy.data.objects[fig_name]
    res = V.coupon_checks(ob, flex=True)
    return res


# ================================================================== stage-2 checks
PARTS = ("black", "orange", "yellow", "green", "pink")
_TREES = {}


def tree(name, refresh=False):
    """Triangulated world-space BVH of an object (cached per session)."""
    if refresh or name not in _TREES:
        ob = bpy.data.objects[name]
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        bm.transform(ob.matrix_world)
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
        _TREES[name] = BVHTree.FromBMesh(bm)
        bm.free()
    return _TREES[name]


def first_hit_part(origin, direction, maxd=400.0, parts=PARTS):
    """Nearest hit among the parts along a ray: (part, loc, normal, dist)."""
    best = None
    for p in parts:
        loc, nrm, idx, dist = tree(p).ray_cast(Vector(origin), Vector(direction), maxd)
        if loc is not None and (best is None or dist < best[3]):
            best = (p, loc, nrm, dist)
    return best


def hits_along(tr, origin, direction, maxd=400.0, eps=1e-5):
    o = Vector(origin)
    d = Vector(direction).normalized()
    out = []
    left = maxd
    for _ in range(80):
        loc, nrm, idx, dist = tr.ray_cast(o, d, left)
        if loc is None:
            break
        out.append((loc.copy(), nrm.copy(), dist))
        o = loc + d * eps
        left -= dist + eps
    return out


def bbox_of(name):
    ob = bpy.data.objects[name]
    co = np.empty(len(ob.data.vertices) * 3, np.float64)
    ob.data.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    return co.min(0), co.max(0)


# ---------------------------------------------------------------- A1, A2
def check_A1_A2(master="M2_windows"):
    lo, hi = bbox_of(master)
    res = {"bbox_min": [r3(v, 4) for v in lo], "bbox_max": [r3(v, 4) for v in hi],
           "extent": [r3(v, 3) for v in hi - lo],
           "centre_xy": [r3(0.5 * (lo[0] + hi[0]), 4), r3(0.5 * (lo[1] + hi[1]), 4)]}
    ob = bpy.data.objects[master]
    co = np.empty(len(ob.data.vertices) * 3, np.float64)
    ob.data.vertices.foreach_get("co", co)
    z = co.reshape(-1, 3)[:, 2]
    near = z[z < 0.01]
    res["bottom_verts_z_min_max"] = [float(near.min()), float(near.max())]
    res["verts_below_0"] = int((z < -1e-6).sum())
    t = tree(master)
    ds = []
    for zz in (2.0, 8.0, 14.0):
        for k in range(24):
            a = math.radians(k * 15 + 7.5)
            dvec = Vector((-math.sin(a), -math.cos(a), 0))
            o = Vector((70 * math.sin(a), 70 * math.cos(a), zz))
            h = t.ray_cast(o, dvec, 100.0)
            if h[0] is not None:
                ds.append(Vector((h[0].x, h[0].y, 0)).length)
    res["base_radius_min_max_n"] = [r3(min(ds), 4), r3(max(ds), 4), len(ds)]
    zt = []
    for k in range(24):
        a = math.radians(k * 15)
        o = Vector((58.3 * math.sin(a), 58.3 * math.cos(a), 60.0))
        h = t.ray_cast(o, Vector((0, 0, -1)), 100.0)
        if h[0] is not None and h[0].z < 17.0:
            zt.append(h[0].z)
    res["deck_z_min_max_n"] = [r3(min(zt), 4), r3(max(zt), 4), len(zt)]
    return res


# ---------------------------------------------------------------- A8, A9
def outline_points(name, inset=1.0, n_edge=4):
    """Centre (deepest inside point) + n_edge points `inset` mm inside the
    outline edge (extreme points in 4 diagonal directions)."""
    loops = FS.outlines()[name]
    pts = np.vstack(loops)
    x0, x1, z0, z1 = pts[:, 0].min(), pts[:, 0].max(), pts[:, 1].min(), pts[:, 1].max()
    xs = np.arange(x0, x1, 0.1)
    zs = np.arange(z0, z1, 0.1)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    D = FS.outline_sdf2(name, X, Z)
    i = np.unravel_index(np.argmin(D), D.shape)
    centre = (float(X[i]), float(Z[i]))
    ring = (D < -inset + 0.05) & (D > -inset - 0.05)
    rx, rz = X[ring], Z[ring]
    out = [("centre", centre)]
    cx, cz = centre
    for k in range(n_edge):
        a = 2 * math.pi * k / n_edge + math.pi / 4
        proj = (rx - cx) * math.cos(a) + (rz - cz) * math.sin(a)
        j = int(np.argmax(proj))
        out.append(("edge%d" % k, (float(rx[j]), float(rz[j]))))
    return out


def skin_at(x, z):
    """Skin at front point (x, z): thickness along the local outer normal,
    the first part hit, and the clear (void) distance behind the skin along
    +Y before ANY solid (i.e. nothing but skin in the light path)."""
    fh = first_hit_part((x, -150.0, z), (0, 1, 0))
    if fh is None:
        return None, None, None, None
    p, loc, nrm, dist = fh
    n = nrm.normalized()
    hs = hits_along(tree(p), loc - n * 1e-4, -n, 20.0)
    th = hs[0][2] + 1e-4 if hs else None
    # exit point of the skin along +Y, then the next solid of any part
    hy = hits_along(tree(p), loc + Vector((0, 1e-4, 0)), (0, 1, 0), 20.0)
    if not hy:
        return th, p, None, None
    back = hy[0][0] + Vector((0, 1e-3, 0))
    nxt = first_hit_part(back, (0, 1, 0))
    return th, p, (nxt[3] if nxt else 999.0), (nxt[0] if nxt else None)


def check_A8(dense_step=0.5):
    res = {}
    for w in FS.WINDOWS:
        rec = []
        for tag, (x, z) in outline_points(w, inset=1.0):
            th, p, nxt, nxtp = skin_at(x, z)
            rec.append({"pt": tag, "x": r3(x, 2), "z": r3(z, 2), "part": p,
                        "skin": r3(th, 4) if th else None,
                        "void_behind_mm": r3(nxt, 2) if nxt else None, "next_part": nxtp})
        res[w] = rec
    dense = {}
    for w in FS.WINDOWS:
        pts = np.vstack(FS.outlines()[w])
        xs = np.arange(pts[:, 0].min(), pts[:, 0].max(), dense_step)
        zs = np.arange(pts[:, 1].min(), pts[:, 1].max(), dense_step)
        X, Z = np.meshgrid(xs, zs, indexing="ij")
        D = FS.outline_sdf2(w, X, Z)
        ths, parts_hit, voids = [], set(), []
        for x, z in zip(X[D < -0.3], Z[D < -0.3]):
            th, p, nxt, nxtp = skin_at(float(x), float(z))
            parts_hit.add(p)
            if th:
                ths.append(th)
            if nxt is not None:
                voids.append(nxt)
        ths = np.array(ths)
        voids = np.array(voids)
        dense[w] = {"n": len(ths), "skin_min": r3(ths.min(), 4), "skin_med": r3(np.median(ths), 4),
                    "skin_max": r3(ths.max(), 4), "first_parts": sorted(parts_hit),
                    "clear_behind_skin_min_med": [r3(voids.min(), 2), r3(np.median(voids), 2)]}
    res["dense"] = dense
    return res


def check_A9():
    pup = {}
    for side, sx in (("L", -1), ("R", 1)):
        cx, cz = sx * P.CAT_EYE_X, P.CAT_EYE_Z
        radii = []
        for k in range(16):
            a = 2 * math.pi * k / 16
            lo_, hi_ = 3.0, 5.0
            for _ in range(30):
                m = 0.5 * (lo_ + hi_)
                fh = first_hit_part((cx + m * math.cos(a), -150, cz + m * math.sin(a)), (0, 1, 0))
                if fh and fh[0] == "black":
                    lo_ = m
                else:
                    hi_ = m
            radii.append(0.5 * (lo_ + hi_))
        fh = first_hit_part((cx, -150, cz), (0, 1, 0))
        n = fh[2].normalized()
        hs = hits_along(tree("black"), fh[1] - n * 1e-4, -n, 20.0)
        # plug depth along +Y at the centre (black from the surface to the pocket/chamber)
        hy = hits_along(tree("black"), fh[1] + Vector((0, 1e-4, 0)), (0, 1, 0), 20.0)
        non_black = 0
        for k in range(64):
            a = 2 * math.pi * k / 64
            for rr in (0.0, 1.5, 3.0, 3.85):
                f2 = first_hit_part((cx + rr * math.cos(a), -150, cz + rr * math.sin(a)), (0, 1, 0))
                if f2 and f2[0] != "black":
                    non_black += 1
        pup[side] = {"diameter_min_max": [r3(2 * min(radii), 3), r3(2 * max(radii), 3)],
                     "black_behind_centre_along_normal": r3(hs[0][2], 3) if hs else None,
                     "black_behind_centre_along_Y": r3(hy[0][2], 3) if hy else None,
                     "non_black_hits_inside_r3.85_of_256": non_black}
    return pup


# ---------------------------------------------------------------- inner surface of the master
def inner_faces_tree(master="M2_windows", outer="ENV_outer", tol=0.02):
    """BVH of the master's faces that are NOT on the outer envelope (chamber,
    pockets, base void), plus their centres / normals / areas."""
    if "_inner" in _TREES:
        return _TREES["_inner"]
    to = tree(outer)
    ob = bpy.data.objects[master]
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    verts = [v.co.copy() for v in bm.verts]
    bm.verts.index_update()
    tris, cen, nrm, area = [], [], [], []
    fn = to.find_nearest
    for f in bm.faces:
        c = f.calc_center_median()
        if fn(c)[3] > tol:
            tris.append([v.index for v in f.verts])
            cen.append(c[:])
            nrm.append(f.normal[:])
            area.append(f.calc_area())
    bm.free()
    t = BVHTree.FromPolygons(verts, tris, all_triangles=True)
    _TREES["_inner"] = (t, np.array(cen), np.array(nrm), np.array(area))
    return _TREES["_inner"]


def sample_surface(name, n, seed=3, zmin=-1e9):
    ob = bpy.data.objects[name]
    me = ob.data
    nf = len(me.polygons)
    area = np.empty(nf, np.float64)
    me.polygons.foreach_get("area", area)
    cen = np.empty(nf * 3, np.float64)
    me.polygons.foreach_get("center", cen)
    cen = cen.reshape(-1, 3)
    nrm = np.empty(nf * 3, np.float64)
    me.polygons.foreach_get("normal", nrm)
    nrm = nrm.reshape(-1, 3)
    ok = cen[:, 2] > zmin
    p = area * ok
    rng = np.random.default_rng(seed)
    idx = rng.choice(nf, size=n, replace=True, p=p / p.sum())
    return cen[idx], nrm[idx]


def owner_part(p, parts=PARTS):
    best, bd = None, 1e9
    for q in parts:
        loc, nrm, idx, d = tree(q).find_nearest(Vector(p))
        if loc is not None and d < bd:
            best, bd = q, d
    return best, bd


def window_delta2d(x, z):
    """Projected (front X-Z) distance to the nearest window outline (0 inside)."""
    d = 1e9
    for w in FS.WINDOWS:
        d = min(d, float(FS.outline_sdf2(w, np.array([x]), np.array([z]))[0]))
    return max(d, 0.0)


def check_A7b(n=4000, flank=3.5):
    """Wall probe with the window flank zone defined as in the spec: front
    points (y < centre plane of their body) whose projected distance to a
    window outline is <= flank (45 deg flank from 0.5 mm deep reaches the
    2.8 mm orange wall only at delta = 3.46)."""
    it, _, _, _ = inner_faces_tree()
    pts, nrms = sample_surface("ENV_outer", n, zmin=16.5)
    ty = tree("yellow")
    D2 = np.full(len(pts), 1e9)
    for w in FS.WINDOWS:
        D2 = np.minimum(D2, FS.outline_sdf2(w, pts[:, 0], pts[:, 2]))
    D2 = np.where(pts[:, 1] < 0, np.maximum(D2, 0.0), 1e9)
    rows = []
    for p, d2 in zip(pts, D2):
        part, _ = owner_part(p)
        dy = ty.find_nearest(Vector(p))[3]
        near = it.find_nearest(Vector(p))
        rows.append((part, float(near[3]), dy < flank or d2 <= flank, p, d2))
    res = {"samples": n, "flank_mm": flank}
    for part in ("black", "orange", "green", "pink"):
        sel = [r for r in rows if r[0] == part]
        if not sel:
            continue
        use = [r for r in sel if not r[2]]
        fz = [r for r in sel if r[2]]
        w = np.array([r[1] for r in use])
        res[part] = {"n": len(sel), "n_used": len(use), "min": r3(w.min(), 3), "p1": r3(np.percentile(w, 1), 3),
                     "median": r3(np.median(w), 3),
                     "lowest": [[r3(r[1], 3), [r3(c, 1) for c in r[3]]] for r in sorted(use, key=lambda r: r[1])[:3]],
                     "flank_zone": {"n": len(fz), "min": r3(min(r[1] for r in fz), 3) if fz else None}}
    return res


def face_arrays(name):
    ob = bpy.data.objects[name]
    me = ob.data
    nf = len(me.polygons)
    cen = np.empty(nf * 3, np.float64)
    me.polygons.foreach_get("center", cen)
    nrm = np.empty(nf * 3, np.float64)
    me.polygons.foreach_get("normal", nrm)
    area = np.empty(nf, np.float64)
    me.polygons.foreach_get("area", area)
    return cen.reshape(-1, 3), nrm.reshape(-1, 3), area


def inside(part, p, dirs=((0.3017, 0.1234, 0.9454), (-0.211, 0.377, 0.902), (0.05, -0.61, 0.79))):
    """Ray-parity point membership with a 3-direction majority vote."""
    t = tree(part)
    votes = 0
    for d in dirs:
        n = 0
        o = Vector(p)
        dv = Vector(d).normalized()
        left = 400.0
        while n < 200:
            loc, nr, idx, dist = t.ray_cast(o, dv, left)
            if loc is None:
                break
            n += 1
            o = loc + dv * 1e-5
            left -= dist + 1e-5
        votes += n % 2
    return votes >= 2


def check_A10_tiling(n_per_part=400, eps=0.02, seed=5):
    """At internal colour boundaries: a point just inside part A must be in A
    only; the point just outside must be in exactly one OTHER part."""
    it, _, _, _ = inner_faces_tree()
    to = tree("ENV_outer")
    rng = np.random.default_rng(seed)
    res = {}
    for A in PARTS:
        cen, nrm, area = face_arrays(A)
        # candidate internal faces: away from outer envelope and master inner surface
        idx = rng.choice(len(cen), size=min(len(cen), 40 * n_per_part), replace=False, p=area / area.sum())
        chosen = []
        for i in idx:
            c = Vector(cen[i])
            if to.find_nearest(c)[3] > 0.05 and it.find_nearest(c)[3] > 0.05:
                chosen.append(i)
            if len(chosen) >= n_per_part:
                break
        bad_in, bad_out, gaps, neigh = 0, 0, 0, {}
        for i in chosen:
            c, n = Vector(cen[i]), Vector(nrm[i]).normalized()
            pin, pout = c - n * eps, c + n * eps
            ins = [p for p in PARTS if inside(p, pin)]
            outs = [p for p in PARTS if inside(p, pout)]
            if ins != [A]:
                bad_in += 1
            if len(outs) != 1 or A in outs:
                if len(outs) == 0:
                    gaps += 1
                else:
                    bad_out += 1
            else:
                neigh[outs[0]] = neigh.get(outs[0], 0) + 1
        res[A] = {"boundary_points": len(chosen), "inside_not_exclusive": bad_in,
                  "outside_overlap_or_self": bad_out, "outside_gap": gaps, "neighbours": neigh}
    return res


def check_A10_match(n_per_part=3000, seed=6):
    """Exact tiling test: each internal boundary face of part A (not on the
    outer envelope, not on the chamber/pocket surface) must coincide with a
    face of another part B (distance ~0, opposite normal).  Reports the
    distribution of the mismatch distance."""
    it, _, _, _ = inner_faces_tree()
    to = tree("ENV_outer")
    rng = np.random.default_rng(seed)
    res = {}
    for A in PARTS:
        cen, nrm, area = face_arrays(A)
        idx = rng.choice(len(cen), size=min(int((area > 0).sum()), 30 * n_per_part), replace=False, p=area / area.sum())
        d_all, bad, partner = [], [], {}
        k = 0
        for i in idx:
            c = Vector(cen[i])
            if to.find_nearest(c)[3] <= 0.02 or it.find_nearest(c)[3] <= 0.02:
                continue
            k += 1
            if k > n_per_part:
                break
            nA = Vector(nrm[i]).normalized()
            best = None
            for Bp in PARTS:
                if Bp == A:
                    continue
                loc, nB, idxB, d = tree(Bp).find_nearest(c)
                if loc is not None and (best is None or d < best[1]):
                    best = (Bp, d, nB)
            d_all.append(best[1])
            partner[best[0]] = partner.get(best[0], 0) + 1
            if best[1] > 0.005 or best[2].dot(nA) > -0.9:
                bad.append([[r3(x, 2) for x in c], best[0], r3(best[1], 4), r3(best[2].dot(nA), 3)])
        d = np.array(d_all)
        res[A] = {"boundary_faces_tested": len(d), "partners": partner,
                  "gap_max_mm": r3(d.max(), 4), "gap_p99_mm": r3(np.percentile(d, 99), 5),
                  "n_over_0.005mm_or_not_opposite": len(bad), "examples": bad[:4]}
    return res


def check_A11():
    import json as _json
    res = {}
    rep = _json.load(open(os.path.join(HERE, "face_outlines.json")))["report"]
    arcs = rep["cat_mouth_arcs"]
    rad = arcs["radius"]
    widths = []
    for (cx, cz) in arcs["centres"]:
        # sample along the lower part of each arc (where the line is)
        for ang in np.radians(np.arange(-150, -29, 15)):
            ux, uz = math.cos(ang), math.sin(ang)
            # sweep radially through the line
            hits = []
            for s in np.arange(-1.6, 1.61, 0.01):
                x, z = cx + (rad + s) * ux, cz + (rad + s) * uz
                fh = first_hit_part((x, -150, z), (0, 1, 0))
                if fh and fh[0] == "pink":
                    hits.append(s)
            if hits and min(hits) > -1.59 and max(hits) < 1.59:
                widths.append(max(hits) - min(hits) + 0.01)
    res["mouth_line_width_min_max_n"] = [r3(min(widths), 3), r3(max(widths), 3), len(widths)]
    # inlay depth: pink thickness along the inward normal at pink outer-surface points
    to = tree("ENV_outer")
    cen, nrm, area = face_arrays("pink")
    depths = []
    for c, n in zip(cen, nrm):
        if to.find_nearest(Vector(c))[3] < 0.02 and len(depths) < 400:
            nv = Vector(n).normalized()
            h = hits_along(tree("pink"), Vector(c) - nv * 1e-4, -nv, 5.0)
            if h:
                depths.append(h[0][2] + 1e-4)
    d = np.array(depths)
    res["inlay_depth_min_med_max_n"] = [r3(d.min(), 3), r3(np.median(d), 3), r3(d.max(), 3), len(d)]
    # stem clearance
    lo_g, hi_g = bbox_of("green")
    lo_p, hi_p = bbox_of("pink")
    res["stem_top_z"] = r3(hi_g[2], 3)
    res["mouth_lowest_z"] = r3(lo_p[2], 3)
    res["stem_to_mouth_clearance"] = r3(lo_p[2] - hi_g[2], 3)
    return res


def ear_tip_radius():
    """Fit a circle to the front-projection silhouette of each ear's tip
    (top 2.5 mm)."""
    out = {}
    names = PARTS
    for side, sx in (("left", -1), ("right", 1)):
        pts = []
        for x in np.arange(sx * 24.0, sx * 42.0, sx * 0.05):
            lo_, hi_ = 140.0, 151.0
            if first_hit_part((x, -150, lo_), (0, 1, 0)) is None:
                continue
            for _ in range(30):
                m = 0.5 * (lo_ + hi_)
                if first_hit_part((x, -150, m), (0, 1, 0)) is not None:
                    lo_ = m
                else:
                    hi_ = m
            pts.append((x, 0.5 * (lo_ + hi_)))
        pts = np.array(pts)
        ztop = pts[:, 1].max()
        xtop = pts[np.argmax(pts[:, 1]), 0]
        sel = pts[pts[:, 1] > ztop - 2.5]
        # algebraic circle fit
        A = np.c_[2 * sel[:, 0], 2 * sel[:, 1], np.ones(len(sel))]
        b = sel[:, 0] ** 2 + sel[:, 1] ** 2
        cx, cz, k = np.linalg.lstsq(A, b, rcond=None)[0]
        R = math.sqrt(k + cx * cx + cz * cz)
        out[side] = {"tip_x": r3(xtop, 3), "tip_z": r3(ztop, 4), "fit_radius_top2.5mm": r3(R, 3),
                     "fit_points": len(sel)}
    return out


def teeth():
    """Orange teeth inside the pumpkin mouth, from a first-hit map (0.05 mm)."""
    xs = np.arange(-26.0, 26.0, 0.05)
    zs = np.arange(34.0, 55.0, 0.05)
    top = np.full(len(xs), np.nan)
    bot = np.full(len(xs), np.nan)
    ty = tree("yellow")
    for i, x in enumerate(xs):
        yz = []
        for z in zs:
            fh = first_hit_part((x, -150, z), (0, 1, 0), parts=("yellow", "orange", "black"))
            if fh and fh[0] == "yellow":
                yz.append(z)
        if yz:
            top[i], bot[i] = max(yz), min(yz)
    out = {}
    # top teeth: yellow top dips; bottom tooth: yellow bottom rises
    for name, arr, sgn, rng_ in (("top_left", top, -1, (-18, -6)), ("top_right", top, -1, (6, 18)),
                                 ("bottom", bot, 1, (-7, 7))):
        m = (xs > rng_[0]) & (xs < rng_[1]) & np.isfinite(arr)
        xx, aa = xs[m], arr[m]
        ref_l, ref_r = aa[0], aa[-1]
        # tooth span: where the curve departs > 1.0 from the straight line between the window ends
        line = ref_l + (ref_r - ref_l) * (xx - xx[0]) / (xx[-1] - xx[0])
        dev = (line - aa) if sgn < 0 else (aa - line)
        span = xx[dev > 1.0]
        # hull line through the shoulders just outside the tooth
        if len(span):
            x0, x1 = span.min(), span.max()
            sh_l = aa[np.argmin(np.abs(xx - (x0 - 0.4)))]
            sh_r = aa[np.argmin(np.abs(xx - (x1 + 0.4)))]
            xc = 0.5 * (x0 + x1)
            hull_c = 0.5 * (sh_l + sh_r)
            tip = aa[np.argmin(np.abs(xx - xc))]
            out[name] = {"width": r3(x1 - x0, 2), "height": r3(abs(hull_c - tip), 2), "x_span": [r3(x0, 2), r3(x1, 2)]}
    return out


def thin_features(n=6000, seed=4):
    """Inward ray thickness at surface samples of each part (min feature
    check).  Excludes the yellow skins, the window flank zone (projected
    distance <= 3.5 mm) and the base z < 16.5 (stage-1 geometry, verified
    separately; its flex arms are 1.6 by design)."""
    res = {}
    for p in ("black", "orange", "green", "pink"):
        cen, nrm, area = face_arrays(p)
        rng = np.random.default_rng(seed)
        idx = rng.choice(len(cen), size=n, replace=True, p=area / area.sum())
        C = cen[idx]
        N = nrm[idx]
        D2 = np.full(len(C), 1e9)
        for w in FS.WINDOWS:
            D2 = np.minimum(D2, FS.outline_sdf2(w, C[:, 0], C[:, 2]))
        keep = (C[:, 2] > 16.5) & ~((C[:, 1] < 0) & (D2 <= 3.5))
        t = tree(p)
        th = []
        for c, nv in zip(C[keep], N[keep]):
            v = Vector(nv).normalized()
            h = t.ray_cast(Vector(c) - v * 1e-4, -v, 100.0)
            if h[0] is not None:
                th.append((h[3] + 1e-4, c))
        th.sort(key=lambda r: r[0])
        res[p] = {"n": len(th), "min": r3(th[0][0], 3), "p1": r3(np.percentile([r[0] for r in th], 1), 3),
                  "lowest": [[r3(a, 3), [r3(x, 1) for x in c]] for a, c in th[:4]]}
    return res


def skin_undersides():
    """Overhang of each window skin's inner face (a 0.5 mm skin whose outer
    surface faces upward is a thin ceiling)."""
    to = tree("ENV_outer")
    cen, nrm, area = face_arrays("yellow")
    inner = np.array([to.find_nearest(Vector(c))[3] > 0.05 for c in cen])
    ang = np.degrees(np.arcsin(np.clip(-nrm[:, 2], -1, 1)))
    W = np.full(len(cen), -1)
    best = np.full(len(cen), 1e9)
    for k, w in enumerate(FS.WINDOWS):
        d = FS.outline_sdf2(w, cen[:, 0], cen[:, 2])
        W = np.where(d < best, k, W)
        best = np.minimum(best, d)
    res = {}
    for k, w in enumerate(FS.WINDOWS):
        m = inner & (W == k) & (ang > 0)
        a = area[m]
        g = ang[m]
        res[w] = {"ceiling_area": r3(a.sum(), 1), "gt45": r3(a[g > 45].sum(), 2), "gt55": r3(a[g > 55].sum(), 2),
                  "gt60": r3(a[g > 60].sum(), 2), "max": r3(g.max(), 1) if len(g) else None,
                  "z_range_gt60": [r3(cen[m][g > 60][:, 2].min(), 1), r3(cen[m][g > 60][:, 2].max(), 1)] if (g > 60).any() else None}
    return res


def base_undercuts():
    """Outer surface near the deck (z 16.2..32): area facing down steeper than
    45 / 55 deg from vertical (spec 7: forms meeting the deck go vertical or
    taper inward <= 45 deg)."""
    cen, nrm, area = face_arrays("ENV_outer")
    m = (cen[:, 2] > 16.2) & (cen[:, 2] < 32.0)
    ang = np.degrees(np.arcsin(np.clip(-nrm[:, 2], -1, 1)))
    out = {}
    for lim in (45, 50, 55, 60):
        s = m & (ang > lim)
        out[">%d" % lim] = {"area_mm2": r3(area[s].sum(), 1),
                            "where_xyz_mean": [r3(v, 1) for v in cen[s].mean(0)] if s.any() else None}
    out["downward_total_area"] = r3(area[m & (ang > 0)].sum(), 1)
    return out


def check_A6(cache):
    """Chamber metrics from the final chamber field (cache dir of build_figure)."""
    load = lambda n: np.load(os.path.join(cache, n + ".npy"))
    g = FS.Grid()
    h = g.h
    xs, ys, zs = g.ax
    C = load("C")
    Cp, Ct, Ch, Cn = load("C_pumpkin"), load("C_torso"), load("C_head"), load("C_neck")
    out = {}
    sec = []
    for z in np.arange(90.0, 96.01, 0.5):
        k = g.kz(z)
        m = C[:, :, k] < 0
        ii, jj = np.nonzero(m)
        sec.append([float(z), r3(m.sum() * h * h, 1), r3(np.ptp(xs[ii]) + h, 1), r3(np.ptp(ys[jj]) + h, 1)])
    out["chamber_section_z90_96"] = sec
    out["neck_min_section"] = min(sec, key=lambda r: r[1])
    link = []
    for z in np.arange(86.0, 100.01, 0.5):
        k = g.kz(z)
        conn = (Ch[:, :, k] < 0) & ((Ct[:, :, k] < 0) | (Cn[:, :, k] < 0))
        if conn.any():
            ii, jj = np.nonzero(conn)
            link.append([float(z), r3(conn.sum() * h * h, 1), r3(np.ptp(xs[ii]) + h, 1), r3(np.ptp(ys[jj]) + h, 1)])
    out["head_torso_link_by_z"] = link
    k0 = g.kz(16.5)
    R = np.hypot(xs[:, None], ys[None, :])
    disc = R < 27.0
    inch = C[:, :, k0:] < 0
    blocked = ~inch
    first = np.where(blocked.any(axis=2), blocked.argmax(axis=2), inch.shape[2])
    kk = np.arange(inch.shape[2])[None, None, :]
    reach = kk < first[:, :, None]
    for nm, Cc in (("pumpkin", Cp), ("torso", Ct)):
        los = ((Cc[:, :, k0:] < 0) & reach).any(axis=2) & disc
        ii, jj = np.nonzero(los)
        out["plenum_to_%s_line_of_sight" % nm] = [r3(los.sum() * h * h, 1), r3(np.ptp(xs[ii]) + h, 1), r3(np.ptp(ys[jj]) + h, 1)]
        dk = disc & (Cc[:, :, k0] < 0)
        out["plenum_to_%s_at_deck_z16.5" % nm] = r3(dk.sum() * h * h, 1)
    out["plenum_open_at_z16.5"] = r3((disc & (C[:, :, k0] < 0)).sum() * h * h, 1)
    best = (0, None)
    for j in range(len(ys)):
        a = ((Cp[:, j, :] < 0) & (Ct[:, j, :] < 0)).sum() * h * h
        if a > best[0]:
            best = (a, float(ys[j]))
    out["pumpkin_torso_overlap_max_section"] = [r3(best[0], 1), best[1]]
    m = C < 0
    seed = np.zeros_like(m)
    seed[g.n[0] // 2, g.n[1] // 2, g.kz(14.0)] = True
    cur = seed & m
    for it in range(3000):
        nxt = cur.copy()
        nxt[1:] |= cur[:-1]; nxt[:-1] |= cur[1:]
        nxt[:, 1:] |= cur[:, :-1]; nxt[:, :-1] |= cur[:, 1:]
        nxt[:, :, 1:] |= cur[:, :, :-1]; nxt[:, :, :-1] |= cur[:, :, 1:]
        nxt &= m
        if nxt.sum() == cur.sum():
            break
        cur = nxt
    out["chamber_voxels"] = int(m.sum())
    out["reached_from_plenum"] = int(cur.sum())
    out["chamber_volume_cm3"] = r3(m.sum() * h ** 3 / 1000.0, 1)
    return out


def check_A4(black="black"):
    """REF dummies against a cropped copy of the black base (exact booleans)."""
    src = bpy.data.objects[black]
    crop = V._dup(src, "_base_crop")
    crop.parent = None
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((70 * (1 if v.co.x > 0 else -1), 70 * (1 if v.co.y > 0 else -1), 20.0 if v.co.z > 0 else -2.0))
    box = B.bm_to_obj(bm, "_crop_box", B.coll("WORK_temp"))
    B.apply_boolean(crop, box, 'INTERSECT')
    B.remove_obj("_crop_box")
    res = V.ref_checks(crop)
    B.remove_obj("_base_crop")
    return res


def check_A12(out_level, out_tilt):
    import overlay_figure as OV
    importlib.reload(OV)
    ov = OV.run(list(PARTS), out_level, out_tilt, step=1)

    def half_width(z, xs=np.arange(0.0, 62.0, 0.05)):
        L = R_ = None
        for x in xs:
            if first_hit_part((x, -150, z), (0, 1, 0)):
                R_ = x
            if first_hit_part((-x, -150, z), (0, 1, 0)):
                L = -x
        return L, R_
    # head: widest silhouette between z 95 and 118 (below the ears)
    hw = []
    for z in np.arange(95.0, 118.01, 1.0):
        L, R_ = half_width(z, np.arange(30.0, 50.0, 0.05))
        hw.append((R_ - L, z))
    head = max(hw)
    # arm span: widest silhouette z 50..90
    aw = []
    for z in np.arange(50.0, 90.01, 1.0):
        L, R_ = half_width(z, np.arange(40.0, 62.0, 0.05))
        aw.append((R_ - L, z, L, R_))
    arm = max(aw)
    lo, hi = bbox_of("orange")
    cat_eyes = []
    for sx in (-1, 1):
        pts = []
        for a in np.linspace(0, 2 * math.pi, 72, endpoint=False):
            lo_, hi_ = 5.0, 12.0
            cx, cz = sx * 17.0, 115.0
            for _ in range(25):
                m = 0.5 * (lo_ + hi_)
                fh = first_hit_part((cx + m * math.cos(a), -150, cz + m * math.sin(a)), (0, 1, 0))
                if fh and fh[0] == "yellow":
                    lo_ = m
                else:
                    hi_ = m
            pts.append((cx + lo_ * math.cos(a), cz + lo_ * math.sin(a)))
        pts = np.array(pts)
        cat_eyes.append([r3(pts[:, 0].mean(), 3), r3(pts[:, 1].mean(), 3), r3(2 * np.mean(np.hypot(pts[:, 0] - pts[:, 0].mean(), pts[:, 1] - pts[:, 1].mean())), 3)])
    return {"overlay": ov, "head_width": [r3(head[0], 2), "at z", head[1]],
            "arm_span": [r3(arm[0], 2), "at z", arm[1], [r3(arm[2], 2), r3(arm[3], 2)]],
            "pumpkin_width_orange_bbox": r3(hi[0] - lo[0], 2),
            "cat_eye_centres_x_z_OD": cat_eyes, "ear_tips": ear_tip_radius()}


def check_A7(n=3000):
    """Wall probe: points on the outer surface (area-weighted, above the deck
    and the base), true wall = distance to the nearest inner-surface point."""
    it, _, _, _ = inner_faces_tree()
    pts, nrms = sample_surface("ENV_outer", n, zmin=16.5)
    ty = tree("yellow")
    rows = []
    for p, nr in zip(pts, nrms):
        part, _ = owner_part(p)
        dy = ty.find_nearest(Vector(p))[3]
        near = it.find_nearest(Vector(p))
        rows.append((part, float(near[3]), float(dy), p))
    res = {"samples": n}
    for part in ("black", "orange", "green", "pink", "yellow"):
        sel = [r for r in rows if r[0] == part]
        if not sel:
            continue
        allw = np.array([r[1] for r in sel])
        excl = np.array([r[2] < 3.5 for r in sel])       # window + 45 deg flank zone
        w = allw[~excl] if part != "yellow" else allw
        lows = sorted([r for r, e in zip(sel, excl) if not e], key=lambda r: r[1])[:4] if part != "yellow" else []
        res[part] = {"n": len(sel), "n_used": int(len(w)), "min": r3(w.min(), 3) if len(w) else None,
                     "p1": r3(np.percentile(w, 1), 3) if len(w) else None,
                     "median": r3(np.median(w), 3) if len(w) else None,
                     "lowest": [[r3(r[1], 3), [r3(c, 1) for c in r[3]]] for r in lows]}
        if part != "yellow":
            fz = allw[excl]
            res[part]["window_flank_zone_n_min"] = [int(len(fz)), r3(fz.min(), 3) if len(fz) else None]
    return res


def check_A13(bridge_z=None):
    """Ceiling faces of the master's inner surface (chamber + pockets); base
    void (z < 18.5) reported separately."""
    it, cen, nrm, area = inner_faces_tree()
    ang = np.degrees(np.arcsin(np.clip(-nrm[:, 2], -1, 1)))      # >0 = ceiling
    fig = cen[:, 2] > 18.5
    bins = [0, 45, 50, 55, 58, 60, 65, 75, 85, 90.01]
    out = {"figure_ceiling_area_mm2": {f"{bins[i]}-{bins[i+1]}": r3(area[fig & (ang >= bins[i]) & (ang < bins[i + 1])].sum(), 1)
                                       for i in range(len(bins) - 1)},
           "base_void_ceiling_area_mm2": {f"{bins[i]}-{bins[i+1]}": r3(area[~fig & (ang >= bins[i]) & (ang < bins[i + 1])].sum(), 1)
                                          for i in range(len(bins) - 1)}}
    # clusters of > 60 deg faces in the figure (bridges)
    sel = np.nonzero(fig & (ang > 60))[0]
    pts = cen[sel]
    used = np.zeros(len(sel), bool)
    clusters = []
    for i in range(len(sel)):
        if used[i]:
            continue
        m = (np.linalg.norm(pts - pts[i], axis=1) < 1.2) & ~used
        for _ in range(400):
            grow = np.zeros(len(sel), bool)
            for j in np.nonzero(m)[0]:
                grow |= (np.linalg.norm(pts - pts[j], axis=1) < 1.2)
            grow &= ~used
            if grow.sum() == m.sum():
                break
            m = grow
        used |= m
        P_ = pts[m]
        ar = float(area[sel][m].sum())
        if len(P_) > 2:
            c = P_ - P_.mean(0)
            _, s, vt = np.linalg.svd(c, full_matrices=False)
            pr = c @ vt.T
            L1 = float(np.ptp(pr[:, 0])) + 0.5
            L2 = float(np.ptp(pr[:, 1])) + 0.5
        else:
            L1 = L2 = 0.5
        clusters.append({"centre": [r3(v, 1) for v in P_.mean(0)], "area": r3(ar, 2),
                         "extent_long_short": [r3(L1, 1), r3(L2, 1)], "max_ang": r3(ang[sel][m].max(), 1)})
    clusters.sort(key=lambda c: -c["area"])
    out["n_clusters_gt60"] = len(clusters)
    out["clusters_gt60_top"] = clusters[:10]
    out["max_short_extent_excluding_top2"] = max([c["extent_long_short"][1] for c in clusters[2:]] or [0])
    return out
