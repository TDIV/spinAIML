# Preparation of the public source copy

The original research notebooks and data were left unchanged. The public copy contains 30 notebooks and the original standalone Python script, retaining their relative directory structure. Experimental images, CSVs, generated figures, cached notebook checkpoints, and the paper PDF are not included.

## Changes applied

- Removed all notebook outputs, execution counts, execution metadata, and institution-specific kernel metadata. No cell attachments were present in the originals.
- Added one introductory Markdown cell to each notebook, linking to the workflow, data requirements, and limitations.
- Added deterministic cell IDs where absent and normalized notebooks to format 4.5 with a generic Python kernel.
- Converted machine-specific absolute source paths to paths relative to the notebook working directory. Explicit dataset prefixes were retained as same-directory or sibling-relative paths; experiment-local artifacts under the historical project root were interpreted relative to the current notebook directory.
- Commented the stray prose line `Print confirmation and a preview` in the three `Prediction_model.ipynb` copies. This fixes Python syntax without changing the surrounding feature-engineering calculations.
- Added documentation, a reconstructed dependency specification, paper citation metadata, Git ignore rules, notebook cleaning, and structural validation in GitHub Actions.

Model architecture, instantiated latent dimensions, losses, data-selection logic, thresholds, train/validation splitting, image processing, and frustration algorithms were preserved. The standalone `mfm_image1/cleaned_code.py` differs only by removal of a redundant final blank line. Relative output-name inconsistencies and recorded runtime issues are documented rather than silently resolved.

## Source-cell edits

Cell numbers in this table refer to the original notebooks, before the new introductory cell. Original machine-specific path prefixes are deliberately omitted from the public record.

| Notebook | Original cell | Change | Portable path / commented text |
| --- | --- | --- | --- |
| `mfm_frust_set2/Predict_frustration_synthetic.ipynb` | 4 | Portable path | `synthetic_mfm_segments_with_arrows` |
| `mfm_image1/Predict_frustration_orginal_mfm.ipynb` | 6 | Portable path | `mfm_segments_with_arrows` |
| `mfm_image1/Predict_frustration_synthetic_mfm.ipynb` | 6 | Portable path | `synthetic_mfm_segments_with_arrows` |
| `mfm_image1/Prediction_model.ipynb` | 2 | Portable path | `all_csv_data` |
| `mfm_image1/Prediction_model.ipynb` | 11 | Commented prose accidentally placed in a code cell | `Print confirmation and a preview` |
| `mfm_image1/Prediction_model.ipynb` | 12 | Portable path | `Data_merged_for_ML` |
| `mfm_image1/VAE_generative_image.ipynb` | 51 | Portable path | `reconstructed_mfm_image_with_directional_arrows.png` |
| `mfm_image1/VAE_generative_image.ipynb` | 51 | Portable path | `reconstructed_synthetic_mfm_image_with_directional_arrows.png` |
| `mfm_image2/Predict_frustration_orginal_mfm.ipynb` | 6 | Portable path | `mfm_segments_with_arrows` |
| `mfm_image2/Predict_frustration_synthetic_mfm.ipynb` | 6 | Portable path | `synthetic_mfm_segments_with_arrows` |
| `mfm_image2/Prediction_model.ipynb` | 2 | Portable path | `all_csv_data` |
| `mfm_image2/Prediction_model.ipynb` | 11 | Commented prose accidentally placed in a code cell | `Print confirmation and a preview` |
| `mfm_image2/Prediction_model.ipynb` | 12 | Portable path | `Data_merged_for_ML` |
| `mfm_image2/VAE_generative_image.ipynb` | 50 | Portable path | `reconstructed_mfm_image_with_directional_arrows.png` |
| `mfm_image2/VAE_generative_image.ipynb` | 50 | Portable path | `reconstructed_synthetic_mfm_image_with_directional_arrows.png` |
| `mfm_image2/diffusion_for_segmentation.ipynb` | 7 | Portable commented checkpoint path | `diffusion_model.pth` |
| `mfm_image2/mask_segmentation_v2.ipynb` | 3 | Portable path | `../mfm_image1/mfm_segments/mfm_segment_*.png` |
| `mfm_image2/mask_segmentation_v2.ipynb` | 3 | Portable path | `../mfm_image1/AB1.png` |
| `mfm_image2/mask_segmentation_v2.ipynb` | 17 | Portable path | `../mfm_image1/mfm_segments/mfm_segment_*.png` |
| `mfm_relax_set1/VAE_generate_image.ipynb` | 37 | Portable path | `reconstructed_mfm_image_with_directional_arrows.png` |
| `mfm_relax_set1/VAE_generate_image.ipynb` | 37 | Portable path | `reconstructed_synthetic_mfm_image_with_directional_arrows.png` |

## Provenance

[source_manifest.json](source_manifest.json) records original and initial-release SHA-256 hashes, sizes, descriptions, and the original indices of source-edited cells. Notebook code-only hashes exclude saved outputs and the added Markdown introduction. The original metadata reports Python 3.11.7. The manifest intentionally records the initial export and is not a lock on future source changes.

The original source files occupied 37.18 MiB; their cleaned copies occupy 1.10 MiB. The documentation and helper scripts are additional files.

## Validation scope

The publication checker performs static source and schema checks without executing the experiments. [VALIDATION.md](VALIDATION.md) records the checks actually run during preparation. No full research-environment installation, VAE retraining, or quantitative paper-result reproduction is implied.
