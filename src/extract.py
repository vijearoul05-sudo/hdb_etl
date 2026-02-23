import requests
import os
import time
import logging
from src.utils import load_config

config = load_config()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_with_retry(url, max_retries=5, wait=5):
    for attempt in range(1, max_retries + 1):
        response = safe_request(url)

        if response.status_code == 429:
            print(f"Rate limited. Waiting {wait}s (Attempt {attempt})...")
            time.sleep(wait)
            wait *= 2  # exponential backoff
            continue

        response.raise_for_status()
        return response

    raise Exception("Max retries exceeded")

def safe_request(url, max_retries=6, wait=5):
    headers = {"User-Agent": "Mozilla/5.0"}

    for attempt in range(1, max_retries + 1):
        response = requests.get(url, headers=headers)

        if response.status_code == 429:
            print(f"[429] Rate limited. Waiting {wait}s (Attempt {attempt})...")
            time.sleep(wait)
            wait *= 2  # exponential backoff
            continue

        response.raise_for_status()
        return response

    raise Exception("Max retries exceeded due to rate limiting")


def get_dataset_ids():
    url = f"{config['collection']['metadata_url']}/collections/{config['collection']['id']}/metadata"

    response = get_with_retry(url)
    data = response.json()

    return data["data"]["collectionMetadata"]["childDatasets"]


def match_datasets(dataset_ids):
    matched = {}

    for ds_id in dataset_ids:
        url = f"{config['collection']['metadata_url']}/datasets/{ds_id}/metadata"
        response = get_with_retry(url)

        name = response.json()["data"]["name"]

        for keywords in config["extraction"]["keywords"]:
            if all(k.lower() in name.lower() for k in keywords):
                filename = (
                    name.replace(" ", "_")
                        .replace(",", "")
                        .replace("(", "")
                        .replace(")", "")
                    + ".csv"
                )

                matched[ds_id] = (name, filename)
                logger.info(f"Matched dataset: {name}")

    return matched


def download_dataset(dataset_id, filename):
    os.makedirs(config["paths"]["raw"], exist_ok=True)

    base_url = config["dataset_api"]["base_url"]

    # Step 1: initiate
    init_url = f"{base_url}/{dataset_id}/initiate-download"
    response = safe_request(init_url)
    response.raise_for_status()

    time.sleep(2)

    # Step 2: poll
    download_url = None

    for _ in range(config["extraction"]["polling"]["attempts"]):
        poll_url = f"{base_url}/{dataset_id}/poll-download"
        response = safe_request(poll_url)
        data = response.json()

        download_url = data.get("data", {}).get("url")

        if download_url:
            break

        time.sleep(config["extraction"]["polling"]["interval_seconds"])

    if not download_url:
        raise Exception("Download URL not ready")

    # Step 3: download file
    file_path = os.path.join(config["paths"]["raw"], filename)

    logger.info(f"Downloading: {filename}")

    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

    logger.info(f"Saved: {file_path}")


def run_extraction():
    logger.info("Starting extraction...")

    dataset_ids = get_dataset_ids()
    matched = match_datasets(dataset_ids)

    if not matched:
        logger.warning("No datasets matched.")
        return

    for i, (ds_id, (name, filename)) in enumerate(matched.items(), 1):
        logger.info(f"[{i}/{len(matched)}] {name}")
        download_dataset(ds_id, filename)

        if i < len(matched):
            time.sleep(5)

    logger.info("Extraction complete.")