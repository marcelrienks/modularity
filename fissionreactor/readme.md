# fission reactor

AI-enabled Fusion 360 workflow: export design data → answer questionnaire → get parameterized Python code.

---

## Overview

**Two integrated workflows:**
1. **Export & Extraction** - Export model data from Fusion 360, transform into standardized metadata
2. **Questionnaire** - Capture design intent through 28 questions, combine with export data

**Result:** AI-ready context package for generating parameterized code that reproduces your model with variations.

---

## Files

| File | Purpose |
|------|---------|
| `export_fusion360_guide.md` | How to export data and transform into metadata (Parts 1 & 2) |
| `questionnaire_guide.md` | How to answer questionnaire and map responses to metadata |
| `questionnaire_template.json` | 28 questions in 8 sections (machine-readable) |
| `questionnaire_example.json` | Real shelf bracket example (all questions answered) |
| `export_fusion360_data.py` | Fusion 360 Add-In script |

---

## Quick Start (5 Steps)

**Step 1:** Prepare model in Fusion 360 (named parameters, logical feature order)

**Step 2:** Export data
- Tools > Add-ins > Scripts and Add-ins > Scripts tab
- Right-click `export_fusion360_data` > Run
- Select output directory → generates `model.json`
- See `export_fusion360_guide.md` Part 1 for details

**Step 3:** Answer questionnaire
- Complete all 28 questions (15-30 minutes)
- Reference: `questionnaire_example.json` for example answers
- See `questionnaire_guide.md` for question explanations
- Result: `context.json`

**Step 4:** Transform to metadata
- Combine `model.json` + `context.json` → 5 metadata files
- See `export_fusion360_guide.md` Part 2 for algorithm & validation

**Step 5:** Send to AI
- Package: model.json, context.json, + 5 metadata files
- Prompt AI: "Generate parameterized Python code to reproduce this model with variations based on the metadata"

---

## Installation

Copy `export_fusion360_data.py` to:
```
~/Library/Application Support/Autodesk/Fusion 360/API/Python/Samples/
```
Restart Fusion 360. Script appears in Scripts tab.

---

## Support

**Q: Why the questionnaire?**
A: AI can extract geometry but not design intent. Questionnaire captures "why" decisions were made.

**Q: How long?**
A: Export ~5 min, questionnaire 15-30 min, transform ~1 min.

**Q: What if I don't know an answer?**
A: Leave blank. More detail = better code. AI makes reasonable assumptions.

**Q: Can I modify questions?**
A: Yes. Edit `questionnaire_template.json`. Guide explains each category.

---

More info: **Fusion 360 API Docs** - https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/
