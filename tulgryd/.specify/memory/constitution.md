# tulgryd Constitution

Governing principles for the parametric design generator system. This constitution ensures quality, modularity, and maintainability across all features and components.

## Repository Model

tulgryd is a **collection of independent parametric model generator tools**. Each tool:
- Lives in its own top-level directory (e.g., `tiles/`, `handles/`)
- Has its own CLI entry point (`generate.py`)
- Has its own `README.md` and documentation
- Is used entirely independently — no global entry point or shared API exists
- May have its own dependencies beyond the shared baseline

**New tools** follow the standards in this constitution. The `handles/` tool is the reference implementation for new-style development. **Existing tools** (e.g., `tiles/`) follow older conventions and will be migrated when touched — no proactive migration required.

## Core Principles

### I. Spec-Driven Design

Every feature begins with a specification document (spec.md) that MUST define user scenarios, acceptance criteria, and non-negotiable constraints BEFORE any code is written.

**Non-Negotiable Rules:**
- Feature specs must include user stories with acceptance scenarios
- Specs must document parameter ranges, validation rules, and error conditions
- Implementation plans (plan.md) MUST reference the spec for traceability
- Legacy features (e.g., Tiles) are exempted; new features follow strictly

**Rationale:** Specifying intent upfront reduces rework, enables parallel task execution, and provides clear quality gates for review.

### II. CLI-First Interface

Every generator tool MUST expose its functionality via a command-line interface using Click framework.

**Non-Negotiable Rules:**
- CLI entry point: `generate.py` with required parameters as options (e.g., `--diameter`, `--height`)
- Output protocol: Success → stdout (file path), Errors → stderr with descriptive messages
- Support multiple output formats where applicable (STL, STEP, JSON metadata)
- CLI must have `--help` flag with clear usage examples

**Rationale:** CLI ensures reproducibility, scriptability, and cross-platform usability. Uniform interface reduces user friction.

### III. Parametric & Modular Design

All generators MUST accept user parameters for customization. Internal geometry rules (reference parameters) are locked and version-controlled.

**Non-Negotiable Rules:**
- Expose only user-facing parameters as CLI options; lock reference parameters in code or config
- Store reference parameters in versioned JSON files (e.g., `handles.json`) with semantic change tracking
- Generators MUST be independently testable and reusable as libraries (not CLI-only)
- Support both programmatic (library import) and command-line interfaces

**Rationale:** Parametric design enables rapid iteration. Locked reference parameters ensure consistent quality across customizations.

### IV. Quality & Validation

All generated outputs MUST pass geometric and format validation before export.

**Non-Negotiable Rules:**
- 3D models must pass validity checks: Shape.isValid() and isClosed() (CadQuery)
- Export format must be validated: file size > 0, geometry serializable without error
- Filenames must encode parameters for traceability (e.g., `handle_d2.6_h2.0.stl`)
- Exit codes: 0 (success), 1 (validation error), 2 (geometry error), 3 (export error)

**Rationale:** Prevents corrupted or invalid model export. User can trace output to input parameters.

### V. Backward Compatibility & Versioning

All releases follow Semantic Versioning (MAJOR.MINOR.PATCH). MAJOR version bumps are required for breaking changes.

**Non-Negotiable Rules:**
- Parameter additions/removals or format changes = MAJOR bump
- New optional parameters or output formats = MINOR bump
- Bug fixes and documentation = PATCH bump
- Breaking changes MUST include migration guide in release notes
- Reference parameter changes tracked in version history

**Rationale:** Users can depend on stable interfaces. Major changes are explicit and documented.

## Technology & Architecture

**Tech Stack:**
- Python 3.8+ (core language)
- CadQuery 2.4+ (parametric 3D modeling, recommended over OpenSCAD)
- Click (CLI framework)
- Jinja2 (assembly guide templates)
- pytest (testing framework, optional but recommended)

**Project Structure:**
- Each generator lives in a top-level folder: `tiles/`, `handles/`, etc.
- Each tool has its own `README.md` as primary documentation
- Core logic in `tool_name/core/` (parameters, builder, exporter, assembly_guide modules)
- Reference models and exported Fusion 360 JSON in `tool_name/origin/`
- Outputs in `tool_name/output/`
- Tests in `tool_name/tests/` (if present)
- No cross-tool shared library or global API

**Performance Goals:**
- Model generation must complete in <2 seconds
- Export (STL/STEP) must complete in <5 seconds total

## Development Workflow

**Feature Phases:**
1. **Phase 0 (Research):** Identify technical decisions, document in research.md
2. **Phase 1 (Design):** Create spec.md, plan.md, data-model.md, quickstart.md
3. **Phase 2 (Implementation):** Build components per tasks.md, validate against spec
4. **Phase 3 (Review):** Spec compliance check, manual testing, quality assurance
5. **Phase 4 (Release):** Version bump, release notes, tag commit

**Legacy Code Upgrade Path:**
- `tiles/` follows older conventions and pragmatic governance until actively touched
- `handles/` is the reference implementation for new-style development — all new tools follow its patterns
- When `tiles/` is refactored or extended, apply new standards incrementally
- No immediate migration required; avoid breaking existing functionality

**Testing Encouragement (Optional):**
- Unit tests: Recommended for parameter validation, builder logic
- Integration tests: Recommended for CLI → output workflows
- Contract tests: Recommended for validating spec acceptance criteria
- Test framework: pytest with fixtures for CadQuery geometry

## Governance

**Constitution as Source of Truth:**
- This constitution supersedes all other practices and conventions
- All PRs referencing "spec-first" or "quality standards" defer to this document
- Disputes on coding practices resolve to the applicable principle above

**Amendment Process:**
1. Propose change with rationale (why is current principle insufficient?)
2. Document change in constitution LAST_AMENDED_DATE field
3. Increment CONSTITUTION_VERSION per semantic versioning
4. All dependent templates updated: spec-template.md, plan-template.md, tasks-template.md
5. Update runtime guidance if principles affect development workflow

**Compliance Verification:**
- Feature PRs must cite which principles they satisfy
- Review checklist includes: Spec exists? CLI present? Reference params documented? Validation implemented?
- Breaking changes require CONSTITUTION_VERSION acknowledgment in commit

**Runtime Guidance:**
- Day-to-day development follows `.specify/` workflow (spec/plan/tasks)
- Project-specific conventions live in `/docs/` folder (if created)
- This constitution is immutable source; guidance documents evolve

---

**Version**: 1.0.0 | **Ratified**: 2026-05-07 | **Last Amended**: 2026-05-07
