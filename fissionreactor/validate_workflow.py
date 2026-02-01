#!/usr/bin/env python3
"""
Validation Framework for fissionreactor Workflow

Validates all stages of the CAD parameterization workflow:
  1. Design Export (model.json) - Structure and required fields
  2. Questionnaire (context.json) - Completeness and correctness
  3. Metadata Transformation - Generated file validity
  4. Code Generation - Output format and usability

Usage:
    python validate_workflow.py <model_dir>
    python validate_workflow.py example-context/

Returns:
    0 - All validations passed
    1 - Validation failures detected (see report)
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any


class ValidationReport:
    """Tracks validation results."""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passed: List[str] = []
    
    def add_error(self, category: str, message: str) -> None:
        """Add validation error."""
        self.errors.append(f"❌ {category}: {message}")
    
    def add_warning(self, category: str, message: str) -> None:
        """Add validation warning."""
        self.warnings.append(f"⚠️  {category}: {message}")
    
    def add_pass(self, category: str, message: str) -> None:
        """Add successful validation."""
        self.passed.append(f"✓ {category}: {message}")
    
    def has_failures(self) -> bool:
        """Check if validation has failures."""
        return len(self.errors) > 0
    
    def print_report(self) -> None:
        """Print formatted validation report."""
        print("\n" + "="*70)
        print("VALIDATION REPORT")
        print("="*70)
        
        if self.passed:
            print("\n✓ PASSED:")
            for msg in self.passed:
                print(f"  {msg}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for msg in self.warnings:
                print(f"  {msg}")
        
        if self.errors:
            print("\n❌ ERRORS:")
            for msg in self.errors:
                print(f"  {msg}")
        
        print("\n" + "="*70)
        if self.has_failures():
            print(f"RESULT: FAILED ({len(self.errors)} errors, {len(self.warnings)} warnings)")
        else:
            print(f"RESULT: PASSED ({len(self.passed)} checks)")
        print("="*70 + "\n")


class ModelValidator:
    """Validates design export (model.json).
    
    Standard structure (canonical):
    {
      "export_metadata": {...},      # Export context
      "model": {                      # Model summary
        "name": str,
        "part_count": int,
        "feature_count": int
      },
      "parameters": [...],            # Top-level parameter array
      "features": [...],              # Top-level feature array
      "components": [...],            # Top-level components array
      "sketches": [...],              # Optional: sketch data
      "timeline": [...]               # Optional: feature timeline
    }
    """
    
    REQUIRED_FIELDS = {
        'export_metadata': {
            'exported_date': str,
            'fusion360_version': str,
        },
        'model': {
            'name': str,
            'part_count': int,
        },
        'parameters': list,
        'features': list,
    }
    
    def __init__(self, model_data: Dict[str, Any]):
        self.data = model_data
    
    def validate(self, report: ValidationReport) -> bool:
        """Validate model.json structure and content."""
        print("Validating model.json...")
        
        if not self.data:
            report.add_error("model.json", "File is empty")
            return False
        
        # Check required top-level fields
        for field, field_type in self.REQUIRED_FIELDS.items():
            if field not in self.data:
                report.add_error("model.json", f"Missing required field: {field}")
                continue
            
            if isinstance(field_type, dict):
                # Nested validation
                if not isinstance(self.data[field], dict):
                    report.add_error("model.json", f"{field} must be an object")
                    continue
                
                for subfield, subtype in field_type.items():
                    if subfield not in self.data[field]:
                        report.add_warning("model.json", f"Missing field: {field}.{subfield}")
        
        # Validate parameters (now at top-level)
        if 'parameters' in self.data:
            params = self.data['parameters']
            if not isinstance(params, list):
                report.add_error("model.json", "parameters must be an array")
            elif len(params) == 0:
                report.add_warning("model.json", "No parameters found (model may not be parameterized)")
            else:
                report.add_pass("model.json", f"Found {len(params)} parameters")
        
        # Validate features (now at top-level)
        if 'features' in self.data:
            features = self.data['features']
            if not isinstance(features, list):
                report.add_error("model.json", "features must be an array")
            elif len(features) == 0:
                report.add_warning("model.json", "No features found")
            else:
                report.add_pass("model.json", f"Found {len(features)} features")
        
        # Validate bodies
        if 'model' in self.data and 'bodies' in self.data['model']:
            bodies = self.data['model']['bodies']
            if not isinstance(bodies, list):
                report.add_error("model.json", "bodies must be an array")
            elif len(bodies) == 0:
                report.add_warning("model.json", "No bodies found (empty model)")
            else:
                report.add_pass("model.json", f"Found {len(bodies)} bodies")
        
        return not report.has_failures()


class QuestionnaireValidator:
    """Validates questionnaire response (context.json)."""
    
    REQUIRED_SECTIONS = [
        'context_metadata',
        'purpose',
        'design_intent',
        'materials',
        'metadata'
    ]
    
    REQUIRED_METADATA_FIELDS = {
        'context_metadata': ['model_name', 'questionnaire_date'],
        'purpose': ['purpose_primary', 'purpose_use_case'],
        'design_intent': ['intent_critical_features', 'intent_design_decisions'],
        'materials': ['material_primary'],
        'metadata': ['meta_version', 'meta_author']
    }
    
    def __init__(self, context_data: Dict[str, Any]):
        self.data = context_data
    
    def validate(self, report: ValidationReport) -> bool:
        """Validate context.json completeness."""
        print("Validating context.json...")
        
        if not self.data:
            report.add_error("context.json", "File is empty")
            return False
        
        # Check for required sections
        missing_sections = []
        for section in self.REQUIRED_SECTIONS:
            if section not in self.data:
                missing_sections.append(section)
                report.add_error("context.json", f"Missing required section: {section}")
        
        # Check required fields in each section
        for section, fields in self.REQUIRED_METADATA_FIELDS.items():
            if section in self.data:
                section_data = self.data[section]
                if not isinstance(section_data, dict):
                    report.add_error("context.json", f"{section} must be an object")
                    continue
                
                for field in fields:
                    if field not in section_data:
                        report.add_warning("context.json", f"Missing field: {section}.{field}")
                    elif not section_data[field]:
                        report.add_warning("context.json", f"Empty field: {section}.{field}")
        
        if not missing_sections:
            report.add_pass("context.json", "All required sections present")
        
        return not report.has_failures()


class MetadataFileValidator:
    """Validates generated metadata files."""
    
    EXPECTED_FILES = {
        'metadata.json': {
            'required_keys': ['metadata', 'model_info', 'design_intent'],
            'description': 'Unified model info and design intent'
        },
        'parameters.json': {
            'required_keys': ['parameters_for_code_generation'],
            'description': 'Code generation ready parameters'
        },
        'constraints.json': {
            'required_keys': ['constraints_for_code_generation'],
            'description': 'Design rules and validation'
        },
        'features.json': {
            'required_keys': ['features'],
            'description': 'Feature timeline and dependencies',
            'optional': True
        },
        'assembly.json': {
            'required_keys': ['assembly'],
            'description': 'Component structure',
            'optional': True
        }
    }
    
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
    
    def validate(self, report: ValidationReport) -> bool:
        """Validate all generated metadata files."""
        print("Validating metadata files...")
        
        for filename, spec in self.EXPECTED_FILES.items():
            filepath = Path(self.base_dir) / filename
            is_optional = spec.get('optional', False)
            
            if not filepath.exists():
                if is_optional:
                    report.add_pass("Metadata files", f"Optional file not present: {filename}")
                else:
                    report.add_warning("Metadata files", f"Missing: {filename}")
                continue
            
            try:
                with open(filepath) as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                report.add_error("Metadata files", f"{filename}: Invalid JSON - {e}")
                continue
            except Exception as e:
                report.add_error("Metadata files", f"{filename}: {e}")
                continue
            
            # Check required keys
            missing_keys = []
            for key in spec['required_keys']:
                if key not in data:
                    missing_keys.append(key)
            
            if missing_keys:
                report.add_warning("Metadata files", 
                    f"{filename}: Missing keys {missing_keys}")
            else:
                report.add_pass("Metadata files", 
                    f"{filename} - {spec['description']}")
        
        return not report.has_failures()


class CodeGenerationValidator:
    """Validates code generation output format."""
    
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
    
    def validate(self, report: ValidationReport) -> bool:
        """Validate code generation readiness."""
        print("Validating code generation readiness...")
        
        # Check for example generator script
        generator_path = Path(self.base_dir) / 'generator-guide' / 'template_generator.py'
        
        if not generator_path.exists():
            report.add_warning("Code generation", 
                "Generator guide not found (optional)")
        else:
            try:
                with open(generator_path) as f:
                    content = f.read()
                    if 'def' in content and 'class' in content:
                        report.add_pass("Code generation", 
                            "Generator template structure valid")
                    else:
                        report.add_warning("Code generation", 
                            "Generator template may be incomplete")
            except Exception as e:
                report.add_warning("Code generation", str(e))
        
        return not report.has_failures()


class WorkflowValidator:
    """Main validator orchestrating all checks."""
    
    def __init__(self, model_dir: str):
        self.model_dir = Path(model_dir)
        self.report = ValidationReport()
    
    def load_json(self, filename: str) -> Tuple[bool, Dict[str, Any]]:
        """Load and parse JSON file."""
        filepath = self.model_dir / filename
        
        if not filepath.exists():
            self.report.add_error("File I/O", f"File not found: {filename}")
            return False, {}
        
        try:
            with open(filepath) as f:
                return True, json.load(f)
        except json.JSONDecodeError as e:
            self.report.add_error("File I/O", f"{filename}: Invalid JSON - {e}")
            return False, {}
        except Exception as e:
            self.report.add_error("File I/O", f"{filename}: {e}")
            return False, {}
    
    def validate(self) -> bool:
        """Run complete validation workflow."""
        print(f"\n🔍 Starting validation for: {self.model_dir}\n")
        
        # Validate model.json
        success, model_data = self.load_json('model.json')
        if success:
            ModelValidator(model_data).validate(self.report)
        
        # Validate context.json
        success, context_data = self.load_json('context.json')
        if success:
            QuestionnaireValidator(context_data).validate(self.report)
        
        # Validate generated metadata files
        MetadataFileValidator(str(self.model_dir)).validate(self.report)
        
        # Validate code generation readiness
        CodeGenerationValidator(str(self.model_dir.parent)).validate(self.report)
        
        # Print report
        self.report.print_report()
        
        return not self.report.has_failures()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    model_dir = sys.argv[1]
    
    validator = WorkflowValidator(model_dir)
    success = validator.validate()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
