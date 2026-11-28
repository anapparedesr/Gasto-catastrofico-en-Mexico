"""Definición única de la variable objetivo: gasto catastrófico en salud.

Gasto catastrófico = 1 si salud / ingreso disponible > 0.30

    ingreso monetario  = ing_cor - (estim_alqu + remu_espec + transf_hog + trans_inst)
    ingreso disponible = ingreso monetario - ali_dentro

Los cuatro componentes que se restan de ing_cor son los no monetarios: según el catálogo
ENIGH 2024 (tabla CONCENTRADOHOGAR) se construyen con gas_nm_tri, es decir, con la tabla de
gasto no monetario (alquiler estimado, remuneraciones en especie y transferencias en especie).
El resto de los componentes de ing_cor sale de ingresos.ing_tri (ingreso monetario).

Se excluyen los hogares con ingreso disponible <= 0 (la razón no es interpretable).
"""
import pandas as pd

UMBRAL = 0.30
COMPONENTES_NO_MONETARIOS = ["estim_alqu", "remu_espec", "transf_hog", "trans_inst"]


def construir_etiqueta(df: pd.DataFrame, excluir: bool = True) -> pd.DataFrame:
    out = df.copy()
    # round(2) evita residuos de punto flotante (p. ej. -1e-10) al restar
    out["ing_monetario"] = (
        out["ing_cor"] - out[COMPONENTES_NO_MONETARIOS].sum(axis=1)
    ).round(2)
    out["ing_disponible"] = out["ing_monetario"] - out["ali_dentro"]
    valido = out["ing_disponible"] > 0

    razon = out["salud"] / out["ing_disponible"].where(valido)
    out["razon_salud"] = razon
    out["gasto_catastrofico"] = (razon > UMBRAL).astype("Int8").where(valido)

    n_excl = (~valido).sum()
    print(f"Hogares con ingreso disponible <= 0: {n_excl:,} ({n_excl / len(out):.2%})")
    return out[valido].copy() if excluir else out