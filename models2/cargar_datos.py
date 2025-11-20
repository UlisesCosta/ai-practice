import pandas as pd
import os
def cargar_csv(ruta: str) -> pd.DataFrame:
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    df = pd.read_csv(ruta)
    return df


