# tulgryd

Parametric model repository and generator scripts for the **ToolGrid** modular workshop organization system.

## Overview

tulgryd is a collection of:

1. **Models** - Parametric and pre-built 3D models for ToolGrid tiles and tool holders
2. **Generator Scripts** - Python utilities to programmatically create customized models with specific dimensions
3. **Design Files** - Fusion 360 source models for reference and modification

This allows you to:
- Generate custom pegboard tiles for your exact workshop dimensions
- Create tool holders tailored to your specific needs
- Version-control design parameters and construction logic
- Rapidly iterate on designs with programmatic variations

## Project Structure

```
tulgryd/
├── tiles/                    # Tile generation system
│   ├── generate.py          # Main CLI tool for tile generation
│   ├── core/                # Core modules (layout, modeling, assembly)
│   └── origin/              # Original hand-designed ToolGrid tiles
├── handles/                  # Custom tool holder models
│   ├── origin/              # Original designs
│   └── (generated models)   # Output from generator scripts
└── tulgryd.f3d              # Master design file (Fusion 360)
```

## Quick Start

### Generate Custom Tiles

```bash
# Generate tiles for a 250×180mm drawer
python tiles/generate.py --total-width 250 --total-length 180

# Generate calibration tile (test hole sizes)
python tiles/generate.py --calibrate --hole-diameter 4.0
```

## About the Fusion 360 Source Files

The `tulgryd.f3d` file contains the master design. For documentation or parameterization work, you can extract design data using the **fissionreactor** tool:

- See [`../fissionreactor/`](../fissionreactor/) for the export Add-In
- Requires Fusion 360 to be running with the design file open
- Generates JSON metadata for analysis or AI-based code generation

This is optional—the core tulgryd generators work independently.

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

- **tulgryd** - Parametric tile and tool holder generation system
- **fissionreactor** - Fusion 360 Add-In for model export and AI-enabled parameterization
- **ToolGrid System:** Learn about the base system at [toolgrid.io](https://toolgrid.io/) (if available)

---

Part of the **Modularity** project - custom implementations for modular workshop organization systems.
