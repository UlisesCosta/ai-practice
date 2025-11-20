
from cargar_datos import cargar_csv
from model_utils import preparar_y_entrenar_knn
from matriz_confusion import evaluar_modelo
from graphics.heatmap_parametros import graficar_resultados


x,y = cargar_csv("../outputs_csvs/afectacion.csv")

grid, x_test, y_test = preparar_y_entrenar_knn(x,y)


y_pred = evaluar_modelo(grid, x_test, y_test)


graficar_resultados(grid)
