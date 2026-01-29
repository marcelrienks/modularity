# fissionreactor

Transform Fusion 360 CAD models into parameterized Python code generators with AI.

## Quick Start (7 Steps, ~45 min total)

```
1. Design model in Fusion 360 (with named parameters)
   ↓
2. Export design data → model.json
   ↓
3. Answer questionnaire → context.json
   ↓
4. Transform metadata → 5 AI-ready JSON files
   ↓
5. Send to AI (Claude/GPT) with context package
   ↓
6. Receive parameterized Python code
   ↓
7. Test & generate STEP/STL files with custom parameters
```

## What You Get

A Python script that:
- Generates your CAD model with any custom parameters
- Validates inputs against design constraints
- Exports to STEP or STL format
- Works with CLI arguments: `python generate_model.py --width 100 --output model.step`

## Installation

```bash
# Copy export script to Fusion 360 (macOS example)
cp export_fusion360_data.py ~/Library/Application\ Support/Autodesk/Fusion\ 360/API/Python/Samples/

# Required: Python 3.6+, CadQuery
pip install cadquery
```

## How It Works

| Phase | Tool | Input | Output | Time |
|-------|------|-------|--------|------|
| 1 | Fusion 360 | CAD design | Prepared model | — |
| 2 | export_fusion360_data.py | .f3d file | model.json | 5 min |
| 3 | Questionnaire | Design intent | context.json | 15-30 min |
| 4 | transform_metadata.py | model + context | 5 metadata files | 1 min |
| 5 | AI (Claude/GPT) | Context package | generate_model.py | 2-5 min |
| 6 | Python + CadQuery | CLI arguments | STEP/STL files | 10 min |

## Core Concept

**Problem:** AI can see geometry but not *why* it was designed that way.

**Solution:** Provide both:
- **model.json** — What was designed (geometry, features, parameters)
- **context.json** — Why it was designed (intent, constraints, variations)

Together, AI generates better parameterized code.

## File Structure

```
fissionreactor/
├── README.md                          # This file
├── export_fusion360_data.py           # Phase 2: Fusion 360 export script
├── questionnaire_template.json        # Phase 3: Design questionnaire
├── questionnaire_example.json         # Phase 3: Completed example
├── transform_metadata.py              # Phase 4: Metadata transformation
├── validate_workflow.py               # Optional: Validation framework
├── template_generator.py              # Phase 5: Code generation template
│
├── docs/                              # Detailed documentation
│   ├── export_fusion360_guide.md      # How to export from Fusion 360
│   ├── questionnaire_guide.md         # How to answer questionnaire
│   ├── transform_metadata_guide.md    # How to run transformation
│   ├── validation_guide.md            # How to validate data
│   ├── generator-guide_README.md      # Code generation overview
│   ├── generator-guide_generation-guide.md   # Detailed generation workflow
│   └── generator-guide_naming-conventions.md # Code naming standards
│
└── examples/                          # Complete working example (ShelfBracket_v1)
    ├── README.md                      # Example guide & checklist
    ├── model.json                     # Exported from Fusion 360
    ├── context.json                   # Questionnaire answers
    ├── metadata.json                  # Generated metadata
    ├── parameters.json                # Generated parameters
    ├── constraints.json               # Generated constraints
    ├── features.json                  # Generated features
    └── generate_shelfbracket_example.py # Working code example
```

## Step-by-Step Guide

### Step 1: Prepare Model in Fusion 360

Design with:
- Named parameters (e.g., Width, Depth, Thickness)
- Features in construction order
- Clear design constraints

See `examples/` for a real model.

### Step 2: Export Design Data

1. Copy `export_fusion360_data.py` to Fusion 360 scripts directory (see docs/)
2. Open your .f3d file
3. Run script: `Tools > Add-ins > Scripts and Add-ins > Scripts > export_fusion360_data > Run`
4. Get: `model.json`

**Details:** `docs/export_fusion360_guide.md`

### Step 3: Complete Questionnaire

Edit `questionnaire_template.json` to answer 28 questions about:
- Purpose & use case
- Design intent & critical features
- Key dimensions & parameter relationships
- Constraints & tolerances
- Materials & fabrication
- Assembly & sub-components
- Planned variations
- Metadata (author, version, date)

Get: `context.json`

**Details:** `docs/questionnaire_guide.md`

### Step 4: Transform Metadata

```bash
python transform_metadata.py path/to/your/model/
```

Generates 5 AI-ready files:
- `metadata.json` — Model info & design intent
- `parameters.json` — Code generation ready (CLI specs, validation)
- `constraints.json` — Design rules & limits
- `features.json` — Feature timeline
- `assembly.json` — Component structure

**Details:** `docs/transform_metadata_guide.md`

### Step 5: Validate (Optional)

```bash
python validate_workflow.py path/to/your/model/
```

Checks that all files are complete and consistent before sending to AI.

**Details:** `docs/validation_guide.md`

### Step 6: Send to AI

Provide all 7 files (model.json + context.json + 5 metadata files) with prompt:

```
Generate a complete parameterized CadQuery Python script that:
1. Accepts all parameters from parameters.json as CLI arguments
2. Validates inputs against constraints.json
3. Builds model following the feature timeline from model.json
4. Validates output (post-generation)
5. Exports to STEP or STL format

Use template_generator.py as reference for code structure.
See examples/generate_shelfbracket_example.py for a working example.
```

**Details:** `docs/generator-guide_generation-guide.md`

### Step 7: Test Generated Code

```bash
# Test help
python generate_mymodel.py --help

# Generate with default parameters
python generate_mymodel.py

# Test with custom parameters
python generate_mymodel.py --width 100 --output small.step

# Test error handling (should reject invalid params)
python generate_mymodel.py --wall-thickness 0.5 --output test.step
```

Verify:
- ✓ Script runs without errors
- ✓ Default parameters match original model
- ✓ Model opens in CAD software
- ✓ Dimensions correct (±0.5mm tolerance)
- ✓ All features present in correct order
- ✓ Parameter variations work
- ✓ Invalid parameters rejected with clear errors

## Example Workflow

The `examples/` directory shows the complete flow for ShelfBracket_v1:

```bash
cd examples/

# View the context package
ls -la *.json

# Example: Generate models with different widths
python generate_shelfbracket_example.py --width 100 --output small.step
python generate_shelfbracket_example.py --width 200 --output medium.step
python generate_shelfbracket_example.py --width 300 --output large.step
```

## Key Concepts

### Parameters vs Constraints

- **Parameters** (parameters.json) — Dimensions that vary with CLI arguments
- **Constraints** (constraints.json) — Rules that parameters must follow (min/max, tolerances, dependencies)

Example:
```json
"BaseWidth": {
  "min": 100, "max": 300, "default": 200,      // Parameter
  "constraint": "Must be multiple of 10"         // Constraint
}
```

### The 5 Metadata Files

| File | Purpose |
|------|---------|
| metadata.json | Unified model info + design intent |
| parameters.json | Code generation specs (CLI, defaults, ranges) |
| constraints.json | Design validation rules |
| features.json | Feature sequence & dependencies |
| assembly.json | Component structure & fasteners |

Together, these files form an **AI-ready context package** that AI systems can use to generate working code.

## Troubleshooting

**Export script doesn't appear in Fusion 360:**
- Verify script is in correct directory
- Restart Fusion 360
- Check: `Tools > Add-ins > Scripts and Add-ins > Scripts`

**Transformation fails:**
```bash
# Verify files exist
ls -la your_model_dir/model.json your_model_dir/context.json

# Validate JSON syntax
python3 -m json.tool your_model_dir/model.json
python3 -m json.tool your_model_dir/context.json
```

**Generated code doesn't run:**
1. Install CadQuery: `pip install cadquery`
2. Verify context package is complete (all 7 JSON files)
3. Check AI included validation code in generated script

**Generated models don't match original:**
- Verify all parameters in parameters.json have correct min/max/default
- Check that all features from model.json are implemented
- Compare context.json to examples/context.json for completeness

## FAQ

**Q: Do I need to know Python?**  
A: No. The generated script works with just CLI arguments. No programming needed.

**Q: How long does it take?**  
A: Export (5 min) + Questionnaire (15-30 min) + Transform (1 min) + AI generation (2-5 min) = ~45 minutes total.

**Q: Why the questionnaire?**  
A: AI sees geometry but not design intent. The questionnaire provides critical context: why decisions were made, what constraints matter, what variations are needed.

**Q: Can I edit the generated code?**  
A: Yes! It's yours to modify. Or regenerate by updating the context package.

**Q: What's the complexity limit?**  
A: Works best for 10-50 parameters and 10-20 features. More complex models may need breaking into sub-models.

## Documentation

- **Export:** `docs/export_fusion360_guide.md`
- **Questionnaire:** `docs/questionnaire_guide.md`
- **Transformation:** `docs/transform_metadata_guide.md`
- **Validation:** `docs/validation_guide.md`
- **Code Generation:** `docs/generator-guide_generation-guide.md`
- **Naming Conventions:** `docs/generator-guide_naming-conventions.md`
- **Example:** `examples/README.md`

## Status

✅ Phase 1: Design (your responsibility)  
✅ Phase 2: Export + Questionnaire (tools included)  
✅ Phase 3: Metadata Transformation (transform_metadata.py)  
✅ Phase 4: AI Code Generation (generation guide included)  
✅ Phase 5: Testing (documented)  

**Overall:** Complete and ready to use.

## Next Steps

1. Review `examples/` to see a complete example
2. Design your model in Fusion 360 with named parameters
3. Follow Step 1-7 above
4. Send context package to AI
5. Test the generated code

Happy generating! 🚀
