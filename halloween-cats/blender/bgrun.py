"""Run a long Blender step without holding the MCP call open.

    import bgrun; bgrun.run("tag", fn, *args)      # returns at once
The step runs on Blender's main thread from a one-shot app timer; its state
(queued / running / done / error, seconds, JSON result or traceback) is written
to scratchpad/bg/<tag>.json, which is polled from outside Blender.
"""
import json
import os
import time
import traceback

import bpy

BG = r"C:\Users\steve\AppData\Local\Temp\claude\H--ClaudeStuff-3d-print-team\803b752c-0c19-4c39-a372-657e0ca1ec54\scratchpad\bg"


def _conv(o):
    if hasattr(o, "item"):
        try:
            return o.item()
        except Exception:
            pass
    if hasattr(o, "tolist"):
        return o.tolist()
    return str(o)


def _write(path, d):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(d, f, default=_conv, indent=1)
    os.replace(tmp, path)


def status_path(tag):
    return os.path.join(BG, tag + ".json")


def run(tag, fn, *args, **kw):
    os.makedirs(BG, exist_ok=True)
    path = status_path(tag)
    _write(path, {"tag": tag, "state": "queued", "t": time.strftime("%H:%M:%S")})

    def job():
        t0 = time.time()
        _write(path, {"tag": tag, "state": "running", "start": time.strftime("%H:%M:%S")})
        try:
            res = fn(*args, **kw)
            _write(path, {"tag": tag, "state": "done", "secs": round(time.time() - t0, 1),
                          "end": time.strftime("%H:%M:%S"), "result": res})
        except Exception:
            _write(path, {"tag": tag, "state": "error", "secs": round(time.time() - t0, 1),
                          "end": time.strftime("%H:%M:%S"), "error": traceback.format_exc()})
        return None
    bpy.app.timers.register(job, first_interval=0.2)
    return path
