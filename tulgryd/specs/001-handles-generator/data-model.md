# Data Model: Handles Generator

**Phase**: 1 (Design)  
**Feature**: Parametric Handles Generator  
**Date**: 2026-05-06

## Entity: Handle Model

### Definition
A Handle Model is a 3D parametric geometry representing a customizable tool grip/holder component. It is defined by two user-provided dimensions (diameter, height) and 23 locked reference parameters that enforce structural and geometric constraints.

### User Parameters (Exposed)

| Parameter | Type | Range | Unit | Description | Source |
|-----------|------|-------|------|-------------|--------|
| `diameter` | float | 1.0–10.0 | mm | Outer diameter of grip end | User input (required) |
| `height` | float | 0.5–5.0 | mm | Height of grip center from mounting surface | User input (required) |

### Reference Parameters (Locked)

Derived from `handles/origin/handles.json`. **NOT exposed to CLI.** Embedded as constants in `HandleParameters` class.

| Parameter ID | Value | Unit | Purpose |
|--------------|-------|------|---------|
| d165 | 0.3 | mm | Fillet radius (edge smoothing) |
| d144 | 0.6 | mm | Wall thickness bottom layer |
| d146 | -0.01 | mm | Draft angle compensation |
| d149 | 0.2 | mm | Surface offset tolerance |
| d176 | 2.6 | mm | Base diameter (reference) |
| d178 | 3.3 | mm | Upper diameter |
| d180 | 1.6 | mm | Transition radius |
| d183 | 1.6 | mm | Mounting interface width |
| d189 | 1.7 | mm | Core thickness |
| d191–d207 | [various] | mm/deg | Derived geometric constraints |

**Interpretation**: Reference params are immutable design rules that ensure structural integrity regardless of user diameter/height choices. They represent learned tolerances and material science decisions from the original design.

### Attributes

- **grip_surface**: Outer cylindrical surface (diameter-controlled)
- **mounting_interface**: Base geometry for grid attachment (locked)
- **structural_geometry**: Internal features ensuring rigidity (locked reference params)
- **layer_structure**: Height-dependent subdivision (2-3 layers typical)

### Relationships

```
Handle Model
├─ Created from: (diameter, height, reference_params)
├─ Generates: Output File (STL or STEP)
└─ Paired with: Assembly Guide README
```

### Validation Rules

1. **Parameter Validation**:
   - `diameter` ∈ [1.0, 10.0] mm (inclusive)
   - `height` ∈ [0.5, 5.0] mm (inclusive)
   - Both must be positive floats; no NaN/infinity

2. **Geometric Validation**:
   - CadQuery `Shape.isValid()` == True (passes topology checks)
   - CadQuery `isClosed()` == True (watertight; no open edges)
   - Export attempt succeeds (serialization validates further)

3. **Naming Rules**:
   - Filename: `handle_d{diameter}_h{height}.{ext}` (ext = stl or step)
   - Assembly guide: `handle_d{diameter}_h{height}_README.md`
   - No special characters; underscores only; precision preserved to input float

---

## Entity: Generation Output

### Definition
A file artifact produced by the Handle Model builder—either STL (for 3D printing) or STEP (for CAD refinement). Includes metadata in filename encoding model parameters. Paired with assembly guide document.

### Attributes

| Attribute | Type | Example | Purpose |
|-----------|------|---------|---------|
| `file_path` | string | `./output/handle_d2.6_h2.0.stl` | Full path to exported file |
| `file_format` | enum | stl, step | Export format |
| `file_size` | int | 45000 bytes | Validates successful export |
| `parameter_diameter` | float | 2.6 | User input (encoded in name) |
| `parameter_height` | float | 2.0 | User input (encoded in name) |
| `export_timestamp` | ISO 8601 | 2026-05-06T14:30:00Z | When file created |
| `integrity_validated` | bool | True | Geometric + export validation passed |

### Relationships

```
Generation Output
├─ File on Disk (STL or STEP)
├─ Paired with: Assembly Guide README
└─ Traceable to: Specific (diameter, height) parameters via filename
```

---

## Entity: Assembly Guide

### Definition
Auto-generated markdown document providing usage instructions, specifications, and troubleshooting for a specific Handle Model output. Generated once per model; overwrites if parameters repeated.

### Attributes

| Section | Content Type | Example |
|---------|--------------|---------|
| **Header** | Metadata | Handle d2.6mm h2.0mm — Generated 2026-05-06 |
| **Specifications** | Table | Diameter: 2.6mm, Height: 2.0mm, Layer count: 3, Material: PLA |
| **Print Settings** | Recommendations | Nozzle: 200°C, Bed: 60°C, Speed: 40mm/s, Supports: None |
| **Assembly** | Steps + diagram | Step 1: Print all files. Step 2: Inspect layers. Step 3: Attach to grid (interlocking interface). ASCII diagram included |
| **Troubleshooting** | Problem→Solution | "Grip too loose? Re-print with +0.1mm diameter adjustment. See main generator docs." |
| **Footer** | Metadata | File location, generation command, reference to main spec |

### Naming

`handle_d{diameter}_h{height}_README.md` — Parallel to model filename for easy discovery.

---

## Data Flow Diagram

```
User Input
  ├─ --diameter (required, float)
  ├─ --height (required, float)
  ├─ --format (optional, default=stl)
  └─ --output-dir (optional, default=./output)
        ↓
Parameter Validation (parameters.py)
  ├─ Type check (float)
  ├─ Range check (diameter 1–10, height 0.5–5)
  └─ [Error → exit with message]
        ↓
Handle Model Build (builder.py)
  ├─ Create HandleParameters instance
  ├─ Execute CadQuery sketch + extrude
  ├─ Apply reference parameter constraints
  └─ Return CadQuery Shape object
        ↓
Geometric Validation (builder.py)
  ├─ Shape.isValid()
  ├─ Shape.isClosed()
  └─ [Error → exit with message]
        ↓
Export + Validation (exporter.py)
  ├─ Write STL (or STEP or both)
  ├─ Verify file size > 0
  ├─ Attempt parse/re-import (extra validation)
  └─ [Error → cleanup + exit]
        ↓
File Overwrite Check
  ├─ File exists? → Prompt user "overwrite? [y/N]"
  ├─ User response: y/yes → Continue
  ├─ User response: n/no/empty → Exit gracefully
  └─ File not exist → Skip this step
        ↓
Output Files Created
  ├─ handle_d{d}_h{h}.stl/step (or both)
  └─ [SUCCESS]
        ↓
Assembly Guide Generation (assembly_guide.py)
  ├─ Render Jinja2 template with (diameter, height, timestamp)
  ├─ Write handle_d{d}_h{h}_README.md
  └─ [SUCCESS]
        ↓
CLI Exit Code: 0 (success)
```

---

## State & Constraints

### Handle Model States

```
┌─────────────────────────────────┐
│     Valid Input Received        │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│    Validated & Constrained      │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│    Geometry Built (CadQuery)    │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│  Exported to STL/STEP (Disk)    │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│  Assembly Guide Generated       │
└─────────────────────────────────┘
```

**Failure Points** (user sees error message and exits):
- Invalid parameter type or range
- CadQuery geometry fails validation (isValid/isClosed)
- Export fails (serialization error)
- Output directory not writable
- User declines file overwrite

**Terminal Success State**: Both files created on disk; exit code 0.

