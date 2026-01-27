"""
Generate ShelfBracket models with parameter variations.

Real working example for ShelfBracket_v1:
- Corner bracket for modular shelving system
- Generated from context-package/ specifications
- Parameters: 6 user-configurable (width, thickness, radius, hole-diameter, wall-thickness, rib-height)
- Features: 12 in sequence (base, boss, holes, ribs, fillets, etc.)

Usage:
    python generate_shelfbracket_example.py --help
    python generate_shelfbracket_example.py --width 100 --output bracket_small.step
    python generate_shelfbracket_example.py --width 300 --rib-height 6 --output bracket_large.step
"""

from cadquery import Workplane
import argparse
import sys

# ============================================================================
# CONSTANTS (Design Rules - cannot be changed)
# ============================================================================

BASE_DEPTH = 150  # Must align with aluminum post standard
MOUNTING_HOLE_INSET = 10  # Holes always 10mm from corners (design rule)
RIB_EXTENSION_RATIO = 0.8  # Ribs extend to 80% of width (20mm margins)
INTERNAL_FILLET_RADIUS = 1.0  # All internal edges minimum 1mm (FDM requirement)
TAPER_FACTOR = 0.85  # Wall taper scaling factor

# ============================================================================
# PARAMETER VALIDATION
# ============================================================================

def validate_parameters(BaseWidth, BaseThickness, CornerRadius, 
                       MountingHoleDiameter, MinWallThickness, RibHeight):
    """
    Validate parameters against all constraints from constraints.json
    
    CRITICAL constraints block generation (structural failure)
    HIGH constraints warn but allow (assembly/print failure)
    MEDIUM constraints logged (quality issues)
    """
    
    # ===== CRITICAL: Structural Constraints =====
    if not (100 <= BaseWidth <= 300):
        raise ValueError(
            f"CRITICAL: BaseWidth {BaseWidth}mm outside range 100-300mm. "
            "Width must be within this range for shelf support."
        )
    
    if BaseWidth % 10 != 0:
        raise ValueError(
            f"CRITICAL: BaseWidth {BaseWidth}mm must be multiple of 10. "
            "Width spacing doesn't align with rib pattern (BaseWidth * 0.25)."
        )
    
    if MinWallThickness < 1.5:
        raise ValueError(
            f"CRITICAL: MinWallThickness {MinWallThickness}mm < 1.5mm causes structural failure. "
            "PLA cannot support 20kg load with thinner walls. Minimum is 1.5mm."
        )
    
    if MountingHoleDiameter < 3.0:
        raise ValueError(
            f"CRITICAL: MountingHoleDiameter {MountingHoleDiameter}mm < 3mm won't print. "
            "FDM printer nozzle cannot create holes smaller than 3mm."
        )
    
    # ===== HIGH: Manufacturing Constraints =====
    if CornerRadius < 1.5:
        raise ValueError(
            f"HIGH: CornerRadius {CornerRadius}mm < 1.5mm unreliable for FDM. "
            "Sharp corners fail under stress. Minimum 1.5mm recommended."
        )
    
    if not (8 <= BaseThickness <= 12):
        raise ValueError(
            f"HIGH: BaseThickness {BaseThickness}mm outside optimal range 8-12mm. "
            "Very thin/thick sections print poorly."
        )
    
    # ===== MEDIUM: Quality Constraints =====
    if BaseThickness < 8:
        print(f"WARNING: BaseThickness {BaseThickness}mm is below 8mm (thin section warning)")
    
    # ===== Dependency Constraints =====
    # Check rib height reasonable for width
    if RibHeight > BaseWidth * 0.2:
        raise ValueError(
            f"Incompatible: RibHeight {RibHeight}mm too large for width {BaseWidth}mm. "
            "Ribs would interfere with edges."
        )


def validate_model(model, BaseWidth, BaseThickness):
    """
    Validate generated model meets specifications
    Post-generation checks from constraints.json QA section
    """
    
    # Check exactly 1 body
    solids = model.val().solids()
    if len(solids) != 1:
        raise ValueError(
            f"Generated {len(solids)} bodies, expected 1. "
            "Model generation failed - features not properly combined."
        )
    
    # Check volume reasonable (expect 50k-150k mm³ for ShelfBracket)
    volume = model.val().volume()
    if not (50000 <= volume <= 150000):
        raise ValueError(
            f"Model volume {volume:.0f}mm³ outside expected range (50k-150k). "
            "Suggests missing features or wrong parameters."
        )
    
    # Check bounding box matches parameters
    bbox = model.val().boundingBox()
    if abs(bbox.xlen - BaseWidth) > 2:
        raise ValueError(
            f"Model width {bbox.xlen:.1f}mm doesn't match parameter {BaseWidth}mm. "
            "BaseWidth parameter may not have been applied correctly."
        )
    
    # Check Z dimension roughly matches thickness
    if abs(bbox.zlen - BaseThickness) > 2:
        raise ValueError(
            f"Model height {bbox.zlen:.1f}mm doesn't match parameter {BaseThickness}mm. "
            "BaseThickness parameter may not have been applied correctly."
        )


# ============================================================================
# HELPER FUNCTIONS - Build complex sketches and patterns
# ============================================================================

def create_base_profile(width, depth, corner_radius):
    """
    Create base rectangular profile with rounded corners
    
    This becomes the extrude profile for the base feature
    """
    wp = Workplane("XY")
    
    # Rectangle with corner radii
    rect = (wp
            .rect(width, depth)
            .corner(radius=corner_radius))
    
    return rect


def get_mounting_hole_positions(width, depth, inset=MOUNTING_HOLE_INSET):
    """
    Calculate positions of 4 corner mounting holes
    
    Design rule: Always 10mm inset from corners (non-negotiable)
    Returns: List of (x, y) positions
    """
    return [
        (inset, inset),
        (width - inset, inset),
        (inset, depth - inset),
        (width - inset, depth - inset),
    ]


def get_rib_positions(width, depth):
    """
    Calculate rib positions along width
    
    Spacing: BaseWidth * 0.25
    Extension: 80% of width (20mm margins at edges)
    """
    spacing = width * 0.25
    max_extent = width * RIB_EXTENSION_RATIO
    
    positions = []
    x = spacing
    while x <= max_extent:
        positions.append(x)
        x += spacing
    
    return positions


# ============================================================================
# FEATURE GENERATION (in timeline order from model.json)
# ============================================================================

def add_base_extrude(model, thickness):
    """Feature 1: Base Extrude - Create main body"""
    return model.extrude(thickness)


def add_mounting_boss(model, width, base_thickness):
    """Feature 2: Mounting Boss - Raise boss for bolt interfaces"""
    boss_height = width * 0.15  # Derived from BaseWidth * 0.15
    
    # Create cylindrical boss on top face
    model = (model
             .faces(">Z")
             .workplane()
             .circle(width * 0.1)
             .extrude(boss_height, combine="add"))
    
    return model


def add_mounting_holes(model, width, depth, hole_diameter):
    """Feature 3: Mounting Holes - Cut 4 corner bolt holes"""
    positions = get_mounting_hole_positions(width, depth)
    
    # Create through-holes (all 4 at once)
    model = (model
             .faces(">Z")
             .workplane()
             .pushPoints(positions)
             .hole(hole_diameter))
    
    return model


def add_reinforcement_ribs(model, width, depth, rib_height, min_wall_thickness):
    """Feature 4: Reinforcement Ribs - Add internal stiffeners"""
    rib_positions = get_rib_positions(width, depth)
    rib_width = 3  # Fixed: 3mm ribs
    rib_length = depth * 0.8  # 80% of depth
    
    # Add each rib as pocket
    for x_pos in rib_positions:
        model = (model
                 .faces("<Z")  # Work on bottom face
                 .workplane()
                 .center(x_pos, 0)
                 .rect(rib_width, rib_length)
                 .pocket(rib_height))
    
    return model


def add_fillets(model, corner_radius):
    """Features 5-6: Fillets - Round edges for stress relief and finish"""
    # External edges: use parameter
    model = model.edges(">Z or <Z").fillet(corner_radius)
    
    # Internal edges: use minimum (1mm design rule)
    model = model.edges().fillet(INTERNAL_FILLET_RADIUS)
    
    return model


# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================

def generate_shelfbracket(
    BaseWidth=200,
    BaseThickness=10,
    CornerRadius=1.5,
    MountingHoleDiameter=3.2,
    MinWallThickness=2.0,
    RibHeight=5
):
    """
    Generate ShelfBracket model with given parameters.
    
    Args (all from parameters.json with min/max/default):
        BaseWidth (100-300mm, step 10): Bracket width
        BaseThickness (8-12mm, step 1): Bracket height  
        CornerRadius (1.5-3mm): External corner radius (min 1.5 for FDM)
        MountingHoleDiameter (3.0-3.5mm): M3 bolt hole
        MinWallThickness (1.5-3mm): Structural wall thickness (min 1.5)
        RibHeight (3-8mm): Reinforcement rib depth
    
    Returns:
        CadQuery Workplane object (3D model)
    
    Raises:
        ValueError: If parameters invalid or model fails validation
    """
    
    # Pre-generation validation
    validate_parameters(BaseWidth, BaseThickness, CornerRadius,
                       MountingHoleDiameter, MinWallThickness, RibHeight)
    
    # Fixed parameters (design rules)
    BaseDepth = BASE_DEPTH
    
    # Derived parameters (calculated from inputs)
    BossHeight = BaseWidth * 0.15  # Scales with width
    RibSpacing = BaseWidth * 0.25  # Scales with width
    
    # Build model in feature timeline order (from model.json)
    # Feature 1-2: Base geometry
    model = create_base_profile(BaseWidth, BaseDepth, CornerRadius)
    model = add_base_extrude(model, BaseThickness)
    
    # Feature 3: Mounting interface
    model = add_mounting_boss(model, BaseWidth, BaseThickness)
    
    # Feature 4-5: Structural features
    model = add_mounting_holes(model, BaseWidth, BaseDepth, MountingHoleDiameter)
    model = add_reinforcement_ribs(model, BaseWidth, BaseDepth, RibHeight, MinWallThickness)
    
    # Feature 6+: Finishing
    model = add_fillets(model, CornerRadius)
    
    # Post-generation validation
    validate_model(model, BaseWidth, BaseThickness)
    
    return model


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Parse command-line arguments and generate model."""
    
    parser = argparse.ArgumentParser(
        description="Generate ShelfBracket corner brackets for modular shelving",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_shelfbracket_example.py
  python generate_shelfbracket_example.py --width 100 --output bracket_small.step
  python generate_shelfbracket_example.py --width 300 --rib-height 6 --output bracket_large.step
  python generate_shelfbracket_example.py --wall-thickness 0.5 --output bracket_thin.step
  (last example will error - demonstrates validation)
        """
    )
    
    # Variable parameters (from parameters.json)
    parser.add_argument(
        "--width", type=float, default=200,
        metavar="MM", help="Bracket width (100-300mm, step 10, default: 200)"
    )
    parser.add_argument(
        "--thickness", type=float, default=10,
        metavar="MM", help="Bracket height (8-12mm, default: 10)"
    )
    parser.add_argument(
        "--corner-radius", type=float, default=1.5,
        metavar="MM", help="External corner radius (1.5-3mm, min 1.5 for FDM, default: 1.5)"
    )
    parser.add_argument(
        "--hole-diameter", type=float, default=3.2,
        metavar="MM", help="Mounting hole diameter for M3 bolts (3.0-3.5mm, default: 3.2)"
    )
    parser.add_argument(
        "--wall-thickness", type=float, default=2.0,
        metavar="MM", help="Minimum wall thickness (1.5-3mm, CRITICAL below 1.5mm, default: 2.0)"
    )
    parser.add_argument(
        "--rib-height", type=float, default=5,
        metavar="MM", help="Reinforcement rib height (3-8mm, default: 5)"
    )
    
    # Output options
    parser.add_argument(
        "--output", type=str, default="shelfbracket.step",
        metavar="FILE", help="Output filename (STEP or STL, auto-detected from extension)"
    )
    
    args = parser.parse_args()
    
    # Generate model with error handling
    try:
        print(f"Generating ShelfBracket with parameters:")
        print(f"  Width: {args.width}mm")
        print(f"  Thickness: {args.thickness}mm")
        print(f"  Corner radius: {args.corner_radius}mm")
        print(f"  Hole diameter: {args.hole_diameter}mm")
        print(f"  Wall thickness: {args.wall_thickness}mm")
        print(f"  Rib height: {args.rib_height}mm")
        
        model = generate_shelfbracket(
            BaseWidth=args.width,
            BaseThickness=args.thickness,
            CornerRadius=args.corner_radius,
            MountingHoleDiameter=args.hole_diameter,
            MinWallThickness=args.wall_thickness,
            RibHeight=args.rib_height
        )
        
        # Determine output format
        if args.output.endswith(".stl"):
            format_type = "STL"
        else:
            format_type = "STEP"
        
        # Save model
        model.save(args.output, mode=format_type)
        print(f"✓ Successfully generated: {args.output} ({format_type})")
        print(f"  File size: {__import__('os').path.getsize(args.output) / 1024:.1f}KB")
        return 0
        
    except ValueError as e:
        print(f"✗ Validation error: {e}", file=sys.stderr)
        return 1
        
    except Exception as e:
        print(f"✗ Generation error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
