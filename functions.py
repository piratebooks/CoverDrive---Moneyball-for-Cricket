#Contains all the reusable functions and variables for the project
from pathlib import Path
# Name says all I guess
BASE_PATH = Path(__file__).resolve().parent

OUTPUT_PATH_CLEANED = BASE_PATH / "Cleaned datasets"

RAW_DATASET_PATH = BASE_PATH / "Raw datasets"