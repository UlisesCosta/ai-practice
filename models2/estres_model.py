import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import os
from cargar_datos import cargar_csv

def construir_preprocesador(df: pd.DataFrame) -> ColumnTransformer:
    columnas_categoricas = ["instituto", "carrera"]
    columnas_numericas = [col for col in df.columns 
                          if col not in columnas_categoricas + ["categoria", "resultado"]]

    preprocessor = ColumnTransformer(
        transformers=[
            ("categoricas", OneHotEncoder(handle_unknown="ignore"), columnas_categoricas),
            ("numericas", StandardScaler(), columnas_numericas),
        ]
    )
    return preprocessor


def entrenar_knn(df: pd.DataFrame):
    X = df.drop(columns=["categoria", "resultado"])
    y = df["categoria"]

    preprocessor = construir_preprocesador(df)

    pipe = Pipeline(steps=[
        ("preprocesador", preprocessor),
        ("knn", KNeighborsClassifier())
    ])

    parametros = {
        "knn__n_neighbors": [3, 5, 7, 9],
        "knn__weights": ["uniform", "distance"],
        "knn__metric": ["minkowski", "euclidean", "manhattan"]
    }

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    grid = GridSearchCV(
        pipe, parametros, cv=2, n_jobs=-1, scoring="accuracy"
    )

    grid.fit(X_train, y_train)
    print(f"\n Resultados del GridSearchCV: Mejor score: {grid.best_score_}")
    print(" Mejor modelo encontrado:")
    print(grid.best_params_)

    return grid, X_test, y_test


def obtener_matriz_confusion(modelo, X_test, y_test):
    pred = modelo.predict(X_test)
    matriz = confusion_matrix(y_test, pred)
    print("\n Clasification Report:")
    print(classification_report(y_test, pred))
    print("\n Matriz de Confusión:")
    print(matriz)
    return matriz


def graficar_matriz_confusion(matriz, titulo="Matriz de Confusión"):
    plt.figure(figsize=(7,5))
    sns.heatmap(matriz, annot=True, fmt="d", cmap="Blues")
    plt.title(titulo)
    plt.xlabel("Predicción")
    plt.ylabel("Valor real")
    plt.show()

df = cargar_csv("../outputs_csvs/estres.csv")
grid, X_test, y_test = entrenar_knn(df)
matriz = obtener_matriz_confusion(grid, X_test, y_test)
graficar_matriz_confusion(matriz, "Matriz de Confusión Estres")