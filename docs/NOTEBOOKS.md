# Source notebook catalog

All 30 notebooks from the supplied experiment directory are retained, with saved outputs removed. The catalog describes their contents; inclusion does not imply successful fresh-kernel execution. For execution order and prerequisites, see [WORKFLOW.md](WORKFLOW.md) and [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

| Source | Purpose / status |
| --- | --- |
| [Prediction_model.ipynb](../Prediction_model.ipynb) | CSV merging and feature engineering; requires prepared input tables. |
| [large_scan_first_phase/Automate_strength_dir_large_sample.ipynb](../large_scan_first_phase/Automate_strength_dir_large_sample.ipynb) | Large-sample segmentation and moment-analysis variant. |
| [large_scan_first_phase/Automate_strength_direction.ipynb](../large_scan_first_phase/Automate_strength_direction.ipynb) | Segmentation and magnetic moment extraction. |
| [large_scan_first_phase/VAE_generate_image.ipynb](../large_scan_first_phase/VAE_generate_image.ipynb) | MFM VAE training and image comparisons; final comparison selects the relaxed dataset. |
| [large_scan_first_phase/test_new_segmentation.ipynb](../large_scan_first_phase/test_new_segmentation.ipynb) | Exploratory segmentation; saved runtime error documented. |
| [large_scan_for_review/Automate_strength_direction_magnetic_moment.ipynb](../large_scan_for_review/Automate_strength_direction_magnetic_moment.ipynb) | Segmentation and moment extraction for the review scan. |
| [large_scan_last_phase/Automate_strength_dir.ipynb](../large_scan_last_phase/Automate_strength_dir.ipynb) | Segmentation and moment extraction for the last-phase scan. |
| [mfm_frust_set1/Automate_strength_direction_magnetic_moment.ipynb](../mfm_frust_set1/Automate_strength_direction_magnetic_moment.ipynb) | Additional dataset analysis; saved runtime errors documented. |
| [mfm_frust_set2/Automate_strength_direction.ipynb](../mfm_frust_set2/Automate_strength_direction.ipynb) | Stage 1: segmentation and magnetic moment extraction. |
| [mfm_frust_set2/Predict_frustration_synthetic.ipynb](../mfm_frust_set2/Predict_frustration_synthetic.ipynb) | Stage 3: synthetic-image vertex analysis and direction optimization. |
| [mfm_frust_set2/VAE_generate_image.ipynb](../mfm_frust_set2/VAE_generate_image.ipynb) | Stage 2: MFM VAE training, reconstruction, and synthetic moments. |
| [mfm_image1/Automate_strength_direction_magnetic_moment.ipynb](../mfm_image1/Automate_strength_direction_magnetic_moment.ipynb) | Segmentation and moment extraction; updated-arrow output paths. |
| [mfm_image1/Highlight_artifacts.ipynb](../mfm_image1/Highlight_artifacts.ipynb) | Artifact inspection and visualization. |
| [mfm_image1/Predict_frustration_orginal_mfm.ipynb](../mfm_image1/Predict_frustration_orginal_mfm.ipynb) | Original-image vertex/frustration analysis and direction optimization. |
| [mfm_image1/Predict_frustration_synthetic_mfm.ipynb](../mfm_image1/Predict_frustration_synthetic_mfm.ipynb) | Synthetic-image vertex/frustration analysis. |
| [mfm_image1/Prediction_model.ipynb](../mfm_image1/Prediction_model.ipynb) | Dataset-local CSV merging and feature-engineering experiment. |
| [mfm_image1/VAE_generative_image.ipynb](../mfm_image1/VAE_generative_image.ipynb) | MFM VAE training, reconstruction, and comparison metrics. |
| [mfm_image1/cleaned_code.py](../mfm_image1/cleaned_code.py) | Earlier standalone preprocessing variant with top-level execution. |
| [mfm_image2/Automate_strength_direction_magnetic_moment.ipynb](../mfm_image2/Automate_strength_direction_magnetic_moment.ipynb) | Segmentation variants and moment extraction; review mixed input names. |
| [mfm_image2/Predict_frustration_orginal_mfm.ipynb](../mfm_image2/Predict_frustration_orginal_mfm.ipynb) | Original-image analysis variant; review copied input paths. |
| [mfm_image2/Predict_frustration_synthetic_mfm.ipynb](../mfm_image2/Predict_frustration_synthetic_mfm.ipynb) | Synthetic-image analysis variant; review copied input paths. |
| [mfm_image2/Prediction_model.ipynb](../mfm_image2/Prediction_model.ipynb) | Dataset-local CSV merging and feature-engineering experiment. |
| [mfm_image2/VAE_for_mask.ipynb](../mfm_image2/VAE_for_mask.ipynb) | Exploratory VAE for mask generation. |
| [mfm_image2/VAE_for_mask_segmentation_v2.ipynb](../mfm_image2/VAE_for_mask_segmentation_v2.ipynb) | Exploratory generator/discriminator model for masks, despite the VAE filename. |
| [mfm_image2/VAE_generative_image.ipynb](../mfm_image2/VAE_generative_image.ipynb) | MFM VAE training/reconstruction variant; review intermediate paths. |
| [mfm_image2/diffusion_for_segmentation.ipynb](../mfm_image2/diffusion_for_segmentation.ipynb) | Exploratory diffusion-style mask reconstruction. |
| [mfm_image2/mask_segmentation_v2.ipynb](../mfm_image2/mask_segmentation_v2.ipynb) | Exploratory U-Net and segmentation methods; uses mfm_image1 training inputs. |
| [mfm_image3/mask_segmentation.ipynb](../mfm_image3/mask_segmentation.ipynb) | Exploratory segmentation; saved runtime errors documented. |
| [mfm_relax_set1/Automate_strength_direction.ipynb](../mfm_relax_set1/Automate_strength_direction.ipynb) | Relaxed-configuration segmentation and moment extraction. |
| [mfm_relax_set1/Frustration_prediction.ipynb](../mfm_relax_set1/Frustration_prediction.ipynb) | Vertex classification, direction toggles, and paper-figure variants. |
| [mfm_relax_set1/VAE_generate_image.ipynb](../mfm_relax_set1/VAE_generate_image.ipynb) | MFM VAE training, loss tracking, reconstruction, and latent-space analysis. |
