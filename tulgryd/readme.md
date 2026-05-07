# tulgryd

Parametric model repository and generator scripts for the **ToolGrid** modular workshop organization system.

## Overview

tulgryd is a collection of independent parametric model generator tools. Each tool lives in its own directory, has its own CLI entry point, and is used entirely independently. There is no global entry point or shared API.

Each tool:
- Accepts user parameters via its own CLI
- Generates 3D models (STL, STEP) ready for printing or CAD work
- Produces assembly guides alongside generated models
- Is documented independently

## Tools

| Tool | Directory | Status | Description |
|------|-----------|--------|-------------|
| Tiles | [`tiles/`](tiles/README.md) | Operational | Generates modular pegboard tiles to fill exact wall dimensions |
| Handles | [`handles/`](handles/README.md) | Operational | Generates custom grip handles with parametric diameter/height; exports STL/STEP with auto assembly guides |

> **Note:** Each tool has its own `README.md` with usage instructions, CLI reference, and output details.

## Project Structure

```
tulgryd/
├── tiles/                    # Tile generator tool
│   ├── generate.py          # CLI entry point
│   ├── README.md            # Tool documentation
│   ├── core/                # Core modules
│   ├── origin/              # Reference models
│   └── output/              # Generated outputs
├── handles/                  # Handles generator tool
│   ├── generate.py          # CLI entry point (in development)
│   ├── README.md            # Tool documentation
│   ├── core/                # Core modules (in development)
│   ├── origin/              # Reference models and parameters
│   └── output/              # Generated outputs
└── tulgryd.f3d              # Master Fusion 360 design file
```

## Shared Requirements

- Python 3.8+
- CadQuery 2.4+ (`pip install cadquery`)

Individual tools may have additional dependencies — see each tool's `README.md`.

## Design Versioning

Reference design data exported from Fusion 360 is stored as JSON:

```
tool_name/
└── origin/
    └── tool_name.json
```

This enables parameter tracking over time, Git version control of design intent, and a reference baseline for generator scripts.

## About the Fusion 360 Source Files

The `tulgryd.f3d` file contains the master design. Design data can be extracted using the **fissionreactor** Add-In (see `../fissionreactor/`) — this is optional and not required to use the generators.
- **ToolGrid System:** Learn about the base system at [toolgrid.io](https://toolgrid.io/) (if available)

---

Part of the **Modularity** project - custom implementations for modular workshop organization systems.
