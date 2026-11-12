# Data requirements

This release contains source code only. The experimental image files, generated segments, CSVs, figures, and any trained weights are excluded from normal Git commits. There is no data-download URL supplied with this release.

The published [data availability statement](https://www.nature.com/articles/s41524-026-02124-8#data-availability) states that representative datasets will be made public following institutional review. Consult that statement and the corresponding authors for the dataset's release status. Add the approved dataset URL and its license here when available.

## Input images

The following filenames were identified in the supplied working directory. Put a dataset's images alongside its notebooks. Image dimensions are width × height in pixels. The morphology and MFM phase images must be spatially registered: segmentation coordinates from the morphology image are applied directly to the phase image.

| Directory | Morphology / mask | MFM phase image | Dimensions |
| --- | --- | --- | --- |
| `mfm_image1/` | `AB1.png` | `AB2.png`; `AB3.png` is an additional image referenced by the setup cells | 258 × 258 |
| `mfm_image2/` | `Mask_image.png` | `mfm_image.png` | 258 × 258 |
| `mfm_image3/` | `mask_image.png` | `mfm_image.png` | 258 × 258 |
| `mfm_frust_set1/` | `m90mtmor.png` | `m90mtphase.png` | 256 × 256 |
| `mfm_frust_set2/` | `p90mtmor.png` | `p90mtphase.png` | 256 × 256 |
| `mfm_relax_set1/` | `relax_mor.png` | `relax.png` | 256 × 256 |
| `large_scan_first_phase/` | `first_mor.png` | `first_phase.png` | 256 × 256 |
| `large_scan_last_phase/` | `last_mor.png` | `last_phase.png` | 256 × 256 |
| `large_scan_for_review/` | `mor034.png` | `phase034.png` | 279 × 279 |

Filenames are case-sensitive. Some exploratory notebooks refer to filenames from a different experiment, such as `AB1.png` or `AB2.png` inside `mfm_image2/`. Those inputs were not found in that dataset directory. Select the intended morphology/phase pair and update those cells before execution; do not assume images from different experiments are interchangeable.

For your own data, replace the input paths and review all segmentation thresholds, expected segment counts, example segment indices, and vertex-distance thresholds. Their current values are tied to the original image scale and geometry.

## Intermediate files

The segmentation and magnetic moment analysis normally produces:

```text
<experiment>/
  bit_segmentation_visualization.png
  bit_visualization_segments/
    segment_<ID>.png
    reconstructed_segmentation_image.png
  mfm_segments/
    mfm_segment_<ID>.png
  mfm_segments_with_arrows/
    magnetic_moments.csv
    mfm_segment_<ID>_with_arrow.png
```

Directory names differ in the arrow-color variants; see [WORKFLOW.md](WORKFLOW.md). Match each consumer's input path to the producer's actual output path.

The VAE's metadata CSV has three columns:

```csv
Segment,Direction,Magnetic_Moment_Strength
mfm_segment_1.png,0,12
mfm_segment_2.png,1,8
```

These two rows illustrate the schema; they are **not experimental measurements**. `Direction` follows the notebooks' binary left/right convention. Strength is an image-derived quantity in arbitrary units, not a calibrated magnetic moment in SI units. The main VAE loss uses the images; direction and strength are carried in the dataset but are not supervised targets for that loss.

The original `MFMDataset` constructs image filenames from row index plus one, rather than parsing the CSV's `Segment` column. Confirm that row order and IDs are appropriate before using a CSV; see [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

VAE reconstruction produces `synthetic_mfm_segments/synthetic_mfm_segment_<ID>.png` and, after the moment-analysis cells, `synthetic_magnetic_moments.csv`. Frustration analysis also consumes original segmentation geometry and produces segment-centroid, vertex-association, classification, and spin-toggle tables.

The feature-engineering `Prediction_model.ipynb` notebooks additionally expect an `all_csv_data/` directory assembled from earlier analyses and write `Data_merged_for_ML/`. These are not independent starting points. Their input collections and all generated results are excluded from this release.
