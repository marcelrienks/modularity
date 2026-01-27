# Modularity

A collection of custom implementations and tools for the **MultiBoard** and **ToolGrid** modular workshop organization systems.

*Note: The project naming intentionally uses creative spellings ("multyboord" and "tulgryd") as homages to these excellent systems.*

## Project Structure

### 📁 [`multyboord/`](./multyboord/)

Custom 3D-printed tool hangers extending the **MultiBoard** modular pegboard system.

- **What is MultiBoard?** An open-source system for creating modular, customizable workshop storage using 3D-printed accessories compatible with a pegboard grid
- **What's here?** Custom-designed tool hangers (hammers, pliers, screwdrivers, sockets, spanners) that integrate seamlessly with MultiBoard
- **Documentation:** See [`multyboord/README.md`](./multyboord/README.md) for detailed model list and printing guide
- **Learn more:** [multiboard.io](https://www.multiboard.io/)

### 📁 [`tulgryd/`](./tulgryd/)

A **parametric system** for creating modular pegboard tiles and custom tool holders (handles, grips, organizers) for the ToolGrid tool-holding system.

**Components:**
- **Tiles:** Parametric pegboard tile generator for custom workshop storage layouts
- **Tool Holders:** Custom-designed handles, grips, and organizers
- **Design Files:** Fusion 360 source models for reference and modification

**Features:**
- Input total dimensions → Generate optimized tile layout automatically
- Smart layout with 100×100mm standard tiles + custom edge pieces
- Export to STL or STEP formats
- Calibration mode for printer tolerance testing
- Full assembly guides with layout diagrams

**What's here?**
- `tiles/generate.py` - CLI tool for tile generation
- `tiles/core/` - Core modules (layout calculation, model building, assembly guides)
- `tiles/origin/` - Original hand-designed ToolGrid system
- `handles/` - Custom tool holder models (grips, organizers, etc.)
- `tulgryd.f3d` - Master design file (Fusion 360)

**Documentation:** See [`tulgryd/README.md`](./tulgryd/README.md) for complete usage guide

**Quick Start - Tiles:**
```bash
# Generate tiles for a 250×180mm drawer
python tulgryd/tiles/generate.py --total-width 250 --total-length 180

# Generate calibration tile to test hole diameters
python tulgryd/tiles/generate.py --calibrate --hole-diameter 4.0
```

### 📁 [`fissionreactor/`](./fissionreactor/)

**AI-Enabled Fusion 360 Workflow** for converting hand-designed models into parameterized Python code generators.

**Intentions:**
- Transform manual CAD designs into automated, parameter-driven code
- Preserve design intent alongside geometry
- Enable rapid generation of model variations
- Bridge the gap between design and code through structured metadata
- Archive complete design context for future reference or AI consumption

**What It Does:**
1. **Export:** Extracts complete design data from `.f3d` files (parameters, sketches, features, timeline)
2. **Capture Context:** Gathers design intent through 28-question questionnaire
3. **Standardize:** Transforms export + context into structured JSON metadata
4. **Enable Generation:** Creates AI-ready package for generating parameterized Python scripts

**Key Features:**
- Fusion 360 Add-In (no external tools required)
- Automated export of model parameters and feature timeline
- Comprehensive questionnaire capturing design decisions and constraints
- JSON-based metadata output for AI processing
- Validation and error checking throughout workflow

**Typical Workflow (15-30 minutes):**
```
Fusion 360 Design (.f3d)
         ↓ (5 min)
Export Design Data (model.json)
         ↓ (15-30 min)
Answer Questionnaire (context.json)
         ↓ (1 min)
Transform to Metadata (5 JSON files)
         ↓
Send to AI for Code Generation
         ↓
Receive Parameterized Python Script
```

**Use Cases:**
- Convert static tile designs to parameterized generators (e.g., ToolGrid tiles)
- Create tool holder variations with custom dimensions
- Generate multiple model versions from single design source
- Version control design parameters and construction logic
- Document design rationale alongside code

**Installation:**
```bash
# Copy script to Fusion 360 directory
cp fissionreactor/export_fusion360_data.py \
  ~/Library/Application\ Support/Autodesk/Fusion\ 360/API/Python/Samples/
# Restart Fusion 360
```

**Quick Start:**
1. Open design in Fusion 360
2. Tools > Add-ins > Scripts and Add-ins > Scripts tab
3. Right-click `export_fusion360_data` > Run
4. Complete questionnaire (see `questionnaire_example.json` for reference)
5. Package output files and send to AI

**Documentation:** See [`fissionreactor/README.md`](./fissionreactor/README.md) for complete usage guide and workflow details

### 📁 [`ToolGrid/`](./ToolGrid/)

A curated collection of community-sourced 3D models for the **ToolGrid** system, organized by tool type.

**What is ToolGrid?** An open-source modular tool storage system featuring interlocking tiles with threaded holes and integrated tool holders.

**What's here?** Crowd-sourced 3D models for:
- Wrench and socket holders
- Plier racks
- Screwdriver organizers
- Specialty tool holders
- And many more!

**Attributions:** This directory contains models from the maker community. Individual credits and attributions are noted in the respective model directories where applicable.

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│            Workshop Organization Systems                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  MultiBoard (multyboord/)          ToolGrid (tulgryd/)      │
│  ─────────────────────             ────────────────         │
│  • Pegboard-based                  • Interlocking tiles      │
│  • Modular grid system             • Custom tool holders     │
│  • 3000+ community models          • Parametric generation   │
│  • Easy customization              • Scalable designs        │
│                                    • Fusion 360 integration  │
│              Both: 100% 3D Printable & Open Source           │
└─────────────────────────────────────────────────────────────┘
```

## Fusion 360 Integration

**AI-Enabled Model Parameterization with fissionreactor:**

The [fissionreactor](./fissionreactor/) Add-In enables extraction and conversion of Fusion 360 models into parameterized Python generators. This workflow bridges the gap between manual CAD design and automated code generation.

**The Three-Phase Workflow:**

1. **Phase 1: Design Export**
   - Extract complete design data from `.f3d` file
   - Captures parameters, sketches, bodies, features, and timeline
   - Generates `model.json` with geometry and construction data

2. **Phase 2: Design Context**
   - Answer 28-question questionnaire about design decisions
   - Captures intent, constraints, use cases, and variations
   - Generates `context.json` with human-readable context

3. **Phase 3: AI Code Generation**
   - Transform model + context into standardized metadata
   - Send to AI (with provided metadata format)
   - Receive parameterized Python script that reproduces model with variations

**Workflow Diagram:**
```
┌─ Fusion 360 Design (.f3d) ─┐
│  (Manual CAD model)        │
└────────────┬────────────────┘
             ↓
     fissionreactor Add-In
             ↓
    ┌────────┴────────┐
    ↓                 ↓
model.json      context.json
(Parameters)    (Design Intent)
    ↓                 ↓
    └────────┬────────┘
             ↓
     5 Metadata Files
   (parameters, features,
    sketches, constraints,
     variations)
             ↓
    AI Code Generation
             ↓
Parameterized Python Script
(generate models with custom params)
             ↓
Production Models (.STL)
```

**Outcome:** Models that were manually designed once can now be generated infinitely with different parameters—enabling scalable, version-controlled, documented design workflows.

**Learn More:** See [`fissionreactor/README.md`](./fissionreactor/README.md) for detailed documentation, questionnaire guide, and examples.

## Getting Started

### For MultiBoard Custom Hangers
1. Navigate to [`multyboord/`](./multyboord/)
2. Choose your tool hanger model (STL or STEP format)
3. Print with your preferred material (PETG or ABS recommended)
4. Mount to your MultiBoard pegboard

### For Custom ToolGrid Tile Generation
1. Navigate to [`tulgryd/`](./tulgryd/)
2. Install dependencies: `pip install -r requirements.txt` (if available)
3. Generate tiles for your dimensions
4. Print the output files
5. Follow the auto-generated assembly guide

### For Crowd-Sourced ToolGrid Models
1. Browse [`ToolGrid/`](./ToolGrid/) for available models
2. Select tools matching your workshop needs
3. Print and assemble with your ToolGrid system

## Requirements

- 3D Printer (FDM recommended)
- Slicing Software (Cura, PrusaSlicer, etc.)
- **For tile generation:** Python 3.8+, CadQuery 2.4+

## License

- **MultiBoard system & models** - Check [multiboard.io](https://www.multiboard.io/) for licensing
- **ToolGrid system & designs** - Check individual sources
- **Custom implementations in this repo** - See individual project READMEs for licensing

## Attribution

- **MultiBoard** - Created by the open-source community at [multiboard.io](https://www.multiboard.io/)
- **ToolGrid System** - Community-driven project with contributions from makers worldwide
- **Crowd-Sourced Models** - Various creators (attributions in ToolGrid directory)
- **This Repository** - Custom implementations and tools by Marcel Rienks
