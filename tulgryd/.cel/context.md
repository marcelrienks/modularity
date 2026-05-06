# tulgryd Project Context

**Last Read:** 2026-05-06  
**Scan Mode:** Full (initial)

---

## Project Purpose

**tulgryd** — Parametric model repository and generator scripts for the ToolGrid modular workshop organization system. 

Core mission: Generate customized pegboard tiles and tool holders from dimensional input. Version-control design parameters. Rapidly iterate designs programmatically.

**Users can:**
- Generate custom pegboard tiles for exact workshop dimensions
- Create tool holders tailored to specific needs
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
├── tiles/                    # Tile generation system
│   ├── generate.py          # Main CLI tool for tile generation
│   ├── core/                # Core modules
│   │   ├── __init__.py
│   │   ├── layout_calculator.py     # Layout optimization
│   │   ├── builder.py               # 3D model building
│   │   ├── assembly_guide.py        # Assembly README generation
│   │   └── parameters.py            # Parameter definitions
│   ├── origin/              # Original hand-designed reference tiles
│   ├── output/              # Generated model outputs
│   └── readme.md
├── handles/                 # Custom tool holder models
│   └── origin/              # Original designs
├── tulgryd.f3d             # Master design file (Fusion 360)
└── readme.md               # Project overview
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
| `readme.md` | Project overview, quick start, requirements, structure |
| `tiles/readme.md` | Detailed tile generator usage, CLI options, Python API, customization |
| `tiles/origin/plan.md` | Implementation strategy, platform analysis (CadQuery recommended) |
| `tiles/core/` | Core module implementations (layout, builder, assembly guide) |
| `tiles/origin/` | Reference models (STEP files) |
| `handles/origin/` | Reference tool holder designs |

---

## File Hashes (Change Detection)

```
43476677d581344cf03d70d85fbb84fe  readme.md
2a920ddf6f378682f7ff2390e4123d00  tiles/readme.md
75c306f96f04af9f54bbc11fa9d29ad0  tiles/origin/plan.md
```

---

## Key Insights

1. **Modular Tile System:** 100×100mm standard tiles + custom edge pieces for exact dimensional fit.
2. **Assembly Automation:** Layout calculator automatically determines tile count and geometry.
3. **3D Printer Tolerance:** Calibration mode enables per-printer diameter adjustment.
4. **Quantity Coding:** Filenames encode quantity (e.g., `qty4` = print 4 copies).
5. **Recommended Platform:** CadQuery (Python + OpenSCAD fallback).
6. **Cross-Verified Design:** All specifications consistent across markdown, PNG drawing, and STEP model.

---

## Next Steps

- Review `tiles/core/` module implementations
- Test `tiles/generate.py` with sample dimensions
- Validate CadQuery export quality against reference STEP
