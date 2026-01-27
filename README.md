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

### 📁 [`Fusion360Export/`](./Fusion360Export/)

**Fusion 360 Add-In** for extracting and documenting design data from open models.

**What it does:**
- Exports complete design data (parameters, sketches, features, timeline) from any `.f3d` file
- Generates structured JSON metadata
- Helps with design documentation and building parameterized generators

**Usage:**
1. Open a design file in Fusion 360
2. Tools > Add-ins > Scripts and Add-ins > Scripts tab
3. Right-click the script > Run
4. Select output directory

**Note:** This is an optional utility for design analysis. The core tulgryd generators work independently.

**Documentation:** See [`Fusion360Export/README.md`](./Fusion360Export/README.md) for detailed usage

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

**Optional Design Export Tool:**

The [Fusion360Export](./Fusion360Export/) Add-In extracts complete design data from Fusion 360 models:

1. **Export:** Extract complete design data (parameters, sketches, features, timeline) from any `.f3d` file
2. **Document:** Generate comprehensive metadata describing the model structure
3. **Parameterize:** Use exported data to create Python scripts that generate models with different parameters

**Workflow:**
```
Fusion 360 Design (.f3d)
        ↓
Fusion360Export Add-In
        ↓
Design Data (JSON)
        ↓
Create Parameterized Python Script
        ↓
Generate Models with Custom Parameters
```

**Use Cases:**
- Convert hand-designed models to parameterized generators
- Create tool holder variations with different dimensions
- Generate models programmatically with CLI arguments
- Version control design parameters and construction logic

**Learn More:** See [`Fusion360Export/README.md`](./Fusion360Export/README.md)

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

---

*These systems represent the power of open-source design. Contribute your own models back to these communities!*
