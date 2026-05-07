# tulgryd Project Context

**Last Read:** 2026-05-07  
**Scan Mode:** Full (updated)

---

## Project Purpose

**tulgryd** — Collection of independent parametric model generator tools for the ToolGrid modular workshop organization system.

Core model: each tool lives in its own directory, has its own CLI entry point and documentation, and is used entirely independently. No global entry point or shared API.

**Current tools:**
- **tiles/** — Generates pegboard tiles to fill exact wall dimensions (operational, older style)
- **handles/** — Generates custom grip handles for tool holders (in development, new reference style)

**Users can:**
- Generate custom pegboard tiles for exact workshop dimensions (tiles tool)
- Generate custom grip handles for tool holders (handles tool)
- Version-control design parameters and construction logic via Git
- Iterate on designs with programmatic variations

---

## Architecture & Tech Stack

### Languages & Frameworks
- **Python 3.8+** (core generator)
- **CadQuery 2.4+** (parametric 3D modeling — RECOMMENDED)
- **OpenSCAD** (fallback option)
- **Fusion 360** (optional source; export via fissionreactor Add-In)

### Core Dependencies
- NumPy (numerical computation)
- Click (CLI framework)
- Jinja2 (template engine for assembly guides)
- pytest (testing framework)

### Project Structure
```
tulgryd/
├── tiles/                    # Tile generator tool (operational, older style)
│   ├── generate.py          # CLI entry point
│   ├── README.md            # Tool documentation
│   ├── core/                # Core modules (layout, builder, assembly guide)
│   ├── origin/              # Reference STEP models + plan.md
│   └── output/              # Generated model outputs
├── handles/                 # Handles generator tool (in development, new style)
│   ├── generate.py          # CLI entry point (in development)
│   ├── README.md            # Tool documentation
│   ├── core/                # Core modules (in development)
│   ├── origin/              # Reference design + handles.json
│   └── output/              # Generated model outputs
├── tulgryd.f3d             # Master design file (Fusion 360)
└── README.md               # Repository overview
```

---

## Key Workflows

### 1. Tile Generation Workflow
**Input:** `--total-width` + `--total-length` (mm)  
**Process:** LayoutCalculator → ModelBuilder → Assembly Guide Generation  
**Output:** 
- Unique STL/STEP files with qty-coded filenames (e.g., `tile_100x100_qty4.stl`)
- `ASSEMBLY_README.md` with layout diagram + assembly instructions
- `layout_diagram.txt` (ASCII visualization)

**Example:**
```bash
python generate.py --total-width 250 --total-length 180
```
→ Outputs tiles filling exactly 250×180mm using 100×100mm standard tiles + custom edge pieces.

### 2. Calibration Mode
**Purpose:** Test hole diameter tolerance for specific 3D printer/material.  
**Input:** `--calibrate --hole-diameter X.X`  
**Output:** Single test tile with 5 holes (diameters: -0.2, -0.1, 0, +0.1, +0.2 from base)  
**Use Case:** Print, test screw fit, determine adjustment value for production.

### 3. Parametric Customization
All dimensions configurable:
- Grid spacing (default 10mm)
- Hole diameter (default 4.0mm; adjustable via `--hole-adjust`)
- Tab/slot dimensions
- Wall thickness (6mm standard)
- Tile geometry (100×100mm standard, custom edge pieces)

### 4. Output Formats
- **STL** (3D printing, default)
- **STEP** (CAD/further design work)
- **Both** (simultaneous export)

---

## Tile Specifications (Standard 100×100mm)

| Property | Value |
|----------|-------|
| Grid | 10×10 holes (100 mounting points) |
| Hole Diameter | 4mm (M3 compatible) |
| Hole Adjustment | Via `--hole-adjust` (e.g., ±0.2mm) |
| Thickness | 6mm |
| Tabs (T/R edges) | Ø3.8mm |
| Slots (B/L edges) | Ø4.0mm |
| Grid Spacing | 10mm |

**Custom Edge Tiles:** Variable dimensions (<100mm), partial grid, compatible interlocking.

---

## Documentation Map

| File | Purpose |
|------|---------|
| `README.md` | Repository overview, tool index, shared requirements |
| `tiles/README.md` | Tiles tool: CLI usage, options, output structure, specs, Python API |
| `tiles/origin/plan.md` | Tiles implementation strategy, platform analysis |
| `handles/README.md` | Handles tool: CLI usage, parameters, output structure, specs |
| `handles/origin/handles.json` | Fusion 360 exported parameters (source of truth for reference params) |
| `.specify/memory/constitution.md` | Governing principles, dev workflow, repo model |

---

## File Hashes (Change Detection)

```
e34c1c9151e0cb8a8a35eeca52f576dc  README.md
2a920ddf6f378682f7ff2390e4123d00  tiles/README.md
75c306f96f04af9f54bbc11fa9d29ad0  tiles/origin/plan.md
247f46295470841086da7d46f770ed6e  handles/README.md
554ea943ff5b7dad458bd8e2857cdb9a  .specify/memory/constitution.md
```

---

## Key Insights

1. **Independent Tools:** No global entry point/API. Each tool is standalone with own CLI.
2. **Style Split:** `tiles/` = older conventions; `handles/` = new reference implementation style.
3. **Modular Tile System:** 100×100mm standard tiles + custom edge pieces for exact dimensional fit.
4. **Assembly Automation:** Layout calculator determines tile count and geometry automatically.
5. **3D Printer Tolerance:** Calibration mode enables per-printer diameter adjustment (tiles).
6. **Quantity Coding:** Filenames encode quantity (e.g., `qty4` = print 4 copies).
7. **Recommended Platform:** CadQuery (Python + OpenSCAD fallback).
8. **Handles Params:** `--diameter` (1–10mm) + `--height` (0.5–5mm), both required, no defaults.

---

## Next Steps

- Review `tiles/core/` module implementations
- Test `tiles/generate.py` with sample dimensions
- Validate CadQuery export quality against reference STEP
