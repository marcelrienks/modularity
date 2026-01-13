"""Tulorg Generator Core Package"""

__version__ = "1.0.0"

from .parameters import Parameters
from .layout_calculator import LayoutCalculator
from .assembly_guide import AssemblyGuideGenerator

# Import builder only if cadquery is available
try:
    from .builder import ModelBuilder
    __all__ = ['Parameters', 'LayoutCalculator', 'ModelBuilder', 'AssemblyGuideGenerator']
except ImportError:
    __all__ = ['Parameters', 'LayoutCalculator', 'AssemblyGuideGenerator']
