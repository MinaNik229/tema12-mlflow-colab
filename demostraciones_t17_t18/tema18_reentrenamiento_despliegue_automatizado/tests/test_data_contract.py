from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"signal_1", "signal_2", "signal_3", "target"}


def load(name):
    path = ROOT / "data" / name
    assert path.exists(), f"Falta {path}. Ejecuta data/generate_data.py"
    return pd.read_csv(path)


def test_training_schema_and_nulls():
    data = load("train.csv")
    assert set(data.columns) == EXPECTED
    assert not data.isnull().any().any()
    assert len(data) >= 100


def test_production_batch_schema_and_nulls():
    data = load("production_batch.csv")
    assert set(data.columns) == EXPECTED
    assert not data.isnull().any().any()
    assert len(data) >= 50
