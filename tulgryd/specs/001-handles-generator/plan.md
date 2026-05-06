# Implementation Plan: Parametric Handles Generator

**Branch**: `001-handles-generator` | **Date**: 2026-05-06 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/001-handles-generator/spec.md`  
**Research**: [research.md](./research.md) — Technical decisions documented

## Summary

**Feature**: Parametric CLI script to generate custom tool holder handle models with user-specified grip diameter (1.0–10.0mm) and height (0.5–5.0mm). Geometry built in CadQuery respecting 23 locked reference parameters from design. Outputs STL/STEP files with parameter-encoded filenames + auto-generated assembly guides. Validates structural integrity (watertight, no self-intersections) before export. Confirms file overwrites interactively.

**Technical Approach**: 
- Build: CadQuery parametric geometry with user params + fixed reference params
- Validate: Shape.isValid() + isClosed() for watertight; export test for serialization
- Output: STL/STEP with filename encoding (e.g., `handle_d2.6_h2.0.stl`) + `ASSEMBLY_README.md`
- CLI: Click framework with required `--diameter` + `--height`; interactive overwrite prompt

## Technical Context

**Language/Version**: Python 3.8+  
**Primary Dependencies**: CadQuery 2.4+, Click (CLI), Jinja2 (assembly guide templates), NumPy  
**Storage**: Files (STL/STEP output to `./output/` or user-specified `--output-dir`)  
**Testing**: pytest (unit + integration + contract tests)  
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)  
**Project Type**: CLI tool + parametric geometry library  
**Performance Goals**: Generate and export handle in <2 seconds (SC-001)  
**Constraints**: Geometric validity (watertight, no self-intersections, export validation pass); ±0.1mm filename precision; 100% validation coverage for out-of-range inputs (SC-002, SC-003)  
**Scale/Scope**: Single generator, 2 exposed user parameters, 23 locked reference parameters, 2 export formats

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Status**: ✓ **PASS** — No constitution violations found

**Notes**: 
- Constitution template is unfilled (no active principles to enforce); feature spec already comprehensive
- Recommend constitution be ratified before next feature to establish project governance
- This feature follows implicit good practices: CLI-first interface, parametric design, test-first approach implicit in acceptance criteria

## Project Structure

### Documentation (this feature)

```text
specs/001-handles-generator/
├── plan.md              # This file (implementation plan)
├── spec.md              # Feature specification
├── research.md          # Phase 0: Technical decisions
├── data-model.md        # Phase 1: Entity definitions and relationships
├── quickstart.md        # Phase 1: Usage guide
├── contracts/
│   ├── cli-contract.md           # Phase 1: CLI interface spec
│   ├── file-output-contract.md   # Phase 1: Output file structure
│   └── assembly-guide-contract.md # Phase 1: README template spec
└── checklists/
    └── requirements.md           # Specification validation
```

### Source Code (repository root)

```text
handles/
├── generate.py                  # Main CLI entry point
├── core/                        # Core modules
│   ├── __init__.py
│   ├── parameters.py            # Parameter validation + HandleParameters class
│   ├── builder.py               # CadQuery geometry building
│   ├── exporter.py              # STL/STEP export with validation
│   └── assembly_guide.py        # Assembly README generation
├── origin/                      # Reference data
│   └── handles.json             # Design parameters export
├── output/                      # Generated models (runtime)
├── tests/                       # Test suite
│   ├── unit/                    # Parameter validation, math
│   ├── integration/             # Geometry building, export
│   └── contract/                # CLI interface, file I/O
└── requirements.txt             # Python dependencies
```

**Structure Decision**: Single project (handles/) with clear module separation:
- `parameters.py`: User input + reference param validation
- `builder.py`: CadQuery geometry construction
- `exporter.py`: Export with integrity validation
- `assembly_guide.py`: Documentation generation
- `tests/`: Three-tier testing (unit/integration/contract)

This mirrors the `tiles/` generator structure for consistency.

## Complexity Tracking

**Status**: No constitution violations. No complexity justification needed.

All design decisions follow established patterns (CadQuery from plan template; CLI from tiles example; test-first from spec acceptance criteria).

---

## Phase Completion Summary

**Phase 0 (Research)**: ✓ Complete  
Output: [research.md](./research.md) — All technical decisions resolved, no NEEDS CLARIFICATION items remain.

**Phase 1 (Design)**: ✓ Complete  
Outputs:
- [data-model.md](./data-model.md) — Entity definitions (Handle Model, Generation Output, Assembly Guide)
- [contracts/cli-contract.md](./contracts/cli-contract.md) — CLI interface spec (command signature, options, exit codes, error messages)
- [contracts/file-output-contract.md](./contracts/file-output-contract.md) — Output file structure (STL/STEP/README naming, validation rules)
- [contracts/assembly-guide-contract.md](./contracts/assembly-guide-contract.md) — Assembly guide Jinja2 template spec
- [quickstart.md](./quickstart.md) — User getting-started guide

**Constitution Check (Re-evaluated)**: ✓ Pass

---

## Ready for Next Phase

**Recommended next step**: `/speckit.tasks` to generate actionable, dependency-ordered tasks from this plan.

**Estimated task count**: 12–16 tasks covering:
1. Project scaffolding (core/ directory, test structure)
2. Parameter validation module
3. CadQuery geometry builder
4. Export + validation logic
5. Assembly guide templating
6. CLI interface (Click setup)
7. Unit tests (3–4 tasks)
8. Integration tests (2–3 tasks)
9. Contract tests (CLI verification)
10. Documentation + README update
