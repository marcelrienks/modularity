# Validate Your Workflow

Check that all data is complete and correct before sending to AI.

## Quick Validation

```bash
python validate_workflow.py your_model_dir/
```

Output shows:
- ✓ PASSED checks (data is valid)
- ⚠️ WARNINGS (non-critical issues to consider)
- ❌ ERRORS (must fix before proceeding)

## What Gets Validated

### Stage 1: Design Export (model.json)
- ✓ File exists and contains valid JSON
- ✓ Has required fields (export_metadata, parameters, features, timeline)
- ✓ Contains at least one parameter and one feature

### Stage 2: Questionnaire (context.json)
- ✓ File exists and contains valid JSON
- ✓ All required sections present (purpose, design_intent, materials, etc.)
- ✓ Required fields in each section are non-empty

### Stage 3: Metadata Transformation
- ✓ All 5 metadata files generated and valid
- ✓ Each file contains required top-level keys
- ✓ Files are consistent with each other

### Stage 4: Code Generation Readiness
- ✓ Generator template exists and is valid
- ✓ Context package is complete and actionable

## When to Validate

| Stage | Command |
|-------|---------|
| After export | `python validate_workflow.py model_dir/` |
| After questionnaire | `python validate_workflow.py model_dir/` |
| After transformation | `python validate_workflow.py model_dir/` |
| Before sending to AI | `python validate_workflow.py model_dir/` |

## Example Output

```
✓ PASSED (5 checks):
  ✓ model.json: Found 8 parameters
  ✓ model.json: Found 12 features
  ✓ context.json: All required sections present
  ✓ Metadata files: All 5 files valid
  ✓ Code generation ready

⚠️ WARNINGS (1 warning):
  ⚠️ model.json: Missing fusion360_version

RESULT: PASSED (ready to send to AI)
```

## Interpreting Results

**✓ PASSED (Green)**
- Requirement met, continue to next step

**⚠️ WARNINGS (Yellow)**
- Non-critical issue, but recommended to address
- Safe to continue, but quality may suffer

**❌ ERRORS (Red)**
- Critical failure, must fix before proceeding
- Fix and re-run validation

## Troubleshooting

| Error | Fix |
|-------|-----|
| "model.json: File not found" | Verify file exists in correct directory |
| "Invalid JSON" | Check file syntax: `python3 -m json.tool file.json` |
| "Missing required section" | Complete questionnaire fully |

## Next Step

Once validation passes, send all 7 files to AI.

See: `generator-guide_generation-guide.md`
