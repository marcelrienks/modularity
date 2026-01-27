# What AI Needs to See - Context Package Requirements

## Executive Summary

To generate working, parameterized Python code from a CAD model, AI needs:

1. **Complete design data** (model.json) - What the model looks like
2. **Design intent** (context.json) - Why the model looks that way
3. **Unified metadata** (metadata.json) - What features are parameterizable and how
4. **Code generation specs** (parameters.json) - Exactly how to build the Python script
5. **Validation rules** (constraints.json) - How to know if generated code is correct

**Without this:** AI generates syntactically correct code that might generate invalid models or miss critical design requirements.

**With this:** AI generates production-ready code that respects all constraints, validates inputs, and generates correct models reliably.

---

## What Each AI System Needs

### Large Language Models (Claude, GPT, etc.)

**Context Package Input:**
- All 5 JSON files provided
- README.md as instruction guide
- Clear prompt: "Generate a CadQuery Python script that reproduces this model with parameter variations per metadata.json specs"

**What LLM Should Do:**
1. Parse and understand all JSON files
2. Identify parameter relationships and constraints
3. Map Fusion 360 features to CadQuery equivalents
4. Generate function skeleton with all parameters
5. Implement each feature in order from model.json
6. Add validation logic from constraints.json
7. Create CLI interface per parameters.json
8. Return complete, tested Python script

**Quality Indicators:**
- Generated script runs without errors
- Output STL/STEP files are valid 3D models
- Generated models match original for default parameters
- Generated models respect all parameter constraints
- CLI accepts all documented arguments
- Validation catches invalid parameter combinations

### Code Generation Systems (AST-based)

**Context Package Input:**
- metadata.json (primary - most structured)
- parameters.json (for CLI specs)
- constraints.json (for validation rules)
- model.json (for feature reference)

**What System Should Do:**
1. Parse JSON AST definitions
2. Generate Python AST nodes per feature specs
3. Build validation function tree from constraints
4. Emit Python source code
5. Format and optimize

**Quality Indicators:**
- Generated code is valid Python
- Functions have correct signatures
- All parameters present in generated functions
- Validation logic matches constraints.json exactly

### Custom AI Workflows

**Adapt Based On:**
- Task complexity (single feature vs. full model)
- Model type (mechanical part, architectural, tool holder)
- Parameterization scope (all features or subset)
- Output format (Python, other languages, simulation data)

**Universal Need:**
- metadata.json is always sufficient starting point
- Other files provide additional detail and specificity
- Validation rules must be honored

---

## Required Information Categories

### 1. Design Data (model.json)

AI needs to know:

```
✅ All parameters and their usage locations
✅ All sketches and their geometry definitions
✅ Feature timeline in exact construction order
✅ Which features are operations (extrude, fillet, etc.)
✅ Feature dependencies (what each feature operates on)
✅ Body structure and naming
✅ Physical dimensions (bounding box, volume)
```

**Example - Why This Matters:**
- Fusion 360 model has "Tapered Walls" feature using scale operation
- Without feature timeline: AI doesn't know about taper
- With timeline: AI can implement scale operation in correct position
- Result: Generated model matches original

### 2. Design Intent (context.json)

AI needs to know:

```
✅ Primary purpose and use cases
✅ Critical features that CANNOT vary
✅ Design trade-offs made (speed vs. strength, cost vs. durability)
✅ Material properties and fabrication method
✅ Assembly requirements and load constraints
✅ Why certain decisions were made
✅ Planned variations and configurations
```

**Example - Why This Matters:**
- Model has 1.5mm minimum wall thickness
- Geometry alone: AI sees "1.5mm" but might think it's negotiable
- With context: AI learns "below 1.5mm, parts break under 20kg load"
- Result: AI adds validation rule, rejects parameters that violate this

### 3. Metadata (metadata.json)

AI needs to know:

```
✅ Which parameters are variable (high/medium/low variability)
✅ Ranges for each parameter and why (hard limits vs. recommended ranges)
✅ Relationships between parameters (derived vs. independent)
✅ Constraints on each parameter individually and together
✅ Design rules that must always be true
✅ How to detect if something went wrong
```

**Example - Why This Matters:**
- BaseThickness parameter: ranges 8-12mm, default 10mm
- Metadata specifies: changes rib prominence, affects load capacity
- Tells AI: "this is structural - don't pick random value, validate it matters"
- Result: AI implements proper validation, not just "check range"

### 4. Code Generation Specs (parameters.json)

AI needs to know:

```
✅ CLI argument names for each parameter
✅ Validation logic (code snippets, not just descriptions)
✅ Derived parameter formulas
✅ Output format and filename patterns
✅ Suggested function signatures
✅ Example CLI commands
✅ Pre and post-generation checks
```

**Example - Why This Matters:**
- parameters.json specifies: `--width` arg, validation `value % 10 == 0`
- Without spec: AI might allow any width value
- With spec: AI implements the 10mm step requirement
- Result: Generated script matches intended behavior exactly

### 5. Validation Rules (constraints.json)

AI needs to know:

```
✅ Tolerance specifications for each constraint
✅ Why each constraint exists (functional vs. manufacturing)
✅ Severity level (CRITICAL vs. HIGH vs. MEDIUM)
✅ How to detect violations (code checks to implement)
✅ How to recover from violations (error messages to show)
✅ QA tests to run on generated models
```

**Example - Why This Matters:**
- Mounting holes must be 3.2mm ± 0.1mm
- Without constraint details: AI implements basic range check
- With constraint: AI knows "0.1mm tolerance means measure test print"
- Result: Generated script helps user validate prints work

---

## Completeness Checklist

Before sending context package to AI, verify all items:

### Design Data
- [ ] All 8 parameters documented with units and ranges
- [ ] Every parameter has min/max/default values
- [ ] All 3 sketches defined (BaseProfile, MountingHoles, RibPattern)
- [ ] All 12 features listed in construction order
- [ ] Each feature specifies which sketch it uses
- [ ] Derived parameters (RibSpacing, BossHeight) have formulas
- [ ] Bounding box dimensions documented

### Design Intent
- [ ] Primary use case documented (shelf mounting)
- [ ] Load requirement specified (20kg capacity)
- [ ] Material specified (PLA)
- [ ] Fabrication method specified (FDM 3D printing)
- [ ] Critical features identified (mounting holes, wall thickness)
- [ ] Design trade-offs explained (tapered walls for weight)
- [ ] Planned variations listed (3 sizes, mirror versions)
- [ ] Assembly method documented (M3 bolts)

### Metadata
- [ ] Parameter variability classified (high/medium/low)
- [ ] Constraints categorized (tolerance/structural/FDM/rules/dependencies)
- [ ] Critical features marked as non-negotiable
- [ ] Design decisions traced to parameters
- [ ] Material properties documented
- [ ] Load and stress information included
- [ ] Variation generation strategy described
- [ ] QA criteria defined

### Code Generation Specs
- [ ] All variable parameters have CLI arguments defined
- [ ] Fixed parameters clearly marked as not configurable
- [ ] Derived parameters have formulas specified
- [ ] Validation rules in code format (not prose)
- [ ] Example CLI commands provided
- [ ] Output filename pattern specified
- [ ] Function signatures suggested
- [ ] Pre/post generation checks listed

### Validation Rules
- [ ] Tolerance constraints specified with ± values
- [ ] Structural constraints tied to failure modes
- [ ] FDM printability constraints documented
- [ ] Design rules specified (must always be true)
- [ ] Parameter dependencies clearly stated
- [ ] Severity levels assigned to each constraint
- [ ] Detection methods specified (code checks)
- [ ] QA tests for model validation provided

---

## Common Information Gaps (What AI Fails At)

### Gap 1: "What's the actual feature construction order?"

❌ **Incomplete:** "Model has 12 features"
✅ **Complete:** "Features 1-3: Base/Boss/Taper, Features 4-5: Holes/Ribs, Features 6-12: Fillets/Chamfers/Shell/Draft/Offset/Final"

### Gap 2: "Why can't this parameter vary?"

❌ **Incomplete:** "BaseDepth = 150mm (fixed)"
✅ **Complete:** "BaseDepth = 150mm (FIXED - must match aluminum post connector spacing standard, cannot vary)"

### Gap 3: "How do I validate generated models?"

❌ **Incomplete:** "Check that model is valid"
✅ **Complete:** "Check: 1) exactly 1 body, 2) 4 through-holes, 3) volume 50k-150k mm³, 4) walls ≥ 2mm, 5) holes 3.0-3.4mm diameter"

### Gap 4: "What parameters can the user change?"

❌ **Incomplete:** "8 parameters total"
✅ **Complete:** "4 variable (width, thickness, corner-radius, rib-height), 2 fixed (depth, base-thickness), 2 derived (spacing, boss-height)"

### Gap 5: "Why does this parameter matter?"

❌ **Incomplete:** "CornerRadius: 1.5mm (range 1.5-3mm)"
✅ **Complete:** "CornerRadius: 1.5mm default (range 1.5-3mm minimum, FDM print reliability - below 1.5mm causes failures)"

---

## Validation: Is Your Package Ready?

### 15-Minute Readiness Check

1. **Open all 5 JSON files** - Are they valid JSON? (Use online validator if unsure)
2. **Check parameter consistency** - Does each parameter appear in model.json, metadata.json, and parameters.json with same name and ranges?
3. **Verify feature timeline** - Are all 12 features listed in construction order in model.json?
4. **Scan constraints** - Do all CRITICAL constraints from constraints.json make sense for the model?
5. **Test CLI specs** - Could you actually run the CLI commands in parameters.json?

**If all 5 pass:** Your package is ready for AI.

### 30-Minute Deep Check

1. **Trace one parameter through all files** - Pick BaseWidth, verify it appears correctly everywhere
2. **Verify one constraint** - Pick "wall thickness 2mm minimum", confirm it's documented in all relevant files
3. **Map one feature** - Pick "Mounting Holes" feature, verify it's defined in model.json and used in constraints.json
4. **Review design decisions** - Are the trade-offs in context.json reflected in constraints.json?
5. **Test parameter relationships** - If you change BaseWidth in metadata, do derived parameters (RibSpacing) update correctly?

**If all 5 pass:** Your package is production-ready.

---

## Examples of "Ready" vs "Not Ready"

### Ready Package ✅
```json
// parameters.json
{
  "BaseWidth": {
    "type": "length",
    "unit": "mm",
    "default": 200,
    "min": 100,
    "max": 300,
    "step": 10,
    "cli_arg": "--width",
    "validation": "if not (100 <= value <= 300 and value % 10 == 0): raise ValueError(...)"
  }
}
```
✅ All fields present. ✅ Validation rule in code format. ✅ CLI arg specified. ✅ Step value documented.

### Not Ready ❌
```json
// parameters.json (incomplete)
{
  "BaseWidth": {
    "default": 200,
    "range": "100-300"
  }
}
```
❌ Missing unit. ❌ No step value. ❌ No CLI arg. ❌ No validation rule. ❌ No "min/max" structure.

---

## Next Steps

### If You Have a Partial Package
1. Use this checklist to identify what's missing
2. Check the example-context-package for complete format
3. Fill in missing information using questionnaire_guide.md for help
4. Run through 15-minute readiness check
5. Send to AI

### If You Have Questions
1. Refer to questionnaire_guide.md for what each question means
2. Check export_fusion360_guide.md for how to get design data
3. Review example-context-package/README.md for what "complete" looks like
4. Consult fissionreactor main README for workflow overview

### If AI Struggles With Your Package
1. Likely cause: Missing information from this document
2. Solution: Review "What Each AI System Needs" section above
3. Compare your package to example-context-package
4. Fill in gaps and resubmit
5. Success rate usually improves 10-20% per round of clarification
