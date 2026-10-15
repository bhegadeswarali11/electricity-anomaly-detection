from pathlib import Path

import pandas as pd

from config import DATA_PATH
from generate_data import generate_dataset


def load_dataset(data_path=DATA_PATH):
    """Load the CSV dataset, creating it if it does not exist."""
    data_path = Path(data_path)
    if not data_path.exists():
        generate_dataset(force_overwrite=False, output_path=data_path)

    df = pd.read_csv(data_path)
    if df.empty:
        raise ValueError("Dataset is empty. Please regenerate the file.")
    return df
