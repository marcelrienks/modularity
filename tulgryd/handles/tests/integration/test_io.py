"""Integration tests for I/O and directory handling (T052)."""

import pytest
import os
import tempfile
from pathlib import Path
from core import HandleParameters, HandleBuilder, HandleExporter


class TestDirectoryCreation:
    """Test output directory creation and error handling."""

    def test_auto_create_output_directory(self):
        """T051: Auto-create output directory if missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "nonexistent" / "nested"
            
            params = HandleParameters(2.6, 2.0)
            builder = HandleBuilder(params)
            shape = builder.build()
            exporter = HandleExporter(shape, 2.6, 2.0)
            
            # Should create directory without error
            files = exporter.export(output_dir, formats="stl")
            
            assert output_dir.exists()
            assert len(files) == 1
            assert files[0].endswith(".stl")

    def test_directory_creation_failure_permission_denied(self):
        """T052: Handle permission errors when directory not writable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "readonly"
            output_dir.mkdir()
            
            # Make directory read-only
            os.chmod(output_dir, 0o444)
            
            try:
                params = HandleParameters(2.6, 2.0)
                builder = HandleBuilder(params)
                shape = builder.build()
                exporter = HandleExporter(shape, 2.6, 2.0)
                
                # Should raise PermissionError
                with pytest.raises(PermissionError):
                    exporter.export(output_dir, formats="stl")
            finally:
                # Restore write permission for cleanup
                os.chmod(output_dir, 0o755)

    def test_existing_directory_not_recreated(self):
        """Test that existing directories are not recreated."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            
            # Create directory first
            marker_file = output_dir / ".marker"
            marker_file.touch()
            
            params = HandleParameters(2.6, 2.0)
            builder = HandleBuilder(params)
            shape = builder.build()
            exporter = HandleExporter(shape, 2.6, 2.0)
            
            files = exporter.export(output_dir, formats="stl")
            
            # Marker file should still exist
            assert marker_file.exists()
            assert len(files) == 1
