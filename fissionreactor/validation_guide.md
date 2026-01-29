# Validation Framework Guide

Comprehensive validation of the CAD parameterization workflow across all stages.

---

## Overview

The validation framework checks **4 major stages**:

1. **Design Export** (model.json) - Structure and required fields
2. **Questionnaire** (context.json) - Completeness and correctness  
3. **Metadata Transformation** - Generated file validity
4. **Code Generation** - Output format and usability

---

## Quick Start

### Run Validation
```bash
python validate_workflow.py example-context/
```

### Output
```
======================================================================
VALIDATION REPORT
======================================================================

✓ PASSED:
  ✓ model.json: Found 8 parameters
  ✓ model.json: Found 12 features
  ✓ context.json: All required sections present
  ✓ Metadata files: metadata.json - Unified model info and design intent
  ✓ Code generation: Generator template structure valid

⚠️  WARNINGS:
  ⚠️  model.json: Missing field: export_metadata.fusion360_version

======================================================================
RESULT: PASSED (5 checks)
======================================================================
```

---

## Stage 1: Design Export Validation (model.json)

### What Gets Validated

✓ File exists and contains valid JSON  
✓ Required structure:
- `export_metadata` - Export timestamp, Fusion 360 version
- `model` - Name, part count, parameters, features, bodies

### Key Metrics

- **Parameters**: Number of named parameters (should be > 0 for parameterized models)
- **Features**: Timeline of features (should match design sequence)
- **Bodies**: Component list (shows assembly complexity)

### Common Failures

| Issue | Cause | Fix |
|-------|-------|-----|
| No parameters found | Model not parameterized | Add named parameters to Fusion 360 design |
| Missing features | Export incomplete | Re-export with the add-in script |
| Invalid JSON | Export error | Check Fusion 360 add-in logs |

### Example Valid model.json Structure

```json
{
  "export_metadata": {
    "exported_date": "2024-01-15T10:30:00Z",
    "fusion360_version": "2.0.12345"
  },
  "model": {
    "name": "ShelfBracket_v1",
    "part_count": 1,
    "parameters": [
      {
        "name": "BaseWidth",
        "value": 100,
        "min": 50,
        "max": 200
      }
    ],
    "features": [
      {
        "name": "BaseSketch",
        "type": "sketch",
        "order": 1
      }
    ],
    "bodies": [
      {
        "name": "Body",
        "component_count": 1
      }
    ]
  }
}
```

---

## Stage 2: Questionnaire Validation (context.json)

### What Gets Validated

✓ File exists and contains valid JSON  
✓ All required sections present:
- `context_metadata` - Model name, questionnaire date
- `purpose` - Primary use, use case description
- `design_intent` - Critical features, design decisions
- `materials` - Primary material and specifications
- `metadata` - Version, author, documentation date

✓ Required fields in each section are non-empty

### Key Metrics

- **Completeness**: All 5 sections filled
- **Documentation**: Design intent clearly stated
- **Accuracy**: Material and purpose match export

### Common Failures

| Issue | Cause | Fix |
|-------|-------|-----|
| Missing section | Questionnaire incomplete | Run questionnaire again |
| Empty fields | Skipped questions | Fill in all required fields |
| Inconsistent model name | Copy-paste error | Verify matches model.json |

### Example Valid context.json Structure

```json
{
  "context_metadata": {
    "model_name": "ShelfBracket_v1",
    "questionnaire_date": "2024-01-15T11:00:00Z"
  },
  "purpose": {
    "purpose_primary": "Wall-mounted shelf bracket",
    "purpose_use_case": "Hold up to 25kg loads",
    "purpose_context": "Home and office environments"
  },
  "design_intent": {
    "intent_critical_features": "Load-bearing mounting points, structural reinforcement ribs",
    "intent_design_decisions": "60-degree angle for optimal load distribution"
  },
  "materials": {
    "material_primary": "Aluminum 6061-T6",
    "material_strength": "Tensile strength 310 MPa"
  },
  "metadata": {
    "meta_version": "1.0",
    "meta_author": "Design Team",
    "meta_date": "2024-01-15"
  }
}
```

---

## Stage 3: Metadata Transformation Validation

### What Gets Validated

✓ All 5 required metadata files generated:

| File | Purpose | Key Fields |
|------|---------|-----------|
| `metadata.json` | Model info + design intent | model_info, design_intent, materials |
| `parameters.json` | Code generation ready | parameters, parameter_groups, default_values |
| `constraints.json` | Design rules & validation | design_rules, parameter_constraints |
| `features.json` | Feature timeline | features, dependencies, construction_order |
| `assembly.json` | Component structure | assembly_structure, components |

✓ Each file contains required top-level keys  
✓ All files contain valid JSON

### Key Metrics

- **Parameter count**: Matches model.json
- **Feature count**: Matches model.json
- **Constraint coverage**: All parameters have constraints
- **Completeness**: All required sections present

### Common Failures

| Issue | Cause | Fix |
|-------|-------|-----|
| Missing metadata files | Transform didn't run | Run: `python transform_metadata.py model-dir/` |
| Invalid JSON | Transform error | Check error logs and fix inputs |
| Empty arrays | Model lacked data | Verify model.json is complete |

### Example Generated metadata.json

```json
{
  "metadata": {
    "version": "1.0",
    "schema_version": "1.0",
    "generated_date": "2024-01-15T11:05:00Z",
    "source_model": "ShelfBracket_v1",
    "source_export": "model.json",
    "source_context": "context.json"
  },
  "model_info": {
    "name": "ShelfBracket_v1",
    "version": "1.0",
    "author": "Design Team",
    "purpose": "Wall-mounted shelf bracket",
    "part_count": 1,
    "assembly_type": "single_component"
  },
  "design_intent": {
    "critical_features": [
      {
        "name": "Load-bearing points",
        "description": "Mounting holes for wall fasteners"
      }
    ],
    "design_decisions": [
      {
        "decision": "60-degree angle",
        "rationale": "Optimal load distribution"
      }
    ]
  }
}
```

---

## Stage 4: Code Generation Readiness

### What Gets Validated

✓ Generator template available and valid  
✓ Required structure in generator script:
- Class definitions for template logic
- Parameter handling functions
- Output generation methods

✓ Metadata files compatible with AI input

### Key Metrics

- **Template completeness**: All methods present
- **Compatibility**: Meets AI code generation API requirements
- **Documentation**: Generator functions documented

### Common Failures

| Issue | Cause | Fix |
|-------|-------|-----|
| Generator template missing | Not downloaded | Get from generator-guide/ |
| Invalid Python syntax | Corrupted template | Replace with original |
| Missing functions | Incomplete template | Regenerate from guide |

---

## Validation Workflow Integration

### Complete Workflow with Validation

```
Step 1: Design in Fusion 360
         ↓
Step 2: Export (5 min) → model.json
         ↓
    ✓ VALIDATE model.json
         ↓
Step 3: Questionnaire (15-30 min) → context.json
         ↓
    ✓ VALIDATE context.json
         ↓
Step 4: Transform (1 min, automated) → 5 metadata files
         ↓
    ✓ VALIDATE metadata files
         ↓
Step 5: Send to AI (2 min)
         ↓
    ✓ VALIDATE code generation output
         ↓
Step 6: Receive code → generate_yourmodel.py
         ↓
Step 7: Test & use (10 min) → STEP/STL files
```

### When to Validate

| Stage | When | Command | Severity |
|-------|------|---------|----------|
| After Export | Right after exporting | `python validate_workflow.py model-dir/` | Critical |
| After Questionnaire | After answering all questions | `python validate_workflow.py model-dir/` | Critical |
| After Transform | After running transform script | `python validate_workflow.py model-dir/` | High |
| Before AI | Before sending to AI system | `python validate_workflow.py model-dir/` | High |

---

## Interpreting Validation Results

### Result Categories

**✓ PASSED (Green)**
- Validation requirement met
- No action needed
- Continue to next stage

**⚠️ WARNINGS (Yellow)**
- Non-critical issue detected
- May affect output quality
- Recommend fixing before proceeding
- Examples: Missing optional field, incomplete documentation

**❌ ERRORS (Red)**
- Critical validation failure
- Must fix before proceeding
- Examples: Invalid JSON, missing required file, empty parameters

---

## Advanced Usage

### Validate Specific Stage

```bash
# Just validate export
python validate_workflow.py model-dir/

# Checks:
# - model.json structure
# - All required export fields
# - Parameter and feature counts
```

### Check Metadata Quality

After running transform:
```bash
# Validates transformation output
python validate_workflow.py model-dir/

# Checks:
# - All 5 metadata files exist
# - Valid JSON in each file
# - Required fields present
# - Data consistency across files
```

### Integration with CI/CD

Example GitHub Actions workflow:
```yaml
- name: Validate workflow
  run: python validate_workflow.py example-context/
  
- name: Fail on validation errors
  if: ${{ failure() }}
  run: echo "Workflow validation failed"
```

---

## Troubleshooting

### "model.json: File not found"
**Solution**: Make sure you're in the correct directory:
```bash
cd fissionreactor/
python validate_workflow.py example-context/
```

### "Invalid JSON" Error
**Solution**: Check file formatting:
```bash
python -m json.tool example-context/model.json > /dev/null
```

### "Missing required section"
**Solution**: Re-run questionnaire to completion:
```bash
python questionnaire_template.json  # Review structure
```

### Multiple Warnings
**Solution**: Non-critical but recommended to fix:
1. Review warning messages
2. Update relevant input files
3. Re-run validation
4. Continue if warnings are acceptable

---

## Validation API (for Integration)

```python
from validate_workflow import WorkflowValidator

# Run validation programmatically
validator = WorkflowValidator('example-context/')
success = validator.validate()

# Access detailed results
if validator.report.has_failures():
    for error in validator.report.errors:
        print(f"Error: {error}")

# Get counts
print(f"Passed: {len(validator.report.passed)}")
print(f"Warnings: {len(validator.report.warnings)}")
print(f"Errors: {len(validator.report.errors)}")
```

---

## Key Metrics Summary

After successful validation, your workflow metrics should show:

- **Model Complexity**: Parameters (8-15), Features (8-20)
- **Documentation Quality**: All 5 sections complete
- **Data Integrity**: Valid JSON in all files
- **Completeness**: All 5 metadata files present
- **Readiness**: Ready for AI code generation

---

## Next Steps

Once validation passes:

1. **Export to AI**: Send metadata files to Claude/GPT
2. **Code Generation**: Receive Python generator script
3. **Test Output**: Generate samples with different parameters
4. **Deploy**: Use generated code in your workflow

For code generation guidance, see: `generator-guide/generation-guide.md`
