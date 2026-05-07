# Parametric Handles Generator

A Python CLI tool for generating custom 3D-printable tool holder handles with parametric grip diameter and height. Built with CadQuery and exportable to STL/STEP CAD formats.

## Quick Start

### Installation

```bash
cd handles
pip install -r requirements.txt
```

### Basic Usage

Generate a handle with 2.6mm grip diameter and 2.0mm height:

```bash
python generate.py --diameter 2.6 --height 2.0
```

This creates:
- `output/handle_d2.6_h2.0.stl` — 3D model (STL format)
- `output/handle_d2.6_h2.0_README.md` — Assembly guide with print settings

### Multiple Formats

Export to both STL and STEP CAD formats:

```bash
python generate.py --diameter 3.5 --height 1.5 --format both
```

Supported formats: `stl`, `step`, `both` (default: `stl`)

### Custom Output Directory

```bash
python generate.py --diameter 2.6 --height 2.0 --output-dir ./models
```

### View Help

```bash
python generate.py --help
```

## Parameter Ranges

| Parameter | Min | Max | Unit |
|-----------|-----|-----|------|
| **Diameter** | 1.0 | 10.0 | mm |
| **Height** | 0.5 | 5.0 | mm |

Out-of-range values are rejected with clear error messages.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Parameter validation error |
| 2 | Geometry building failed |
| 3 | Export failed (permissions, disk space) |
| 4 | User cancelled (file overwrite declined) |

## Features

✓ **Parametric Design** — Custom diameter and height  
✓ **Multi-Format Export** — STL and STEP formats  
✓ **Auto Assembly Guide** — Markdown documentation with print settings  
✓ **Geometry Validation** — Ensures watertight, exportable models  
✓ **Interactive Overwrite Prompt** — Prevents accidental file loss  
✓ **Cross-Platform** — Works on Linux, macOS, Windows

## Generated Assembly Guide

Each handle generation creates a README.md with:
- Specifications table (diameter, height, material, format)
- Print settings for PLA, PETG, and TPU materials
- Step-by-step assembly instructions
- Troubleshooting guides for common 3D printing issues
- Maintenance and care instructions

## Testing

Run the full test suite:

```bash
python -m pytest tests/ -v
```

Run specific test categories:

```bash
python -m pytest tests/unit/ -v          # Parameter validation
python -m pytest tests/contract/ -v      # CLI interface
python -m pytest tests/integration/ -v   # End-to-end workflows
```

## Architecture

```
handles/
├── generate.py              Main CLI entry point
├── core/
│   ├── parameters.py        Parameter validation
│   ├── builder.py           CadQuery geometry construction
│   ├── exporter.py          STL/STEP export
│   ├── assembly_guide.py    Assembly documentation
│   └── templates/           Jinja2 templates
├── output/                  Generated models (runtime)
└── tests/
    ├── unit/                Parameter validation tests
    ├── integration/         End-to-end workflow tests
    └── contract/            CLI interface tests
```

## Troubleshooting

### File Permission Error

**Problem**: `ERROR: Output directory not writable`

**Solution**: Check directory permissions. Try with `--output-dir` in a writable location:
```bash
python generate.py --diameter 2.6 --height 2.0 --output-dir ~/Desktop/handles
```

### Validation Error

**Problem**: `ERROR: diameter must be between 1.0 and 10.0 mm`

**Solution**: Check parameter ranges. Valid values:
- Diameter: 1.0–10.0mm
- Height: 0.5–5.0mm

### Out of Disk Space

**Problem**: `ERROR: Export failed - No space left on device`

**Solution**: Free up disk space or specify alternative output directory with more space.

## Performance

Typical generation time: <1 second (geometry + export + documentation)

## Requirements

- Python 3.8+
- CadQuery 2.4+
- Click 8.0+
- Jinja2 3.0+
- pytest 7.0+ (testing only)
- NumPy 1.20+

See [requirements.txt](./requirements.txt) for exact versions.

## License

Part of the Tulgryd modular design system.

### Output

```
output/
├── handle_d2.6_h2.0.stl           # 3D model (STL)
├── handle_d2.6_h2.0.step          # 3D model (STEP, if requested)
└── handle_d2.6_h2.0_README.md     # Assembly guide with specs and printing tips
```

Filenames encode parameters for traceability.

## Handle Specifications

The handle geometry is derived from the reference model in `origin/handles.json`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `handles_diameter` | 2.6mm | Diameter of the grip end |
| `handles_height` | 2.0mm | Height of handle center from gryd surface (i.e., diameter/2 + height) |

Reference (internal) parameters are locked and version-controlled in `origin/handles.json` — these are not exposed as CLI options.

## Project Structure

```
handles/
├── generate.py          # CLI entry point
├── README.md            # This file
├── core/                # Core modules
│   ├── parameters.py    # Parameter definitions and validation
│   ├── builder.py       # 3D geometry construction (CadQuery)
│   └── assembly_guide.py # Assembly README generation
├── origin/              # Reference design data
│   └── handles.json     # Fusion 360 exported parameters (source of truth)
└── output/              # Generated models (gitignored)
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Validation error (invalid parameters) |
| 2 | Geometry error |
| 3 | Export error |
