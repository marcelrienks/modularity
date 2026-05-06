# Research: Handles Generator Technical Decisions

**Date**: 2026-05-06  
**Feature**: Parametric Handles Generator (001-handles-generator)

## Research Tasks Completed

### 1. CadQuery Parametric Geometry Best Practices

**Question**: How to build parametric handle geometry in CadQuery while maintaining reference parameter constraints?

**Decision**: Use CadQuery's `Workplane` API with parameter-driven sketch constraints.
- Exposed params: diameter, height (user input)
- Locked params: 23 reference dimensions from handles.json (embedded in builder)
- Approach: Build base geometry from exposed params, then apply fixed offsets/radii/features from reference params
- Validation: CadQuery's STL/STEP exporters automatically validate geometry (watertight, self-intersection checks)

**Rationale**: CadQuery's constraint system ensures parametric integrity; export validation is built-in.

**Alternative Rejected**: OpenSCAD — lacks sophisticated constraint system; reference parameter management would be error-prone.

---

### 2. Structural Integrity Validation (SC-002)

**Question**: How to ensure "100% structural integrity = watertight, no self-intersections, export validation pass"?

**Decision**: Implement two-tier validation:
1. **Geometric validation**: CadQuery's `Shape.isValid()` + `isClosed()` for watertight/intersection checks
2. **Export validation**: Attempt STL/STEP write; catch serialization errors as malformed geometry

**Validation Sequence**:
```
Build geometry → Shape.isValid() + isClosed() → Export attempt → Verify file size > 0
```

**Rationale**: CadQuery validates during export; errors caught before user receives file.

---

### 3. File Overwrite Confirmation UI

**Question**: How to implement interactive prompt ("File exists, overwrite? [y/N]") in CLI?

**Decision**: Use Python's `input()` with explicit [y/N] prompt; default to 'N' on empty input.

**Pattern**:
```python
if os.path.exists(filepath):
    response = input(f"File exists, overwrite? [y/N]: ").strip().lower()
    if response not in ('y', 'yes'):
        sys.exit("Aborted.")
```

**Rationale**: Simple, cross-platform, matches Unix conventions; doesn't require external deps (Click already imported).

---

### 4. Parameter Encoding in Filenames

**Question**: How to encode diameter/height with ±0.1mm precision in filenames without truncation or special characters?

**Decision**: Use format `handle_d{diameter}_h{height}.{ext}` with Python f-string formatting.

**Example**: 
- Input: `--diameter 2.6 --height 2.0` → `handle_d2.6_h2.0.stl`
- Input: `--diameter 3.0 --height 1.5` → `handle_d3.0_h1.5.stl`

**Handling Precision**:
- Accept float inputs; store as-provided (Python `float` maintains full precision)
- Format in filename: `f"handle_d{diameter}_h{height}"`  → preserves input precision
- Validation: Accept floats with arbitrary decimal places; no rounding before filename

**Rationale**: Simple, readable, no URL encoding needed; ±0.1mm precision maintained.

---

### 5. Reference Parameter Management

**Question**: How to embed 23 reference parameters (locked) in generator while allowing only 2 user params?

**Decision**: Store reference params as constants in `Parameters` class from `handles/origin/handles.json`.

**Structure**:
```python
class HandleParameters(Parameters):
    # User parameters (CLI input)
    diameter: float  # mm
    height: float    # mm
    
    # Reference parameters (locked, from handles.json)
    d165 = 0.3        # mm
    d144 = 0.6        # mm
    d176 = 2.6        # mm
    # ... 20 more reference params
```

**Rationale**: Separation of concerns; reference params never exposed to CLI; easy to update from future exports.

---

### 6. Assembly Guide Generation

**Question**: Should assembly guide be generated for every run, or only on first run per parameters?

**Decision**: Generate for every run; overwrite with same naming scheme as 3D model.

**Naming**: `handle_d{diameter}_h{height}_README.md` (parallel to model filename)

**Content**:
- Handle specifications (diameter, height, material, layer count)
- Grid/hole information (inherited from tiles context)
- 3D printer settings recommendations (default: PLA, 0.2mm layer height, supports if needed)
- Assembly/usage instructions
- Troubleshooting (common print failures + fixes)

**Rationale**: Documentation always fresh; filename parallelism aids discoverability.

---

### 7. Testing Strategy

**Question**: What testing approach ensures quality across geometry, I/O, and UX?

**Decision**: Three-tier testing strategy (pyramid model):

| Level | Scope | Tool | Example |
|-------|-------|------|---------|
| **Unit** | Parameter validation, file path building, math | pytest | `test_validate_diameter_range()` |
| **Integration** | Geometry building, STL/STEP export, file I/O | pytest + temp files | `test_build_and_export_stl()` |
| **Contract** | CLI interface, filename encoding, help text | pytest + subprocess | `test_cli_diameter_height_params()` |

**Rationale**: Unit tests fast; integration tests verify end-to-end; contract tests protect CLI stability.

---

## Key Decisions Summary

| Decision | Approach | Why |
|----------|----------|-----|
| Geometry Building | CadQuery + reference params | Parametric, validated, cross-platform |
| Integrity Validation | Shape.isValid() + export test | Comprehensive; catches geometry/serialization issues |
| File Overwrite | Interactive input() prompt | Simple, cross-platform, Unix-like behavior |
| Filename Encoding | `handle_d{d}_h{h}` format | Readable, precise, no special chars |
| Locked Params | Python constants class | Immutable, versionable, clear separation |
| Assembly Guide | Per-run generation | Fresh docs, parallel naming scheme |
| Testing | Unit + Integration + Contract | Comprehensive coverage, fast feedback |

---

## No NEEDS CLARIFICATION Items

All technical decisions clarified during spec phase. Ready for Phase 1 design.
