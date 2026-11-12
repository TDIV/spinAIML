Artificial intelligence and machine learning for spin systems
# VAE analysis of artificial spin ice from MFM images

Research notebooks for **Deep generative learning of magnetic frustration in artificial spin ice from magnetic force microscopy images**, by Arnab Neogi, Suryakant Mishra, Prasad P. Iyer, Tzu-Ming Lu, Ezra Bussmann, Sergei Tretiak, Andrew C. Jones, and Jian-Xin Zhu, *npj Computational Materials* **12**, 266 (2026).

**Paper:** <https://doi.org/10.1038/s41524-026-02124-8>

The code processes magnetic force microscopy (MFM) images of honeycomb artificial spin ice (ASI): it segments individual nanomagnets, estimates their magnetic moment directions and relative strengths, trains a variational autoencoder (VAE) to reconstruct MFM segments, and analyzes vertex frustration and candidate spin reversals.

This is a source release of the research notebooks, including exploratory variants. Experimental images, generated tables and figures, notebook outputs, and model weights are not bundled. The notebooks retain experiment-specific assumptions and require the inputs and adjustments described below; they are not an automated reproduction of every paper figure.

## Open-Source Assertion

**O5072 — Automation for Spin Systems** was approved for **Open-Source Assertion on April 21, 2026**. This reference is included so that the copyright assertion can be confirmed.


## Getting started

Use **Python 3.11** in a new environment. The dependencies below are a reconstructed installation specification, not a recovered snapshot of the original training environment.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
# CPU installation, suitable for the original fully connected VAE notebooks:
python -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
python -m ipykernel install --sys-prefix --name asi-vae --display-name "Python (ASI VAE)"
jupyter lab
```

On Windows, activate the environment with `.venv\Scripts\activate` instead. For CUDA, install a matching PyTorch/torchvision build using the [PyTorch installation instructions](https://pytorch.org/get-started/locally/). The main MFM VAE notebooks use CPU tensors; installing CUDA alone does not move their training to a GPU.

1. Read the [data requirements](docs/DATA.md) and place the required input images in the corresponding experiment directory.
2. Follow the [workflow guide](docs/WORKFLOW.md). For a compact three-notebook sequence, start with `mfm_frust_set2/`; `mfm_image1/` and `mfm_relax_set1/` contain additional analyses.
3. Run each notebook with its **own directory as the kernel working directory**, using the environment created above. Review path settings and execute cells in order. Output files are written into that experiment directory.

## Repository contents

| Location | Contents |
| --- | --- |
| `mfm_image1/` | Segmentation, VAE training, original/synthetic frustration analyses, artifact analysis, and a standalone preprocessing script |
| `mfm_relax_set1/` | Relaxed-configuration segmentation, VAE analysis, frustration classification and spin-toggle analysis |
| `docs/` | Workflow, data requirements, notebook catalog, preparation changes, and reproducibility notes |
| `scripts/` | Notebook cleaning and repository validation utilities |

See the [complete notebook catalog](docs/NOTEBOOKS.md) for all the notebooks.

## Reproducibility

 This release preserves the training calls; it does not silently choose which value produced the published results.

The notebooks also contain unseeded train/validation splits, stochastic latent sampling, paths from different analysis variants, and exploratory cells with recorded errors. Read [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) before using them to reproduce quantitative results.

The release checks validate notebook structure, Python syntax, output removal, and citation metadata. See the [validation record](docs/VALIDATION.md) for the checks performed during preparation.

Use a separate validation environment to avoid conflicts with Jupyter's dependencies:

```bash
python3.11 -m venv .venv-checks
source .venv-checks/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate_repository.py --require-schema
deactivate
```

## Citation

Please cite the paper when using this work. GitHub's **Cite this repository** feature uses [CITATION.cff](CITATION.cff); a BibTeX entry is supplied in [citation.bib](citation.bib). The DOI identifies the paper, not a separately archived software release.

## License and data availability

A software license has not yet been selected for this prepared release; see [LICENSE_STATUS.md](LICENSE_STATUS.md). The paper's publication license does not automatically license the source code or experimental data.

The data requirements and the paper's availability statement are linked in [docs/DATA.md](docs/DATA.md). Instructions for the maintainer to create the GitHub repository are in [PUBLISHING.md](PUBLISHING.md).
