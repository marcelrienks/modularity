# fission reactor

Fusion 360 Add-In for exporting complete design data and gathering context for AI-enabled parameterized code generation.

## Overview

**fission reactor** is a Fusion 360 workflow tool that enables conversion of hand-designed models into parameterized Python generators. It combines design export, user context gathering, and metadata standardization to feed AI with everything needed to generate working code.

**Core Features:**
- Export complete model data (parameters, sketches, features, timeline)
- Gather design context via interactive questionnaire
- Generate standardized JSON metadata
- Create AI-ready context packages
- Enable parameterized script generation via AI

## Use Cases

- **Design Documentation** - Capture complete model metadata and intent
- **Parameterization** - Extract design data for AI-based code generation
- **Version Control** - Store design parameters and features as JSON
- **Analysis** - Programmatically inspect model structure and features
- **AI Workflow** - Feed AI with standardized context for script generation

## Workflow

```
1. User Opens Design in Fusion 360
2. Run fission reactor Add-In
3. Answer Questionnaire (design intent, constraints, etc.)
4. Select Output Directory
5. Get Structured JSON Files:
   - model.json (design data)
   - context.json (user responses)
   - metadata.json (standardized format)
   - parameters.json (formatted for code gen)
   - constraints.json (design limits)
6. Feed Context Package to AI
7. AI Generates Parameterized Python Script
8. Script Generates Models with Parameter Variations
```

## Quick Start

1. Open a `.f3d` design file in Fusion 360
2. Go to **Tools > Add-ins > Scripts and Add-ins**
3. Select the **Scripts** tab
4. Right-click `export_fusion360_data` > **Run**
5. Select output directory

The script will export all models and create a complete context package:

```
your_selected_directory/
├── model_name_1/
│   ├── origin/
│   │   └── model_name_1.json (design data)
│   ├── context.json (user questionnaire responses)
│   ├── metadata.json (standardized metadata)
│   ├── parameters.json (formatted parameters)
│   └── constraints.json (design constraints)
└── model_name_2/
    ├── origin/
    │   └── model_name_2.json
    ├── context.json
    ├── metadata.json
    ├── parameters.json
    └── constraints.json
```

All files together form an **AI-ready context package** for code generation.

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

- `export_fusion360_data.py` - Main Add-In script (currently exports design data only)
- `readme.md` - This file
- `export_fusion360_guide.md` - Detailed usage guide

## Next Development

The following features are planned to complete the AI-enabled workflow:

1. **Questionnaire Integration** - Interactive prompts for design context
2. **Metadata Generation** - Standardized JSON files for parameters, constraints, assembly
3. **Context Package** - Complete bundle of all export files for AI consumption
4. **AI Integration Guide** - How to use exported context with ChatGPT/Claude for code generation

See [../todo.md](../todo.md) for the full roadmap.

## Documentation

- `export_fusion360_guide.md` - Add-In usage instructions
- See `../README.md` for project context

## Requirements

- Fusion 360 (any recent version with Python API support)
- A `.f3d` design file open in Fusion 360

## Output Formats

**Current Export (model.json):**

```json
{
  "export_metadata": { "exported_date", "model_name", "source_f3d", ... },
  "user_parameters": [...],
  "reference_parameters": [...],
  "timeline": { "events": [...] },
  "sketches": { "sketches": [...] },
  "features": { "features": [...] },
  "components": { "components": [...] },
  "summary": { ... }
}
```

**Planned Additions:**
- `context.json` - User responses to questionnaire
- `metadata.json` - Standardized model metadata
- `parameters.json` - Formatted parameters for code generation
- `constraints.json` - Design constraints and limits

## Next Steps

1. Review exported design file
2. Plan questionnaire for design context
3. Define standardized metadata schema
4. Create AI integration guide
5. Generate first parameterized script

---

Part of the **Modularity** project - AI-enabled tools for workshop organization systems.
