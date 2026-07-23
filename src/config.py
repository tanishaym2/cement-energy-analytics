from pathlib import Path

# Project Root
ROOT_DIR = Path(__file__).resolve().parent.parent

# Data Directories
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

# Other Directories
EXPORT_DIR = ROOT_DIR / "exports"
DATABASE_DIR = ROOT_DIR / "database"
MODEL_DIR = ROOT_DIR / "models"

# Dataset
WORKBOOK_PATH = RAW_DIR / "DiB - Cement Plant data.xlsx"

# SQLite
DATABASE_PATH = DATABASE_DIR / "cement_analytics.db"