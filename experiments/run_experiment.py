"""Experiment runner – placeholder for Milestone 0."""
import argparse
import yaml
from pathlib import Path


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Run an accountable-agents experiment.")
    parser.add_argument("--config", required=True, help="Path to a YAML config file.")
    args = parser.parse_args()

    config = load_config(args.config)
    output_dir = Path(config["logging"]["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loaded config: {args.config}")
    print(f"Output dir:    {output_dir}")
    print("Agent type:   ", config["agent"]["type"])
    print("\nExperiment runner not yet implemented – skeleton only.")


if __name__ == "__main__":
    main()
