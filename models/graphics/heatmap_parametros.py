import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV

def graficar_resultados(grid: GridSearchCV) -> None:
    plt.figure(figsize=(10, 6))

    resultados = pd.DataFrame(grid.cv_results_)

    # Usar solo métricas numéricas para el heatmap
    tabla = resultados.pivot_table(
        values="mean_test_score",
        index="param_knn__n_neighbors",
        columns="param_knn__weights"
    )

    sns.heatmap(tabla, annot=True, cmap="coolwarm", fmt=".3f")

    plt.title("GridSearchCV - KNN (Accuracy)")
    plt.ylabel("n_neighbors")
    plt.xlabel("weights")

    plt.show()
