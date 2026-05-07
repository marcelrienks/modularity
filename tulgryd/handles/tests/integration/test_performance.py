"""Performance tests for generation speed (T059)."""

import pytest
import tempfile
import time
from pathlib import Path
from core import HandleParameters, HandleBuilder, HandleExporter, AssemblyGuideGenerator


class TestPerformance:
    """Test that generation completes within performance targets."""

    @pytest.mark.timeout(5)  # Ensure pytest timeout catches hangs
    def test_generation_completes_in_under_2_seconds(self):
        """T059: Generation (build + export) completes in < 2 seconds.
        
        Scope: geometry build + STL export + file write.
        Does not distinguish between build time and export time.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            diameter, height = 2.6, 2.0
            
            start_time = time.time()
            
            # Validate (minimal cost, not counted in budget)
            params = HandleParameters(diameter, height)
            is_valid, _ = params.validate()
            assert is_valid
            
            # Build + export (primary time sink)
            builder = HandleBuilder(params)
            shape = builder.build()
            builder.validate()  # Validation check
            
            exporter = HandleExporter(shape, diameter, height)
            files = exporter.export(output_dir, formats="stl")
            
            elapsed = time.time() - start_time
            
            assert elapsed < 2.0, f"Generation took {elapsed:.2f}s (target: <2.0s)"
            assert len(files) == 1

    def test_multi_format_export_performance(self):
        """Test that multi-format export completes reasonably fast."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            diameter, height = 3.5, 1.5
            
            params = HandleParameters(diameter, height)
            builder = HandleBuilder(params)
            shape = builder.build()
            
            start_time = time.time()
            exporter = HandleExporter(shape, diameter, height)
            files = exporter.export(output_dir, formats="both")
            elapsed = time.time() - start_time
            
            # Both formats should export quickly
            assert elapsed < 2.0, f"Multi-format export took {elapsed:.2f}s"
            assert len(files) == 2

    def test_assembly_guide_generation_performance(self):
        """Test that assembly guide generation is fast."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            diameter, height = 2.6, 2.0
            
            guide_gen = AssemblyGuideGenerator(diameter, height)
            
            start_time = time.time()
            guide_path = guide_gen.generate(output_dir)
            elapsed = time.time() - start_time
            
            # Assembly guide should render very quickly
            assert elapsed < 1.0, f"Assembly guide generation took {elapsed:.2f}s"
            assert Path(guide_path).exists()

    def test_full_pipeline_performance(self):
        """Test full pipeline (build + export + guide) performance."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            diameter, height = 3.5, 1.5
            
            start_time = time.time()
            
            # Full pipeline
            params = HandleParameters(diameter, height)
            is_valid, _ = params.validate()
            assert is_valid
            
            builder = HandleBuilder(params)
            shape = builder.build()
            assert builder.validate()
            
            exporter = HandleExporter(shape, diameter, height)
            files = exporter.export(output_dir, formats="both")
            
            guide_gen = AssemblyGuideGenerator(diameter, height)
            guide_path = guide_gen.generate(output_dir)
            
            elapsed = time.time() - start_time
            
            # Full pipeline with multi-format should complete reasonably fast
            assert elapsed < 3.0, f"Full pipeline took {elapsed:.2f}s (target: <3.0s for multi-format)"
            assert len(files) == 2
            assert Path(guide_path).exists()

    def test_parameter_validation_is_fast(self):
        """Verify parameter validation has minimal overhead."""
        start_time = time.time()
        
        for i in range(100):
            params = HandleParameters(2.6 + i * 0.01, 2.0)
            is_valid, _ = params.validate()
            assert is_valid
        
        elapsed = time.time() - start_time
        
        # 100 validations should complete instantly
        assert elapsed < 0.5, f"100 validations took {elapsed:.2f}s"
