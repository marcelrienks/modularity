# Tasks: Parametric Handles Generator

**Branch**: `001-handles-generator`  
**Input**: Design documents from `specs/001-handles-generator/`  
**Tech Stack**: Python 3.8+, CadQuery 2.4+, Click, Jinja2, pytest  
**Project Structure**: Single project (handles/ generator + tests/)

**User Stories** (from spec):
- **US1** (P1): Generate custom handles with CLI parameters — Core MVP
- **US2** (P2): Export in multiple formats (STL + STEP) — Adds CAD workflow
- **US3** (P2): Validate parameter inputs — Quality gate (foundational)
- **US4** (P3): Generate assembly guide — Documentation

**Testing**: 3-tier pyramid (unit + integration + contract tests)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and test framework

- [X] T001 Create project structure: `handles/core/`, `handles/tests/`
- [X] T002 Create `requirements.txt` with CadQuery, Click, Jinja2, pytest
- [X] T003 [P] Initialize pytest configuration (`pytest.ini` or `pyproject.toml`)
- [X] T004 [P] Copy `handles/origin/handles.json` to `handles/core/reference_params.json` for locked parameters

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core modules required by all user stories

**⚠️ CRITICAL**: No user story work begins until Phase 2 complete

- [X] T005 [P] Create `HandleParameters` class in `handles/core/parameters.py` with diameter, height user params + 23 reference params from handles.json
- [X] T006 [P] Create parameter validation logic in `handles/core/parameters.py`: range checks (diameter 1–10mm, height 0.5–5mm), type checks (float), error message generation
- [X] T007 [P] Create CadQuery geometry builder skeleton in `handles/core/builder.py` (Shape building, geometry validation stub)
- [X] T008 [P] Create exporter skeleton in `handles/core/exporter.py` (export to STL/STEP, file validation stub)
- [X] T009 [P] Create `handles/core/__init__.py` with module exports
- [X] T010 Create `handles/generate.py` main CLI entry point stub (Click app, basic --help)

**Checkpoint**: Foundation ready — US implementation can begin in parallel

---

## Phase 3: User Story 3 - Validate parameter inputs (Priority: P2) 🔒 Gating

**Goal**: Validate diameter/height inputs with clear error messages before geometry generation

**Independent Test**: Running generator with invalid parameters exits with clear error message

### Unit Tests for US3 (Test-First)

- [X] T011 [P] [US3] Write unit test for diameter range validation in `tests/unit/test_parameters.py`
- [X] T012 [P] [US3] Write unit test for height range validation in `tests/unit/test_parameters.py`
- [X] T013 [P] [US3] Write unit test for non-numeric input rejection in `tests/unit/test_parameters.py`
- [X] T014 [P] [US3] Write unit test for error message formatting in `tests/unit/test_parameters.py`

### Implementation for US3

- [X] T015 [US3] Implement `validate_diameter()` with range check (1.0–10.0mm) + error message in `handles/core/parameters.py`
- [X] T016 [US3] Implement `validate_height()` with range check (0.5–5.0mm) + error message in `handles/core/parameters.py`
- [X] T017 [US3] Implement `validate_all()` orchestrator calling both validators in `handles/core/parameters.py`
- [X] T018 [US3] Add validation call to CLI in `handles/generate.py` (exit on validation failure with error code 1)

**Checkpoint**: Parameter validation complete and tested. Ready for US1.

---

## Phase 4: User Story 1 - Generate custom handles with CLI parameters (Priority: P1) 🎯 MVP

**Goal**: User can run `python generate.py --diameter 2.6 --height 2.0` and get a valid handle_d2.6_h2.0.stl file

**Independent Test**: CLI generates output file with correct filename and valid STL geometry

### Contract Tests for US1 (Test-First)

- [X] T019 [P] [US1] Write contract test for CLI `--diameter` + `--height` options in `tests/contract/test_cli_params.py`
- [X] T020 [P] [US1] Write contract test for required parameters (error if missing) in `tests/contract/test_cli_params.py`
- [X] T020a [P] [US1] Write contract test for missing single required parameter: `python generate.py --diameter 2.5` (height missing) must exit with code 1 in `tests/contract/test_cli_params.py` [**CRITICAL: G1 Gap**]
- [X] T021 [P] [US1] Write contract test for `--help` flag output in `tests/contract/test_cli_help.py`

### Integration Tests for US1 (Test-First)

- [X] T022 [P] [US1] Write integration test for end-to-end generation (valid input → output file) in `tests/integration/test_generate.py`
- [X] T023 [P] [US1] Write integration test for geometry validation (Shape.isValid, isClosed) in `tests/integration/test_geometry.py`
- [X] T024 [P] [US1] Write integration test for STL export and file size validation in `tests/integration/test_export.py`
- [X] T024a [P] [US1] Write integration test for round-trip geometry validation: export to STL → re-import as Shape → validate watertight/closed in `tests/integration/test_export.py` [**CRITICAL: G2 Gap - validates SC-002**]

### Implementation for US1

- [X] T025 [P] [US1] Build CadQuery geometry from (diameter, height) parameters in `handles/core/builder.py`: base cylinders + mounting interface
- [X] T026 [P] [US1] Implement geometry validation (`Shape.isValid()`, `Shape.isClosed()`) in `handles/core/builder.py`
- [X] T027 [P] [US1] Implement STL export with file validation in `handles/core/exporter.py`
- [X] T028 [US1] Add Click CLI options `--diameter` and `--height` (required) in `handles/generate.py`
- [X] T029 [US1] Integrate parameter validation → geometry building → export pipeline in `handles/generate.py`
- [X] T030 [US1] Implement output directory creation (`--output-dir` default: `./output`) in `handles/generate.py`
- [X] T031 [US1] Implement output filename encoding: `handle_d{diameter}_h{height}.stl` in `handles/core/exporter.py`
- [X] T031a [P] [US1] Write contract test for filename precision encoding with edge values (d1.0, d10.0, d2.61) verifying ±0.1mm precision without truncation in `tests/contract/test_filename_encoding.py` [**MEDIUM: I1 Gap - validates SC-004**]
- [X] T032 [US1] Add exit codes: 0 (success), 1 (validation error), 2 (geometry error), 3 (export error) in `handles/generate.py`
- [X] T033 [US1] Add user-facing error messages (FR-011) in `handles/core/parameters.py` and `handles/core/exporter.py`

**Checkpoint**: US1 complete. Users can generate basic handles from CLI. MVP ready.

---

## Phase 5: User Story 2 - Export in multiple formats (Priority: P2)

**Goal**: User can specify `--format [stl|step|both]` to export geometry in multiple CAD formats

**Independent Test**: `--format step` produces valid STEP file; `--format both` produces both STL and STEP with matching geometry

### Contract Tests for US2 (Test-First)

- [X] T034 [P] [US2] Write contract test for `--format` option (stl, step, both) in `tests/contract/test_cli_format.py`
- [X] T035 [P] [US2] Write contract test for default format (stl) in `tests/contract/test_cli_format.py`

### Integration Tests for US2 (Test-First)

- [X] T036 [P] [US2] Write integration test for STEP export and file validation in `tests/integration/test_step_export.py`
- [X] T037 [P] [US2] Write integration test for STL and STEP geometry matching in `tests/integration/test_format_parity.py`

### Implementation for US2

- [X] T038 [P] [US2] Implement STEP export in `handles/core/exporter.py` (CadQuery `Shape.exportStep()`)
- [X] T039 [P] [US2] Add `--format` option to CLI (choices: stl, step, both; default: stl) in `handles/generate.py`
- [X] T040 [US2] Update export logic to handle multiple formats based on `--format` option in `handles/core/exporter.py`
- [X] T041 [US2] Implement filename consistency: `handle_d{d}_h{h}.stl` and `handle_d{d}_h{h}.step` in `handles/core/exporter.py`
- [X] T042 [US2] Add re-import validation for STEP files (parse validation) in `handles/core/exporter.py`

**Checkpoint**: US1 + US2 complete. Multiple export formats supported.

---

## Phase 6: User Story 4 - Generate assembly guide (Priority: P3)

**Goal**: Auto-generate `handle_d{d}_h{h}_README.md` with print settings, specifications, and usage instructions

**Independent Test**: Assembly guide markdown file created with correct filename and contains required sections (specs, print settings, troubleshooting)

### Unit Tests for US4 (Test-First)

- [X] T042a [P] [US4] Write unit test for Jinja2 assembly guide template rendering (mock context → rendered markdown) in `tests/unit/test_assembly_guide.py` [**MEDIUM: C1 Gap**]

### Integration Tests for US4 (Test-First)

- [X] T043 [P] [US4] Write integration test for assembly guide file creation in `tests/integration/test_assembly_guide.py`
- [X] T044 [P] [US4] Write integration test for README content validation (required sections) in `tests/integration/test_assembly_guide.py`

### Implementation for US4

- [X] T045 [P] [US4] Create assembly guide Jinja2 template in `handles/core/templates/assembly_guide.md.j2` (specs table, print settings, troubleshooting)
- [X] T046 [P] [US4] Create `AssemblyGuideGenerator` class in `handles/core/assembly_guide.py` (template rendering + file writing)
- [X] T047 [US4] Integrate assembly guide generation into CLI pipeline in `handles/generate.py` (called after export)
- [X] T048 [US4] Implement auto-calculated values (layer_count from height, timestamp) in `handles/core/assembly_guide.py`
- [X] T049 [US4] Test README renders correctly in GitHub (markdown validation) in integration tests

**Checkpoint**: US1 + US2 + US4 complete. Full MVP with documentation.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Production-ready refinements and edge cases

- [X] T050 [P] Implement file overwrite confirmation: `"File exists, overwrite? [y/N]"` prompt in `handles/generate.py` (uses Python `input()`); handle user abort (exit code 4)
- [X] T051 [P] Auto-create output directory if missing (mkdir -p behavior) in `handles/core/exporter.py`
- [X] T052 [P] Test output directory creation failure handling (permissions error) in `tests/integration/test_io.py`
- [X] T053 [P] Add `--version` flag to CLI showing generator version in `handles/generate.py`
- [X] T054 [P] Enhance `--help` output with usage examples per cli-contract.md in `handles/generate.py`
- [X] T055 [P] Add success message with file paths and generation time in `handles/generate.py`
- [X] T056 Create `handles/README.md` with quickstart, CLI examples, troubleshooting in `handles/README.md`
- [X] T057 Update root `readme.md` to mention handles generator in project overview
- [X] T058 Write end-to-end test: 3 different parameter sets → 3 model files + READMEs in `tests/integration/test_e2e.py`
- [X] T059 Performance test: generation completes in <2 seconds (SC-001) in `tests/integration/test_performance.py` [**NOTE: C3 clarification - scope includes geometry build + STL export file write; does not distinguish**]

**Checkpoint**: All features complete. Production ready.

---

## Phase 8: Final Validation & Documentation

**Purpose**: Verify all requirements met and documentation complete

- [X] T060 [P] Run full test suite (unit + integration + contract) and verify 100% pass rate
- [X] T061 [P] Validate all CLI exit codes (0, 1, 2, 3, 4) in manual testing script
- [X] T062 [P] Verify STL/STEP files are 3D-printable (spot check with slicer software)
- [X] T063 [P] Verify assembly guide content (print settings, troubleshooting, specs) matches contract
- [X] T064 [P] Test with multiple 3D printer profiles (if available)
- [X] T065 Create final project checklist in `handles/IMPLEMENTATION_CHECKLIST.md`
- [X] T066 Update `.specify/feature.json` with completion status
- [X] T067 Commit implementation completion: all tests passing, all requirements met

---

## Task Statistics

| Phase | Count | Status |
|-------|-------|--------|
| Setup | 4 | Infrastructure |
| Foundational | 6 | Blocking |
| US3 (Validation) | 8 | Gating |
| US1 (Core MVP) | 18 | Critical path (+3 gap fixes: T020a, T024a, T031a) |
| US2 (Multi-format) | 9 | Dependent on US1 |
| US4 (Assembly Guide) | 8 | Dependent on US1 (+1 gap fix: T042a) |
| Polish | 10 | Final refinements |
| Validation | 7 | Quality gates |
| **TOTAL** | **70** | **Fully scoped + gap remediation** |

---

## Parallelization Strategy

### Can Run in Parallel (No Dependencies)

**Setup Phase** (T001–T004):
- T001, T002, T003 independent
- T004 independent (separate config)

**Foundational Phase** (T005–T009):
- T005–T009 all independent (separate modules)
- T010 depends on T005–T009 (CLI requires modules)

**Within US3** (T011–T014):
- All test tasks parallel (unit tests)

**Within US1** (T025–T027):
- Geometry building and export can develop in parallel
- T028–T033 depend on T025–T027 (integration)

**Within US2** (T038–T039):
- STEP export independent of CLI option addition

### Dependency Chain (Critical Path)

```
Setup (T001–T004)
    ↓
Foundational (T005–T010)
    ↓
US3 Tests (T011–T014) + US3 Implementation (T015–T018)
    ↓
US1 Tests (T019–T024) + US1 Implementation (T025–T033) ← CRITICAL PATH
    ↓
US2 Tests (T034–T037) + US2 Implementation (T038–T042)
    ↓
US4 Tests (T043–T044) + US4 Implementation (T045–T049)
    ↓
Polish (T050–T059)
    ↓
Validation (T060–T066)
```

**Estimated duration with full parallelization**: 3–4 developer-days (vs. 5–6 sequential)

---

## Test Requirements

**Total tests written**: ~30 test functions across:
- Unit: 8 functions (parameter validation)
- Integration: 15 functions (generation, export, guide)
- Contract: 7 functions (CLI interface)

**Coverage goals**:
- Parameter validation: 100% (all edge cases)
- Geometry/export: 95%+ (all formats, error cases)
- CLI: 100% (all options, exit codes)
- Assembly guide: 90%+ (template rendering, content)

**Test execution**: `pytest tests/` (all), `pytest tests/unit/` (fast feedback)

---

## Success Criteria Mapping

| Criterion | Task(s) | Verification |
|-----------|---------|--------------|
| SC-001: <2s generation | T059 | Performance test |
| SC-002: Geometric validity | T023, T026, T042 | Shape.isValid() + export |
| SC-003: 100% input validation | T011–T018 | Unit + contract tests |
| SC-004: ±0.1mm filename precision | T031 | Filename encoding test |
| SC-005: 95% user self-sufficiency | T054 | Enhanced --help + quickstart |
| SC-006: 100% assembly guide coverage | T049, T063 | Template validation |

---

## Functional Requirements Mapping

| Requirement | Task(s) |
|-------------|---------|
| FR-001/002: Required --diameter/--height | T028, T034–T035 |
| FR-003/004: Validate ranges | T015–T016 |
| FR-005: Generate 3D model | T025–T027 |
| FR-006: STL export + filename | T027, T031 |
| FR-007: --format option | T039 |
| FR-008/009: Create output dir | T051 |
| FR-010: Assembly guide generation | T045–T048 |
| FR-011: Error messages | T033 |
| FR-012: --help flag | T054 |
| FR-013: Locked params | T005 |
| FR-014: Overwrite confirmation | T050, T050b |

---

## Implementation Notes

- **Test-First Approach**: All test tasks (T011–T024, T034–T044) must be written BEFORE implementation
- **Modular Design**: Each core module (parameters, builder, exporter, assembly_guide) independently testable
- **CLI-First**: generate.py orchestrates pipeline; logic in core modules
- **Contract-Driven**: CLI contract tested via contract tests (user-facing guarantees)
- **Iterative**: After US1 complete, US2 and US4 can proceed in parallel with US1 fixes
- **Ready for Tasks**: All blockers and dependencies identified. Ready for implementation.

