"""v2 verification additions (run inside Blender, after build_figure_v2).
Reuses verify_figure.py for the unchanged checks.

    check_A7_bands   orange / black wall by distance-from-window band (>= 12,000 samples each)
    check_A8_v2      skin at the 5 spec points + dense grid; void behind along the normal AND +Y
    check_A9_v12     spec v1.2 pupils: flush black skin discs, no plug
"""
import math
import importlib

import bpy
import numpy as np
from mathutils import Vector

import params as P
import figure_shapes as FS
import verify_figure as VF

PARTS = VF.PARTS


def r3(v, n=3):
    return round(float(v), n)


def outer_faces_of(part, tol=0.01):
    """Faces of `part` lying on the outer envelope (centre within tol)."""
    to = VF.tree("ENV_outer")
    cen, nrm, area = VF.face_arrays(part)
    on = np.array([to.find_nearest(Vector(c))[3] <= tol for c in cen])
    return cen[on], nrm[on], area[on]


def sample_on(cen, area, n, rng, near_pts=None):
    """Area-weighted face sample, without repeats when there are enough faces."""
    ok = area > 0
    p = np.where(ok, area, 0.0)
    p = p / p.sum()
    k = int(ok.sum())
    return rng.choice(len(cen), size=min(n, k), replace=False, p=p) if k >= n else \
        rng.choice(len(cen), size=n, replace=True, p=p)


def outer_tris_of(part, tol=0.01):
    """Triangles of `part` lying on the outer envelope: (A, B, C) corner arrays."""
    import export_figure_v2 as EX
    V, F = EX.tri_arrays(bpy.data.objects[part])
    V = V.astype(np.float64)
    A, B_, C = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    cen = (A + B_ + C) / 3.0
    to = VF.tree("ENV_outer")
    on = np.array([to.find_nearest(Vector(c))[3] <= tol for c in cen])
    return A[on], B_[on], C[on]


def random_points(A, B_, C, n, rng, weight_mask=None):
    area = 0.5 * np.linalg.norm(np.cross(B_ - A, C - A), axis=1)
    if weight_mask is not None:
        area = area * weight_mask
    i = rng.choice(len(A), size=n, replace=True, p=area / area.sum())
    r1 = np.sqrt(rng.random(n))
    r2 = rng.random(n)
    return (1 - r1)[:, None] * A[i] + (r1 * (1 - r2))[:, None] * B_[i] + (r1 * r2)[:, None] * C[i]


def check_A7_bands(n=15000, n_near=12000, seed=21, bands=None):
    """Wall = distance from an outer-surface point to the nearest inner
    surface of the master (chamber, pockets) = the shortest line of sight
    from the lit interior to that point.  Bands by 3-D distance to the
    nearest yellow (window) point: 0-3.5 (flank zone), 3.5-4, 4-5, 5-6, >6.
    n uniform random surface points per part + n_near more within 8 mm of a
    window (area-weighted, random positions inside the triangles)."""
    it = VF.inner_faces_tree()[0]
    ty = VF.tree("yellow")
    rng = np.random.default_rng(seed)
    bands = bands or [(0.0, 3.5), (3.5, 4.0), (4.0, 5.0), (5.0, 6.0), (6.0, 1e9)]
    out = {}
    for part, rule in (("orange", P.WALL_PUMPKIN_MIN), ("black", P.WALL_CAT_MIN)):
        A, B_, C = outer_tris_of(part)
        cz = (A[:, 2] + B_[:, 2] + C[:, 2]) / 3.0
        keep = cz > 16.5
        A, B_, C = A[keep], B_[keep], C[keep]
        cen = (A + B_ + C) / 3.0
        dwin_c = np.array([ty.find_nearest(Vector(c))[3] for c in cen])
        P1 = random_points(A, B_, C, n, rng)
        P2 = random_points(A, B_, C, n_near, rng, weight_mask=(dwin_c < 8.5).astype(float))
        PP = np.vstack([P1, P2])
        if part == "black":
            # the pupils are black WINDOW SKIN (spec v1.2), not wall: excluded
            pup = np.zeros(len(PP), bool)
            for sx in (-1, 1):
                pup |= (np.hypot(PP[:, 0] - sx * P.CAT_EYE_X, PP[:, 2] - P.CAT_EYE_Z) < 4.3) & (PP[:, 1] < -5)
            PP = PP[~pup]
        pts = [Vector(p) for p in PP]
        W = np.array([it.find_nearest(p)[3] for p in pts])
        D = np.array([ty.find_nearest(p)[3] for p in pts])
        res = {"samples": int(len(pts)), "uniform": int(n), "near_window": int(n_near), "rule_mm": rule}
        for lo, hi in bands:
            m = (D >= lo) & (D < hi)
            key = "%.1f-%s" % (lo, ("%.1f" % hi) if hi < 1e8 else "inf")
            if m.any():
                j = np.nonzero(m)[0][np.argmin(W[m])]
                res[key] = {"n": int(m.sum()), "min": r3(W[m].min()), "p1": r3(np.percentile(W[m], 1)),
                            "median": r3(np.median(W[m])), "below_rule": int((W[m] < rule).sum()),
                            "min_at": [r3(v, 2) for v in pts[j]]}
            else:
                res[key] = {"n": 0}
        m = D >= 3.5
        res["outside_3.5_min"] = r3(W[m].min()) if m.any() else None
        res["outside_3.5_below_rule"] = int((W[m] < rule).sum())
        out[part] = res
    # green (stem) and pink (inlay + black behind): same metric, no band
    for part in ("green", "pink"):
        cen, nrm, area = outer_faces_of(part)
        idx = sample_on(cen, area, 3000, rng)
        W = np.array([it.find_nearest(Vector(cen[i]))[3] for i in idx])
        out[part] = {"samples": 3000, "min": r3(W.min()), "median": r3(np.median(W))}
    return out


def skin_normal(x, z):
    """Front point (x, z): first part hit along +Y, skin thickness along the
    inward outer normal, then the clear distance behind the skin along the
    normal and along +Y before any solid of any part."""
    fh = VF.first_hit_part((x, -150.0, z), (0, 1, 0))
    if fh is None:
        return None
    p, loc, nrm, dist = fh
    n = nrm.normalized()
    hs = VF.hits_along(VF.tree(p), loc - n * 1e-4, -n, 20.0)
    if not hs:
        return None
    th = hs[0][2] + 1e-4
    back = hs[0][0] - n * 1e-3
    nxt_n = VF.first_hit_part(back, -n)
    hy = VF.hits_along(VF.tree(p), loc + Vector((0, 1e-4, 0)), (0, 1, 0), 20.0)
    nxt_y = VF.first_hit_part(hy[0][0] + Vector((0, 1e-3, 0)), (0, 1, 0)) if hy else None
    return {"part": p, "skin": th, "void_normal": nxt_n[3] if nxt_n else 999.0,
            "void_normal_part": nxt_n[0] if nxt_n else None,
            "void_y": nxt_y[3] if nxt_y else 999.0, "void_y_part": nxt_y[0] if nxt_y else None}


def check_A8_v2(dense_step=0.5):
    res = {}
    for w in FS.WINDOWS:
        rec = []
        for tag, (x, z) in VF.outline_points(w, inset=1.0):
            s = skin_normal(x, z)
            rec.append({"pt": tag, "x": r3(x, 2), "z": r3(z, 2), "part": s["part"], "skin": r3(s["skin"], 4),
                        "void_behind_normal": r3(s["void_normal"], 2), "void_behind_Y": r3(s["void_y"], 2)})
        res[w] = rec
    dense = {}
    for w in FS.WINDOWS:
        pts = np.vstack(FS.outlines()[w])
        xs = np.arange(pts[:, 0].min(), pts[:, 0].max(), dense_step)
        zs = np.arange(pts[:, 1].min(), pts[:, 1].max(), dense_step)
        X, Z = np.meshgrid(xs, zs, indexing="ij")
        D = FS.outline_sdf2(w, X, Z)
        th, vn, vy, parts, vy_block = [], [], [], set(), 0
        for x, z in zip(X[D < -0.3], Z[D < -0.3]):
            s = skin_normal(float(x), float(z))
            if s is None:
                continue
            parts.add(s["part"])
            th.append(s["skin"])
            vn.append(s["void_normal"])
            vy.append(s["void_y"])
        th, vn, vy = np.array(th), np.array(vn), np.array(vy)
        dense[w] = {"n": len(th), "skin_min": r3(th.min(), 4), "skin_med": r3(np.median(th), 4),
                    "skin_max": r3(th.max(), 4), "first_parts": sorted(parts),
                    "void_behind_normal_min_med": [r3(vn.min(), 2), r3(np.median(vn), 2)],
                    "void_behind_Y_min_med": [r3(vy.min(), 2), r3(np.median(vy), 2)],
                    "Y_rays_blocked_within_2mm": int((vy < 2.0).sum())}
    res["dense"] = dense
    # rib-free: rib groove depth at every pumpkin-window vertex of the yellow part
    me = bpy.data.objects["yellow"].data
    co = np.empty(len(me.vertices) * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    pk = co[co[:, 2] < 95]
    x0, x1, z0, z1 = FS.face_box()
    cx, cz, hx, hz = 0.5 * (x0 + x1), 0.5 * (z0 + z1), 0.5 * (x1 - x0), 0.5 * (z1 - z0)
    qx = np.abs(pk[:, 0] - cx) - hx
    qz = np.abs(pk[:, 2] - cz) - hz
    dface = np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qz, 0) ** 2) + np.minimum(np.maximum(qx, qz), 0)
    fade2 = FS.smoothstep(P.RIB_FACE_CLEAR, P.RIB_FACE_CLEAR + P.RIB_FADE_W, dface)
    front = FS.smoothstep(0.0, 8.0, P.PK_YC - pk[:, 1])
    res["rib_factor_max_at_pumpkin_window_vertices"] = float((1.0 - front * (1.0 - fade2)).max())
    res["pumpkin_window_vertices"] = int(len(pk))
    return res


def check_A13_v2(limit_deg=60.0, zmin=18.5):
    """Interior ceilings of the master flatter than limit_deg from vertical,
    grouped by mesh connectivity (shared vertices).  Each cluster: area and
    the extent of its VERTICES along its two principal axes (short extent =
    bridge span).  Works for large decimated faces (v1 used centroids)."""
    import export_figure_v2 as EX
    it, cen0, nrm0, area0 = VF.inner_faces_tree()
    V, F = EX.tri_arrays(bpy.data.objects["M2_windows"])
    V = V.astype(np.float64)
    A, B_, C = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    cen = (A + B_ + C) / 3.0
    nrm = np.cross(B_ - A, C - A)
    area = 0.5 * np.linalg.norm(nrm, axis=1)
    nrm = nrm / np.maximum(2 * area, 1e-30)[:, None]
    to = VF.tree("ENV_outer")
    inner = np.array([to.find_nearest(Vector(c))[3] > 0.02 for c in cen])
    ang = np.degrees(np.arcsin(np.clip(-nrm[:, 2], -1, 1)))
    sel = np.nonzero(inner & (cen[:, 2] > zmin) & (ang > limit_deg) & (area > 1e-9))[0]
    # union-find over shared vertices
    parent = {}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for i in sel:
        parent[i] = i
    vfaces = {}
    for i in sel:
        for v in F[i]:
            vfaces.setdefault(int(v), []).append(int(i))
    for fl in vfaces.values():
        r0 = find(fl[0])
        for f in fl[1:]:
            r = find(f)
            if r != r0:
                parent[r] = r0
    groups = {}
    for i in sel:
        groups.setdefault(find(i), []).append(i)
    clusters = []
    for g in groups.values():
        g = np.array(g)
        vid = np.unique(F[g].ravel())
        Pv = V[vid]
        c = Pv - Pv.mean(0)
        if len(Pv) >= 3:
            _, s, vt = np.linalg.svd(c, full_matrices=False)
            pr = c @ vt.T
            L1, L2 = float(np.ptp(pr[:, 0])), float(np.ptp(pr[:, 1]))
        else:
            L1 = L2 = 0.0
        clusters.append({"centre": [r3(v, 1) for v in Pv.mean(0)], "area": r3(area[g].sum(), 2),
                         "extent_long_short": [r3(L1, 1), r3(L2, 1)], "max_ang": r3(ang[g].max(), 1),
                         "z": r3(Pv[:, 2].mean(), 2)})
    clusters.sort(key=lambda c: -c["area"])
    return {"n_clusters": len(clusters), "total_area_gt%d" % limit_deg: r3(area[sel].sum(), 1),
            "clusters": clusters[:14],
            "short_extent_max_small_clusters": max([c["extent_long_short"][1] for c in clusters
                                                    if c["area"] < 5.0] or [0])}


def yellow_pocket_ceilings():
    """Skin inner faces (pocket floor, on the master's inner surface) that
    face downward: overhang of the 0.5 mm skin, per window."""
    it = VF.inner_faces_tree()[0]
    cen, nrm, area = VF.face_arrays("yellow")
    onfloor = np.array([it.find_nearest(Vector(c))[3] < 0.005 for c in cen])
    ang = np.degrees(np.arcsin(np.clip(-nrm[:, 2], -1, 1)))
    W = np.full(len(cen), -1)
    best = np.full(len(cen), 1e9)
    for k, w in enumerate(FS.WINDOWS):
        d = FS.outline_sdf2(w, cen[:, 0], cen[:, 2])
        W = np.where(d < best, k, W)
        best = np.minimum(best, d)
    res = {}
    for k, w in enumerate(FS.WINDOWS):
        m = onfloor & (W == k) & (ang > 0)
        a, g = area[m], ang[m]
        res[w] = {"downward_floor_area": r3(a.sum(), 1), "gt45": r3(a[g > 45].sum(), 2), "gt55": r3(a[g > 55].sum(), 2),
                  "gt60": r3(a[g > 60].sum(), 2), "max": r3(g.max(), 1) if len(g) else None}
    return res


def check_A9_v12():
    """Pupils (spec v1.2): black disc in the skin, dia 8.0 +/- 0.3, thickness
    0.40-0.60 at >= 5 points, flush, nothing behind, nothing yellow inside."""
    to = VF.tree("ENV_outer")
    out = {}
    for side, sx in (("L", -1), ("R", 1)):
        cx, cz = sx * P.CAT_EYE_X, P.CAT_EYE_Z
        radii = []
        for k in range(32):
            a = 2 * math.pi * k / 32
            lo_, hi_ = 3.0, 5.0
            for _ in range(30):
                m = 0.5 * (lo_ + hi_)
                fh = VF.first_hit_part((cx + m * math.cos(a), -150, cz + m * math.sin(a)), (0, 1, 0))
                if fh and fh[0] == "black":
                    lo_ = m
                else:
                    hi_ = m
            radii.append(0.5 * (lo_ + hi_))
        pts = [(0.0, 0.0)] + [(2.5 * math.cos(a), 2.5 * math.sin(a)) for a in np.radians([0, 90, 180, 270, 45, 135, 225, 315])]
        th = []
        for dx, dz in pts:
            s = skin_normal(cx + dx, cz + dz)
            th.append({"at": [r3(dx, 2), r3(dz, 2)], "part": s["part"], "skin": r3(s["skin"], 4),
                       "void_behind_normal": r3(s["void_normal"], 2), "void_behind_Y": r3(s["void_y"], 2)})
        # flush: black pupil outer faces lie on the envelope
        cen, nrm, area = VF.face_arrays("black")
        m = (np.hypot(cen[:, 0] - cx, cen[:, 2] - cz) < 3.9) & (cen[:, 1] < 0)
        on = [to.find_nearest(Vector(c))[3] for c in cen[m]]
        non_black = 0
        for k in range(64):
            a = 2 * math.pi * k / 64
            for rr in (0.0, 1.5, 3.0, 3.85):
                f2 = VF.first_hit_part((cx + rr * math.cos(a), -150, cz + rr * math.sin(a)), (0, 1, 0))
                if f2 and f2[0] != "black":
                    non_black += 1
        # yellow ring next to the pupil: skin thickness at r 4.3 (same skin plane)
        ring = [r3(skin_normal(cx + 4.3 * math.cos(a), cz + 4.3 * math.sin(a))["skin"], 4)
                for a in np.radians([0, 90, 180, 270])]
        out[side] = {"diameter_min_max": [r3(2 * min(radii), 3), r3(2 * max(radii), 3)],
                     "thickness_points": th,
                     "thickness_min_max": [min(t["skin"] for t in th), max(t["skin"] for t in th)],
                     "pupil_faces_on_envelope_max_dist": r3(max(on), 5) if on else None,
                     "pupil_front_faces": int(m.sum()),
                     "non_black_hits_inside_r3.85_of_256": non_black,
                     "adjacent_yellow_ring_skin_r4.3": ring}
    # black shells: the two pupil discs are thin (volume ~ pi*4^2*0.5 = 25 mm3)
    import build_figure as BF
    st = BF.mesh_stats(bpy.data.objects["black"])
    out["black_shells"] = st["shells"]
    out["black_shell_sizes"] = st["shell_sizes"][:3]
    return out
