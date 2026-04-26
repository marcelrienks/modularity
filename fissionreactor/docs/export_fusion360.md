# Export Design Data from Fusion 360

Export complete design data from your Fusion 360 model as `model.json`.

## Installation

### macOS
```bash
cp ExportMetaData.py ~/Library/Application\ Support/Autodesk/Fusion\ 360/API/Python/Samples/
```

### Windows
```cmd
copy ExportMetaData.py "%APPDATA%\Autodesk\Fusion 360\API\Python\Samples\"
```

### Linux
```bash
cp ExportMetaData.py ~/.Autodesk/Fusion\ 360/API/Python/Samples/
```

## Usage

1. **Restart Fusion 360** after copying the script
2. **Open your .f3d design file**
3. Go to: **Tools > Add-ins > Scripts and Add-ins > Scripts tab**
4. Right-click `ExportMetaData` → **Run**
5. **Select output directory**
6. Get: **model.json** (in your selected directory)

## What Gets Exported

- **User parameters** — All named dimensions (Width, Depth, etc.)
- **Reference parameters** — Calculated/derived values
- **Timeline** — Complete feature construction sequence
- **Sketches** — All sketches with geometry
- **Features** — Extrude, Pocket, Hole, Fillet, Pattern, etc.
- **Components** — Body/part hierarchy
- **Metadata** — Export date, Fusion 360 version

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Script doesn't appear | Verify correct installation path, restart Fusion 360 |
| "No active document" | Open your .f3d file first |
| Export cancelled | Run again and select a valid directory |
| Invalid JSON | Check Fusion 360 API logs |

## Next Step

Complete questionnaire → `context.json`

See: `questionnaire_guide.md`
