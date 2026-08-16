from pathlib import Path

import pandas as pd


# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "gagea_afghanica_occurrences.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = PROCESSED_DIR / "gagea_afghanica_clean.csv"


# Read the raw dataset
data = pd.read_csv(RAW_FILE)

print(f"Original records: {len(data)}")


# Standardize species names
data["species"] = data["species"].astype(str).str.strip()


# Convert coordinates to numeric values
data["latitude"] = pd.to_numeric(data["latitude"], errors="coerce")
data["longitude"] = pd.to_numeric(data["longitude"], errors="coerce")


# Remove records with missing coordinates
data = data.dropna(subset=["latitude", "longitude"])


# Keep only geographically valid coordinates
data = data[
    data["latitude"].between(-90, 90)
    & data["longitude"].between(-180, 180)
]


# Remove exact duplicate occurrence records
data = data.drop_duplicates(
    subset=["species", "latitude", "longitude"]
).reset_index(drop=True)


# Create the processed-data folder if it does not exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# Save the cleaned dataset
data.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print(f"Clean records: {len(data)}")
print(f"Removed records: {194 - len(data)}")
print(f"Saved to: {OUTPUT_FILE}")
