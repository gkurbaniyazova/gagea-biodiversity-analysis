from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# Project folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "gagea_afghanica_clean.csv"
)
FIGURES_DIR = PROJECT_ROOT / "figures"
OUTPUT_FILE = FIGURES_DIR / "gagea_afghanica_occurrences.png"


# Read the cleaned occurrence dataset
data = pd.read_csv(DATA_FILE)


# Create the occurrence map
fig, ax = plt.subplots(figsize=(9, 7))

ax.scatter(
    data["longitude"],
    data["latitude"],
    s=30,
    color="#2E7D32",
    edgecolor="white",
    linewidth=0.4,
    alpha=0.8,
)


# Map formatting
ax.set_title(
    "Occurrence records of Gagea afghanica",
    fontsize=15,
    fontstyle="italic",
    pad=15,
)

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.grid(
    linestyle="--",
    linewidth=0.5,
    alpha=0.5,
)

ax.text(
    0.02,
    0.02,
    f"Unique records: {len(data)}",
    transform=ax.transAxes,
    fontsize=10,
    bbox={
        "facecolor": "white",
        "alpha": 0.8,
        "edgecolor": "gray",
    },
)


# Save the figure
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
plt.tight_layout()
plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight",
)
plt.close()

print(f"Map created from {len(data)} occurrence records.")
print(f"Saved to: {OUTPUT_FILE}")
