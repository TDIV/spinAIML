# Publishing this source release

Publish the contents of **`github_release/`**, not the surrounding working directory. The surrounding directory contains the original notebooks, embedded experimental outputs, and image/CSV data; those files were not modified by preparation of this copy.

## Finalize the release information

**O5072 — Automation for Spin Systems** was approved for **Open-Source Assertion on April 21, 2026**, as confirmed by the institutional Export Control team. Retain the O5072 reference in `README.md` so that the copyright assertion can be confirmed. Add the selected software license and copyright notice as described in [LICENSE_STATUS.md](LICENSE_STATUS.md).

Review the [reproducibility notes](docs/REPRODUCIBILITY.md), especially the latent-dimension discrepancy. Decide whether this is an archival source release with the documented limitations or whether a verified reproduction workflow will be added. The source preparation preserves the existing scientific settings.

When a public data repository is available, add its persistent URL and data license to `docs/DATA.md`. This source-only release does not contain the paper PDF, experimental data, model checkpoints, or derived figures.

## Check and commit locally

Run these commands from this directory. Use a separate environment for the lightweight checks to keep their dependencies separate from Jupyter:

```bash
python3.11 -m venv .venv-checks
source .venv-checks/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/clean_notebooks.py --check
python scripts/validate_repository.py --require-schema
deactivate
git init -b main
git add .
git diff --cached --stat
git status --short
git commit -m "Prepare research source release for ASI MFM VAE paper"
```

If you have executed notebooks locally, clear their saved outputs before staging:

```bash
source .venv-checks/bin/activate
python scripts/clean_notebooks.py
python scripts/validate_repository.py --require-schema
deactivate
git add .
```

The ignore rules keep images, CSVs, model weights, environments, and credentials out of normal `git add` operations. Review the staged file list before each commit. Do not use `git add -f` to include data unless it is deliberately part of the release and documented with its own terms.

## Connect to GitHub

Create an empty repository on GitHub, for example `asi-mfm-vae`. Do not initialize the remote with another README or license. Replace `YOUR_GITHUB_ACCOUNT` below with your account or organization:

```bash
git remote add origin https://github.com/YOUR_GITHUB_ACCOUNT/asi-mfm-vae.git
git push -u origin main
```

After choosing the URL, add it as `repository-code` in `CITATION.cff`. For a stable paper reference, tag the reviewed version and create a GitHub release; a Zenodo archive can supply a separate software DOI. Do not use the paper DOI as the software DOI.

Once the source code is publicly accessible, forward the repository URL to the institutional Export Control team, citing **O5072**. The team requested this link for reporting the code to the **Energy Science and Technology Software Center (ESTSC)** and depositing the access link to fulfill DOE-NNSA obligations. If publication is delayed, provide the team with the anticipated publication date.

## Updating the notebooks

Edit the public copy, clear outputs, and rerun validation. The [source manifest](docs/source_manifest.json) and [change record](docs/PREPARATION.md) describe the initial export from the research workspace. Preserve that record when making subsequent scientific changes, and describe those changes in the Git history.
