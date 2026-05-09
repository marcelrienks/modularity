"""Contract tests for filename encoding precision (User Story 1)."""

import pytest
from core.exporter import HandleExporter
from unittest.mock import Mock


class TestFilenameEncoding:
    """Test filename encoding maintains ±0.1mm precision."""

    def test_filename_min_diameter(self):
        """Filename with minimum diameter."""
        mock_shape = Mock()
        exporter = HandleExporter(mock_shape, diameter=10.0, height=15.0)
        filename = exporter._get_filename("stl")
        assert filename == "handle_d10.0_h15.0.stl"

    def test_filename_max_diameter(self):
        """Filename with maximum diameter."""
        mock_shape = Mock()
        exporter = HandleExporter(mock_shape, diameter=30.0, height=15.0)
        filename = exporter._get_filename("stl")
        assert filename == "handle_d30.0_h15.0.stl"

    def test_filename_with_decimal_precision(self):
        """Filename preserves decimal precision."""
        mock_shape = Mock()
        exporter = HandleExporter(mock_shape, diameter=20.61, height=10.5)
        filename = exporter._get_filename("stl")
        assert "20.61" in filename, "Should preserve 0.01mm precision"
        assert "10.5" in filename

    def test_filename_edge_value_precision(self):
        """Filename with edge-case precision values."""
        mock_shape = Mock()
        # Test 0.1mm precision edge case
        exporter = HandleExporter(mock_shape, diameter=15.6, height=3.0)
        filename = exporter._get_filename("stl")
        assert filename == "handle_d15.6_h3.0.stl"

    def test_filename_step_format(self):
        """Filename with STEP format."""
        mock_shape = Mock()
        exporter = HandleExporter(mock_shape, diameter=20.14, height=12.71)
        filename = exporter._get_filename("step")
        assert filename.endswith(".step")
        assert "20.14" in filename
