from pathlib import Path

import geopandas as gpd
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

OUTPUT_FILE = (
    FIGURES_DIR
    / "gagea_afghanica_occurrences.png"
)


# Official Natural Earth country boundaries
BOUNDARY_URL = (
    "https://naturalearth.s3.amazonaws.com/"
    "110m_cultural/ne_110m_admin_0_countries.zip"
)


# Read the cleaned occurrence dataset
data = pd.read_csv(DATA_FILE)


# Convert occurrence records to spatial points
occurrences = gpd.GeoDataFrame(
    data,
    geometry=gpd.points_from_xy(
        data["longitude"],
        data["latitude"],
    ),
    crs="EPSG:4326",
)


# Read country boundaries
world = gpd.read_file(BOUNDARY_URL)


# Select countries intersecting the study extent
region = world.cx[62:73, 37:43]

uzbekistan = world[
    world["ADMIN"] == "Uzbekistan"
]


# Create the geographic map
fig, ax = plt.subplots(
    figsize=(10, 8),
)


# Plot neighbouring countries
region.plot(
    ax=ax,
    color="#F2EFE9",
    edgecolor="#666666",
    linewidth=0.8,
)


# Highlight Uzbekistan
uzbekistan.plot(
    ax=ax,
    color="#DCEFD8",
    edgecolor="#333333",
    linewidth=1.1,
)


# Plot occurrence records
occurrences.plot(
    ax=ax,
    color="#C62828",
    edgecolor="white",
    linewidth=0.35,
    markersize=32,
    alpha=0.85,
    label="Occurrence records",
)


# Map extent
ax.set_xlim(62.5, 72.5)
ax.set_ylim(37.0, 42.8)


# Map formatting
ax.set_title(
    "Geographic distribution of Gagea afghanica",
    fontsize=15,
    fontstyle="italic",
    pad=15,
)

ax.set_xlabel("Longitude (°E)")
ax.set_ylabel("Latitude (°N)")

ax.grid(
    linestyle="--",
    linewidth=0.4,
    alpha=0.4,
)

ax.legend(
    loc="lower left",
    frameon=True,
)

ax.text(
    0.98,
    0.02,
    f"Unique records: {len(occurrences)}",
    transform=ax.transAxes,
    ha="right",
    fontsize=10,
    bbox={
        "facecolor": "white",
        "alpha": 0.85,
        "edgecolor": "gray",
    },
)


# Save the map
FIGURES_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

plt.tight_layout()

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight",
)

plt.close()

print(
    f"Geographic map created from "
    f"{len(occurrences)} occurrence records."
)

print(f"Saved to: {OUTPUT_FILE}")
