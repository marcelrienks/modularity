#!/bin/bash
# Quick reference for running the Fusion 360 API Export Script

# FILE LOCATIONS
# ==============================================================
SCRIPT_LOCATION="/Users/marcelrienks/make/modularity/tulgryd/handles/origin/ExportFusion360Data.py"
USAGE_GUIDE="/Users/marcelrienks/make/modularity/tulgryd/handles/origin/EXPORT_SCRIPT_USAGE.md"

# MAC: Copy script to Fusion 360 Scripts folder
cp "$SCRIPT_LOCATION" ~/Library/Application\ Support/Autodesk/Fusion\ 360/API/Python/Samples/

# WINDOWS: Copy to Scripts folder (from PowerShell)
# Copy-Item "$SCRIPT_LOCATION" "$env:APPDATA\Autodesk\Fusion 360\API\Python\Samples\"

# ==============================================================
# RUNNING THE SCRIPT
# ==============================================================

# Step 1: Open Fusion 360 and load tulgryd handles.f3d
# 
# Step 2: Tools > Add-ins > Scripts and Add-ins
# 
# Step 3: Click Scripts tab
# 
# Step 4: Find ExportFusion360Data in list
# 
# Step 5: Right-click > Run
# 
# Step 6: Dialog appears - select output directory
#         (choose /Users/marcelrienks/make/modularity/tulgryd/handles/origin/)
# 
# Step 7: Success! JSON file created

# ==============================================================
# RESULT
# ==============================================================

# Output file: tulgryd_fusion360_export_YYYYMMDD_HHMMSS.json
# 
# Example: tulgryd_fusion360_export_20260126_123500.json
# 
# Contains:
#   • User parameters (handle_diameter, handle_height, etc.)
#   • Reference parameters (derived values)
#   • Timeline (feature history)
#   • Sketches (names, geometry)
#   • Features (extrude, mirror, shell, hole, chamfer)
#   • Components (tree structure)
#   • Summary statistics

# ==============================================================
# VERIFY RESULTS
# ==============================================================

# Check parameters were exported
# jq '.user_parameters' tulgryd_fusion360_export_*.json

# Check timeline sequence
# jq '.timeline.events' tulgryd_fusion360_export_*.json

# Check feature count
# jq '.summary.features_count' tulgryd_fusion360_export_*.json

# ==============================================================
# TROUBLESHOOTING
# ==============================================================

# Issue: Script doesn't appear in list
# Solution: 
#   1. Verify file copied to correct folder
#   2. Restart Fusion 360
#   3. Check folder path in Scripts UI (Tools > Add-ins)

# Issue: "No active document" error
# Solution:
#   1. Open tulgryd handles.f3d first
#   2. Then run script

# Issue: "Active document is not a design" error
# Solution:
#   1. Must use .f3d design file (not drawing or other type)

# ==============================================================
# FOR MORE HELP
# ==============================================================

# Read the comprehensive guide:
# cat "$USAGE_GUIDE"

# Or view specific section:
# grep -A 20 "QUICK START" "$USAGE_GUIDE"
