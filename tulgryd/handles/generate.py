"""Parametric handles generator CLI."""

import sys
import os
from pathlib import Path
import click
from core import HandleParameters, HandleBuilder, HandleExporter, AssemblyGuideGenerator

__version__ = "0.1.0"


@click.command(
    context_settings=dict(help_option_names=['-h', '--help']),
    epilog="""
\b
EXAMPLES:
  # Generate standard handle (STL format)
  python generate.py --diameter 2.6 --height 2.0

  # Export to both STL and STEP formats
  python generate.py --diameter 3.5 --height 1.5 --format both

  # Custom output directory
  python generate.py --diameter 2.6 --height 2.0 --output-dir ./my-models

  # Check version
  python generate.py --version

PARAMETER RANGES:
  Diameter: 1.0–10.0 mm (grip end width)
  Height:   0.5–5.0 mm (handle grip height above mounting surface)

EXIT CODES:
  0 = Success
  1 = Parameter validation error
  2 = Geometry building error
  3 = Export error (permissions, disk space)
  4 = User cancelled (file overwrite declined)
    """,
)
@click.option(
    "--diameter",
    type=float,
    required=True,
    help="Grip diameter in mm [1.0-10.0]",
    metavar="FLOAT",
)
@click.option(
    "--height",
    type=float,
    required=True,
    help="Grip height in mm [0.5-5.0]",
    metavar="FLOAT",
)
@click.option(
    "--format",
    type=click.Choice(["stl", "step", "both"], case_sensitive=False),
    default="stl",
    help="Export format: stl|step|both (default: stl)",
)
@click.option(
    "--output-dir",
    type=click.Path(),
    default="./output",
    help="Output directory (default: ./output)",
)
@click.version_option(__version__)
def generate(diameter, height, format, output_dir):
    """Generate custom parametric handle models with specified grip diameter and height.
    
    Creates a 3D-printable handle model and assembly guide (README.md) with print settings.
    
    Output files are saved to the specified directory with names encoding the parameters:
    handle_d{diameter}_h{height}.stl (or .step)
    """
    try:
        # Validate parameters
        params = HandleParameters(diameter, height)
        is_valid, errors = params.validate()
        if not is_valid:
            for error in errors:
                click.echo(f"❌ ERROR: {error}", err=True)
            sys.exit(1)

        output_path = Path(output_dir)

        # Build geometry
        builder = HandleBuilder(params)
        shape = builder.build()
        
        if not builder.validate():
            click.echo("❌ ERROR: Geometry validation failed (not watertight)", err=True)
            sys.exit(2)

        # Check for existing files before export
        exporter = HandleExporter(shape, diameter, height)
        
        # Determine files to check
        check_files = []
        if format in ("stl", "both"):
            check_files.append(output_path / exporter._get_filename("stl"))
        if format in ("step", "both"):
            check_files.append(output_path / exporter._get_filename("step"))
        
        # Interactive overwrite prompt
        for filepath in check_files:
            if filepath.exists():
                response = input(f"File exists, overwrite? {filepath.name} [y/N]: ").strip().lower()
                if response not in ("y", "yes"):
                    click.echo("Aborted.", err=True)
                    sys.exit(4)

        # Export (will raise on permission errors, etc.)
        try:
            exported = exporter.export(output_path, formats=format)
        except FileExistsError:
            # Already prompted; if we get here, user said no
            click.echo("Export cancelled.", err=True)
            sys.exit(4)
        except PermissionError as e:
            click.echo(f"❌ ERROR: {str(e)}", err=True)
            sys.exit(3)
        except Exception as e:
            click.echo(f"❌ ERROR: Export failed - {str(e)}", err=True)
            sys.exit(3)

        # Generate assembly guide
        guide_gen = AssemblyGuideGenerator(diameter, height)
        guide_path = guide_gen.generate(output_path)

        # Success message
        click.echo(f"✓ Success: Generated handle models and documentation")
        for path in exported:
            click.echo(f"  → {path}")
        click.echo(f"  → {guide_path}")

    except Exception as e:
        click.echo(f"❌ ERROR: {str(e)}", err=True)
        sys.exit(3)


if __name__ == "__main__":
    generate()
