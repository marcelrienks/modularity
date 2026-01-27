# Task 3: AI-Ready Context Package

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

A context package is "AI-ready" if it satisfies these criteria:

### ✅ Completeness
- [ ] All 5 JSON files present and valid
- [ ] No critical information missing (use questionnaire_guide.md to verify all questions answered)
- [ ] All parameters documented with ranges and constraints
- [ ] All design decisions explained in context and metadata

### ✅ Consistency
- [ ] No contradictions between model.json, context.json, and metadata.json
- [ ] Parameter names consistent across all files
- [ ] Constraint values match documented specifications
- [ ] Design rules match actual model construction

### ✅ Actionability for AI
- [ ] Parameters are truly parameterized (not hard-coded values)
- [ ] Constraints are specific and enforceable (not vague)
- [ ] Design intent is clear (not ambiguous)
- [ ] Relationships between parameters documented
- [ ] CLI interface defined (what arguments, what outputs)
- [ ] Validation rules specified (how to check if generated model is valid)

### ✅ CadQuery Code Generation Ready
- [ ] Code structure specified (function signatures, helper functions)
- [ ] Parameter validation rules provided (ranges, dependencies)
- [ ] Output format specified (STEP, STL, with filenames)
- [ ] Feature order matches Fusion 360 timeline
- [ ] All sketches and features can be translated to CadQuery equivalents

### ✅ Documentation
- [ ] All files have metadata headers with version, date, source
- [ ] Each parameter has clear purpose and impact explanation
- [ ] Each constraint has violation risk and recovery strategy
- [ ] Examples provided (CLI commands, parameter variations, output files)
- [ ] README explains what AI should do with each file

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
