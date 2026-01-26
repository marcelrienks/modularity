# Fusion 360 API Export Script - Usage Guide

## Overview

This Python script (`ExportFusion360Data.py`) uses the Fusion 360 API to extract and export all design data from your model:
- ✅ User parameters (handle_diameter, handle_height, etc.)
- ✅ Reference parameters (derived values)
- ✅ Timeline/feature history (all design steps)
- ✅ Sketch information (names, geometry counts, constraints)
- ✅ Feature information (extrudes, holes, shells, mirrors, chamfers, fillets)
- ✅ Component tree structure

Output: **JSON file** with complete design information for Python parameterization

---

## Installation & Setup

### Prerequisites

1. **Fusion 360** installed on your computer
2. **Python 3.7+** (included with Fusion 360)
3. **Fusion 360 API SDK** (included with Fusion 360)

### Verify API is Installed

In Fusion 360:
- Go to **Scripts and Add-ins** (Tools > Add-ins > Scripts and Add-ins)
- Look for the **Scripts** folder path displayed in the dialog
- API SDK should be automatically available

---

## How to Run the Script

### Option 1: Using Fusion 360 Scripts UI (EASIEST)

1. **Open your model** - Open `tulgryd handles.f3d` in Fusion 360

2. **Copy the script**
   ```bash
   # Copy ExportFusion360Data.py to Fusion 360 scripts folder
   # On Mac: ~/Library/Application Support/Autodesk/Fusion 360/API/Python/Samples/
   # On Windows: %APPDATA%\Autodesk\Fusion 360\API\Python\Samples\
   ```

3. **Access Scripts Panel**
   - Go to **Tools > Add-ins > Scripts and Add-ins**
   - Select **Scripts** tab
   - Look for `ExportFusion360Data` in the list

4. **Run the script**
   - Right-click `ExportFusion360Data`
   - Select **Run**

5. **Select output directory**
   - Dialog appears asking where to save
   - Choose your `tulgryd/handles/origin/` directory
   - Click **OK**

6. **Success!**
   - Message shows summary of exported data
   - JSON file created with timestamp

### Option 2: Run from Terminal/Command Line

```bash
# Mac/Linux
/Applications/Autodesk\ Fusion\ 360.app/Contents/MacOS/Fusion\ 360 \
  --scriptFile /path/to/ExportFusion360Data.py

# Windows (from PowerShell or Command Prompt)
cd "C:\Program Files\Autodesk\Fusion 360\bin"
Fusion360.exe --scriptFile "C:\path\to\ExportFusion360Data.py"
```

**Note:** Script must have a Fusion 360 file open before running

---

## Output Format

The script generates a JSON file with this structure:

```json
{
  "export_metadata": {
    "exported_date": "2026-01-26T12:35:00.123456",
    "fusion_360_api": "Autodesk Fusion 360 API",
    "model_name": "tulgryd",
    "document_path": "/path/to/tulgryd handles.f3d"
  },
  "user_parameters": [
    {
      "name": "handle_diameter",
      "value": 26.0,
      "unit": "mm",
      "comment": "",
      "type": "user_parameter"
    },
    {
      "name": "handle_height",
      "value": 33.0,
      "unit": "mm",
      "comment": "",
      "type": "user_parameter"
    }
  ],
  "reference_parameters": [
    {
      "name": "handle_radius",
      "value": 13.0,
      "unit": "mm",
      "comment": "Derived: handle_diameter / 2",
      "type": "reference_parameter"
    }
  ],
  "timeline": {
    "total_events": 12,
    "events": [
      {
        "index": 0,
        "name": "Sketch",
        "feature_type": "SketchFeature",
        "is_suppressed": false
      },
      {
        "index": 1,
        "name": "Extrude",
        "feature_type": "ExtrudeFeature",
        "is_suppressed": false
      }
    ]
  },
  "sketches": {
    "total_count": 1,
    "sketches": [
      {
        "name": "Sketch",
        "parent": "root",
        "geometry_count": 15,
        "profile_count": 2,
        "is_visible": true,
        "constraints_count": 8
      }
    ]
  },
  "features": {
    "total_count": 5,
    "features": [
      {
        "type": "Extrude",
        "name": "Extrude",
        "parent": "root"
      },
      {
        "type": "Mirror",
        "name": "Mirror",
        "parent": "root"
      },
      {
        "type": "Shell",
        "name": "Shell",
        "parent": "root"
      },
      {
        "type": "Hole",
        "name": "Hole",
        "parent": "root"
      },
      {
        "type": "Chamfer",
        "name": "Chamfer",
        "parent": "root"
      }
    ]
  },
  "components": {
    "total_count": 1,
    "components": [
      {
        "name": "tulgryd",
        "parent": "root",
        "feature_count": 5,
        "sketch_count": 1
      }
    ]
  },
  "summary": {
    "user_parameters_count": 2,
    "reference_parameters_count": 1,
    "timeline_events_count": 12,
    "sketches_count": 1,
    "features_count": 5,
    "components_count": 1
  }
}
```

---

## Using the Exported Data

### 1. Verify Parameters

Compare exported parameters with your `parameters.json`:

```bash
# View exported file
cat tulgryd_fusion360_export_20260126_123500.json | jq '.user_parameters'

# Should show:
# - handle_diameter: 26.0
# - handle_height: 33.0
# - (any other user parameters)
```

### 2. Validate Feature Sequence

Check that timeline events match your `geometry_formulas.json`:

```bash
# View feature timeline
cat tulgryd_fusion360_export_20260126_123500.json | jq '.timeline.events'

# Expected sequence:
# 1. Sketch
# 2. Extrude (half-grip)
# 3. Mirror
# 4. Shell
# 5. Extrude (base)
# 6. Hole (small)
# 7. Hole (large)
# 8. Chamfer
```

### 3. Update Metadata Files

If any new parameters found:
1. Add to `parameters.json`
2. Update `geometry_formulas.json` with correct values
3. Update `validation_rules.json` with new constraints

### 4. Store for Version Control

```bash
# Move to version control location
mv tulgryd_fusion360_export_*.json /path/to/handles/origin/

# Commit to git
git add tulgryd_fusion360_export_*.json
git commit -m "Export Fusion 360 parameter data for handles model"
```

---

## Troubleshooting

### Script doesn't appear in Scripts panel

**Solution:**
1. Verify script is in correct folder (check path in Scripts UI)
2. Restart Fusion 360
3. Script should now appear

### "No active document" error

**Solution:**
1. Open `tulgryd handles.f3d` first
2. Then run script
3. Script requires active design file

### "Active document is not a design" error

**Solution:**
1. Open a `.f3d` design file (not drawing or other document type)
2. Run script again

### Permission denied when saving

**Solution:**
1. Ensure directory is writable
2. Try saving to `Desktop` first (always writable)
3. Check folder permissions

### JSON file is empty or incomplete

**Solution:**
1. Check Fusion 360 console for errors (Tools > Add-ins > Scripts and Add-ins)
2. Ensure model has parameters and features defined
3. Try running on simpler model first

---

## Advanced Usage

### Modify Script for Custom Export

You can edit `ExportFusion360Data.py` to:

1. **Add more feature types:**
   ```python
   # Add after chamfers section
   for feature in component.features.threads:
       features.append({
           'type': 'Thread',
           'name': feature.name,
           'parent': parent_name
       })
   ```

2. **Extract specific parameter properties:**
   ```python
   # Add to user parameters loop
   'is_driving': param.isDriving,
   'is_user': param.isUser,
   ```

3. **Export to different format (CSV):**
   ```python
   # Replace JSON export with CSV
   import csv
   with open(output_path, 'w', newline='') as f:
       writer = csv.writer(f)
       writer.writerow(['Name', 'Value', 'Unit'])
       for param in user_params_list:
           writer.writerow([param['name'], param['value'], param['unit']])
   ```

---

## Expected Output for Your Model

For `tulgryd handles.f3d`, you should see approximately:

```
Export Complete!

File saved to:
/Users/marcelrienks/make/modularity/tulgryd/handles/origin/tulgryd_fusion360_export_20260126_123500.json

Summary:
  • User Parameters: 2
  • Reference Parameters: 1-3
  • Timeline Events: 8-12
  • Sketches: 1-2
  • Features: 5-8
  • Components: 1

The JSON file contains complete design information
ready for parameterization script development.
```

---

## Next Steps

After running the export:

1. ✅ **Review exported JSON file**
   - Open in text editor
   - Verify parameter names and values

2. ✅ **Compare with metadata files**
   - Check `parameters.json` matches exported values
   - Update if any discrepancies

3. ✅ **Validate timeline sequence**
   - Ensure feature order matches `geometry_formulas.json`
   - Document any unexpected features

4. ✅ **Commit to version control**
   - Add JSON export file to git
   - Provides audit trail of model parameters

5. ✅ **Use for Python parameterization**
   - Reference JSON file in your parameterization script
   - Extract values programmatically
   - Generate new model variants

---

## API Documentation

For more information on Fusion 360 API:
- **Official Docs:** https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/
- **API Reference:** https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ReferenceManual_UM.htm
- **Sample Scripts:** https://github.com/fusion360-api-cheatsheet/Fusion360_API_Documentation_Samples

---

## Support

If you encounter issues:

1. Check **Fusion 360 API Console** (Tools > Add-ins > Scripts and Add-ins > Scripts > right-click > Edit > View Log)
2. Review error message carefully
3. Ensure Fusion 360 and API SDK are up to date
4. Try running on a simpler model first
5. Check API documentation for object availability

---
