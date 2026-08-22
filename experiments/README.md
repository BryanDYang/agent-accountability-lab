# Experiments

Each subdirectory here corresponds to a named experiment run.

## Running an experiment

```bash
python experiments/run_experiment.py --config configs/baseline.yaml
```

Results are written to `experiments/results/<experiment-name>/`.

## Structure

```
experiments/
├── run_experiment.py   # CLI entry point
└── results/            # Auto-created; gitignored (raw logs)
```
