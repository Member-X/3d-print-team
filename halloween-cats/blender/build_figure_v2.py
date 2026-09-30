"""Stage-2 v2 build of the "Pumpkin Hug" figure (run inside Blender).

v2 changes against v1 (build_figure.py, kept unchanged in v1_scripts/):
  * window pockets built in SURFACE-NORMAL coordinates: the pocket flank
    angle phi is measured from the local surface normal and chosen per outline
    point (<= WINDOW_FLANK_MAX_DEG, pocket ceilings <= 55/60 deg), instead of
    45 deg to the Y projection axis (which thinned the orange wall);
  * smoother pumpkin ribs (figure_shapes.rib_offset);
  * lighter meshes: the envelope, chamber, cutters and zones are decimated
    BEFORE the booleans, so the five parts still tile exactly;
  * head roof bridge R 9.4.
Heavy steps are launched with bgrun.run(...) so no MCP call has to stay open.

    import build_figure_v2 as B2
    B2.setup_file()                  # new file blender/halloween-cat-v2.blend
    bgrun.run("fields", B2.step_fields)
    ...
"""
import math
import os
import sys
import time
import importlib

import bpy
import bmesh
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree

HERE = r"H:\ClaudeStuff\3d-print-team\halloween-cats\blender"
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import params as P            # noqa: E402
importlib.reload(P)
import figure_shapes as FS    # noqa: E402
importlib.reload(FS)
import build_test_parts as B  # noqa: E402
importlib.reload(B)
import build_figure as BF     # noqa: E402
importlib.reload(BF)

SCR = r"C:\Users\steve\AppData\Local\Temp\claude\H--ClaudeStuff-3d-print-team\803b752c-0c19-4c39-a372-657e0ca1ec54\scratchpad"
CACHE = os.path.join(SCR, "cache_v2")
LOGFILE = os.path.join(SCR, "bg", "v2_build.log")
BLEND = os.path.join(HERE, "halloween-cat-v2.blend")
VERSIONS = os.path.join(HERE, "versions")

# point the v1 helpers at the v2 cache / file / log
BF.CACHE = CACHE
BF.BLEND = BLEND


def log(msg):
    s = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)
    with open(LOGFILE, "a") as f:
        f.write(s + "\n")
    print(s)


BF.log = log
coll = BF.coll
remove_obj = BF.remove_obj


def save(tag=None):
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    if tag:
        os.makedirs(VERSIONS, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(VERSIONS, "halloween-cat_%s.blend" % tag), copy=True)
    log("saved %s%s" % (BLEND, (" + versions/halloween-cat_%s.blend" % tag) if tag else ""))
    return BLEND


def setup_file():
    """New file for v2 (the v1 file halloween-cat.blend is left untouched)."""
    bpy.ops.wm.read_homefile(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.unit_settings.length_unit = 'MILLIMETERS'
    sc.unit_settings.scale_length = 0.001
    coll(BF.COLL_FIG)
    B.build_refs()
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    log("new v2 file " + BLEND)
    return BLEND


# ================================================================== mesh helpers
def tri_count(ob):
    ob.data.calc_loop_triangles()
    return len(ob.data.loop_triangles)


def decimate(ob, target_tris=None, ratio=None):
    """Quadric edge-collapse decimation (Blender DECIMATE/COLLAPSE), applied
    through the depsgraph (no operators).  Triangulated result."""
    n0 = tri_count(ob)
    if ratio is None:
        ratio = min(1.0, float(target_tris) / n0)
    mod = ob.modifiers.new("dec_tmp", 'DECIMATE')
    mod.decimate_type = 'COLLAPSE'
    mod.ratio = ratio
    mod.use_collapse_triangulate = True
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    ev = ob.evaluated_get(dg)
    new = bpy.data.meshes.new_from_object(ev)
    ob.modifiers.remove(mod)
    old = ob.data
    new.name = old.name
    ob.data = new
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return {"tris_before": n0, "tris_after": tri_count(ob), "ratio": round(ratio, 4)}


def crossings(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
    n = len(BF.crossing_pairs(bm))
    bm.free()
    return n


def tree_of(ob):
    return BF.bvh_of(ob)


def verts_of(ob):
    co = np.empty(len(ob.data.vertices) * 3, np.float64)
    ob.data.vertices.foreach_get("co", co)
    return co.reshape(-1, 3)


def deviation(fine, dec, n=150000, seed=1):
    """Two-sided vertex-to-surface distance between two meshes (sampled)."""
    rng = np.random.default_rng(seed)
    out = {}
    for a, b, tag in ((fine, dec, "fine_to_dec"), (dec, fine, "dec_to_fine")):
        V = verts_of(a)
        if len(V) > n:
            V = V[rng.choice(len(V), n, replace=False)]
        fn = tree_of(b).find_nearest
        d = np.array([fn(p)[3] for p in V.tolist()])
        out[tag] = {"n": len(d), "max": round(float(d.max()), 4), "p99.9": round(float(np.percentile(d, 99.9)), 4),
                    "mean": round(float(d.mean()), 5)}
    return out


def snap_z0(ob, tol=1e-4):
    """Vertices within tol of z 0 go to exactly 0 (bed plane)."""
    V = verts_of(ob)
    m = np.abs(V[:, 2]) < tol
    V[m, 2] = 0.0
    ob.data.vertices.foreach_set("co", V.astype(np.float32).ravel())
    ob.data.update()
    return int(m.sum())


def join_shells(name, outer, inner, collection):
    """M0 = outer shell + inner shell with reversed normals (no boolean: the
    chamber lies >= 2 mm inside the envelope)."""
    bm = bmesh.new()
    bm.from_mesh(outer.data)
    n1 = len(bm.faces)
    bm.from_mesh(inner.data)
    bm.faces.ensure_lookup_table()
    bmesh.ops.reverse_faces(bm, faces=[bm.faces[i] for i in range(n1, len(bm.faces))])
    remove_obj(name)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    return ob


def shells_overlap(a, b):
    ta, tb = tree_of(a), tree_of(b)
    return len(ta.overlap(tb))


# ================================================================== steps 1-3
def step_fields():
    g, f = BF.step_fields()
    return {"grid": list(g.n)}


def preview_env(name="ENV_preview"):
    g = FS.Grid()
    E = BF.load_arr("f_E")
    pts, flat, sizes = BF.vdb_mesh(g, E)
    ob = BF.obj_from_arrays(name, pts, flat, sizes, coll(BF.COLL_WORK), (0.2, 0.2, 0.2, 1))
    return {"faces": len(sizes)}


def dout_from_mesh(ob, g):
    """Exact outer distance field (negative inside) for mesh ob: OpenVDB level
    set, refined to exact point-to-mesh distance in the wall band."""
    import openvdb as vdb
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    pts = np.array([v.co[:] for v in bm.verts], np.float32)
    bm.verts.index_update()
    tris = np.array([[v.index for v in f.verts] for f in bm.faces], np.uint32)
    tree = BVHTree.FromBMesh(bm)
    bm.free()
    ls = vdb.FloatGrid.createLevelSetFromPolygons(
        pts, triangles=tris, transform=vdb.createLinearTransform(voxelSize=g.h),
        exBandWidth=6.0, inBandWidth=16.0)
    D = np.zeros(g.n, np.float32)
    ls.copyToArray(D, ijk=tuple(g.i0))
    idx = np.nonzero((D < 1.2) & (D > -4.6))
    xs, ys, zs = g.ax
    Pp = np.stack([xs[idx[0]], ys[idx[1]], zs[idx[2]]], 1).astype(np.float64)
    out = np.empty(len(Pp), np.float32)
    fn = tree.find_nearest
    for i, p in enumerate(Pp.tolist()):
        out[i] = fn(p)[3]
    sgn = np.sign(D[idx])
    sgn[sgn == 0] = 1.0
    diff = np.abs(sgn * out - D[idx])
    D[idx] = sgn * out
    return D, {"refined_voxels": int(len(out)), "vdb_err_max": round(float(diff.max()), 3),
               "vdb_err_p99.9": round(float(np.percentile(diff, 99.9)), 4)}


def step_outer():
    """Mesh E (0.5 grid) -> ENV_fine; decimate a copy -> ENV_outer; exact
    D_out from the DECIMATED mesh (so walls and skins refer to the final
    outer surface)."""
    t0 = time.time()
    g = FS.Grid()
    E = BF.load_arr("f_E")
    pts, flat, sizes = BF.vdb_mesh(g, E)
    fixed = BF.fix_islands(g, E, pts, flat, sizes, keep=1)
    if fixed:
        BF.save_arr("f_E", E)
        pts, flat, sizes = BF.vdb_mesh(g, E)
    fine = BF.obj_from_arrays("ENV_fine", pts, flat, sizes, coll(BF.COLL_WORK), (0.2, 0.2, 0.2, 1))
    fine.hide_set(True)
    rep = {"islands_fixed": fixed, "fine": BF.mesh_stats(fine)}
    dec = BF.dup(fine, "ENV_outer", coll(BF.COLL_WORK))
    rep["decimate"] = decimate(dec, target_tris=P.DEC_ENV_TRIS)
    rep["z0_snapped"] = snap_z0(dec)
    rep["dec"] = BF.mesh_stats(dec)
    rep["dec_crossing_pairs"] = crossings(dec)
    rep["volume_change_pct"] = round(100.0 * (rep["dec"]["volume_mm3"] - rep["fine"]["volume_mm3"]) /
                                     rep["fine"]["volume_mm3"], 5)
    rep["deviation"] = deviation(fine, dec)
    D, info = dout_from_mesh(dec, g)
    BF.save_arr("D_out", D)
    rep["D_out"] = info
    rep["secs"] = round(time.time() - t0, 1)
    log("step_outer v2: %s" % rep)
    return rep


def step_master():
    """Chamber field -> CHAMBER_fine -> decimated CHAMBER_void; M0 = ENV_outer
    + reversed CHAMBER_void."""
    t0 = time.time()
    g = FS.Grid()
    f = {k: BF.load_arr("f_" + k) for k in ("E", "pumpkin", "torso_alone", "head_alone")}
    D = BF.load_arr("D_out")
    C, parts, info = FS.chamber(g, f, D, log)
    BF.save_arr("C", C)
    for k, v in parts.items():
        BF.save_arr("C_" + k, v)
    del parts, f, D
    cp, cflat, csz = BF.vdb_mesh(g, C)
    fixed = BF.fix_islands(g, C, cp, cflat, csz, keep=1)
    if fixed:
        BF.save_arr("C", C)
        cp, cflat, csz = BF.vdb_mesh(g, C)
    chf = BF.obj_from_arrays("CHAMBER_fine", cp, cflat, csz, coll(BF.COLL_WORK), (0.9, 0.9, 0.2, 1))
    chf.hide_set(True)
    info["chamber_islands_fixed"] = fixed
    info["chamber_fine"] = BF.mesh_stats(chf)
    ch = BF.dup(chf, "CHAMBER_void", coll(BF.COLL_WORK))
    info["chamber_decimate"] = decimate(ch, target_tris=P.DEC_CHAMBER_TRIS)
    info["chamber_dec"] = BF.mesh_stats(ch)
    info["chamber_dec_crossing_pairs"] = crossings(ch)
    info["chamber_volume_change_pct"] = round(100.0 * (info["chamber_dec"]["volume_mm3"] -
                                                       info["chamber_fine"]["volume_mm3"]) /
                                              info["chamber_fine"]["volume_mm3"], 5)
    info["chamber_deviation"] = deviation(chf, ch)
    ch.hide_set(True)
    env = bpy.data.objects["ENV_outer"]
    info["env_chamber_overlap_pairs"] = shells_overlap(env, ch)
    m0 = join_shells("M0_master", env, ch, coll(BF.COLL_FIG))
    m0.color = (0.05, 0.05, 0.05, 1)
    info["master"] = BF.mesh_stats(m0)
    info["secs"] = round(time.time() - t0, 1)
    log("step_master v2: %s" % info)
    return info


def step_base_void():
    st, sv = BF.step_base_void()
    return {"M1": st, "void": sv}


# ================================================================== windows (v2)
WG = {
    "cat": {"windows": FS.CAT_WINDOWS, "inlays": FS.INLAYS, "wall": P.WALL_CAT,
            "x": (-36.0, 36.0), "z": (95.0, 134.0)},
    "pk": {"windows": FS.PK_WINDOWS, "inlays": (), "wall": P.WALL_PUMPKIN,
           "x": (-36.0, 36.0), "z": (25.0, 86.4)},
}


class DoutSampler:
    """Trilinear value / gradient of the cached D_out on a sub-block."""

    def __init__(self, lo, hi):
        g = FS.Grid()
        D = BF.load_arr("D_out")
        self.h = g.h
        self.i0 = []
        sl = []
        for d in range(3):
            a = max(0, int(math.floor(lo[d] / g.h)) - g.i0[d] - 2)
            b = min(g.n[d], int(math.ceil(hi[d] / g.h)) - g.i0[d] + 3)
            sl.append(slice(a, b))
            self.i0.append(g.i0[d] + a)
        self.D = np.ascontiguousarray(D[tuple(sl)]).astype(np.float32)
        del D
        gx, gy, gz = np.gradient(self.D, self.h)
        self.G = (gx.astype(np.float32), gy.astype(np.float32), gz.astype(np.float32))
        self.n = self.D.shape

    def _idx(self, a, d):
        f = np.asarray(a, np.float64) / self.h - self.i0[d]
        i = np.clip(np.floor(f).astype(np.int64), 0, self.n[d] - 2)
        return i, (f - i)

    def _interp(self, A, x, y, z):
        ix, fx = self._idx(x, 0)
        iy, fy = self._idx(y, 1)
        iz, fz = self._idx(z, 2)
        out = np.zeros(np.shape(ix), np.float64)
        for a in (0, 1):
            wx = fx if a else 1 - fx
            for b in (0, 1):
                wy = fy if b else 1 - fy
                for c in (0, 1):
                    wz = fz if c else 1 - fz
                    out += wx * wy * wz * A[ix + a, iy + b, iz + c]
        return out

    def value(self, x, y, z):
        return self._interp(self.D, x, y, z)

    def normal(self, x, y, z):
        n = np.stack([self._interp(G, x, y, z) for G in self.G], -1)
        return n / np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-9)


def ceiling_angle(phi_deg, n, t3):
    """Angle from vertical of a flank at angle phi (from the inward normal,
    toward t3) where it faces down; 0 where it faces up (a floor)."""
    ph = np.radians(phi_deg)
    nz = -np.cos(ph) * t3[..., 2] - np.sin(ph) * n[..., 2]      # air-side normal z
    return np.degrees(np.arcsin(np.clip(-nz, 0.0, 1.0)))


def surface_frame(tree, S, x, z, gx, gz):
    """Front surface point, smooth outward normal and in-surface directions
    (e3 along the outline, t3 away from the window) for outline samples."""
    y = np.full(len(x), np.nan)
    for i in range(len(x)):
        loc, nrm, idx, dist = tree.ray_cast(Vector((x[i], -150.0, z[i])), Vector((0, 1, 0)), 300.0)
        if loc is not None:
            y[i] = loc.y
    n = S.normal(x, y, z)
    e2x, e2z = -gz, gx
    dfe = -(n[:, 0] * e2x + n[:, 2] * e2z) / np.where(np.abs(n[:, 1]) > 0.05, n[:, 1], -0.05)
    e3 = np.stack([e2x, dfe, e2z], 1)
    e3 /= np.linalg.norm(e3, axis=1, keepdims=True)
    t3 = np.cross(n, e3)
    t3 /= np.linalg.norm(t3, axis=1, keepdims=True)
    flip = (t3[:, 0] * gx + t3[:, 2] * gz) < 0
    t3[flip] *= -1
    return y, n, e3, t3


def pocket_sdf2(w, px, pz):
    """2D SDF of a window's POCKET outline: the outer loop only (spec v1.2:
    the cat-eye pocket is the whole dia 17.5 disc, pupil included)."""
    return FS.sd_polygon2(px, pz, FS.outlines()[w][0])


def pupil_sdf2(px, pz):
    d = None
    for w in ("cat_pupil_L", "cat_pupil_R"):
        dd = FS.outline_sdf2(w, px, pz)
        d = dd if d is None else np.minimum(d, dd)
    return d


def flank_table(group, step=0.25):
    """Per pocket-outline sample: x, z, phi (deg), ceiling angle alpha (deg)."""
    G = WG[group]
    tree = tree_of(bpy.data.objects["ENV_outer"])
    lo = (G["x"][0] - 2, -80.0, G["z"][0] - 2)
    hi = (G["x"][1] + 2, 40.0, G["z"][1] + 2)
    S = DoutSampler(lo, hi)
    rows = []
    rep = {}
    phis = np.arange(0.0, 60.01, 0.5)
    for w in G["windows"]:
        for li, loop in enumerate(FS.outlines()[w][:1]):
            hole = False
            L = np.asarray(loop, float)
            cl = np.vstack([L, L[:1]])
            seg = np.hypot(*np.diff(cl, axis=0).T)
            cum = np.concatenate([[0.0], np.cumsum(seg)])
            s = np.arange(0.0, cum[-1], step)
            x = np.interp(s, cum, cl[:, 0])
            z = np.interp(s, cum, cl[:, 1])
            h = 0.02
            gx = (pocket_sdf2(w, x + h, z) - pocket_sdf2(w, x - h, z)) / (2 * h)
            gz = (pocket_sdf2(w, x, z + h) - pocket_sdf2(w, x, z - h)) / (2 * h)
            gn = np.hypot(gx, gz)
            gx, gz = gx / gn, gz / gn
            y, n, e3, t3 = surface_frame(tree, S, x, z, gx, gz)
            pmax = P.WINDOW_FLANK_MAX_DEG
            cand = phis[phis <= pmax + 1e-9]
            A = np.stack([ceiling_angle(p, n, t3) for p in cand], 1)          # (samples, cand)
            ok55 = A <= P.POCKET_CEIL_PREF_DEG
            ok60 = A <= P.POCKET_CEIL_MAX_DEG
            best = np.empty(len(x))
            for i in range(len(x)):
                if ok55[i].any():
                    best[i] = cand[np.nonzero(ok55[i])[0].max()]
                elif ok60[i].any():
                    best[i] = cand[np.nonzero(ok60[i])[0].max()]
                else:
                    best[i] = cand[np.argmin(A[i])]
            # smooth along the (closed) loop, then snap back into the feasible set
            k = max(1, int(round(P.FLANK_SMOOTH_MM / step)))
            ext = np.concatenate([best[-k:], best, best[:k]])
            sm = np.convolve(ext, np.ones(2 * k + 1) / (2 * k + 1), mode="valid")
            fin = np.empty(len(x))
            alpha = np.empty(len(x))
            for i in range(len(x)):
                a_sm = float(ceiling_angle(sm[i], n[i], t3[i]))
                a_best = float(ceiling_angle(best[i], n[i], t3[i]))
                if a_sm <= max(P.POCKET_CEIL_MAX_DEG, a_best) + 0.25:
                    fin[i], alpha[i] = sm[i], a_sm
                else:
                    feas = cand[ok60[i]] if ok60[i].any() else np.array([best[i]])
                    j = np.argmin(np.abs(feas - sm[i]))
                    fin[i] = feas[j]
                    alpha[i] = float(ceiling_angle(fin[i], n[i], t3[i]))
            for i in range(len(x)):
                rows.append((x[i], z[i], fin[i], alpha[i], float(hole), y[i], n[i, 0], n[i, 1], n[i, 2]))
            key = "%s%s" % (w, "_hole" if hole else "")
            over = alpha > P.POCKET_CEIL_MAX_DEG
            rep[key] = {"samples": len(x), "phi_min_max": [round(float(fin.min()), 1), round(float(fin.max()), 1)],
                        "alpha_max": round(float(alpha.max()), 1),
                        "outline_len_mm_alpha_gt55": round(float((alpha > P.POCKET_CEIL_PREF_DEG).sum() * step), 2),
                        "outline_len_mm_alpha_gt60": round(float(over.sum() * step), 2),
                        "gt60_xz": [[round(float(a), 1), round(float(b), 1)] for a, b in
                                    zip(x[over][::8], z[over][::8])]}
    T = np.array(rows)
    np.save(os.path.join(CACHE, "flank_%s.npy" % group), T)
    log("flank table %s: %s" % (group, rep))
    return rep


def column_grid(group):
    """Per-column data on the fine (x, z) grid: outer surface y, smooth normal,
    projected outline distance + gradient, surface stretch, chamber depth along
    the normal, pocket back limit, flank angle.  Cached as cols2_<group>.npz."""
    t0 = time.time()
    G = WG[group]
    h = P.FINE_H
    xs = np.arange(G["x"][0], G["x"][1] + 1e-9, h)
    zs = np.arange(G["z"][0], G["z"][1] + 1e-9, h)
    XX, ZZ = np.meshgrid(xs, zs, indexing="ij")
    dwin = np.full(XX.shape, 1e3)          # yellow (window) outline, pupil holes excluded
    dpk = np.full(XX.shape, 1e3)           # pocket outline (outer loops only)
    for w in G["windows"]:
        dwin = np.minimum(dwin, FS.outline_sdf2(w, XX, ZZ))
        dpk = np.minimum(dpk, pocket_sdf2(w, XX, ZZ))
    dpup = pupil_sdf2(XX, ZZ) if group == "cat" else np.full(XX.shape, 1e3)
    dinl = np.full(XX.shape, 1e3)
    for w in G["inlays"]:
        dinl = np.minimum(dinl, FS.outline_sdf2(w, XX, ZZ))
    need = (dpk <= P.WINDOW_BAND_MM + 3.0) | (dinl <= 5.0)
    env = bpy.data.objects["ENV_outer"]
    t_out = tree_of(env)
    t_ch = tree_of(bpy.data.objects["CHAMBER_void"])
    S = DoutSampler((G["x"][0] - 2, -80.0, G["z"][0] - 2), (G["x"][1] + 2, 40.0, G["z"][1] + 2))
    y_out = np.full(XX.shape, np.nan)
    ii, kk = np.nonzero(need)
    d = Vector((0.0, 1.0, 0.0))
    for a, b in zip(ii.tolist(), kk.tolist()):
        loc, nrm, idx, dist = t_out.ray_cast(Vector((float(xs[a]), -150.0, float(zs[b]))), d, 300.0)
        if loc is not None:
            y_out[a, b] = loc.y
    fin = np.isfinite(y_out)
    N = np.zeros(XX.shape + (3,))
    N[fin] = S.normal(XX[fin], y_out[fin], ZZ[fin])
    # chamber depth along the inward normal
    v_ch = np.full(XX.shape, np.nan)
    fi, fk = np.nonzero(fin & (dpk <= P.WINDOW_BAND_MM + 3.0))
    for a, b in zip(fi.tolist(), fk.tolist()):
        n = Vector(N[a, b])
        o = Vector((float(xs[a]), float(y_out[a, b]), float(zs[b]))) - n * 0.01
        loc, nrm, idx, dist = t_ch.ray_cast(o, -n, 30.0)
        v_ch[a, b] = (dist + 0.01) if loc is not None else 30.0
    # nearest pocket column's chamber depth (pocket back limit)
    ins = np.nonzero((dpk <= 0) & np.isfinite(v_ch))
    kd = KDTree(len(ins[0]))
    for m, (a, b) in enumerate(zip(ins[0].tolist(), ins[1].tolist())):
        kd.insert((float(xs[a]), float(zs[b]), 0.0), m)
    kd.balance()
    v_near = np.full(XX.shape, np.nan)
    for a, b in zip(fi.tolist(), fk.tolist()):
        co, m, dd = kd.find((float(xs[a]), float(zs[b]), 0.0))
        v_near[a, b] = v_ch[ins[0][m], ins[1][m]]
    v_lim = np.where(dpk <= 0, v_ch, np.fmin(v_ch, v_near)) + P.WINDOW_BACK_OVERLAP
    # surface stretch of the projected distance, for windows and inlays
    def stretch_of(Fd):
        gX, gZ = np.gradient(Fd, h)
        gn = np.maximum(np.hypot(gX, gZ), 1e-9)
        gX, gZ = gX / gn, gZ / gn
        ny = np.where(np.abs(N[..., 1]) > 0.05, N[..., 1], -0.05)
        dfg = -(N[..., 0] * gX + N[..., 2] * gZ) / ny
        return np.sqrt(1.0 + dfg * dfg)
    st_w = np.where(fin, stretch_of(np.clip(dwin, -50, 50)), 1.0)
    st_p = np.where(fin, stretch_of(np.clip(dpk, -50, 50)), 1.0)
    st_u = np.where(fin, stretch_of(np.clip(dpup, -50, 50)), 1.0)
    st_i = np.where(fin, stretch_of(np.clip(dinl, -50, 50)), 1.0)
    # flank angle of the nearest outline sample
    T = np.load(os.path.join(CACHE, "flank_%s.npy" % group))
    kd2 = KDTree(len(T))
    for m, r in enumerate(T):
        kd2.insert((float(r[0]), float(r[1]), 0.0), m)
    kd2.balance()
    phi = np.full(XX.shape, float(P.WINDOW_FLANK_MAX_DEG))
    for a, b in zip(ii.tolist(), kk.tolist()):
        co, m, dd = kd2.find((float(xs[a]), float(zs[b]), 0.0))
        phi[a, b] = T[m, 2]
    cd = {"xs": xs, "zs": zs, "dwin": dwin, "dpk": dpk, "dpup": dpup, "dinl": dinl, "y_out": y_out, "N": N,
          "v_ch": v_ch, "v_near": v_near, "v_lim": v_lim, "st_w": st_w, "st_p": st_p, "st_u": st_u,
          "st_i": st_i, "phi": phi}
    np.savez(os.path.join(CACHE, "cols2_%s.npz" % group), **cd)
    ok = np.isfinite(v_ch) & (dpk <= 0)
    rep = {"columns": int(need.sum()), "window_columns": int(ok.sum()),
           "v_ch_window_min_med_max": [round(float(np.nanmin(v_ch[ok])), 3), round(float(np.nanmedian(v_ch[ok])), 3),
                                       round(float(np.nanmax(v_ch[ok])), 3)],
           "stretch_window_max": round(float(st_p[ok].max()), 3), "secs": round(time.time() - t0, 1)}
    log("column_grid %s: %s" % (group, rep))
    return rep


def _bilinear(A, xs, zs, x, z):
    h = xs[1] - xs[0]
    fx = (x - xs[0]) / h
    fz = (z - zs[0]) / h
    i = np.clip(np.floor(fx).astype(np.int64), 0, len(xs) - 2)
    k = np.clip(np.floor(fz).astype(np.int64), 0, len(zs) - 2)
    tx = np.clip(fx - i, 0, 1)
    tz = np.clip(fz - k, 0, 1)
    return ((1 - tx) * (1 - tz) * A[i, k] + tx * (1 - tz) * A[i + 1, k] +
            (1 - tx) * tz * A[i, k + 1] + tx * tz * A[i + 1, k + 1])


def _nearest(A, xs, zs, x, z):
    h = xs[1] - xs[0]
    i = np.clip(np.rint((x - xs[0]) / h).astype(np.int64), 0, len(xs) - 1)
    k = np.clip(np.rint((z - zs[0]) / h).astype(np.int64), 0, len(zs) - 1)
    return A[i, k]


def window_fields(group, exact_band=None):
    """Pocket cutter / yellow zone / pink zone fields on the local 0.2 mm grid
    in surface-normal coordinates, meshed with OpenVDB (BEAUTY tris)."""
    t0 = time.time()
    G = WG[group]
    cd = dict(np.load(os.path.join(CACHE, "cols2_%s.npz" % group)))
    xs, zs = cd["xs"], cd["zs"]
    h = float(xs[1] - xs[0])
    skin = P.SKIN_T
    eps = P.WINDOW_EPS_V2
    # fill the column arrays outside their valid region with harmless values
    big = 1e3
    dwin = cd["dwin"]
    dpk = cd["dpk"]
    dpup = cd["dpup"]
    dinl = cd["dinl"]
    fin = np.isfinite(cd["y_out"])
    v_lim = np.where(np.isfinite(cd["v_lim"]), cd["v_lim"], -big)
    st_w, st_p, st_u, st_i = cd["st_w"], cd["st_p"], cd["st_u"], cd["st_i"]
    phi = cd["phi"]
    boss_t = min(float(P.PUPIL_BOSS_T), P.PUPIL_BOSS_T_MAX) if group == "cat" else 0.0
    tb = math.tan(math.radians(P.PUPIL_BOSS_FLANK_DEG))
    rel = fin & ((dpk <= P.WINDOW_BAND_MM + 2.0) | (dinl <= 4.0))
    vmax = float(np.nanmax(np.where(rel & (dpk <= P.WINDOW_BAND_MM + 2.0), v_lim, np.nan)))
    vmax = min(vmax, 16.0)
    ylo = float(np.nanmin(np.where(rel, cd["y_out"], np.nan))) - P.INLAY_FRONT - 1.2
    yhi = float(np.nanmax(np.where(rel, cd["y_out"], np.nan))) + vmax / 0.25 + 1.0
    yhi = min(yhi, float(np.nanmax(np.where(rel, cd["y_out"], np.nan))) + 25.0)
    ys = np.arange(math.floor(ylo / h) * h, yhi + h, h)
    S = DoutSampler((xs[0], ys[0], zs[0]), (xs[-1], ys[-1], zs[-1]))
    tree = tree_of(bpy.data.objects["ENV_outer"])
    fn = tree.find_nearest
    shape = (len(xs), len(ys), len(zs))
    FP = np.full(shape, FS.FAR, np.float32)
    FY = np.full(shape, FS.FAR, np.float32)
    FK = np.full(shape, FS.FAR, np.float32) if G["inlays"] else None
    n_sel = 0
    n_exact = 0
    Zc = zs[None, :]
    for i0 in range(0, len(xs), 12):
        i1 = min(len(xs), i0 + 12)
        relc = rel[i0:i1]                                     # (nx, nz)
        if not relc.any():
            continue
        X, Yv, Z = np.meshgrid(xs[i0:i1], ys, zs, indexing="ij")
        m = np.broadcast_to(relc[:, None, :], X.shape)
        x, y, z = X[m], Yv[m], Z[m]
        v = -S.value(x, y, z)
        keep = (v >= -2.2) & (v <= vmax + 1.0)
        idx_all = np.nonzero(m.ravel())[0][keep]
        x, y, z, v = x[keep], y[keep], z[keep], v[keep]
        if len(x) == 0:
            continue
        nrm = S.normal(x, y, z)
        q = np.stack([x, y, z], 1) + v[:, None] * nrm       # foot point on the outer surface
        # exact distance and foot point for EVERY evaluated voxel (a switch
        # between approximate and exact foot points left sub-0.05 mm ledges
        # in the zone walls, i.e. hairline cracks in the tiling - v2 test)
        if exact_band is None or exact_band >= 99:
            ex = np.ones(len(x), bool)
        else:
            dq = _bilinear(np.clip(dpk, -50, 50), xs, zs, q[:, 0], q[:, 2])
            iq = _bilinear(np.clip(dinl, -50, 50), xs, zs, q[:, 0], q[:, 2])
            ex = ((np.abs(v - skin) < exact_band) & (dq < 1.5)) | ((np.abs(v - P.INLAY_DEPTH) < exact_band) & (iq < 1.5))
        if ex.any():
            ei = np.nonzero(ex)[0]
            va = v.copy()
            for j in ei.tolist():
                pj = (x[j], y[j], z[j])
                loc, fnrm, fidx, dist = fn(pj)
                if abs(va[j]) > 0.05:
                    sg = 1.0 if va[j] > 0 else -1.0
                else:
                    w = Vector(pj) - loc
                    sg = 1.0 if w.dot(fnrm) < 0 else -1.0    # behind the face -> inside (v > 0)
                v[j] = sg * dist
                q[j] = loc[:]
            n_exact += len(ei)
        qx, qz = q[:, 0], q[:, 2]
        s_p = _bilinear(np.clip(dpk, -50, 50), xs, zs, qx, qz) * _bilinear(st_p, xs, zs, qx, qz)
        s_w = _bilinear(np.clip(dwin, -50, 50), xs, zs, qx, qz) * _bilinear(st_w, xs, zs, qx, qz)
        ph = np.radians(_nearest(phi, xs, zs, qx, qz))
        vl = _nearest(v_lim, xs, zs, qx, qz)
        fp = np.maximum(np.maximum(skin - v, (s_p - eps - (v - skin) * np.tan(ph)) * np.cos(ph)), v - vl)
        if boss_t > 0:
            # optional black backing boss on the inner face of each pupil skin:
            # dia 8 at the skin, narrowing inward at PUPIL_BOSS_FLANK_DEG, thickness boss_t
            s_u = _bilinear(np.clip(dpup, -50, 50), xs, zs, qx, qz) * _bilinear(st_u, xs, zs, qx, qz)
            fb = np.maximum(np.maximum(s_u + (v - skin) * tb, skin - 0.05 - v), v - (skin + boss_t))
            fp = np.maximum(fp, -fb)
        fy = np.maximum(np.maximum(s_w, v - (skin + P.YELLOW_BACK)), -v - P.INLAY_FRONT)
        sub = (i1 - i0, len(ys), len(zs))
        FPs = FP[i0:i1].reshape(-1)
        FYs = FY[i0:i1].reshape(-1)
        FPs[idx_all] = np.clip(fp, -FS.FAR, FS.FAR)
        FYs[idx_all] = np.clip(fy, -FS.FAR, FS.FAR)
        FP[i0:i1] = FPs.reshape(sub)
        FY[i0:i1] = FYs.reshape(sub)
        if FK is not None:
            iq = _bilinear(np.clip(dinl, -50, 50), xs, zs, q[:, 0], q[:, 2])
            s_i = iq * _bilinear(st_i, xs, zs, q[:, 0], q[:, 2])
            fk = np.maximum(np.maximum(s_i, v - P.INLAY_DEPTH), -v - P.INLAY_FRONT)
            FKs = FK[i0:i1].reshape(-1)
            FKs[idx_all] = np.clip(fk, -FS.FAR, FS.FAR)
            FK[i0:i1] = FKs.reshape(sub)
        n_sel += len(x)
    x0, y0, z0 = float(xs[0]), float(ys[0]), float(zs[0])
    out = {"grid": list(shape), "voxels_evaluated": n_sel, "exact_voxels": n_exact, "vmax": round(vmax, 2)}
    cut = BF.local_mesh(FP, x0, y0, z0, h, "CUT_pockets_" + group, coll(BF.COLL_WORK), (1, 0.3, 0.3, 1))
    del FP
    yz = BF.local_mesh(FY, x0, y0, z0, h, "ZONE_yellow_" + group, coll(BF.COLL_WORK), (1, 0.9, 0.1, 1))
    del FY
    objs = [cut, yz]
    if FK is not None:
        pz = BF.local_mesh(FK, x0, y0, z0, h, "ZONE_pink", coll(BF.COLL_WORK), (1, 0.45, 0.65, 1))
        objs.append(pz)
        del FK
    for ob in objs:
        out[ob.name] = {"dropped_specks": BF.drop_small_shells(ob), "stats": BF.mesh_stats(ob)}
    out["secs"] = round(time.time() - t0, 1)
    log("window_fields %s: %s" % (group, out))
    return out


def decimate_inputs(names, ratio):
    rep = {}
    for nm in names:
        ob = bpy.data.objects[nm]
        v0 = BF.mesh_stats(ob)["volume_mm3"]
        d = decimate(ob, ratio=ratio)
        st = BF.mesh_stats(ob)
        d.update({"vol_before": v0, "vol_after": st["volume_mm3"], "nonmanifold": st["nonmanifold_edges"],
                  "boundary": st["boundary_edges"], "shells": st["shells"], "crossing_pairs": crossings(ob)})
        rep[nm] = d
    log("decimate_inputs: %s" % rep)
    return rep


def step_windows():
    return BF.step_windows()


def join_yellow():
    remove_obj("ZONE_yellow")
    yc, yp = bpy.data.objects["ZONE_yellow_cat"], bpy.data.objects["ZONE_yellow_pk"]
    y = yc.copy()
    y.data = yc.data.copy()
    y.name = "ZONE_yellow"
    coll(BF.COLL_WORK).objects.link(y)
    bm = bmesh.new()
    bm.from_mesh(y.data)
    bm.from_mesh(yp.data)
    bm.to_mesh(y.data)
    bm.free()
    return BF.mesh_stats(y)


def clean_micro(names=("black", "orange", "yellow", "green", "pink"), dist=2e-5, apply=True, dissolve=False):
    """Remove the EXACT boolean's zero-area micro-triangles: merge vertices
    closer than `dist` (float32 would weld them anyway on export) and dissolve
    the resulting degenerate edges/faces.  Moves no vertex by more than dist.
    A part is only replaced if it stays a closed 2-manifold with unchanged
    shell count and volume (else it is left as it was and reported)."""
    rep = {}
    for n in names:
        ob = bpy.data.objects[n]
        st0 = BF.mesh_stats(ob)
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
        v0, f0 = len(bm.verts), len(bm.faces)
        zero0 = sum(1 for f in bm.faces if f.calc_area() < 1e-10)
        bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=dist)
        if dissolve and any(f.calc_area() < 1e-10 for f in bm.faces):
            bmesh.ops.dissolve_degenerate(bm, dist=dist, edges=bm.edges[:])
        bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
        zero1 = sum(1 for f in bm.faces if f.calc_area() < 1e-10)
        me = bpy.data.meshes.new(n + "_clean_tmp")
        bm.to_mesh(me)
        bm.free()
        tmp = bpy.data.objects.new(n + "_clean_tmp", me)
        coll(BF.COLL_WORK).objects.link(tmp)
        st1 = BF.mesh_stats(tmp)
        cr = crossings(tmp)
        ok = (st1["nonmanifold_edges"] == 0 and st1["boundary_edges"] == 0 and st1["shells"] == st0["shells"]
              and abs(st1["volume_mm3"] - st0["volume_mm3"]) < 0.05 and cr == 0)
        rep[n] = {"verts": [v0, len(me.vertices)], "tris": [f0, len(me.polygons)], "zero_area": [zero0, zero1],
                  "nonmanifold": st1["nonmanifold_edges"], "boundary": st1["boundary_edges"], "shells": st1["shells"],
                  "vol": [st0["volume_mm3"], st1["volume_mm3"]], "crossings": cr, "accepted": bool(ok and apply)}
        if ok and apply:
            old = ob.data
            ob.data = me
            me.name = old.name
            bpy.data.meshes.remove(old)
            bpy.data.objects.remove(tmp, do_unlink=True)
        else:
            bpy.data.objects.remove(tmp, do_unlink=True)
            bpy.data.meshes.remove(me)
    log("clean_micro: %s" % rep)
    return rep


def union_check(names=("black", "orange", "yellow", "green", "pink")):
    """Tiling test on the triangulated parts: weld all vertices (exact
    coordinates), drop every triangle that has an exactly coincident,
    opposite triangle in ANOTHER part (a shared interface), and check that
    what is left (the union's boundary) is a closed 2-manifold whose volume
    equals the sum of the part volumes.  Unmatched interface triangles
    (gaps, overlaps or non-conforming seams) would show as open or
    non-manifold edges."""
    import export_figure_v2 as EX
    importlib.reload(EX)
    parts, src = [], []
    for n in names:
        Vp, Fp, Sp, polys = EX.tri_arrays(bpy.data.objects[n], with_src=True)
        parts.append((n, Vp, Fp))
        src.append((Sp, polys))
    V, F, lab, n_int = EX.exterior_faces(parts, src)
    e = np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])
    und = np.sort(e, axis=1)
    key = und[:, 0] * len(V) + und[:, 1]
    _, cnt = np.unique(key, return_counts=True)
    a, b, c = V[F[:, 0]].astype(np.float64), V[F[:, 1]].astype(np.float64), V[F[:, 2]].astype(np.float64)
    vol = float(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6.0)
    psum = 0.0
    for n, Vp, Fp in parts:
        a, b, c = Vp[Fp[:, 0]].astype(np.float64), Vp[Fp[:, 1]].astype(np.float64), Vp[Fp[:, 2]].astype(np.float64)
        psum += float(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6.0)
    return {"union_tris": int(len(F)), "interface_tris_removed": n_int,
            "edges_used_once": int((cnt == 1).sum()), "edges_used_gt2": int((cnt > 2).sum()),
            "union_volume": round(vol, 3), "sum_part_volumes": round(psum, 3)}


def side_of(tree, p):
    """Signed distance of point p to a closed mesh via its nearest face
    (negative inside)."""
    loc, n, idx, d = tree.find_nearest(p)
    if loc is None:
        return 1e9
    return d if (p - loc).dot(n) >= 0 else -d


def gap_probe(n_per_part=4000, eps=0.004, seed=11):
    """Tiling probe at internal colour boundaries: for sampled boundary faces
    of each part (not on the outer envelope, not on the chamber/pocket
    surface), the point eps inside must be in that part only and the point
    eps outside in exactly one other part (nearest-face sign test)."""
    import verify_figure as VF
    names = ("black", "orange", "yellow", "green", "pink")
    trees = {n: tree_of(bpy.data.objects[n]) for n in names}
    to = tree_of(bpy.data.objects["ENV_outer"])
    it = VF.inner_faces_tree()[0]
    rng = np.random.default_rng(seed)
    rep = {}
    for A in names:
        cen, nrm, area = VF.face_arrays(A)
        ok = area > 1e-9
        idx = rng.choice(np.nonzero(ok)[0], size=min(int(ok.sum()), 40 * n_per_part), replace=False,
                         p=area[ok] / area[ok].sum())
        k = 0
        bad = []
        for i in idx:
            c = Vector(cen[i])
            if to.find_nearest(c)[3] <= 0.01 or it.find_nearest(c)[3] <= 0.01:
                continue
            k += 1
            if k > n_per_part:
                break
            nv = Vector(nrm[i]).normalized()
            pin, pout = c - nv * eps, c + nv * eps

            def owners(p):
                res = []
                for n in names:
                    loc, fn_, idx_, d = trees[n].find_nearest(p)
                    if d < 0.05:
                        if (p - loc).dot(fn_) < 0:
                            res.append(n)
                    elif VF.inside(n, p):
                        res.append(n)
                return res
            ins = owners(pin)
            outs = owners(pout)
            if ins != [A] or len(outs) != 1 or A in outs:
                bad.append([[round(v, 3) for v in c], ins, outs])
        rep[A] = {"tested": min(k, n_per_part), "bad": len(bad), "examples": bad[:5]}
    return rep


def step_zones():
    return BF.step_zones()


PART_OPS = {
    "black": [('DIFFERENCE', "ZONE_orange"), ('DIFFERENCE', "ZONE_green"),
              ('DIFFERENCE', "ZONE_yellow"), ('DIFFERENCE', "ZONE_pink")],
    "orange": [('INTERSECT', "ZONE_orange"), ('DIFFERENCE', "ZONE_green"), ('DIFFERENCE', "ZONE_yellow")],
    "yellow": [('INTERSECT', "ZONE_yellow")],
    "green": [('INTERSECT', "ZONE_green")],
    "pink": [('INTERSECT', "ZONE_pink")],
}


def step_part(name, fix=False):
    m2 = bpy.data.objects["M2_windows"]
    col = P.hex_to_rgba(P.COLORS[name])
    ob, rec = BF.boolean_seq(m2, name, PART_OPS[name], col)
    fx = BF.fix_crossings(ob) if fix else None
    st = BF.mesh_stats(ob)
    out = {"ops": rec, "fix_crossings": fx, "final": st}
    log("part %s: %s" % (name, out))
    return out


def fix_crossings_synced(names=("black", "orange", "yellow", "green", "pink"), max_iter=8,
                         passive=(), project_to="M2_windows"):
    """Relax micro-folds (crossing triangle pairs on boolean seams) WITHOUT
    breaking the tiling or the outer/inner surfaces: every vertex that
    coincides with vertices of other parts (shared colour boundary) moves
    together with them, and a vertex that lies on the master's surface (outer
    envelope, chamber, pockets) is projected back onto that surface after the
    move, so it only slides tangentially and the union of the parts stays
    exactly the master.  Laplacian 0.5 of the crossing triangles' vertices
    only; topology never changes."""
    tm = tree_of(bpy.data.objects[project_to]) if project_to else None
    bms = {}
    for n in tuple(names) + tuple(passive):
        bm = bmesh.new()
        bm.from_mesh(bpy.data.objects[n].data)
        bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
        bm.verts.ensure_lookup_table()
        bm.faces.ensure_lookup_table()
        bms[n] = bm
    # coincidence groups over all parts + passive meshes (exact positions, 1e-6 rounding)
    keys, owners = [], []
    for n in tuple(names) + tuple(passive):
        for v in bms[n].verts:
            keys.append(tuple(np.round(np.array(v.co[:], np.float64) / 1e-6).astype(np.int64)))
            owners.append((n, v.index))
    group = {}
    for k, o in zip(keys, owners):
        group.setdefault(k, []).append(o)
    member = {}
    for k, lst in group.items():
        if len(lst) > 1:
            for o in lst:
                member[o] = lst
    rep = {n: {"before": len(BF.crossing_pairs(bms[n]))} for n in names}
    maxmove = 0.0
    shared_moves = 0
    projected = 0
    for it in range(max_iter):
        moved = False
        for n in names:
            bm = bms[n]
            bm.faces.ensure_lookup_table()
            cr = BF.crossing_pairs(bm)
            if not cr:
                continue
            moved = True
            vs = {v for a, b in cr for fi in (a, b) for v in bm.faces[fi].verts}
            newpos = {}
            for v in vs:
                nb = [e.other_vert(v).co for e in v.link_edges]
                avg = sum(nb, Vector()) / len(nb)
                p = v.co + 0.5 * (avg - v.co)
                if tm is not None and tm.find_nearest(v.co)[3] < 1e-5:
                    p = tm.find_nearest(p)[0].copy()          # stay on the master surface
                    projected += 1
                newpos[v] = p
            for v, p in newpos.items():
                maxmove = max(maxmove, (p - v.co).length)
                for (m, idx) in member.get((n, v.index), [(n, v.index)]):
                    bms[m].verts[idx].co = p.copy()
                    if m != n:
                        shared_moves += 1
        if not moved:
            break
    for n in names:
        rep[n]["after"] = len(BF.crossing_pairs(bms[n]))
    for n in tuple(passive):
        rep[n] = {"after": len(BF.crossing_pairs(bms[n]))}
    for n in tuple(names) + tuple(passive):
        bms[n].to_mesh(bpy.data.objects[n].data)
        bpy.data.objects[n].data.update()
        bms[n].free()
    rep["iterations"] = it + 1
    rep["max_vertex_move_mm"] = round(maxmove, 5)
    rep["shared_vertex_moves"] = shared_moves
    rep["projected_to_master_surface"] = projected
    rep["coincidence_groups"] = sum(1 for lst in group.values() if len(lst) > 1)
    log("fix_crossings_synced: %s" % rep)
    return rep
