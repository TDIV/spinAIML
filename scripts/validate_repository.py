#!/usr/bin/env python3
"""Validate source packaging without importing or executing the experiments."""

import argparse
import ast
import json
import re
from pathlib import Path

from clean_notebooks import ROOT, clean_notebook, source_files


LOCAL_PATH = re.compile(r"/(?:global|home|Users|scratch|pscratch|mnt|content)/")
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}
REQUIRED = (
    "README.md", "CITATION.cff", "citation.bib", "LICENSE_STATUS.md",
    "PUBLISHING.md", "CONTRIBUTING.md", "requirements.txt",
    "requirements-dev.txt", ".gitignore", ".gitattributes",
    ".github/workflows/validate.yml", "docs/DATA.md", "docs/WORKFLOW.md",
    "docs/REPRODUCIBILITY.md", "docs/NOTEBOOKS.md", "docs/PREPARATION.md",
    "docs/source_manifest.json", "docs/VALIDATION.md",
)


def check_source(source, location, errors):
    try:
        ast.parse(source, filename=location)
    except SyntaxError as exc:
        errors.append(f"{location}: Python syntax error at line {exc.lineno}: {exc.msg}")
    if LOCAL_PATH.search(source):
        errors.append(f"{location}: machine-specific absolute path remains")
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(source):
            # Never echo the matching value into a log.
            errors.append(f"{location}: possible {label}; review before publishing")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-schema", action="store_true",
        help="Require nbformat and cffconvert for notebook and citation schemas.",
    )
    args = parser.parse_args()
    errors = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"Missing release file: {relative}")

    try:
        import nbformat
    except ImportError:
        nbformat = None
    try:
        from cffconvert import Citation
    except ImportError:
        Citation = None

    if args.require_schema and (nbformat is None or Citation is None):
        errors.append("Schema dependencies missing: pip install -r requirements-dev.txt")

    manifest_path = ROOT / "docs/source_manifest.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for entry in manifest["files"]:
                relative = Path(entry["path"])
                if relative.is_absolute() or ".." in relative.parts:
                    errors.append("Source manifest contains a path outside the repository")
                elif not (ROOT / relative).is_file():
                    errors.append(f"Missing original source file: {relative}")
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f"Invalid source manifest: {exc}")

    notebooks = code_cells = python_files = 0
    for path in source_files():
        relative = path.relative_to(ROOT).as_posix()
        if path.is_symlink():
            errors.append(f"{relative}: source must be a regular file, not a symbolic link")
            continue
        if path.stat().st_size > 10 * 1024 * 1024:
            errors.append(f"{relative}: source exceeds 10 MiB; check for embedded data")
        if path.suffix == ".py":
            python_files += 1
            check_source(path.read_text(encoding="utf-8"), relative, errors)
            continue
        notebooks += 1
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
            if clean_notebook(notebook, relative) != notebook:
                errors.append(f"{relative}: run scripts/clean_notebooks.py before committing")
            if nbformat is not None:
                nbformat.validate(notebook)
            for index, cell in enumerate(notebook["cells"], start=1):
                source = "".join(cell.get("source", []))
                if cell["cell_type"] == "code":
                    code_cells += 1
                    check_source(source, f"{relative}:cell {index}", errors)
                elif LOCAL_PATH.search(source):
                    errors.append(f"{relative}:cell {index}: machine-specific path remains")
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f"{relative}: invalid notebook: {exc}")
        except Exception as exc:
            # nbformat raises its own validation exception hierarchy.
            detail = getattr(exc, "message", str(exc).splitlines()[0])
            errors.append(f"{relative}: notebook schema failed: {detail}")

    if Citation is not None and (ROOT / "CITATION.cff").is_file():
        try:
            Citation((ROOT / "CITATION.cff").read_text(encoding="utf-8")).validate()
        except Exception as exc:
            detail = getattr(exc, "message", str(exc).splitlines()[0])
            errors.append(f"CITATION.cff: citation schema failed: {detail}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Validated {notebooks} notebooks, {code_cells} code cells, and {python_files} Python files.")
    if nbformat is not None and Citation is not None:
        print("Notebook and CFF citation schemas passed.")
    else:
        print("Schema checks incomplete; install requirements-dev.txt and use --require-schema.")
    print("Experiments were not executed; scientific reproducibility is not tested here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
