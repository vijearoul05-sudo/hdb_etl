import pandas as pd
import os
import logging
from src.utils import load_config, should_skip

config = load_config()
logger = logging.getLogger(__name__)


def run_validation():
    output_valid = config["paths"]["validated"]
    output_failed = config["paths"]["failed_validation"]

    if should_skip(output_valid, config):
        logger.info("Skipping validation")
        return

    df = pd.read_csv(config["paths"]["combined"])

    valid = []
    failed = []

    for _, row in df.iterrows():
        try:
            if pd.isna(row["month"]):
                raise Exception("Invalid month")

            if "TO" not in row["storey_range"]:
                raise Exception("Invalid storey")

            valid.append(row)
        except:
            failed.append(row)

    valid_df = pd.DataFrame(valid)
    failed_df = pd.DataFrame(failed)

    os.makedirs("data/cleaned", exist_ok=True)
    os.makedirs("data/failed", exist_ok=True)

    valid_df.to_csv(output_valid, index=False)
    failed_df.to_csv(output_failed, index=False)

    logger.info(f"Valid: {len(valid_df)}, Failed: {len(failed_df)}")