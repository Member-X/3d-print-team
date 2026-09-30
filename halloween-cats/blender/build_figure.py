"""Stage-2 build of the "Pumpkin Hug" figure.  Run inside Blender:

    import sys, importlib
    sys.path.insert(0, r"H:/ClaudeStuff/3d-print-team/halloween-cats/blender")
    import build_figure as BF; importlib.reload(BF)
    BF.step_fields()      # implicit fields -> envelope E (cached .npy)
    BF.step_outer()       # mesh E, exact outer distance D_out
    BF.step_master()      # chamber C, master shell M0 (outer + chamber surfaces)
    BF.step_base_void()   # EXACT boolean: stage-1 pocket/tabs/arms/tunnel/plenum
    BF.step_windows()     # window pocket cutters, EXACT boolean
    BF.step_parts()       # colour zones, 5 parts by EXACT booleans
Every step reads the previous step's cache / objects, so a revision is a
re-run of the steps downstream of the changed parameter.
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

HERE = r"H:\ClaudeStuff\3d-print-team\halloween-cats\blender"
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import params as P            # noqa: E402
importlib.reload(P)           # reload in dependency order (Blender caches modules)
import figure_shapes as FS    # noqa: E402
importlib.reload(FS)
import build_test_parts as B  # noqa: E402  (stage-1 builders, reused unchanged)
importlib.reload(B)

CACHE = r"C:\Users\steve\AppData\Local\Temp\claude\H--ClaudeStuff-3d-print-team\803b752c-0c19-4c39-a372-657e0ca1ec54\scratchpad\cache"
BLEND = os.path.join(HERE, "halloween-cat.blend")
VERSIONS = os.path.join(HERE, "versions")
COLL_FIG = "FIGURE"
COLL_PARTS = "FIGURE_PARTS"
COLL_WORK = "WORK_temp"
COLL_REF = B.COLL_REF
LOG = []


def log(msg):
    s = "[%s] %s" % (time.strftime("%H:%M:%S"), msg)
    LOG.append(s)
    print(s)


def cpath(name):
    os.makedirs(CACHE, exist_ok=True)
    return os.path.join(CACHE, name + ".npy")


def save_arr(name, a):
    np.save(cpath(name), a)


def load_arr(name):
    return np.load(cpath(name))


# ------------------------------------------------------------------ blender helpers
def coll(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def remove_obj(name):
    B.remove_obj(name)


def obj_from_arrays(name, pts, faces_flat, face_sizes, collection, color=None):
    """Mesh object from numpy arrays (pts (N,3); faces as flat index list +
    per-face vertex counts)."""
    remove_obj(name)
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(pts))
    me.vertices.foreach_set("co", np.ascontiguousarray(pts, np.float32).ravel())
    me.loops.add(len(faces_flat))
    me.loops.foreach_set("vertex_index", np.ascontiguousarray(faces_flat, np.int32))
    starts = np.concatenate([[0], np.cumsum(face_sizes)[:-1]]).astype(np.int32)
    me.polygons.add(len(face_sizes))
    me.polygons.foreach_set("loop_start", starts)
    me.update(calc_edges=True)
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    if color is not None:
        ob.color = color
    return ob


def obj_from_quads(name, pts, quads, collection, color=None):
    q = np.asarray(quads, np.int64)
    return obj_from_arrays(name, pts, q.ravel(), np.full(len(q), 4, np.int32), collection, color)


def mesh_arrays(ob):
    me = ob.data
    n = len(me.vertices)
    co = np.empty(n * 3, np.float32)
    me.vertices.foreach_get("co", co)
    lt = np.empty(len(me.polygons), np.int32)
    me.polygons.foreach_get("loop_total", lt)
    vi = np.empty(len(me.loops), np.int32)
    me.loops.foreach_get("vertex_index", vi)
    return co.reshape(-1, 3), vi, lt


def tri_arrays(ob):
    """Triangulated copy of an object's mesh as (verts (N,3), tris (M,3))."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    v = np.array([vv.co[:] for vv in bm.verts], np.float64)
    bm.verts.index_update()
    t = np.array([[vv.index for vv in f.verts] for f in bm.faces], np.int64)
    bm.free()
    return v, t


def quads_to_tris(pts, quads):
    """Split every (generally non-planar) quad along the diagonal whose two
    triangles are the most coplanar.  Keeps later EXACT booleans free of
    warped faces, whose re-triangulation otherwise folds (self-intersects)."""
    q = np.asarray(quads, np.int64)
    P_ = np.asarray(pts, np.float64)
    a, b, c, d = (P_[q[:, i]] for i in range(4))

    def cosn(u, v):
        nu = np.linalg.norm(u, axis=1) + 1e-30
        nv = np.linalg.norm(v, axis=1) + 1e-30
        return np.einsum("ij,ij->i", u, v) / (nu * nv)
    c1 = cosn(np.cross(b - a, c - a), np.cross(c - a, d - a))       # diagonal a-c
    c2 = cosn(np.cross(b - a, d - a), np.cross(c - b, d - b))       # diagonal b-d
    use1 = c1 >= c2
    t1 = np.where(use1[:, None], q[:, [0, 1, 2]], q[:, [0, 1, 3]])
    t2 = np.where(use1[:, None], q[:, [0, 2, 3]], q[:, [1, 2, 3]])
    tris = np.empty((2 * len(q), 3), np.int64)
    tris[0::2] = t1
    tris[1::2] = t2
    return tris


def beauty_tris(pts, quads):
    """Triangulate OpenVDB quads with Blender's BEAUTY rule (tested: 0 crossing
    triangle pairs on the envelope, where the fixed 0-2 diagonal gave 448).
    Every later EXACT boolean then sees planar faces only, so its output
    polygons stay planar and cannot fold when triangulated for export."""
    q = np.asarray(quads, np.int64)
    me = bpy.data.meshes.new("_tri_tmp")
    me.vertices.add(len(pts))
    me.vertices.foreach_set("co", np.ascontiguousarray(pts, np.float32).ravel())
    me.loops.add(4 * len(q))
    me.loops.foreach_set("vertex_index", np.ascontiguousarray(q.ravel(), np.int32))
    me.polygons.add(len(q))
    me.polygons.foreach_set("loop_start", np.arange(0, 4 * len(q), 4, dtype=np.int32))
    me.update(calc_edges=True)
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
    bm.verts.index_update()
    tris = np.array([[v.index for v in f.verts] for f in bm.faces], np.int64)
    co = np.array([v.co[:] for v in bm.verts], np.float32)
    bm.free()
    bpy.data.meshes.remove(me)
    return co, tris


def vdb_mesh(g, F, iso=0.0, adaptivity=0.0):
    """Mesh the zero level of a full-grid field with OpenVDB.  Returns
    (points, faces_flat, face_sizes) as BEAUTY triangles."""
    import openvdb as vdb
    grid = vdb.FloatGrid(background=float(FS.FAR))
    grid.transform = vdb.createLinearTransform(voxelSize=g.h)
    grid.copyFromArray(np.ascontiguousarray(np.clip(F, -FS.FAR, FS.FAR).astype(np.float32)),
                       ijk=tuple(g.i0))
    pts, quads = grid.convertToQuads(iso)
    co, tris = beauty_tris(pts, quads)
    return co, tris.ravel(), np.full(len(tris), 3, np.int32)


def mesh_stats(ob, with_selfx=False):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    nonman = sum(1 for e in bm.edges if not e.is_manifold)
    bound = sum(1 for e in bm.edges if e.is_boundary)
    vol = bm.calc_volume(signed=True)
    # connected shells
    bm.verts.ensure_lookup_table()
    parent = list(range(len(bm.verts)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for e in bm.edges:
        a, b = find(e.verts[0].index), find(e.verts[1].index)
        if a != b:
            parent[a] = b
    roots = {}
    for v in bm.verts:
        r = find(v.index)
        roots[r] = roots.get(r, 0) + 1
    co = np.array([v.co[:] for v in bm.verts])
    out = {"verts": len(bm.verts), "faces": len(bm.faces), "nonmanifold_edges": nonman,
           "boundary_edges": bound, "volume_mm3": round(vol, 1), "shells": len(roots),
           "shell_sizes": sorted(roots.values(), reverse=True)[:8],
           "bbox": [round(float(x), 4) for x in (co[:, 0].min(), co[:, 0].max(), co[:, 1].min(),
                                                 co[:, 1].max(), co[:, 2].min(), co[:, 2].max())]}
    if with_selfx:
        tree = BVHTree.FromBMesh(bm, epsilon=0.00001)
        out["self_intersect_pairs"] = len(tree.overlap(tree))
    bm.free()
    return out


def save(tag=None):
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    if tag:
        os.makedirs(VERSIONS, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(VERSIONS, "halloween-cat_%s.blend" % tag), copy=True)
    log("saved %s%s" % (BLEND, (" + versions/halloween-cat_%s.blend" % tag) if tag else ""))


def shells_of(pts, flat, sizes):
    """Connected shells of a face soup: list of (n_verts, signed volume, bbox)."""
    n = len(pts)
    parent = np.arange(n)

    def find(x):
        r = x
        while parent[r] != r:
            r = parent[r]
        while parent[x] != r:
            parent[x], x = r, parent[x]
        return r
    starts = np.concatenate([[0], np.cumsum(sizes)[:-1]])
    for s, k in zip(starts.tolist(), sizes.tolist()):
        a = find(flat[s])
        for j in range(1, k):
            b = find(flat[s + j])
            if a != b:
                parent[b] = a
    roots = np.array([find(i) for i in range(n)])
    out = []
    for r in np.unique(roots):
        idx = np.nonzero(roots == r)[0]
        out.append({"root": int(r), "n": len(idx), "bbox": (pts[idx].min(0), pts[idx].max(0))})
    # signed volume per shell (fan triangulation of each face)
    vol = {}
    tri_a, tri_b, tri_c = [], [], []
    for s, k in zip(starts.tolist(), sizes.tolist()):
        for j in range(1, k - 1):
            tri_a.append(flat[s]); tri_b.append(flat[s + j]); tri_c.append(flat[s + j + 1])
    A, Bv, Cv = pts[tri_a], pts[tri_b], pts[tri_c]
    v6 = np.einsum("ij,ij->i", A, np.cross(Bv, Cv)) / 6.0
    rt = roots[np.array(tri_a)]
    for r, v in zip(rt.tolist(), v6.tolist()):
        vol[r] = vol.get(r, 0.0) + v
    for o in out:
        o["volume"] = vol.get(o["root"], 0.0)
    return sorted(out, key=lambda o: -o["n"])


def fix_islands(g, F, pts, flat, sizes, keep=1, max_n=20000):
    """Remove every shell except the `keep` largest by flipping the sign of the
    field inside it (local flood fill in the shell's bounding box)."""
    from collections import deque
    sh = shells_of(pts, flat, sizes)
    fixed = []
    for o in sh[keep:]:
        if o["n"] > max_n:
            raise RuntimeError("large extra shell %s" % o)
        lo, hi = o["bbox"]
        sl = []
        for d in range(3):
            a = max(0, int(math.floor(lo[d] / g.h)) - g.i0[d] - 2)
            b = min(g.n[d], int(math.ceil(hi[d] / g.h)) - g.i0[d] + 3)
            sl.append(slice(a, b))
        sub = F[tuple(sl)]
        solid_island = o["volume"] > 0          # encloses F < 0
        mask = (sub < 0) if solid_island else (sub >= 0)
        lab = np.zeros(mask.shape, np.int32)
        comp = 0
        for start in zip(*np.nonzero(mask)):
            if lab[start]:
                continue
            comp += 1
            q = deque([start]); lab[start] = comp; mem = [start]; touches = False
            while q:
                c = q.popleft()
                for d in range(3):
                    for s in (-1, 1):
                        nb = list(c); nb[d] += s; nb = tuple(nb)
                        if nb[d] < 0 or nb[d] >= mask.shape[d]:
                            touches = True
                            continue
                        if mask[nb] and not lab[nb]:
                            lab[nb] = comp; q.append(nb); mem.append(nb)
            if not touches:
                for c in mem:
                    sub[c] = abs(sub[c]) + 0.05 if solid_island else -abs(sub[c]) - 0.05
                fixed.append({"centre": [round(float(v), 2) for v in 0.5 * (lo + hi)],
                              "voxels": len(mem), "solid": bool(solid_island)})
    return fixed


def preview_outer():
    """Quick look: mesh the cached envelope E (no distance field)."""
    g = FS.Grid()
    E = load_arr("f_E")
    pts, flat, sizes = vdb_mesh(g, E)
    fixed = fix_islands(g, E, pts, flat, sizes, keep=1)
    if fixed:
        pts, flat, sizes = vdb_mesh(g, E)
        save_arr("f_E", E)
    ob = obj_from_arrays("ENV_outer", pts, flat, sizes, coll(COLL_WORK), (0.08, 0.08, 0.08, 1))
    return ob, fixed


# ------------------------------------------------------------------ file setup
def setup_file():
    """Start a NEW file for the figure (never touches the test-parts file)."""
    bpy.ops.wm.read_homefile(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.unit_settings.length_unit = 'MILLIMETERS'
    sc.unit_settings.scale_length = 0.001
    coll(COLL_FIG)
    B.build_refs()                       # REF_puck (+ ring), REF_cable_4, REF_cable_5
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    log("new file " + BLEND)


# ------------------------------------------------------------------ steps
def step_fields():
    t0 = time.time()
    g = FS.Grid()
    log("grid %s voxels (%.1f M), h %.2f" % (g.n, np.prod(g.n) / 1e6, g.h))
    comps = FS.components(g, log)
    f = FS.compose(g, comps, log)
    for k in ("E", "black", "pumpkin", "pumpkin_noribs", "stem", "torso_alone", "head_alone"):
        save_arr("f_" + k, f[k])
    sl, rib = comps["rib_offset"]
    np.save(cpath("rib_offset"), rib)
    with open(os.path.join(CACHE, "rib_sl.txt"), "w") as fh:
        fh.write(repr([(s.start, s.stop) for s in sl]))
    log("step_fields %.1f s" % (time.time() - t0))
    return g, f


def step_outer(show=True):
    """Mesh the envelope and compute the exact outer distance D_out."""
    import openvdb as vdb
    t0 = time.time()
    g = FS.Grid()
    E = load_arr("f_E")
    pts, flat, sizes = vdb_mesh(g, E)
    fixed = fix_islands(g, E, pts, flat, sizes, keep=1)
    if fixed:
        log("envelope islands removed: %s" % fixed)
        save_arr("f_E", E)
        pts, flat, sizes = vdb_mesh(g, E)
    log("outer mesh: %d verts, %d faces" % (len(pts), len(sizes)))
    ob = obj_from_arrays("ENV_outer", pts, flat, sizes, coll(COLL_WORK), (0.2, 0.2, 0.2, 1))
    ob.hide_set(not show)
    # level set (fast, approximate away from the surface) ...
    tris = flat.reshape(-1, 3)
    ls = vdb.FloatGrid.createLevelSetFromPolygons(
        pts.astype(np.float32), triangles=tris.astype(np.uint32),
        transform=vdb.createLinearTransform(voxelSize=g.h), exBandWidth=6.0, inBandWidth=16.0)
    D = np.zeros(g.n, np.float32)
    ls.copyToArray(D, ijk=tuple(g.i0))
    # ... refined to exact point-to-mesh distance in the band that sets the walls
    tree = BVHTree.FromPolygons([tuple(p) for p in pts.tolist()], tris.tolist(), all_triangles=True)
    idx = np.nonzero((D < -0.6) & (D > -4.6))
    xs, ys, zs = g.ax
    P_ = np.stack([xs[idx[0]], ys[idx[1]], zs[idx[2]]], 1).astype(np.float64)
    out = np.empty(len(P_), np.float32)
    fn = tree.find_nearest
    for i, p in enumerate(P_.tolist()):
        out[i] = fn(p)[3]
    diff = np.abs(-out - D[idx])
    log("D_out refine: %d voxels, vdb error max %.3f, 99.9%% %.3f" %
        (len(out), float(diff.max()), float(np.percentile(diff, 99.9))))
    D[idx] = -out
    save_arr("D_out", D)
    log("step_outer %.1f s" % (time.time() - t0))
    return D


def build_base_void(name="_base_void"):
    """The stage-1 coupon void (pocket + entry/top chamfers + shelf aperture +
    plenum bore + tunnel + flex-arm cutouts - snap tabs), built with the SAME
    stage-1 helpers in the SAME order as build_test_parts.build_coupon('flex').
    Only two lengths differ: the plenum bore runs to BASE_VOID_TOP (z 18, inside
    the chamber) and the tunnel prism runs past the r 60 base edge."""
    work = coll(COLL_WORK)
    H = P.BASE_VOID_TOP - 1.0           # pocket_void_profile(H) reaches z H + 1
    R = P.BASE_D / 2.0
    void = B.bm_to_obj(B.revolve_bm(B.pocket_void_profile(H), phase=0.5), name, work)
    tun = B.bm_to_obj(B.prism_bm(B.tunnel_poly(), 'Y', 20.0, R + 5.0), "_tunnel", work)
    B.apply_boolean(void, tun, 'UNION')
    remove_obj("_tunnel")
    for phi in P.TAB_ANGLES:
        g = P.arm_angles(phi)
        lo, hi = sorted((g["root"], g["gap_end"]))
        C = P.RELIEF_CEIL_C
        f_prof = [(30.0, -1.5), (P.SLOT_R_OUT, -1.5), (P.SLOT_R_OUT, C - P.SLOT_R_OUT), (30.0, C - 30.0)]
        F = B.bm_to_obj(B.revolve_bm(f_prof, lo, hi, phase=0.5), "_armcut", work)
        if P.ARM_ROOT_SIDE < 0:
            a_lo, a_hi = g["root"] - 2.0, g["free"]
        else:
            a_lo, a_hi = g["free"], g["root"] + 2.0
        a_prof = [(29.5, -2.0), (P.ARM_R_OUT, -2.0), (P.ARM_R_OUT, P.ARM_H), (29.5, P.ARM_H)]
        A = B.bm_to_obj(B.revolve_bm(a_prof, a_lo, a_hi, phase=0.25), "_arm", work)
        B.apply_boolean(F, A, 'DIFFERENCE')
        remove_obj("_arm")
        B.apply_boolean(void, F, 'UNION')
        remove_obj("_armcut")
    ht = B.tab_half_deg(P.TAB_ENGAGE)
    for phi in P.TAB_ANGLES:
        T = B.bm_to_obj(B.revolve_bm(B.tab_profile(P.TAB_ENGAGE), phi - ht, phi + ht, phase=0.75), "_tab", work)
        B.apply_boolean(void, T, 'DIFFERENCE')
        remove_obj("_tab")
    return void


def step_base_void():
    """M1 = M0 - stage-1 base void (EXACT)."""
    t0 = time.time()
    m0 = bpy.data.objects["M0_master"]
    remove_obj("M1_base")
    m1 = m0.copy()
    m1.data = m0.data.copy()
    m1.name = "M1_base"
    coll(COLL_FIG).objects.link(m1)
    void = build_base_void()
    sv = mesh_stats(void)
    log("base void: %s" % sv)
    v0 = mesh_stats(m1)["volume_mm3"]
    B.apply_boolean(m1, void, 'DIFFERENCE')
    st = mesh_stats(m1)
    log("M1 after base void: %s (volume %.1f -> %.1f, removed %.1f)" %
        (st, v0, st["volume_mm3"], v0 - st["volume_mm3"]))
    m0.hide_set(True)
    log("step_base_void %.1f s" % (time.time() - t0))
    return st, sv


# ------------------------------------------------------------------ windows / zones
WINDOW_GROUPS = {
    "cat": {"windows": FS.CAT_WINDOWS, "inlays": FS.INLAYS, "skin": P.SKIN_T_CAT, "wall": P.WALL_CAT,
            "x": (-40.0, 40.0), "z": (93.0, 136.0)},
    "pk": {"windows": FS.PK_WINDOWS, "inlays": (), "skin": P.SKIN_T_PUMPKIN, "wall": P.WALL_PUMPKIN,
           "x": (-40.0, 40.0), "z": (22.0, 90.0)},
}


def bvh_of(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.transform(ob.matrix_world)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    t = BVHTree.FromBMesh(bm)
    bm.free()
    return t


def depth_point(tree_out, x, z, y_out, depth, nrm_y):
    """y along the +Y ray at column (x, z) whose distance to the outer surface
    equals `depth` (the offset surface, i.e. measured along the normal)."""
    lo = y_out
    hi = y_out + max(3.0 * depth, depth / max(abs(nrm_y), 0.2) + 0.5)
    fn = tree_out.find_nearest
    for _ in range(26):
        mid = 0.5 * (lo + hi)
        if fn((x, mid, z))[3] < depth:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def column_data(group, h=None, dmax=12.0):
    """Per-column (x, z) data for a window group on a fine local grid:
    y_out (outer surface), y_floor (skin inner face, exact offset), y_inl
    (inlay back face at INLAY_DEPTH), y_ch (chamber entry), delta (2D
    distance to the nearest window of the group, 0 inside)."""
    G = WINDOW_GROUPS[group]
    h = h or P.FINE_H
    xs = np.arange(G["x"][0], G["x"][1] + 1e-9, h)
    zs = np.arange(G["z"][0], G["z"][1] + 1e-9, h)
    XX, ZZ = np.meshgrid(xs, zs, indexing="ij")
    dwin = np.full(XX.shape, 1e3)
    for w in G["windows"]:
        dwin = np.minimum(dwin, FS.outline_sdf2(w, XX, ZZ))
    dinl = np.full(XX.shape, 1e3)
    for w in G["inlays"]:
        dinl = np.minimum(dinl, FS.outline_sdf2(w, XX, ZZ))
    t_out = bvh_of(bpy.data.objects["ENV_outer"])
    t_ch = bvh_of(bpy.data.objects["CHAMBER_void"])
    nx, nz = XX.shape
    y_out = np.full((nx, nz), np.nan)
    y_fl = np.full((nx, nz), np.nan)
    y_in = np.full((nx, nz), np.nan)
    y_ch = np.full((nx, nz), np.nan)
    d = Vector((0.0, 1.0, 0.0))
    for i in range(nx):
        for k in range(nz):
            need_w = dwin[i, k] <= dmax
            need_i = dinl[i, k] <= 2.0
            if not (need_w or need_i):
                continue
            x, z = float(xs[i]), float(zs[k])
            loc, nrm, idx, dist = t_out.ray_cast(Vector((x, -120.0, z)), d, 300.0)
            if loc is None:
                continue
            y_out[i, k] = loc.y
            if need_w:
                if dwin[i, k] < 4.0:
                    y_fl[i, k] = depth_point(t_out, x, z, loc.y, G["skin"], nrm.y)
                else:
                    y_fl[i, k] = loc.y + G["skin"] / max(abs(nrm.y), 0.2)
                l2, n2, i2, d2 = t_ch.ray_cast(Vector((x, loc.y, z)), d, 80.0)
                if l2 is not None:
                    y_ch[i, k] = l2.y
            if need_i and dinl[i, k] < 1.0:
                y_in[i, k] = depth_point(t_out, x, z, loc.y, P.INLAY_DEPTH, nrm.y)
    cd = {"xs": xs, "zs": zs, "dwin": dwin, "dinl": dinl, "y_out": y_out, "y_fl": y_fl,
          "y_in": y_in, "y_ch": y_ch, "h": h, "skin": G["skin"], "wall": G["wall"]}
    np.savez(os.path.join(CACHE, "cols_%s.npz" % group), **cd)
    return cd


def load_cols(group):
    d = np.load(os.path.join(CACHE, "cols_%s.npz" % group))
    cd = {k: d[k] for k in d.files}
    for k in ("h", "skin", "wall"):
        cd[k] = float(cd[k])
    return cd


def local_mesh(F, x0, y0, z0, h, name, collection, color=None):
    """Mesh a local field whose voxel (0,0,0) sits at world (x0, y0, z0)."""
    import openvdb as vdb
    grid = vdb.FloatGrid(background=float(FS.FAR))
    m = np.identity(4)
    m[0, 0] = m[1, 1] = m[2, 2] = h
    m[3, 0], m[3, 1], m[3, 2] = x0, y0, z0
    grid.transform = vdb.createLinearTransform(matrix=m.tolist())
    grid.copyFromArray(np.ascontiguousarray(np.clip(F, -FS.FAR, FS.FAR).astype(np.float32)), ijk=(0, 0, 0))
    pts, quads = grid.convertToQuads(0.0)
    if len(quads) == 0:
        return None
    co, tris = beauty_tris(pts, quads)
    return obj_from_arrays(name, co, tris.ravel(), np.full(len(tris), 3, np.int32), collection, color)


def dout_local(xs, ys, zs):
    """Trilinear interpolation of the cached exact D_out onto a local grid."""
    g = FS.Grid()
    D = load_arr("D_out")

    def idx(a, d):
        f = a / g.h - g.i0[d]
        i0 = np.clip(np.floor(f).astype(int), 0, g.n[d] - 2)
        return i0, (f - i0).astype(np.float32)
    ix, fx = idx(xs, 0)
    iy, fy = idx(ys, 1)
    iz, fz = idx(zs, 2)
    out = np.zeros((len(xs), len(ys), len(zs)), np.float32)
    for a in (0, 1):
        wx = (fx if a else 1 - fx)[:, None, None]
        for b in (0, 1):
            wy = (fy if b else 1 - fy)[None, :, None]
            for c in (0, 1):
                wz = (fz if c else 1 - fz)[None, None, :]
                out += wx * wy * wz * D[np.ix_(ix + a, iy + b, iz + c)]
    return out


def build_window_cutters(group, cd):
    """Pocket cutter, yellow zone and (cat group) pink zone meshes."""
    xs, zs, h = cd["xs"], cd["zs"], cd["h"]
    y_out, y_fl, y_in, y_ch = cd["y_out"], cd["y_fl"], cd["y_in"], cd["y_ch"]
    dwin, dinl = cd["dwin"], cd["dinl"]
    skin, wall = cd["skin"], cd["wall"]
    ok = np.isfinite(y_fl) & np.isfinite(y_ch)
    y_front = np.where(ok, y_fl + np.maximum(0.0, dwin - P.WINDOW_EPS), np.nan)
    # back limit: the chamber behind the column, but never deeper than the
    # chamber behind the NEAREST window point.  A flank outside the outline
    # then pinches off in a 45 deg wedge instead of tunnelling through thick
    # wall (which would leave flat ceilings where it stops).
    from mathutils.kdtree import KDTree
    ii, kk = np.nonzero((dwin <= 0) & ok)
    kd = KDTree(len(ii))
    for n_, (a, b) in enumerate(zip(ii.tolist(), kk.tolist())):
        kd.insert((float(xs[a]), float(zs[b]), 0.0), n_)
    kd.balance()
    y_near = np.full(y_ch.shape, np.nan)
    oi, ok_ = np.nonzero(ok & (dwin > 0))
    for a, b in zip(oi.tolist(), ok_.tolist()):
        co, n_, dd = kd.find((float(xs[a]), float(zs[b]), 0.0))
        y_near[a, b] = y_ch[ii[n_], kk[n_]]
    y_near = np.where(dwin <= 0, y_ch, y_near)
    y_back = np.where(ok, np.minimum(y_ch, y_near) + P.WINDOW_BACK_OVERLAP, np.nan)
    has = ok & (y_front < y_back - 0.01)
    ylo = float(np.nanmin(np.where(np.isfinite(y_out), y_out, np.nan))) - P.INLAY_FRONT - 1.0
    yhi = float(np.nanmax(np.where(has, y_back, np.nan))) + 1.0
    ys = np.arange(math.floor(ylo / h) * h, yhi + h, h)
    Y = ys[None, :, None]
    # ---- pocket: y_front <= y <= y_back, and never closer to the outside than
    # min(wall, delta + skin) (keeps the flank honest on curved surfaces)
    yf = np.where(has, y_front, 1e3)[:, None, :]
    yb = np.where(has, y_back, -1e3)[:, None, :]
    Fp = np.maximum(yf - Y, Y - yb).astype(np.float32)
    Dl = dout_local(xs, ys, zs)
    lim = np.minimum(wall, dwin + skin)[:, None, :]
    use = (dwin >= 1.0)[:, None, :]
    Fp = np.where(use, np.maximum(Fp, Dl + lim - 0.02), Fp).astype(np.float32)
    x0, y0, z0 = float(xs[0]), float(ys[0]), float(zs[0])
    cut = local_mesh(Fp, x0, y0, z0, h, "CUT_pockets_" + group, coll(COLL_WORK), (1, 0.3, 0.3, 1))
    del Fp, Dl
    # ---- yellow zone: inside the outline, from in front of the surface to
    # YELLOW_BACK behind the skin (inside the pocket void)
    fin = np.isfinite(y_out) & np.isfinite(y_fl)
    yfr = np.where(fin, y_out - P.INLAY_FRONT, 1e3)[:, None, :]
    ybk = np.where(fin, y_fl + P.YELLOW_BACK, -1e3)[:, None, :]
    Fy = np.maximum(np.maximum(dwin[:, None, :] + 0.0 * Y, yfr - Y), Y - ybk).astype(np.float32)
    yz = local_mesh(Fy, x0, y0, z0, h, "ZONE_yellow_" + group, coll(COLL_WORK), (1, 0.9, 0.1, 1))
    del Fy
    pz = None
    if WINDOW_GROUPS[group]["inlays"]:
        fin = np.isfinite(y_out) & np.isfinite(y_in)
        yfr = np.where(fin, y_out - P.INLAY_FRONT, 1e3)[:, None, :]
        ybk = np.where(fin, y_in, -1e3)[:, None, :]
        Fk = np.maximum(np.maximum(dinl[:, None, :] + 0.0 * Y, yfr - Y), Y - ybk).astype(np.float32)
        pz = local_mesh(Fk, x0, y0, z0, h, "ZONE_pink", coll(COLL_WORK), (1, 0.45, 0.65, 1))
        del Fk
    return cut, yz, pz, {"y_range": [x0, float(ys[-1])], "grid": [len(xs), len(ys), len(zs)]}


def drop_small_shells(ob, min_verts=200):
    """Delete connected pieces with fewer than min_verts vertices (meshing
    specks).  Returns the list of dropped (centre, n_verts)."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.verts.ensure_lookup_table()
    seen, dropped, kill = set(), [], []
    for v in bm.verts:
        if v.index in seen:
            continue
        stack, mem = [v], []
        seen.add(v.index)
        while stack:
            x = stack.pop()
            mem.append(x)
            for e in x.link_edges:
                o = e.other_vert(x)
                if o.index not in seen:
                    seen.add(o.index)
                    stack.append(o)
        if len(mem) < min_verts:
            c = sum((m.co for m in mem), Vector()) / len(mem)
            dropped.append(([round(c.x, 2), round(c.y, 2), round(c.z, 2)], len(mem)))
            kill += mem
    if kill:
        bmesh.ops.delete(bm, geom=kill, context='VERTS')
        bm.to_mesh(ob.data)
        ob.data.update()
    bm.free()
    return dropped


def repair_mesh(ob, speck_verts=100, merge_dist=1e-4, max_hole_edges=12):
    """Minimal clean-up after an EXACT boolean (the solver occasionally emits
    a speck, near-duplicate vertices, a coincident double face or a tiny
    hole far from the cut).  Reports every change; refuses large holes."""
    rep = {"specks": drop_small_shells(ob, speck_verts)}
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    n0 = len(bm.verts)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=merge_dist)
    rep["merged_verts"] = n0 - len(bm.verts)
    # coincident double faces (same vertex set)
    seen, dup = {}, []
    for f in bm.faces:
        key = tuple(sorted(v.index for v in f.verts))
        if key in seen:
            dup += [f, seen[key]]
        else:
            seen[key] = f
    dup = list(set(dup))
    if dup:
        bmesh.ops.delete(bm, geom=dup, context='FACES_ONLY')
    rep["double_faces_removed"] = len(dup)
    # zero-volume flaps: two tiny opposite-facing faces on a >2-face edge
    flap = set()
    for e in bm.edges:
        if len(e.link_faces) > 2:
            fs = sorted(e.link_faces, key=lambda f: f.calc_area())
            if fs[0].normal.dot(fs[1].normal) < -0.9 and fs[1].calc_area() < 0.01:
                flap.update(fs[:2])
    if flap:
        bmesh.ops.delete(bm, geom=list(flap), context='FACES_ONLY')
    rep["flap_faces_removed"] = len(flap)
    # lone faces whose every edge is a boundary edge (floating slivers)
    lone = [f for f in bm.faces if all(len(e.link_faces) == 1 for e in f.edges) and f.calc_area() < 0.01]
    if lone:
        bmesh.ops.delete(bm, geom=lone, context='FACES_ONLY')
    rep["lone_faces_removed"] = len(lone)
    loose = [e for e in bm.edges if not e.link_faces]
    if loose:
        bmesh.ops.delete(bm, geom=loose, context='EDGES')
    lv = [v for v in bm.verts if not v.link_faces]
    if lv:
        bmesh.ops.delete(bm, geom=lv, context='VERTS')
    bnd = [e for e in bm.edges if e.is_boundary]
    if len(bnd) > max_hole_edges:
        bm.free()
        raise RuntimeError("repair_mesh: %d boundary edges, refusing to fill" % len(bnd))
    filled = bmesh.ops.holes_fill(bm, edges=bnd, sides=0)["faces"] if bnd else []
    rep["holes_filled_faces"] = len(filled)
    if filled:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(ob.data)
    ob.data.update()
    bm.free()
    return rep


def crossing_pairs(bm):
    """Pairs of triangles (triangulated bmesh) that intersect without sharing
    a vertex (true self-intersections)."""
    bm.faces.ensure_lookup_table()
    tr = BVHTree.FromBMesh(bm, epsilon=0.00001)
    out = []
    for a, b in tr.overlap(tr):
        fa, fb = bm.faces[a], bm.faces[b]
        if not ({v.index for v in fa.verts} & {v.index for v in fb.verts}):
            out.append((a, b))
    return out


def fix_crossings(ob, max_iter=6, collapse=0.01):
    """Remove micro-folds on cut seams: triangulate (BEAUTY), collapse edges
    shorter than `collapse` mm, then relax ONLY the vertices of triangles that
    still cross (Laplacian, factor 0.5).  Reports counts and the largest
    vertex move."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
    # NOTE: edge collapsing (dissolve_degenerate) was tried and broke the
    # topology (non-manifold edges); relaxation alone never changes topology.
    cr = crossing_pairs(bm)
    rep = {"before": len(cr)}
    maxmove = 0.0
    it = 0
    while cr and it < max_iter:
        it += 1
        bm.faces.ensure_lookup_table()
        vs = {v for a, b in cr for fi in (a, b) for v in bm.faces[fi].verts}
        newpos = {}
        for v in vs:
            nb = [e.other_vert(v).co for e in v.link_edges]
            avg = sum(nb, Vector()) / len(nb)
            newpos[v] = v.co + 0.5 * (avg - v.co)
        for v, p in newpos.items():
            maxmove = max(maxmove, (p - v.co).length)
            v.co = p
        cr = crossing_pairs(bm)
    rep["after_relax"] = len(cr)
    rep["relax_iterations"] = it
    rep["max_vertex_move_mm"] = round(maxmove, 5)
    bm.to_mesh(ob.data)
    ob.data.update()
    bm.free()
    return rep


def fix_zero_area(ob, area_tol=1e-9, max_pass=6):
    """Remove zero-area (collinear) triangles by rotating their longest edge.
    No vertex moves; topology stays a closed 2-manifold."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
    n0 = sum(1 for f in bm.faces if f.calc_area() < area_tol)
    for _ in range(max_pass):
        z = [f for f in bm.faces if f.calc_area() < area_tol]
        if not z:
            break
        edges = []
        for f in z:
            e = max(f.edges, key=lambda e: e.calc_length())
            if len(e.link_faces) == 2 and e not in edges:
                edges.append(e)
        bmesh.ops.rotate_edges(bm, edges=edges, use_ccw=False)
    n1 = sum(1 for f in bm.faces if f.calc_area() < area_tol)
    bm.to_mesh(ob.data)
    ob.data.update()
    bm.free()
    return {"zero_area_before": n0, "after": n1}


def step_windows():
    """M2 = M1 - window pocket cutters (EXACT)."""
    t0 = time.time()
    m1 = bpy.data.objects["M1_base"]
    remove_obj("M2_windows")
    m2 = m1.copy()
    m2.data = m1.data.copy()
    m2.name = "M2_windows"
    coll(COLL_FIG).objects.link(m2)
    rep = {}
    for gname in ("cat", "pk"):
        cut = bpy.data.objects["CUT_pockets_" + gname]
        rep["dropped_" + gname] = drop_small_shells(cut)
        v0 = mesh_stats(m2)["volume_mm3"]
        B.apply_boolean(m2, cut, 'DIFFERENCE')
        rep["repair_" + gname] = repair_mesh(m2)
        st = mesh_stats(m2)
        rep[gname] = {"removed_mm3": round(v0 - st["volume_mm3"], 1), "after": st}
        log("pockets %s: removed %.1f mm3, M2 %s" % (gname, v0 - st["volume_mm3"], st))
    m1.hide_set(True)
    log("step_windows %.1f s" % (time.time() - t0))
    return rep


def step_zones():
    """Orange / green zone meshes from the fields (bisector boundaries), and
    one joined yellow zone.  Orange zone Zo' deliberately INCLUDES the stem
    region; the orange/green boundary then comes only from Zg (subtracted)."""
    g = FS.Grid()
    PK, ST, BL = load_arr("f_pumpkin"), load_arr("f_stem"), load_arr("f_black")
    Zo = np.maximum(np.maximum(PK - BL, PK - 6.0), -PK - 30.0).astype(np.float32)
    Zg = np.maximum(np.maximum(ST - PK, ST - BL), np.maximum(ST - 6.0, -ST - 12.0)).astype(np.float32)
    out = {}
    for nm, F, col in (("ZONE_orange", Zo, (1, 0.42, 0, 1)), ("ZONE_green", Zg, (0.18, 0.55, 0.18, 1))):
        pts, flat, sizes = vdb_mesh(g, F)
        fixed = fix_islands(g, F, pts, flat, sizes, keep=1)
        if fixed:
            pts, flat, sizes = vdb_mesh(g, F)
        ob = obj_from_arrays(nm, pts, flat, sizes, coll(COLL_WORK), col)
        out[nm] = mesh_stats(ob)
        out[nm]["islands_fixed"] = fixed
    # joined yellow zone (the two groups are far apart -> disjoint shells)
    remove_obj("ZONE_yellow")
    yc, yp = bpy.data.objects["ZONE_yellow_cat"], bpy.data.objects["ZONE_yellow_pk"]
    y = yc.copy(); y.data = yc.data.copy(); y.name = "ZONE_yellow"
    coll(COLL_WORK).objects.link(y)
    bm = bmesh.new(); bm.from_mesh(y.data); bm.from_mesh(yp.data); bm.to_mesh(y.data); bm.free()
    out["ZONE_yellow"] = mesh_stats(y)
    return out


def dup(ob, name, collection=None):
    remove_obj(name)
    d = ob.copy()
    d.data = ob.data.copy()
    d.name = name
    (collection or coll(COLL_PARTS)).objects.link(d)
    return d


def boolean_seq(src, name, ops, color):
    """dup src -> apply [(op, zone_name)...] in order; returns stats per step."""
    ob = dup(src, name)
    ob.color = color
    rec = []
    for op, zn in ops:
        v0 = mesh_stats(ob)["volume_mm3"]
        B.apply_boolean(ob, bpy.data.objects[zn], op)
        st0 = mesh_stats(ob)
        fix = None
        if st0["nonmanifold_edges"] or st0["boundary_edges"]:
            fix = repair_mesh(ob, speck_verts=50)
        st = mesh_stats(ob)
        rec.append({"op": op, "zone": zn, "vol_before": v0, "vol_after": st["volume_mm3"],
                    "shells": st["shells"], "nonmanifold": st["nonmanifold_edges"],
                    "boundary": st["boundary_edges"], "raw_nonmanifold": st0["nonmanifold_edges"],
                    "repair": fix})
        log("%s %s %s: %.1f -> %.1f mm3, shells %d, nonman %d" % (name, op, zn, v0, st["volume_mm3"],
                                                                    st["shells"], st["nonmanifold_edges"]))
    return ob, rec


def step_master(show=True):
    t0 = time.time()
    g = FS.Grid()
    f = {k: load_arr("f_" + k) for k in ("E", "pumpkin", "torso_alone", "head_alone")}
    D = load_arr("D_out")
    C, parts, info = FS.chamber(g, f, D, log)
    save_arr("C", C)
    for k, v in parts.items():
        save_arr("C_" + k, v)
    S = np.maximum(f["E"], -C)
    pts, flat, sizes = vdb_mesh(g, S)
    log("master mesh: %d verts, %d faces" % (len(pts), len(sizes)))
    ob = obj_from_arrays("M0_master", pts, flat, sizes, coll(COLL_FIG), (0.05, 0.05, 0.05, 1))
    # chamber surface alone (for checks)
    cp, cflat, csz = vdb_mesh(g, C)
    ch = obj_from_arrays("CHAMBER_void", cp, cflat, csz, coll(COLL_WORK), (0.9, 0.9, 0.2, 1))
    ch.hide_set(True)
    info["master"] = mesh_stats(ob)
    info["chamber"] = mesh_stats(ch)
    log("master stats %s" % info["master"])
    log("chamber stats %s" % info["chamber"])
    log("step_master %.1f s" % (time.time() - t0))
    return info
