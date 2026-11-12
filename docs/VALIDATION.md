# Source-release validation

The following checks were run locally during preparation on 2026-11-12, using Python 3.11.15. Notebook and citation schema validation used `nbformat==5.10.4` and `cffconvert==2.0.0` in a separate temporary environment.

| Check | Result |
| --- | --- |
| Python parsing | All 739 code cells in 30 notebooks and all three Python files passed |
| Notebook schemas | All 30 notebooks passed format 4.5 validation |
| Citation schema | `CITATION.cff` passed CFF 1.2.0 validation |
| Citation metadata | Paper title, eight authors, DOI, volume, and article number matched Crossref's published metadata |
| Source provenance | SHA-256 hashes confirmed all 31 original research source files were unchanged |
| Output cleaning | No saved notebook outputs, execution counts, attachments, or inline image data remained |
| Cleaning integration | A temporary copy with injected execution output failed the checker; cleanup restored the original notebook content and validation then passed |
| Portability checks | No machine-specific absolute paths remained in the released notebook/Python source |
| Local document links | All relative Markdown file links resolved |
| Git staging | A temporary Git index contained the intended source/documentation files; representative data, checkpoint, credential, and environment paths were ignored |
| Whitespace | The prepared files passed `git diff --cached --check` in the temporary repository |
| Workflow configuration | The GitHub Actions YAML parsed and used read-only repository permissions |

The Git checks used a temporary repository; no commit or GitHub publication was created. The Actions workflow was checked locally, not run on a GitHub remote.

## Repeat the main checks

From the repository root, create an isolated validation environment:

```bash
python3.11 -m venv .venv-checks
source .venv-checks/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/clean_notebooks.py --check
python scripts/validate_repository.py --require-schema
deactivate
```

These are source-packaging checks. The full research dependency environment was not installed or used to run the experiments. VAE training, runtime of every notebook, numerical metrics, and paper-figure reproduction were not validated. The outstanding scientific and workflow limitations are described in [REPRODUCIBILITY.md](REPRODUCIBILITY.md).
