# Metadata Transformation Guide

This guide explains how to use the `transform_metadata.py` script to create AI-ready metadata files from your Fusion 360 export and questionnaire responses.

---

## Overview

After completing Phase 2 (Export & Questionnaire), you have:
- `model.json` - Geometric data exported from Fusion 360
- `context.json` - Questionnaire responses capturing design intent

**Phase 3 transforms these into 5 standardized metadata files:**
- `metadata.json` - Unified model info + design intent
- `parameters.json` - Code generation ready (CLI arguments, validation rules)
- `constraints.json` - Design rules and validation logic
- `features.json` - Feature timeline and dependencies
- `assembly.json` - Component structure and assembly process

These 5 files form your **AI-ready context package** for code generation.

---

## Installation

No installation needed! The script is standalone Python 3 with only standard library imports:
- `json` (standard library)
- `sys`, `os`, `pathlib` (standard library)
- `datetime` (standard library)
- `typing` (standard library)

**Requirements:**
- Python 3.6+
- Both `model.json` and `context.json` in the same directory

---

## Quick Start

### Basic Usage

```bash
# Transform files in-place
python transform_metadata.py path/to/model/directory

# Example:
python transform_metadata.py example-context/
```

Output: Generates 5 metadata files in the same directory.

### Advanced Usage

```bash
# Transform files, save to different directory
python transform_metadata.py input_dir/ output_dir/

# Example:
python transform_metadata.py example-context/ ./metadata_output/
```

Output: Generates 5 metadata files in `output_dir/`.

---

## What Gets Transformed

### Input: `model.json`
```
├── export_metadata      → metadata.json (timestamps, source)
├── parameters[]         → parameters.json (all parameters with ranges)
├── features[]           → features.json (feature timeline)
├── components[]         → assembly.json (component structure)
└── sketches[]           (referenced in features.json)
```

### Input: `context.json`
```
├── purpose              → metadata.json (design intent, use cases)
├── design_intent        → metadata.json (critical features, decisions)
├── parameters           → parameters.json (relationships, scaling strategy)
├── constraints          → constraints.json (all design rules)
├── materials            → metadata.json + constraints.json (fabrication rules)
├── assembly             → assembly.json (fasteners, instructions)
└── variations           → metadata.json (planned variants)
```

### Output: 5 Metadata Files

#### **1. metadata.json** - Unified Model Info
```json
{
  "metadata": {
    "version": "1.0",
    "generated_date": "2026-01-29T...",
    "source_model": "ShelfBracket_v1"
  },
  "model_info": {
    "name": "ShelfBracket_v1",
    "purpose": "Modular shelving bracket",
    "author": "Your Name",
    "part_count": 1
  },
  "design_intent": {
    "critical_features": [...],
    "design_decisions": [...],
    "load_requirements": "..."
  },
  "materials": {
    "material_type": "PLA",
    "fabrication_method": "FDM 3D printing"
  },
  "variations": {
    "planned_variants": "Small, Medium, Large",
    "variable_parameters": "Width (100-300mm)"
  }
}
```

**What AI uses this for:** Understanding design purpose, context, and variations.

#### **2. parameters.json** - Code Generation Ready
```json
{
  "parameters_for_code_generation": {
    "parameters": {
      "BaseWidth": {
        "type": "length",
        "unit": "mm",
        "default": 200,
        "min": 100,
        "max": 300,
        "step": 10,
        "cli_arg": "--width",
        "cli_help": "Bracket width in mm (100-300, step 10)",
        "fixed": false
      },
      "BaseDepth": {
        "type": "length",
        "default": 150,
        "min": 150,
        "max": 150,
        "cli_arg": null,
        "fixed": true
      }
    },
    "scaling_strategy": "Width varies, depth fixed"
  }
}
```

**What AI uses this for:** Generating Python function signatures, CLI arguments, and validation rules.

#### **3. constraints.json** - Design Rules
```json
{
  "constraints_for_code_generation": {
    "constraint_categories": {
      "tolerance_constraints": {
        "constraints": [{
          "name": "Mounting hole tolerance",
          "description": "3.2 ± 0.1mm",
          "severity": "CRITICAL"
        }]
      },
      "structural_constraints": {
        "constraints": [{
          "name": "Minimum wall thickness",
          "description": "1.5mm minimum",
          "severity": "CRITICAL"
        }]
      }
    }
  }
}
```

**What AI uses this for:** Writing validation code that rejects invalid parameters.

#### **4. features.json** - Feature Timeline
```json
{
  "features": {
    "feature_sequence": [
      {
        "index": 0,
        "name": "Base Extrude",
        "type": "extrude",
        "critical": true
      },
      {
        "index": 1,
        "name": "Mounting Holes",
        "type": "hole",
        "critical": true
      }
    ],
    "critical_features": ["Base Extrude", "Mounting Holes"]
  }
}
```

**What AI uses this for:** Reconstructing the feature sequence in CadQuery code.

#### **5. assembly.json** - Component Structure
```json
{
  "assembly": {
    "structure": {
      "part_count": 1,
      "assembly_type": "single_component"
    },
    "components": [
      {
        "name": "ShelfBracket_v1",
        "feature_count": 12
      }
    ],
    "fasteners": [
      {
        "description": "Four M3 x 20mm stainless steel bolts"
      }
    ]
  }
}
```

**What AI uses this for:** Understanding multi-part assemblies and fastening requirements.

---

## Step-by-Step Workflow

### Phase 2 (Complete) → Phase 3 → Phase 4

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 2: Extract & Questionnaire (Done)                         │
├─────────────────────────────────────────────────────────────────┤
│ ✓ model.json   (Fusion 360 export)                              │
│ ✓ context.json (28 questions answered)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 3: Metadata Transformation (YOU ARE HERE)                 │
├─────────────────────────────────────────────────────────────────┤
│ python transform_metadata.py <your_dir>/                        │
│                                                                 │
│ Generates:                                                      │
│ ✓ metadata.json     (model info + design intent)               │
│ ✓ parameters.json   (CLI specs + validation)                   │
│ ✓ constraints.json  (design rules)                              │
│ ✓ features.json     (timeline + dependencies)                   │
│ ✓ assembly.json     (components + fasteners)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 4: AI Code Generation (Next)                              │
├─────────────────────────────────────────────────────────────────┤
│ Send all 5 JSON files to Claude/GPT with generation guide       │
│ → Receive: generate_yourmodel.py (complete, working code)       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Detailed Example

### Starting Point
You have completed Phase 2 for ShelfBracket_v1:
```
example-context/
├── model.json       (Fusion 360 export)
├── context.json     (28 questions answered)
```

### Running Transformation
```bash
$ cd fissionreactor
$ python transform_metadata.py example-context/

Loading model.json...
Loading context.json...
Transforming metadata...

Generating metadata files in example-context:
  ✓ metadata.json        (   3.5 KB)
  ✓ parameters.json      (   3.5 KB)
  ✓ constraints.json     (   3.0 KB)
  ✓ features.json        (   2.5 KB)
  ✓ assembly.json        (   1.1 KB)

✅ Transformation complete!

Package is now AI-ready for code generation.
```

### Result
```
example-context/
├── model.json              ← Original
├── context.json            ← Original
├── metadata.json           ← NEW
├── parameters.json         ← NEW
├── constraints.json        ← NEW
├── features.json           ← NEW
└── assembly.json           ← NEW
```

### Next Steps
1. Verify the 5 files look correct
2. Send all 7 files (model.json, context.json + 5 metadata files) to AI
3. Request: "Generate parameterized CadQuery script per this context package"
4. Receive: `generate_shelfbracket.py` (complete working code)

---

## Validation Checklist

After running transformation, verify:

```bash
# Check all files were created
ls -lh example-context/*.json

# Verify all JSON is valid
for f in example-context/*.json; do
  python3 -m json.tool "$f" > /dev/null && echo "✓ $f" || echo "✗ $f"
done

# Check file sizes are reasonable
# metadata.json should be ~3-10 KB
# parameters.json should be ~2-6 KB
# constraints.json should be ~2-5 KB
# features.json should be ~1-4 KB
# assembly.json should be ~0.5-2 KB
```

---

## Troubleshooting

### Error: "File not found: model.json"
**Cause:** Missing required input files  
**Solution:** Ensure both `model.json` and `context.json` are in the directory you specify

```bash
# Check what files are present
ls -la example-context/

# Should show:
# -rw-r--r-- model.json
# -rw-r--r-- context.json
```

### Error: "Invalid JSON in model.json"
**Cause:** JSON syntax error in input files  
**Solution:** Validate input files first

```bash
python3 -m json.tool example-context/model.json > /dev/null
python3 -m json.tool example-context/context.json > /dev/null
```

### Generated metadata.json looks incomplete
**Cause:** Some fields may be empty if not filled in questionnaire  
**Solution:** This is OK! AI can work with partial data. But more complete context = better code.

Check these fields in context.json:
- `design_intent.intent_critical_features` - Should describe critical features
- `constraints.constraint_minimum` - Should specify minimum dimensions
- `materials.material_type` - Should specify material and fabrication method
- `variations.var_examples` - Should give specific examples of variations

### Generated parameters.json has fewer parameters than expected
**Cause:** Some parameters may be fixed (min == max)  
**Solution:** This is correct! Fixed parameters don't get CLI arguments.

Check: In parameters.json, "fixed": true parameters won't have cli_arg

---

## Command-Line Reference

```bash
# Minimum: just the directory
python transform_metadata.py path/to/model/

# Maximum: input dir + output dir
python transform_metadata.py path/to/input/ path/to/output/

# Verbose examples
python transform_metadata.py example-context/
python transform_metadata.py /Users/you/Projects/MyModel/
python transform_metadata.py input_models/MyBracket/ output_metadata/MyBracket/
```

---

## What Transformation Does (Internal)

The transformer:

1. **Loads** both JSON files
2. **Extracts** model name from context_metadata
3. **Transforms parameters:** Converts parameter list with min/max/step into code-generation-ready format with CLI arguments
4. **Transforms constraints:** Groups constraints by type (tolerance, structural, geometric, material, parameter dependencies)
5. **Transforms features:** Extracts feature timeline and marks critical features
6. **Transforms assembly:** Groups component info and fastener requirements
7. **Validates** all outputs are valid JSON
8. **Saves** 5 files with proper formatting

The transformation is **deterministic** - same inputs always produce same outputs.

---

## Integration with Workflow

| Step | Tool | Input | Output |
|------|------|-------|--------|
| 1 | Fusion 360 | CAD model | Prepared model |
| 2 | export_fusion360_data.py | F3D file | model.json |
| 3 | Questionnaire | Design intent | context.json |
| **3a** | **transform_metadata.py** | **model.json + context.json** | **5 metadata files** |
| 4 | AI (Claude/GPT) | All 7 JSON files | generate_model.py |
| 5 | Python/CadQuery | generate_model.py | STEP/STL files |

---

## FAQ

**Q: Can I edit the generated metadata files?**  
A: Yes! They're just JSON. You can:
- Add/remove parameters
- Adjust constraints
- Reorder features
- Update design intent
Then use the updated files for code generation.

**Q: Do I need to run transformation again if I change context.json?**  
A: Yes. Run transformation again to regenerate the 5 metadata files with your changes.

**Q: Can I use these metadata files for other purposes?**  
A: Yes! The metadata is valuable for:
- Documenting design rationale
- Sharing design specs with team
- Validating generated code
- Creating variations of the design

**Q: What if I have multiple models?**  
A: Run transformation separately for each:
```bash
python transform_metadata.py model1_dir/
python transform_metadata.py model2_dir/
python transform_metadata.py model3_dir/
```

**Q: Is transformation reversible? Can I get model.json back from metadata?**  
A: No. Transformation is one-way. metadata.json is derived from model.json, not identical to it.

---

## Next Steps

1. ✅ Run: `python transform_metadata.py your_model_dir/`
2. ✅ Verify: All 5 JSON files created and valid
3. ✅ Send: All 7 files (2 input + 5 metadata) to AI
4. ⏭️ Next: Follow generator-guide/ for code generation

See `../generator-guide/README.md` for Phase 4 (AI code generation).
