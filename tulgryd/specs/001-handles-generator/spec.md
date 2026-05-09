# Feature Specification: Parametric Handles Generator

**Feature Branch**: `001-handles-generator`  
**Created**: 2026-05-06  
**Status**: Draft  
**Input**: User description: "Parametric handles generator script for custom tool holder models"

## Clarifications

### Session 2026-05-06

- Q: What does "100% structural integrity" mean in practice? → A: Geometric validity (watertight, no self-intersections, export validation pass)
- Q: When user runs generator twice with same parameters to same output directory, should the script overwrite, confirm, error, or rename? → A: Overwrite with confirmation (ask user before replacing)
- Q: For CLI parameter handling, should script require both diameter and height, offer presets, or provide smart defaults? → A: Require both parameters (no defaults; explicit intent)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate custom handles with CLI parameters (Priority: P1)

User wants to generate a single handle model with custom grip diameter and height, specifying parameters via command line without editing configuration files.

**Why this priority**: Core MVP functionality—parametric generation is the entire feature purpose. Without this, the tool has no value.

**Independent Test**: Can be fully tested by running CLI with custom parameters, checking that output file is generated with correct geometry.

**Acceptance Scenarios**:

1. **Given** user has Python 3.8+ and CadQuery installed, **When** running `python generate.py --diameter 3.0 --height 2.5`, **Then** outputs `handle_d3.0_h2.5.stl` with correct geometry
2. **Given** user specifies metric dimensions, **When** running generator with valid numeric inputs, **Then** output reflects exactly those custom dimensions
3. **Given** user provides custom output directory, **When** running with `--output-dir /path`, **Then** file is created in specified directory
4. **Given** user omits required parameters, **When** running generator without `--diameter` or `--height`, **Then** exits with error message showing required usage

---

### User Story 2 - Export in multiple formats (Priority: P2)

User wants to export generated handles in both STL (for 3D printing) and STEP (for CAD refinement) without running separate commands.

**Why this priority**: Supports both 3D printing and design iteration workflows; increases tool utility without added complexity.

**Independent Test**: Can be fully tested by running generator with `--format both` and verifying both file types exist with matching geometry.

**Acceptance Scenarios**:

1. **Given** generator supports multiple formats, **When** running with `--format both`, **Then** outputs both `.stl` and `.step` files
2. **Given** user requests STEP format only, **When** running with `--format step`, **Then** outputs only `.step` file
3. **Given** handles geometry is identical regardless of format, **When** comparing output files, **Then** dimensions match across STL and STEP

---

### User Story 3 - Validate parameter inputs (Priority: P2)

User provides invalid diameter or height values (negative, zero, out-of-range) and expects meaningful error messages instead of cryptic failures.

**Why this priority**: Prevents garbage outputs and improves user experience. Enables self-service debugging without support questions.

**Independent Test**: Can be fully tested by providing invalid inputs and verifying error messages guide user to correct values.

**Acceptance Scenarios**:

1. **Given** user enters negative diameter, **When** generator validates inputs, **Then** returns clear error message indicating valid range
2. **Given** user provides zero height, **When** generator checks constraints, **Then** rejects with explanation that height must be positive
3. **Given** user provides non-numeric input, **When** CLI parser processes arguments, **Then** shows help with example valid usage
4. **Given** output file already exists, **When** user runs generator to same path, **Then** prompts "File exists, overwrite? [y/N]" and honors user choice

---

### User Story 4 - Generate assembly guide (Priority: P3)

User receives auto-generated README with handle specifications, usage notes, and assembly diagram alongside each model output.

**Why this priority**: Improves documentation and speeds up 3D printing workflow; lower priority than core generation but valuable for production use.

**Independent Test**: Can be fully tested by verifying README is created, contains handle dimensions, and includes usage instructions.

**Acceptance Scenarios**:

1. **Given** handles are generated, **When** script completes, **Then** auto-generates `handle_d{diameter}_h{height}_README.md` with handle specs
2. **Given** README is created, **When** user reads it, **Then** contains diameter, height, material recommendations, and printing tips
3. **Given** multiple handles are generated with same parameters, **When** README is created, **Then** filename reflects custom parameters (e.g., `handle_d2.6_h2.0_README.md`)

---

### Edge Cases

- What happens when diameter is less than 10.0mm or greater than 30.0mm (physical constraints)?
- Output file already exists in directory: script prompts "File exists, overwrite? [y/N]" and waits for user response
- What if output directory is not writable or doesn't exist?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Script MUST require `--diameter` parameter (mm) as floating point input; error if missing
- **FR-002**: Script MUST require `--height` parameter (mm) as floating point input; error if missing
- **FR-003**: Script MUST validate that diameter is positive and within printable range (≥10.0mm, ≤30.0mm)
- **FR-004**: Script MUST validate that height is positive and within structural limits (≥3.0mm, ≤30.0mm)
- **FR-005**: Script MUST generate 3D model respecting reference parameters as fixed derived constraints
- **FR-006**: Script MUST export to STL format with filenames encoding parameters (e.g., `handle_d2.6_h2.0.stl`)
- **FR-007**: Script MUST support `--format` option with choices: `stl`, `step`, `both`
- **FR-008**: Script MUST create output directory if it doesn't exist
- **FR-009**: Script MUST support `--output-dir` parameter to specify custom output location; directory is created if missing (mkdir -p behavior), but script errors if directory exists and is unwritable
- **FR-010**: Script MUST generate assembly guide README with handle specifications and usage guide (filename: `handle_d{diameter}_h{height}_README.md`, parallel to model file)
- **FR-011**: Script MUST provide clear error messages for invalid inputs with guidance on valid ranges
- **FR-012**: Script MUST support `--help` flag showing all options with examples
- **FR-013**: Script MUST expose only diameter and height as user parameters; all other dimensions locked to reference values
- **FR-014**: Script MUST prompt user for confirmation before overwriting existing files ("File exists, overwrite? [y/N]") with default behavior N (no overwrite); user may enter 'y' to proceed or 'N'/Enter to abort

### Key Entities *(include if feature involves data)*

- **Handle Model**: 3D geometry defined by diameter, height, and 23 reference parameters (locked). Attributes: grip surface, mounting interface, structural geometry
- **Generation Output**: STL/STEP file with metadata in filename. Relationships: created from single parameter set, paired with assembly guide

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can generate custom handles in under 2 seconds from CLI invocation
- **SC-002**: Generated models are 3D-printable without manual geometry correction (100% structural integrity = watertight, no self-intersections, export validation pass)
- **SC-003**: Parameter validation catches 100% of out-of-range inputs before attempting model generation
- **SC-004**: Output filename encoding supports parameter values with ±0.1mm precision without truncation
- **SC-005**: 95% of users can generate their first handle without consulting documentation (CLI is self-explanatory via `--help`)
- **SC-006**: Assembly guide is generated for 100% of runs (filename: `handle_d{d}_h{h}_README.md`) and contains all required sections: specifications table, print settings (PLA/PETG/TPU), assembly steps, troubleshooting (fit issues, layer adhesion, warping), and maintenance guidance

## Assumptions

- Python 3.8+ is available and CadQuery 2.4+ is installed in user's environment
- Both `--diameter` and `--height` parameters are required; no default values provided (explicit intent required)
- Reference parameters from `handles/origin/handles.json` remain fixed during MVP; user customization of reference params is out of scope
- Output formats (STL, STEP) are sufficient; OBJ/3MF added in future iterations if needed
- Diameter range 10.0–30.0mm covers all practical use cases; edge case values outside this range can be documented as unsupported
- Users have basic understanding of millimeter dimensions and 3D printing; detailed CAD knowledge not required
- Assembly guide template follows pattern from `tiles/` generator for consistency but tailored to handles context
- Filenames use simple encoding scheme (e.g., `handle_d2.6_h2.0`) rather than UUID; no collision detection needed for v1
- Users accept prompt confirmation for file overwrites; non-interactive workflows should handle this via script wrappers
