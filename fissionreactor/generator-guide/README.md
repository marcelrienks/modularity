# Parameterized Script Generation Guide

Task 4 documentation: How to transform a context package into working parameterized Python code.

## Contents

### 1. **GENERATION-GUIDE.md** (Main Guide - 19KB)

Comprehensive workflow for code generation from context packages.

**Sections:**
- Code Generation Workflow (5 phases)
- Phase 1: Parse context package
- Phase 2: Design script structure  
- Phase 3: Implement features (Feature mapping Fusion360 → CadQuery)
- Phase 4: Implement validation (pre and post-generation)
- Phase 5: Implement CLI interface
- Template structure (complete skeleton)
- Success criteria for generated scripts
- Common pitfalls and how to avoid them
- Workflow summary

**Key takeaway:** 5-phase process from JSON files to working Python script.

### 2. **template_generator.py** (Boilerplate Skeleton - 14KB)

Reusable template showing all necessary sections and patterns.

**Sections:**
- Imports and constants
- Parameter validation function
- Model validation function
- Helper functions (sketches, patterns)
- Feature generation functions (add_feature_*)
- Main generation function
- CLI interface with argparse
- Error handling

**How to use:**
1. Copy this template
2. Replace `{ModelName}`, `{model_name}`, parameter names
3. Implement helper functions for your model's sketches
4. Implement feature functions (one per feature from model.json)
5. Test against original model

### 3. **generate_shelfbracket_example.py** (Real Working Example - 14KB)

Complete, functional example for ShelfBracket_v1.

**Shows:**
- All 6 parameters properly validated
- All critical design rules enforced (1.5mm walls, 3mm holes, etc.)
- Feature implementation in CadQuery (extrude, pocket, fillet, patterns)
- Pre and post-generation validation
- CLI interface with all arguments
- Error messages with recovery suggestions

**How to use:**
1. Study this as reference for your own model
2. See how Fusion 360 features map to CadQuery code
3. Understand validation patterns (CRITICAL vs HIGH vs MEDIUM)
4. Copy structure for your model (replace feature implementations)

### 4. **NAMING-CONVENTIONS.md** (Reference - 11KB)

Standardized naming for consistency and maintainability.

**Covers:**
- Script names: `generate_{model_name}.py`
- Function names: `add_{Feature}()`, `create_{Sketch}()`, `validate_*()`
- Parameter names: PascalCase in Python, kebab-case in CLI
- Fixed constants: UPPERCASE_UNDERSCORE
- Local variables: lowercase_underscore
- Output filenames: `{ModelName}_{Variant}.{ext}`
- Comments and docstrings
- Consistency checklist

**Use this:** When writing your own generator to keep naming consistent.

---

## Quick Start: Generate Code from Context Package

### For AI Systems (Claude, GPT, etc.)

1. **Load context package:**
   ```
   Read all 5 JSON files from example-context/
   ```

2. **Read this guide:**
   ```
   Understand Phase 1-5 in GENERATION-GUIDE.md
   Read template_generator.py to understand structure
   ```

3. **Generate code:**
   - Use template_generator.py as starting structure
   - Implement features per model.json timeline
   - Add validation per constraints.json
   - Create CLI per parameters.json
   - Test with provided example

4. **Return script:**
   - Complete, working generate_{model_name}.py
   - Produces models matching original with default parameters
   - Handles all parameter variations correctly
   - Validates inputs and shows helpful errors

### For Humans Writing Scripts

1. **Start with template:**
   ```bash
   cp template_generator.py generate_mymodel.py
   ```

2. **Update constants:**
   - Replace fixed parameters from constraints.json
   - Add UPPERCASE constants for design rules

3. **Implement functions:**
   - Each feature from model.json gets an `add_*` function
   - Use CadQuery operations (`.extrude()`, `.pocket()`, `.fillet()`, etc.)
   - Build in feature timeline order

4. **Test:**
   ```bash
   python generate_mymodel.py --help
   python generate_mymodel.py  # Default parameters
   python generate_mymodel.py --param1 100 --output test.step
   ```

5. **Validate:**
   - Open output in CAD software
   - Compare to original model
   - Test boundary conditions (min/max parameters)
   - Test error cases (invalid parameters should error)

---

## Feature Mapping: Fusion 360 → CadQuery

Common Fusion 360 operations and their CadQuery equivalents:

| Fusion 360 | CadQuery | Example |
|-----------|---------|---------|
| Extrude | `.extrude()` | `wp.extrude(10)` |
| Pocket | `.pocket()` | `wp.pocket(5, combine="cut")` |
| Through Hole | `.hole()` | `wp.hole(3.2)` (auto through) |
| Fillet | `.fillet()` | `model.edges().fillet(1.5)` |
| Chamfer | `.chamfer()` | `model.edges().chamfer(0.5)` |
| Pattern (Linear) | `.rarray()` | `wp.rarray(spacing, count)` |
| Pattern (Polar) | `.polarArray()` | `wp.polarArray(count, angle)` |
| Sketch | `.sketch()` | `wp.sketch("name")` |
| Mirror | Mirror pattern + combine | Complex - use native CQ operations |
| Shell (Hollow) | Manual thickness | Use wall thickness in pocket depth |
| Draft (Taper) | `.rotateObject()` or geometry tricks | Model specific |

**Key CadQuery Methods:**
- `.extrude(length)` - Extrude sketch profile
- `.pocket(depth)` - Pocket (negative extrude)
- `.faces(selector)` - Select faces (">Z" = top, "<Z" = bottom, etc.)
- `.edges(selector)` - Select edges for fillet/chamfer
- `.fillet(radius)` - Round edges
- `.workplane(offset)` - Create new workplane for next operations
- `.hole(diameter)` - Create through-hole
- `.cboreHole()` - Counter-bore hole
- `.rarray(spacing, count)` - Rectangular array
- `.pushPoints(positions)` - Position workplane at multiple points

---

## Success Checklist

✅ **Before generating code:**
- [ ] Complete context package created (all 5 JSON files)
- [ ] All parameters documented with ranges
- [ ] All features listed in model.json in construction order
- [ ] All constraints documented in constraints.json
- [ ] CLI interface specified in parameters.json

✅ **After generating code:**
- [ ] Script runs without errors: `python generate_*.py --help`
- [ ] Default parameters produce valid model: `python generate_*.py`
- [ ] Model can open in CAD software
- [ ] Model dimensions match original (within 0.5mm)
- [ ] All features present in correct order
- [ ] Parameter variations work: `--param1 100` vs `--param1 300`
- [ ] Invalid parameters rejected with clear error: `--wall-thickness 0.5` errors

✅ **Quality checks:**
- [ ] Code is readable with docstrings
- [ ] No hardcoded values (all parameters used)
- [ ] Validation catches CRITICAL constraints (< 1.5mm walls)
- [ ] Validation catches HIGH constraints (< 1.5mm fillets)
- [ ] Post-generation validation confirms model correctness
- [ ] Error messages are helpful and actionable

---

## Common Questions

### Q: Where do I get the context package?

A: From Task 3 (example-context/) or create one:
1. Export Fusion 360 model with fissionreactor add-in
2. Answer questionnaire
3. Run metadata transformation
4. Use example-context/README.md to understand what goes in each file

### Q: How do I know what order features should be in?

A: From model.json features list - it's the Fusion 360 construction timeline.
Each feature depends on previous ones.

Example order:
1. Base extrude (creates solid)
2. Mounting boss (adds on top)
3. Mounting holes (cuts through)
4. Reinforcement ribs (adds internal structure)
5. Fillets (rounds all edges)

### Q: How much detail do I need in validation?

A: At minimum:
- Pre-generation: Check parameter ranges (from parameters.json)
- Post-generation: Check body count, volume, key dimensions

Better:
- Pre-generation: Also check parameter relationships/dependencies
- Post-generation: Also check critical features present (holes, surfaces)

Best (production):
- Pre-generation: All constraints from constraints.json
- Post-generation: QA checks from constraints.json QA section

### Q: Can I skip CadQuery and use something else?

A: Yes! These guides work for:
- CadQuery (primary, recommended)
- OpenSCAD (parameter substitution)
- FreeCAD Python API
- Other CAD Python libraries

The principles are the same - load parameters, build features in order, validate output.

### Q: Should I release generated code or regenerate it?

A: Best practice:
- ✅ Release context package (5 JSON files) + generation code
- ✅ Users can regenerate with different parameters
- ✅ Document version of generation code used

Not recommended:
- ❌ Release pre-generated models only (can't customize)
- ❌ Release generation code without context package (can't modify generation)

---

## Next Steps

### If you're an AI system:
1. Read GENERATION-GUIDE.md
2. Study template_generator.py and generate_shelfbracket_example.py
3. Generate code from context package
4. Return working script

### If you're writing code manually:
1. Read GENERATION-GUIDE.md phases
2. Copy template_generator.py as starting point
3. Reference generate_shelfbracket_example.py for patterns
4. Implement your model's features
5. Use NAMING-CONVENTIONS.md for consistency

### If you're integrating with automation:
1. Parse context package (model.json, parameters.json, constraints.json)
2. Validate consistency
3. Generate script using template structure
4. Test generated script
5. Return to user with validation report

---

## File References

All example files refer to ShelfBracket_v1:
- Context package: `../example-context/`
- Model specs: `../example-context/model.json`
- Parameters: `../example-context/parameters.json`
- Constraints: `../example-context/constraints.json`
- Design intent: `../example-context/context.json`

Use these as reference when creating your own context package and generator.
