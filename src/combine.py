import pandas as pd
import glob
import os
import logging
from src.utils import load_config, should_skip

config = load_config()
logger = logging.getLogger(__name__)


def run_combine():
    output_path = config["paths"]["combined"]

    if should_skip(output_path, config):
        logger.info("Skipping combine")
        return

    files = glob.glob(os.path.join(config["paths"]["raw"], "*.csv"))

    df_list = []

    for file in files:
        logger.info(f"Reading {file}")
        df = pd.read_csv(file)

        if "remaining_lease" not in df.columns:
            df["remaining_lease"] = None

        df_list.append(df)

    df = pd.concat(df_list, ignore_index=True)

    df["month"] = pd.to_datetime(df["month"], errors="coerce")

    df = df[
        (df["month"] >= "2012-01-01") &
        (df["month"] <= "2016-12-31")
    ]

    os.makedirs("data/combined", exist_ok=True)
    df.to_csv(output_path, index=False)

    logger.info("Combine completed")