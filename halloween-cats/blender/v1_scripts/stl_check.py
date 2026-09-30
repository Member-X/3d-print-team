"""Independent STL / 3MF read-back checks (pure numpy, no Blender).

    python stl_check.py            -> checks every figure STL + the 3MF + tile skins

Checks per STL: file size consistent with the triangle count, unique-vertex
welding, non-manifold edges (edge use count != 2), orientation consistency
(each directed edge used once and its reverse once), degenerate triangles,
connected bodies, signed volume, bbox, bottom flatness.
"""
import json
import os
import struct
import sys
import zipfile
import xml.etree.ElementTree as ET

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STL = os.path.join(ROOT, "stl")


def read_stl(path):
    data = open(path, "rb").read()
    n = struct.unpack("<I", data[80:84])[0]
    ok = len(data) == 84 + 50 * n
    rec = np.frombuffer(data, dtype=np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]),
                        count=n, offset=84)
    return rec["v"].astype(np.float64), ok, n


def weld(tri):
    v = tri.reshape(-1, 3)
    uniq, inv = np.unique(v, axis=0, return_inverse=True)
    return uniq, inv.reshape(-1, 3)


def topology(faces, nverts):
    e = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    und = np.sort(e, axis=1)
    key = und[:, 0] * nverts + und[:, 1]
    _, cnt = np.unique(key, return_counts=True)
    nonman = int((cnt != 2).sum())
    dkey = e[:, 0] * nverts + e[:, 1]
    ud, dc = np.unique(dkey, return_counts=True)
    rev = e[:, 1] * nverts + e[:, 0]
    has_rev = np.isin(rev, ud)
    orient_bad = int((dc != 1).sum()) + int((~has_rev).sum())
    # connected bodies (union-find over vertices)
    parent = np.arange(nverts)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b, c in faces:
        ra, rb, rc = find(a), find(b), find(c)
        parent[rb] = ra
        parent[find(rc)] = ra
    roots = np.array([find(i) for i in range(nverts)])
    bodies = len(np.unique(roots[faces[:, 0]]))
    return nonman, orient_bad, bodies


def check_stl(path):
    tri, ok, n = read_stl(path)
    V, F = weld(tri)
    deg = int(((F[:, 0] == F[:, 1]) | (F[:, 1] == F[:, 2]) | (F[:, 0] == F[:, 2])).sum())
    nonman, orient_bad, bodies = topology(F, len(V))
    a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    vol = float(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6.0)
    lo, hi = V.min(0), V.max(0)
    zmin = lo[2]
    bottom = int(np.all(np.abs(V[F][:, :, 2] - zmin) < 1e-6, axis=1).sum())
    return {"file": os.path.basename(path), "size_ok": ok, "triangles": n, "unique_verts": len(V),
            "degenerate": deg, "nonmanifold_edges": nonman, "orientation_errors": orient_bad,
            "bodies": bodies, "volume_mm3": round(vol, 2),
            "bbox_min": [round(float(x), 4) for x in lo], "bbox_max": [round(float(x), 4) for x in hi],
            "size_xyz": [round(float(x), 3) for x in hi - lo], "bottom_tris_at_zmin": bottom}


def ray_hits_z(tri, x, z, y0=-50.0):
    """All y where the ray (x, y0 -> +inf, z) crosses the triangle soup."""
    a, b, c = tri[:, 0], tri[:, 1], tri[:, 2]
    o = np.array([x, y0, z])
    d = np.array([0.0, 1.0, 0.0])
    e1, e2 = b - a, c - a
    p = np.cross(d, e2)
    det = np.einsum("ij,ij->i", e1, p)
    ok = np.abs(det) > 1e-12
    inv = np.where(ok, 1.0 / np.where(ok, det, 1), 0)
    s = o - a
    u = np.einsum("ij,ij->i", s, p) * inv
    q = np.cross(s, e1)
    v = (q @ d) * inv
    t = np.einsum("ij,ij->i", e2, q) * inv
    m = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 0)
    return np.sort(y0 + t[m])


def tile_skins(path, xs=(-21.0, -7.0, 7.0, 21.0), zc=17.0):
    tri, _, _ = read_stl(path)
    out = []
    for x in xs:
        vals = []
        for dx, dz in ((0, 0), (-4, 0), (4, 0), (0, -9), (0, 9)):
            h = ray_hits_z(tri, x + dx, zc + dz)
            vals.append(round(float(h[1] - h[0]), 4) if len(h) >= 2 else None)
        out.append({"x": x, "skin_at_5_points": vals})
    return out


def check_3mf(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    root = ET.fromstring(z.read("3D/3dmodel.model"))
    ns = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"}
    objs = []
    for o in root.findall("m:resources/m:object", ns):
        mesh = o.find("m:mesh", ns)
        if mesh is None:
            comps = o.findall("m:components/m:component", ns)
            objs.append({"id": o.get("id"), "name": o.get("name"), "components": len(comps)})
            continue
        vs = mesh.findall("m:vertices/m:vertex", ns)
        ts = mesh.findall("m:triangles/m:triangle", ns)
        V = np.array([[float(v.get("x")), float(v.get("y")), float(v.get("z"))] for v in vs])
        F = np.array([[int(t.get("v1")), int(t.get("v2")), int(t.get("v3"))] for t in ts])
        nonman, orient_bad, bodies = topology(F, len(V))
        a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
        vol = float(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6.0)
        objs.append({"id": o.get("id"), "name": o.get("name"), "verts": len(V), "tris": len(F),
                     "nonmanifold_edges": nonman, "orientation_errors": orient_bad, "bodies": bodies,
                     "volume_mm3": round(vol, 2), "zmin": round(float(V[:, 2].min()), 4)})
    build = [{"objectid": i.get("objectid")} for i in root.findall("m:build/m:item", ns)]
    return {"files": names, "objects": objs, "build_items": build, "unit": root.get("unit")}


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    res = {}
    if what in ("all", "tile"):
        res["tile_standing"] = tile_skins(os.path.join(STL, "skin-calibration-tile.stl"))
        res["tile_flat"] = tile_skins(os.path.join(STL, "skin-calibration-tile_flat-print.stl"))
    if what in ("all", "figure"):
        for p in ("black", "orange", "yellow", "green", "pink", "combined"):
            f = os.path.join(STL, "halloween-cat_%s.stl" % p)
            if os.path.exists(f):
                res[p] = check_stl(f)
        f3 = os.path.join(ROOT, "3mf", "halloween-cat.3mf")
        if os.path.exists(f3):
            res["3mf"] = check_3mf(f3)
    print(json.dumps(res, indent=1))
