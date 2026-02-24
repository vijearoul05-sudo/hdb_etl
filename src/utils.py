import yaml
from pathlib import Path
import logging
import os


def load_config(path="config/config.yaml"):
    # Get project root (one level above src/)
    project_root = Path(__file__).resolve().parent.parent

    config_path = project_root / path

    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def setup_logger(log_path):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_path)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def should_skip(path, config):
    return config["pipeline"]["skip_if_exists"] and os.path.exists(path)