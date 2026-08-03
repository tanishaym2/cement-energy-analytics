from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Industrial Energy Analytics API"}

@app.get("/plant-performance")
def plant_performance():
    df = pd.read_csv("data/exports/plant_performance.csv")
    return df.to_dict(orient="records")

@app.get("/dashboard")
def dashboard():
    df = pd.read_csv("data/exports/dashboard_kpis.csv")
    return df.to_dict(orient="records")

@app.get("/energy")
def energy():
    df = pd.read_csv("data/exports/energy_analysis.csv")
    return df.to_dict(orient="records")

@app.get("/transport")
def transport():
    df = pd.read_csv("data/exports/transport_analysis.csv")
    return df.to_dict(orient="records")

@app.get("/co2")
def co2():
    df = pd.read_csv("data/exports/co2_analysis.csv")
    return df.to_dict(orient="records")

@app.get("/materials")
def materials():
    df = pd.read_csv("data/exports/material_summary.csv")
    return df.to_dict(orient="records")

@app.get("/benchmark")
def benchmark():
    df = pd.read_csv("data/exports/plant_benchmark.csv")
    return df.to_dict(orient="records")