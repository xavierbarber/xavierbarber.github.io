"""Compatibility entry point for the bilingual website builder."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("build_professional_site.py")),run_name="__main__")
