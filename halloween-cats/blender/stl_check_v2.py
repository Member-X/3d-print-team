"""Independent read-back of every v2 export (system Python: numpy only).

    python stl_check_v2.py  > report json

For each part the triangles are compared ACROSS formats (STL, core 3MF,
Bambu 3MF, OBJ) as exact float32 coordinate triples, so "identical
coordinates in every format" is tested bit for bit.
"""
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

import numpy as np

import stl_check as SC

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STL = os.path.join(ROOT, "stl", "v2")
TMF = os.path.join(ROOT, "3mf", "v2")
OBJD = os.path.join(ROOT, "obj", "v2")
PREFIX = "halloween-cat-v2"
PARTS = ("black", "orange", "yellow", "green", "pink")
NS = {"m": "http://schemas.microsoft.com/3dmanufacturing/core/2015/02",
      "p": "http://schemas.microsoft.com/3dmanufacturing/production/2015/06"}


def mesh_report(V, F):
    V = np.asarray(V, np.float64)
    F = np.asarray(F, np.int64)
    uniq, inv = np.unique(V, axis=0, return_inverse=True)
    W = inv.ravel()[F]
    deg = int(((W[:, 0] == W[:, 1]) | (W[:, 1] == W[:, 2]) | (W[:, 0] == W[:, 2])).sum())
    nonman, orient_bad, bodies = SC.topology(W, len(uniq))
    a, b, c = uniq[W[:, 0]], uniq[W[:, 1]], uniq[W[:, 2]]
    vol = float(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6.0)
    lo, hi = uniq.min(0), uniq.max(0)
    return {"tris": int(len(F)), "verts_welded": int(len(uniq)), "degenerate": deg, "nonmanifold_edges": nonman,
            "orientation_errors": orient_bad, "bodies": bodies, "volume_mm3": round(vol, 2),
            "bbox_min": [round(float(x), 4) for x in lo], "bbox_max": [round(float(x), 4) for x in hi]}


def tri_key_set(V, F):
    """Order-independent fingerprint of a triangle soup: sorted rows of the
    9 float32 coordinates of each triangle (rotated so the smallest vertex
    comes first, orientation kept)."""
    T = np.asarray(V, np.float32)[np.asarray(F, np.int64)]          # (n, 3, 3)
    keys = T.reshape(len(T), 9).view(np.uint32).reshape(len(T), 3, 3)
    # rotate each triangle so the lexicographically smallest vertex is first
    k3 = [tuple(map(tuple, t)) for t in keys.tolist()]
    out = []
    for t in k3:
        i = min(range(3), key=lambda j: t[j])
        out.append(t[i:] + t[:i])
    out.sort()
    return out


def read_stl_arrays(path):
    tri, ok, n = SC.read_stl(path)
    V = tri.reshape(-1, 3)
    F = np.arange(len(V)).reshape(-1, 3)
    return V, F


def parse_mesh_elem(mesh):
    vs = mesh.findall("m:vertices/m:vertex", NS)
    ts = mesh.findall("m:triangles/m:triangle", NS)
    V = np.array([[float(v.get("x")), float(v.get("y")), float(v.get("z"))] for v in vs], np.float64)
    F = np.array([[int(t.get("v1")), int(t.get("v2")), int(t.get("v3"))] for t in ts], np.int64)
    return V, F


def check_core_3mf(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read("3D/3dmodel.model"))
    parts, comps = {}, []
    for o in root.findall("m:resources/m:object", NS):
        mesh = o.find("m:mesh", NS)
        if mesh is not None:
            parts[o.get("name")] = parse_mesh_elem(mesh)
        else:
            comps = [c.get("objectid") for c in o.findall("m:components/m:component", NS)]
    build = [i.get("objectid") for i in root.findall("m:build/m:item", NS)]
    return parts, {"files": z.namelist(), "unit": root.get("unit"), "components": comps, "build_items": build}


def check_bambu_3mf(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    info = {"files": names}
    main = ET.fromstring(z.read("3D/3dmodel.model"))
    info["unit"] = main.get("unit")
    info["requiredextensions"] = main.get("requiredextensions")
    info["metadata"] = {m.get("name"): (m.text or "") for m in main.findall("m:metadata", NS)}
    objs = main.findall("m:resources/m:object", NS)
    info["main_objects"] = [{"id": o.get("id"), "type": o.get("type"),
                             "components": [{"path": c.get("{%s}path" % NS["p"]), "objectid": c.get("objectid"),
                                             "transform": c.get("transform")}
                                            for c in o.findall("m:components/m:component", NS)]} for o in objs]
    info["build_items"] = [{"objectid": i.get("objectid"), "transform": i.get("transform"), "printable": i.get("printable")}
                           for i in main.findall("m:build/m:item", NS)]
    rels = ET.fromstring(z.read("3D/_rels/3dmodel.model.rels"))
    info["model_rels_targets"] = [r.get("Target") for r in rels]
    sub = ET.fromstring(z.read("3D/Objects/object_1.model"))
    meshes = {}
    for o in sub.findall("m:resources/m:object", NS):
        meshes[o.get("id")] = parse_mesh_elem(o.find("m:mesh", NS))
    ms = ET.fromstring(z.read("Metadata/model_settings.config"))
    parts = []
    for o in ms.findall("object"):
        for p in o.findall("part"):
            md = {m.get("key"): m.get("value") for m in p.findall("metadata") if m.get("key")}
            parts.append({"id": p.get("id"), "subtype": p.get("subtype"), "name": md.get("name"),
                          "extruder": md.get("extruder"), "matrix": md.get("matrix"),
                          "face_count": p.find("mesh_stat").get("face_count") if p.find("mesh_stat") is not None else None})
        info["object_settings"] = {m.get("key"): m.get("value") for m in o.findall("metadata") if m.get("key")}
    plate = ms.find("plate")
    info["plate"] = {m.get("key"): m.get("value") for m in plate.findall("metadata")} if plate is not None else None
    info["plate_instance"] = {m.get("key"): m.get("value") for m in plate.find("model_instance").findall("metadata")} \
        if plate is not None and plate.find("model_instance") is not None else None
    info["parts_settings"] = parts
    ps = json.loads(z.read("Metadata/project_settings.config"))
    info["project_settings"] = {k: ps.get(k) for k in ("printer_model", "printer_settings_id", "print_settings_id",
                                                       "filament_settings_id", "filament_colour", "filament_type",
                                                       "detect_thin_wall", "printable_area")}
    # map part name -> mesh via part id (== sub-object id)
    by_name = {}
    for p in parts:
        by_name[p["name"]] = meshes[p["id"]]
    return by_name, info


def read_obj(path):
    objs = {}
    cur = None
    mtl_of = {}
    V = []
    F = {}
    cur_mtl = None
    with open(path) as f:
        for line in f:
            if line.startswith("v "):
                V.append([float(x) for x in line.split()[1:4]])
            elif line.startswith("f "):
                idx = [int(t.split("/")[0]) - 1 for t in line.split()[1:4]]
                key = cur if cur is not None else cur_mtl
                F.setdefault(key, []).append(idx)
                mtl_of.setdefault(key, set()).add(cur_mtl)
            elif line.startswith("o "):
                cur = line.split()[1]
            elif line.startswith("usemtl "):
                cur_mtl = line.split()[1]
    V = np.array(V, np.float64)
    return V, {k: np.array(v, np.int64) for k, v in F.items()}, {k: sorted(v) for k, v in mtl_of.items()}


def read_obj_by_material(path):
    V = []
    F = {}
    mtl = None
    with open(path) as f:
        for line in f:
            if line.startswith("v "):
                V.append([float(x) for x in line.split()[1:4]])
            elif line.startswith("usemtl "):
                mtl = line.split()[1]
            elif line.startswith("f "):
                F.setdefault(mtl, []).append([int(t.split("/")[0]) - 1 for t in line.split()[1:4]])
    return np.array(V, np.float64), {k: np.array(v, np.int64) for k, v in F.items()}


def read_mtl(path):
    mats = {}
    cur = None
    with open(path) as f:
        for line in f:
            s = line.split()
            if not s:
                continue
            if s[0] == "newmtl":
                cur = s[1]
                mats[cur] = {}
            elif s[0] == "Kd" and cur:
                mats[cur]["Kd"] = [float(x) for x in s[1:4]]
    return mats


def compact(V, F):
    """Only the vertices referenced by F (OBJ files share one vertex list)."""
    used = np.unique(F)
    remap = -np.ones(len(V), np.int64)
    remap[used] = np.arange(len(used))
    return V[used], remap[F]


if __name__ == "__main__":
    res = {"stl": {}, "core_3mf": {}, "bambu_3mf": {}, "obj_parts": {}, "identical": {}}
    stl_keys = {}
    for p in PARTS + ("combined",):
        path = os.path.join(STL, "%s_%s.stl" % (PREFIX, p))
        r = SC.check_stl(path)
        res["stl"][p] = r
        if p in PARTS:
            V, F = read_stl_arrays(path)
            stl_keys[p] = tri_key_set(V, F)
    core_parts, core_info = check_core_3mf(os.path.join(TMF, "%s_core-3mf.3mf" % PREFIX))
    res["core_3mf"]["info"] = core_info
    for p in PARTS:
        V, F = core_parts[p]
        res["core_3mf"][p] = mesh_report(V, F)
    bam_parts, bam_info = check_bambu_3mf(os.path.join(TMF, "%s_bambu-studio.3mf" % PREFIX))
    res["bambu_3mf"]["info"] = bam_info
    for p in PARTS:
        V, F = bam_parts[p]
        res["bambu_3mf"][p] = mesh_report(V, F)
    Vo, Fo, mt = read_obj(os.path.join(OBJD, "%s_5-parts.obj" % PREFIX))
    res["obj_parts"]["materials_per_object"] = mt
    res["obj_parts"]["mtl"] = read_mtl(os.path.join(OBJD, "%s.mtl" % PREFIX))
    for p in PARTS:
        Vc, Fc = compact(Vo, Fo[p])
        res["obj_parts"][p] = mesh_report(Vc, Fc)
    # painted single mesh
    Vp, Fp_by = read_obj_by_material(os.path.join(OBJD, "%s_painted-single-mesh.obj" % PREFIX))
    allF = np.vstack(list(Fp_by.values()))
    res["obj_painted"] = mesh_report(Vp, allF)
    res["obj_painted"]["faces_per_material"] = {k: int(len(v)) for k, v in Fp_by.items()}
    und = np.sort(np.concatenate([allF[:, [0, 1]], allF[:, [1, 2]], allF[:, [2, 0]]]), axis=1)
    _, cnt = np.unique(und[:, 0] * len(Vp) + und[:, 1], return_counts=True)
    res["obj_painted"]["edges_used_once"] = int((cnt == 1).sum())
    res["obj_painted"]["edges_used_gt2"] = int((cnt > 2).sum())
    # identical coordinates across formats, triangle by triangle
    for p in PARTS:
        ks = stl_keys[p]
        V, F = core_parts[p]
        kc = tri_key_set(V, F)
        V, F = bam_parts[p]
        kb = tri_key_set(V, F)
        Vc, Fc = compact(Vo, Fo[p])
        ko = tri_key_set(Vc, Fc)
        res["identical"][p] = {"stl_tris": len(ks), "core_3mf_equal": kc == ks, "bambu_3mf_equal": kb == ks,
                               "obj_equal": ko == ks}
    # A14: calibration tile skins + bed fit (stage-1 files, unchanged)
    res["tile_standing"] = SC.tile_skins(os.path.join(ROOT, "stl", "skin-calibration-tile.stl"))
    res["tile_flat"] = SC.tile_skins(os.path.join(ROOT, "stl", "skin-calibration-tile_flat-print.stl"))
    c = res["stl"]["combined"]
    size = c["size_xyz"]
    res["bed_fit_256"] = {"size_xyz": size, "fits": bool(size[0] <= 256 and size[1] <= 256 and size[2] <= 256),
                          "centre_xy": [round((c["bbox_min"][i] + c["bbox_max"][i]) / 2, 4) for i in (0, 1)]}
    print(json.dumps(res, indent=1, default=str))
