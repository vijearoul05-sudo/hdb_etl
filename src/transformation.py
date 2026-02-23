import pandas as pd
import logging
import os
from src.utils import load_config, should_skip

config = load_config()
logger = logging.getLogger(__name__)


def run_transformation():
    output_path = config["paths"]["transformed"]

    if should_skip(output_path, config):
        logger.info("Skipping transformation")
        return

    df = pd.read_csv(config["paths"]["cleaned"])

    df["month"] = pd.to_datetime(df["month"])

    avg_df = df.groupby(
        ["month", "town", "flat_type"]
    )["resale_price"].mean().reset_index()

    avg_df["prefix"] = avg_df["resale_price"].astype(int).astype(str).str[:2]

    df = df.merge(avg_df, on=["month", "town", "flat_type"])

    df["block_num"] = df["block"].str.extract(r"(\d+)")[0].str.zfill(3)
    df["month_num"] = df["month"].dt.month.astype(str).str.zfill(2)
    df["town_char"] = df["town"].str[0]

    df["resale_id"] = (
        "S"
        + df["block_num"]
        + df["prefix"]
        + df["month_num"]
        + df["town_char"]
    )

    os.makedirs("data/transformed", exist_ok=True)
    df.to_csv(output_path, index=False)

    logger.info("Transformation completed")