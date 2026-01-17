# Modularity

A collection of custom implementations and tools for the **MultiBoard** and **ToolGrid** modular workshop organization systems.

*Note: The project naming intentionally uses creative spellings ("multyboord" and "tulgryd") as homages to these excellent open-source systems.*

## Project Structure

### 📁 [`multyboord/`](./multyboord/)

Custom 3D-printed tool hangers extending the **MultiBoard** modular pegboard system.

- **What is MultiBoard?** An open-source system for creating modular, customizable workshop storage using 3D-printed accessories compatible with a pegboard grid
- **What's here?** Custom-designed tool hangers (hammers, pliers, screwdrivers, sockets, spanners) that integrate seamlessly with MultiBoard
- **Documentation:** See [`multyboord/README.md`](./multyboord/README.md) for detailed model list and printing guide
- **Learn more:** [multiboard.io](https://www.multiboard.io/)

### 📁 [`tulgryd/`](./tulgryd/)

A **parametric tile generator** for creating custom pegboards compatible with the ToolGrid tool-holding system.

**Features:**
- Input total dimensions → Generate optimized tile layout automatically
- Smart layout with 100×100mm standard tiles + custom edge pieces
- Export to STL or STEP formats
- Calibration mode for printer tolerance testing
- Full assembly guides with layout diagrams

**What's here?**
- `generate.py` - Main CLI tool for tile generation
- `core/` - Core modules (layout calculation, model building, assembly guides)
- `origin/` - Original hand-designed ToolGrid system (basis for the generator)

**Documentation:** See [`tulgryd/README.md`](./tulgryd/README.md) for complete usage guide and API reference

**Quick Start:**
```bash
# Generate tiles for a 250×180mm drawer
python generate.py --total-width 250 --total-length 180

# Generate calibration tile to test hole diameters
python generate.py --calibrate --hole-diameter 4.0
```

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
│  • Modular grid system             • Parametric generation   │
│  • 3000+ community models          • Custom layouts          │
│  • Easy customization              • Scalable designs        │
│                                                               │
│              Both: 100% 3D Printable & Open Source           │
└─────────────────────────────────────────────────────────────┘
```

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
