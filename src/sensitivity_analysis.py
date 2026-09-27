import numpy as np
import pandas as pd
from pathlib import Path

from karst_model import run_karst_model


def main():

    project_root = Path(__file__).resolve().parents[1]

    rainfall_file = project_root / "data" / "synthetic_rainfall.csv"
    output_file = project_root / "data" / "sensitivity_results.csv"

    df = pd.read_csv(rainfall_file)
    rainfall = df["rainfall_mm"].to_numpy()

    results = []

    # Test one parameter at a time around the baseline model
    parameter_ranges = {
        "recharge_fraction": [0.5, 0.6, 0.7, 0.8, 0.9],
        "fast_coefficient": [0.15, 0.25, 0.35, 0.45, 0.55],
        "slow_coefficient": [0.01, 0.02, 0.03, 0.04, 0.05],
        "fast_storage_capacity": [50, 75, 100, 125, 150],
        "slow_storage_capacity": [300, 400, 500, 600, 700],
    }

    baseline = {
        "recharge_fraction": 0.7,
        "fast_coefficient": 0.35,
        "slow_coefficient": 0.03,
        "fast_storage_capacity": 100.0,
        "slow_storage_capacity": 500.0,
    }

    for parameter, values in parameter_ranges.items():

        for value in values:

            parameters = baseline.copy()
            parameters[parameter] = value

            _, _, discharge = run_karst_model(
                rainfall,
                recharge_fraction=parameters["recharge_fraction"],
                fast_coefficient=parameters["fast_coefficient"],
                slow_coefficient=parameters["slow_coefficient"],
                fast_storage_capacity=parameters["fast_storage_capacity"],
                slow_storage_capacity=parameters["slow_storage_capacity"],
            )

            results.append({
                "parameter": parameter,
                "value": value,
                "q95": np.percentile(discharge, 95),
                "q99": np.percentile(discharge, 99),
                "maximum": discharge.max(),
                "mean": discharge.mean(),
            })

    results_df = pd.DataFrame(results)

    results_df.to_csv(output_file, index=False)

    print("Sensitivity analysis complete")
    print(f"Parameter combinations tested: {len(results_df)}")
    print()
    print(results_df.to_string(index=False))
    print()
    print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()