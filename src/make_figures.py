import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data"
FIGURES = PROJECT_ROOT / "figures"

FIGURES.mkdir(exist_ok=True)


# Load model output
df = pd.read_csv(DATA / "calibrated_model_output.csv")
df["date"] = pd.to_datetime(df["date"])


# -----------------------------
# Figure 1: Rainfall and discharge
# -----------------------------
fig, ax1 = plt.subplots(figsize=(11, 5))

ax1.plot(
    df["date"],
    df["rainfall_mm"],
    linewidth=0.7,
    alpha=0.6,
    label="Rainfall"
)

ax1.set_xlabel("Date")
ax1.set_ylabel("Rainfall (mm/day)")

ax2 = ax1.twinx()

ax2.plot(
    df["date"],
    df["calibrated_discharge"],
    linewidth=0.9,
    label="Modeled discharge"
)

ax2.set_ylabel("Modeled discharge")

ax1.set_title(
    "Synthetic Rainfall and Modeled Karst Spring Response"
)

fig.tight_layout()

fig.savefig(
    FIGURES / "rainfall_discharge_timeseries.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# -----------------------------
# Figure 2: Annual maximum flow
# -----------------------------
annual_max = (
    df.groupby(df["date"].dt.year)["calibrated_discharge"]
    .max()
)

fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(
    annual_max.index,
    annual_max.values,
    marker="o",
    linewidth=1.5
)

ax.set_xlabel("Year")
ax.set_ylabel("Annual maximum modeled discharge")

ax.set_title(
    "Annual Maximum Modeled Discharge"
)

ax.grid(alpha=0.3)

fig.tight_layout()

fig.savefig(
    FIGURES / "annual_maximum_discharge.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# -----------------------------
# Figure 3: Fast vs slow pathways
# -----------------------------
model = pd.read_csv(DATA / "karst_model_output.csv")
model["date"] = pd.to_datetime(model["date"])

# Show one representative year
subset = model[
    (model["date"] >= "2020-01-01") &
    (model["date"] <= "2020-12-31")
]

fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(
    subset["date"],
    subset["fast_discharge"],
    label="Fast pathway",
    linewidth=1
)

ax.plot(
    subset["date"],
    subset["slow_discharge"],
    label="Slow pathway",
    linewidth=1
)

ax.plot(
    subset["date"],
    subset["total_discharge"],
    label="Total discharge",
    linewidth=1.2
)

ax.set_xlabel("Date")
ax.set_ylabel("Modeled discharge")

ax.set_title(
    "Fast and Slow Karst Flow Components"
)

ax.legend()
ax.grid(alpha=0.3)

fig.tight_layout()

fig.savefig(
    FIGURES / "fast_slow_flow_components.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("Figures created:")
print("1. rainfall_discharge_timeseries.png")
print("2. annual_maximum_discharge.png")
print("3. fast_slow_flow_components.png")