# Fissionreactor Project Review: Issues & Gaps

**Date:** 2026-01-29  
**Reviewed By:** Code Review Agent  
**Overall Score:** 65/100 - Not Production Ready

---

## CRITICAL ISSUES

### 1. **Export Script Only Works in Fusion 360 (Major Limitation)**
**Severity: CRITICAL**

The `export_fusion360_data.py` script is designed ONLY as a Fusion 360 Add-In. It:
- Requires `import adsk.core` / `import adsk.fusion` (Fusion API)
- Only works inside Fusion 360 via Tools > Add-ins menu
- **Cannot be tested** in development/CI without Fusion 360

**Impact:** Users cannot verify the export flow works. No example `model.json` format exists in the code—only a manually created example.

**Fix needed:** 
- Create standalone test mode OR example model.json generator
- Document that export output structure must match example

---

### 2. **Model.json Schema Mismatch with Transform Script**
**Severity: HIGH**

`validate_workflow.py` expects:
```python
REQUIRED_FIELDS = {
    'export_metadata': {...},
    'model': {
        'name': str,
        'part_count': int,
        'parameters': list,  # Expected at model.parameters
        'features': list,    # Expected at model.features
        'bodies': list       # Expected at model.bodies
    }
}
```

But `transform_metadata.py` extracts from:
```python
self.model.get('parameters', [])      # Top level
self.model.get('features', [])        # Top level  
self.model.get('components', [])      # Top level
```

**The real issue:** Example `model.json` has:
- `model.name`, `model.part_count`, `model.feature_count`
- Top-level `parameters` array
- Top-level `features` array (from timeline extraction)
- NO `model.parameters` or `model.features`

This means:
1. Validation will WARN about missing fields
2. Transform will work (it reads top-level)
3. **Documentation disagrees with actual code**

**Fix needed:** Standardize one structure across all three (export, validate, transform)

---

### 3. **Export Script Creates Wrong Directory Structure**
**Severity: MEDIUM**

Export code does:
```python
model_dir = self.script_dir / model_name
output_dir = model_dir / "origin"      # Creates model_name/origin/
output_file = output_dir / f"{model_name}.json"
```

Creates: `ShelfBracket_v1/origin/ShelfBracket_v1.json`

But docs & examples expect: `ShelfBracket_v1/model.json`

**Impact:** Users running export will get wrong directory structure. Then transform & validate will fail looking for `model.json` in wrong place.

**Fix needed:** Export should save to `model_dir/model.json` directly, not `model_dir/origin/model.json`

---

### 4. **Missing Input Validation for Export**
**Severity: MEDIUM**

`load_design()` checks design exists, but:
- No validation that design has parameters
- No validation that design has features
- No error if design is empty
- `export_model()` will happily create JSON with 0 parameters / 0 features

**Impact:** Silent failure - bad export files with no data

**Fix needed:** Add post-export validation in `FusionExporter.run()`

---

### 5. **Template Generator is NOT a Real Template**
**Severity: HIGH**

`template_generator.py` has:
- Placeholder function names like `def add_feature_1_base_extrude()`
- Placeholder parameters `Param1`, `Param2`, `Param3`
- Placeholder validation with made-up ranges
- Comments saying `{ModelName}`, `{Date}` but not actually filled in

**Problem:** This is NOT a reusable template. It's a worked example mixed with instructions.

Real issues:
1. Users can't use this as a starting point for their own models
2. AI would need to understand this is a template, not actual code
3. No template logic for automatic feature mapping

**What's really needed:**
- A Python script that GENERATES the generator script (codegen)
- Takes `parameters.json` + `constraints.json` + `features.json` as input
- Outputs actual `generate_mymodel.py` with real feature functions

**Current state:** Users are expected to ask AI to "use this as reference" and write from scratch.

---

### 6. **Questionnaire Fields Don't Map Cleanly to Output**
**Severity: MEDIUM**

Questionnaire JSON uses field IDs like:
- `purpose_primary`, `purpose_use_case`, `purpose_context`
- `intent_critical_features`, `intent_design_decisions`
- `constraint_tolerances`, `constraint_minimum`, `constraint_rules`

Transform script reads these fields directly and creates metadata files. But:
- Some questionnaire fields are optional (text_long with `required: false`)
- Transform doesn't validate these are filled before generating metadata
- Some metadata files will be incomplete if questionnaire is partial

**Impact:** Users can generate incomplete metadata without warning

**Fix needed:** Transform script should validate questionnaire completeness before proceeding

---

## REDUNDANCY & INCONSISTENCIES

### 7. **Documentation Inconsistency: model.json Structure**
- README says export creates `model.json` (correct)
- examples/README shows model.json with top-level fields (correct)
- validate_workflow.py expects nested `model.parameters` (wrong)
- docs/transform_metadata.md shows actual transform code (correct—reads top-level)

**Fix:** Update validation to match actual structure

---

### 8. **Redundant Field Names Across JSON Files**
- `metadata.json` repeats model name, version, author
- `parameters.json` repeats model name
- `constraints.json` repeats model name
- `features.json` repeats model name
- `assembly.json` repeats model name

**OK, but increases maintenance burden.** If model name changes, all 5 files must update.

---

### 9. **Multiple Validation Points with Different Rules**
- `validate_workflow.py` validates model.json structure
- `transform_metadata.py` loads model.json but doesn't validate structure
- `validate_workflow.py` checks context.json completeness
- `transform_metadata.py` doesn't check context.json required fields

**Better approach:** Consolidate validation into single tool or validate earlier

---

## MISSING PIECES

### 10. **No Schema Definitions**
**Severity: MEDIUM**

No JSON Schema files (`.schema.json`) for:
- model.json (Fusion 360 export output format)
- context.json (questionnaire responses)
- metadata.json, parameters.json, constraints.json, features.json, assembly.json

**Why it matters:**
- Users don't know what fields are required vs optional
- No automatic validation against schema
- AI can't validate output against schema

**Fix:** Create 7 JSON Schema files

---

### 11. **No Test Cases**
**Severity: MEDIUM**

No unit tests for:
- `transform_metadata.py` (does it handle edge cases?)
- `validate_workflow.py` (what about malformed JSON?)
- Example metadata transformation (is it repeatable?)

Can't verify:
- Invalid questionnaire → valid metadata?
- Partial questionnaire → partial metadata?
- Wrong parameter ranges → detected?

**Fix:** Add pytest tests for all Python scripts

---

### 12. **No Error Recovery Guide**
**Severity: LOW**

Docs explain what *should* happen, but not what to do if:
- Export produces invalid JSON
- Transform fails on bad input
- Generated code doesn't run
- Model doesn't match original

README has "Troubleshooting" but it's minimal.

**Fix:** Expand troubleshooting section with real failure scenarios

---

### 13. **No Conversion Tool from Old to New Format**
**Severity: LOW**

If someone exports with an old version of the add-in, can they upgrade? No migration guide.

---

## CODE QUALITY ISSUES

### 14. **Export Script Has Bare `except:` Clauses**
**Severity: MEDIUM**

Multiple places use bare exception handlers:
```python
except:  # Line 149, 194, etc.
    pass
```

This hides real errors. Should catch specific exceptions.

---

### 15. **Parameter Default Values Are Magic Numbers**
**Severity: LOW**

In `transform_metadata.py`:
```python
param_max = param_value * 2 if param_value else 100  # Magic numbers
```

Where does `* 2` or `100` come from? Should be configurable.

---

### 16. **No Type Hints**
**Severity: LOW**

Some type hints (in transform_metadata.py) but missing in:
- validate_workflow.py (especially report messages)
- export_fusion360_data.py

---

## MISSING DOCUMENTATION

### 17. **No JSON Schema Documentation**
No docs explaining:
- `model.json` required vs optional fields
- `context.json` required vs optional fields  
- Expected value types and ranges

### 18. **No Troubleshooting for Common Errors**
Example missing answers:
- "I filled questionnaire partially—will it work?" (No, transform fails silently on some fields)
- "Export created `model_name/origin/` folder—where's model.json?" (Wrong folder)
- "Transform completed but metadata looks empty" (Questionnaire incomplete)
- "Generated code won't run" (Missing CadQuery? Parameters wrong?)

### 19. **No API Documentation**
For developers extending the tool:
- How to add new constraint types?
- How to add new parameter types?
- How to customize metadata transformation?

---

## WORKFLOW ISSUES

### 20. **No Dry-Run Mode**
**Severity: LOW**

Users can't test workflow without actually:
1. Exporting from Fusion 360
2. Filling questionnaire
3. Running transformation
4. Sending to AI

A dry-run with synthetic data would help testing.

---

## ASSESSMENT SUMMARY

### **Code Readiness: 65% / 100**

**What Works:**
✅ transform_metadata.py — solid, handles most cases, produces valid output  
✅ validate_workflow.py — decent validation, clear reporting  
✅ generate_shelfbracket_example.py — excellent worked example, proper structure  
✅ questionnaire template — comprehensive, covers design space  
✅ Documentation — thorough and well-organized  

**What Doesn't Work:**
❌ export_fusion360_data.py — untestable, wrong directory structure, unvalidated output  
❌ Model schema — inconsistent between export, validation, transform  
❌ template_generator.py — not a real template, more like a reference  
❌ No automated testing  
❌ Silent failures on incomplete questionnaire  

**What's Missing:**
❌ JSON Schemas (7 files)
❌ Unit tests  
❌ Codegen tool to generate generator scripts  
❌ Better error handling  
❌ Schema validation at each step  

---

## RECOMMENDATIONS (Priority Order)

### P0 (Breaking Issues)
1. **Fix export script directory structure** — currently wrong
2. **Standardize model.json schema** — currently inconsistent
3. **Add questionnaire validation** — currently accepts incomplete data
4. **Add schema validation** — currently no schema validation at any step

### P1 (Major Gaps)
5. Create JSON Schema files for all 5 metadata formats
6. Create codegen tool to generate generator scripts
7. Add unit tests for all Python scripts
8. Fix bare `except:` clauses

### P2 (Nice to Have)
9. Add more troubleshooting examples
10. Add developer API docs
11. Add dry-run mode with synthetic data
12. Create migration guide for format versions

---

## Can This Ship?

**Currently: NO** — Export script has critical bugs that will break user workflow

**After P0 fixes: MAYBE** — Core workflow works but lacks validation and testing

**After P0+P1: YES** — Robust, tested, well-defined
