#!/usr/bin/env python3
"""
tulgryd Generator - Main CLI Entry Point
Generates modular tool grid tiles for custom drawer dimensions
"""

import click
import sys
from pathlib import Path
from datetime import datetime

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

from core.parameters import Parameters
from core.layout_calculator import LayoutCalculator
from core.builder import ModelBuilder
from core.assembly_guide import AssemblyGuideGenerator


@click.command()
@click.option('--total-width', type=float, help='Total width in mm')
@click.option('--total-length', type=float, help='Total length in mm')
@click.option('--single-tile', is_flag=True, help='Generate single tile instead of assembly')
@click.option('--tile-width', type=float, default=100.0, help='Tile width for single tile mode')
@click.option('--tile-length', type=float, default=100.0, help='Tile length for single tile mode')
@click.option('--output-dir', type=click.Path(), default='./output', help='Output directory')
@click.option('--format', type=click.Choice(['stl', 'step', 'both']), default='stl', help='Output format')
@click.option('--config', type=click.Path(exists=True), help='JSON config file')
@click.option('--preset', type=str, help='Use preset configuration')
@click.option('--hole-adjust', type=float, default=0.0, help='Hole diameter adjustment in mm (e.g., 0.2, -0.1)')
def generate(total_width, total_length, single_tile, tile_width, tile_length, 
             output_dir, format, config, preset, hole_adjust):
    """
    tulgryd Generator - Generate modular tool grid tiles
    
    Examples:
    
        # Generate tiles for 250×180mm drawer
        python generate.py --total-width 250 --total-length 180
        
        # Generate single 100×100mm tile
        python generate.py --single-tile
        
        # Generate custom single tile
        python generate.py --single-tile --tile-width 100 --tile-length 45
    """
    
    try:
        # Load parameters
        if config:
            params = Parameters.from_json(config)
        elif preset:
            preset_path = Path(__file__).parent / 'config' / 'presets' / f'{preset}.json'
            if preset_path.exists():
                params = Parameters.from_json(str(preset_path))
            else:
                click.echo(f"Error: Preset '{preset}' not found", err=True)
                return 1
        else:
            params = Parameters()
        
        # Apply hole diameter adjustment
        params.hole_diameter_adjustment = hole_adjust
        
        # Single tile mode
        if single_tile:
            adjust_text = f" (holes: Ø{params.hole_diameter + hole_adjust:.1f}mm)" if hole_adjust != 0 else ""
            click.echo(f"\n🔨 Generating single tile: {tile_length}×{tile_width}mm{adjust_text}\n")
            params.set_dimensions(tile_width, tile_length)
            
            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Build model
            builder = ModelBuilder(params)
            click.echo("Building model...")
            builder.build()
            
            # Export
            if format in ['stl', 'both']:
                stl_file = output_path / f"tile_{tile_length:.0f}x{tile_width:.0f}.stl"
                click.echo(f"Exporting STL: {stl_file}")
                builder.export_stl(str(stl_file))
            
            if format in ['step', 'both']:
                step_file = output_path / f"tile_{tile_length:.0f}x{tile_width:.0f}.step"
                click.echo(f"Exporting STEP: {step_file}")
                builder.export_step(str(step_file))
            
            click.echo(f"\n✅ Single tile generated successfully!")
            click.echo(f"   Output: {output_path.absolute()}\n")
            return 0
        
        # Assembly mode
        if not total_width or not total_length:
            click.echo("Error: --total-width and --total-length required for assembly mode", err=True)
            click.echo("Use --single-tile for single tile generation", err=True)
            return 1
        
        adjust_text = f" (holes: Ø{params.hole_diameter + hole_adjust:.1f}mm)" if hole_adjust != 0 else ""
        click.echo(f"\n🔨 Generating tile assembly for {total_length}×{total_width}mm{adjust_text}\n")
        
        # Calculate layout
        click.echo("Calculating layout...")
        calculator = LayoutCalculator(total_width, total_length)
        
        click.echo(f"✓ Layout calculated: {calculator.get_total_tile_count()} total tiles, "
                  f"{calculator.get_unique_count()} unique geometries\n")
        
        # Create timestamped output directory
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        output_path = Path(output_dir) / f"{timestamp}_{total_length:.0f}x{total_width:.0f}mm"
        output_path.mkdir(parents=True, exist_ok=True)
        
        click.echo(f"Output directory: {output_path.absolute()}\n")
        
        # Generate each unique tile
        unique_tiles = calculator.get_unique_tiles()
        click.echo("Generating tiles:")
        
        for i, tile_info in enumerate(unique_tiles, 1):
            dims = tile_info['dimensions']
            qty = tile_info['quantity']
            
            click.echo(f"  [{i}/{len(unique_tiles)}] {dims[0]:.0f}×{dims[1]:.0f}mm (qty: {qty})...", nl=False)
            
            # Set dimensions
            params.set_dimensions(dims[1], dims[0])  # width, length
            
            # Build model
            builder = ModelBuilder(params)
            builder.build()
            
            # Export
            filename = f"tile_{dims[0]:.0f}x{dims[1]:.0f}_qty{qty}"
            
            if format in ['stl', 'both']:
                stl_file = output_path / f"{filename}.stl"
                builder.export_stl(str(stl_file))
            
            if format in ['step', 'both']:
                step_file = output_path / f"{filename}.step"
                builder.export_step(str(step_file))
            
            click.echo(" ✓")
        
        # Generate assembly guide
        click.echo("\nGenerating assembly guide...")
        guide_gen = AssemblyGuideGenerator(calculator)
        readme_path = guide_gen.generate_readme(output_path)
        diagram_path = guide_gen.generate_layout_diagram_file(output_path)
        
        click.echo(f"  ✓ {Path(readme_path).name}")
        click.echo(f"  ✓ {Path(diagram_path).name}")
        
        # Summary
        click.echo(f"\n✅ Assembly generation complete!")
        click.echo(f"\n📦 Summary:")
        click.echo(f"   Total tiles to manufacture: {calculator.get_total_tile_count()}")
        click.echo(f"   Unique geometries: {calculator.get_unique_count()}")
        click.echo(f"   Output format: {format.upper()}")
        click.echo(f"   Location: {output_path.absolute()}")
        click.echo(f"\n📖 Next steps:")
        click.echo(f"   1. Review {readme_path}")
        click.echo(f"   2. Send STL files to 3D printer/CNC")
        click.echo(f"   3. Manufacture quantities as indicated in filenames")
        click.echo(f"   4. Follow assembly instructions in README\n")
        
        return 0
        
    except Exception as e:
        click.echo(f"\n❌ Error: {str(e)}", err=True)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(generate())
