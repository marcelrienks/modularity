# Export & Extraction Guide

This guide covers exporting design data from Fusion 360 and transforming it into standardized metadata files for AI-based parameterized code generation.

---

## Part 1: Exporting Design Data from Fusion 360

### Quick Start

1. Open a `.f3d` design file in Fusion 360
2. Go to **Tools > Add-ins > Scripts and Add-ins**
3. Select the **Scripts** tab
4. Right-click `export_fusion360_data` > **Run**
5. Select the directory where you want to save the exported JSON files

### What Gets Exported

The `export_fusion360_data.py` script exports a comprehensive `model.json` file containing:

- **User parameters** - All parameterized dimensions (Width, Depth, etc.)
- **Reference parameters** - Derived/calculated values
- **Timeline** - Complete feature construction history
- **Sketches** - All sketches with geometry constraints
- **Features** - Extrude, Hole, Shell, Mirror, Chamfer, Fillet, Pattern, Thread
- **Components** - Part/body hierarchy and relationships
- **Metadata** - Export date, source file name, Fusion 360 version

### Output Structure

```
your_selected_directory/
├── model_name_1/
│   ├── origin/
│   │   └── model_name_1.json          (design geometry & parameters)
│   ├── context.json                    (user questionnaire responses)
│   ├── metadata.json                   (standardized model metadata)
│   ├── parameters.json                 (formatted for code generation)
│   └── constraints.json                (design limits & rules)
└── model_name_2/
    ├── origin/
    │   └── model_name_2.json
    ├── context.json
    ├── metadata.json
    ├── parameters.json
    └── constraints.json
```

### File Behavior

- Creates folder named after each model
- Saves JSON file with model name in `origin/` subdirectory
- **Overwrites existing files** if re-exported
- Directories auto-created if they don't exist

### Troubleshooting

**Script doesn't appear in Add-In list:**
1. Copy `export_fusion360_data.py` to: `~/Library/Application Support/Autodesk/Fusion 360/API/Python/Samples/`
2. Restart Fusion 360
3. Go to Tools > Add-ins > Scripts and Add-ins > Scripts tab

**No active document:**
- Open a `.f3d` design file first
- Then run the script from the Scripts panel

**Export cancelled:**
- The script was cancelled from the folder selection dialog
- Run it again and select a valid output directory

---

## Part 2: Metadata Extraction & Transformation

### Overview

The exported `model.json` contains geometric data that the AI can understand. However, design intent, constraints, and parameterization strategy cannot be automatically extracted from the 3D file. That's where the **questionnaire** comes in.

The transformation process:
1. **Export** `model.json` from Fusion 360 (automatic)
2. **Complete questionnaire** to capture design context (user)
3. **Transform** model.json + context.json → 5 metadata files (automatic)
4. **Package** as AI-ready context bundle

### What Can Be Extracted from model.json

**Automatic extraction (no user input needed):**
- User-defined parameters and their values
- Derived/calculated parameters
- Feature construction sequence (timeline)
- Component hierarchy and structure
- Sketch geometry and constraints
- Design metadata (name, date, version)

### What Requires Questionnaire Input

**Must come from context.json (questionnaire responses):**
- Design intent (why decisions were made)
- Critical features (what must never change)
- Parameter relationships and constraints
- Tolerance specifications
- Material and fabrication method
- Assembly instructions and variations
- Parameterization strategy (which dimensions should vary)

### Data Extraction Flow

```
.f3d File (Fusion 360)
    ↓
Fusion 360 Python API
    ↓
export_fusion360_data.py
    ↓
model.json (geometric data: parameters, features, timeline)
    ↓
    ├─ User completes questionnaire (captured as context.json)
    │
    └─→ Transformation Algorithm
        ↓
        Generate 5 Metadata Files:
        ├── metadata.json          (model information & purpose)
        ├── parameters.json        (parameterization strategy)
        ├── constraints.json       (design rules & limits)
        ├── features.json          (feature sequence & dependencies)
        └── assembly.json          (assembly structure & fasteners)
```

### 5 Metadata Files

Each file serves a specific AI question. All are generated from model.json + context.json:

| File | Generated From | Contains | Why AI Needs It |
|------|---|---|---|
| **metadata.json** | context (purpose, intent, materials) + model (export_metadata) | Model info, purpose, design intent, material, fabrication | Understand what the model is for and how it should be used |
| **parameters.json** | model (user/reference parameters) + context (parameter ranges, relationships) | Primary parameters with min/max, derived parameters, relationships, standard variants | Generate code with correct parameter initialization and validation |
| **constraints.json** | context (constraints) + inferred from materials/fabrication | Tolerance constraints, geometric constraints, material/fabrication rules, validation rules | Validate parameter changes don't violate design limits |
| **features.json** | model (timeline, sketches, features) + context (critical_features) | Feature sequence, feature types, dependencies, critical features, guidelines | Regenerate features in correct order, preserve essential features |
| **assembly.json** | model (component hierarchy) + context (assembly section) | Components, assembly instructions, fasteners, sub-assembly hierarchy | Understand multi-part models and generate assembly code |

### Transformation Algorithm (Pseudocode)

```python
def transform_to_metadata(model_json, context_json):
    """Transform model and context data into 5 metadata files."""
    return {
        'metadata.json': {
            'generated_date': model_json['export_metadata']['exported_date'],
            'model_info': model_json['export_metadata'],
            'purpose': context_json['purpose'],
            'design_intent': context_json['design_intent'],
            'fabrication': context_json['materials']
        },
        'parameters.json': {
            'primary_parameters': transform_parameters(
                model_json['user_parameters'],
                context_json['parameters']
            ),
            'derived_parameters': model_json['reference_parameters'],
            'parameter_relationships': context_json['param_relationships'],
            'standard_variants': context_json['variations']
        },
        'constraints.json': {
            'tolerance_constraints': extract_tolerances(context_json),
            'geometric_constraints': extract_constraints(context_json),
            'material_constraints': infer_from_material(context_json['materials']),
            'fabrication_constraints': infer_from_fabrication(context_json['materials']),
            'rule_engine': generate_validation_rules(context_json)
        },
        'features.json': {
            'feature_sequence': transform_timeline(model_json['timeline']),
            'feature_types': categorize_features(model_json['features']),
            'critical_features': context_json['design_intent']['critical_features'],
            'dependencies': build_dependency_graph(model_json)
        },
        'assembly.json': {
            'components': model_json['components'],
            'assembly_instructions': context_json['assembly']['instructions'],
            'fasteners': context_json['assembly']['fasteners']
        }
    }
```

### Transformation Example

**Input:** Shelf bracket model

From `model.json`:
```json
{
  "user_parameters": [
    {"name": "Width", "value": 200, "unit": "mm"},
    {"name": "Depth", "value": 150, "unit": "mm"}
  ],
  "timeline": [
    {"index": 0, "name": "BaseSketch", "feature_type": "Sketch"},
    {"index": 1, "name": "BaseExtrude", "feature_type": "Extrude"}
  ]
}
```

From `context.json` (questionnaire):
```json
{
  "param_primary": "Width: 100-300mm, Depth: 100-250mm",
  "constraint_tolerances": "Holes ±0.1mm",
  "var_examples": "Small: 100mm, Medium: 200mm, Large: 300mm"
}
```

Generated `parameters.json`:
```json
{
  "primary_parameters": [
    {
      "name": "Width",
      "value": 200,
      "minimum": 100,
      "maximum": 300
    }
  ],
  "standard_variants": [
    {"name": "Small", "parameters": {"Width": 100}},
    {"name": "Medium", "parameters": {"Width": 200}},
    {"name": "Large", "parameters": {"Width": 300}}
  ]
}
```

### Validation Steps

After transformation, validate:
1. ✅ All parameters match Fusion 360 export values
2. ✅ All features in timeline appear in feature_sequence
3. ✅ All components are documented in assembly
4. ✅ Constraints are realistic and testable
5. ✅ No conflicts between files
6. ✅ All cross-references are valid

---

## Summary

This workflow ensures AI receives complete, consistent, standardized information:

| Stage | Source | Output | Purpose |
|-------|--------|--------|---------|
| Export | Fusion 360 | model.json | Geometric data (automatic) |
| Questionnaire | User | context.json | Design intent (manual) |
| Transform | model.json + context.json | 5 metadata files | AI-ready package |
| Generate | 5 metadata files | Parameterized Python script | Reproducible models |

All files together form an **AI-ready context package** for code generation.

---

## More Information

- **Fusion 360 API Docs:** https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/
- See the main **README.md** for overall workflow overview
- See **questionnaire_guide.md** for how the questionnaire captures design context
