import json
import logging
from pathlib import Path

import pandas as pd
import yaml
import os
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

def inspect_csv(filepath):
    """Read a CSV file and display basic information."""
    file = pd.read_csv(filepath)
    logger.info(f"Inspecting CSV: {filepath}")
    print(file.head(3))


def inspect_json(filepath):
    """Read a JSON file and display basic information."""
    with open(filepath, "r") as file:
        data = json.load(file)
    logger.info(f"Inspecting JSON: {filepath}")
    print(data)


def inspect_yaml(filepath):
    """Read a YAML file and display basic information."""
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)
    logger.info(f"Inspecting YAML: {filepath}")
    print(config)


def inspect_env():
    """Read a .env file and display basic information."""
    load_dotenv()

    keys = [
        key for key in ["USERNAME", "PASSWORD"]
        if os.getenv(key) is not None
    ]

    logger.info("Loaded environment variables from .env")
    print(keys)

def main():
    data_dir = Path('data')
    csvf = data_dir / 'sample.csv'
    jsonf = data_dir / 'sample.json'
    yamlf = data_dir / 'sample.yaml'
    envf = data_dir / '.env'

    inspect_csv(csvf)
    inspect_json(jsonf)
    inspect_yaml(yamlf)
    inspect_env()

if __name__ == "__main__":
    main()
