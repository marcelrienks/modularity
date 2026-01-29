# Code Generation Overview

Generate parameterized Python code from your context package using AI.

## What You Have

7 JSON files (your context package):
- `model.json` — Design geometry and features
- `context.json` — Design intent and constraints
- `metadata.json`, `parameters.json`, `constraints.json`, `features.json`, `assembly.json` — AI-ready specs

## What You Get

A complete Python script (`generate_yourmodel.py`) that:
- Accepts CLI parameters: `python generate_yourmodel.py --width 200 --output model.step`
- Validates inputs against design constraints
- Generates your CAD model with custom parameters
- Exports to STEP or STL format
- Works out of the box

## How It Works

1. **Send** all 7 JSON files to AI (Claude, GPT-4, etc.)
2. **Provide** generation prompt (see below)
3. **AI generates** working Python script using CadQuery
4. **Receive** `generate_yourmodel.py`
5. **Use** to generate models with any parameters

## Generation Prompt

```
Generate a complete parameterized CadQuery Python script that:

1. Accepts all parameters from parameters.json as CLI arguments
2. Validates inputs against constraints.json (pre-generation)
3. Builds model following the feature timeline from model.json
4. Validates output (post-generation)
5. Exports to STEP or STL format

Requirements:
- Use template_generator.py as reference for code structure
- Study examples/generate_shelfbracket_example.py for patterns
- Follow naming conventions from generator-guide_naming-conventions.md
- Include helpful error messages when constraints are violated
- Support both --output filename.step and .stl formats

Return the complete, working generate_yourmodel.py script.
```

## Testing Generated Code

```bash
# Show help
python generate_yourmodel.py --help

# Generate with defaults
python generate_yourmodel.py

# Test custom parameters
python generate_yourmodel.py --width 100 --output small.step

# Test error handling (should reject invalid params)
python generate_yourmodel.py --width 50 --output test.step  # Should error if < min
```

## Validation Checklist

✓ Script runs without errors  
✓ Default parameters match original model  
✓ Model opens in CAD software  
✓ Dimensions correct (±0.5mm tolerance)  
✓ All features present and in correct order  
✓ Parameter variations work correctly  
✓ Invalid parameters rejected with helpful errors

## Resources

- **Template:** `template_generator.py` (boilerplate skeleton)
- **Example:** `examples/generate_shelfbracket_example.py` (working code)
- **Detailed Guide:** `generator-guide_generation-guide.md`
- **Naming:** `generator-guide_naming-conventions.md`

## Next Steps

1. Send context package + prompt to AI
2. Receive generated script
3. Test thoroughly
4. Use for model generation with custom parameters
