#!/usr/bin/env python3
"""
Comprehensive STL Analysis Tool for SCAD Debugging

Complete STL file analysis combining dimensional and geometric inspection.
Analyzes both basic metrics (dimensions, volume) and advanced geometry
(shape, complexity, features, curvature) to fully understand STL models.

Features:
  - Dual format support (ASCII + binary STL)
  - Complete dimensional analysis
  - Geometric complexity measurement
  - Feature detection (pegs, curves, cavities, symmetry)
  - Surface analysis and properties
  - Volume and material estimation
  - Comprehensive comparison mode
  - Batch processing with detailed tables
  - Multiple output formats

Usage:
    python3 stl_tool.py model.stl                  # Full analysis
    python3 stl_tool.py --compare file1 file2     # Detailed comparison
    python3 stl_tool.py --dimensions model.stl    # Dimensions only
    python3 stl_tool.py --geometry model.stl      # Geometry only
    python3 stl_tool.py --features model.stl      # Features only
    python3 stl_tool.py --help                     # Show help

Examples:
    python3 stl_tool.py examples/toolgrid_ratchet_1-4inch.stl
    python3 stl_tool.py --compare generated.stl reference.stl
    python3 stl_tool.py --dimensions examples/*.stl
    python3 stl_tool.py --geometry --verbose model.stl
"""

import struct
import re
import sys
import os
from pathlib import Path
from typing import Dict, Tuple, List, Optional
from collections import defaultdict
import argparse
from dataclasses import dataclass


@dataclass
class STLFileInfo:
    """Container for complete STL analysis"""
    filepath: str
    filename: str
    format: str
    num_vertices: int
    num_triangles: int


class STLTool:
    """Comprehensive STL analysis tool with dimensional and geometric inspection"""

    def __init__(self, filepath: str, verbose: bool = False):
        """Initialize tool and parse file"""
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.verbose = verbose
        self.coordinates = []
        self.format = None
        
        self._parse()
        self._calculate_dimensions()
        self._analyze_geometry()

    # ============================================================================
    # PARSING
    # ============================================================================

    def _parse(self):
        """Auto-detect format and parse"""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")

        try:
            self.coordinates = self._parse_ascii()
            self.format = "ASCII"
            if self.verbose:
                print(f"  [Parsed as ASCII: {len(self.coordinates)} vertices]")
            return
        except Exception:
            pass

        try:
            self.coordinates = self._parse_binary()
            self.format = "Binary"
            if self.verbose:
                print(f"  [Parsed as Binary: {len(self.coordinates)} vertices]")
            return
        except Exception as e:
            raise ValueError(f"Failed to parse STL file: {e}")

    def _parse_ascii(self) -> List[Tuple[float, float, float]]:
        """Parse ASCII STL file"""
        with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        vertices = re.findall(
            r'vertex\s+([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)',
            content
        )

        if not vertices:
            raise ValueError("No vertices found in ASCII STL")

        return [(float(x), float(y), float(z)) for x, y, z in vertices]

    def _parse_binary(self) -> List[Tuple[float, float, float]]:
        """Parse binary STL file"""
        with open(self.filepath, 'rb') as f:
            f.read(80)
            num_triangles = struct.unpack('I', f.read(4))[0]

            if num_triangles == 0:
                raise ValueError("No triangles in binary STL")

            coordinates = []
            for _ in range(num_triangles):
                f.read(12)  # normal
                for _ in range(3):
                    x, y, z = struct.unpack('fff', f.read(12))
                    coordinates.append((x, y, z))
                f.read(2)  # attribute

        return coordinates

    # ============================================================================
    # DIMENSIONAL ANALYSIS
    # ============================================================================

    def _calculate_dimensions(self):
        """Calculate all dimensional metrics"""
        if not self.coordinates:
            raise ValueError("No coordinates to analyze")

        xs = [c[0] for c in self.coordinates]
        ys = [c[1] for c in self.coordinates]
        zs = [c[2] for c in self.coordinates]

        # Basic bounds
        self.min_x, self.max_x = min(xs), max(xs)
        self.min_y, self.max_y = min(ys), max(ys)
        self.min_z, self.max_z = min(zs), max(zs)

        # Dimensions
        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y
        self.depth = self.max_z - self.min_z

        # Center
        self.center_x = (self.min_x + self.max_x) / 2
        self.center_y = (self.min_y + self.max_y) / 2
        self.center_z = (self.min_z + self.max_z) / 2

        # Volume (bounding box approximation)
        self.volume = self.width * self.height * self.depth

        # Surface area (bounding box approximation)
        self.surface_area = 2 * (
            self.width * self.height +
            self.height * self.depth +
            self.depth * self.width
        )

        # Vertex and triangle counts
        self.num_vertices = len(self.coordinates)
        self.num_triangles = len(self.coordinates) // 3

    # ============================================================================
    # GEOMETRIC ANALYSIS
    # ============================================================================

    def _analyze_geometry(self):
        """Perform comprehensive geometric analysis"""
        xs = [c[0] for c in self.coordinates]
        ys = [c[1] for c in self.coordinates]
        zs = [c[2] for c in self.coordinates]

        # Unique levels (complexity indicator)
        self.unique_z = len(set(round(z * 10) / 10 for z in zs))
        self.unique_x = len(set(round(x * 10) / 10 for x in xs))
        self.unique_y = len(set(round(y * 10) / 10 for y in ys))

        # Feature detection
        self._detect_features()
        self._detect_curves()
        self._detect_cavities()
        self._detect_symmetry()
        self._estimate_wall_thickness()
        self._classify_shape()

    def _detect_features(self):
        """Detect mounting pegs and basic features"""
        if self.min_z < -2:
            self.peg_height = abs(self.min_z)
            self.has_pegs = True
        else:
            self.peg_height = 0
            self.has_pegs = False

    def _detect_curves(self):
        """Detect curved surfaces"""
        z_levels = sorted(set(round(z, 1) for z in [c[2] for c in self.coordinates]))
        curvature_count = 0

        for z_level in z_levels[:min(20, len(z_levels))]:
            level_coords = [
                c for c in self.coordinates if abs(c[2] - z_level) < 0.3
            ]

            if len(level_coords) > 10:
                ys = [c[1] for c in level_coords]
                y_unique = len(set(round(y, 1) for y in ys))

                if y_unique > 15:
                    curvature_count += 1

        self.has_curves = curvature_count > 5

    def _detect_cavities(self):
        """Detect interior cavities"""
        self.cavities = []
        z_bins = defaultdict(list)

        for coord in self.coordinates:
            z_bin = round(coord[2], 1)
            z_bins[z_bin].append(coord)

        for z_level, coords in z_bins.items():
            if len(coords) < 20:
                continue

            xs = [c[0] for c in coords]
            ys = [c[1] for c in coords]

            x_range = max(xs) - min(xs)
            y_range = max(ys) - min(ys)

            if x_range < self.width * 0.7 and y_range < self.height * 0.7:
                self.cavities.append((min(xs), min(ys), z_level))

        self.num_cavities = len(set(self.cavities))

    def _detect_symmetry(self):
        """Detect axis symmetry"""
        xs = [c[0] for c in self.coordinates]
        ys = [c[1] for c in self.coordinates]

        # X-axis symmetry
        left_points = sum(1 for x in xs if x < self.center_x)
        right_points = sum(1 for x in xs if x > self.center_x)
        self.x_symmetric = abs(left_points - right_points) / max(left_points, right_points) < 0.1 if max(left_points, right_points) > 0 else False

        # Y-axis symmetry
        front_points = sum(1 for y in ys if y < self.center_y)
        back_points = sum(1 for y in ys if y > self.center_y)
        self.y_symmetric = abs(front_points - back_points) / max(front_points, back_points) < 0.1 if max(front_points, back_points) > 0 else False

    def _estimate_wall_thickness(self):
        """Estimate wall thickness"""
        x_counts = defaultdict(int)
        for x in [c[0] for c in self.coordinates]:
            x_rounded = round(x, 1)
            x_counts[x_rounded] += 1

        if len(x_counts) < 10:
            self.wall_thickness = None
            return

        sorted_xs = sorted(x_counts.keys())
        gaps = []

        for i in range(len(sorted_xs) - 1):
            gap = sorted_xs[i + 1] - sorted_xs[i]
            if gap > 0.5:
                gaps.append(gap)

        if gaps:
            avg_wall = sum(gaps) / len(gaps)
            self.wall_thickness = min(avg_wall, self.width * 0.2)
        else:
            self.wall_thickness = None

    def _classify_complexity(self) -> str:
        """Classify geometric complexity"""
        score = self.unique_z
        if score > 100:
            return "Very Complex"
        elif score > 50:
            return "Complex"
        elif score > 20:
            return "Moderate"
        elif score > 10:
            return "Moderate"
        else:
            return "Simple"

    def _classify_shape(self):
        """Classify overall shape"""
        self.complexity = self._classify_complexity()

        if self.has_pegs:
            if self.has_curves:
                self.estimated_shape = "Cylindrical holder with mounting pegs"
            else:
                self.estimated_shape = "Rectangular holder with mounting pegs"
        else:
            if self.has_curves:
                self.estimated_shape = "Curved/cylindrical shape (no pegs)"
            else:
                self.estimated_shape = "Rectangular/box shape"

        if self.num_cavities > 0:
            self.estimated_shape += f" with {self.num_cavities} cavities"

    # ============================================================================
    # OUTPUT METHODS
    # ============================================================================

    def print_full_analysis(self):
        """Print complete analysis report"""
        print(f"\n{'='*80}")
        print(f"STL COMPREHENSIVE ANALYSIS: {self.filename}")
        print(f"{'='*80}")

        self.print_file_info()
        self.print_dimensional_analysis()
        self.print_geometric_analysis()
        self.print_features()
        self.print_properties()

    def print_file_info(self):
        """Print file information"""
        print(f"\nFile Information:")
        print(f"  Format: {self.format}")
        print(f"  Path: {self.filepath}")
        print(f"  Vertices: {self.num_vertices:,}")
        print(f"  Triangles: {self.num_triangles:,}")

    def print_dimensional_analysis(self):
        """Print dimensional metrics"""
        print(f"\nDimensional Analysis:")
        print(f"  Width (X):  {self.width:.4f} mm ({self.min_x:.4f} to {self.max_x:.4f})")
        print(f"  Height (Y): {self.height:.4f} mm ({self.min_y:.4f} to {self.max_y:.4f})")
        print(f"  Depth (Z):  {self.depth:.4f} mm ({self.min_z:.4f} to {self.max_z:.4f})")
        print(f"  Center: ({self.center_x:.4f}, {self.center_y:.4f}, {self.center_z:.4f})")

    def print_geometric_analysis(self):
        """Print geometric metrics"""
        print(f"\nGeometric Analysis:")
        print(f"  Complexity Level: {self.complexity}")
        print(f"  Unique Z Levels: {self.unique_z}")
        print(f"  Unique X Levels: {self.unique_x}")
        print(f"  Unique Y Levels: {self.unique_y}")

    def print_features(self):
        """Print detected features"""
        print(f"\nDetected Features:")
        
        if self.has_pegs:
            print(f"  ✓ Mounting pegs: extend {self.peg_height:.2f}mm below base")
        else:
            print(f"  ✗ No mounting pegs detected")

        if self.has_curves:
            print(f"  ✓ Curved surfaces detected: cylindrical or rounded edges")
        else:
            print(f"  ✗ No curved surfaces (flat or rectangular)")

        if self.num_cavities > 0:
            print(f"  ✓ Interior cavities: {self.num_cavities} distinct voids")
        else:
            print(f"  ✗ No interior cavities")

        if self.x_symmetric:
            print(f"  ✓ X-axis symmetry detected")
        if self.y_symmetric:
            print(f"  ✓ Y-axis symmetry detected")

        if self.wall_thickness:
            print(f"  ✓ Estimated wall thickness: {self.wall_thickness:.1f}mm")

    def print_properties(self):
        """Print surface properties and estimates"""
        print(f"\nSurface Properties:")
        print(f"  Est. Volume: {self.volume:,.2f} mm³")
        print(f"  Est. Surface Area: {self.surface_area:,.2f} mm²")
        
        # Material estimates
        density_pla = 1.24  # g/cm³
        volume_cm3 = self.volume / 1000  # convert mm³ to cm³
        weight_pla = volume_cm3 * density_pla
        print(f"  Est. Weight (PLA): {weight_pla:.1f}g")

        print(f"\nEstimated Shape:")
        print(f"  {self.estimated_shape}")

        print(f"\n{'='*80}\n")

    def print_dimensions_only(self):
        """Print dimensions in table format"""
        print(f"\n{self.filename}")
        print("-" * 70)
        print(f"  Format: {self.format}")
        print(f"  Dimensions (W × L × H): {self.width:.2f} × {self.height:.2f} × {self.depth:.2f} mm")
        print(f"  Bounding box:")
        print(f"    X: {self.min_x:.4f} to {self.max_x:.4f} mm")
        print(f"    Y: {self.min_y:.4f} to {self.max_y:.4f} mm")
        print(f"    Z: {self.min_z:.4f} to {self.max_z:.4f} mm")
        print(f"  Vertices: {self.num_vertices:,}")
        print(f"  Triangles: {self.num_triangles:,}")

    def print_geometry_only(self):
        """Print geometry metrics only"""
        print(f"\n{self.filename} - Geometric Analysis")
        print("-" * 70)
        print(f"  Complexity: {self.complexity}")
        print(f"  Z Levels: {self.unique_z}")
        print(f"  Mounting Pegs: {self.has_pegs}")
        print(f"  Curved Surfaces: {self.has_curves}")
        print(f"  Cavities: {self.num_cavities}")
        print(f"  Shape: {self.estimated_shape}")

    def print_features_only(self):
        """Print features only"""
        print(f"\n{self.filename} - Feature Analysis")
        print("-" * 70)
        features = []
        if self.has_pegs:
            features.append(f"pegs({self.peg_height:.1f}mm)")
        if self.has_curves:
            features.append("curves")
        if self.num_cavities > 0:
            features.append(f"cavities({self.num_cavities})")
        if self.x_symmetric:
            features.append("x-sym")
        if self.y_symmetric:
            features.append("y-sym")
        if self.wall_thickness:
            features.append(f"wall({self.wall_thickness:.1f}mm)")

        if features:
            print(f"  Features: {', '.join(features)}")
        else:
            print(f"  Features: none")
        print(f"  Shape: {self.estimated_shape}")

    def __str__(self) -> str:
        """String representation"""
        return (f"{self.filename} ({self.format}): "
                f"{self.width:.2f}×{self.height:.2f}×{self.depth:.2f}mm | "
                f"{self.complexity} | {self.estimated_shape}")


# ============================================================================
# COMPARISON FUNCTIONS
# ============================================================================

def compare_models(tool1: STLTool, tool2: STLTool) -> Dict:
    """Compare two STL models"""
    return {
        'tool1': tool1,
        'tool2': tool2,
        'dimension_match': (
            abs(tool1.width - tool2.width) < 0.5 and
            abs(tool1.height - tool2.height) < 0.5 and
            abs(tool1.depth - tool2.depth) < 0.5
        ),
        'complexity_match': tool1.complexity == tool2.complexity,
        'features_match': (
            tool1.has_pegs == tool2.has_pegs and
            tool1.has_curves == tool2.has_curves
        ),
        'width_diff': abs(tool1.width - tool2.width),
        'height_diff': abs(tool1.height - tool2.height),
        'depth_diff': abs(tool1.depth - tool2.depth),
        'complexity_diff': abs(tool1.unique_z - tool2.unique_z),
    }


def print_comparison(tool1: STLTool, tool2: STLTool):
    """Print detailed comparison"""
    comparison = compare_models(tool1, tool2)

    print(f"\n{'='*80}")
    print(f"COMPREHENSIVE STL COMPARISON")
    print(f"{tool1.filename} vs {tool2.filename}")
    print(f"{'='*80}")

    # Full analysis of both
    print(f"\nModel 1: {tool1.filename}")
    print("-" * 80)
    tool1.print_file_info()
    tool1.print_dimensional_analysis()
    tool1.print_geometric_analysis()

    print(f"\nModel 2: {tool2.filename}")
    print("-" * 80)
    tool2.print_file_info()
    tool2.print_dimensional_analysis()
    tool2.print_geometric_analysis()

    # Comparison results
    print(f"\n{'='*80}")
    print(f"COMPARISON RESULTS")
    print(f"{'='*80}")

    print(f"\nDimensional Comparison:")
    print(f"  Width:  {tool1.width:8.2f}mm vs {tool2.width:8.2f}mm (diff: {comparison['width_diff']:7.2f}mm)")
    print(f"  Height: {tool1.height:8.2f}mm vs {tool2.height:8.2f}mm (diff: {comparison['height_diff']:7.2f}mm)")
    print(f"  Depth:  {tool1.depth:8.2f}mm vs {tool2.depth:8.2f}mm (diff: {comparison['depth_diff']:7.2f}mm)")
    print(f"  Volume: {tool1.volume:,.2f}mm³ vs {tool2.volume:,.2f}mm³")

    print(f"\nGeometric Comparison:")
    print(f"  Complexity: {tool1.complexity} vs {tool2.complexity} (Z levels: {tool1.unique_z} vs {tool2.unique_z})")
    print(f"  Complexity Difference: {comparison['complexity_diff']} Z levels")

    print(f"\nFeature Comparison:")
    print(f"  Mounting pegs: {tool1.has_pegs} vs {tool2.has_pegs}")
    print(f"  Curved surfaces: {tool1.has_curves} vs {tool2.has_curves}")
    print(f"  Cavities: {tool1.num_cavities} vs {tool2.num_cavities}")
    print(f"  X-axis symmetry: {tool1.x_symmetric} vs {tool2.x_symmetric}")
    print(f"  Y-axis symmetry: {tool1.y_symmetric} vs {tool2.y_symmetric}")

    # Overall assessment
    print(f"\n{'='*80}")
    print(f"ASSESSMENT")
    print(f"{'='*80}")

    if comparison['dimension_match']:
        print(f"✓ Dimensions match (within 0.5mm tolerance)")
    else:
        print(f"✗ Dimensions DO NOT match")

    if comparison['features_match']:
        print(f"✓ Key features match (pegs, curves)")
    else:
        print(f"✗ Key features DO NOT match")
        if tool1.has_pegs != tool2.has_pegs:
            print(f"    - Mounting pegs: {tool1.has_pegs} vs {tool2.has_pegs}")
        if tool1.has_curves != tool2.has_curves:
            print(f"    - Curved surfaces: {tool1.has_curves} vs {tool2.has_curves}")

    if comparison['complexity_match']:
        print(f"✓ Geometry complexity matches")
    else:
        print(f"✗ Geometry complexity differs ({comparison['complexity_diff']} Z level difference)")

    overall_match = (
        comparison['dimension_match'] and
        comparison['features_match'] and
        abs(comparison['complexity_diff']) < 30
    )

    print(f"\n{'='*80}")
    if overall_match:
        print(f"✓✓✓ MODELS MATCH - Geometries are compatible")
    else:
        print(f"✗✗✗ MODELS DIFFER - Significant differences detected")
    print(f"{'='*80}\n")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Comprehensive STL Analysis Tool - Complete dimensional and geometric inspection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full analysis
  python3 stl_tool.py model.stl

  # Compare two models
  python3 stl_tool.py --compare generated.stl reference.stl

  # Dimensions only
  python3 stl_tool.py --dimensions examples/*.stl

  # Geometry only
  python3 stl_tool.py --geometry model.stl

  # Features only
  python3 stl_tool.py --features model.stl

  # Batch analysis
  python3 stl_tool.py examples/*.stl

  # Verbose output
  python3 stl_tool.py --verbose model.stl
        """
    )

    parser.add_argument('files', nargs='*', help='STL file(s) to analyze')
    parser.add_argument('--compare', action='store_true', help='Compare first two files')
    parser.add_argument('--dimensions', action='store_true', help='Show dimensions only')
    parser.add_argument('--geometry', action='store_true', help='Show geometry only')
    parser.add_argument('--features', action='store_true', help='Show features only')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if not args.files:
        parser.print_help()
        return

    # Comparison mode
    if args.compare and len(args.files) >= 2:
        try:
            tool1 = STLTool(args.files[0], args.verbose)
            tool2 = STLTool(args.files[1], args.verbose)
            print_comparison(tool1, tool2)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # Single file - select output format
    if len(args.files) == 1:
        try:
            tool = STLTool(args.files[0], args.verbose)
            if args.dimensions:
                tool.print_dimensions_only()
            elif args.geometry:
                tool.print_geometric_analysis()
            elif args.features:
                tool.print_features_only()
            else:
                tool.print_full_analysis()
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # Multiple files - batch analysis
    if len(args.files) > 1:
        if args.dimensions:
            print(f"\n{'='*100}")
            print(f"DIMENSIONAL ANALYSIS - BATCH")
            print(f"{'='*100}")
            for filepath in args.files:
                try:
                    tool = STLTool(filepath, args.verbose)
                    tool.print_dimensions_only()
                except Exception as e:
                    print(f"Error parsing {filepath}: {e}", file=sys.stderr)
        else:
            print(f"\n{'='*100}")
            print(f"COMPREHENSIVE STL ANALYSIS - BATCH")
            print(f"{'='*100}\n")

            tools = []
            for filepath in args.files:
                try:
                    tool = STLTool(filepath, args.verbose)
                    tools.append(tool)
                except Exception as e:
                    print(f"Error parsing {filepath}: {e}", file=sys.stderr)

            if tools:
                # Summary table
                print(f"{'File':<40} {'Format':<8} {'W×H×D':<18} {'Complexity':<12} {'Features':<40}")
                print("-" * 120)

                for tool in tools:
                    features = []
                    if tool.has_pegs:
                        features.append("pegs")
                    if tool.has_curves:
                        features.append("curves")
                    if tool.num_cavities > 0:
                        features.append(f"cavities({tool.num_cavities})")
                    if tool.x_symmetric or tool.y_symmetric:
                        features.append("sym")
                    if tool.wall_thickness:
                        features.append(f"wall({tool.wall_thickness:.1f}mm)")

                    feature_str = ", ".join(features) if features else "none"
                    dims = f"{tool.width:.1f}×{tool.height:.1f}×{tool.depth:.1f}"
                    print(f"{tool.filename:<40} {tool.format:<8} {dims:<18} {tool.complexity:<12} {feature_str:<40}")

                print(f"\n{'='*100}\n")


if __name__ == '__main__':
    main()
