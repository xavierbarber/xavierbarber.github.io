"""Build the three public pages from their R Markdown sources using Pandoc."""
from pathlib import Path
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--pandoc", default="pandoc", help="Path to the Pandoc executable")
args = parser.parse_args()
root = Path(__file__).resolve().parent
for name in ("index", "xbarber", "cva"):
    subprocess.run([args.pandoc, str(root / (name + ".Rmd")),
                    "--from=markdown", "--to=html5", "--standalone",
                    "--template=" + str(root / "site-template.html"),
                    "--output=" + str(root / (name + ".html"))], check=True)
print("Built index.html, xbarber.html and cva.html")
