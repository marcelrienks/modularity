#!/usr/bin/env python3
"""
Fusion 360 Model Export Add-In

Fusion 360 Add-In script that exports complete design data from the active model.

Add-In Usage:
    1. Open a .f3d design file in Fusion 360
    2. Go to Tools > Add-ins > Scripts and Add-ins > Scripts tab
    3. Right-click this script > Run
    4. Select output directory for exported JSON files
    5. Exports automatically using the project name
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
    
    def __init__(self, ui):
        """
        Initialize exporter (Add-In mode only).
        
        Args:
            ui: Fusion UI object for dialogs and messaging.
        """
        self.ui = ui
        self.script_dir = None
        self.design = None
    
    def log(self, message):
        """Log message to UI dialog."""
        self.ui.messageBox(message)
    
    def load_design(self):
        """Load active Fusion 360 design."""
        if not FUSION_API_AVAILABLE:
            raise RuntimeError("Fusion 360 API not available")
        
        try:
            app = adsk.core.Application.get()
            product = app.activeProduct
            if not product:
                raise ValueError("No active document. Please open a design file first.")
            self.design = adsk.fusion.Design.cast(product)
            
            if not self.design:
                raise ValueError("Document is not a Fusion 360 design")
            
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to load design: {str(e)}")
    
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
            self.log(f"Warning: Error extracting user parameters: {str(e)}")
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
            self.log(f"Warning: Error extracting reference parameters: {str(e)}")
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
            self.log(f"Warning: Error extracting timeline: {str(e)}")
        return timeline_list
    
    def extract_sketches(self):
        """Extract sketches from the design."""
        sketches = []
        try:
            root = self.design.rootComponent
            for sketch in root.sketches:
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
            self.log(f"Warning: Error extracting sketches: {str(e)}")
        return sketches
    
    def extract_bodies(self):
        """Extract bodies from the design."""
        bodies = []
        try:
            # Try design.bodies first
            if hasattr(self.design, 'bodies'):
                for body in self.design.bodies:
                    bodies.append({
                        'name': body.name,
                        'volume': body.volume if hasattr(body, 'volume') else 'Unknown'
                    })
            # Otherwise try rootComponent.bodies
            elif hasattr(self.design.rootComponent, 'bodies'):
                for body in self.design.rootComponent.bodies:
                    bodies.append({
                        'name': body.name,
                        'volume': body.volume if hasattr(body, 'volume') else 'Unknown'
                    })
        except Exception as e:
            self.log(f"Warning: Error extracting bodies: {str(e)}")
        return bodies
    
    def get_document_path(self):
        """Get the path to the source .f3d file."""
        try:
            if self.design.parentDocument and hasattr(self.design.parentDocument, 'file'):
                return self.design.parentDocument.file.fullFileName
        except:
            pass
        return 'Unknown'
    
    def get_project_name(self):
        """Get the project name from the .f3d file name."""
        try:
            if self.design.parentDocument and hasattr(self.design.parentDocument, 'file'):
                full_path = self.design.parentDocument.file.fullFileName
                # Extract filename without extension
                filename = Path(full_path).stem
                return filename
        except:
            pass
        return 'export'
    
    def export(self):
        """Export complete design data."""
        try:
            # Get project name from the .f3d filename
            export_name = self.get_project_name()
            
            user_params = self.extract_user_parameters()
            ref_params = self.extract_reference_parameters()
            timeline = self.extract_timeline()
            sketches = self.extract_sketches()
            bodies = self.extract_bodies()
            
            export_data = {
                'export_metadata': {
                    'exported_date': datetime.now().isoformat(),
                    'fusion_360_api': 'Autodesk Fusion 360 API',
                    'export_name': export_name,
                    'source_f3d': self.get_document_path()
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
                'bodies': {
                    'total_count': len(bodies),
                    'bodies': bodies
                },
                'summary': {
                    'user_parameters_count': len(user_params),
                    'reference_parameters_count': len(ref_params),
                    'timeline_events_count': len(timeline),
                    'sketches_count': len(sketches),
                    'bodies_count': len(bodies)
                }
            }
            
            # Create output directories: export_name/origin/
            model_dir = self.script_dir / export_name
            output_dir = model_dir / "origin"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Write JSON file
            output_file = output_dir / f"{export_name}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            summary = f"Export Complete!\n\n"
            summary += f"Project: {export_name}\n"
            summary += f"File: {output_file}\n\n"
            summary += f"Exported:\n"
            summary += f"• User Parameters: {len(user_params)}\n"
            summary += f"• Reference Parameters: {len(ref_params)}\n"
            summary += f"• Timeline Events: {len(timeline)}\n"
            summary += f"• Sketches: {len(sketches)}\n"
            summary += f"• Bodies: {len(bodies)}\n"
            self.log(summary)
            
            return True
        except Exception as e:
            self.log(f"Error during export: {str(e)}")
            return False
    
    def run(self):
        """Execute export process."""
        try:
            self.load_design()
            self.export()
            return True
        except Exception as e:
            self.log(f"Error: {str(e)}")
            return False


def run(context):
    """Entry point for Fusion 360 Add-In mode."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Get output directory from user
        dlg = ui.createFolderDialog()
        dlg.title = 'Select directory to save Fusion 360 export'
        dlg.showDialog()
        
        if not dlg.folder:
            ui.messageBox('Export cancelled.')
            return
        
        # Create exporter and run
        exporter = FusionExporter(ui)
        exporter.script_dir = Path(dlg.folder)
        exporter.run()
        
    except Exception as ex:
        if ui:
            ui.messageBox(f'Error: {str(ex)}')
