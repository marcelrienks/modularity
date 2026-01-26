#!/usr/bin/env python3
"""
Fusion 360 Model Export Script - Unified CLI & Add-In Version

Dual-mode script that works both as:
1. Command-line tool (when run standalone)
2. Fusion 360 Add-In (when run from Scripts panel)

CLI Usage:
    python export_fusion360_data.py <f3d_file_path> [model_name]

Add-In Usage:
    Run from Fusion 360 Tools > Add-ins > Scripts and Add-ins > Scripts > Right-click > Run

Examples:
    python export_fusion360_data.py "/path/to/model.f3d"           # CLI: Export all models
    python export_fusion360_data.py "/path/to/model.f3d" handles   # CLI: Export specific model
    (Run from Fusion UI for interactive Add-In mode)
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

try:
    import adsk.core
    import adsk.fusion
    FUSION_API_AVAILABLE = True
except ImportError:
    FUSION_API_AVAILABLE = False


class FusionExporter:
    """Exports complete design data from Fusion 360 .f3d files."""
    
    def __init__(self, f3d_path=None, model_name=None, ui=None):
        """
        Initialize exporter.
        
        Args:
            f3d_path: Full path to .f3d file (CLI mode). None for Add-In mode.
            model_name: Optional specific model/body name to export.
            ui: Fusion UI object (for Add-In mode dialogs).
        """
        self.f3d_path = Path(f3d_path) if f3d_path else None
        self.model_name = model_name
        self.ui = ui
        self.mode = "addon" if ui else "cli"
        self.script_dir = Path(__file__).parent
        self.design = None
        self.models_exported = []
    
    def log(self, message, is_error=False):
        """Log message (UI dialog for Add-In, print for CLI)."""
        if self.mode == "addon" and self.ui:
            self.ui.messageBox(message)
        else:
            if is_error:
                print(f"✗ {message}")
            else:
                print(message)
    
    def validate_inputs(self):
        """Validate f3d file exists and is accessible (CLI mode only)."""
        if self.mode == "cli":
            if not self.f3d_path.exists():
                raise FileNotFoundError(f"F3D file not found: {self.f3d_path}")
            if not self.f3d_path.suffix.lower() == '.f3d':
                raise ValueError(f"File must be .f3d format, got: {self.f3d_path.suffix}")
            print(f"✓ F3D file found: {self.f3d_path}")
    
    def load_design(self):
        """Load Fusion 360 design from f3d file."""
        if not FUSION_API_AVAILABLE:
            raise RuntimeError("Fusion 360 API not available")
        
        try:
            if self.mode == "cli":
                # CLI mode: Open f3d file
                app = adsk.core.Application.get()
                documents = app.documents
                doc = documents.open(str(self.f3d_path), False)
                self.design = adsk.fusion.Design.cast(doc.product)
            else:
                # Add-In mode: Get active design
                app = adsk.core.Application.get()
                product = app.activeProduct
                if not product:
                    raise ValueError("No active document")
                self.design = adsk.fusion.Design.cast(product)
                self.f3d_path = Path(self.design.parentDocument.filePath) if self.design.parentDocument else None
            
            if not self.design:
                raise ValueError("Document is not a Fusion 360 design")
            
            if self.mode == "cli":
                print(f"✓ Design loaded: {self.design.name}")
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to load design: {str(e)}")
    
    def get_all_components(self):
        """Get all top-level components (bodies/models) in design."""
        components = []
        try:
            for component in self.design.rootComponent.childComponents:
                components.append(component)
            
            # Include root component if it has features
            if self.design.rootComponent.features.count > 0:
                components.append(self.design.rootComponent)
            
            return components
        except Exception as e:
            if self.mode == "cli":
                print(f"Warning: Error retrieving components: {str(e)}")
            return []
    
    def extract_user_parameters(self):
        """Extract all user-defined parameters from design."""
        user_params = []
        try:
            for param in self.design.userParameters:
                user_params.append({
                    'name': param.name,
                    'value': param.value,
                    'unit': param.unit,
                    'comment': param.comment if param.comment else '',
                    'type': 'user_parameter'
                })
        except Exception as e:
            if self.mode == "cli":
                print(f"Warning: Error extracting user parameters: {str(e)}")
        return user_params
    
    def extract_reference_parameters(self):
        """Extract all derived/reference parameters."""
        ref_params = []
        try:
            for param in self.design.allParameters:
                if param not in self.design.userParameters:
                    ref_params.append({
                        'name': param.name,
                        'value': param.value,
                        'unit': param.unit,
                        'comment': param.comment if param.comment else '',
                        'type': 'reference_parameter'
                    })
        except Exception as e:
            if self.mode == "cli":
                print(f"Warning: Error extracting reference parameters: {str(e)}")
        return ref_params
    
    def extract_timeline(self):
        """Extract feature timeline/history."""
        timeline_list = []
        try:
            timeline = self.design.timeline
            for i in range(timeline.count):
                event = timeline.item(i)
                timeline_list.append({
                    'index': i,
                    'name': event.name,
                    'feature_type': type(event).__name__,
                    'is_suppressed': event.isSuppressed
                })
        except Exception as e:
            if self.mode == "cli":
                print(f"Warning: Error extracting timeline: {str(e)}")
        return timeline_list
    
    def extract_sketches(self, component):
        """Extract sketches from a component."""
        sketches = []
        try:
            for sketch in component.sketches:
                constraints = []
                try:
                    for constraint in sketch.geometricConstraints:
                        constraints.append({
                            'type': type(constraint).__name__,
                            'name': constraint.name if hasattr(constraint, 'name') else ''
                        })
                except:
                    pass
                
                sketch_entry = {
                    'name': sketch.name,
                    'parent': component.name,
                    'geometry_count': (
                        sketch.sketchCurves.sketchLines.count +
                        sketch.sketchCurves.sketchCircles.count +
                        sketch.sketchCurves.sketchArcs.count
                    ),
                    'profile_count': sketch.profiles.count,
                    'is_visible': sketch.isVisible,
                    'constraints_count': len(constraints)
                }
                sketches.append(sketch_entry)
        except Exception as e:
            if self.mode == "cli":
                print(f"Warning: Error extracting sketches from {component.name}: {str(e)}")
        return sketches
    
    def extract_features(self, component):
        """Extract all features from a component."""
        features = []
        feature_types = [
            ('extrusions', 'Extrude'),
            ('holes', 'Hole'),
            ('shells', 'Shell'),
            ('mirrors', 'Mirror'),
            ('chamfers', 'Chamfer'),
            ('fillets', 'Fillet'),
            ('patterns', 'Pattern'),
            ('threads', 'Thread')
        ]
        
        try:
            for attr_name, feature_type in feature_types:
                try:
                    feature_collection = getattr(component.features, attr_name)
                    for feature in feature_collection:
                        features.append({
                            'type': feature_type,
                            'name': feature.name,
                            'parent': component.name
                        })
                except:
                    pass
        except Exception as e:
            if self.mode == "cli":
                print(f"Warning: Error extracting features from {component.name}: {str(e)}")
        return features
    
    def extract_components(self):
        """Extract component tree structure."""
        components_list = []
        
        def process_components(component, parent_name="root"):
            comp_entry = {
                'name': component.name,
                'parent': parent_name,
                'feature_count': sum([
                    component.features.extrusions.count,
                    component.features.holes.count,
                    component.features.shells.count,
                    component.features.mirrors.count,
                    component.features.chamfers.count,
                    component.features.fillets.count,
                    component.features.patterns.count if hasattr(component.features, 'patterns') else 0,
                    component.features.threads.count if hasattr(component.features, 'threads') else 0
                ]),
                'sketch_count': component.sketches.count
            }
            components_list.append(comp_entry)
            
            # Process child components
            for child in component.childComponents:
                process_components(child, component.name)
        
        try:
            process_components(self.design.rootComponent)
        except Exception as e:
            if self.mode == "cli":
                print(f"Warning: Error extracting components: {str(e)}")
        
        return components_list
    
    def export_model(self, component):
        """Export complete data for a single model/component."""
        model_name = component.name
        
        if self.mode == "cli":
            print(f"  Extracting data for: {model_name}")
        
        # Extract all data
        user_params = self.extract_user_parameters()
        ref_params = self.extract_reference_parameters()
        timeline = self.extract_timeline()
        sketches = self.extract_sketches(component)
        features = self.extract_features(component)
        components = self.extract_components()
        
        # Build export data structure
        export_data = {
            'export_metadata': {
                'exported_date': datetime.now().isoformat(),
                'fusion_360_api': 'Autodesk Fusion 360 API',
                'model_name': model_name,
                'source_f3d': str(self.f3d_path) if self.f3d_path else 'Unknown',
                'document_path': self.design.parentDocument.filePath if self.design.parentDocument else 'Unknown'
            },
            'user_parameters': user_params,
            'reference_parameters': ref_params,
            'timeline': {
                'total_events': len(timeline),
                'events': timeline
            },
            'sketches': {
                'total_count': len(sketches),
                'sketches': sketches
            },
            'features': {
                'total_count': len(features),
                'features': features
            },
            'components': {
                'total_count': len(components),
                'components': components
            },
            'summary': {
                'user_parameters_count': len(user_params),
                'reference_parameters_count': len(ref_params),
                'timeline_events_count': len(timeline),
                'sketches_count': len(sketches),
                'features_count': len(features),
                'components_count': len(components)
            }
        }
        
        # Create output directories: model_name/origin/
        model_dir = self.script_dir / model_name
        output_dir = model_dir / "origin"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Write JSON file
        output_file = output_dir / f"{model_name}.json"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            if self.mode == "cli":
                print(f"  ✓ Exported to: {output_file}")
            
            self.models_exported.append({
                'name': model_name,
                'path': str(output_file),
                'parameters': len(user_params),
                'sketches': len(sketches),
                'features': len(features)
            })
            return True
        except Exception as e:
            if self.mode == "cli":
                print(f"  ✗ Error saving export: {str(e)}")
            else:
                self.log(f"Error saving export: {str(e)}", is_error=True)
            return False
    
    def run(self):
        """Execute export process."""
        try:
            if self.mode == "cli":
                print("=" * 60)
                print("Fusion 360 Model Export - CLI")
                print("=" * 60)
            
            # Validate inputs
            self.validate_inputs()
            
            # Load design
            self.load_design()
            
            if self.model_name:
                # Export specific model
                if self.mode == "cli":
                    print(f"\nExporting specific model: {self.model_name}")
                
                found = False
                for component in self.get_all_components():
                    if component.name == self.model_name:
                        self.export_model(component)
                        found = True
                        break
                
                if not found:
                    msg = f"Model '{self.model_name}' not found in design"
                    if self.mode == "cli":
                        print(f"✗ {msg}")
                    else:
                        self.log(msg, is_error=True)
                    return False
            else:
                # Export all models
                if self.mode == "cli":
                    print("\nExporting all models from design...")
                
                components = self.get_all_components()
                if not components:
                    msg = "No models/components found in design"
                    if self.mode == "cli":
                        print(f"✗ {msg}")
                    else:
                        self.log(msg, is_error=True)
                    return False
                
                for component in components:
                    self.export_model(component)
            
            # Summary
            self.print_summary()
            return True
        
        except Exception as e:
            msg = f"Error: {str(e)}"
            if self.mode == "cli":
                print(f"\n✗ {msg}")
            else:
                self.log(msg, is_error=True)
            return False
    
    def print_summary(self):
        """Print export summary."""
        if self.mode == "addon":
            # For Add-In: show in dialog
            if not self.models_exported:
                self.log("No models exported.")
                return
            
            summary = "Export Complete!\n\n"
            summary += f"Models exported: {len(self.models_exported)}\n\n"
            for model in self.models_exported:
                summary += f"• {model['name']}.json\n"
                summary += f"  Path: {model['path']}\n"
                summary += f"  Parameters: {model['parameters']}\n"
                summary += f"  Sketches: {model['sketches']}\n"
                summary += f"  Features: {model['features']}\n\n"
            self.log(summary)
        else:
            # For CLI: print to console
            print("\n" + "=" * 60)
            print("EXPORT SUMMARY")
            print("=" * 60)
            
            if not self.models_exported:
                print("No models exported.")
                return
            
            print(f"Models exported: {len(self.models_exported)}\n")
            for model in self.models_exported:
                print(f"  {model['name']}.json")
                print(f"    Path: {model['path']}")
                print(f"    Parameters: {model['parameters']}")
                print(f"    Sketches: {model['sketches']}")
                print(f"    Features: {model['features']}")
                print()
            
            print("=" * 60)


def run(context):
    """Entry point for Fusion 360 Add-In mode."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Get output directory from user
        dlg = ui.createFolderDialog()
        dlg.title = 'Select directory to save Fusion 360 export'
        if dlg.showDialog() != adsk.core.DialogResults.OKResult:
            ui.messageBox('Export cancelled.')
            return
        
        # Create exporter in Add-In mode
        exporter = FusionExporter(f3d_path=None, model_name=None, ui=ui)
        exporter.script_dir = Path(dlg.folder)
        exporter.run()
        
    except Exception as ex:
        if ui:
            ui.messageBox(f'Error: {str(ex)}')


def main():
    """Main entry point for CLI mode."""
    if len(sys.argv) < 2:
        print("Fusion 360 Model Export - CLI & Add-In")
        print("\nCLI Usage:")
        print("  python export_fusion360_data.py <f3d_file_path> [model_name]")
        print("\nExamples:")
        print("  python export_fusion360_data.py '/path/to/model.f3d'")
        print("  python export_fusion360_data.py '/path/to/model.f3d' handles")
        print("\nAdd-In Mode:")
        print("  Run from Fusion 360: Tools > Add-ins > Scripts and Add-ins > Scripts > Right-click > Run")
        sys.exit(1)
    
    f3d_path = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    exporter = FusionExporter(f3d_path, model_name)
    success = exporter.run()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
