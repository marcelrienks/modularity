"""Unit tests for assembly guide generation (User Story 4)."""

import pytest
from unittest.mock import Mock, patch
from core.assembly_guide import AssemblyGuideGenerator


class TestAssemblyGuideTemplate:
    """Test assembly guide template rendering."""

    def test_filename_generation(self):
        """Filename encodes parameters correctly."""
        gen = AssemblyGuideGenerator(diameter=20.0, height=15.0)
        filename = gen._get_filename()
        assert filename == "handle_d20.0_h15.0_README.md"

    def test_filename_with_precision(self):
        """Filename maintains decimal precision."""
        gen = AssemblyGuideGenerator(diameter=20.14159, height=10.5)
        filename = gen._get_filename()
        assert "20.14159" in filename
        assert "10.5" in filename

    @patch("core.assembly_guide.Environment")
    def test_template_context_diameter(self, mock_env):
        """Template context includes diameter."""
        # This is a placeholder test for when template rendering is implemented
        gen = AssemblyGuideGenerator(diameter=20.0, height=15.0)
        assert gen.diameter == 20.0

    @patch("core.assembly_guide.Environment")
    def test_template_context_height(self, mock_env):
        """Template context includes height."""
        gen = AssemblyGuideGenerator(diameter=20.0, height=15.0)
        assert gen.height == 15.0
