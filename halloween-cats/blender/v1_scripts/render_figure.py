"""Renders of the stage-2 figure (Workbench engine, explicit orthographic
camera placed per view; used because the Blender window is not being drawn,
so viewport screenshots come back black).  Every image is checked for being
non-empty after rendering.

    import render_figure as R; R.setup(); R.view("front.png", (0,-1,0.0))
"""
import math
import os

import bpy
import bmesh
import numpy as np
from mathutils import Vector

import params as P

OUT = r"H:\ClaudeStuff\3d-print-team\halloween-cats\renders"
PARTS = ("black", "orange", "yellow", "green", "pink")
COLL_SEC = "SECTIONS_display_no_export"
BLACK_SHOW = (0.035, 0.035, 0.038, 1.0)      # lifted a little so form reads in renders


def lin(hexs):
    return P.hex_to_rgba(hexs)


def setup(res=(1400, 1400)):
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_WORKBENCH'
    sh = sc.display.shading
    sh.light = 'STUDIO'
    sh.color_type = 'OBJECT'
    sh.show_cavity = True
    sh.cavity_type = 'WORLD'
    sh.show_object_outline = False
    sh.show_specular_highlight = False
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = 'PNG'
    if sc.world is None:
        sc.world = bpy.data.worlds.new("World")
    sc.world.color = (0.55, 0.57, 0.61)
    sc.display.render_aa = '8'
    cam = bpy.data.objects.get("CAM_render")
    if cam is None:
        cd = bpy.data.cameras.new("CAM_render")
        cam = bpy.data.objects.new("CAM_render", cd)
        sc.collection.objects.link(cam)
    cam.data.type = 'ORTHO'
    cam.data.clip_start = 1.0
    cam.data.clip_end = 2000.0
    sc.camera = cam
    return cam


def part_colors(exact=False):
    for p in PARTS:
        ob = bpy.data.objects.get(p)
        if ob is None:
            continue
        c = lin(P.COLORS[p])
        if p == "black" and not exact:
            c = BLACK_SHOW
        ob.color = c


def show_only(names):
    names = set(names)
    for o in bpy.data.objects:
        if o.type in ('MESH',):
            o.hide_render = o.name not in names
            o.hide_viewport = False


def place(direction, target=(0, 0, 75), dist=600.0, scale=190.0, up=(0, 0, 1)):
    cam = bpy.data.objects["CAM_render"]
    d = Vector(direction).normalized()
    t = Vector(target)
    cam.location = t + d * dist
    z = d                     # camera looks along -z(local): local +z points back to the camera
    upv = Vector(up)
    if abs(z.dot(upv)) > 0.99:
        upv = Vector((0, 1, 0)) if abs(z.z) > 0.5 else Vector((0, 0, 1))
    x = upv.cross(z).normalized()
    y = z.cross(x).normalized()
    from mathutils import Matrix
    m = Matrix((x, y, z)).transposed()
    cam.rotation_euler = m.to_euler()
    cam.data.ortho_scale = scale
    return cam


def render(filename, names, direction, target=(0, 0, 75), scale=190.0, up=(0, 0, 1), exact=False):
    part_colors(exact)
    show_only(names)
    place(direction, target, scale=scale, up=up)
    path = os.path.join(OUT, filename)
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    img = bpy.data.images.load(path, check_existing=False)
    a = np.empty(img.size[0] * img.size[1] * 4, np.float32)
    img.pixels.foreach_get(a)
    a = a.reshape(-1, 4)[:, :3]
    bg = np.array([0.55, 0.57, 0.61]) ** (1 / 2.2)
    frac = float((np.abs(a - a[0]).sum(1) > 0.05).mean())
    bpy.data.images.remove(img)
    return {"path": path, "non_background_fraction": round(frac, 4)}


# ---------------------------------------------------------------- sections
def section(part, name, plane_co, plane_no, cap_color):
    """Copy `part`, cut away the half-space in +plane_no, fill the cut with a
    cap (separate object `name`_cap coloured cap_color)."""
    src = bpy.data.objects[part]
    for n in (name, name + "_cap"):
        o = bpy.data.objects.get(n)
        if o:
            me = o.data
            bpy.data.objects.remove(o, do_unlink=True)
            if me.users == 0:
                bpy.data.meshes.remove(me)
    c = bpy.data.collections.get(COLL_SEC)
    if c is None:
        c = bpy.data.collections.new(COLL_SEC)
        bpy.context.scene.collection.children.link(c)
    bm = bmesh.new()
    bm.from_mesh(src.data)
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    r = bmesh.ops.bisect_plane(bm, geom=geom, dist=1e-6, plane_co=plane_co, plane_no=plane_no,
                               clear_inner=False, clear_outer=True)
    cut_edges = [e for e in r["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
    fill = bmesh.ops.triangle_fill(bm, use_beauty=True, use_dissolve=False, edges=cut_edges,
                                   normal=Vector(plane_no))
    cap_faces = set(fill["geom"]) & set(bm.faces)
    # split caps into their own mesh
    bm2 = bm.copy()
    capidx = {f.index for f in cap_faces}
    bmesh.ops.delete(bm2, geom=[f for f in bm2.faces if f.index not in capidx], context='FACES')
    bmesh.ops.delete(bm, geom=list(cap_faces), context='FACES_ONLY')
    me1 = bpy.data.meshes.new(name)
    bm.to_mesh(me1)
    bm.free()
    me2 = bpy.data.meshes.new(name + "_cap")
    bm2.to_mesh(me2)
    bm2.free()
    o1 = bpy.data.objects.new(name, me1)
    o2 = bpy.data.objects.new(name + "_cap", me2)
    c.objects.link(o1)
    c.objects.link(o2)
    o1.color = BLACK_SHOW if part == "black" else lin(P.COLORS[part])
    o2.color = cap_color
    o1["export"] = False
    o2["export"] = False
    return [o1.name, o2.name], len(cap_faces)


CAP = {"black": (0.30, 0.30, 0.33, 1.0), "orange": (1.0, 0.55, 0.25, 1.0), "yellow": (1.0, 1.0, 0.3, 1.0),
       "green": (0.45, 0.8, 0.45, 1.0), "pink": (1.0, 0.6, 0.8, 1.0)}


def section_set(tag, plane_co, plane_no):
    names = []
    info = {}
    for p in PARTS:
        nm, ncap = section(p, "SEC_%s_%s" % (tag, p), plane_co, plane_no, CAP[p])
        names += nm
        info[p] = ncap
    return names, info
