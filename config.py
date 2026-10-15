from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
DATA_PATH = DATA_DIR / "electricity_consumption.csv"
PROCESSED_PATH = OUTPUT_DIR / "processed_electricity_data.csv"

RANDOM_SEED = 42
CONTAMINATION = 0.04
COLLEGE_WORKING_START = 8
COLLEGE_WORKING_END = 18

BUILDINGS = [
    "Engineering Block",
    "Computer Lab 1",
    "Computer Lab 2",
    "Library",
    "Administration Block",
    "Workshop",
    "Canteen",
    "Seminar Hall",
    "Classroom Block",
    "Hostel A",
    "Hostel B",
]

HOLIDAY_DATES = {
    "2025-01-26",
    "2025-02-26",
    "2025-03-15",
    "2025-03-31",
    "2025-04-10",
    "2025-05-01",
    "2025-06-15",
    "2025-08-15",
    "2025-09-05",
    "2025-10-02",
    "2025-11-14",
    "2025-12-25",
}

REQUIRED_COLUMNS = [
    "Record_ID",
    "Date",
    "Time",
    "Building",
    "Consumption_kWh",
    "Occupancy",
    "Temperature_C",
    "Day_of_Week",
    "Day_Type",
    "Working_Hours",
    "Previous_Consumption_kWh",
]
