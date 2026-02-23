import pandas as pd
import logging
import os
from src.utils import load_config, should_skip

config = load_config()
logger = logging.getLogger(__name__)


def run_anomaly():
    output_path = config["paths"]["anomalies"]

    if should_skip(output_path, config):
        logger.info("Skipping anomaly detection")
        return

    df = pd.read_csv(config["paths"]["cleaned"])

    Q1 = df["resale_price"].quantile(0.25)
    Q3 = df["resale_price"].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    anomalies = df[
        (df["resale_price"] < lower) |
        (df["resale_price"] > upper)
    ]

    os.makedirs("data/failed", exist_ok=True)
    anomalies.to_csv(output_path, index=False)

    logger.info(f"Anomalies: {len(anomalies)}")