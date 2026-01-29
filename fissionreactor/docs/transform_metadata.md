# Transform Metadata

Convert `model.json` + `context.json` into 5 AI-ready metadata files.

## Overview

After exporting and completing the questionnaire, transform them into standardized metadata:

```
model.json + context.json  →  transform_metadata.py  →  5 metadata files
```

## Installation

No installation needed! Uses only Python standard library.

**Requirements:**
- Python 3.6+
- Both `model.json` and `context.json` in the same directory

## Usage

### Basic

```bash
python transform_metadata.py path/to/your/model/
```

Generates 5 files in the same directory.

### Output to Different Directory

```bash
python transform_metadata.py input_dir/ output_dir/
```

## Generated Files

| File | Purpose |
|------|---------|
| **metadata.json** | Unified model info + design intent |
| **parameters.json** | CLI arguments, validation, code generation |
| **constraints.json** | Design rules and validation limits |
| **features.json** | Feature sequence and dependencies |
| **assembly.json** | Component structure and fasteners |

Together these form an **AI-ready context package**.

## Example

```bash
python transform_metadata.py examples/
# Generates 5 new files in examples/
```

## What Gets Transformed

**From model.json:**
- Parameters (names, types, values)
- Features (timeline and types)
- Components (hierarchy)
- Sketches (geometry)

**From context.json:**
- Purpose and design intent
- Parameter relationships and ranges
- All constraints and validation rules
- Material and fabrication info
- Assembly instructions
- Planned variations

## Validation

Verify transformation succeeded:

```bash
# Check all files created
ls -la your_model_dir/metadata.json your_model_dir/parameters.json

# Verify JSON is valid
python3 -m json.tool your_model_dir/metadata.json > /dev/null && echo "✓ Valid"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "File not found: model.json" | Verify both model.json and context.json exist in directory |
| "Invalid JSON in model.json" | Check JSON syntax: `python3 -m json.tool model.json` |
| Generated metadata looks incomplete | Normal if questionnaire had empty fields; AI can work with partial data |

## Next Step

Send all 7 files (model.json + context.json + 5 metadata files) to AI for code generation.

See: `generator-guide_generation-guide.md`
