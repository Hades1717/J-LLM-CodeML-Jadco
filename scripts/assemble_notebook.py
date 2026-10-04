"""Assemble nb/00..10 into the final deliverable equinoxe_2026.ipynb, then run it top to bottom.

Usage (from the project root):
    python scripts/assemble_notebook.py            # assemble + execute
    python scripts/assemble_notebook.py --no-run   # assemble only
    python scripts/assemble_notebook.py --sections # also execute each section notebook in nb/ (refreshes data/interim/)
    python scripts/assemble_notebook.py --sections --skip 06   # same, without touching nb/06 in place

Cells tagged `io-only` (the %run / read_parquet / to_parquet plumbing that lets each section notebook run on its
own) are dropped, so the final notebook reads as one continuous story using in-memory variables.
Do not edit equinoxe_2026.ipynb by hand: edit the section notebooks and re-run this script.
"""
import argparse
import sys
from pathlib import Path

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NB_DIR = PROJECT_ROOT / "nb"
OUTPUT_PATH = PROJECT_ROOT / "equinoxe_2026.ipynb"
IO_ONLY_TAG = "io-only"
CELL_TIMEOUT_SECONDS = 1200  # the bootstrap and sensitivity grid are the slowest cells


def section_paths():
    """Section notebooks in execution order (00_..., 01_..., ...)."""
    return sorted(p for p in NB_DIR.glob("[0-9][0-9]_*.ipynb"))


def execute(notebook, working_dir):
    ExecutePreprocessor(timeout=CELL_TIMEOUT_SECONDS, kernel_name="python3").preprocess(
        notebook, {"metadata": {"path": str(working_dir)}})


def run_sections(skip=()):
    """Execute each section notebook in place (they read/write data/interim/ through their io-only cells)."""
    for path in section_paths():
        if path.name[:2] in skip:
            print(f"skipping {path.name} (still included in the assembled notebook)")
            continue
        print(f"running {path.name} ...", flush=True)
        notebook = nbformat.read(path, as_version=4)
        execute(notebook, NB_DIR)
        nbformat.write(notebook, path)


def assemble():
    final = nbformat.v4.new_notebook()
    final.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    for path in section_paths():
        section = nbformat.read(path, as_version=4)
        for cell in section.cells:
            if IO_ONLY_TAG in cell.get("metadata", {}).get("tags", []):
                continue
            if cell.cell_type == "code":
                cell.outputs, cell.execution_count = [], None
            final.cells.append(cell)
    return final


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--no-run", action="store_true", help="assemble without executing")
    parser.add_argument("--sections", action="store_true", help="first execute every section notebook in nb/")
    parser.add_argument("--skip", nargs="*", default=[], help="section prefixes not to re-execute in place, e.g. --skip 06")
    args = parser.parse_args()

    if args.sections:
        run_sections(args.skip)
    final = assemble()
    if not args.no_run:
        print("executing assembled notebook ...", flush=True)
        execute(final, PROJECT_ROOT)
    nbformat.write(final, OUTPUT_PATH)
    print(f"wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)} ({len(final.cells)} cells)")


if __name__ == "__main__":
    sys.exit(main())
