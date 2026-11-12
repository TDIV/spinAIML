#!/usr/bin/env python3
"""Clear outputs and execution metadata in this repository's public notebooks."""

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    ".git", ".venv", "venv", "env", ".ipynb_checkpoints", "__pycache__",
    ".agents", ".codex", ".cache", "data", "outputs", "results",
}


def source_files(root=ROOT):
    """Walk only this repository; skip environments and generated-data folders."""
    for directory, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(
            d for d in dirs
            if d not in SKIP_DIRS and not d.startswith(".venv")
            and not (Path(directory) / d).is_symlink()
        )
        for name in sorted(names):
            path = Path(directory) / name
            if path.suffix in {".ipynb", ".py"}:
                yield path


def clean_notebook(notebook, relative_path):
    """Return an output-free copy; leave cell source and order unchanged."""
    result = copy.deepcopy(notebook)
    if result.get("nbformat") != 4:
        raise ValueError("Only notebook format 4 is supported")
    result["nbformat_minor"] = 5
    result["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python"},
    }
    for index, cell in enumerate(result["cells"]):
        tags = cell.get("metadata", {}).get("tags")
        cell["metadata"] = {"tags": tags} if tags else {}
        cell.pop("attachments", None)
        if "id" not in cell:
            key = f"{relative_path}:{index}".encode("utf-8")
            cell["id"] = hashlib.sha256(key).hexdigest()[:12]
        if cell["cell_type"] == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="Report notebooks needing cleanup without changing any files.",
    )
    args = parser.parse_args()
    changed = 0
    total = 0
    for path in source_files():
        if path.suffix != ".ipynb":
            continue
        if path.is_symlink():
            raise SystemExit(f"Refusing to modify a symbolic link: {path.name}")
        total += 1
        relative = path.relative_to(ROOT).as_posix()
        original = json.loads(path.read_text(encoding="utf-8"))
        cleaned = clean_notebook(original, relative)
        if cleaned != original:
            changed += 1
            if args.check:
                print(f"Needs cleanup: {relative}")
            else:
                path.write_text(
                    json.dumps(cleaned, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8",
                )
                print(f"Cleaned: {relative}")
    if args.check and changed:
        print("Run python scripts/clean_notebooks.py before committing.")
        return 1
    print(f"Checked {total} notebooks; {changed} needed cleanup.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
