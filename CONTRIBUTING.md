# Contributing

Please use GitHub issues to report problems, including the notebook name, cell, Python/package versions, expected behavior, and a small example when possible. Remove local paths and unpublished experimental data from logs before sharing them.

Keep changes to scientific methods separate from formatting or portability changes. Explain any change to segmentation thresholds, image preprocessing, train/validation splits, latent dimensions, loss functions, magnetic moment conventions, or frustration rules, and include the evidence used to assess it.

Before a pull request, clear notebook outputs and run the publication checks in a separate validation environment:

```bash
python3.11 -m venv .venv-checks
source .venv-checks/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/clean_notebooks.py
python scripts/validate_repository.py --require-schema
deactivate
```

The automated checks do not execute training or validate scientific conclusions. Describe any additional execution or numerical validation in the pull request. Dataset and checkpoint contributions should use a separately documented data release rather than incidental files in a code commit.
