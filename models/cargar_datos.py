import pandas as pd

def cargar_csv(csv_path: str) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(csv_path,dtype=str)
    
    columnas = list(df.columns)

    categoria_col = columnas[-2]
    resultado_col = columnas[-1]

    x = df.drop(columns=[categoria_col,resultado_col])
    y = df[categoria_col]

    print("----DATOS----\n",x)
    return (x,y)