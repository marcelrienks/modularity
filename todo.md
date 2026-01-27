# TODO - Modularity Project

## Fusion360Export - Completion & Enhancement

### Goal
Create a fully functional, AI-enabled workflow that converts hand-designed Fusion 360 models into parameterized Python generators.

**End State:** User exports model → AI gathers context via questionnaire → Metadata standardized → AI generates parameterized script that reproduces the original model

---

## Tasks

### 1. User Context Questionnaire Template
- [ ] Design questionnaire template for model export
  - Model purpose/use case
  - Key dimensions and parameters
  - Design constraints and tolerances
  - Material/print considerations
  - Assembly instructions needed?
  - Variations/configurations planned?
  - Any special features or non-obvious design decisions
- [ ] Integrate questionnaire into Add-In workflow
  - Display after user selects output directory
  - Save responses as JSON alongside export data
  - Use template structure for consistency

### 2. Standardized Metadata & File Types
- [ ] Define standard metadata schema
  - Model metadata (name, version, purpose, author)
  - Parameters (all user parameters with ranges/defaults)
  - Constraints (tolerances, limits, dependencies)
  - Features (construction sequence, critical features)
  - Materials (print materials, durability notes)
  - Assembly info (part count, assembly difficulty, instructions)
- [ ] Create standard file output structure
  - `model.json` - Design data export (already exists)
  - `context.json` - User questionnaire responses (NEW)
  - `metadata.json` - Standardized metadata (NEW)
  - `parameters.json` - Formatted parameters for code generation (NEW)
  - `constraints.json` - Design constraints and limits (NEW)
- [ ] Document format specifications for each file
- [ ] Create validation schema for metadata completeness

### 3. AI-Ready Context Package
- [ ] Create template/example of complete context package
  - Real example from exported model
  - Show all standard files populated
  - Include documentation reference
- [ ] Document what AI needs to see in context package
- [ ] Define success criteria for "AI-ready" export

### 4. Parameterized Script Generation Guide
- [ ] Document the code generation workflow
  - Input: Complete context package (all standard files)
  - Output: Parameterized Python generator script
  - Success: Generated script produces identical model with parameter variations
- [ ] Create template for parameterized generator structure
- [ ] Define naming conventions for generated scripts
- [ ] Examples of CadQuery-based generators

### 5. Integration & Workflow
- [ ] Create step-by-step workflow documentation
  1. User exports model from Fusion 360 (Add-In)
  2. Add-In displays questionnaire → saves context.json
  3. Add-In exports design data → model.json
  4. Generate standardized metadata files
  5. Create context package
  6. User feeds context package to AI (Claude/ChatGPT/etc)
  7. AI generates parameterized script
  8. Validate generated script produces equivalent model
- [ ] Create example workflow walkthrough
- [ ] Create troubleshooting guide

---

## Dependencies

- Fusion360Export Add-In (exists)
- CadQuery library knowledge
- AI integration documentation
- Parameter handling patterns

## Success Criteria

- ✓ Questionnaire captures all necessary context
- ✓ Metadata files are complete and standardized
- ✓ AI can use context package to generate working scripts
- ✓ Generated scripts produce models matching originals
- ✓ Process is documented and repeatable
- ✓ Example end-to-end workflow exists

## Notes

- Focus on making AI's job easier by providing structured, complete context
- Standardization is key—consistent file formats and metadata enable reliable code generation
- This is an iterative process; first export may need refinement based on generation results
