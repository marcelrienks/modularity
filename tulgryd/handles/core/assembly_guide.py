"""Auto-generate assembly guide documentation."""

from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


class AssemblyGuideGenerator:
    """Generate assembly guide README from Jinja2 template."""

    VERSION = "0.1.0"

    def __init__(self, diameter: float, height: float, template_dir: Path = None):
        """Initialize with parameters and optional custom template directory."""
        self.diameter = diameter
        self.height = height
        self.template_dir = template_dir or Path(__file__).parent / "templates"

    def generate(self, output_dir: Path) -> str:
        """Render and write assembly guide. Return file path."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        template = env.get_template("assembly_guide.md.j2")
        
        # Prepare context for template rendering
        context = {
            "diameter": self.diameter,
            "height": self.height,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": self.VERSION,
        }
        
        # Render template
        rendered = template.render(**context)
        
        # Write to file
        filepath = output_dir / self._get_filename()
        with open(filepath, "w") as f:
            f.write(rendered)
        
        return str(filepath)

    def _get_filename(self) -> str:
        """Generate README filename."""
        return f"handle_d{self.diameter}_h{self.height}_README.md"
