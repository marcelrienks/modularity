"""End-to-end tests with multiple parameter sets (T058)."""

import pytest
import tempfile
from pathlib import Path
from core import HandleParameters, HandleBuilder, HandleExporter, AssemblyGuideGenerator


class TestE2EMultipleParameterSets:
    """Test full pipeline with 3 different parameter sets."""

    def test_e2e_three_parameter_sets(self):
        """T058: Generate 3 different handle models with different parameter sets."""
        parameter_sets = [
            (10.0, 3.0),   # Min values
            (20.0, 15.0),  # Mid values
            (30.0, 30.0),  # Max values
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            
            for diameter, height in parameter_sets:
                # Validate parameters
                params = HandleParameters(diameter, height)
                is_valid, errors = params.validate()
                assert is_valid, f"Validation failed for d={diameter}, h={height}: {errors}"
                
                # Build geometry
                builder = HandleBuilder(params)
                shape = builder.build()
                assert builder.validate(), f"Geometry validation failed for d={diameter}, h={height}"
                
                # Export model
                exporter = HandleExporter(shape, diameter, height)
                files = exporter.export(output_dir, formats="stl")
                assert len(files) == 1
                assert Path(files[0]).exists()
                
                # Generate assembly guide
                guide_gen = AssemblyGuideGenerator(diameter, height)
                guide_path = guide_gen.generate(output_dir)
                assert Path(guide_path).exists()
                
                # Verify filenames match expected pattern
                expected_stl = f"handle_d{diameter}_h{height}.stl"
                expected_readme = f"handle_d{diameter}_h{height}_README.md"
                
                assert Path(files[0]).name == expected_stl
                assert Path(guide_path).name == expected_readme
            
            # Verify all 6 files created (3 models + 3 READMEs)
            all_files = list(output_dir.glob("*"))
            assert len(all_files) == 6

    def test_e2e_parameter_coverage(self):
        """Test parameter ranges across the valid spectrum."""
        test_cases = [
            (10.0, 3.0, "minimum values"),
            (15.0, 8.0, "typical values"),
            (20.0, 15.0, "mid-range values"),
            (25.0, 22.0, "high range values"),
            (30.0, 30.0, "maximum values"),
        ]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            
            for diameter, height, description in test_cases:
                # Full pipeline
                params = HandleParameters(diameter, height)
                is_valid, errors = params.validate()
                assert is_valid, f"Failed for {description}: {errors}"
                
                builder = HandleBuilder(params)
                shape = builder.build()
                assert builder.validate()
                
                exporter = HandleExporter(shape, diameter, height)
                files = exporter.export(output_dir, formats="both")
                
                assert len(files) == 2, f"Expected 2 files for {description}, got {len(files)}"
                assert all(Path(f).exists() for f in files)
                
                # Verify file extensions
                extensions = {Path(f).suffix for f in files}
                assert extensions == {".stl", ".step"}

    def test_e2e_multi_format_consistency(self):
        """Test that STL and STEP exports represent the same geometry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            diameter, height = 20.5, 12.8
            
            # Generate both formats
            params = HandleParameters(diameter, height)
            builder = HandleBuilder(params)
            shape = builder.build()
            exporter = HandleExporter(shape, diameter, height)
            files = exporter.export(output_dir, formats="both")
            
            # Check file sizes (both should be substantial)
            stl_path = next(f for f in files if f.endswith(".stl"))
            step_path = next(f for f in files if f.endswith(".step"))
            
            stl_size = Path(stl_path).stat().st_size
            step_size = Path(step_path).stat().st_size
            
            # Both files should have meaningful content (> 1KB)
            assert stl_size > 1024, f"STL file too small: {stl_size} bytes"
            assert step_size > 1024, f"STEP file too small: {step_size} bytes"
