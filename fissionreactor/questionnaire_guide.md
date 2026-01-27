# Questionnaire Guide - Design Context for AI Code Generation

## Overview

The questionnaire is designed to capture the design intent, constraints, and context that are critical for an AI to understand how to generate parameterized scripts that can reproduce the original model with variations.

**Key Principle:** The questionnaire bridges the gap between what an AI can extract from geometric data (shape, size, topology) and what it cannot (design intent, non-obvious decisions, constraints, use cases).

**How It Works:**
1. User completes the questionnaire (answers 28 questions across 8 sections)
2. Responses are saved as `context.json`
3. Combined with exported `model.json` from Fusion 360
4. Transformed into 5 standardized metadata files
5. Metadata files sent to AI for parameterized script generation

---

## Why This Matters for Code Generation

When an AI generates a parameterized script, it needs to understand:

1. **What to vary** - Which dimensions should be parameters?
2. **How to vary** - Should dimensions scale together? Have limits?
3. **What to preserve** - Which features are critical and must never change?
4. **Why it was designed** - What was the designer thinking when making this choice?

Without this context, the AI might:
- Create meaningless parameters (e.g., making a non-functional feature parameterizable)
- Break the design by varying incompatible dimensions
- Ignore critical constraints that ensure the model works
- Generate scripts that technically work but don't match the design intent

---

## Questionnaire Sections

### 1. Model Purpose & Use Case

**Why it matters:** Understanding intended application reveals what's critical vs. what can vary safely.

- **Primary purpose:** What category? (Functional part, assembly, prototype, structural element)
- **Use case:** How will this be used? (e.g., "Will hold up to 5kg load", "Connects two parts")
- **Assembly context:** Part of a larger system? (e.g., "One of 8 identical brackets in an assembly")

---

### 2. Design Intent & Key Features

**Why it matters:** Not all features are equal. Some are functional necessities, others implementation details.

- **Critical features:** What MUST remain? (e.g., "M3 threaded holes for standard fasteners")
- **Design decisions:** Why certain choices? (e.g., "Tapered walls for print strength", "Ribs for stiffness")
- **Aesthetic elements:** Does appearance matter? (e.g., "Smooth curves", "Symmetry required")

---

### 3. Key Dimensions & Parameters

**Why it matters:** This is what gets parameterized. Designer knows which dimensions matter most.

- **Primary dimensions:** 3-5 most important measurements (e.g., "Width: 100mm, Depth: 150mm, Thickness: 10mm")
- **Dimensional relationships:** Do dimensions depend on each other? (e.g., "Height = Width × 0.15", "Hole spacing = 10% of width")
- **Scaling strategy:** How should the model grow/shrink? (e.g., "All dimensions scale together" or "Holes stay same size, outer changes")

---

### 4. Design Constraints & Tolerances

**Why it matters:** Constraints prevent AI from creating invalid models.

- **Tolerances:** What variation is acceptable? (e.g., "Holes ±0.1mm", "Walls ±0.2mm")
- **Min/Max limits:** Physical bounds? (e.g., "Minimum wall 1.5mm", "Maximum height 200mm")
- **Design rules:** Hard rules that must always hold? (e.g., "All fillets ≥ 1mm", "Wall thickness ≥ 2mm")
- **Feature dependencies:** Do some features require certain conditions? (e.g., "Ribs only when wall < 3mm")

---

### 5. Materials & Fabrication

**Why it matters:** Material and fabrication method drive design decisions.

- **Material:** What will this be made from? (e.g., "PLA plastic", "Aluminum 6061")
- **Fabrication method:** How manufactured? (e.g., "FDM 3D printing", "CNC milling")
- **Material-specific constraints:** What does material/method impose? (e.g., "Minimum wall 2mm", "Needs 5° draft angles")
- **Post-processing:** What happens after? (e.g., "Support removal", "Assembly required")

---

### 6. Assembly & Sub-components

**Why it matters:** Understanding assembly structure prevents breaking part interfaces.

- **Structure:** How many separate parts? (e.g., "1 solid part" or "3 bodies")
- **Assembly process:** How do parts fit together? (e.g., "Part A slides into Part B, Part C bolted on top")
- **Fasteners:** How are parts joined? (e.g., "M3 bolts", "Snap-fit tabs")
- **Difficulty:** Simple, Moderate, or Complex assembly?

---

### 7. Variations & Configurations

**Why it matters:** Goal of parameterization is enabling variations.

- **Planned variants:** What variations are needed? (e.g., "Small (100mm), Medium (200mm), Large (300mm)")
- **Variant examples:** Specific examples with parameter values
- **Variant parameters:** Which parameters vary between versions?

---

### 8. Model Metadata

**Why it matters:** Documentation and traceability.

- **Model name/part number:** Human-readable identifier
- **Version/revision:** Version tracking
- **Author/designer:** Who created this
- **Design date:** When was this designed
- **Additional notes:** Anything else important

**Questions:**

- **Planned variations:** What different versions are needed?
  - *Example answers:*
    - "Three sizes: Small, Medium, Large for different applications"
    - "Left and right-hand versions"
    - "Different material versions: flexible (TPU) and rigid (PLA)"

- **Specific examples:** Concrete examples of variations
  - *Example answers:*
    - "Small: 50×50×25mm, Medium: 100×100×50mm, Large: 200×200×100mm"
    - "With 4 holes, 6 holes, or 8 holes in pattern"
    - "Thin wall (1.5mm) for lightweight, thick wall (3mm) for strength"

- **Variable parameters:** Which parameters change between variations?
  - *Example answers:*
    - "Overall width and depth scale together, height can be independent"
    - "Hole count and pattern spacing change, hole diameter stays M3"
    - "Wall thickness option changes, all other dimensions stay fixed"

**How AI will use this:**
- Prioritize parameterization strategy
- Generate the specific variations the designer needs
- Validate that the generated script can produce all required variants

---

### 8. Model Metadata

**Why it matters:** Metadata helps with documentation, version control, and understanding model history.

**Questions:**

- **Name:** What should this model be called?
  - *Example answers:* "Handle_v2", "Tile_connector_45deg", "Support_bracket_corner"

- **Version:** What revision is this?
  - *Example answers:* "v1.0", "Rev B", "Prototype 3"

- **Author:** Who designed it?
  - Helps with attribution and follow-up questions

- **Date:** When was it designed?
  - Context for understanding design decisions

- **Additional notes:** Anything else AI should know?
  - Catch-all for important context that doesn't fit elsewhere

**How AI will use this:**
- Include in generated script documentation
- Version the generated code appropriately
- Cross-reference with design files

---

## How Answers Inform Code Generation

Here's an example of how questionnaire answers flow into generated code:

### Input from Questionnaire
```
Purpose: "Part of modular shelving system"
Critical features: "Four M3 mounting holes in corners"
Key dimensions: "Width: 200mm, Depth: 150mm, Thickness: 10mm"
Dimensional relationships: "Width can vary, depth stays 150mm, thickness fixed at 10mm"
Min/Max constraints: "Width 100-300mm"
Material: "PLA (3D printed)"
Fabrication: "FDM printing, no support"
Variations: "Small (100mm), Medium (200mm), Large (300mm)"
```

### Generated Code Structure
```python
class ShelfBracket:
    def __init__(self, width=200, depth=150, thickness=10, corner_radius=1.5):
        # Validate constraints
        assert 100 <= width <= 300, "Width must be 100-300mm"
        assert depth == 150, "Depth is fixed at 150mm"
        assert thickness == 10, "Thickness is fixed at 10mm"
        
        # Critical feature: M3 holes at corners (3.2mm for M3 bolt)
        hole_diameter = 3.2
        hole_inset = 10  # 10mm from corner
        
        # Generate bracket with parameterized width
        self.create_base(width, depth, thickness, corner_radius)
        self.create_corner_holes(width, depth, hole_diameter, hole_inset)
        
    def create_base(self, width, depth, thickness, corner_radius):
        # Create rectangular base with rounded corners for FDM print quality
        ...
    
    def create_corner_holes(self, width, depth, diameter, inset):
        # Create four M3 holes at corners (non-parameterized for critical feature)
        ...

# Generate three size variants
small = ShelfBracket(width=100)    # Small version
medium = ShelfBracket(width=200)   # Medium version
large = ShelfBracket(width=300)    # Large version
```

---

## Best Practices for Answering

- **Be Specific:** "M3 bolt holes (3.2mm) in all four corners" vs. "Some holes"
- **Explain Why:** "Fillets are 2mm for print quality (prevents breakage)" vs. just "2mm fillets"
- **Fill Gaps:** Say "Not applicable" if question doesn't apply
- **Use Measurements:** Include units (mm, inches); reference Fusion 360 parameter names
- **Plan Variations:** What could change in future? What must stay fixed? What breaks if changed?

---

## Mapping: From Questionnaire to Metadata Files

The questionnaire responses (context.json) are combined with the Fusion 360 export (model.json) and transformed into 5 standardized metadata files.

**Mapping Summary:**

| Questionnaire Section | Maps To | Purpose |
|---|---|---|
| 1. Purpose & Use Case | metadata.json | Understand what the model is for |
| 2. Design Intent & Features | features.json + metadata.json | Know what's critical and what can change |
| 3. Key Dimensions & Parameters | parameters.json | Define parameterization strategy |
| 4. Constraints & Tolerances | constraints.json | Enforce design rules and limits |
| 5. Materials & Fabrication | metadata.json + constraints.json | Understand manufacturing constraints |
| 6. Assembly & Sub-components | assembly.json | Define part structure and assembly |
| 7. Variations & Configurations | parameters.json | Enable model variations |
| 8. Model Metadata | metadata.json | Track authorship and versioning |

**Detailed Examples:**

### Example 1: Parameters & Constraints
From questionnaire:
```json
{
  "param_primary": "Width: 100-300mm, Depth: 150mm (fixed)",
  "param_scaling": "Width varies, depth stays fixed",
  "constraint_minimum": "Minimum wall 1.5mm",
  "constraint_tolerances": "Holes ±0.1mm"
}
```

Generated files:
```json
// parameters.json
{
  "primary_parameters": [
    {"name": "Width", "value": 200, "minimum": 100, "maximum": 300, "varies": true},
    {"name": "Depth", "value": 150, "varies": false}
  ]
}

// constraints.json
{
  "geometric_constraints": [
    {"name": "Minimum wall thickness", "value": 1.5, "type": "global_minimum"}
  ],
  "tolerance_constraints": [
    {"feature": "Holes", "tolerance": "±0.1mm"}
  ]
}
```

### Example 2: Features & Assembly
From questionnaire:
```json
{
  "intent_critical_features": "Four M3 holes (must accept standard fasteners)",
  "assembly_fasteners": "M3 bolts with washers"
}
```

Generated files:
```json
// features.json
{
  "critical_features": ["M3_mounting_holes"],
  "guidelines": {"preserve": ["M3_mounting_holes"]}
}

// assembly.json
{
  "fasteners": [
    {"type": "Bolt", "specification": "M3 x 20mm", "quantity": 4}
  ]
}
```

**Input: Shelf Bracket Model**

From questionnaire (`context.json`):
```json
{
  "purpose": {
    "purpose_primary": "Modular shelving bracket",
    "purpose_use_case": "Holds shelves, supports 20kg"
  },
  "design_intent": {
    "intent_critical_features": "Four M3 holes"
  },
  "parameters": {
    "param_primary": "Width: 100-300mm",
    "param_scaling": "Width varies"
  },
  "constraints": {
    "constraint_tolerances": "Holes ±0.1mm"
  },
  "materials": {
    "material_type": "PLA plastic"
  },
  "variations": {
    "var_examples": "Small: 100mm, Medium: 200mm, Large: 300mm"
  }
}
```

From Fusion 360 export (`model.json`):
```json
{
  "user_parameters": [
    {"name": "Width", "value": 200, "unit": "mm"}
  ],
  "timeline": [
    {"index": 0, "name": "BaseSketch", "feature_type": "Sketch"},
    {"index": 1, "name": "BaseExtrude", "feature_type": "Extrude"}
  ]
}
```

**Generated Metadata Files:**

1. **metadata.json**
   - Purpose: Modular shelving bracket
   - Material: PLA plastic
   - Design intent: Four M3 holes critical

2. **parameters.json**
   - Primary parameter: Width (100-300mm)
   - Variants: Small/Medium/Large
   - Scaling: Width varies

3. **constraints.json**
   - Hole tolerance: ±0.1mm
   - Material shrinkage: Inferred from PLA

4. **features.json**
   - Feature sequence: BaseSketch → BaseExtrude
   - Critical: BaseExtrude (must preserve)

5. **assembly.json**
   - Structure: Single body
   - Fasteners: M3 bolts

All 5 files + model.json + context.json = **AI-ready context package** ready for code generation.

---

## Appendix: Question Types Reference

| Type | Description | Use When |
|------|-------------|----------|
| `text` | Single line input | Short answers, names, numbers |
| `text_long` | Multi-line input | Descriptions, detailed explanations |
| `select` | Dropdown menu | Fixed set of options (e.g., "Simple/Moderate/Complex") |
| `checkbox` | Multiple selection | User can pick multiple options |
| `number` | Numeric input | Measurements, counts, tolerances |

