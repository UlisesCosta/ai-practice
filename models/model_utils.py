from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
import pandas as pd



def construir_prepocesador(columnas_categoricas) -> ColumnTransformer:
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), columnas_categoricas)
        ]
    )
    return preprocessor



def construir_pipe(preprocessor: ColumnTransformer)-> Pipeline:
    pipe = Pipeline(steps=[
        ("onehot", preprocessor),
        ("scaler", StandardScaler(with_mean=False)),
        ("knn", KNeighborsClassifier())
    ])
    return pipe



def dividir_datos(x: pd.DataFrame,y: pd.Series , test_size = 0.2) -> list:
    return train_test_split(x, y, test_size=test_size, random_state=42)


def entrenar_knn_gridSearch(pipeline: Pipeline, 
                            x_train: pd.DataFrame, y_train: pd.Series, ) -> GridSearchCV:
    param_grid = {
        "knn__n_neighbors": [3, 5, 7, 9,11,],
        "knn__weights": ["uniform", "distance"],
        "knn__metric": ["euclidean", "manhattan"]
    }

    grid = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        cv=2,
        scoring="accuracy",
        n_jobs=-1)

    grid.fit(x_train, y_train)

    return grid



def preparar_y_entrenar_knn(x: pd.DataFrame, y: pd.Series) -> tuple[GridSearchCV, pd.DataFrame, pd.Series]:

    #preprocesamos los datos
    preprocesador = construir_prepocesador(x.columns.tolist())

    #creamos el pipeline
    pipe = construir_pipe(preprocesador)

    #dividimos los datos
    x_train, x_test, y_train, y_test = dividir_datos(x, y)

    #entrenamos el modelo
    grid = entrenar_knn_gridSearch(pipe, x_train, y_train)

    print(f"Mejores parámetros: {grid.best_params_}")  # Imprimir los mejores parámetrosgrid.best_params_)

    print(f"Mejor score: {grid.best_score_}")  # Imprimir el mejor scoregrid.best_score_)

    return grid, x_test, y_test
