from src.combine import run_combine
from src.validation import run_validation
from src.cleaning import run_cleaning
from src.transformation import run_transformation
from src.hashing import run_hashing
from src.anomaly import run_anomaly
from src.utils import load_config, setup_logger


def run_pipeline():
    config = load_config()
    logger = setup_logger(config["paths"]["logs"])

    logger.info("===== PIPELINE START =====")

    run_combine()
    run_validation()
    run_cleaning()
    run_transformation()
    run_hashing()
    run_anomaly()

    logger.info("===== PIPELINE COMPLETE =====")


if __name__ == "__main__":
    run_pipeline()