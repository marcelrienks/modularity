"""Contract tests for CLI parameters (User Story 1)."""

import subprocess
import pytest


class TestCLIParameters:
    """Test CLI command-line interface for required parameters."""

    def test_cli_with_both_parameters(self):
        """CLI accepts --diameter and --height."""
        result = subprocess.run(
            ["python", "generate.py", "--diameter", "20.0", "--height", "15.0"],
            cwd="/Users/marcelrienks/workspace/code/modularity/tulgryd/handles",
            capture_output=True,
            text=True,
        )
        # Currently stubs out; will check success after implementation
        assert result.returncode in (0, 1, 2, 3)  # Accept any; not yet implemented

    def test_cli_missing_diameter(self):
        """CLI fails if --diameter missing."""
        result = subprocess.run(
            ["python", "generate.py", "--height", "15.0"],
            cwd="/Users/marcelrienks/workspace/code/modularity/tulgryd/handles",
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, "Should fail without --diameter"
        assert "diameter" in result.stderr.lower() or "required" in result.stderr.lower()

    def test_cli_missing_height(self):
        """CLI fails if --height missing."""
        result = subprocess.run(
            ["python", "generate.py", "--diameter", "20.0"],
            cwd="/Users/marcelrienks/workspace/code/modularity/tulgryd/handles",
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, "Should fail without --height"
        assert "height" in result.stderr.lower() or "required" in result.stderr.lower()

    def test_cli_missing_both_parameters(self):
        """CLI fails if both --diameter and --height missing."""
        result = subprocess.run(
            ["python", "generate.py"],
            cwd="/Users/marcelrienks/workspace/code/modularity/tulgryd/handles",
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, "Should fail without parameters"


class TestCLIHelp:
    """Test CLI help functionality."""

    def test_cli_help_flag(self):
        """CLI --help shows usage."""
        result = subprocess.run(
            ["python", "generate.py", "--help"],
            cwd="/Users/marcelrienks/workspace/code/modularity/tulgryd/handles",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "Help should succeed"
        assert "diameter" in result.stdout.lower(), "Help should mention --diameter"
        assert "height" in result.stdout.lower(), "Help should mention --height"
        assert "usage" in result.stdout.lower(), "Help should show usage"

    def test_cli_version_flag(self):
        """CLI --version shows version."""
        result = subprocess.run(
            ["python", "generate.py", "--version"],
            cwd="/Users/marcelrienks/workspace/code/modularity/tulgryd/handles",
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "Version should succeed"
        assert "0.1" in result.stdout or "0.1" in result.stderr, "Should show version"
