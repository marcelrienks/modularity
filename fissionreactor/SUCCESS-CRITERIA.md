# Task 3 Success Criteria - AI-Ready Context Package

## Overview

This document defines what makes a context package "AI-ready" - i.e., sufficient for AI to generate working parameterized code.

---

## Three Success Tiers

### Tier 1: Package Completeness ✓

**Question:** Are all necessary files present and valid?

**Criteria:**

```
☐ All 5 files present:
  ☐ model.json (design export)
  ☐ context.json (questionnaire responses)
  ☐ metadata.json (standardized metadata)
  ☐ parameters.json (code generation specs)
  ☐ constraints.json (validation rules)

☐ All JSON files valid:
  ☐ No syntax errors in any file
  ☐ All required top-level keys present
  ☐ No unclosed braces or quotes

☐ File sizes reasonable:
  ☐ model.json: 5-20KB (design export varies by model complexity)
  ☐ context.json: 3-8KB (questionnaire is fixed-size)
  ☐ metadata.json: 10-30KB (comprehensive specs)
  ☐ parameters.json: 5-15KB (parameter definitions)
  ☐ constraints.json: 10-30KB (constraint documentation)
  ☐ Total: 33-103KB (indicates sufficient detail)

☐ Metadata headers complete:
  ☐ version field present
  ☐ generated_date or created_date present
  ☐ source_file or model_name present
```

**Verification Method:**
- Run JSON validator on each file
- Check file sizes with `ls -lh`
- Open in text editor, verify readable and complete

**Pass/Fail:** If any file missing or invalid, package is NOT ready. Return to Phase 1-2 (export and questionnaire).

---

### Tier 2: Data Consistency ✓

**Question:** Do the files agree about what the model is?

**Criteria:**

```
☐ Model name consistent:
  ☐ Same name appears in: model.json, context.json, metadata.json
  ☐ No spelling variations or abbreviations

☐ Parameter consistency:
  ☐ All 8 parameters appear in: model.json, metadata.json, parameters.json
  ☐ Same names (no "Width" vs "width" vs "BaseWidth" confusion)
  ☐ Same min/max/default values across all files
  ☐ Same unit (all mm, not mm/cm mix)
  ☐ Same variability classification (variable/fixed/derived)

☐ Feature consistency:
  ☐ All 12 features listed in model.json appear in metadata.json context
  ☐ Same feature names and order
  ☐ Feature descriptions match between files

☐ Constraint consistency:
  ☐ All constraints in constraints.json match design intent from context.json
  ☐ Tolerance values (± numbers) are realistic and consistent
  ☐ No contradictory constraints (e.g., "width 100-300mm" vs "width 150mm minimum" conflict)

☐ Material consistency:
  ☐ Material type same in context.json and metadata.json
  ☐ Fabrication method consistent (no "FDM" vs "3D printing" confusion)
  ☐ Print settings (layer height, infill) reasonable for stated material
```

**Verification Method:**
- Create comparison spreadsheet: parameter names, ranges across files
- Search for constraint values: confirm they appear consistently
- Review model.json and metadata.json in parallel, cross-reference

**Pass/Fail:** If significant inconsistencies found (>2 conflicting values), fix and revalidate.

---

### Tier 3: AI Actionability ✓

**Question:** Can AI actually use this to generate code?

**Criteria:**

#### A. Parameters are Truly Parameterized

```
☐ No hard-coded values in feature definitions:
  ☐ Features use parameter names, not numbers
  ☐ Example GOOD: "distance": "BaseThickness"
  ☐ Example BAD: "distance": 10

☐ Derived parameters have formulas:
  ☐ RibSpacing = BaseWidth * 0.25 (formula specified, not value)
  ☐ BossHeight = BaseWidth * 0.15 (formula specified, not value)

☐ Parameter ranges make sense:
  ☐ Min < Max (not backwards)
  ☐ Default between Min and Max
  ☐ Step divides range evenly
  ☐ Example BAD: min=300, max=100 (backwards)

☐ At least one parameter is truly variable:
  ☐ BaseWidth varies (100-300mm)
  ☐ Not all parameters fixed or derived
  ☐ Variations make sense (not changing random tiny feature)
```

#### B. Constraints are Specific & Enforceable

```
☐ Constraints have numerical thresholds:
  ☐ NOT: "Holes should be reasonable"
  ✓ YES: "Holes must be 3.2 ± 0.1mm" or "if hole_diameter < 3.0: raise ValueError"

☐ Constraints have enforcement methods:
  ☐ Code validation rules specified (not just descriptions)
  ☐ Example: validation: "if not (1.5 <= value <= 3): raise ValueError(...)"

☐ Constraints have severity levels:
  ☐ CRITICAL constraints marked (model fails without)
  ☐ HIGH constraints marked (assembly fails without)
  ☐ MEDIUM constraints marked (print quality without)

☐ Constraints have failure descriptions:
  ☐ Each constraint explains: what happens if violated
  ☐ Example: "MinWallThickness < 1.5mm → part breaks under 20kg load"

☐ At least one constraint is truly structural:
  ☐ Not all constraints are formatting issues
  ☐ Example: MinWallThickness = 1.5mm (failure if violated)
```

#### C. Design Intent is Clear

```
☐ Purpose explicitly stated:
  ☐ NOT: "A bracket thing"
  ✓ YES: "Corner bracket for modular shelving, supports 20kg load"

☐ Load/stress requirements documented:
  ☐ If structural: rated load specified
  ☐ Material properties documented
  ☐ Failure modes described

☐ Design trade-offs explained:
  ☐ NOT: "Tapered walls"
  ✓ YES: "Tapered walls reduce weight while maintaining strength"

☐ Critical features marked as non-negotiable:
  ☐ Example: "Mounting holes MUST be in exact corners"
  ☐ Example: "BaseDepth MUST be 150mm for post alignment"

☐ Planned variations described:
  ☐ What variations are possible (sizes, materials, orientations)
  ☐ How many variations planned (3 sizes, 2 orientations, etc.)
  ☐ How to generate variations (change which parameters)
```

#### D. Code Generation is Specified

```
☐ Function signatures specified:
  ☐ Input parameters defined
  ☐ Output format defined (STEP, STL, etc.)
  ☐ Return type clear (CadQuery object)

☐ CLI interface defined:
  ☐ Argument names specified (--width, --thickness, etc.)
  ☐ Example commands provided
  ☐ Default output filename specified

☐ Validation logic specified:
  ☐ Pre-generation checks (validate parameters before generating)
  ☐ Post-generation checks (validate model after generation)
  ☐ Code format for checks provided

☐ Feature implementation hints provided:
  ☐ Which features are extrudes, which are pockets, etc.
  ☐ Which sketch each feature uses
  ☐ Feature dependencies documented

☐ Helper functions identified:
  ☐ Complex sketches broken into helper functions
  ☐ Patterns (rib spacing) identified as separate functions
```

#### E. Model is Realistic

```
☐ Part has appropriate complexity:
  ☐ At least 3-4 varied parameters (not trivial)
  ☐ At least 8-12 features (not overly simple)
  ☐ Meaningful constraints (not just "must fit in printer")

☐ Parameters have meaningful ranges:
  ☐ NOT: width 100-101mm (too narrow)
  ✓ YES: width 100-300mm (meaningful variation)

☐ Model has clear purpose:
  ☐ NOT: "Generic shape experiment"
  ✓ YES: "Shelf bracket for 3D-printed storage system"

☐ Fabrication method specified:
  ☐ Material type (PLA, PETG, etc.)
  ☐ Process (FDM 3D printing)
  ☐ Printer model or specifications
```

**Verification Method:**
- Read parameters.json: can you construct a CLI from this?
- Read constraints.json: can you write validation code from this?
- Read metadata.json: do design decisions make sense?
- Read context.json: would a new person understand the model's purpose?
- Read model.json: can you trace feature construction?

**Pass/Fail:** If any section fails, identify which criteria are missing and add them to metadata/parameters/constraints files.

---

### Tier 3 Advanced: AI Tested

**Question:** Does AI actually generate working code?

**Criteria:**

```
☐ AI generates without errors:
  ☐ Code runs without syntax errors
  ☐ No import errors or missing dependencies
  ☐ Script executes with --help and returns usage

☐ Generated code accepts parameters:
  ☐ CLI arguments work (--width 200 produces different model than --width 100)
  ☐ Parameters affect model correctly
  ☐ Invalid parameters rejected with clear error messages

☐ Generated models are valid:
  ☐ Output files created (STEP/STL files appear)
  ☐ Output files can be opened in CAD software (Fusion 360, Meshlab)
  ☐ Output models are solids, not broken geometry
  ☐ Output models have correct bounding box for parameters

☐ Generated models match original:
  ☐ Model with default parameters visually matches Fusion 360 original
  ☐ Feature sequence is correct (extrudes, pockets, fillets in right order)
  ☐ Dimensions are within 0.5mm of original
  ☐ Mounting holes in correct positions

☐ Model variations work:
  ☐ Changing width parameter produces correctly-sized variants
  ☐ All constraint rules honored (walls never < 1.5mm, holes always ± 0.1mm, etc.)
  ☐ Output quality consistent across parameter variations

☐ Documentation is correct:
  ☐ Generated code includes comments explaining features
  ☐ Constraint violations produce helpful error messages
  ☐ Generated CLI help is accurate (matches actual parameters)
```

**Verification Method:**
1. Send complete context package to AI (Claude/ChatGPT with CadQuery knowledge)
2. Request: "Generate parameterized CadQuery script per metadata.json"
3. Test generated script:
   - `python generate_shelfbracket.py --help`
   - `python generate_shelfbracket.py --width 100 --output test_small.step`
   - `python generate_shelfbracket.py --width 300 --output test_large.step`
   - `python generate_shelfbracket.py --wall-thickness 1.0 --output test_invalid.step` (should error)
4. Open generated STEP files in Fusion 360 or Meshlab, verify geometry

**Pass/Fail:** If generated code runs and produces valid models matching original, Tier 3 Advanced is COMPLETE. Context package is production-ready.

---

## Quick Checklist (5 Minutes)

```
Tier 1: Completeness
☐ All 5 JSON files present and valid

Tier 2: Consistency  
☐ Same parameter names everywhere
☐ Same model name everywhere
☐ No contradictory constraints

Tier 3: Actionability
☐ At least 1 parameter varies (min < max)
☐ At least 1 constraint structural
☐ Design intent clear (purpose + load requirements)
☐ Code generation specs provided (function sig, CLI args)
☐ Validation rules in code format
```

**Result:** If all checked, package is ready for AI.

---

## Scoring (for Project Management)

| Criterion | Points | Details |
|-----------|--------|---------|
| Tier 1: Completeness | 0-10 | All 5 files (2 pts each) |
| Tier 2: Consistency | 0-20 | Parameters (10), Features (5), Constraints (5) |
| Tier 3: Actionability | 0-70 | Parameterization (14), Constraints (14), Intent (14), Code Specs (14), Realistic (14) |
| **Total** | **0-100** | Points for evaluation |

**Scoring Guide:**
- 0-30: Not ready - missing major sections
- 31-60: Partially ready - needs significant clarification
- 61-85: Mostly ready - minor gaps, AI can work with it
- 86-100: Production ready - AI can generate working code

---

## Common Failure Points

### ❌ Fails: Parameters not truly variable
Example: `"BaseWidth": {"default": 200, "min": 200, "max": 200}`
Fix: Provide realistic range like `"min": 100, "max": 300`

### ❌ Fails: Constraints too vague
Example: `"Note": "Holes should be reasonable size"`
Fix: Specify exactly: `"Holes must be 3.2 ± 0.1mm diameter"`

### ❌ Fails: Design intent missing
Example: `"Purpose": "A bracket"`
Fix: Describe fully: `"Corner bracket for modular shelving system, connects aluminum posts to shelves, supports 20kg load per bracket"`

### ❌ Fails: Code generation specs incomplete
Example: `"Parameters": ["width", "height"]`
Fix: Provide full spec: CLI args, validation rules, function signatures

### ❌ Fails: Features not in order
Example: model.json lists Tapered Walls before Base Extrude
Fix: Reorder to match Fusion 360 timeline: Base → Holes → Ribs → Tapers → Fillets

---

## Success Story: ShelfBracket_v1

The example-context-package passes all Tiers:

**Tier 1:** ✅ All 5 files present, valid JSON, reasonable sizes
**Tier 2:** ✅ Consistent model name (ShelfBracket_v1) across files, 8 parameters match everywhere, 12 features match, constraints align with design intent
**Tier 3:** ✅ BaseWidth varies 100-300mm, MinWallThickness constraint is structural, purpose clear (shelf bracket + 20kg load), code generation specs complete, CLI args specified

**Result:** Ready for AI code generation → AI successfully generates `generate_shelfbracket.py` → Generated script produces valid models for all parameter combinations → Models match original for default parameters → Users can run: `python generate_shelfbracket.py --width 200 --output bracket.step`

---

## Next Steps

### If Package Passes All Tiers
1. ✅ Send to AI for code generation
2. ✅ AI generates parameterized Python script
3. ✅ Test generated script (run on default params, verify output matches original)
4. ✅ Document workflow for next model
5. ✅ Archive context package with design files

### If Package Fails a Tier
1. Identify which criteria failed
2. Refer to relevant section above for fixes
3. Compare against example-context-package
4. Re-validate using checklist
5. Resubmit for verification
