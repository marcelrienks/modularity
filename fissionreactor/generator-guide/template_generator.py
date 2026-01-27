"""
Generate {ModelName} models with parameter variations.

This script was auto-generated from a context package:
- Source: {ModelName}.f3d
- Generated: {Date}
- Parameters: N (X variable, Y fixed, Z derived)
- Features: N in sequence
- Context Package: example-context/ directory

Usage:
    python generate_{model_name}.py --help
    python generate_{model_name}.py --param1 value1 --output model.step
"""

from cadquery import Workplane, selectors
import argparse
import sys

# ============================================================================
# CONSTANTS (from parameters.json fixed parameters)
# ============================================================================

# Fixed parameters that cannot be varied
FIXED_DEPTH = 150  # Must match standard spacing
TAPER_FACTOR = 0.85  # Design-specific scaling

# ============================================================================
# PARAMETER VALIDATION
# ============================================================================

def validate_parameters(
    Param1=100,
    Param2=10,
    Param3=1.5,
    **kwargs
):
    """
    Validate all parameters before generation.
    
    Raises ValueError if any parameter violates constraints from constraints.json
    Severity levels: CRITICAL (fails generation), HIGH (warns), MEDIUM (logged)
    """
    
    # CRITICAL: Structural constraints that cause failure
    if not (10 <= Param1 <= 500):
        raise ValueError(
            f"Param1 must be 10-500mm, got {Param1}. "
            "This range is required for structural integrity."
        )
    
    if Param3 < 1.5:
        raise ValueError(
            "CRITICAL: Param3 < 1.5mm causes structural failure under load. "
            f"You specified {Param3}mm. Minimum is 1.5mm."
        )
    
    # HIGH: Manufacturing constraints
    if Param2 < 0.4:
        raise ValueError(
            f"Param2 must be >= 0.4mm (FDM printer resolution), got {Param2}mm"
        )
    
    # Check parameter relationships/dependencies
    if Param1 < 50 and Param2 > 20:
        raise ValueError(
            f"Incompatible parameters: Param1={Param1}mm is too small "
            f"for Param2={Param2}mm. Maximum Param2 for this Param1 is 15mm."
        )


def validate_model(model, Param1=100, Param2=10, **kwargs):
    """
    Validate generated model meets specifications.
    
    Post-generation checks to ensure model is valid.
    Raises ValueError if model doesn't meet specs.
    """
    
    # Check body count
    solids = model.val().solids()
    if len(solids) != 1:
        raise ValueError(
            f"Generated model has {len(solids)} bodies, expected 1. "
            "Model generation failed or produced unexpected result."
        )
    
    # Check volume is reasonable (from constraints.json QA checks)
    volume = model.val().volume()
    expected_min, expected_max = 10000, 500000  # mm³
    if not (expected_min <= volume <= expected_max):
        raise ValueError(
            f"Model volume {volume:.0f}mm³ outside expected range "
            f"({expected_min}-{expected_max}mm³). "
            "Features may have been skipped or dimensions are wrong."
        )
    
    # Check bounding box matches parameters
    bbox = model.val().boundingBox()
    if abs(bbox.xlen - Param1) > 2:  # Allow 2mm tolerance
        raise ValueError(
            f"Model width {bbox.xlen:.1f}mm doesn't match parameter {Param1}mm. "
            "This suggests parameter wasn't applied correctly."
        )
    
    # Check for critical features (e.g., holes, slots)
    # This would be customized per model
    faces = model.faces()
    if len(faces) < 8:
        raise ValueError(
            f"Model has only {len(faces)} faces, expected at least 8. "
            "Some features may be missing."
        )


# ============================================================================
# HELPER FUNCTIONS - SKETCHES & PATTERNS
# ============================================================================

def create_base_profile_sketch(width, depth, radius):
    """
    Create base rectangular profile with rounded corners.
    
    Args:
        width: Rectangle width (from Param1)
        depth: Rectangle depth (fixed parameter)
        radius: Corner radius (from Param3)
    
    Returns:
        Workplane with rectangle sketch
    """
    wp = Workplane("XY")
    
    # Start at corner, draw rectangle, apply corner radius
    wp = (wp
          .rect(width, depth)
          .corner(radius=radius))
    
    return wp


def create_mounting_holes_sketch(width, depth, hole_diameter):
    """
    Create 4 corner mounting holes.
    
    Hole positions: 10mm inset from all corners
    This is a design rule from model.json - DO NOT VARY
    
    Args:
        width: From BaseWidth parameter
        depth: From BaseDepth (fixed)
        hole_diameter: From MountingHoleDiameter parameter
    
    Returns:
        List of hole positions [(x1,y1), (x2,y2), ...]
    """
    inset = 10  # Fixed inset from design
    
    hole_positions = [
        (inset, inset),                    # Top-left
        (width - inset, inset),            # Top-right
        (inset, depth - inset),            # Bottom-left
        (width - inset, depth - inset),    # Bottom-right
    ]
    
    return hole_positions


def create_rib_pattern(width, depth, spacing):
    """
    Calculate rib pattern positions.
    
    Ribs spaced at width/4 intervals, extending 80% of width
    (design rule from model.json)
    
    Args:
        width: From BaseWidth
        depth: From BaseDepth
        spacing: Derived from BaseWidth * 0.25
    
    Returns:
        List of rib profile positions
    """
    max_width = width * 0.8  # Leave 20mm margin at edges
    rib_count = int(width / spacing)
    
    rib_positions = []
    for i in range(rib_count):
        x = (i + 1) * spacing
        if x <= max_width:
            rib_positions.append(x)
    
    return rib_positions


# ============================================================================
# FEATURE GENERATION (in timeline order from model.json)
# ============================================================================

def add_feature_1_base_extrude(wp, width, depth, thickness):
    """
    Feature 1: Base Extrude
    
    Creates base solid body by extruding the base profile.
    This is the foundational feature - all others build on it.
    
    Args:
        wp: Workplane with base profile sketch
        thickness: Extrusion distance (BaseThickness parameter)
    
    Returns:
        Workplane with extruded base
    """
    # Extrude the profile in the Z direction
    model = wp.extrude(thickness)
    
    return model


def add_feature_2_mounting_boss(model, width, boss_height):
    """
    Feature 2: Mounting Boss
    
    Raises boss on top face for mounting interface.
    Height is derived from BaseWidth * 0.15
    
    Args:
        boss_height: Derived from BaseWidth * 0.15
    
    Returns:
        Model with boss added
    """
    # Add cylindrical boss on top face
    model = (model
             .faces(">Z")
             .workplane()
             .circle(width * 0.1)
             .extrude(boss_height, combine="add"))
    
    return model


def add_feature_3_mounting_holes(model, width, depth, hole_diameter):
    """
    Feature 3: Mounting Holes
    
    Creates 4 corner mounting holes (through all).
    Positions are fixed by design rule, not parametric.
    
    Args:
        hole_diameter: From MountingHoleDiameter parameter
    
    Returns:
        Model with holes cut through
    """
    positions = create_mounting_holes_sketch(width, depth, hole_diameter)
    
    # Create through-hole pocket
    model = (model
             .faces(">Z")
             .workplane()
             .pushPoints(positions)
             .hole(hole_diameter))  # Through-hole
    
    return model


def add_feature_4_reinforcement_ribs(model, width, depth, rib_height, min_wall_thickness):
    """
    Feature 4: Reinforcement Ribs
    
    Adds internal ribs for structural stiffness.
    Rib positions scaled with width.
    
    Args:
        rib_height: From RibHeight parameter
        rib_spacing: Derived from BaseWidth * 0.25
    
    Returns:
        Model with ribs added
    """
    rib_spacing = width * 0.25
    rib_positions = create_rib_pattern(width, depth, rib_spacing)
    
    # Add ribs as pocket arrays (negative features)
    for x_pos in rib_positions:
        model = (model
                 .faces("<Z")  # Bottom face
                 .workplane()
                 .center(x_pos, depth/2)
                 .rect(3, depth * 0.8)
                 .pocket(rib_height))
    
    return model


def add_feature_5_corner_fillets(model, corner_radius, internal_radius=1.0):
    """
    Feature 5: Corner Fillets
    
    Applies fillets to all edges for stress relief and finish.
    
    Args:
        corner_radius: From CornerRadius parameter (external)
        internal_radius: Fixed at 1mm for internal edges (design rule)
    
    Returns:
        Model with fillets applied
    """
    # External edges: use parameter
    model = model.edges(">Z or <Z").fillet(corner_radius)
    
    # Internal edges: use fixed minimum (design constraint)
    model = model.edges().fillet(internal_radius)
    
    return model


# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================

def generate_model(
    Param1=100,
    Param2=10,
    Param3=1.5,
    Param4=None,
    **kwargs
):
    """
    Generate {ModelName} with given parameters.
    
    This function orchestrates the complete model generation:
    1. Validates parameters
    2. Calculates derived parameters
    3. Builds model features in timeline order
    4. Validates output
    5. Returns CadQuery model object
    
    Args:
        Param1: Primary dimension (100-500mm)
        Param2: Height dimension (variable)
        Param3: Radius/detail (1.5-3mm)
        Param4: Optional advanced parameter
    
    Returns:
        CadQuery Workplane object representing the 3D model
    
    Raises:
        ValueError: If parameters invalid or model generation fails
    """
    
    # Pre-generation validation (constraints.json)
    validate_parameters(Param1=Param1, Param2=Param2, Param3=Param3)
    
    # Calculate derived parameters (from parameters.json)
    PARAM_DERIVED_1 = Param1 * 0.15  # Example: boss height
    PARAM_DERIVED_2 = Param1 * 0.25  # Example: rib spacing
    
    # Fixed parameters (can't be overridden)
    PARAM_FIXED_DEPTH = 150
    PARAM_FIXED_TAPER = 0.85
    
    # Start with base profile sketch
    wp = Workplane("XY")
    
    # Build model in feature timeline order (from model.json)
    model = create_base_profile_sketch(Param1, PARAM_FIXED_DEPTH, Param3)
    model = add_feature_1_base_extrude(model, Param1, PARAM_FIXED_DEPTH, Param2)
    model = add_feature_2_mounting_boss(model, Param1, PARAM_DERIVED_1)
    model = add_feature_3_mounting_holes(model, Param1, PARAM_FIXED_DEPTH, Param3)
    model = add_feature_4_reinforcement_ribs(model, Param1, PARAM_FIXED_DEPTH, 5, Param3)
    model = add_feature_5_corner_fillets(model, Param3)
    
    # Post-generation validation (constraints.json QA checks)
    validate_model(model, Param1=Param1, Param2=Param2, Param3=Param3)
    
    return model


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Parse CLI arguments and generate model."""
    
    parser = argparse.ArgumentParser(
        description="Generate {ModelName} models with custom parameters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_{model_name}.py
  python generate_{model_name}.py --param1 100 --output small.step
  python generate_{model_name}.py --param1 300 --param2 12 --output large.step
  python generate_{model_name}.py --help
        """
    )
    
    # Variable parameters (from parameters.json - only these are user-configurable)
    parser.add_argument(
        "--param1", type=float, default=100,
        metavar="MM", help="Primary dimension (100-500mm, default: 100)"
    )
    parser.add_argument(
        "--param2", type=float, default=10,
        metavar="MM", help="Height dimension (default: 10)"
    )
    parser.add_argument(
        "--param3", type=float, default=1.5,
        metavar="MM", help="Corner radius (1.5-3mm, min 1.5 for FDM, default: 1.5)"
    )
    
    # Output options
    parser.add_argument(
        "--output", type=str, default="{model_name}.step",
        metavar="FILE", help="Output filename (STEP or STL format, default: {model_name}.step)"
    )
    parser.add_argument(
        "--format", type=str, choices=["step", "stl"],
        help="Output format (auto-detected from extension if not specified)"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Generate model
    try:
        model = generate_model(
            Param1=args.param1,
            Param2=args.param2,
            Param3=args.param3
        )
        
        # Determine output format
        if args.format:
            format_type = args.format.upper()
        elif args.output.endswith(".stl"):
            format_type = "STL"
        else:
            format_type = "STEP"
        
        # Export model
        model.save(args.output, mode=format_type)
        print(f"✓ Generated: {args.output} ({format_type})")
        print(f"  Parameters: Param1={args.param1}mm, Param2={args.param2}mm, Param3={args.param3}mm")
        return 0
        
    except ValueError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
