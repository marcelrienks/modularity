# tulgryd

Parametric model repository and generator scripts for the **ToolGrid** modular workshop organization system.

## Overview

tulgryd is a collection of:

1. **Models** - Parametric and pre-built 3D models for ToolGrid tiles and tool holders
2. **Generator Scripts** - Python utilities to programmatically create customized models with specific dimensions
3. **Design Data** - Complete design information extracted from Fusion 360 source files

This allows you to:
- Generate custom pegboard tiles for your exact workshop dimensions
- Create tool holders tailored to your specific needs
- Version-control design parameters and construction logic
- Rapidly iterate on designs with programmatic variations

## Project Structure

```
tulgryd/
├── tiles/                          # Tile generation system
│   ├── generate.py                # Main CLI tool for tile generation
│   ├── core/                      # Core modules (layout, modeling, assembly)
│   └── origin/                    # Original hand-designed ToolGrid tiles
├── handles/                        # Custom tool holder models
│   ├── origin/                    # Original designs
│   └── (generated models)         # Output from generator scripts
├── export_fusion360_data.py       # Fusion 360 export utility (separate)
├── export_fusion360_guide.md      # Guide for export tool
└── tulgryd.f3d                    # Master design file (Fusion 360)
```

## Quick Start

### Generate Custom Tiles

```bash
# Generate tiles for a 250×180mm drawer
python tiles/generate.py --total-width 250 --total-length 180

# Generate calibration tile (test hole sizes)
python tiles/generate.py --calibrate --hole-diameter 4.0
```

### Export Design Data (Optional)

The `export_fusion360_data.py` tool is included to help extract design data from Fusion 360 files for documentation and future parameterization:

1. Open a design file in Fusion 360
2. Tools > Add-ins > Scripts and Add-ins > Scripts tab
3. Right-click `export_fusion360_data` > Run
4. Select output directory

See [`export_fusion360_guide.md`](./export_fusion360_guide.md) for detailed usage.

## About the Fusion 360 Export Tool

The `export_fusion360_data.py` script is a **separate utility** included for design documentation purposes. It is not part of the core tulgryd system but rather a helper Add-In that:

- Extracts complete design data (parameters, sketches, features, timeline) from the active `.f3d` file in Fusion 360
- Outputs structured JSON metadata about the models
- Enables conversion of hand-designed models into parameterized generators

**Note:** This tool requires Fusion 360 to be running with a design file open. It is optional—the core tulgryd generators work independently.

## Generator Scripts

Generator scripts take design parameters as input and programmatically create models. Examples:

- **Tiles:** Input dimensions → Output optimized pegboard tile layout
- **Tool Holders:** Input tool dimensions → Output custom organizer

Generators produce:
- STL files (for 3D printing)
- STEP files (for further design work)
- Assembly guides (with layout diagrams)

## Design Versioning

Design data exported from Fusion 360 models is stored as JSON in the structure:

```
model_name/
└── origin/
    └── model_name.json
```

This enables:
- Design documentation
- Parameter tracking over time
- Git version control of design intent
- Reference for building new generators

## Requirements

- Python 3.8+
- CadQuery 2.4+ (for tile generation)
- Fusion 360 (optional, only for using export tool)

## Getting Started

1. **Browse existing models** - Check `tiles/origin/` and `handles/origin/` for reference designs
2. **Generate custom tiles** - Run `tiles/generate.py` with your dimensions
3. **Print and assemble** - Follow generated assembly guides

For more details on tile generation, see `tiles/` directory.

## Learn More

- **Parent Project:** See [`../README.md`](../README.md) for overview of Modularity project
- **Fusion 360 Export:** See [`export_fusion360_guide.md`](./export_fusion360_guide.md)
- **ToolGrid System:** Learn about the base system at [toolgrid.io](https://toolgrid.io/) (if available)

---

Part of the **Modularity** project - custom implementations for modular workshop organization systems.
