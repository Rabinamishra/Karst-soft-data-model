import numpy as np
import pandas as pd
from pathlib import Path


# Reproducible random numbers
rng = np.random.default_rng(42)

# 10 years of daily data
dates = pd.date_range("2015-01-01", "2024-12-31", freq="D")

# Seasonal rainfall pattern
day_of_year = dates.dayofyear

seasonal_factor = (
    0.25
    + 0.75 * np.maximum(
        0,
        np.sin(2 * np.pi * (day_of_year - 90) / 365)
    )
)

# Probability of a rainy day
rain_probability = 0.25 + 0.25 * seasonal_factor

rainy_day = rng.random(len(dates)) < rain_probability

# Gamma-distributed rainfall amounts
rainfall = np.zeros(len(dates))

rainfall[rainy_day] = rng.gamma(
    shape=1.8,
    scale=8.0,
    size=rainy_day.sum()
)

# Add occasional intense rainfall events
extreme_days = rng.random(len(dates)) < 0.01

rainfall[extreme_days] += rng.gamma(
    shape=2.5,
    scale=30.0,
    size=extreme_days.sum()
)

# Create dataframe
df = pd.DataFrame({
    "date": dates,
    "rainfall_mm": rainfall
})

# Save
output_path = Path(__file__).resolve().parents[1] / "data" / "synthetic_rainfall.csv"
output_path.parent.mkdir(exist_ok=True)

df.to_csv(output_path, index=False)

print(f"Saved: {output_path}")
print(f"Days: {len(df)}")
print(f"Total rainfall: {df['rainfall_mm'].sum():.1f} mm")
print(f"Maximum daily rainfall: {df['rainfall_mm'].max():.1f} mm")