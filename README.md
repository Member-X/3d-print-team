# 3d-print-team

A solo 3D-printing shop's design pipeline: an agent team that takes a product idea from "is this
worth making?" through concept art, spec, CAD model, printability testing, and final sign-off.

## The team

### 3d-director
**Role:** the single point of contact for any design request — orchestrates everyone else so you
don't have to remember which agent does what. Asks clarifying questions up front (especially
whether a design mates with real hardware, the highest-risk case), checks `./dot_pipeline/` for
existing in-progress work before assuming a fresh start, delegates to the rest of the team in
order, and relays questions/blockers between them and you in plain language.
**Tools/services:** `Agent` (to dispatch the rest of the team), `AskUserQuestion`, `SendMessage`,
`Read`, `Glob`, `Grep`, `Bash`.

### 3d-concept-designer
**Role:** upstream visual concept exploration, before any modeling begins. Given reference images
(e.g. a competitor product) and a description of how the new design should differ, generates a
proposed variation image, then iterates through rounds of human feedback until approved. Produces
an approved image plus a written visual brief (`./<project>/concept/brief.md`) that becomes what
`3d-planner` builds toward. Skipped when the idea is already fully specified.
**Tools/services:** `Read`, `Write`, `Glob`, `Grep`, and the `openai-image-gen` MCP server
(`generate_concept_image`, `generate_variation` — OpenAI's `gpt-image-2` model).

### 3d-planner
**Role:** translates a business/product idea (or a concept-designer brief) into a technical spec
at `./dot_pipeline/specs.md` — the contract every other agent builds against. Tags every dimension
`VERIFIED` or `ESTIMATED`, calls out mating-hardware risk explicitly, and states material,
printer constraints, and print orientation up front rather than leaving them implicit.
**Tools/services:** `Read`, `Write`, `Edit`, `Glob`, `Grep`, `WebSearch`, `WebFetch`.

### 3d-coder
**Role:** implements the spec as watertight, dimensionally correct, print-ready geometry —
parametric CAD (Fusion 360) for anything with exact-dimension mating features, mesh/OpenSCAD for
organic/freeform shapes with no critical mating dimensions. Verifies body/face counts after every
boolean operation (a silent way designs quietly break), enforces minimum wall thickness against
the spec's nozzle diameter, and compensates hole diameters for FDM shrinkage. Exports STEP, 3MF,
and STL to `./dot_pipeline/`, print-ready (bed-face at Z=0, centered in X/Y).
**Tools/services:** `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`, and Fusion 360 via the
`fusion` MCP server (`fusion_mcp_execute`, `fusion_mcp_read`, `fusion_mcp_update`,
`fusion_mcp_electronics_read`).

### 3d-tester
**Role:** tries to break the design before a customer does. Blocks on any `ESTIMATED` dimension
that mates with real hardware until it's verified or the risk is explicitly accepted in writing.
Runs drop, load, and fit/clearance tests (including clearance for hardware's *own* mounting
screws, not just its visible face), flags PLA brittleness risk on thin/stressed features and
recommends PETG/ABS with a stated reason, and checks slicer-level concerns (support needs,
bed adhesion) when a slicer is available. Writes results to `./dot_pipeline/tests.md` and a
pass/fail verdict to `./dot_pipeline/verdict.md`.
**Tools/services:** `Read`, `Write`, `Bash`, `Glob`, `Grep`, `WebSearch`, `WebFetch`, and read-only
Fusion access via `fusion_mcp_read`.

### 3d-reviewer
**Role:** final approve/reject gate, after Planner, Coder, and Tester have all produced output.
Separately checks business fit (does it solve the actual stated problem?) and technical parity
(does it actually replicate/fit the real-world object it mates with?) — a design can pass one and
fail the other. Confirms lightweight documentation exists (parameter sheet, README with
limitations/orientation/material reasoning) and sanity-checks material cost. On approval, produces
a final marketing render of the *real* built geometry (not a generated image) using Fusion's own
Render workspace, and flags if the built design visually drifted from an approved concept-designer
brief. Outputs the verdict to `./dot_pipeline/verdict.md`.
**Tools/services:** `Read`, `Write`, `Bash`, `Glob`, `Grep`, and Fusion access via
`fusion_mcp_read` / `fusion_mcp_execute` (the latter specifically for triggering the final render).

### etsy-market-research
**Role:** the only team member not focused on building — finds product ideas worth building in
the first place. Mines Etsy listings/search results and broader trend signals (seller forums,
trend roundups) for demand, competition, printability, and rough margin sanity checks, then hands
a ranked shortlist to `3d-director` once an idea is picked. Checks existing project folders first
so it doesn't recommend something already built.
**Tools/services:** `WebSearch`, `WebFetch`, `Read`, `Write`, `Glob`, `Grep`, and Claude's browser
automation tools (`preview_start`, `navigate`, `computer`, `read_page`, `find`, `form_input`,
`get_page_text`, `browser_batch`, `tabs_close`) — though Etsy's search box is confirmed (as of
2026-08-25) to silently block synthetic keyboard input, so this agent defaults to direct URL
navigation + `WebSearch` rather than repeatedly attempting the live autocomplete sweep.

## Supporting services (MCP servers)

These aren't team members themselves — they're capabilities the agents above call into.

| Server | Purpose | Backing |
|---|---|---|
| `mcp-servers/openai-vision` | Bulk image/video analysis (screenshot comparisons, reference-photo triage) without burning Claude's own context reading every frame. | OpenAI `gpt-5.4-mini` (or specified model) |
| `mcp-servers/openai-web-research` | Fetches a page (or several), extracts the readable main content locally, and answers a specific question about it — for research without pulling full page text into Claude's context. | OpenAI `gpt-5.4-mini` (or specified model) |
| `mcp-servers/openai-image-gen` | Generates and edits images from text prompts and/or reference images — powers `3d-concept-designer`'s iteration loop. | OpenAI `gpt-image-2` |
| `blender` (external) | Blender scene inspection/scripting, for projects modeled in Blender instead of Fusion. | Local Blender + MCP add-on |
| `fusion` (external) | Fusion 360 read/execute/update access — the primary CAD tool for the Coder, Tester, and Reviewer. | Local Fusion 360 + MCP add-on |

All three `openai-*` servers share one `OPENAI_API_KEY` (set as a persistent environment
variable — see each server's own README for setup) and run in their own isolated `.venv`, so
their dependencies never conflict with each other or a global Python environment. Cost/rate
limits for these are on the OpenAI account, not Claude's — the point is offloading token-heavy
work (page reading, image analysis, image generation) to a service already paid for separately.

## Typical flow

```
etsy-market-research  →  3d-director  →  [3d-concept-designer]  →  3d-planner
                                                                        ↓
                          3d-reviewer  ←  3d-tester  ←  3d-coder  ←────┘
```

`3d-director` is the only agent you need to talk to directly for a build — it decides whether
`3d-concept-designer` is needed (skipped if the idea is already fully specified) and drives the
rest of the pipeline in order, looping back to an earlier stage if a later one finds a problem
(e.g. the Tester finding an unresolved dimension routes back to the Planner, not a silent patch).
`etsy-market-research` runs independently, upstream of all of this, whenever you want ideas rather
than to build something already decided on.

## How to talk to the team

You don't need special syntax — just describe what you want in plain language, and name an agent
directly if you want to skip straight to it instead of going through the director.

**Starting a new design (goes through the director):**
> "I want to design a wall-mounted holder for cat toy wands."

The director will ask a few qualifying questions (does it mate with real hardware? printer/material
preferences? new design or a revision?) before delegating onward.

**Checking on something already in progress:**
> "What's the status of the noise maker project?"

**Asking for product ideas, bypassing the build pipeline entirely:**
> "Have the Etsy market researcher look into pet urns and memorial items."

> "Kick off the market research agent — no specific niche, just see what's trending."

**Going straight to visual concept iteration** (skips the director if you already know you want to
start from a reference image rather than a full spec):
> "Use the concept designer to make a variation of this propagation station listing photo — same
> idea, but a wave shape instead of a ring, and holding two tubes instead of one."

Then, after it generates a first pass: *"Move the tubes closer together and make the base wider"* —
keep giving feedback in plain language each round until you approve one.

**Going straight to a specific pipeline stage**, when you don't need the whole flow (e.g. re-testing
after a manual tweak, or asking for one more test without redoing the spec):
> "Have the tester re-check the clearance on the current propagation station model."

> "Ask the reviewer to do a final render of the noise maker now that it's done."

If you're not sure who should handle something, just describe the goal to the director — it's built
to figure out the right agent and ask you anything it's missing, rather than you needing to know
the team roster by heart.

## Project folders

Each product gets its own top-level folder (e.g. `noise-maker/`, `cat-toy-holder/`) containing:
- `dot_pipeline/` — `specs.md`, `tests.md`, `verdict.md` (the pipeline's working record)
- `step/`, `stl/`, `3mf/` — exported geometry
- `concept/` — visual concept images + brief, if `3d-concept-designer` was used
- `README.md` — what the print is, for anyone who wasn't in the room when it was designed
- `parameters.md` — enough dimensional/build detail to recreate the design from scratch

`market-research/findings.md` is a standalone running log of `etsy-market-research` output, not
tied to any one project.
