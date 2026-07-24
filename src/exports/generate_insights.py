"""
Generate business insights from exported dashboard data.
"""

from pathlib import Path
import pandas as pd

EXPORT_DIR = Path("data/exports")

plants = pd.read_csv(EXPORT_DIR / "plants_summary.csv")
composition = pd.read_csv(EXPORT_DIR / "composition_summary.csv")
transport = pd.read_csv(EXPORT_DIR / "transport_summary.csv")

highest_material = plants.loc[
    plants["total_materials"].idxmax()
]

highest_transport = transport.loc[
    transport["avg_distance"].idxmax()
]

largest_product = composition.loc[
    composition["total_quantity"].idxmax()
]

lines = [
"# Industrial Energy & Sustainability Analytics",
"",
"## Key Insights",
"",
f"• **{highest_material['plant']}** has the highest total material consumption ({highest_material['total_materials']:.2f}).",
"",
f"• **{highest_transport['plant']}** has the highest average transport distance ({highest_transport['avg_distance']:.2f} km).",
"",
f"• **{largest_product['product']}** requires the largest total material input ({largest_product['total_quantity']:.2f}).",
"",
"## Recommendation",
"",
"- Review transportation routes for long-distance raw materials.",
"- Benchmark high-consumption plants against lower-consumption plants.",
"- Optimize material mix to improve energy efficiency.",
]

with open(EXPORT_DIR / "insights.md", "w") as f:
    f.write("\n".join(lines))

print("Generated insights.md")