import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

input_file = PROJECT_ROOT / "data" / "sensitivity_results.csv"
output_file = PROJECT_ROOT / "figures" / "parameter_sensitivity.png"

df = pd.read_csv(input_file)

fig, ax = plt.subplots(figsize=(10, 6))

for parameter in ["recharge_fraction", "fast_coefficient", "slow_coefficient"]:
    subset = df[df["parameter"] == parameter]

    ax.plot(
        subset["value"],
        subset["maximum"],
        marker="o",
        linewidth=1.5,
        label=parameter.replace("_", " ").title()
    )

ax.set_xlabel("Parameter value")
ax.set_ylabel("Maximum modeled discharge")
ax.set_title("Sensitivity of Extreme Flow to Key Model Parameters")

ax.grid(alpha=0.3)
ax.legend()

fig.tight_layout()

fig.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"Saved: {output_file}")