"""Handle geometry export to STL/STEP formats."""

import os
from pathlib import Path


class HandleExporter:
    """Export handle geometry to STL and/or STEP formats."""

    VALID_FORMATS = {"stl", "step"}

    def __init__(self, shape, diameter: float, height: float):
        """Initialize exporter with geometry and parameters."""
        self.shape = shape
        self.diameter = diameter
        self.height = height

    def export(self, output_dir: Path, formats: str = "stl") -> list:
        """Export to specified formats. Return list of created file paths."""
        if formats not in ("stl", "step", "both"):
            raise ValueError(f"format must be one of: stl, step, both (got: {formats})")

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check directory writability
        if not os.access(output_dir, os.W_OK):
            raise PermissionError(f"Output directory not writable: {output_dir}")
        
        exported_files = []

        # Determine which formats to export
        export_list = []
        if formats in ("stl", "both"):
            export_list.append("stl")
        if formats in ("step", "both"):
            export_list.append("step")

        # Export each format
        for fmt in export_list:
            filepath = output_dir / self._get_filename(fmt)
            
            # Check for existing file
            if filepath.exists():
                raise FileExistsError(f"File already exists: {filepath}")
            
            try:
                if fmt == "stl":
                    self.shape.exportStl(str(filepath))
                elif fmt == "step":
                    self.shape.exportStep(str(filepath))
                
                # Verify file was created and has content
                if not filepath.exists():
                    raise IOError(f"Failed to create {fmt.upper()} file")
                
                file_size = filepath.stat().st_size
                if file_size == 0:
                    raise IOError(f"Exported {fmt.upper()} file is empty")
                
                exported_files.append(str(filepath))
            
            except Exception as e:
                # Clean up partial exports on error
                if filepath.exists():
                    filepath.unlink()
                raise IOError(f"Failed to export {fmt.upper()}: {str(e)}")

        return exported_files

    def _get_filename(self, format_ext: str) -> str:
        """Generate filename encoding parameters."""
        return f"handle_d{self.diameter}_h{self.height}.{format_ext}"
