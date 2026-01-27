# Fusion360Export

Fusion 360 Add-In for exporting complete design data from open models as structured JSON.

## Overview

This utility helps you extract and document design data from Fusion 360 models. It captures:

- **Parameters** - User-defined and derived parameters
- **Timeline** - Complete feature history
- **Sketches** - All sketches with geometry and constraints
- **Features** - Extrude, Hole, Shell, Mirror, Chamfer, Fillet, Pattern, Thread
- **Components** - Component/body hierarchy
- **Metadata** - Export date, source file path

## Use Cases

- **Design Documentation** - Generate comprehensive metadata about your models
- **Version Control** - Store design parameters as JSON in git
- **Parameterization** - Extract design intent for building code generators
- **Analysis** - Programmatically inspect model structure and features

## Quick Start

1. Open a `.f3d` design file in Fusion 360
2. Go to **Tools > Add-ins > Scripts and Add-ins**
3. Select the **Scripts** tab
4. Right-click `export_fusion360_data` > **Run**
5. Select output directory

The script will export all models from the design as JSON files in the structure:

```
your_selected_directory/
├── model_name_1/
│   └── origin/
│       └── model_name_1.json
└── model_name_2/
    └── origin/
        └── model_name_2.json
```

## Installation

### Option 1: Manual Installation
Copy `export_fusion360_data.py` to:
```
~/Library/Application Support/Autodesk/Fusion 360/API/Python/Samples/
```

Then restart Fusion 360. The script will appear in the Scripts tab.

### Option 2: Direct Use
Place the script in any accessible location and browse to it from the Scripts panel.

## Files

- `export_fusion360_data.py` - Main Add-In script
- `readme.md` - This file

## Documentation

See `export_fusion360_guide.md` in the same directory for detailed usage and troubleshooting.

## Requirements

- Fusion 360 (any recent version with Python API support)
- A `.f3d` design file open in Fusion 360

## Output Format

Each exported model produces a JSON file containing:

```json
{
  "export_metadata": {
    "exported_date": "ISO timestamp",
    "model_name": "string",
    "source_f3d": "file path",
    "document_path": "file path"
  },
  "user_parameters": [...],
  "reference_parameters": [...],
  "timeline": { "total_events": n, "events": [...] },
  "sketches": { "total_count": n, "sketches": [...] },
  "features": { "total_count": n, "features": [...] },
  "components": { "total_count": n, "components": [...] },
  "summary": { ... }
}
```

## Next Steps

1. Export your design file
2. Review the JSON output structure
3. Use exported data for documentation or analysis
4. Consider using this data to build parameterized code generators

## Learn More

- **Fusion 360 API Docs:** https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/
- **Parent Project:** See [`../README.md`](../README.md) for overview of Modularity project

---

Part of the **Modularity** project - tools for workshop organization systems.
