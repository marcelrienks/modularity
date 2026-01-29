# AI-Ready Context Package

## Overview

This directory contains a **complete, real-world example** of an "AI-ready context package" - everything an AI system needs to successfully generate parameterized Python code that reproduces a CAD model with variations.

The example uses the **ShelfBracket_v1** - a corner bracket for a modular shelving system.

## What's Included

### 1. **model.json** - Design Data Export
Complete design data extracted from Fusion 360:
- All parameters (8 total: 4 variable, 2 fixed, 2 derived)
- Sketch definitions (BaseProfile, MountingHoles, RibPattern)
- Feature timeline (12 features in construction order)
- Bodies and appearance
- Bounding box and physical properties

**Why AI needs this:** Defines the exact geometry construction sequence and which parameters drive which features.

### 2. **context.json** - Design Intent & User Context
User responses to 28-question questionnaire:
- Purpose and use case (modular shelving component)
- Critical design features (mounting holes precision, wall thickness, edge radii)
- Design decisions and trade-offs (tapered walls, reinforcement ribs)
- Parameters and relationships (which vary, which are fixed, why)
- Material and fabrication specs (FDM PLA, Prusa printer)
- Assembly requirements and load capacity (20kg per bracket)
- Planned variations (3 standard sizes)

**Why AI needs this:** Explains the "why" behind design choices. Geometry alone doesn't communicate that 1.5mm walls will fail under load or why rib spacing must scale with width.

### 3. **metadata.json** - Standardized Metadata
Unified, well-structured metadata combining model + context:
- Model information (name, version, purpose, author)
- Design intent analysis (critical features, design decisions, aesthetic requirements)
- Parameter metadata (8 parameters with full specs: type, range, variability, impact)
- Constraints metadata (tolerances, minimums, rules, dependencies)
- Materials metadata (print process, properties, post-processing)
- Assembly metadata (mounting interface, installation steps, load capacity)
- Variations metadata (planned sizes, how to generate them)

**Why AI needs this:** Single, authoritative source of truth formatted specifically for AI consumption. Removes ambiguity about parameter ranges, constraints, and relationships.

### 4. **parameters.json** - Code Generation Ready
Parameter definitions formatted for CLI and code generation:
- 8 parameters with: type, unit, min/max/default, step, CLI arguments, validation rules
- Derived parameters (rib spacing, boss height calculated from base width)
- CLI interface specification (example commands, usage patterns)
- Validation rules (pre-generation and post-generation checks)
- Code structure recommendations (imports, function signatures, helper functions)

**Why AI needs this:** Directly usable template for generating Python CLI. Tells AI exactly what function signature to create, what command-line arguments to support, and what validation to implement.

### 5. **constraints.json** - Design Rules & Validation
Complete constraint specification:
- Tolerance constraints (mounting holes ±0.1mm, walls ±0.2mm, corners ±0.5mm)
- Structural constraints (minimum wall thickness 1.5mm, hole diameter 3mm minimum)
- FDM printability constraints (minimum feature 0.4mm, fillet radius 1mm, overhang 45°)
- Design rule constraints (hole positions, base depth fixed, rib spacing formula, taper factor)
- Parameter dependency constraints (height scales with width, spacing scales with width)
- Variation constraints (3 standard sizes, mirroring)
- Quality assurance checks (body count, hole verification, volume, dimensions)

**Why AI needs this:** Prevents AI from generating invalid variations. Tells AI which parameters can vary, which must be fixed, what are the hard limits, and how to validate generated models.

## Success Criteria - What Makes a Package "AI-Ready"

A context package is "AI-ready" if it satisfies these criteria across three validation tiers:

### Tier 1: Package Completeness ✅

**All necessary files are present and valid:**
- [ ] All 5 JSON files present (model, context, metadata, parameters, constraints)
- [ ] Valid JSON syntax in each file (no unclosed braces or quotes)
- [ ] File sizes reasonable (model: 5-20KB, metadata: 10-30KB, parameters: 5-15KB, constraints: 10-30KB)
- [ ] Metadata headers complete (version, date, source_file, model_name)
- [ ] Total package size 30-100KB (indicates sufficient detail)

**Verification:** Run JSON validator on each file, check file sizes, confirm headers present.

### Tier 2: Data Consistency ✅

**The 5 files agree about what the model is:**
- [ ] Model name identical across all files (no spelling variations)
- [ ] All parameters appear in model.json, metadata.json, and parameters.json with same names, ranges, units, and defaults
- [ ] All 12 features appear consistently across model.json and metadata.json
- [ ] All constraints in constraints.json match design intent from context.json
- [ ] Material type consistent between context.json and metadata.json
- [ ] No contradictory constraints (e.g., width ranges don't conflict)

**Verification:** Cross-reference parameter names and values across files, verify constraint values align.

### Tier 3: AI Actionability ✅

**AI can actually use this to generate code:**

**Parameters are truly parameterized:**
- [ ] Features use parameter names, not hard-coded numbers (e.g., "BaseThickness" not "10")
- [ ] Derived parameters have formulas specified (e.g., RibSpacing = BaseWidth * 0.25)
- [ ] Parameter ranges are correct (min < default < max, steps divide range evenly)
- [ ] At least one parameter varies meaningfully (not all fixed or trivial)

**Constraints are specific and enforceable:**
- [ ] Constraints have numerical thresholds (not vague like "reasonable size")
- [ ] Constraints have enforcement methods (code validation rules, not just descriptions)
- [ ] Constraints tagged with severity (CRITICAL/HIGH/MEDIUM, not unlabeled)
- [ ] Each constraint explains failure consequences (what breaks if violated)
- [ ] At least one structural constraint present (model fails without it, not just formatting)

**Design intent is clear:**
- [ ] Purpose explicitly stated (not generic like "a bracket")
- [ ] Load/stress requirements documented (rated capacity, failure modes)
- [ ] Design trade-offs explained (why each decision was made)
- [ ] Critical features marked as non-negotiable (must always be true)
- [ ] Planned variations described (what, how many, how to generate)

**Code generation is specified:**
- [ ] Function signatures specified (input parameters, output format, return type)
- [ ] CLI interface fully defined (argument names, example commands, defaults)
- [ ] Validation logic specified in code format (not prose)
- [ ] Feature implementation hints provided (which features are which operations)
- [ ] Helper functions identified (sketches, pattern algorithms)

**Verification:** Read parameters.json—can you build a CLI from it? Read constraints.json—can you write validation code? Read metadata.json—do design decisions make sense? Can you trace feature construction in model.json?

### Tier 3 Advanced: AI Tested ✅ (Validation After Code Generation)

**Does AI actually generate working code?**
- [ ] Generated code runs without syntax errors
- [ ] CLI accepts all documented parameters
- [ ] Invalid parameters rejected with clear error messages
- [ ] Output files valid (can open in CAD software, are solid geometry)
- [ ] Generated models match original for default parameters (within 0.5mm)
- [ ] Model variations work correctly (constraints honored across all variations)

**Quick Readiness Check (5 minutes):**
```
☐ All 5 JSON files present and valid
☐ Same parameter names everywhere
☐ Same model name everywhere
☐ No contradictory constraints
☐ At least 1 parameter varies (min < max)
☐ At least 1 structural constraint
☐ Design intent clear (purpose + load requirements)
☐ Code generation specs provided (function sig, CLI args)
☐ Validation rules in code format
```
If all checked → **Ready for AI.**

## What AI Should Do With This Package

When given this complete context package, AI should:

1. **Parse and Validate** (10 seconds)
   - Load all 5 JSON files
   - Verify consistency between files
   - Confirm no missing constraints or parameters

2. **Understand the Model** (30 seconds)
   - Trace through feature timeline in model.json
   - Understand how each parameter drives features
   - Identify derived parameters and relationships

3. **Generate Python Code** (2-5 minutes)
   - Create `generate_shelfbracket.py` using CadQuery
   - Implement all parameters from parameters.json
   - Add all validation rules from constraints.json
   - Build features in order specified in model.json

4. **Generate CLI Interface** (1 minute)
   - Create argparse interface per parameters.json spec
   - Add all validation and error checking
   - Support all output formats (STEP, STL)

5. **Generate Examples** (30 seconds)
   - Create example commands from cli_interface section
   - Generate sample models for different parameter values
   - Verify output matches documented behavior

6. **Return Generated Script** (immediately)
   - Complete `generate_shelfbracket.py` file
   - With all features, validation, and CLI
   - Ready to use immediately

**Result:** AI should be able to generate working parameterized code that:
- Reproduces the original model with default parameters
- Accepts all documented CLI arguments
- Validates inputs against all constraints
- Generates correct model variations
- Produces valid STEP/STL files

## Usage Example

```bash
# AI receives this context package and generates generate_shelfbracket.py

# User can then do:
python generate_shelfbracket.py --width 100 --output bracket_small.step
python generate_shelfbracket.py --width 200 --output bracket_medium.step
python generate_shelfbracket.py --width 300 --output bracket_large.step

# Or with custom parameters:
python generate_shelfbracket.py --width 150 --rib-height 6 --output custom.step
```

## Validation Checklist

Before sending to AI, verify:

- [ ] All 5 JSON files present
- [ ] All JSON files are valid (no syntax errors)
- [ ] No contradictions between files
- [ ] All parameters have min/max/default values
- [ ] All constraints documented with enforcement method
- [ ] CLI arguments specified for variable parameters
- [ ] Validation rules clear for each constraint
- [ ] Design relationships documented (which parameters affect what)
- [ ] Output format specified (STEP, STL, filename pattern)
- [ ] Quality assurance checks defined (how to validate generated model)

## Next Steps

### For Content Creators
1. Export your Fusion 360 model using fissionreactor export script
2. Answer the 28-question questionnaire
3. Run metadata transformation (Phase 2 of fissionreactor workflow)
4. Use this directory structure as template
5. Verify checklist above
6. Send to AI

### For AI Integration
1. Create standardized parser for all 5 JSON files
2. Implement consistency validation
3. Extract code generation templates from parameters.json
4. Use constraints.json for validation logic
5. Return both generated code and validation report

## File Sizes & Complexity

| File | Size | Complexity | Primary Audience |
|------|------|-----------|------------------|
| model.json | ~6KB | Medium | AI (feature timeline) |
| context.json | ~4KB | High | AI (design rationale) |
| metadata.json | ~13KB | High | AI (unified spec) |
| parameters.json | ~6KB | Medium | AI (code generation) |
| constraints.json | ~12KB | High | AI (validation rules) |

**Total: ~41KB** (including example files)

## Design Philosophy

This context package follows key principles:

1. **Completeness over brevity** - Better to repeat information clearly than have AI guess
2. **Explicit over implicit** - Constraints documented explicitly, not hidden in examples
3. **Actionable over descriptive** - Includes code templates, CLI specs, validation rules
4. **Validated over assumed** - QA checks specify how to verify generated models work
5. **AI-friendly over human-readable** - Structured JSON, not prose descriptions

## Related Documentation

- `../questionnaire_guide.md` - How to fill out context questionnaire
- `../export_fusion360_guide.md` - How to export design data from Fusion 360
- `../README.md` - fissionreactor overview and workflow
- `../transform_metadata_guide.md` - How to use the metadata transformation tool
- `../generator-guide/generation-guide.md` - How to generate parameterized code

## Common Failures to Avoid

When creating your own context package:

### ❌ Parameters Not Truly Variable
```
BAD:  "BaseWidth": {"min": 200, "max": 200}  (no range)
GOOD: "BaseWidth": {"min": 100, "max": 300}  (meaningful variation)
```

### ❌ Constraints Too Vague
```
BAD:  "Note": "Holes should be reasonable size"
GOOD: "Holes must be 3.2 ± 0.1mm diameter (M3 bolt fit tolerance)"
```

### ❌ Design Intent Missing
```
BAD:  "Purpose": "A bracket"
GOOD: "Corner bracket for modular shelving, connects aluminum posts to shelves, supports 20kg load per bracket"
```

### ❌ Code Generation Specs Incomplete
```
BAD:  "Parameters": ["width", "height"]
GOOD: Includes cli_arg (--width), validation rule, default, range, step
```

### ❌ Features in Wrong Order
```
BAD:  Features listed: Tapered Walls, Base Extrude, Holes  (not construction order)
GOOD: Features listed: Base Extrude, Holes, Tapers, Fillets  (matches Fusion 360 timeline)
```

## How to Create Your Own Package

1. **Export your model** using fissionreactor export script → `model.json`
2. **Answer questionnaire** using questionnaire_guide.md → `context.json`
3. **Create metadata.json** by combining model + context, using metadata.json from this example as template
4. **Create parameters.json** specifying CLI interface and validation rules
5. **Create constraints.json** documenting all design rules and limits
6. **Validate** using the Quick Readiness Check above (5 minutes)
7. **Send to AI** with prompt: "Generate parameterized CadQuery script per these specifications"

## Troubleshooting

### If AI generates code but models are wrong:
→ Likely missing constraint information. Check constraints.json completeness.

### If AI generates code with poor validation:
→ Likely missing validation rules. Check parameters.json has validation field.

### If AI generates code but features are missing:
→ Likely feature timeline incomplete. Check model.json has all features in correct order.

### If generated code doesn't match original model:
→ Likely parameter specification wrong. Check parameters.json min/max/default values match Fusion 360.

## Scoring: Is Your Package Ready?

| Criterion | Points |
|-----------|--------|
| Tier 1: All 5 files present & valid | 10 pts |
| Tier 2: Parameter consistency | 20 pts |
| Tier 2: Constraint consistency | 10 pts |
| Tier 3: Parameters parameterized | 14 pts |
| Tier 3: Constraints enforceable | 14 pts |
| Tier 3: Design intent clear | 14 pts |
| Tier 3: Code specs complete | 14 pts |

**Score: 0-30** = Not ready (missing major sections)
**Score: 31-60** = Partially ready (needs clarification)
**Score: 61-85** = Mostly ready (minor gaps)
**Score: 86-100** = Production ready (AI can generate working code)
