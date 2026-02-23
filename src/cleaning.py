import pandas as pd
import logging
import os
from src.utils import load_config, should_skip

config = load_config()
logger = logging.getLogger(__name__)


def run_cleaning():
    output_path = config["paths"]["cleaned"]

    if should_skip(output_path, config):
        logger.info("Skipping cleaning")
        return

    df = pd.read_csv(config["paths"]["validated"])

    df["flat_model"] = df["flat_model"].str.upper()
    df["town"] = df["town"].str.upper()

    key_cols = [c for c in df.columns if c != "resale_price"]

    df = df.sort_values("resale_price", ascending=False)
    df = df.drop_duplicates(subset=key_cols)

    os.makedirs("data/cleaned", exist_ok=True)
    df.to_csv(output_path, index=False)

    logger.info("Cleaning completed")