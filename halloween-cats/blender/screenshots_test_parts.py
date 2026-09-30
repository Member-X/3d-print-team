"""Viewport screenshots of the stage-1 test parts (screen.screenshot_area, never
render_viewport_to_path).  Section objects are display-only copies kept in
SECTIONS_display_no_export.

    import sys, importlib
    sys.path.insert(0, r"H:/ClaudeStuff/3d-print-team/halloween-cats/blender")
    import screenshots_test_parts as S; importlib.reload(S)
"""
import bpy
import bmesh
import math
import sys
import importlib
import mathutils

HERE = r"H:\ClaudeStuff\3d-print-team\halloween-cats\blender"
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import params as P  # noqa: E402
import build_test_parts as B  # noqa: E402
importlib.reload(P)
importlib.reload(B)

OUT = r"H:\ClaudeStuff\3d-print-team\halloween-cats\renders"
COLL_SEC = "SECTIONS_display_no_export"
SHOT_BLACK = (0.045, 0.045, 0.045, 1.0)   # lightened from #111111 for legibility in shots


def view3d():
    for w in bpy.context.window_manager.windows:
        for a in w.screen.areas:
            if a.type == 'VIEW_3D':
                r = [r for r in a.regions if r.type == 'WINDOW'][0]
                return w, a, r
    raise RuntimeError("no 3D view")


def setup_viewport():
    w, a, r = view3d()
    s = a.spaces.active
    s.shading.type = 'SOLID'
    s.shading.color_type = 'OBJECT'
    s.shading.light = 'STUDIO'
    s.shading.show_cavity = True
    s.shading.cavity_type = 'WORLD'
    s.shading.show_object_outline = True
    s.shading.show_xray = False
    s.shading.background_type = 'VIEWPORT'
    s.shading.background_color = (0.62, 0.64, 0.68)
    s.overlay.show_floor = False
    s.overlay.show_axis_x = False
    s.overlay.show_axis_y = False
    s.overlay.show_ortho_grid = False
    s.overlay.show_cursor = False
    s.overlay.show_extras = False
    s.show_region_toolbar = False
    s.show_region_ui = False
    s.clip_start = 0.1
    s.clip_end = 5000
    return {"region": (r.width, r.height)}


def box_obj(name, lo, hi):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = mathutils.Vector([lo[i] if v.co[i] < 0 else hi[i] for i in range(3)])
    return B.bm_to_obj(bm, name, B.coll(B.COLL_WORK))


def section(src_name, sec_name, lo, hi, color=None):
    src = bpy.data.objects[src_name]
    B.remove_obj(sec_name)
    d = src.copy()
    d.data = src.data.copy()
    d.name = sec_name
    d.parent = None
    d.matrix_world = src.matrix_world.copy()
    B.coll(COLL_SEC).objects.link(d)
    for c in list(d.users_collection):
        if c.name != COLL_SEC:
            c.objects.unlink(d)
    # box in the section object's local frame -> put it at the same transform
    bx = box_obj("_secbox", lo, hi)
    bx.matrix_world = d.matrix_world.copy()
    B.apply_boolean(d, bx, 'INTERSECT')
    B.remove_obj("_secbox")
    d["export"] = False
    if color:
        d.color = color
    return d


def cap(sec_name, axis, value, sign, color, lift=0.02):
    """Copy the faces of a section object that lie in the cut plane into a
    separate, lightly offset object so the cut face reads clearly."""
    src = bpy.data.objects[sec_name]
    i = "xyz".index(axis)
    bm = bmesh.new()
    bm.from_mesh(src.data)
    keep = [f for f in bm.faces if all(abs(v.co[i] - value) < 1e-4 for v in f.verts)
            and f.normal[i] * sign > 0.99]
    drop = [f for f in bm.faces if f not in set(keep)]
    bmesh.ops.delete(bm, geom=drop, context='FACES')
    for v in bm.verts:
        v.co[i] += sign * lift
    name = sec_name + "_cap"
    ob = B.bm_to_obj(bm, name, B.coll(COLL_SEC), color)
    ob.matrix_world = src.matrix_world.copy()
    ob["export"] = False
    return ob, len(keep)


def show_only(names):
    for o in bpy.data.objects:
        vis = o.name in names
        o.hide_set(not vis)
        o.hide_viewport = False


def shot(filename, view=None, names=(), persp=None, rot=None, loc=None, dist=None, frame=True,
         zoom_pad=1.0):
    show_only(set(names))
    w, a, r = view3d()
    s = a.spaces.active
    with bpy.context.temp_override(window=w, area=a, region=r):
        if view:
            bpy.ops.view3d.view_axis(type=view)
        rv = s.region_3d
        if rot is not None:
            rv.view_rotation = mathutils.Euler([math.radians(x) for x in rot], 'XYZ').to_quaternion()
        if persp:
            rv.view_perspective = persp
        if frame:
            bpy.ops.view3d.view_all(center=False)
        if loc is not None:
            rv.view_location = loc
        if dist is not None:
            rv.view_distance = dist
        elif zoom_pad != 1.0:
            rv.view_distance *= zoom_pad
    bpy.context.view_layer.update()
    for _ in range(2):
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    path = OUT + "\\" + filename
    with bpy.context.temp_override(window=w, area=a, region=r):
        bpy.ops.screen.screenshot_area(filepath=path)
    return path
