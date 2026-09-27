import numpy as np
import pandas as pd
from pathlib import Path


def main():

    project_root = Path(__file__).resolve().parents[1]

    input_file = project_root / "data" / "calibrated_model_output.csv"
    output_file = project_root / "data" / "extreme_flow_summary.csv"

    df = pd.read_csv(input_file)
    df["date"] = pd.to_datetime(df["date"])

    discharge = df["calibrated_discharge"]

    # Percentile-based extreme flows
    q95 = discharge.quantile(0.95)
    q99 = discharge.quantile(0.99)

    # Annual maximum discharge
    annual_max = (
        df.groupby(df["date"].dt.year)["calibrated_discharge"]
        .max()
        .reset_index()
    )

    annual_max.columns = ["year", "annual_max_discharge"]

    annual_max.to_csv(output_file, index=False)

    print("Extreme-flow analysis complete")
    print(f"95th percentile discharge: {q95:.3f}")
    print(f"99th percentile discharge: {q99:.3f}")
    print(f"Maximum discharge: {discharge.max():.3f}")
    print()
    print("Annual maximum discharge:")
    print(annual_max.to_string(index=False))
    print()
    print(f"Saved: {output_file}")


if __name__ == "__main__":
    main()