"""
Recommendation Engine

Generates simple recommendations from benchmark results.
"""

from pathlib import Path
import pandas as pd

EXPORT_DIR = Path("data/exports")


def main():

    benchmark = pd.read_csv(
        EXPORT_DIR / "plant_benchmark.csv"
    )

    recommendations = []

    best = benchmark.iloc[0]
    worst = benchmark.iloc[-1]

    recommendations.append(
        f"🏆 Best performing plant: {best['plant']}"
    )

    recommendations.append(
        f"⚠ Highest energy consumer: {benchmark.sort_values('total_energy', ascending=False).iloc[0]['plant']}"
    )

    recommendations.append(
        f"🌱 Lowest CO₂ plant: {benchmark.sort_values('total_co2').iloc[0]['plant']}"
    )

    recommendations.append(
        f"📈 Improvement focus: {worst['plant']}"
    )

    with open(
        EXPORT_DIR / "recommendations.md",
        "w"
    ) as f:

        for rec in recommendations:
            f.write(f"- {rec}\n")

    print("\nRecommendations Generated")
    print(*recommendations, sep="\n")


if __name__ == "__main__":
    main()