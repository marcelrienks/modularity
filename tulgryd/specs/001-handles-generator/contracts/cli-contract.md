# Contract: CLI Interface

**Phase**: 1 (Design)  
**Feature**: Parametric Handles Generator  
**Date**: 2026-05-06  
**Contract Type**: User-facing CLI specification

## Command Signature

```bash
python handles/generate.py [OPTIONS]
```

## Required Options

```
--diameter FLOAT    Grip diameter in mm [1.0–10.0]. REQUIRED.
--height FLOAT      Grip height in mm [0.5–5.0]. REQUIRED.
```

## Optional Options

```
--format [stl|step|both]     Export format (default: stl)
--output-dir PATH            Output directory (default: ./output)
--help                       Show help message and exit
--version                    Show version and exit
```

## Exit Codes

| Code | Meaning | Example |
|------|---------|---------|
| 0 | Success (files created, guides generated) | Generated handle_d2.6_h2.0.stl + README |
| 1 | Input validation error | "Error: diameter must be between 1.0 and 10.0" |
| 2 | Geometry building error | "Error: CadQuery shape validation failed" |
| 3 | Export error | "Error: STL serialization failed (check permissions)" |
| 4 | User aborted (file overwrite declined) | "Aborted." |

## Error Messages (User-Facing)

### Validation Errors

```
❌ ERROR: diameter required. Usage: generate.py --diameter <float> --height <float>
❌ ERROR: height required. Usage: generate.py --diameter <float> --height <float>
❌ ERROR: diameter must be between 1.0 and 10.0 mm (got: <value>)
❌ ERROR: height must be between 0.5 and 5.0 mm (got: <value>)
❌ ERROR: diameter must be a number (got: '<value>')
❌ ERROR: height must be a number (got: '<value>')
❌ ERROR: output-dir does not exist and cannot be created: <path>
❌ ERROR: output-dir is not writable: <path>
```

### Geometry/Export Errors

```
❌ ERROR: Geometry validation failed (CadQuery Shape.isValid() returned False)
❌ ERROR: Geometry is not watertight (CadQuery Shape.isClosed() returned False)
❌ ERROR: STL export failed: <reason>
❌ ERROR: STEP export failed: <reason>
```

### User Interaction

```
⚠️  File exists: ./output/handle_d2.6_h2.0.stl
   Overwrite? [y/N]: 
```

If user enters 'y' or 'yes' → Continue  
If user enters anything else or EOF → "Aborted."

## Help Output

```
Usage: python generate.py [OPTIONS]

Generate custom parametric handle models for ToolGrid workshop organization system.

Options:
  --diameter FLOAT    Grip diameter in mm [required; range: 1.0–10.0]
  --height FLOAT      Grip height in mm [required; range: 0.5–5.0]
  --format TEXT       Export format: stl, step, or both [default: stl]
  --output-dir PATH   Output directory [default: ./output]
  --help              Show this help message
  --version           Show version

Examples:
  # Generate standard handle (2.6mm diameter, 2.0mm height)
  python generate.py --diameter 2.6 --height 2.0

  # Generate custom handle in STEP format
  python generate.py --diameter 3.0 --height 1.5 --format step

  # Generate in custom output directory
  python generate.py --diameter 2.6 --height 2.0 --output-dir ./my_models

  # Export to both STL and STEP
  python generate.py --diameter 2.6 --height 2.0 --format both

For more information, see: <project_url>
```

## Success Output

```
✓ Generated: handle_d2.6_h2.0.stl (45.2 KB)
✓ Generated: handle_d2.6_h2.0_README.md (2.5 KB)
✓ Ready for 3D printing!

Output directory: ./output
Total time: 0.8 seconds
```

## Important Behaviors

1. **Parameter Requirement**: Both `--diameter` and `--height` MUST be provided; script exits with error if missing.
2. **No Defaults**: No default values for diameter/height; explicit intent required.
3. **File Overwrite Confirmation**: If output file exists, user is prompted and must explicitly confirm (default is 'N' = no).
4. **Exit on Validation Failure**: If any validation fails, script exits immediately (no partial outputs).
5. **Output Directory Auto-Creation**: If `--output-dir` specified but doesn't exist, attempt to create it; error if creation fails.
6. **Filename Encoding**: Parameter values preserved in filename with float precision (e.g., `handle_d2.6_h2.0.stl` not `handle_d2p6_h2p0.stl`).

