import numpy as np
import pandas as pd
from pathlib import Path

from karst_model import run_karst_model


def soft_data_metrics(rainfall, discharge):
    """
    Convert qualitative hydrogeological observations into
    simple quantitative response metrics.

    Soft-data concepts:
    1. Rapid response after intense rainfall.
    2. Strong event response.
    3. Gradual recession after rainfall.
    """

    extreme_threshold = np.percentile(rainfall, 99)
    extreme_events = np.where(rainfall >= extreme_threshold)[0]

    rapid_responses = []

    for i in extreme_events:
        if i + 3 < len(discharge):
            event_peak = np.max(discharge[i:i + 4])
            rapid_responses.append(event_peak)

    rapid_response = (
        np.mean(rapid_responses)
        if rapid_responses
        else 0.0
    )

    # Fraction of days showing non-increasing discharge.
    # This represents the prevalence of recession behavior.
    daily_change = np.diff(discharge)
    recession_fraction = np.mean(daily_change <= 0)

    # Normalize the two components so they can be combined.
    response_score = rapid_response / np.max(discharge)

    recession_score = recession_fraction

    return response_score, recession_score


def objective(params, rainfall):
    """
    Conceptual objective function combining soft-data constraints.
    """

    recharge_fraction, fast_coefficient, slow_coefficient = params

    _, _, discharge = run_karst_model(
        rainfall,
        recharge_fraction=recharge_fraction,
        fast_coefficient=fast_coefficient,
        slow_coefficient=slow_coefficient,
    )

    response_score, recession_score = soft_data_metrics(
        rainfall,
        discharge
    )

    # Equal weighting of rapid-response and recession behavior.
    score = (
        0.5 * response_score
        + 0.5 * recession_score
    )

    return score, discharge, response_score, recession_score


def main():

    project_root = Path(__file__).resolve().parents[1]

    rainfall_file = project_root / "data" / "synthetic_rainfall.csv"
    output_file = project_root / "data" / "calibration_results.csv"
    calibrated_file = project_root / "data" / "calibrated_model_output.csv"

    df = pd.read_csv(rainfall_file)
    rainfall = df["rainfall_mm"].to_numpy()

    results = []

    for recharge in [0.5, 0.6, 0.7, 0.8, 0.9]:
        for fast in [0.15, 0.25, 0.35, 0.45, 0.55]:
            for slow in [0.01, 0.03, 0.05]:

                params = (recharge, fast, slow)

                score, discharge, response, recession = objective(
                    params,
                    rainfall
                )

                results.append({
                    "recharge_fraction": recharge,
                    "fast_coefficient": fast,
                    "slow_coefficient": slow,
                    "soft_data_score": score,
                    "rapid_response_score": response,
                    "recession_score": recession,
                    "maximum_discharge": discharge.max(),
                    "q95": np.percentile(discharge, 95),
                    "q99": np.percentile(discharge, 99),
                })

    results_df = pd.DataFrame(results)

    best_index = results_df["soft_data_score"].idxmax()
    best = results_df.loc[best_index]

    # Re-run the selected parameter set
    _, _, calibrated_discharge = run_karst_model(
        rainfall,
        recharge_fraction=best["recharge_fraction"],
        fast_coefficient=best["fast_coefficient"],
        slow_coefficient=best["slow_coefficient"],
    )

    df["calibrated_discharge"] = calibrated_discharge

    results_df.to_csv(output_file, index=False)
    df.to_csv(calibrated_file, index=False)

    print("Soft-data calibration complete")
    print()
    print("Selected parameters:")
    print(f"Recharge fraction: {best['recharge_fraction']}")
    print(f"Fast coefficient: {best['fast_coefficient']}")
    print(f"Slow coefficient: {best['slow_coefficient']}")
    print()
    print(f"Soft-data score: {best['soft_data_score']:.4f}")
    print(f"Rapid-response score: {best['rapid_response_score']:.4f}")
    print(f"Recession score: {best['recession_score']:.4f}")
    print()
    print(f"Q95: {best['q95']:.3f}")
    print(f"Q99: {best['q99']:.3f}")
    print(f"Maximum discharge: {best['maximum_discharge']:.3f}")
    print()
    print(f"Saved: {output_file}")
    print(f"Saved: {calibrated_file}")


if __name__ == "__main__":
    main()