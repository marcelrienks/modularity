# Fusion 360 Export Script Guide

**Location:** `/Users/marcelrienks/make/modularity/tulgryd/export_fusion360_data.py`

Unified script that works in **CLI mode** (command-line) or **Add-In mode** (Fusion 360 UI).
Both modes produce identical JSON output.

---

## Quick Start

### CLI Mode
```bash
# Export all models
python export_fusion360_data.py "/path/to/model.f3d"

# Export specific model
python export_fusion360_data.py "/path/to/model.f3d" model_name
```

### Add-In Mode
1. Open .f3d file in Fusion 360
2. Tools > Add-ins > Scripts and Add-ins > Scripts tab
3. Right-click `export_fusion360_data` > Run
4. Select output directory

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

---

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

### CLI: Export All Models
```bash
python export_fusion360_data.py "~/tulgryd/handles/origin/tulgryd handles.f3d"
```
Creates:
- `handle_grip/origin/handle_grip.json`
- `handle_base/origin/handle_base.json`

### CLI: Export Specific Model
```bash
python export_fusion360_data.py "~/tulgryd/handles/origin/tulgryd handles.f3d" handle_grip
```
Creates:
- `handle_grip/origin/handle_grip.json`

---

## Troubleshooting

**File not found:**
- Use absolute path (e.g., `/Users/user/path/to/file.f3d`)
- Verify file exists

**Model not found:**
- Export without model name to see all available models
- Check spelling (case-sensitive)

**Script doesn't appear in Add-In list:**
- Copy to: `~/Library/Application Support/Autodesk/Fusion 360/API/Python/Samples/`
- Restart Fusion 360

**No active document (Add-In mode):**
- Open a .f3d design file first
- Then run script from Scripts panel

---

## Next Steps

1. Review exported JSON file
2. Use exported data to generate documentation
3. Commit JSON files to version control
4. Use metadata to create parameterized code

---

## More Information

- **Fusion 360 API Docs:** https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/
