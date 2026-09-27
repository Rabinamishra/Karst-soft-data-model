import numpy as np
import pandas as pd
from pathlib import Path


def run_karst_model(
    rainfall,
    recharge_fraction=0.7,
    fast_coefficient=0.35,
    slow_coefficient=0.03,
    fast_storage_capacity=100.0,
    slow_storage_capacity=500.0,
):
    """
    Conceptual two-component karst rainfall-flow model.

    Fast component:
        Represents rapid conduit/macropore response.

    Slow component:
        Represents delayed matrix/storage response.

    Parameters are conceptual and have no direct physical units
    corresponding to a specific real karst catchment.
    """

    fast_storage = 0.0
    slow_storage = 0.0

    fast_discharge = []
    slow_discharge = []
    total_discharge = []

    for rain in rainfall:

        recharge = rain * recharge_fraction

        # Partition recharge between fast and slow pathways
        fast_input = 0.65 * recharge
        slow_input = 0.35 * recharge

        # Update storages
        fast_storage += fast_input
        slow_storage += slow_input

        # Calculate discharge
        q_fast = fast_coefficient * fast_storage
        q_slow = slow_coefficient * slow_storage

        # Prevent discharge from exceeding available storage
        q_fast = min(q_fast, fast_storage)
        q_slow = min(q_slow, slow_storage)

        # Update storage after discharge
        fast_storage -= q_fast
        slow_storage -= q_slow

        # Apply conceptual storage limits
        fast_storage = min(fast_storage, fast_storage_capacity)
        slow_storage = min(slow_storage, slow_storage_capacity)

        fast_discharge.append(q_fast)
        slow_discharge.append(q_slow)
        total_discharge.append(q_fast + q_slow)

    return (
        np.array(fast_discharge),
        np.array(slow_discharge),
        np.array(total_discharge),
    )


def main():

    project_root = Path(__file__).resolve().parents[1]

    rainfall_file = project_root / "data" / "synthetic_rainfall.csv"
    output_file = project_root / "data" / "karst_model_output.csv"

    # Load rainfall
    rainfall_df = pd.read_csv(rainfall_file)

    rainfall = rainfall_df["rainfall_mm"].to_numpy()

    # Run model
    fast_q, slow_q, total_q = run_karst_model(rainfall)

    # Store results
    output = rainfall_df.copy()

    output["fast_discharge"] = fast_q
    output["slow_discharge"] = slow_q
    output["total_discharge"] = total_q

    output.to_csv(output_file, index=False)

    print(f"Saved: {output_file}")
    print(f"Days simulated: {len(output)}")
    print(f"Maximum discharge: {output['total_discharge'].max():.3f}")
    print(f"Mean discharge: {output['total_discharge'].mean():.3f}")


if __name__ == "__main__":
    main()