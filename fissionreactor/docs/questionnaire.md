# Answer the Design Questionnaire

Copy and complete `questionnaire_template.json` to capture design intent and context that AI needs.

## Overview

The questionnaire bridges the gap: AI can see geometry, but not *why* it was designed that way. Your answers provide critical context for generating better code.

**Reference:** `schemas/questionnaire.schema` (schema specification)  
**Example:** `examples/questionnaire.json` (completed example for ShelfBracket_v1)  
**Output:** `context.json` (your questionnaire responses)

## The 8 Sections (28 Questions Total)

### 1. Purpose & Use Case

What is this model for and how will it be used?

- Primary purpose (functional part, assembly component, prototype, etc.)
- Specific use case (what does it do? what loads does it support?)
- Assembly context (standalone or part of a larger system?)

### 2. Design Intent & Critical Features

What must never change, and why?

- Critical features (e.g., "M3 holes for standard fasteners")
- Design decisions (e.g., "Ribs added for strength", "Tapered for printability")
- Aesthetic requirements (curved edges, symmetry, etc.)

### 3. Key Dimensions & Parameters

Which dimensions should vary, and how?

- Primary dimensions (3-5 most important measurements)
- Parameter relationships (e.g., "Height scales with width", "Depth is fixed at 150mm")
- Scaling strategy (all together? independently? with constraints?)

### 4. Constraints & Tolerances

What are the hard limits?

- Tolerances (e.g., "Holes ±0.1mm", "Walls ±0.2mm")
- Min/Max limits (e.g., "Minimum wall 1.5mm or it fails")
- Design rules (e.g., "All fillets ≥ 1mm", "No overhangs > 45°")
- Dependencies (e.g., "Ribs only when width < 300mm")

### 5. Materials & Fabrication

What will this be made from and how?

- Material (PLA, Aluminum 6061, etc.)
- Fabrication method (FDM 3D printing, CNC milling, injection molding, etc.)
- Material-specific constraints (minimum wall thickness, shrinkage, support requirements, etc.)

### 6. Assembly & Sub-Components

How does it fit together?

- Part count (single body or multiple parts?)
- Assembly process (how do parts connect?)
- Fasteners (bolts, screws, snap-fits, etc.)

### 7. Variations & Planned Sizes

What different versions are needed?

- Example variants: "Small (100mm), Medium (200mm), Large (300mm)"
- Which parameters change between variants
- Parameter values for each variant

### 8. Model Metadata

Who, when, and what version?

- Model name / part number
- Version / revision
- Author / designer
- Design date
- Additional notes

## Example Answers

**Purpose:**
```
"Corner bracket for modular shelving system, supports 20kg per bracket"
```

**Critical Features:**
```
"Four M3 threaded holes in corners - must be exact for standard fasteners"
```

**Key Dimensions:**
```
"Width: 100-300mm (variable)
 Depth: 150mm (fixed)
 Thickness: 10mm (fixed)
 Corner radius: 1.5mm (minimum for FDM printing)"
```

**Constraints:**
```
"Minimum wall thickness: 1.5mm (structural requirement)
 Hole tolerance: ±0.1mm (M3 fastener fit)
 Fillet radius: minimum 1mm (FDM printability)"
```

**Materials:**
```
"PLA plastic, FDM 3D printing on Prusa i3 MK3S+
 Minimum wall: 2mm for reliability
 Support removal required"
```

**Variations:**
```
"Three standard sizes:
  - Small: 100mm width
  - Medium: 200mm width
  - Large: 300mm width"
```

## Best Practices

✓ **Be specific:** "M3 bolt holes (3.2mm diameter) at corners" not "some holes"  
✓ **Include units:** "100-300mm" not "100-300"  
✓ **Explain why:** "1.5mm walls minimum (failure below this)" not just "1.5mm"  
✓ **Reference Fusion 360 parameter names:** Use exact names from your design  
✓ **Specify all constraints:** What breaks if limits are violated?  
✓ **Give concrete examples:** Real dimensions for variants, not vague ranges

## Output

Your answers become `context.json`, which combines with `model.json` to generate metadata files.

## Next Step

Run metadata transformation:

```bash
python transform_metadata.py your_model_dir/
```

See: `../docs/transform_metadata.md`
