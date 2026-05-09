"""Handle parameter management and validation."""

import json
from pathlib import Path
from typing import Tuple


class HandleParameters:
    """Manage user parameters and locked reference parameters for handle generation."""

    # Reference parameters (locked, from Fusion 360 export)
    REFERENCE_PARAMS = {
        "d165": 0.30000000000000004,  # Fillet radius
        "d144": 0.6000000000000001,   # Wall thickness bottom layer
        "d145": 0.0,                  # Angle
        "d146": -0.010000000000000002,  # Draft angle compensation
        "d149": 0.2,                  # Surface offset tolerance
        "d176": 2.6,                  # Base diameter (reference)
        "d178": 3.3,                  # Upper diameter
        "d180": 1.6,                  # Transition radius
        "d183": 1.6,                  # Mounting interface width
        "d189": 1.7,                  # Core thickness
        "d191": 0.9424241430000001,   # Derived constraint
        "d192": 1.8848482860000002,   # Derived constraint
    }

    # User parameters (exposed via CLI)
    DIAMETER_MIN = 10.0
    DIAMETER_MAX = 30.0
    HEIGHT_MIN = 3.0
    HEIGHT_MAX = 30.0

    def __init__(self, diameter: float, height: float):
        """Initialize with user parameters."""
        self.diameter = diameter
        self.height = height
        self._errors = []

    def validate(self) -> Tuple[bool, list]:
        """Validate all parameters. Return (is_valid, error_messages)."""
        self._errors = []
        self._validate_diameter()
        self._validate_height()
        return len(self._errors) == 0, self._errors

    def _validate_diameter(self) -> None:
        """Validate diameter parameter."""
        if not isinstance(self.diameter, (int, float)):
            self._errors.append(f"diameter must be a number (got: {type(self.diameter).__name__})")
            return

        if self.diameter < self.DIAMETER_MIN or self.diameter > self.DIAMETER_MAX:
            self._errors.append(
                f"diameter must be between {self.DIAMETER_MIN} and {self.DIAMETER_MAX} mm (got: {self.diameter})"
            )

    def _validate_height(self) -> None:
        """Validate height parameter."""
        if not isinstance(self.height, (int, float)):
            self._errors.append(f"height must be a number (got: {type(self.height).__name__})")
            return

        if self.height < self.HEIGHT_MIN or self.height > self.HEIGHT_MAX:
            self._errors.append(
                f"height must be between {self.HEIGHT_MIN} and {self.HEIGHT_MAX} mm (got: {self.height})"
            )

    @staticmethod
    def load_from_json(json_path: Path) -> dict:
        """Load reference parameters from JSON file (for future extensibility)."""
        with open(json_path) as f:
            data = json.load(f)
        return {param["name"]: param["value"] for param in data.get("reference_parameters", [])}
