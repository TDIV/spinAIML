# Reproducibility and known limitations

This document records issues visible in the source at the time of preparation. It distinguishes the research code as supplied from the limited checks applied to its public copy. Packaging has not established that a fresh run reproduces the published figures or metrics.

## Model settings

The paper describes a latent dimension of **60**. In each of the following notebooks, `VAE.__init__` defaults to 60, but the actual training call supplies **`latent_dim=30`**:

- `mfm_image1/VAE_generative_image.ipynb`
- `mfm_relax_set1/VAE_generate_image.ipynb`


The preparation keeps those calls unchanged. The author needs to establish which setting corresponds to each reported result before making an exact-reproduction claim. Changing the value to 60 creates a new training run; it does not establish the provenance of a previous result.

The model loss is binary cross-entropy plus KL divergence with unit KL weight. The source does not expose a separate beta parameter for these training runs.

## Dataset identity and stochastic behavior

- The main `MFMDataset` uses `labels_df.index + 1` to choose `mfm_segment_<ID>.png`, instead of parsing the CSV's `Segment` column. Some supplied CSVs list filenames in lexicographic order and omit segments. Check alignment and included IDs explicitly when preparing a new run. Although direction and strength do not enter the VAE loss, the image selection and downstream moment comparisons still need consistent IDs.
- No fixed random seed or saved split indices were found in these five notebooks. Their `random_split` calls and latent sampling are stochastic. Calling `model.eval()` does not disable sampling in their `reparameterize` method.
- `test_vae` stops after its first validation batch. When the validation subset exceeds the batch size of 64, that function does not save reconstructions for the remaining validation samples. The training-subset export is a separate function. Count generated segments before assembling a full image.
- Missing images can be returned as `None` and filtered by `collate_fn`. An entirely invalid batch will still fail. Validate input completeness before training.
- No pretrained model checkpoints or original package lockfile were found in the supplied directory. Notebook metadata records Python 3.11.7; `requirements.txt` is a reconstructed Python 3.11 setup specification, not evidence of the original package versions.



## What publication checks establish

`scripts/validate_repository.py` checks that the source files exist, notebook cells have valid Python syntax, outputs and execution metadata are cleared, machine-specific absolute paths have been removed, and the citation/notebook metadata pass schema validation when the development dependencies are installed. It also checks Python scripts for syntax errors.

It does not execute scientific code, install the full research environment, train a model, compare numerical results, or verify every file dependency. Scientific settings, equations, data-selection logic, image processing, and frustration rules were not changed. [PREPARATION.md](PREPARATION.md) records the actual packaging edits and source provenance.
