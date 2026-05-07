"""Unit tests for parameter validation (User Story 3)."""

import pytest
from core.parameters import HandleParameters


class TestDiameterValidation:
    """Test diameter parameter validation."""

    def test_diameter_valid_min(self):
        """Valid minimum diameter."""
        params = HandleParameters(1.0, 2.0)
        is_valid, errors = params.validate()
        assert is_valid, f"Expected valid, got errors: {errors}"

    def test_diameter_valid_max(self):
        """Valid maximum diameter."""
        params = HandleParameters(10.0, 2.0)
        is_valid, errors = params.validate()
        assert is_valid, f"Expected valid, got errors: {errors}"

    def test_diameter_valid_mid(self):
        """Valid mid-range diameter."""
        params = HandleParameters(5.5, 2.0)
        is_valid, errors = params.validate()
        assert is_valid, f"Expected valid, got errors: {errors}"

    def test_diameter_below_min(self):
        """Diameter below minimum."""
        params = HandleParameters(0.9, 2.0)
        is_valid, errors = params.validate()
        assert not is_valid
        assert any("diameter must be between" in str(e) for e in errors)

    def test_diameter_above_max(self):
        """Diameter above maximum."""
        params = HandleParameters(10.1, 2.0)
        is_valid, errors = params.validate()
        assert not is_valid
        assert any("diameter must be between" in str(e) for e in errors)

    def test_diameter_zero(self):
        """Zero diameter."""
        params = HandleParameters(0.0, 2.0)
        is_valid, errors = params.validate()
        assert not is_valid

    def test_diameter_negative(self):
        """Negative diameter."""
        params = HandleParameters(-1.5, 2.0)
        is_valid, errors = params.validate()
        assert not is_valid


class TestHeightValidation:
    """Test height parameter validation."""

    def test_height_valid_min(self):
        """Valid minimum height."""
        params = HandleParameters(2.6, 0.5)
        is_valid, errors = params.validate()
        assert is_valid, f"Expected valid, got errors: {errors}"

    def test_height_valid_max(self):
        """Valid maximum height."""
        params = HandleParameters(2.6, 5.0)
        is_valid, errors = params.validate()
        assert is_valid, f"Expected valid, got errors: {errors}"

    def test_height_valid_mid(self):
        """Valid mid-range height."""
        params = HandleParameters(2.6, 2.5)
        is_valid, errors = params.validate()
        assert is_valid, f"Expected valid, got errors: {errors}"

    def test_height_below_min(self):
        """Height below minimum."""
        params = HandleParameters(2.6, 0.4)
        is_valid, errors = params.validate()
        assert not is_valid
        assert any("height must be between" in str(e) for e in errors)

    def test_height_above_max(self):
        """Height above maximum."""
        params = HandleParameters(2.6, 5.1)
        is_valid, errors = params.validate()
        assert not is_valid
        assert any("height must be between" in str(e) for e in errors)


class TestNonNumericInput:
    """Test non-numeric input rejection."""

    def test_diameter_string(self):
        """String diameter."""
        params = HandleParameters("2.6", 2.0)
        is_valid, errors = params.validate()
        assert not is_valid
        assert any("diameter must be a number" in str(e) for e in errors)

    def test_height_string(self):
        """String height."""
        params = HandleParameters(2.6, "2.0")
        is_valid, errors = params.validate()
        assert not is_valid
        assert any("height must be a number" in str(e) for e in errors)

    def test_diameter_none(self):
        """None diameter."""
        params = HandleParameters(None, 2.0)
        is_valid, errors = params.validate()
        assert not is_valid

    def test_height_none(self):
        """None height."""
        params = HandleParameters(2.6, None)
        is_valid, errors = params.validate()
        assert not is_valid


class TestErrorMessageFormatting:
    """Test error message formatting and clarity."""

    def test_error_message_includes_value(self):
        """Error message includes actual value."""
        params = HandleParameters(15.0, 2.0)
        is_valid, errors = params.validate()
        assert not is_valid
        assert any("15" in str(e) for e in errors), "Error should include invalid value"

    def test_error_message_includes_range(self):
        """Error message includes valid range."""
        params = HandleParameters(2.6, 10.0)
        is_valid, errors = params.validate()
        assert not is_valid
        assert any("0.5" in str(e) and "5.0" in str(e) for e in errors), "Error should show range"

    def test_multiple_errors(self):
        """Both diameter and height invalid."""
        params = HandleParameters(0.5, 10.0)
        is_valid, errors = params.validate()
        assert not is_valid
        assert len(errors) == 2, "Should report both errors"
