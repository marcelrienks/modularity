# Fusion 360 Export Add-In Guide

**Location:** `/Users/marcelrienks/make/modularity/tulgryd/export_fusion360_data.py`

Fusion 360 Add-In script that exports complete design data from the currently open model.

---

## Quick Start

1. Open a `.f3d` design file in Fusion 360
2. Go to **Tools > Add-ins > Scripts and Add-ins**
3. Select the **Scripts** tab
4. Right-click `export_fusion360_data` > **Run**
5. Select the directory where you want to save the exported JSON files

---

## What Gets Exported

Each model exports a JSON file containing:
- **User parameters** - All parameterized dimensions
- **Reference parameters** - Derived/calculated values
- **Timeline** - Complete feature history
- **Sketches** - All sketches with geometry/constraints
- **Features** - Extrude, Hole, Shell, Mirror, Chamfer, Fillet, Pattern, Thread
- **Components** - Component/body hierarchy
- **Metadata** - Export date, source file path

## Output Structure

### Directory Layout
```
tulgryd/
├── export_fusion360_data.py
├── model_name_1/
│   └── origin/
│       └── model_name_1.json
└── model_name_2/
    └── origin/
        └── model_name_2.json
```

### File Behavior
- Creates folder named after each model
- Saves JSON file with model name
- **Overwrites existing files** if re-exported
- Directories auto-created if they don't exist

---

## Usage Examples

### Export All Models
When you run the Add-In, it will export all models/components from the open design file:

```
model_name_1/
└── origin/
    └── model_name_1.json
model_name_2/
└── origin/
    └── model_name_2.json
```

Each JSON file contains complete design data for that model.

---

## Output Location

The script prompts you to select a directory. Exported files will be created in that directory with the structure:

```
your_selected_directory/
├── model_name_1/
│   └── origin/
│       └── model_name_1.json
└── model_name_2/
    └── origin/
        └── model_name_2.json
```

---

## Troubleshooting

**Script doesn't appear in Add-In list:**
1. Copy `export_fusion360_data.py` to: `~/Library/Application Support/Autodesk/Fusion 360/API/Python/Samples/`
2. Restart Fusion 360
3. Go to Tools > Add-ins > Scripts and Add-ins > Scripts tab

**No active document:**
- Open a `.f3d` design file first
- Then run the script from the Scripts panel

**Export cancelled:**
- The script was cancelled from the folder selection dialog
- Run it again and select a valid output directory

---

## Next Steps

1. Review exported JSON file
2. Use exported data to generate documentation
3. Commit JSON files to version control
4. Use metadata to create parameterized code

---

## More Information

- **Fusion 360 API Docs:** https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/
