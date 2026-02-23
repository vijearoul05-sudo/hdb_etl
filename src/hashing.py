import pandas as pd
import hashlib
import logging
import os
from src.utils import load_config, should_skip

config = load_config()
logger = logging.getLogger(__name__)


def run_hashing():
    output_path = config["paths"]["hashed"]

    if should_skip(output_path, config):
        logger.info("Skipping hashing")
        return

    df = pd.read_csv(config["paths"]["transformed"])

    df["hashed_id"] = df["resale_id"].apply(
        lambda x: hashlib.sha256(x.encode()).hexdigest()
    )

    os.makedirs("data/hashed", exist_ok=True)
    df.to_csv(output_path, index=False)

    logger.info("Hashing completed")