"""
KPI Engine for Industrial Energy & Sustainability Analytics
"""

import sqlite3
import pandas as pd

DB_PATH = "data/cement.db"


class KPIEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DB_PATH)

    def inventory(self):

        return pd.read_sql(
            "SELECT * FROM inventory",
            self.conn
        )

    def composition(self):

        return pd.read_sql(
            "SELECT * FROM composition",
            self.conn
        )

    def transport(self):

        return pd.read_sql(
            "SELECT * FROM transport",
            self.conn
        )

    def emission_factors(self):

        return pd.read_sql(
            "SELECT * FROM emission_factors",
            self.conn
        )


if __name__ == "__main__":

    kpi = KPIEngine()

    inventory = kpi.inventory()
    composition = kpi.composition()
    transport = kpi.transport()
    factors = kpi.emission_factors()

    print("Inventory:", inventory.shape)
    print("Composition:", composition.shape)
    print("Transport:", transport.shape)
    print("Factors:", factors.shape)