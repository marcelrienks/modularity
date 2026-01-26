#Author: Marcel Rienks (via AI assistance)
#Description: Export Fusion 360 parameters, timeline, and sketch data to JSON
#Usage: Run as Fusion 360 Add-In (Scripts > Create Scripts > Run)

import adsk.core
import adsk.fusion
import json
import os
from datetime import datetime

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Get active document and design
        product = app.activeProduct
        if not product:
            ui.messageBox('No active document. Please open a Fusion 360 file.')
            return
            
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('Active document is not a design. Please open a Fusion 360 design file.')
            return
        
        # ============================================================
        # 1. EXTRACT USER PARAMETERS
        # ============================================================
        parameters_data = {}
        user_params_list = []
        
        for param in design.userParameters:
            param_entry = {
                'name': param.name,
                'value': param.value,
                'unit': param.unit,
                'comment': param.comment if param.comment else '',
                'type': 'user_parameter'
            }
            user_params_list.append(param_entry)
            parameters_data[param.name] = param.value
        
        # ============================================================
        # 2. EXTRACT DERIVED/REFERENCE PARAMETERS
        # ============================================================
        ref_params_list = []
        
        for param in design.allParameters:
            # Skip user parameters (already captured)
            if param in design.userParameters:
                continue
                
            ref_entry = {
                'name': param.name,
                'value': param.value,
                'unit': param.unit,
                'comment': param.comment if param.comment else '',
                'type': 'reference_parameter'
            }
            ref_params_list.append(ref_entry)
        
        # ============================================================
        # 3. EXTRACT TIMELINE / FEATURE HISTORY
        # ============================================================
        timeline_list = []
        timeline = design.timeline
        
        for i in range(timeline.count):
            event = timeline.item(i)
            timeline_entry = {
                'index': i,
                'name': event.name,
                'feature_type': type(event).__name__,
                'is_suppressed': event.isSuppressed
            }
            timeline_list.append(timeline_entry)
        
        # ============================================================
        # 4. EXTRACT SKETCH INFORMATION
        # ============================================================
        sketches_list = []
        
        def process_sketches(component, parent_name=""):
            sketches = []
            for sketch in component.sketches:
                sketch_name = sketch.name
                sketch_entry = {
                    'name': sketch_name,
                    'parent': parent_name if parent_name else 'root',
                    'geometry_count': sketch.sketchCurves.sketchLines.count + 
                                    sketch.sketchCurves.sketchCircles.count +
                                    sketch.sketchCurves.sketchArcs.count,
                    'profile_count': sketch.profiles.count,
                    'is_visible': sketch.isVisible
                }
                
                # Extract sketch constraints
                constraints = []
                for constraint in sketch.geometricConstraints:
                    constraints.append({
                        'type': type(constraint).__name__,
                        'name': constraint.name if hasattr(constraint, 'name') else ''
                    })
                
                sketch_entry['constraints_count'] = len(constraints)
                
                sketches.append(sketch_entry)
            
            return sketches
        
        sketches_list.extend(process_sketches(design.rootComponent))
        
        # ============================================================
        # 5. EXTRACT FEATURE INFORMATION
        # ============================================================
        features_list = []
        
        def process_features(component, parent_name=""):
            features = []
            
            # Extrude features
            for feature in component.features.extrusions:
                features.append({
                    'type': 'Extrude',
                    'name': feature.name,
                    'parent': parent_name if parent_name else 'root'
                })
            
            # Hole features
            for feature in component.features.holes:
                features.append({
                    'type': 'Hole',
                    'name': feature.name,
                    'parent': parent_name if parent_name else 'root'
                })
            
            # Shell features
            for feature in component.features.shells:
                features.append({
                    'type': 'Shell',
                    'name': feature.name,
                    'parent': parent_name if parent_name else 'root'
                })
            
            # Mirror features
            for feature in component.features.mirrors:
                features.append({
                    'type': 'Mirror',
                    'name': feature.name,
                    'parent': parent_name if parent_name else 'root'
                })
            
            # Chamfer features
            for feature in component.features.chamfers:
                features.append({
                    'type': 'Chamfer',
                    'name': feature.name,
                    'parent': parent_name if parent_name else 'root'
                })
            
            # Fillet features
            for feature in component.features.fillets:
                features.append({
                    'type': 'Fillet',
                    'name': feature.name,
                    'parent': parent_name if parent_name else 'root'
                })
            
            return features
        
        features_list.extend(process_features(design.rootComponent))
        
        # ============================================================
        # 6. EXTRACT COMPONENT TREE STRUCTURE
        # ============================================================
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
                    component.features.fillets.count
                ]),
                'sketch_count': component.sketches.count
            }
            components_list.append(comp_entry)
            
            # Process child components
            for child in component.childComponents:
                process_components(child, component.name)
        
        process_components(design.rootComponent)
        
        # ============================================================
        # 7. BUILD COMPLETE EXPORT OBJECT
        # ============================================================
        export_data = {
            'export_metadata': {
                'exported_date': datetime.now().isoformat(),
                'fusion_360_api': 'Autodesk Fusion 360 API',
                'model_name': design.name,
                'document_path': design.parentDocument.filePath if design.parentDocument else 'Unknown'
            },
            'user_parameters': user_params_list,
            'reference_parameters': ref_params_list,
            'timeline': {
                'total_events': timeline.count,
                'events': timeline_list
            },
            'sketches': {
                'total_count': len(sketches_list),
                'sketches': sketches_list
            },
            'features': {
                'total_count': len(features_list),
                'features': features_list
            },
            'components': {
                'total_count': len(components_list),
                'components': components_list
            },
            'summary': {
                'user_parameters_count': len(user_params_list),
                'reference_parameters_count': len(ref_params_list),
                'timeline_events_count': timeline.count,
                'sketches_count': len(sketches_list),
                'features_count': len(features_list),
                'components_count': len(components_list)
            }
        }
        
        # ============================================================
        # 8. SAVE TO JSON FILE
        # ============================================================
        
        # Determine output path - ask user for directory
        dlg = ui.createFolderDialog()
        dlg.title = 'Select directory to save Fusion 360 export'
        if dlg.showDialog() == adsk.core.DialogResults.OKResult:
            output_dir = dlg.folder
        else:
            ui.messageBox('Export cancelled.')
            return
        
        # Create output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'{design.name}_fusion360_export_{timestamp}.json'
        output_path = os.path.join(output_dir, output_filename)
        
        # Write JSON file with nice formatting
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        # ============================================================
        # 9. DISPLAY SUCCESS MESSAGE
        # ============================================================
        success_message = f'''Export Complete!

File saved to:
{output_path}

Summary:
  • User Parameters: {len(user_params_list)}
  • Reference Parameters: {len(ref_params_list)}
  • Timeline Events: {timeline.count}
  • Sketches: {len(sketches_list)}
  • Features: {len(features_list)}
  • Components: {len(components_list)}

The JSON file contains complete design information
ready for parameterization script development.
'''
        ui.messageBox(success_message, 'Export Successful')
        
    except Exception as ex:
        if ui:
            ui.messageBox(f'Error: {str(ex)}\n\n{adsk.core.getLastError()}')
