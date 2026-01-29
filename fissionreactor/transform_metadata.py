#!/usr/bin/env python3
"""
Metadata Transformation Tool

Transforms model.json (Fusion 360 export) + context.json (questionnaire) 
into 5 standardized AI-ready metadata files:
  - metadata.json (unified model info + design intent)
  - parameters.json (code generation ready)
  - constraints.json (design rules & validation)
  - features.json (feature timeline & dependencies)
  - assembly.json (component structure)

Usage:
    python transform_metadata.py <model_dir> [output_dir]
    
Example:
    python transform_metadata.py example-context/
    python transform_metadata.py example-context/ ./output/

The script expects model.json and context.json in the model_dir,
and creates/overwrites the 5 metadata files in the same directory
(or output_dir if specified).
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class MetadataTransformer:
    """Transforms model.json + context.json into 5 metadata files."""
    
    def __init__(self, model_json: Dict[str, Any], context_json: Dict[str, Any]):
        """Initialize transformer with model and context data."""
        self.model = model_json
        self.context = context_json
        self.model_name = context_json.get('context_metadata', {}).get('model_name', 'Unknown')
        self.generated_date = datetime.now().isoformat()
    
    def transform_all(self) -> Dict[str, Dict[str, Any]]:
        """Generate all 5 metadata files."""
        return {
            'metadata.json': self.transform_metadata(),
            'parameters.json': self.transform_parameters(),
            'constraints.json': self.transform_constraints(),
            'features.json': self.transform_features(),
            'assembly.json': self.transform_assembly()
        }
    
    def transform_metadata(self) -> Dict[str, Any]:
        """Generate metadata.json - unified model info + design intent."""
        context_meta = self.context.get('context_metadata', {})
        export_meta = self.model.get('export_metadata', {})
        purpose = self.context.get('purpose', {})
        design_intent = self.context.get('design_intent', {})
        materials = self.context.get('materials', {})
        metadata_section = self.context.get('metadata', {})
        
        critical_features = []
        for feature_desc in [design_intent.get('intent_critical_features', '')]:
            if feature_desc:
                critical_features.append({
                    'name': 'Critical Features',
                    'description': feature_desc,
                    'reason': 'Core functionality'
                })
        
        design_decisions = []
        for decision_desc in [design_intent.get('intent_design_decisions', '')]:
            if decision_desc:
                design_decisions.append({
                    'decision': 'Design Optimization',
                    'rationale': decision_desc
                })
        
        return {
            'metadata': {
                'version': '1.0',
                'schema_version': '1.0',
                'generated_date': self.generated_date,
                'source_model': self.model_name,
                'source_export': 'model.json',
                'source_context': 'context.json'
            },
            'model_info': {
                'name': self.model_name,
                'version': metadata_section.get('meta_version', '1.0'),
                'author': metadata_section.get('meta_author', 'Unknown'),
                'created_date': metadata_section.get('meta_date', export_meta.get('exported_date', '')),
                'purpose': purpose.get('purpose_primary', 'Unknown'),
                'description': purpose.get('purpose_use_case', ''),
                'assembly_context': purpose.get('purpose_context', ''),
                'part_count': self.model.get('model', {}).get('part_count', 1),
                'assembly_type': 'single_component' if self.model.get('model', {}).get('part_count', 1) == 1 else 'assembly'
            },
            'design_intent': {
                'critical_features': critical_features if critical_features else [{'name': 'All Features', 'description': 'Design functionality'}],
                'design_decisions': design_decisions if design_decisions else [{'decision': 'Default Design'}],
                'aesthetic_requirements': design_intent.get('intent_aesthetic', ''),
                'load_requirements': purpose.get('purpose_use_case', '')
            },
            'materials': {
                'material_type': materials.get('material_type', 'Unknown'),
                'fabrication_method': materials.get('material_fabrication', 'Unknown'),
                'material_considerations': materials.get('material_considerations', ''),
                'post_processing': materials.get('material_finish', '')
            },
            'variations': {
                'planned_variants': self.context.get('variations', {}).get('var_planned', ''),
                'variant_examples': self.context.get('variations', {}).get('var_examples', ''),
                'variable_parameters': self.context.get('variations', {}).get('var_parameters', '')
            }
        }
    
    def transform_parameters(self) -> Dict[str, Any]:
        """Generate parameters.json - code generation ready."""
        model_params = self.model.get('parameters', [])
        param_context = self.context.get('parameters', {})
        
        parameters = {}
        for param in model_params:
            param_name = param.get('name', '')
            param_type = param.get('type', 'length')
            param_unit = param.get('unit', 'mm')
            
            # Handle value safely
            param_value = param.get('value', 0)
            try:
                param_value = float(param_value) if param_value is not None else 0
            except (TypeError, ValueError):
                param_value = 0
            
            # Handle min/max safely - may contain formulas
            param_min = param.get('min', 0)
            param_max = param.get('max', param_value)
            
            try:
                param_min = float(param_min) if param_min is not None else 0
            except (TypeError, ValueError):
                param_min = 0
            
            try:
                param_max = float(param_max) if param_max is not None else param_value
            except (TypeError, ValueError):
                # If max is a formula string, use a default range
                param_max = param_value * 2 if param_value else 100
            
            # Determine if parameter is fixed
            is_fixed = param_min >= param_max
            
            cli_arg = None
            if not is_fixed:
                cli_arg = '--' + param_name[0].lower() + param_name[1:].replace('_', '-').lower()
            
            step = param.get('step')
            if step is None:
                step = None if is_fixed else 1
            
            parameters[param_name] = {
                'type': param_type,
                'unit': param_unit,
                'default': param_value,
                'min': param_min,
                'max': param_max,
                'step': step,
                'cli_arg': cli_arg,
                'cli_help': f'{param_name} in {param_unit}' if cli_arg else None,
                'code_type': 'float' if param_type == 'length' else 'int',
                'fixed': is_fixed,
                'comment': param.get('note', '')
            }
        
        derived_parameters = []
        if 'param_relationships' in param_context:
            relationships = param_context['param_relationships']
            if relationships:
                derived_parameters.append({
                    'name': 'Derived Parameters',
                    'formula': relationships,
                    'note': 'Automatically calculated from primary parameters'
                })
        
        return {
            'parameters_for_code_generation': {
                'version': '1.0',
                'generated_date': self.generated_date,
                'model_name': self.model_name,
                'description': 'Code-generation-ready parameter definitions',
                'parameters': parameters,
                'derived_parameters': derived_parameters if derived_parameters else [],
                'scaling_strategy': self.context.get('parameters', {}).get('param_scaling', 'Proportional scaling')
            }
        }
    
    def transform_constraints(self) -> Dict[str, Any]:
        """Generate constraints.json - design rules & validation."""
        constraints_context = self.context.get('constraints', {})
        
        constraint_categories = {
            'tolerance_constraints': {
                'category': 'Manufacturing & Fit Tolerances',
                'priority': 'CRITICAL',
                'source': 'Design specifications',
                'constraints': []
            },
            'structural_constraints': {
                'category': 'Load & Strength Requirements',
                'priority': 'CRITICAL',
                'source': 'Design intent - load-bearing functionality',
                'constraints': []
            },
            'geometric_constraints': {
                'category': 'Geometric & Dimensional Rules',
                'priority': 'HIGH',
                'source': 'Design requirements',
                'constraints': []
            },
            'material_constraints': {
                'category': 'Material & Fabrication Rules',
                'priority': 'HIGH',
                'source': 'Fabrication process',
                'constraints': []
            },
            'parameter_constraints': {
                'category': 'Parameter Relationships & Dependencies',
                'priority': 'MEDIUM',
                'source': 'Design logic',
                'constraints': []
            }
        }
        
        if constraints_context.get('constraint_tolerances'):
            constraint_categories['tolerance_constraints']['constraints'].append({
                'name': 'Tolerance specification',
                'description': constraints_context['constraint_tolerances'],
                'severity': 'CRITICAL'
            })
        
        if constraints_context.get('constraint_minimum'):
            constraint_categories['structural_constraints']['constraints'].append({
                'name': 'Minimum dimensions',
                'description': constraints_context['constraint_minimum'],
                'severity': 'CRITICAL'
            })
        
        if constraints_context.get('constraint_rules'):
            constraint_categories['geometric_constraints']['constraints'].append({
                'name': 'Design rules',
                'description': constraints_context['constraint_rules'],
                'severity': 'HIGH'
            })
        
        if constraints_context.get('constraint_dependencies'):
            constraint_categories['parameter_constraints']['constraints'].append({
                'name': 'Parameter dependencies',
                'description': constraints_context['constraint_dependencies'],
                'severity': 'MEDIUM'
            })
        
        materials = self.context.get('materials', {})
        if materials.get('material_considerations'):
            constraint_categories['material_constraints']['constraints'].append({
                'name': 'Material-specific rules',
                'description': materials['material_considerations'],
                'severity': 'HIGH'
            })
        
        return {
            'constraints_for_code_generation': {
                'version': '1.0',
                'generated_date': self.generated_date,
                'model_name': self.model_name,
                'description': 'Design constraints and validation rules',
                'constraint_categories': constraint_categories
            }
        }
    
    def transform_features(self) -> Dict[str, Any]:
        """Generate features.json - feature timeline & dependencies."""
        model_params = self.model.get('parameters', [])
        design_intent = self.context.get('design_intent', {})
        
        features = []
        if 'features' in self.model and isinstance(self.model['features'], list):
            features = self.model['features']
        elif 'features' in self.model and isinstance(self.model['features'], dict):
            features = self.model['features'].get('features', [])
        
        critical_features_text = design_intent.get('intent_critical_features', '')
        critical_feature_names = []
        if critical_features_text:
            critical_feature_names = [line.strip() for line in critical_features_text.split('\n') if line.strip()]
        
        feature_sequence = []
        for idx, feature in enumerate(features):
            feature_name = feature.get('name', f'Feature_{idx}')
            feature_type = feature.get('type', 'Unknown')
            
            is_critical = any(crit.lower() in feature_name.lower() for crit in critical_feature_names)
            
            feature_sequence.append({
                'index': idx,
                'name': feature_name,
                'type': feature_type,
                'parent': feature.get('parent', 'root'),
                'critical': is_critical,
                'preservable': True
            })
        
        return {
            'features': {
                'version': '1.0',
                'generated_date': self.generated_date,
                'model_name': self.model_name,
                'description': 'Feature timeline and dependencies',
                'feature_count': len(feature_sequence),
                'feature_sequence': feature_sequence,
                'critical_features': [f['name'] for f in feature_sequence if f['critical']],
                'guidelines': {
                    'preserve': [f['name'] for f in feature_sequence if f['critical']],
                    'order_matters': True,
                    'construction_method': 'Timeline order from Fusion 360'
                }
            }
        }
    
    def transform_assembly(self) -> Dict[str, Any]:
        """Generate assembly.json - component structure."""
        assembly_context = self.context.get('assembly', {})
        
        components = []
        if 'components' in self.model and isinstance(self.model['components'], list):
            components = self.model['components']
        elif 'components' in self.model and isinstance(self.model['components'], dict):
            components = self.model['components'].get('components', [])
        
        assembly_components = []
        for comp in components:
            assembly_components.append({
                'name': comp.get('name', 'Unknown'),
                'parent': comp.get('parent', 'root'),
                'feature_count': comp.get('feature_count', 0),
                'sketch_count': comp.get('sketch_count', 0)
            })
        
        fasteners = []
        if assembly_context.get('assembly_fasteners'):
            fasteners.append({
                'description': assembly_context['assembly_fasteners'],
                'type': 'specified'
            })
        
        return {
            'assembly': {
                'version': '1.0',
                'generated_date': self.generated_date,
                'model_name': self.model_name,
                'description': 'Assembly structure and component hierarchy',
                'structure': {
                    'part_count': len(assembly_components),
                    'assembly_type': 'single_component' if len(assembly_components) <= 1 else 'multi_component',
                    'description': assembly_context.get('assembly_structure', 'Single component model')
                },
                'components': assembly_components,
                'assembly_process': {
                    'instructions': assembly_context.get('assembly_instructions', ''),
                    'difficulty': assembly_context.get('assembly_difficulty', 'Not specified'),
                    'required_tools': []
                },
                'fasteners': fasteners if fasteners else [],
                'sub_assemblies': []
            }
        }


def load_json(file_path: Path) -> Dict[str, Any]:
    """Load and validate JSON file."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {file_path}: {str(e)}")


def save_json(data: Dict[str, Any], file_path: Path) -> None:
    """Save data to JSON file with pretty formatting."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    model_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else model_dir
    
    if not model_dir.is_dir():
        print(f"Error: Directory not found: {model_dir}")
        sys.exit(1)
    
    model_file = model_dir / 'model.json'
    context_file = model_dir / 'context.json'
    
    if not model_file.exists() or not context_file.exists():
        print(f"Error: Missing required files:")
        print(f"  - {model_file.exists() and 'OK' or 'MISSING'}: {model_file}")
        print(f"  - {context_file.exists() and 'OK' or 'MISSING'}: {context_file}")
        sys.exit(1)
    
    try:
        print(f"Loading model.json...")
        model_json = load_json(model_file)
        
        print(f"Loading context.json...")
        context_json = load_json(context_file)
        
        print(f"Transforming metadata...")
        transformer = MetadataTransformer(model_json, context_json)
        metadata_files = transformer.transform_all()
        
        print(f"\nGenerating metadata files in {output_dir}:")
        for filename, data in metadata_files.items():
            output_file = output_dir / filename
            save_json(data, output_file)
            size_kb = output_file.stat().st_size / 1024
            print(f"  ✓ {filename:20s} ({size_kb:6.1f} KB)")
        
        print(f"\n✅ Transformation complete!")
        print(f"\nGenerated files:")
        print(f"  - metadata.json:    Model info + design intent")
        print(f"  - parameters.json:  Code generation ready")
        print(f"  - constraints.json: Design rules & validation")
        print(f"  - features.json:    Feature timeline")
        print(f"  - assembly.json:    Component structure")
        print(f"\nPackage is now AI-ready for code generation.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
