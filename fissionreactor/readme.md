# fissionreactor - AI-Enabled CAD Parameterization Workflow

Transform hand-designed Fusion 360 models into parameterized Python code generators.

**Complete workflow:** Design CAD model → Export + questionnaire → AI generates Python code → Use with custom parameters

---

## 8-Step Workflow (End-to-End)

### Phase 1: Design & Preparation (Your CAD Model)

**Step 1: Prepare model in Fusion 360**
- Use named parameters (not hard-coded values)
- Organize features in logical construction order
- Document design intent and constraints
- Example: ShelfBracket_v1 in example-context/

**Example:**
```
Parameters: BaseWidth, BaseThickness, CornerRadius, MountingHoleDiameter, MinWallThickness, RibHeight
Features: Base Extrude → Mounting Boss → Mounting Holes → Reinforcement Ribs → Fillets
```

### Phase 2: Extract Design Data (fissionreactor Add-In)

**Step 2: Export design data from Fusion 360**
- Install: Copy `export_fusion360_data.py` to Fusion 360 Scripts directory
- Run: Tools > Add-ins > Scripts and Add-ins > Scripts tab > Right-click `export_fusion360_data` > Run
- Select output directory
- Output: `model.json` (all parameters, sketches, features, timeline)
- Details: See `export_fusion360_guide.md`

**Example output:**
```json
{
  "parameters": [
    {"name": "BaseWidth", "type": "length", "value": 200, "min": 100, "max": 300},
    ...
  ],
  "features": [
    {"index": 1, "name": "Base Extrude", "type": "extrude", ...},
    ...
  ]
}
```

**Step 3: Answer questionnaire**
- Complete all 28 questions in 8 sections (15-30 minutes)
- Questions cover: purpose, critical features, design decisions, materials, assembly, variations
- Reference: See `questionnaire_example.json` for completed example
- Guide: See `questionnaire_guide.md` for question explanations
- Output: `context.json` (design intent and user context)

**Example questions:**
- What is the primary purpose of this model?
- What are the critical features that MUST NOT vary?
- What load capacity or performance requirements?
- What materials and fabrication method?
- What variations are you planning?

### Phase 3: Generate AI-Ready Package (Metadata Transformation)

**Step 4: Generate standardized metadata files**
- Combine `model.json` (geometry) + `context.json` (intent)
- Generate 5 standardized files:
  - `metadata.json` - Unified spec combining model + context
  - `parameters.json` - Code generation specs (CLI args, validation rules)
  - `constraints.json` - Design rules (tolerances, minimums, dependencies)
  - `model.json` - Design export (already have)
  - `context.json` - Questionnaire responses (already have)
- Details: See `example-context/README.md` for complete example

**Step 5: Create context package**
- Package all 5 JSON files in `example-context/` directory structure
- Verify: Use success criteria checklist (see example-context/README.md)
- Result: AI-ready context package

**Validation checklist:**
```
☐ All 5 JSON files present and valid
☐ Parameter names consistent across all files
☐ All features listed in construction order
☐ All constraints with numerical thresholds (not vague)
☐ CLI interface fully specified (arguments, defaults, validation)
```

### Phase 4: AI Code Generation (LLM or Automated System)

**Step 6: Send context package to AI**
- Provide all 5 JSON files + generation guide
- Prompt AI: "Generate parameterized CadQuery Python script per this context package"
- Reference guides: `generator-guide/generation-guide.md` and `generator-guide/generate_shelfbracket_example.py`
- AI should generate complete, working script

**Example AI prompt:**
```
I'm providing a context package for ShelfBracket_v1. Generate a complete parameterized 
CadQuery Python script that:

1. Accepts all parameters from parameters.json as CLI arguments
2. Validates inputs against constraints.json rules (pre-generation)
3. Builds model following feature timeline from model.json
4. Validates output against QA checks (post-generation)
5. Exports to STEP/STL format

Use generator-guide/generate_shelfbracket_example.py as a reference for structure.
```

**Step 7: AI generates parameterized script**
- AI produces `generate_{model_name}.py`
- Script accepts CLI arguments for all parameters
- Script validates inputs (constraints.json)
- Script builds model (feature timeline from model.json)
- Script validates output
- Script exports to STEP or STL

**Generated script capabilities:**
```bash
python generate_shelfbracket.py --help
python generate_shelfbracket.py                          # Default parameters
python generate_shelfbracket.py --width 100 --output small.step
python generate_shelfbracket.py --width 300 --output large.step
python generate_shelfbracket.py --wall-thickness 0.5 --output invalid.step  # Errors with explanation
```

### Phase 5: Validation & Testing

**Step 8: Validate generated script produces equivalent model**
- Test with default parameters: Output matches original Fusion 360 model
- Test variations: Different parameters produce correctly-sized variants
- Test error handling: Invalid parameters rejected with helpful messages
- Test output formats: Both STEP and STL export correctly

**Validation checklist:**
```
✓ Script runs without errors: python generate_*.py --help
✓ Default parameters produce valid model
✓ Model opens in CAD software
✓ Dimensions match original (within ±0.5mm)
✓ All features present in correct order
✓ Parameter variations work: --width 100 produces different model than --width 300
✓ Invalid parameters rejected: --wall-thickness 0.5 shows CRITICAL error
```

---

## Quick Reference: What Goes Where

| Step | Input | Tool/Action | Output |
|------|-------|-----------|--------|
| 1 | Fusion 360 CAD | Organize parameters, features | Prepared model |
| 2 | Fusion 360 model | Run export_fusion360_data.py | `model.json` |
| 3 | Design specs | Answer questionnaire (15-30 min) | `context.json` |
| 4 | model.json + context.json | Metadata transformation | `metadata.json`, `parameters.json`, `constraints.json` |
| 5 | All 5 JSON files | Package together | Context package (example-context/) |
| 6 | Context package | Send to AI (Claude/GPT/etc) | Request for code generation |
| 7 | AI generates | CadQuery Python | `generate_{model_name}.py` |
| 8 | Generated script | Test + validate | Working generator with all parameters |

---

## Directory Structure

```
fissionreactor/
├── readme.md (this file)                  # Workflow overview
├── export_fusion360_data.py               # Fusion 360 Add-In script
├── export_fusion360_guide.md              # How to export data
├── questionnaire_template.json            # 28-question template
├── questionnaire_guide.md                 # How to answer questions
├── questionnaire_example.json             # Completed example
│
├── example-context/                       # Complete example package
│   ├── README.md                          # Package guide + success criteria
│   ├── model.json                         # Design export
│   ├── context.json                       # Questionnaire responses
│   ├── metadata.json                      # Unified metadata
│   ├── parameters.json                    # Code generation specs
│   └── constraints.json                   # Design rules & validation
│
└── generator-guide/                       # Code generation reference
    ├── readme.md                          # Generator overview
    ├── generation-guide.md                # 5-phase generation workflow
    ├── template_generator.py              # Reusable skeleton
    ├── generate_shelfbracket_example.py   # Real working example
    └── naming-conventions.md              # Naming standards
```

---

## Installation

### Fusion 360 Add-In Setup

```bash
# macOS
cp export_fusion360_data.py \
  ~/Library/Application\ Support/Autodesk/Fusion\ 360/API/Python/Samples/

# Windows
copy export_fusion360_data.py ^
  "%APPDATA%\Autodesk\Fusion 360\API\Python\Samples\"

# Linux
cp export_fusion360_data.py \
  ~/.Autodesk/Fusion\ 360/API/Python/Samples/
```

Restart Fusion 360. Script will appear in Tools > Add-ins > Scripts and Add-ins > Scripts tab.

### Python Dependencies (for generated scripts)

```bash
pip install cadquery
```

---

## Workflow Examples

### Example 1: ShelfBracket_v1
- **Input:** Corner bracket CAD model
- **Context package:** `example-context/`
- **Generated script:** `generator-guide/generate_shelfbracket_example.py`
- **Use:** `python generate_shelfbracket_example.py --width 200 --output bracket.step`

### Example 2: Create Your Own
1. Design model in Fusion 360 (use example-context/README.md for reference)
2. Export: Run `export_fusion360_data.py`
3. Questionnaire: Answer all 28 questions
4. Package: Create 5 JSON files using example-context/ as template
5. Validate: Use success criteria checklist
6. Generate: Send to AI with generator-guide reference
7. Test: Verify generated script works with your parameters

---

## Troubleshooting

### Export Fails

**Problem:** "Script not found in Scripts tab"
- **Solution:** Restart Fusion 360 after copying file to Scripts directory

**Problem:** "Cannot write to output directory"
- **Solution:** Ensure write permissions on selected directory, avoid cloud folders

### Questionnaire Issues

**Problem:** "Don't know how to answer a question"
- **Solution:** Leave blank or put "unknown". More detail = better code, but not required.

**Problem:** "Questions seem wrong for my model"
- **Solution:** Edit `questionnaire_template.json` to customize questions for your use case

### AI Code Generation

**Problem:** "Generated code doesn't run"
- **Solution:** Check: Python 3.8+, CadQuery installed, context package valid. See generator-guide/troubleshooting.md

**Problem:** "Generated models don't match original"
- **Solution:** May need more detail in context package. Compare to example-context/ completeness.

**Problem:** "Parameters not working as expected"
- **Solution:** Verify parameters.json validation rules match actual model behavior

### Generated Script Issues

**Problem:** "Script says 'wall thickness too thin' but I want thin walls"
- **Solution:** This is a CRITICAL constraint - thin walls cause structural failure. Use minimum 1.5mm.

**Problem:** "How do I modify the generated code?"
- **Solution:** Edit the Python script directly. Regenerate if context package changes.

---

## FAQ

**Q: Why do I need a questionnaire? Can't AI just look at the geometry?**
A: AI can see geometry but not design intent. The questionnaire captures "why" - load requirements, critical features, planned variations, material constraints. This makes generated code 10-100x better.

**Q: How long does the whole workflow take?**
A: Export (5 min) + Questionnaire (15-30 min) + Metadata transform (1 min) + AI generation (2-5 min) = **25-45 minutes total**.

**Q: Do I need to know Python?**
A: No. The generated script is usable without any coding knowledge. Just run it with CLI arguments.

**Q: Can I regenerate the script if I find a bug?**
A: Yes. Fix the context package (JSON files), resend to AI, get updated script. Or edit the Python script directly.

**Q: What if my model is really complex?**
A: fissionreactor works best for ~10-50 parameters and ~10-20 features. Very complex models may need custom handling.

**Q: Can I use this for non-FDM models?**
A: Yes - adapt questionnaire and constraints for your fabrication method (injection molding, CNC, etc.).

---

## References

- **Fusion 360 API:** https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/
- **CadQuery:** https://cadquery.readthedocs.io/
- **Context Package Spec:** See `example-context/README.md`
- **Code Generation Guide:** See `generator-guide/generation-guide.md`
- **Naming Conventions:** See `generator-guide/naming-conventions.md`

---

## Next Steps

1. **Try it:** Work through Steps 1-8 with a simple model
2. **Reference:** Use example-context/ as template for your model
3. **Generate:** Follow generator-guide/ for AI code generation
4. **Share:** Release both context package + generated script for reproducibility
