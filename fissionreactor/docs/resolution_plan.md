# Fissionreactor Project Resolution Plan

**Status: PLANNING**  
**Current Code Readiness: 65/100**  
**Target: 90/100 for production release**

---

## Overview

The fissionreactor project has solid concepts but critical implementation issues that block user workflows. This plan prioritizes fixes by impact and complexity.

### Quick Summary
- **Breaking issues**: 4 (export directory structure, schema mismatch, validation gaps, untestable code)
- **Major gaps**: 4 (no schemas, no tests, no codegen tool, missing error handling)
- **Nice-to-haves**: 4 (better docs, dry-run mode, migration guide, API docs)

---

## P0: Breaking Issues (Must Fix Before Any Release)

These issues will immediately break user workflows.

### ⬜ 1. Fix Export Script Directory Structure
**Impact**: CRITICAL — Users will have wrong file structure  
**Effort**: 30 min  
**Status**: NOT STARTED

**Issue:**
- Export saves to: `ShelfBracket_v1/origin/ShelfBracket_v1.json`
- Expected: `ShelfBracket_v1/model.json`
- Then transform & validate look for `model.json` and fail

**Solution:**
1. [ ] Modify `export_fusion360_data.py` line 282-287
   - Remove `/origin` subdirectory creation
   - Save directly to `model_dir / "model.json"`
   - Update documentation in function comment
2. [ ] Update docstring to show correct output path
3. [ ] Test with example (verify it would produce correct structure)

**Files to change:**
- `export_fusion360_data.py` (lines 282-287)

---

### ⬜ 2. Standardize model.json Schema Across All Scripts
**Impact**: HIGH — Validation/transform/export disagree on format  
**Effort**: 2 hours  
**Status**: NOT STARTED

**Issue:**
- `validate_workflow.py` expects nested: `model.parameters`, `model.features`, `model.bodies`
- `transform_metadata.py` reads flat: top-level `parameters`, `features`
- `export_fusion360_data.py` creates flat structure
- Example `model.json` has flat structure

**Solution:**
1. [ ] Decide on ONE canonical structure (recommendation: flat/top-level)
   - Top-level: `parameters`, `features`, `components`, `sketches`, `timeline`
   - Nested: `export_metadata`, `model` (for summary info only)
2. [ ] Update `validate_workflow.py` ModelValidator.REQUIRED_FIELDS (lines 83-95)
   - Change to match actual structure
   - Add validation for top-level arrays
3. [ ] Update export script docstring to show correct structure
4. [ ] Add comment to all 3 scripts referencing the canonical schema

**Files to change:**
- `validate_workflow.py` (ModelValidator.REQUIRED_FIELDS)
- `export_fusion360_data.py` (docstring/comments)
- Add new file: `docs/model_json_schema.md` (documentation)

**Reference:** examples/model.json shows the correct structure to match against

---

### ⬜ 3. Add Questionnaire Validation Before Transform
**Impact**: HIGH — Silent failures on incomplete questionnaire  
**Effort**: 1 hour  
**Status**: NOT STARTED

**Issue:**
- Many questionnaire fields are optional (`required: false`)
- Transform accepts empty questionnaire gracefully
- Resulting metadata files are incomplete
- Users don't realize their questionnaire was incomplete

**Solution:**
1. [ ] Create validation function in `transform_metadata.py`
   ```python
   def validate_context_json(context_data) -> List[str]:
       """Return list of warnings/errors for incomplete context"""
   ```
   Check for:
   - [ ] `context_metadata.model_name` not empty
   - [ ] `purpose.purpose_primary` not empty
   - [ ] `design_intent.intent_critical_features` not empty
   - [ ] `materials.material_type` not empty (if any material fields filled)
   - [ ] All constraint fields empty OR all filled (don't mix)

2. [ ] Call validation in `main()` before `transformer.transform_all()`
3. [ ] Print warnings if incomplete, but allow proceeding with `--force` flag
4. [ ] Update docstring with new `--force` option

**Files to change:**
- `transform_metadata.py` (add validation function, update main())
- `docs/transform_metadata.md` (add note about completeness)

---

### ⬜ 4. Make Export Script Testable (Add Offline Mode)
**Impact**: MEDIUM — Can't verify export works without Fusion 360  
**Effort**: 1.5 hours  
**Status**: NOT STARTED

**Issue:**
- Export script only runs inside Fusion 360
- No way to test if export produces correct JSON
- Can't add to CI/CD pipeline
- Users can't verify their export worked before sending to transform

**Solution:**
1. [ ] Create test/standalone mode that generates synthetic model.json
2. [ ] Add command-line flag to export script: `--generate-test-data`
3. [ ] When flag set:
   - Don't require Fusion 360 API
   - Create synthetic model.json with sample parameters/features/sketches
   - Save to output directory
   - Verify output matches schema
4. [ ] Create helper function `generate_synthetic_model()` that creates realistic test data
5. [ ] Document in `docs/export_fusion360.md` how to test export locally

**Files to change:**
- `export_fusion360_data.py` (add test mode logic, synthetic generator)
- `docs/export_fusion360.md` (add "Testing without Fusion 360" section)

---

## P1: Major Gaps (Required Before Production Use)

These won't break workflows but make the project fragile and hard to maintain.

### ⬜ 5. Create JSON Schema Files
**Impact**: HIGH — No formal specification of data formats  
**Effort**: 3 hours  
**Status**: NOT STARTED

**Issue:**
- Users don't know required vs optional fields
- No automatic validation
- No clear spec for custom implementations

**Solution:**
Create 7 JSON Schema files in `schemas/` directory:

1. [ ] `schemas/model.json.schema`
   - Top-level: `export_metadata`, `parameters`, `features`, `components`, `sketches`, `timeline`
   - Define all field types, required fields, constraints
2. [ ] `schemas/context.json.schema`
   - Define questionnaire response structure
   - Mark optional sections
3. [ ] `schemas/metadata.json.schema`
   - Define output of transform_metadata.py
4. [ ] `schemas/parameters.json.schema`
   - Parameters for code generation
5. [ ] `schemas/constraints.json.schema`
   - Constraint specifications
6. [ ] `schemas/features.json.schema`
   - Feature timeline
7. [ ] `schemas/assembly.json.schema`
   - Component structure

Each schema should:
- [ ] Be valid JSON Schema Draft 7
- [ ] Have `$schema`, `title`, `description`, `type`, `properties`, `required`
- [ ] Include examples
- [ ] Link to documentation

2. [ ] Add schema validation to `validate_workflow.py`:
   ```python
   def validate_against_schema(json_file, schema_file):
       """Validate JSON against schema"""
   ```

3. [ ] Create `docs/data_format_specification.md` explaining all schemas

**Files to create:**
- `schemas/model.json.schema`
- `schemas/context.json.schema`
- `schemas/metadata.json.schema`
- `schemas/parameters.json.schema`
- `schemas/constraints.json.schema`
- `schemas/features.json.schema`
- `schemas/assembly.json.schema`
- `docs/data_format_specification.md`

**Files to update:**
- `validate_workflow.py` (add schema validation)

---

### ⬜ 6. Create Proper Code Generation Tool
**Impact**: HIGH — template_generator.py is not actually usable  
**Effort**: 4 hours  
**Status**: NOT STARTED

**Issue:**
- `template_generator.py` is a static reference, not a template
- Has placeholder names like `Param1`, `Param2`
- Users can't programmatically generate code from metadata
- Only option: ask AI to write from scratch (error-prone)

**Solution:**
Create new script `generate_generator.py` (code generator):
1. [ ] Takes 3 inputs: `parameters.json`, `constraints.json`, `features.json`
2. [ ] Outputs: `generate_mymodel.py` (working Python script)
3. [ ] Features:
   - [ ] Reads parameter names from parameters.json
   - [ ] Generates proper CLI arguments (kebab-case)
   - [ ] Generates validation code from constraints.json
   - [ ] Generates feature functions stubs from features.json
   - [ ] Generates main() with proper argparse setup
   - [ ] Generates docstrings with parameter specs

```python
def generate_generator_script(
    parameters_json: Dict,
    constraints_json: Dict,
    features_json: Dict,
    model_name: str,
    output_file: Path
) -> None:
    """Generate complete generate_mymodel.py from metadata"""
```

4. [ ] Integration:
   - [ ] Add to `transform_metadata.py` workflow as optional step
   - [ ] Or create standalone script that calls it
   - [ ] Add CLI: `python generate_generator.py examples/ --output examples/generate_shelfbracket_generated.py`

5. [ ] Update documentation:
   - [ ] Add section to README about code generation
   - [ ] Update docs/generator.md with tool info
   - [ ] Create docs/code_generation_automation.md

**Files to create:**
- `generate_generator.py` (new code generation tool)
- `docs/code_generation_automation.md`

**Files to update:**
- `readme.md` (add note about automation)
- `docs/generator.md`

---

### ⬜ 7. Add Comprehensive Unit Tests
**Impact**: HIGH — No way to verify code works after changes  
**Effort**: 4 hours  
**Status**: NOT STARTED

**Issue:**
- No unit tests for transform_metadata.py
- No tests for validate_workflow.py
- No tests for edge cases (partial questionnaire, invalid JSON, etc.)
- Can't guarantee code quality or catch regressions

**Solution:**
Create test suite with pytest:

1. [ ] Create `tests/` directory with structure:
   ```
   tests/
   ├── __init__.py
   ├── conftest.py               # Pytest fixtures
   ├── test_transform_metadata.py
   ├── test_validate_workflow.py
   ├── test_export_fusion360.py  # Mock Fusion API
   ├── fixtures/                 # Test data
   │   ├── minimal_model.json
   │   ├── complete_model.json
   │   ├── minimal_context.json
   │   ├── complete_context.json
   │   ├── invalid_*.json        # Edge cases
   └── test_schemas.py           # Schema validation tests
   ```

2. [ ] `test_transform_metadata.py`:
   - [ ] Test: minimal valid inputs → valid output
   - [ ] Test: complete inputs → complete output
   - [ ] Test: partial questionnaire → warning + partial metadata
   - [ ] Test: all parameter types (length, angle, etc.)
   - [ ] Test: derived parameters calculation
   - [ ] Test: constraint mapping to all 5 metadata files

3. [ ] `test_validate_workflow.py`:
   - [ ] Test: valid model.json passes
   - [ ] Test: missing required fields warns
   - [ ] Test: invalid JSON fails with clear error
   - [ ] Test: valid context.json passes
   - [ ] Test: partial context.json generates warnings

4. [ ] `test_export_fusion360.py`:
   - [ ] Mock Fusion 360 API
   - [ ] Test: export creates correct directory structure
   - [ ] Test: export creates valid JSON
   - [ ] Test: empty design fails validation
   - [ ] Test: design with 0 parameters generates warning

5. [ ] `test_schemas.py`:
   - [ ] Test: example model.json validates against schema
   - [ ] Test: example context.json validates against schema
   - [ ] Test: all generated metadata validate against schemas

6. [ ] Create `conftest.py` with fixtures:
   - [ ] minimal_model
   - [ ] complete_model
   - [ ] minimal_context
   - [ ] complete_context
   - [ ] temporary_output_dir

7. [ ] Add pytest.ini configuration
8. [ ] Create CI pipeline (GitHub Actions):
   - [ ] Run tests on push
   - [ ] Check code coverage (target: 80%+)

**Files to create:**
- `tests/` directory (entire suite)
- `tests/__init__.py`
- `tests/conftest.py`
- `tests/test_transform_metadata.py`
- `tests/test_validate_workflow.py`
- `tests/test_export_fusion360.py`
- `tests/test_schemas.py`
- `tests/fixtures/` (test data)
- `pytest.ini`
- `.github/workflows/tests.yml` (CI)

---

### ⬜ 8. Fix Code Quality Issues
**Impact**: MEDIUM — Code has antipatterns and poor error handling  
**Effort**: 1 hour  
**Status**: NOT STARTED

**Issue:**
- Bare `except:` clauses hide real errors
- Magic numbers without explanation
- Inconsistent type hints
- Poor error messages

**Solution:**
1. [ ] Fix bare exception handlers in `export_fusion360_data.py`:
   - Line 149: `except:` → `except Exception:`
   - Line 194: `except:` → `except AttributeError:`
   - Add logging for each exception
2. [ ] Add type hints to all functions:
   - [ ] `validate_workflow.py` ValidationReport methods
   - [ ] `export_fusion360_data.py` FusionExporter methods
3. [ ] Replace magic numbers with named constants:
   - [ ] `transform_metadata.py` line 149: `* 2` and `100`
   - [ ] Document where default values come from
4. [ ] Improve error messages:
   - [ ] Add context to each error
   - [ ] Suggest fixes when possible
   - [ ] Example: Instead of "File not found", say "File not found: model.json. Expected in: /path/to/model_dir/"

**Files to update:**
- `export_fusion360_data.py`
- `validate_workflow.py`
- `transform_metadata.py`

---

## P2: Nice-to-Have Improvements

These improve user experience but aren't blocking issues.

### ⬜ 9. Expand Troubleshooting Documentation
**Impact**: LOW — Reduces user frustration  
**Effort**: 1.5 hours

**Add to `readme.md` Troubleshooting section:**
1. [ ] "My export created `model_name/origin/` but transform looks for `model.json`"
2. [ ] "Transform says my questionnaire is incomplete"
3. [ ] "Generated code won't run—missing CadQuery"
4. [ ] "Generated model doesn't match original design"
5. [ ] "Validation passes but metadata looks empty"

For each, include:
- [ ] Root cause explanation
- [ ] How to fix it
- [ ] How to prevent it next time

**Files to update:**
- `readme.md` (expand Troubleshooting section)

---

### ⬜ 10. Create Developer API Documentation
**Impact**: LOW — Helps developers extend the tool  
**Effort**: 2 hours

**Create `docs/developer_guide.md` covering:**
1. [ ] Architecture overview
2. [ ] How to add new parameter types
3. [ ] How to add new constraint types
4. [ ] How to customize code generation
5. [ ] How to add new metadata file types
6. [ ] How to extend validation

**Files to create:**
- `docs/developer_guide.md`

---

### ⬜ 11. Add Dry-Run Mode
**Impact**: LOW — Helps testing without Fusion 360  
**Effort**: 1.5 hours

**Add to transform_metadata.py:**
1. [ ] `--dry-run` flag
2. [ ] Doesn't write files, just reports what would be created
3. [ ] Validates completeness
4. [ ] Shows file sizes/complexity
5. [ ] Reports warnings/errors without stopping

**Files to update:**
- `transform_metadata.py` (add dry-run mode)
- `docs/transform_metadata.md`

---

### ⬜ 12. Create Migration Guide
**Impact**: LOW — Handles version upgrades  
**Effort**: 1 hour

**Create `docs/migration.md` for:**
1. [ ] Schema version changes
2. [ ] How to upgrade old model.json to new format
3. [ ] How to upgrade old context.json to new format
4. [ ] Backwards compatibility policy

**Files to create:**
- `docs/migration.md`

---

## Implementation Order

### Phase 1: Critical Fixes (1 day)
1. Fix export directory structure (30 min)
2. Standardize model.json schema (2 hours)
3. Add questionnaire validation (1 hour)
4. Make export testable (1.5 hours)

**Result: Workflows no longer break**

### Phase 2: Robustness (2 days)
5. Create JSON schemas (3 hours)
6. Create code gen tool (4 hours)
7. Add unit tests (4 hours)
8. Fix code quality (1 hour)

**Result: Production-ready with validation and testing**

### Phase 3: Polish (1 day)
9. Expand troubleshooting (1.5 hours)
10. Developer API docs (2 hours)
11. Dry-run mode (1.5 hours)
12. Migration guide (1 hour)

**Result: Professional documentation and extensibility**

---

## Success Criteria

### Phase 1 Complete ✅
- [ ] Export saves to correct directory: `model_name/model.json`
- [ ] All scripts agree on model.json structure
- [ ] Transform validates questionnaire completeness
- [ ] Export works in offline mode for testing

### Phase 2 Complete ✅
- [ ] 7 JSON schema files exist and validate all examples
- [ ] Code generation tool creates working `generate_*.py` scripts
- [ ] All Python files have >80% test coverage
- [ ] No bare except clauses or magic numbers

### Phase 3 Complete ✅
- [ ] Troubleshooting section has 5+ real examples
- [ ] Developer guide covers extending each component
- [ ] Dry-run mode works on all scripts
- [ ] Migration guide documents version handling

### Overall ✅
- [ ] Code readiness: 90+/100
- [ ] All tests pass
- [ ] Documentation complete
- [ ] Ready for production use

---

## Dependencies & Blockers

**None.** All fixes are independent and can be implemented in parallel.

---

## Estimated Effort

| Phase | Tasks | Estimated Time | Complexity |
|-------|-------|-----------------|-----------|
| P0 | 4 fixes | 5 hours | Low-Medium |
| P1 | 4 improvements | 13 hours | Medium-High |
| P2 | 4 nice-to-haves | 6 hours | Low |
| **Total** | **12 tasks** | **24 hours** | **Medium** |

---

## Notes

- All changes should maintain backwards compatibility where possible
- Update documentation alongside code changes
- Each PR should include tests
- Run full test suite before merging
- Update CHANGELOG for each fix
