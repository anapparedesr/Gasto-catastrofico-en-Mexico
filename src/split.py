"""Genera el split train/test a nivel hogar. Se corre UNA sola vez."""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

RAW = Path("data/raw/concentradohogar.csv")
OUT = Path("data/interim")
SEMILLA = 42
PROP_TEST = 0.20


def main():
    # Los folios deben leerse como texto para no perder ceros a la izquierda
    df = pd.read_csv(RAW, dtype={"folioviv": str, "foliohog": str, "ubica_geo": str})
    df["folioviv"] = df["folioviv"].str.zfill(10)
    df["id_hogar"] = df["folioviv"] + df["foliohog"]
    assert df["id_hogar"].is_unique, "Hay id_hogar duplicados"

    # Estratificamos por entidad (primeros 2 dígitos del folio de vivienda)
    entidad = df["folioviv"].str[:2]

    train, test = train_test_split(
        df, test_size=PROP_TEST, random_state=SEMILLA, stratify=entidad
    )
    assert set(train["id_hogar"]).isdisjoint(test["id_hogar"])

    OUT.mkdir(parents=True, exist_ok=True)
    train.to_parquet(OUT / "train.parquet", index=False)
    test.to_parquet(OUT / "test.parquet", index=False)
    print(f"Total: {len(df):,} | train: {len(train):,} | test: {len(test):,}")


if __name__ == "__main__":
    main()